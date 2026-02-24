FROM python:3.13-slim

# ติดตั้ง OS dependencies ที่จำเป็นสำหรับ Postgres
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements และติดตั้ง
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run with Gunicorn
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]