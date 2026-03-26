from fastapi import APIRouter, Depends      # ใช้สร้าง API Router และจัดการ Dependency
from sqlalchemy.orm import Session          # ใช้จัดการการเชื่อมต่อกับฐานข้อมูล
from sqlalchemy import func                 # ใช้ฟังก์ชัน SQL เช่น SUM
from database import SessionLocal           # ใช้สร้าง Session สำหรับเชื่อมต่อ Database
import models                               # เรียกใช้ Model เช่น Order, Customer, Menu


# สร้าง Router สำหรับ API Dashboard
router = APIRouter(
    prefix="/dashboard",    # กำหนด path ของ API เช่น /dashboard
    tags=["Dashboard"]      # ชื่อหมวดใน Swagger
)


# ฟังก์ชันสำหรับเชื่อมต่อ Database
def get_db():
    db = SessionLocal()     # เปิดการเชื่อมต่อฐานข้อมูล
    try:
        yield db            # ส่ง db ไปใช้ใน API
    finally:
        db.close()          # ปิดการเชื่อมต่อเมื่อใช้งานเสร็จ


# ---------------- DASHBOARD API ----------------
@router.get("/")
def get_dashboard(db: Session = Depends(get_db)):

    # คำนวณยอดขายทั้งหมด โดยใช้ SUM รวมราคาของ Order ทั้งหมด
    total_sales = db.query(func.sum(models.Order.total_price)).scalar() or 0

    # นับจำนวนออเดอร์ทั้งหมดในระบบ
    total_orders = db.query(models.Order).count()

    # นับจำนวนลูกค้าทั้งหมด
    total_customers = db.query(models.Customer).count()

    # นับจำนวนเมนูอาหารทั้งหมด
    total_menus = db.query(models.Menu).count()

    # ส่งข้อมูลสรุปกลับไปแสดงใน Dashboard
    return {
        "ยอดขายทั้งหมด": total_sales,
        "จำนวนออเดอร์": total_orders,
        "จำนวนลูกค้า": total_customers,
        "จำนวนเมนู": total_menus
    }