FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install yfinance flask prometheus_client
CMD ["python", "app.py"]