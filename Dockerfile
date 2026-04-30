FROM python:3.13-slim

# 1. นำเข้า uv จาก official image
#COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 2. ติดตั้ง OS dependencies ที่จำเป็นสำหรับ Postgres
RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

# 3. Copy requirements และติดตั้งด้วย uv (ใช้ Cache)
COPY requirements.txt .

#RUN uv install --system --no-cache -r requirements.txt
RUN pip install -r requirements.txt

# 4. Copy Code ส่วนที่เหลือ
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]