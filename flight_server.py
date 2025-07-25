import os
import pandas as pd
import pyarrow as pa
import pyarrow.flight as flight

PARQUET_PATH = os.environ.get("PARQUET_PATH", "/data/example.parquet")

# Load table with error handling
def load_table():
    try:
        if os.path.exists(PARQUET_PATH):
            print(f"Loading parquet file from: {PARQUET_PATH}")
            return pa.Table.from_pandas(pd.read_parquet(PARQUET_PATH))
        else:
            print(f"Parquet file not found at {PARQUET_PATH}, creating sample data")
            # Create sample data if file doesn't exist
            sample_df = pd.DataFrame({
                'id': [1, 2, 3, 4, 5],
                'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
                'value': [10.5, 20.3, 30.1, 40.8, 50.2]
            })
            return pa.Table.from_pandas(sample_df)
    except Exception as e:
        print(f"Error loading data: {e}")
        print("Creating empty sample table")
        sample_df = pd.DataFrame({'error': ['Failed to load data']})
        return pa.Table.from_pandas(sample_df)

TABLE = load_table()

class InMemoryFlightServer(flight.FlightServerBase):
    def __init__(self, location):
        super().__init__(location)
        self.tables = {"default": TABLE}

    def list_flights(self, context, criteria):
        descriptor = flight.FlightDescriptor.for_path("default")
        endpoint = flight.FlightEndpoint(b"default", ["grpc://0.0.0.0:8815"])
        return [flight.FlightInfo(self.tables["default"].schema, descriptor, [endpoint], 
                                self.tables["default"].num_rows, -1)]

    def get_flight_info(self, context, descriptor):
        endpoint = flight.FlightEndpoint(b"default", ["grpc://0.0.0.0:8815"])
        return flight.FlightInfo(self.tables["default"].schema, descriptor, [endpoint], 
                               self.tables["default"].num_rows, -1)

    def do_get(self, context, ticket):
        # ticket should be "default" but let's be flexible
        return flight.RecordBatchStream(self.tables["default"])

    def do_put(self, context, descriptor, reader, writer):
        self.tables["default"] = reader.read_all()

if __name__ == "__main__":
    server = InMemoryFlightServer("grpc://0.0.0.0:8815")
    print(f"Starting Arrow Flight server on grpc://0.0.0.0:8815")
    print(f"Loading data from: {PARQUET_PATH}")
    try:
        server.serve()
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"Server error: {e}")
        raise