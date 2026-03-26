from pydantic import BaseModel


class MenuCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: int


class Menu(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int

    class Config:
        from_attributes = True