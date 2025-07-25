import pyarrow as pa
import pyarrow.flight as flight

client = flight.connect("grpc://localhost:8815")

# 📥 Fetch table from server
info = client.get_flight_info(flight.FlightDescriptor.for_path("default"))
reader = client.do_get(info.endpoints[0].ticket)
table = reader.read_all()

print("Fetched table:")
print(table.to_pandas())

# 📤 Upload new table (overwrite)
new_table = pa.table({"x": [10, 20, 30], "y": ["a", "b", "c"]})
writer, _ = client.do_put(flight.FlightDescriptor.for_path("default"), new_table.schema)
writer.write_table(new_table)
writer.close()

print("Uploaded new table.")