from fastapi import APIRouter, Depends, HTTPException  # ใช้สร้าง API และจัดการ error
from sqlalchemy.orm import Session                     # ใช้เชื่อมต่อและจัดการ Database
from database import SessionLocal                      # เรียกใช้งาน Session ของฐานข้อมูล
import models                                          # เรียกใช้ Model เช่น Customer


# สร้าง Router สำหรับจัดการ API ของลูกค้า
router = APIRouter(
    prefix="/customers",   # กำหนด path หลักของ API เช่น /customers
    tags=["Customers"]     # ชื่อหมวดใน Swagger
)


# ฟังก์ชันสำหรับเชื่อมต่อ Database
def get_db():
    db = SessionLocal()   # สร้างการเชื่อมต่อฐานข้อมูล
    try:
        yield db          # ส่ง db ไปใช้งานใน API
    finally:
        db.close()        # ปิดการเชื่อมต่อเมื่อใช้งานเสร็จ


# ---------------- GET ALL CUSTOMERS ----------------
@router.get("/")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()  # ดึงข้อมูลลูกค้าทั้งหมดจากฐานข้อมูล
    return customers                              # ส่งข้อมูลลูกค้ากลับ


# ---------------- GET CUSTOMER BY ID ----------------
@router.get("/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):

    # ค้นหาลูกค้าตาม id
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    # ถ้าไม่พบข้อมูลลูกค้า
    if not customer:
        raise HTTPException(status_code=404, detail="ไม่พบลูกค้า")

    return customer


# ---------------- CREATE CUSTOMER ----------------
@router.post("/")
def create_customer(
    name: str,
    phone: str,
    address: str,
    db: Session = Depends(get_db)
):

    # สร้างลูกค้าใหม่
    new_customer = models.Customer(
        name=name,
        phone=phone,
        address=address
    )

    db.add(new_customer)      # เพิ่มข้อมูลเข้า database
    db.commit()               # บันทึกข้อมูล
    db.refresh(new_customer)  # อัปเดตข้อมูลล่าสุดจาก database

    return {
        "message": "เพิ่มลูกค้าสำเร็จ",
        "customer": new_customer
    }


# ---------------- UPDATE CUSTOMER ----------------
@router.put("/{customer_id}")
def update_customer(
    customer_id: int,
    name: str,
    phone: str,
    address: str,
    db: Session = Depends(get_db)
):

    # ค้นหาลูกค้าตาม id
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    # ถ้าไม่พบข้อมูล
    if not customer:
        raise HTTPException(status_code=404, detail="ไม่พบลูกค้า")

    # แก้ไขข้อมูลลูกค้า
    customer.name = name
    customer.phone = phone
    customer.address = address

    db.commit()  # บันทึกการแก้ไข

    return {
        "message": "แก้ไขข้อมูลลูกค้าสำเร็จ"
    }


# ---------------- DELETE CUSTOMER ----------------
@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):

    # ค้นหาลูกค้า
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    # ถ้าไม่พบข้อมูล
    if not customer:
        raise HTTPException(status_code=404, detail="ไม่พบลูกค้า")

    db.delete(customer)  # ลบข้อมูลลูกค้า
    db.commit()          # บันทึกการลบ

    return {
        "message": "ลบลูกค้าสำเร็จ"
    }


# ---------------- SEARCH CUSTOMER ----------------
@router.get("/search/")
def search_customer(keyword: str, db: Session = Depends(get_db)):

    # ค้นหาลูกค้าจาก keyword ในชื่อ
    customers = db.query(models.Customer).filter(
        models.Customer.name.contains(keyword)
    ).all()

    return customers