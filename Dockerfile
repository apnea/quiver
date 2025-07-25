FROM python:3.11-slim

WORKDIR /app
COPY flight_server.py .

RUN pip install pandas pyarrow==12.0.1

EXPOSE 8815

CMD ["python3", "flight_server.py"]