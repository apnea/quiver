#!/bin/bash
# Entry point script for the Docker container

# Set default parquet path if not provided
if [ -z "$PARQUET_FILENAME" ]; then
    export PARQUET_FILENAME="EURUSD.parquet"
fi

export PARQUET_PATH="/data/$PARQUET_FILENAME"

echo "Starting Flight server with parquet file: $PARQUET_PATH"

# Check if the file exists
if [ -f "$PARQUET_PATH" ]; then
    echo "Found parquet file: $PARQUET_PATH"
else
    echo "Warning: Parquet file not found: $PARQUET_PATH"
    echo "Available files in /data:"
    ls -la /data/ 2>/dev/null || echo "No files found in /data directory"
fi

# Start the Python server
exec python flight_server.py
