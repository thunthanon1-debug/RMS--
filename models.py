from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime  # ใช้สร้างคอลัมน์ใน database
from datetime import datetime                                                 # ใช้เก็บวันเวลา
from database import Base                                                     # Base class สำหรับ model


# ---------------- USER TABLE ----------------
class User(Base):
    __tablename__ = "users"   # ชื่อตารางใน database

    id = Column(Integer, primary_key=True)  # รหัสผู้ใช้ (Primary Key)
    username = Column(String)               # ชื่อผู้ใช้
    password = Column(String)               # รหัสผ่าน (ถูกเข้ารหัส)
    role = Column(String)                   # บทบาท เช่น admin หรือ user


# ---------------- CUSTOMER TABLE ----------------
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)  # รหัสลูกค้า
    name = Column(String)                   # ชื่อลูกค้า
    phone = Column(String)                  # เบอร์โทรลูกค้า
    address = Column(String)                # ที่อยู่ลูกค้า


# ---------------- CATEGORY TABLE ----------------
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)  # รหัสหมวดหมู่
    name = Column(String)                   # ชื่อหมวดหมู่เมนู


# ---------------- MENU TABLE ----------------
class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)             # รหัสเมนู
    name = Column(String)                              # ชื่อเมนู
    description = Column(String)                       # รายละเอียดเมนู
    price = Column(Float)                              # ราคา
    category_id = Column(Integer, ForeignKey("categories.id"))  
    # เชื่อมกับตาราง categories


# ---------------- ORDER TABLE ----------------
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)  # รหัสออเดอร์
    customer_id = Column(Integer, ForeignKey("customers.id"))  
    # เชื่อมกับตาราง customers

    total_price = Column(Float)             # ราคารวมของออเดอร์
    created_at = Column(DateTime, default=datetime.utcnow)  
    # วันที่และเวลาที่สร้างออเดอร์


# ---------------- ORDER ITEM TABLE ----------------
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)  # รหัสรายการในออเดอร์
    order_id = Column(Integer)              # รหัสออเดอร์
    menu_id = Column(Integer)               # รหัสเมนู
    quantity = Column(Integer)              # จำนวนที่สั่ง
    price = Column(Float)                   # ราคา