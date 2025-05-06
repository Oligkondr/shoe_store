from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    token: str


class UserRegisterResponse(BaseModel):
    success: bool

class ClientProductResponse(BaseModel):
    success: bool

class ClientPayResponse(BaseModel):
    success: bool

