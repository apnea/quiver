FROM python:3.11-slim

# Install dependencies
RUN pip install pandas pyarrow

# Create directory for Plasma socket
RUN mkdir -p /tmp/plasma

# Add script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]