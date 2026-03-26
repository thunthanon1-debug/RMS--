from sqladmin.authentication import AuthenticationBackend   # ใช้สร้างระบบ Authentication สำหรับ Admin
from sqlalchemy.orm import Session                           # ใช้เชื่อมต่อฐานข้อมูล
from database import SessionLocal                            # เรียกใช้ Session ของ database
import models                                                # เรียกใช้ Model เช่น User
from auth import verify_password                             # ฟังก์ชันตรวจสอบรหัสผ่าน


# สร้างระบบ Authentication สำหรับ Admin
class AdminAuth(AuthenticationBackend):

    async def login(self, request):
        # รับข้อมูลจากฟอร์ม login
        form = await request.form()

        username = form.get("username")   # รับค่า username
        password = form.get("password")   # รับค่า password

        db: Session = SessionLocal()      # เชื่อมต่อ database

        # ค้นหาผู้ใช้จาก username
        user = db.query(models.User).filter(
            models.User.username == username
        ).first()

        # ถ้าไม่พบผู้ใช้
        if not user:
            return False

        # ตรวจสอบ password
        if not verify_password(password, user.password):
            return False

        # ถ้าถูกต้อง ให้สร้าง session login
        request.session.update({"token": user.username})

        return True


    async def logout(self, request):
        # ลบ session เมื่อ logout
        request.session.clear()
        return True


    async def authenticate(self, request):
        # ตรวจสอบว่ามี session login อยู่หรือไม่
        token = request.session.get("token")

        if not token:
            return False

        # ถ้ามี session แสดงว่ายัง login อยู่
        return True