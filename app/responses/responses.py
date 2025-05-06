from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    token: str


class ClientRegisterResponse(BaseModel):
    email: str
    phone: str
    name: str
    surname: str
    account: int

class ClientDepositResponse(BaseModel):
    email: str
    phone: str
    name: str
    surname: str
    account: int


class UserRegisterResponse(BaseModel):
    success: bool


class ClientProductResponse(BaseModel):
    success: bool


class ClientPayResponse(BaseModel):
    success: bool
