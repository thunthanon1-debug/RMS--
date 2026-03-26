from sqladmin import ModelView   # ใช้สร้างหน้า Admin สำหรับจัดการข้อมูลใน Database
import models                    # เรียกใช้ Model ที่สร้างไว้ เช่น User, Customer, Menu
from auth import hash_password   # ฟังก์ชันสำหรับเข้ารหัสรหัสผ่านก่อนบันทึกลงฐานข้อมูล


# ---------------- USER ADMIN ----------------
class UserAdmin(ModelView, model=models.User):
    name = "ผู้ใช้"                # ชื่อที่แสดงในหน้า Admin
    name_plural = "ผู้ใช้ทั้งหมด"  # ชื่อที่แสดงในเมนูรวมหลายรายการ

    column_list = [
        models.User.id,           # แสดงรหัสผู้ใช้
        models.User.username,     # แสดงชื่อผู้ใช้
        models.User.role          # แสดงบทบาท เช่น admin / user
    ]

    column_searchable_list = [
        models.User.username      # สามารถค้นหาข้อมูลจาก username ได้
    ]

    column_sortable_list = [
        models.User.id,           # สามารถเรียงข้อมูลตาม id
        models.User.username      # สามารถเรียงข้อมูลตาม username
    ]

    form_columns = [
        models.User.username,     # ฟอร์มสำหรับกรอก username
        models.User.password,     # ฟอร์มสำหรับกรอก password
        models.User.role          # ฟอร์มสำหรับเลือก role
    ]

    async def on_model_change(self, data, model, is_created, request):
        # ฟังก์ชันนี้ทำงานตอนมีการเพิ่มหรือแก้ไขข้อมูล
        if "password" in data and data["password"]:
            model.password = hash_password(data["password"])  
            # เข้ารหัส password ก่อนบันทึกลงฐานข้อมูลเพื่อความปลอดภัย


# ---------------- CUSTOMER ADMIN ----------------
class CustomerAdmin(ModelView, model=models.Customer):
    name = "ลูกค้า"               # ชื่อเมนูในหน้า Admin
    name_plural = "ข้อมูลลูกค้า"

    column_list = [
        models.Customer.id,       # รหัสลูกค้า
        models.Customer.name,     # ชื่อลูกค้า
        models.Customer.phone,    # เบอร์โทรลูกค้า
        models.Customer.address   # ที่อยู่ลูกค้า
    ]

    column_searchable_list = [
        models.Customer.name,     # ค้นหาจากชื่อลูกค้า
        models.Customer.phone     # ค้นหาจากเบอร์โทร
    ]

    column_sortable_list = [
        models.Customer.id,       # เรียงตาม id
        models.Customer.name      # เรียงตามชื่อ
    ]


# ---------------- CATEGORY ADMIN ----------------
class CategoryAdmin(ModelView, model=models.Category):
    name = "หมวดหมู่"
    name_plural = "หมวดหมู่เมนู"

    column_list = [
        models.Category.id,       # รหัสหมวดหมู่
        models.Category.name      # ชื่อหมวดหมู่
    ]

    column_searchable_list = [
        models.Category.name      # ค้นหาจากชื่อหมวดหมู่
    ]

    column_sortable_list = [
        models.Category.id,       # เรียงตาม id
        models.Category.name      # เรียงตามชื่อ
    ]


# ---------------- MENU ADMIN ----------------
class MenuAdmin(ModelView, model=models.Menu):
    name = "เมนูอาหาร"
    name_plural = "รายการเมนู"

    column_list = [
        models.Menu.id,           # รหัสเมนู
        models.Menu.name,         # ชื่อเมนู
        models.Menu.description,  # รายละเอียดเมนู
        models.Menu.price,        # ราคา
        models.Menu.category_id   # หมวดหมู่ของเมนู
    ]

    column_searchable_list = [
        models.Menu.name,         # ค้นหาจากชื่อเมนู
        models.Menu.description   # ค้นหาจากรายละเอียด
    ]

    column_sortable_list = [
        models.Menu.id,           # เรียงตาม id
        models.Menu.name,         # เรียงตามชื่อเมนู
        models.Menu.price,        # เรียงตามราคา
        models.Menu.category_id   # เรียงตามหมวดหมู่
    ]


# ---------------- ORDER ADMIN ----------------
class OrderAdmin(ModelView, model=models.Order):
    name = "ออเดอร์"
    name_plural = "รายการสั่งอาหาร"

    column_list = [
        models.Order.id,          # รหัสออเดอร์
        models.Order.customer_id, # ลูกค้าที่สั่ง
        models.Order.total_price, # ราคารวมของออเดอร์
        models.Order.created_at   # วันที่และเวลาที่สั่ง
    ]

    column_searchable_list = [
        models.Order.customer_id  # ค้นหาออเดอร์จากรหัสลูกค้า
    ]

    column_sortable_list = [
        models.Order.id,          # เรียงตาม id
        models.Order.total_price, # เรียงตามราคารวม
        models.Order.created_at   # เรียงตามวันที่สั่ง
    ]