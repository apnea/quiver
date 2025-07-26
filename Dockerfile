FROM python:3.11-slim

# Install system updates and security patches
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m appuser
USER appuser

# Set working directory
WORKDIR /home/appuser/app

# Copy requirements and install dependencies
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY --chown=appuser:appuser . .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Set entrypoint or command as needed
ENTRYPOINT ["./entrypoint.sh"]