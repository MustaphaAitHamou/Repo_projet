FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libssl-dev \
      libffi-dev \
      python3-dev \
      default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests

ENTRYPOINT ["sh", "-c"]
CMD ["until mysqladmin ping -h mysql --silent; do echo '⏳ Waiting for MySQL…'; sleep 2; done && exec gunicorn app.routes:app --bind 0.0.0.0:5000"]