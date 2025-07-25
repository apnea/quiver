FROM python:3.11-slim

RUN pip install pandas pyarrow==12.0.1

COPY flight_server.py /app/flight_server.py
WORKDIR /app

CMD ["python", "flight_server.py"]