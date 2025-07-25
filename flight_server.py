import os
import pandas as pd
import pyarrow as pa
import pyarrow.flight as flight

PARQUET_PATH = os.environ.get("PARQUET_PATH", "/data/example.parquet")
TABLE = pa.Table.from_pandas(pd.read_parquet(PARQUET_PATH))

class InMemoryFlightServer(flight.FlightServerBase):
    def __init__(self, location):
        super().__init__(location)
        self.tables = {"default": TABLE}

    def list_flights(self, context, criteria):
        return [flight.FlightInfo(TABLE.schema, flight.FlightDescriptor.for_path("default"), [], -1, -1)]

    def get_flight_info(self, context, descriptor):
        return flight.FlightInfo(TABLE.schema, descriptor, [], -1, -1)

    def do_get(self, context, ticket):
        return flight.RecordBatchStream(self.tables["default"])

    def do_put(self, context, descriptor, reader, writer):
        self.tables["default"] = reader.read_all()

server = InMemoryFlightServer("grpc://0.0.0.0:8815")
server.serve()