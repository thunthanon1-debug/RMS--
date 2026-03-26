from fastapi import APIRouter, Depends, HTTPException   # ใช้สร้าง API และจัดการ error
from sqlalchemy.orm import Session                      # ใช้จัดการการเชื่อมต่อฐานข้อมูล
from database import SessionLocal                       # ใช้สร้าง session สำหรับ database
import models                                           # เรียกใช้ Model เช่น Order
from datetime import datetime                           # ใช้เก็บวันเวลาที่สร้างออเดอร์


# สร้าง Router สำหรับ API ออเดอร์
router = APIRouter(
    prefix="/orders",     # path หลักของ API เช่น /orders
    tags=["Orders"]       # หมวดที่แสดงใน Swagger
)


# ฟังก์ชันสำหรับเชื่อมต่อฐานข้อมูล
def get_db():
    db = SessionLocal()     # เปิดการเชื่อมต่อฐานข้อมูล
    try:
        yield db            # ส่ง db ไปใช้ใน API
    finally:
        db.close()          # ปิดการเชื่อมต่อเมื่อเสร็จ


# ---------------- GET ALL ORDERS ----------------
@router.get("/")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()   # ดึงข้อมูลออเดอร์ทั้งหมด
    return orders


# ---------------- GET ORDER BY ID ----------------
@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):

    # ค้นหาออเดอร์ตาม id
    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    # ถ้าไม่พบออเดอร์
    if not order:
        raise HTTPException(status_code=404, detail="ไม่พบออเดอร์")

    return order


# ---------------- CREATE ORDER ----------------
@router.post("/")
def create_order(
    customer_id: int,
    total_price: float,
    db: Session = Depends(get_db)
):

    # สร้างออเดอร์ใหม่
    new_order = models.Order(
        customer_id=customer_id,
        total_price=total_price,
        created_at=datetime.now()   # บันทึกวันเวลาที่สร้างออเดอร์
    )

    db.add(new_order)        # เพิ่มข้อมูลลง database
    db.commit()              # บันทึกข้อมูล
    db.refresh(new_order)    # อัปเดตข้อมูลล่าสุด

    return {
        "message": "สร้างออเดอร์สำเร็จ",
        "order": new_order
    }


# ---------------- DELETE ORDER ----------------
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):

    # ค้นหาออเดอร์
    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    # ถ้าไม่พบข้อมูล
    if not order:
        raise HTTPException(status_code=404, detail="ไม่พบออเดอร์")

    db.delete(order)   # ลบออเดอร์
    db.commit()        # บันทึกการลบ

    return {
        "message": "ลบออเดอร์สำเร็จ"
    }


# ---------------- GET ORDERS BY CUSTOMER ----------------
@router.get("/customer/{customer_id}")
def get_customer_orders(customer_id: int, db: Session = Depends(get_db)):

    # ดึงออเดอร์ทั้งหมดของลูกค้าคนนั้น
    orders = db.query(models.Order).filter(
        models.Order.customer_id == customer_id
    ).all()

    return orders