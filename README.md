# quiver
## a container of Apache arrows

- the purpose of this project is to provide an in memory data store that provide SOTA read speed for data sets
- can be run as a Flight server in Docker, and clients can connect remotely or locally
- compatible with latest PyArrow
- supports zero-copy, efficient streaming of Arrow tables and RecordBatches

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python3 flight_server.py

# In another terminal, run the client
python3 client.py

# Run tests
python3 test_server.py
```

### Docker Deployment
```bash
# Build and run with docker-compose
docker-compose up --build

# Or build and run manually
docker build -t quiver .
docker run -p 8815:8815 -v ./data:/data quiver
```

## Features
- In-memory Arrow data storage with fast access
- Flight protocol for efficient data transfer
- Sample data generation if no parquet file provided
- Error handling and graceful degradation
- Docker support with volume mounting

## Data Format
Place your parquet files in the `data/` directory. The server will load `/data/example.parquet` by default, or you can specify a custom path with the `PARQUET_PATH` environment variable.

## Fixed Issues
- ✅ Syntax error in flight_server.py
- ✅ Added proper error handling for missing data files
- ✅ Fixed Docker port exposure
- ✅ Corrected docker-compose environment variables
- ✅ Added requirements.txt for local development
- ✅ Enhanced client with better error handling
- ✅ Created sample test data
