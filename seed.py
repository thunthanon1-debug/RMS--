from database import SessionLocal, engine, Base
import models
from auth import hash_password
from datetime import datetime, timedelta
import random

# สร้างตารางใน database
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ---------------- USERS ----------------
users = [
    models.User(username="admin", password=hash_password("1234"), role="admin"),
    models.User(username="manager", password=hash_password("manager"), role="admin"),
    models.User(username="staff1", password=hash_password("staff1"), role="user"),
    models.User(username="staff2", password=hash_password("staff2"), role="user")
]

db.add_all(users)
db.commit()

# ---------------- CATEGORIES ----------------
categories = [
    models.Category(name="อาหารจานหลัก"),
    models.Category(name="เครื่องดื่ม"),
    models.Category(name="ของหวาน")
]

db.add_all(categories)
db.commit()

# ---------------- CUSTOMERS ----------------
customers = []

names = [
"สมชาย","สมหญิง","วิชัย","กานต์","ณัฐพล","อนันต์","ปวีณา","วีระ","สายใจ","เกรียงไกร",
"ธันวา","นภา","จิรายุ","วรรณา","อาทิตย์","พงศ์เทพ","กิตติ","มนัส","ปกรณ์","อารีย์",
"ศิริพร","พัชรา","ก้องภพ","ธีรภัทร์","รัตนา","ศุภชัย","ชลธิชา","อรุณ","ดวงใจ","ภัทร"
]

for i in range(30):
    customers.append(
        models.Customer(
            name=names[i] + " ลูกค้า",
            phone=f"08{random.randint(10000000,99999999)}",
            address="กรุงเทพ"
        )
    )

db.add_all(customers)
db.commit()

# ---------------- MENUS ----------------
menus = [
    models.Menu(name="พิซซ่า", description="พิซซ่าชีส", price=199, category_id=1),
    models.Menu(name="เบอร์เกอร์", description="เบอร์เกอร์เนื้อ", price=129, category_id=1),
    models.Menu(name="ข้าวผัดหมู", description="ข้าวผัดหมูสูตรร้าน", price=79, category_id=1),
    models.Menu(name="ข้าวกระเพรา", description="กระเพราหมู", price=75, category_id=1),
    models.Menu(name="สปาเก็ตตี้", description="สปาเก็ตตี้ซอสแดง", price=159, category_id=1),
    models.Menu(name="สเต็กหมู", description="สเต็กหมูพริกไทยดำ", price=189, category_id=1),
    models.Menu(name="ข้าวมันไก่", description="ข้าวมันไก่สูตรร้าน", price=60, category_id=1),
    models.Menu(name="ผัดไทย", description="ผัดไทยกุ้งสด", price=90, category_id=1),

    models.Menu(name="โค้ก", description="เครื่องดื่มเย็น", price=35, category_id=2),
    models.Menu(name="ชาเย็น", description="ชาไทยเย็น", price=40, category_id=2),
    models.Menu(name="กาแฟ", description="กาแฟดำ", price=50, category_id=2),
    models.Menu(name="น้ำส้ม", description="น้ำส้มคั้นสด", price=45, category_id=2),
    models.Menu(name="ชาเขียว", description="ชาเขียวเย็น", price=50, category_id=2),
    models.Menu(name="น้ำมะนาว", description="น้ำมะนาวสด", price=45, category_id=2),

    models.Menu(name="ไอศกรีม", description="ไอศกรีมวานิลลา", price=59, category_id=3),
    models.Menu(name="เค้กช็อกโกแลต", description="เค้กช็อกโกแลต", price=89, category_id=3),
    models.Menu(name="บราวนี่", description="บราวนี่ช็อกโกแลต", price=79, category_id=3),
    models.Menu(name="แพนเค้ก", description="แพนเค้กน้ำผึ้ง", price=99, category_id=3),
    models.Menu(name="เครป", description="เครปหวาน", price=69, category_id=3),
    models.Menu(name="โดนัท", description="โดนัทช็อกโกแลต", price=49, category_id=3)
]

db.add_all(menus)
db.commit()

# ---------------- ORDERS ----------------
orders = []

for day in range(10):
    for i in range(12):
        order = models.Order(
            customer_id=random.randint(1, 30),
            total_price=0,
            created_at=datetime.now() - timedelta(days=day)
        )
        orders.append(order)

db.add_all(orders)
db.commit()

# ---------------- ORDER ITEMS ----------------
order_items = []

for order in orders:

    total_price = 0

    # สุ่มจำนวนเมนูในออเดอร์
    for i in range(random.randint(1,3)):

        menu = random.choice(menus)
        quantity = random.randint(1,3)

        price = menu.price * quantity
        total_price += price

        order_items.append(
            models.OrderItem(
                order_id=order.id,
                menu_id=menu.id,
                quantity=quantity,
                price=price
            )
        )

    order.total_price = total_price

db.add_all(order_items)
db.commit()

print("Seed Data สำเร็จ")
print("Users:", len(users))
print("Customers:", len(customers))
print("Menus:", len(menus))
print("Orders:", len(orders))
print("OrderItems:", len(order_items))