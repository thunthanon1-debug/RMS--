import hashlib                     # ใช้เข้ารหัสรหัสผ่าน
import os                          # ใช้ดึงค่าตัวแปรจากระบบ (Environment)
from datetime import datetime, timedelta   # ใช้กำหนดเวลาหมดอายุของ Token
from jose import jwt               # ใช้สร้าง JWT Token
from dotenv import load_dotenv     # ใช้โหลดค่าจากไฟล์ .env

load_dotenv()                      # โหลดค่าตัวแปรในไฟล์ .env มาใช้งาน


# ดึง SECRET_KEY จากไฟล์ .env เพื่อใช้เข้ารหัส JWT
SECRET_KEY = os.getenv("SECRET_KEY")

# Algorithm ที่ใช้เข้ารหัส Token
ALGORITHM = "HS256"

# กำหนดอายุ Token 60 นาที
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ---------------- HASH PASSWORD ----------------
def hash_password(password: str):
    # เข้ารหัส password ด้วย SHA256 ก่อนเก็บใน database
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- VERIFY PASSWORD ----------------
def verify_password(password: str, hashed: str):
    # เข้ารหัส password ที่ผู้ใช้กรอก
    # แล้วเปรียบเทียบกับ password ที่เก็บใน database
    return hashlib.sha256(password.encode()).hexdigest() == hashed


# ---------------- CREATE ACCESS TOKEN ----------------
def create_access_token(data: dict):

    # copy ข้อมูลที่จะเก็บใน token
    to_encode = data.copy()

    # กำหนดเวลาหมดอายุของ token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # เพิ่มข้อมูล exp ลงใน token
    to_encode.update({"exp": expire})

    # สร้าง JWT Token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # ส่ง token กลับไปใช้งาน
    return encoded_jwt