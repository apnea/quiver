import pyarrow as pa
import pyarrow.flight as flight

def main():
    try:
        client = flight.connect("grpc://localhost:8815")
        print("Connected to Flight server")

        # List available flights/tables
        flights = list(client.list_flights())
        print(f"Available tables: {[f.descriptor.path[0].decode() for f in flights]}")

        # 📥 Fetch table from server (using "default" table)
        try:
            info = client.get_flight_info(flight.FlightDescriptor.for_path("default"))
            reader = client.do_get(info.endpoints[0].ticket)
            table = reader.read_all()

            print("Fetched table from 'default':")
            print(table.to_pandas())
        except flight.FlightUnavailableError:
            print("No 'default' table found. Server may be empty.")

        # 📤 Upload new table (overwrite)
        new_table = pa.table({"x": [10, 20, 30], "y": ["a", "b", "c"]})
        writer, _ = client.do_put(flight.FlightDescriptor.for_path("default"), new_table.schema)
        writer.write_table(new_table)
        writer.close()

        print("Uploaded new table to 'default'.")
        
    except flight.FlightServerError as e:
        print(f"Flight server error: {e}")
    except ConnectionError as e:
        print(f"Connection error: {e}")
        print("Make sure the Flight server is running on localhost:8815")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()