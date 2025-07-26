#!/usr/bin/env python3
"""
Test script to verify the Arrow Flight server works correctly
"""
import subprocess
import time
import sys
import os
import pyarrow.flight as flight

def test_server():
    print("Starting Flight server test...")
    
    # Set environment variable to load test data
    env = os.environ.copy()
    env['PARQUET_PATH'] = 'data/EURUSD.parquet'
    
    # Start the server in background
    server_process = subprocess.Popen([sys.executable, "flight_server.py"], env=env)
    
    try:
        # Give server time to start
        time.sleep(3)
        
        # Test connection
        client = flight.connect("grpc://localhost:8815")
        print("✅ Successfully connected to server")
        
        # List available tables
        flights = list(client.list_flights())
        available_tables = [f.descriptor.path[0].decode() for f in flights]
        print(f"✅ Available tables: {available_tables}")
        
        # Test data retrieval
        info = client.get_flight_info(flight.FlightDescriptor.for_path("default"))
        ticket = flight.Ticket("default".encode())
        reader = client.do_get(ticket)
        table = reader.read_all()
        
        print(f"✅ Retrieved table with {len(table)} rows and {len(table.schema)} columns")
        print("Schema:", table.schema)
        print("Sample data:")
        print(table.to_pandas().head())
        
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        # Clean up
        server_process.terminate()
        server_process.wait()
        print("Server stopped")
    
    return True

if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)
