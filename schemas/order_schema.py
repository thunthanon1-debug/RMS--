from pydantic import BaseModel
from typing import List


class OrderItemCreate(BaseModel):
    menu_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]


class Order(BaseModel):
    id: int
    customer_id: int

    class Config:
        from_attributes = True