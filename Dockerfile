FROM python:3.10-slim

# نصب ابزارهای لازم
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config && \
    pip install --upgrade pip && \
    pip install pipenv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Pipfile Pipfile.lock* /app/

RUN pipenv install --system --skip-lock

COPY . /app/

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
