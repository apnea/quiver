#!/bin/bash
set -e

# Start Plasma store in the background
plasma_store -m 4000000000 -s /tmp/plasma/store &
PLASMA_PID=$!

# Wait for the socket
while [ ! -e /tmp/plasma/store ]; do
  echo "Waiting for Plasma socket..."
  sleep 1
done

# Check if PARQUET_PATH is set and file exists
if [[ -n "$PARQUET_PATH" && -f "$PARQUET_PATH" ]]; then
  echo "Loading Parquet file: $PARQUET_PATH"

  python3 - <<EOF
import pyarrow as pa
import pyarrow.plasma as plasma
import pandas as pd
import os

parquet_path = os.environ["PARQUET_PATH"]
df = pd.read_parquet(parquet_path)

client = plasma.connect("/tmp/plasma/store")

# Convert and store as Arrow buffer
batch = pa.RecordBatch.from_pandas(df)
buf = pa.ipc.serialize_record_batch(batch).to_buffer()
object_id = plasma.ObjectID.from_random()

client.create_and_seal(object_id, buf)
print(f"Loaded DataFrame from '{parquet_path}' into Plasma with ObjectID: {object_id.hex()}")
EOF

else
  echo "No Parquet file specified or file not found at \$PARQUET_PATH."
fi

# Keep the container alive
wait $PLASMA_PID