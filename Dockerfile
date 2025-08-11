FROM python:3.10-slim

# نصب ابزارهای لازم
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config && \
    pip install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# کپی فایل requirements.txt
COPY requirements.txt /app/

# نصب پکیج‌ها
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . /app/

# دستور اجرای پیش‌فرض
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
