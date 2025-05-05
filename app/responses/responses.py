from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    token: str


class UserRegisterResponse(BaseModel):
    success: bool
