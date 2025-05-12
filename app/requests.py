from pydantic import BaseModel, Field


class AdminCreateRequest(BaseModel):
    email: str = Field(..., description="Электронная почта")
    password: str = Field(..., description="Пароль")
    phone: str = Field(..., description="Номер телефона")
    name: str = Field(..., description="Имя")
    surname: str = Field(..., description="Фамилия")
    patronymic: str = Field(..., description="Отчество")
    is_super: bool = Field(..., description="Является ли админ супером")


class ClientCreateRequest(BaseModel):
    email: str = Field(..., description="Электронная почта")
    password: str = Field(..., description="Пароль")
    phone: str = Field(..., description="Номер телефона")
    name: str = Field(..., description="Имя")
    surname: str = Field(..., description="Фамилия")


class ClientUpdateRequest(BaseModel):
    email: str = Field(..., description="Электронная почта")
    phone: str = Field(..., description="Номер телефона")
    name: str = Field(..., description="Имя")
    surname: str = Field(..., description="Фамилия")


class UserAuthRequest(BaseModel):
    email: str = Field(..., description="Электронная почта")
    password: str = Field(..., description="Пароль")


class ClientProductRequest(BaseModel):
    id: int = Field(..., description="Id product_size")
    quantity: int = Field(..., description="Кол-во продукта")


class ClientDepositRequest(BaseModel):
    amount: int = Field(..., description="Сумма пополнения")


class NewQuantityRequest(BaseModel):
    quantity: int = Field(..., description="Новое кол-во товара")
