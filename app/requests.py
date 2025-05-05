from pydantic import BaseModel, Field


class AdminCreateRequest(BaseModel):
    email: str
    password: str
    phone: str
    name: str
    surname: str
    patronymic: str
    is_super: bool


class ClientCreateRequest(BaseModel):
    email: str
    password: str
    phone: str
    name: str
    surname: str


class AdminAuthRequest(BaseModel):
    email: str = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=6, max_length=12, description="Пароль, от 1 до 12 символов")
