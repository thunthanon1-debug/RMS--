from dotenv import load_dotenv
load_dotenv()   # โหลดค่าตัวแปรจากไฟล์ .env

from fastapi import FastAPI                # ใช้สร้าง Web API
from sqladmin import Admin                 # ใช้สร้าง Admin Panel
from starlette.middleware.sessions import SessionMiddleware  # ใช้จัดการ session login

from database import engine, Base          # เรียกใช้งาน database engine และ base
import models                              # เรียกใช้ models ของระบบ

# เรียกใช้ Admin Views
from admin.admin import (
    UserAdmin,
    CustomerAdmin,
    CategoryAdmin,
    MenuAdmin,
    OrderAdmin
)

from admin_auth import AdminAuth           # ระบบ login สำหรับ admin panel

# เรียกใช้ API Router ต่าง ๆ
from api.menu_api import router as menu_router
from api.order_api import router as order_router
from api.customer_api import router as customer_router
from api.dashboard_api import router as dashoard_router
from api.login_api import router as login_router   # API สำหรับ JWT Login


# สร้าง FastAPI Application
app = FastAPI(
    title="ระบบจัดการร้านอาหาร"
)


# สร้างตารางในฐานข้อมูลจาก models
Base.metadata.create_all(bind=engine)


# เพิ่ม Session Middleware สำหรับ login admin
app.add_middleware(
    SessionMiddleware,
    secret_key="secret123"
)


# ตั้งค่า Authentication สำหรับ Admin Panel
authentication_backend = AdminAuth(secret_key="secret123")


# สร้าง Admin Panel
admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend
)


# เพิ่มเมนูจัดการข้อมูลใน Admin Panel
admin.add_view(UserAdmin)
admin.add_view(CustomerAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(MenuAdmin)
admin.add_view(OrderAdmin)


# เพิ่ม API Routes ของระบบ
app.include_router(menu_router)       # API เมนูอาหาร
app.include_router(order_router)      # API ออเดอร์
app.include_router(customer_router)   # API ลูกค้า
app.include_router(dashoard_router)   # API Dashboard
app.include_router(login_router, prefix="/api")   # API Login แบบ JWT


# API หน้าแรกของระบบ
@app.get("/")
def home():
    return {
        "message": "ยินดีต้อนรับสู่ระบบจัดการร้านอาหาร"
    }

# uvicorn main:app --reload
#http://127.0.0.1:8000/docs
#http://127.0.0.1:8000/admin