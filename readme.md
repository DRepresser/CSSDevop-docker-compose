# Resume Hub — Full-Stack DevOps Lab

ระบบ Resume Platform แบบ Full-Stack ที่ประกอบด้วย Django REST API, React Frontend, PostgreSQL, Redis Cache และ Caddy Reverse Proxy พร้อม Load Balancing

## Architecture

```
Browser → Caddy (:80) ─┬─ /api/*    → backend-1 ┐
                        │             backend-2 ├─ Postgres + Redis
                        │             backend-3 ┘
                        └─ /*        → React SPA (static files)
```

## Services

| Service | Image / Build | หน้าที่ |
|---|---|---|
| `caddy` | `caddy:2-alpine` | Reverse Proxy + Static File Server |
| `backend` (×3) | `./backend` | Django REST API (Gunicorn) |
| `db` | `postgres:17-alpine` | ฐานข้อมูล PostgreSQL |
| `redis` | `redis:alpine` | Cache Layer |
| `frontend-build` | `./frontend` | Build React → Volume |
| `migrate` | `./backend` | รัน DB Migration (one-shot) |

## วิธีรัน (Docker Compose)

### 1. Clone Repository

```bash
git clone <repo-url>
cd djrepo
```

### 2. Build และ Start ทุก Services (3 Backend Replicas)

```bash
docker compose up -d --build --scale backend=3
```

### 3. ตรวจสอบสถานะ Services

```bash
docker compose ps
```

ผลลัพธ์ที่ควรเห็น:

```
NAME               STATUS          PORTS
djrepo-backend-1   Up              
djrepo-backend-2   Up              
djrepo-backend-3   Up              
djrepo-caddy-1     Up              0.0.0.0:80->80/tcp
djrepo-db-1        Up (healthy)    5432/tcp
djrepo-redis-1     Up (healthy)    6379/tcp
```

### 4. เติมข้อมูลตัวอย่าง

```bash
# สร้าง Superuser สำหรับ Django Admin
docker compose exec backend python manage.py createsuperuser

# สร้าง Resume ตัวอย่าง (กี่ชุดก็ได้)
docker compose exec backend python manage.py generate_resumes --number 50
```

### 5. เปิดใช้งาน

| URL | คำอธิบาย |
|---|---|
| `http://localhost` | Resume Hub (React Frontend) |
| `http://localhost/api/resumes/` | REST API |
| `http://localhost/admin` | Django Admin |

---

## คำสั่งที่ใช้บ่อย

```bash
# ดู Log แบบ Real-time (พิสูจน์ Load Balancing)
docker compose logs -f backend

# หยุดทุก Services
docker compose down

# หยุดและลบ Volume (ล้างข้อมูลทั้งหมด)
docker compose down -v

# รัน Scale ใหม่ (ไม่ต้อง Build ใหม่)
docker compose up -d --scale backend=3

# เข้า Redis CLI ตรวจสอบ Cache
docker compose exec redis redis-cli -n 1 KEYS "*"
```

---

## การส่งงาน (Project Submission)

### สิ่งที่ต้องส่ง

#### 1. GitHub Repository

Push โค้ดทั้งหมดขึ้น GitHub โดยตรวจสอบว่า repository มีไฟล์ครบดังนี้:

```
djrepo/
├── backend/            ← Django API
├── frontend/           ← React + Vite
├── Caddyfile           ← Reverse Proxy config
├── docker-compose.yml  ← Full stack definition
└── readme.md           ← ไฟล์นี้
```

> **หมายเหตุ**: ไฟล์ `.env` และโฟลเดอร์ที่อยู่ใน `.gitignore` (เช่น `__pycache__`, `node_modules`, `venv`) **ไม่ต้อง** push ขึ้น

```bash
git add .
git commit -m "feat: complete full-stack docker compose lab"
git push
```

---

#### 2. Screenshots ที่ต้องถ่าย

**Screenshot 1 — หน้าเว็บ Frontend แสดง Resume**

เปิด `http://localhost` แล้วถ่าย screenshot หน้าเว็บที่แสดงการ์ด Resume จริงจาก Database

**Screenshot 2 — `docker compose ps`**

รันคำสั่งด้านล่างแล้วถ่าย screenshot ผลลัพธ์ที่แสดง services ครบทุกตัว:

```bash
docker compose ps
```

ต้องเห็น `backend-1`, `backend-2`, `backend-3` พร้อมกัน

**Screenshot 3 — Load Balancing Logs**

รันคำสั่งด้านล่างเพื่อพิสูจน์ว่า Request กระจายไป Backend ทั้ง 3 ตัว:

```bash
# เรียก API หลายครั้ง
for i in 1 2 3 4 5 6; do curl -s http://localhost/api/resumes/ > /dev/null; done

1..6 | ForEach-Object { Invoke-WebRequest -Uri "http://localhost/api/resumes/" -UseBasicParsing | Out-Null }

# ดู Log (ต้องเห็น backend-1, backend-2, backend-3 สลับกัน)
docker compose logs --tail=20 backend
```

ถ่าย screenshot log ที่เห็น `backend-1`, `backend-2`, `backend-3` รับ Request สลับกัน

**Screenshot 4 — Redis Cache**

```bash
docker compose exec redis redis-cli -n 1 KEYS "*"
```

ถ่าย screenshot ที่เห็น key `:1:resume_list` ใน Redis
