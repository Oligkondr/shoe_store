from pydantic import BaseModel


class AdminCreateRequest(BaseModel):
    email: str
    password: str
    phone: str
    name: str
    surname: str
    patronymic: str
    is_super: bool


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
