from typing import Generic, TypeVar, Any
from datetime import datetime
from pydantic import BaseModel

from app.models import Product, Order, BaseColor

T = TypeVar('T')

class TestResponse(BaseModel):
    fild_a: int
    fild_b: str

class ResponseModel(BaseModel, Generic[T]):
    success: bool
    data: T


class ErrorResponseModel(BaseModel):
    success: bool
    error: str


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


class OrderResponse(BaseModel):
    id: int
    client_id: int
    approved_at: datetime
    status_id: int
    price: int


class CategoryResponse(BaseModel):
    id: int
    name: str


class BaseColorResponse(BaseModel):
    id: int
    name: str
    hex: str


class ColorResponse(BaseModel):
    id: int
    name: str

    base_colors: dict


class ModelResponse(BaseModel):
    id: int
    name: str
    description: str
    sex_id: int
    category_id: int

    category: CategoryResponse


class ModelColorResponse(BaseModel):
    id: int
    name: str
    model_id: int
    color_id: str

    model: ModelResponse
    color: ColorResponse


class ProductResponse(BaseModel):
    id: int
    price: int
    model_color_id: int

    size_grid: dict
    model_color: ModelColorResponse


class OrderProductResponse(BaseModel):
    id: int
    price: int
    quantity: int

    order: OrderResponse
    product: ProductResponse
