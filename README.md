# quiver
- An Apache Arrow Flight Server

Quiver provides a simple, containerized in-memory data service using Apache Arrow Flight. It allows clients to efficiently upload (`do_put`) and download (`do_get`) Arrow data tables over gRPC.

## Features

-   **High-Performance I/O**: Built on Arrow Flight for fast, network-efficient data transfer.
-   **In-Memory Cache**: Holds Arrow Tables in memory for low-latency access.
-   **Dockerized**: Easy to deploy and run using Docker and Docker Compose.
-   **Initial Data Loading**: Can automatically load a Parquet file into memory on startup.

## Getting Started

### Prerequisites

-   Docker and Docker Compose

### Running the Server

1.  **Place your data:** Create a `data` directory in the project root and place your Parquet files inside it (e.g., `data/example.parquet`, `data/EURUSD.parquet`, `data/other_data.parquet`).

2.  **Build and run the container:**

    You can run it with the default file (`example.parquet`):
    ```bash
    docker compose up --build
    ```

    Or, you can specify a different file at runtime by setting the `PARQUET_FILENAME` environment variable:
    ```bash
    PARQUET_FILENAME=EURUSD.parquet docker compose up --build
    ```
    
    The server will start, load the initial data, and listen on port `8815`. The data will be accessible both by its filename (without extension) and as "default" for backward compatibility.

### Using the Python Client

You can use the provided `client.py` to interact with the server. Ensure you have `pyarrow` installed in your local environment (`pip install pyarrow`).

The client demonstrates how to:
-   Fetch a table from the server.
-   Upload a new table to the server.

```bash
python3 client.py
```

The client is configured to connect to `localhost:8815` and interact with a table named `default`. You can modify it to use different table names (paths).
