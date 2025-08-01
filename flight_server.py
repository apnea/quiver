import os
import signal
import threading
import sys
import pyarrow.parquet as pq
import pyarrow.flight as flight
import time

# Ensure stdout/stderr are unbuffered for Docker logs
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

def log_message(message):
    """Print message with explicit flush for Docker logs"""
    print(message, flush=True)

class InMemoryFlightServer(flight.FlightServerBase):
    def __init__(self, host="0.0.0.0", port=8815, initial_parquet_path=None):
        location = f"grpc://{host}:{port}"
        super().__init__(location)
        self._location = location
        self._tables = {}
        self._lock = threading.Lock()

        if initial_parquet_path and os.path.exists(initial_parquet_path):
            log_message(f"Loading initial data from {initial_parquet_path}")
            try:
                start_time = time.time()
                table = pq.read_table(initial_parquet_path)
                end_time = time.time()
                transfer_time = end_time - start_time
                
                # Use the filename without extension as the table name
                table_name = os.path.splitext(os.path.basename(initial_parquet_path))[0]
                self._tables[table_name] = table
                # Also store as "default" for backward compatibility
                self._tables["default"] = table
                log_message(f"Loaded table '{table_name}' with {table.num_rows} rows and {table.num_columns} columns in {transfer_time:.3f} seconds for a total of {table.nbytes / (1024 * 1024):.2f} MB.")
                log_message(f"Table is accessible as both '{table_name}' and 'default'")
            except Exception as e:
                log_message(f"Error loading initial Parquet file: {e}")
        else:
            log_message("No initial Parquet file found or specified. Starting with an empty server.")

    def list_flights(self, context, criteria):
        with self._lock:
            for name, table in self._tables.items():
                descriptor = flight.FlightDescriptor.for_path(name)
                yield flight.FlightInfo(table.schema, descriptor, [], table.num_rows, -1)

    def get_flight_info(self, context, descriptor):
        path = descriptor.path[0].decode('utf-8')
        with self._lock:
            if path in self._tables:
                table = self._tables[path]
                return flight.FlightInfo(table.schema, descriptor, [], table.num_rows, -1)
        raise flight.FlightUnavailableError(f"Unknown table: {path}")

    def do_get(self, context, ticket):
        path = ticket.ticket.decode('utf-8')
        with self._lock:
            if path in self._tables:
                return flight.RecordBatchStream(self._tables[path])
        raise flight.FlightUnavailableError(f"Unknown table: {path}")

    def do_put(self, context, descriptor, reader, writer):
        path = descriptor.path[0].decode('utf-8')
        table = reader.read_all()
        with self._lock:
            self._tables[path] = table
        log_message(f"Stored table '{path}' with {table.num_rows} rows.")

    def serve(self):
        log_message(f"Starting Flight server at {self._location}")
        super().serve()

    def shutdown(self):
        log_message("Shutting down Flight server...")
        super().shutdown()

def main():
    parquet_path = os.environ.get("PARQUET_PATH")
    server = InMemoryFlightServer(initial_parquet_path=parquet_path)

    def handle_shutdown(signum, frame):
        server.shutdown()

    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    server.serve()

if __name__ == "__main__":
    main()