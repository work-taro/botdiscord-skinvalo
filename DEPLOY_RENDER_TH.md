# ☁️ วิธีเอาบอทขึ้น Render (ฟรี รันตลอด 24 ชม.)

> โหมดนี้ = Render Free Web Service + keep-alive + UptimeRobot
> ⚠️ ข้อจำกัด: ทุกครั้งที่ service restart/deploy ใหม่ ข้อมูลล็อกอิน (`data/users.json`) จะหาย → เพื่อนต้อง `/cookies` ใหม่ (ยอมรับได้ตามที่คุยกัน)

ไฟล์ที่จำเป็นเตรียมไว้ให้แล้ว: `requirements.txt`, `keep_alive.py`, `render.yaml`, `Dockerfile`, `main.py` (เรียก keep_alive)

---

## ขั้นที่ 1 — push โปรเจกต์ขึ้น GitHub ของคุณเอง

repo ตอนนี้ชี้ไปที่ของ staciax (ต้นฉบับ) ต้องสร้าง repo ของตัวเอง

1. ไปสร้าง repo เปล่าใหม่ที่ https://github.com/new (เช่นชื่อ `my-valorant-bot`) — **ตั้งเป็น Private** ก็ได้
2. ในโฟลเดอร์โปรเจกต์ รันคำสั่ง (เปลี่ยน URL เป็นของคุณ):

```powershell
git remote remove origin
git remote add origin https://github.com/<your-username>/my-valorant-bot.git
git add .
git commit -m "deploy: setup for Render"
git branch -M main
git push -u origin main
```

> ✅ `.env` และ `data/*.json` ถูก `.gitignore` ไว้แล้ว → token กับข้อมูลล็อกอิน **จะไม่ถูก push** ปลอดภัย

---

## ขั้นที่ 2 — สร้าง Web Service บน Render

1. สมัคร/ล็อกอิน https://render.com (ใช้ GitHub login ได้)
2. กด **New +** → **Web Service**
3. เชื่อม GitHub แล้วเลือก repo `my-valorant-bot`
4. ตั้งค่า (ถ้า Render อ่าน `render.yaml` เจอ จะเติมให้อัตโนมัติ):
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
   - **Instance Type:** **Free**

---

## ขั้นที่ 3 — ใส่ค่า Environment Variables

ในหน้าตั้งค่า service → แท็บ **Environment** → เพิ่ม 2 ตัว:

| Key | Value |
|-----|-------|
| `DISCORD_TOKEN` | token ของบอท |
| `OWNER_ID` | Discord ID ของคุณ |

> อย่าลืม! ค่าพวกนี้ใส่ในเว็บ Render เท่านั้น ไม่ต้องใส่ในโค้ด

กด **Create Web Service** → Render จะ build + deploy (รอ ~2-3 นาที)
ดูที่แท็บ **Logs** ถ้าเห็น `BOT IS READY !` = สำเร็จ 🎉

---

## ขั้นที่ 4 — กันบอทหลับ (สำคัญมาก!)

Render free จะ **หลับหลังไม่มีคนเข้า 15 นาที** ต้องมีตัวคอย ping:

1. คัดลอก URL ของ service (เช่น `https://valorant-discord-bot-xxxx.onrender.com`)
2. ไปที่ https://uptimerobot.com สมัครฟรี
3. **Add New Monitor**:
   - Monitor Type: **HTTP(s)**
   - URL: วาง URL ของ Render
   - Monitoring Interval: **5 minutes**
4. Save

UptimeRobot จะ ping ทุก 5 นาที → บอทไม่หลับ ✅

---

## 🔄 เวลาแก้โค้ดแล้วอัปเดต

แค่ push ขึ้น GitHub Render จะ deploy ใหม่ให้อัตโนมัติ:

```powershell
git add .
git commit -m "update"
git push
```

---

## ❓ ปัญหาที่อาจเจอ

| อาการ | สาเหตุ / วิธีแก้ |
|-------|------------------|
| Logs ขึ้น `Port scan timeout` | keep_alive ไม่ทำงาน — เช็คว่า `main.py` เรียก `keep_alive()` และมี `keep_alive.py` |
| บอทออนไลน์แล้วหายหลัง 15 นาที | ยังไม่ได้ตั้ง UptimeRobot (ขั้นที่ 4) |
| เพื่อนล็อกอินค้างไว้แล้วหลุดหมด | service restart → `data/users.json` หาย (ข้อจำกัดของ free tier ตามที่ทราบ) |
| build fail เรื่อง Python version | เช็คว่ามีไฟล์ `.python-version` (=3.12) หรือ env `PYTHON_VERSION=3.12.7` |
