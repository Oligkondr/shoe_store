from pydantic import BaseModel, EmailStr, Field


class AdminCreateRequest(BaseModel):
    email: str
    password: str
    phone: str
    name: str
    surname: str
    patronymic: str
    is_super: bool


class AdminAuthRequest(BaseModel):
    email: str = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")