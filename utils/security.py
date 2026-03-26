import hashlib                     # ใช้เข้ารหัสรหัสผ่าน
import os                          # ใช้ดึงค่า Environment Variable
from datetime import datetime, timedelta   # ใช้กำหนดเวลา Token หมดอายุ
from jose import jwt               # ใช้สร้าง JWT Token สำหรับ Authentication


SECRET_KEY = os.getenv("SECRET_KEY")   # ดึง SECRET_KEY จาก environment เพื่อใช้เข้ารหัส Token
ALGORITHM = "HS256"                    # Algorithm ที่ใช้ในการเข้ารหัส JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 60       # กำหนดอายุ Token = 60 นาที


# ---------------- HASH PASSWORD ----------------
def hash_password(password: str):
    # เข้ารหัส password ด้วย SHA256 ก่อนเก็บลงฐานข้อมูล
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- VERIFY PASSWORD ----------------
def verify_password(password: str, hashed: str):
    # เข้ารหัส password ที่ผู้ใช้กรอก แล้วเปรียบเทียบกับค่าที่อยู่ใน database
    return hashlib.sha256(password.encode()).hexdigest() == hashed


# ---------------- CREATE ACCESS TOKEN ----------------
def create_access_token(data: dict):

    # copy ข้อมูลที่ต้องการใส่ใน token
    to_encode = data.copy()

    # กำหนดเวลาหมดอายุของ token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # เพิ่มข้อมูล exp ลงใน token
    to_encode.update({"exp": expire})

    # สร้าง JWT Token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # ส่ง token กลับ
    return encoded_jwt