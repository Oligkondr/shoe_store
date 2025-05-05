from pydantic import BaseModel


class AdminLoginResponse(BaseModel):
    token: str


class AdminRegisterResponse(BaseModel):
    success: bool
