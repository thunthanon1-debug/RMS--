from pydantic import BaseModel

class CustomerCreate(BaseModel):
    name: str
    phone: str
    address: str

class Customer(BaseModel):
    id: int
    name: str
    phone: str
    address: str

    class Cobfig:
        from_attributee = True
        