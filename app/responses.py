from typing import Generic, TypeVar, List
from datetime import datetime
from pydantic import BaseModel

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


class ClientResponse(BaseModel):
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


class ApprovedOrderResponse(BaseModel):
    id: int
    client_id: int
    approved_at: datetime | None
    status_id: int
    price: int


class ActiveOrderResponse(BaseModel):
    id: int
    client_id: int
    approved_at: None
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

    base_colors: list[BaseColorResponse]


class ModelResponse(BaseModel):
    id: int
    name: str
    description: str
    sex_id: int

    category: CategoryResponse


class ModelColorResponse(BaseModel):
    id: int
    name: str

    model: ModelResponse
    color: ColorResponse


class SizeResponse(BaseModel):
    id: int
    ru: str
    cm: str


class SizeGridResponse(BaseModel):
    id: int
    quantity: int

    size: SizeResponse


class ProductResponse(BaseModel):
    id: int
    price: int
    model_color_id: int

    size_grid: list[SizeGridResponse]
    model_color: ModelColorResponse


class OrderProductResponse(BaseModel):
    id: int
    price: int
    quantity: int

    order: ActiveOrderResponse
    product: ProductResponse


class ProductsResponse(BaseModel):
    products: list[ProductResponse]


class OrdersResponse(BaseModel):
    orders: list[ApprovedOrderResponse]
