content = """

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

# ดู Log (ต้องเห็น backend-1, backend-2, backend-3 สลับกัน)
docker compose logs --tail=20 backend
```

ถ่าย screenshot log ที่เห็น `backend-1`, `backend-2`, `backend-3` รับ Request สลับกัน

**Screenshot 4 — Redis Cache**

```bash
docker compose exec redis redis-cli -n 1 KEYS "*"
```

ถ่าย screenshot ที่เห็น key `:1:resume_list` ใน Redis
"""

with open(r"D:\\Doc\\Y4-2\\DevOps\\djrepo\\readme.md", "a", encoding="utf-8") as f:
    f.write(content)
print("Done")
