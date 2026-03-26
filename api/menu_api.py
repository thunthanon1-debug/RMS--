from fastapi import APIRouter, Depends, HTTPException   # ใช้สร้าง API และจัดการ error
from sqlalchemy.orm import Session                      # ใช้จัดการการเชื่อมต่อฐานข้อมูล
from database import SessionLocal                       # ใช้สร้าง session ของ database
import models                                           # เรียกใช้ model เช่น Menu


# สร้าง Router สำหรับ API เมนูอาหาร
router = APIRouter(
    prefix="/menus",     # path หลักของ API เช่น /menus
    tags=["Menus"]       # ชื่อหมวดที่แสดงใน Swagger
)


# ฟังก์ชันสำหรับเชื่อมต่อ Database
def get_db():
    db = SessionLocal()     # เปิดการเชื่อมต่อฐานข้อมูล
    try:
        yield db            # ส่ง db ไปใช้งานใน API
    finally:
        db.close()          # ปิดการเชื่อมต่อเมื่อเสร็จ


# ---------------- GET ALL MENUS ----------------
@router.get("/")
def get_menus(db: Session = Depends(get_db)):
    menus = db.query(models.Menu).all()   # ดึงข้อมูลเมนูทั้งหมดจาก database
    return menus                          # ส่งข้อมูลเมนูกลับ


# ---------------- SEARCH MENU ----------------
@router.get("/search")
def search_menu(keyword: str, db: Session = Depends(get_db)):
    menus = db.query(models.Menu).filter(
        models.Menu.name.contains(keyword)  # ค้นหาเมนูจาก keyword ในชื่อ
    ).all()
    return menus


# ---------------- GET MENU BY ID ----------------
@router.get("/{menu_id}")
def get_menu(menu_id: int, db: Session = Depends(get_db)):

    # ค้นหาเมนูตาม id
    menu = db.query(models.Menu).filter(
        models.Menu.id == menu_id
    ).first()

    # ถ้าไม่พบเมนู
    if not menu:
        raise HTTPException(status_code=404, detail="ไม่พบเมนู")

    return menu


# ---------------- CREATE MENU ----------------
@router.post("/")
def create_menu(
    name: str,
    description: str,
    price: float,
    category_id: int,
    db: Session = Depends(get_db)
):

    # สร้างเมนูใหม่
    new_menu = models.Menu(
        name=name,
        description=description,
        price=price,
        category_id=category_id
    )

    db.add(new_menu)        # เพิ่มข้อมูลลง database
    db.commit()             # บันทึกข้อมูล
    db.refresh(new_menu)    # อัปเดตข้อมูลล่าสุดจาก database

    return {
        "message": "เพิ่มเมนูสำเร็จ",
        "menu": new_menu
    }


# ---------------- UPDATE MENU ----------------
@router.put("/{menu_id}")
def update_menu(
    menu_id: int,
    name: str,
    description: str,
    price: float,
    category_id: int,
    db: Session = Depends(get_db)
):

    # ค้นหาเมนูตาม id
    menu = db.query(models.Menu).filter(
        models.Menu.id == menu_id
    ).first()

    # ถ้าไม่พบเมนู
    if not menu:
        raise HTTPException(status_code=404, detail="ไม่พบเมนู")

    # แก้ไขข้อมูลเมนู
    menu.name = name
    menu.description = description
    menu.price = price
    menu.category_id = category_id

    db.commit()   # บันทึกการแก้ไข

    return {
        "message": "แก้ไขเมนูสำเร็จ"
    }


# ---------------- DELETE MENU ----------------
@router.delete("/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):

    # ค้นหาเมนูตาม id
    menu = db.query(models.Menu).filter(
        models.Menu.id == menu_id
    ).first()

    # ถ้าไม่พบเมนู
    if not menu:
        raise HTTPException(status_code=404, detail="ไม่พบเมนู")

    db.delete(menu)   # ลบเมนู
    db.commit()       # บันทึกการลบ

    return {
        "message": "ลบเมนูสำเร็จ"
    }