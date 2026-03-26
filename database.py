from sqlalchemy import create_engine          # ใช้สร้างการเชื่อมต่อกับฐานข้อมูล
from sqlalchemy.orm import sessionmaker, declarative_base  # ใช้สร้าง session และ base model


# กำหนดตำแหน่งฐานข้อมูล (SQLite)
DATABASE_URL = "sqlite:///./restaurant.db"


# สร้าง engine สำหรับเชื่อมต่อ database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  
    # ใช้กับ SQLite เพื่อให้หลาย request ใช้งาน database ได้
)


# สร้าง session สำหรับใช้ query database
SessionLocal = sessionmaker(bind=engine)


# สร้าง Base class สำหรับ model ทุกตัวในระบบ
Base = declarative_base()