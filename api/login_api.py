from fastapi import APIRouter, Depends, HTTPException   # ใช้สร้าง API และจัดการ error
from sqlalchemy.orm import Session                      # ใช้จัดการการเชื่อมต่อฐานข้อมูล
from database import SessionLocal                       # เรียกใช้ Session ของ database
import models                                           # เรียกใช้ Model เช่น User
from auth import verify_password, create_access_token   # ฟังก์ชันตรวจสอบรหัสผ่าน และสร้าง Token


# สร้าง Router สำหรับ API
router = APIRouter()


# ฟังก์ชันสำหรับเชื่อมต่อฐานข้อมูล
def get_db():
    db = SessionLocal()     # เปิดการเชื่อมต่อฐานข้อมูล
    try:
        yield db            # ส่ง db ไปใช้ใน API
    finally:
        db.close()          # ปิดการเชื่อมต่อเมื่อใช้งานเสร็จ


# ---------------- LOGIN API ----------------
@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):

    # ค้นหาผู้ใช้จาก username
    user = db.query(models.User).filter(models.User.username == username).first()

    # ถ้าไม่พบ username
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")

    # ตรวจสอบรหัสผ่าน โดยใช้ฟังก์ชัน verify_password
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    # สร้าง JWT Token สำหรับการยืนยันตัวตน
    token = create_access_token({
        "sub": user.username
    })

    # ส่ง token กลับไปให้ผู้ใช้
    return {
        "access_token": token,
        "token_type": "bearer"
    }