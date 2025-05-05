from pydantic import BaseModel


class AdminResponse(BaseModel):
    token: str

