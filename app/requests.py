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


class ClientUpdateRequest(BaseModel):
    email: str
    phone: str
    name: str
    surname: str


class UserAuthRequest(BaseModel):
    email: str = Field(..., description="Электронная почта")
    password: str = Field(..., description="Пароль")


class ClientProductRequest(BaseModel):
    id: int
    quantity: int


class ClientDepositRequest(BaseModel):
    amount: int


class ClientQuantityRequest(BaseModel):
    quantity: int
