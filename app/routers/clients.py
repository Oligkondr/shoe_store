from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from sqlalchemy import select, Nullable
from starlette import status

from app.auth.auth_handler import verify_password, create_access_token, get_current_client
from app.models import Client, Order, Product, OrderProduct, ModelColor, ProductSize, Model
from app.database import session_maker
from app.requests import ClientCreateRequest, UserAuthRequest, ClientProductRequest, ClientDepositRequest, \
    ClientUpdateRequest, NewQuantityRequest
from app.responses import UserLoginResponse, ClientResponse, ResponseModel, OrderProductResponse, \
    ApprovedOrderResponse, ProductResponse, ProductsResponse, OrdersResponse, ActiveOrderResponse, ModelsResponse, \
    ModelResponse

clients_router = APIRouter(prefix="/api/v1", tags=["Client"])


# @clients_router.get('/test', summary='Test get request')
# def test(request: Request):
#     params = request.query_params
#     params_dict = dict(params)
#     model = params_dict['model']
#     return model


@clients_router.get('/orders', summary='Get client approved orders', response_model=ResponseModel[OrdersResponse])
def get_approved_orders(client: Client = Depends(get_current_client)):
    with session_maker() as session:
        orders_obj = session.query(Order).filter(
            Order.client_id == client.id,
            Order.status_id != Order.STATUS_NEW_ID,
        ).all()

        result_dto = [ApprovedOrderResponse.model_validate(row, from_attributes=True) for row in orders_obj]

    return ResponseModel[OrdersResponse](
        success=True,
        data=OrdersResponse(orders=result_dto)
    )


@clients_router.get('/order', summary='Get client active order', response_model=ResponseModel[ActiveOrderResponse])
def get_active_order(client: Client = Depends(get_current_client)):
    with session_maker() as session:
        order_obj = session.query(Order).filter_by(client_id=client.id, status_id=Order.STATUS_NEW_ID).one_or_none()

        if order_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нет активной корзины")

        result_dto = ActiveOrderResponse.model_validate(order_obj, from_attributes=True)

    return ResponseModel[ActiveOrderResponse](
        success=True,
        data=result_dto
    )


@clients_router.get('/profile', summary='Get client profile', response_model=ResponseModel[ClientResponse])
def get_client_profile(client: Client = Depends(get_current_client)):
    with session_maker() as session:
        client_obj = session.get(Client, client.id)

        result_dto = ClientResponse.model_validate(client_obj, from_attributes=True)

    return ResponseModel[ClientResponse](
        success=True,
        data=result_dto
    )


@clients_router.get('/products', summary='Get all products', response_model=ResponseModel[ProductsResponse])
def get_all_products(
        model_id: Optional[int] = Query(None),
        client: Client = Depends(get_current_client)
):
    with session_maker() as session:
        smtm = select(Product)

        if model_id:
            smtm = smtm.join(Product.model_color).filter(ModelColor.model_id == model_id)

        result = session.execute(smtm).scalars().all()

        result_dto = [ProductResponse.model_validate(row, from_attributes=True) for row in result]

    return ResponseModel[ProductsResponse](
        success=True,
        data=ProductsResponse(products=result_dto)
    )


@clients_router.post('/register', summary='Create new client', response_model=ResponseModel[ClientResponse])
def create_admin(client: ClientCreateRequest):
    with session_maker() as session:
        if session.query(Client).filter_by(email=client.email).first() is not None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Пользователь с такой почтой уже зарегистрирован")

        if session.query(Client).filter_by(phone=client.phone).first() is not None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Пользователь с таким номером уже зарегистрирован")

        new_client = Client(
            email=client.email,
            phone=client.phone,
            name=client.name,
            surname=client.surname,
        )
        new_client.set_password(client.password)

        session.add(new_client)
        session.commit()

        result_dto = ClientResponse.model_validate(new_client, from_attributes=True)

    return ResponseModel[ClientResponse](success=True, data=result_dto)


@clients_router.post('/login', summary='Login client', response_model=ResponseModel[UserLoginResponse])
def login_client(client: UserAuthRequest):
    with session_maker() as session:
        stmt = select(Client).where(Client.email == client.email)
        result = session.execute(stmt)
        client_db = result.scalar_one_or_none()

    if client_db is None or verify_password(plain_password=client.password,
                                            hashed_password=client_db.password) is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')

    access_token = create_access_token({
        'id': client_db.id,
        'type': 'client',
    })

    return ResponseModel[UserLoginResponse](success=True, data=UserLoginResponse(token=access_token))


@clients_router.post('/product', summary='Add product to order', response_model=ResponseModel[OrderProductResponse])
def add_product(data: ClientProductRequest, client: Client = Depends(get_current_client)):
    with session_maker() as session:
        order_obj = client.get_or_create_current_order()

        product_size_obj = session.get(ProductSize, data.id)

        new_order_product = OrderProduct(
            product_size_id=product_size_obj.id,
            order_id=order_obj.id,
            quantity=data.quantity,
            price=product_size_obj.product.price,
        )

        session.add(new_order_product)
        session.commit()

        order_obj.update_price()

        result_dto = OrderProductResponse.model_validate(new_order_product, from_attributes=True)

    return ResponseModel[OrderProductResponse](
        success=True,
        data=result_dto
    )


@clients_router.delete("/product/{id}", summary='Remove product from order', response_model=ResponseModel)
def remove_product(id: int, client: Client = Depends(get_current_client)):
    with session_maker() as session:
        order_obj = client.get_current_order(session)
        order_product = session.get(OrderProduct, id)

        if order_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого продукта нет к корзине')

        if order_obj.id == order_product.order_id:
            session.delete(order_product)
            session.commit()
            order_obj.update_price()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return ResponseModel(success=True, data=None)


@clients_router.patch("/product/{id}", summary='Change quantity of product in order', response_model=ResponseModel)
def change_product_quantity(id: int, data: NewQuantityRequest, client: Client = Depends(get_current_client)):
    with session_maker() as session:
        order_obj = client.get_current_order(session)
        order_product = session.get(OrderProduct, id)

        if order_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого продукта нет к корзине')

        if order_obj.id == order_product.order_id:
            order_product.quantity = data.quantity
            session.commit()

            order_obj.update_price()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return ResponseModel(success=True, data=None)


@clients_router.post('/deposit', summary='Add money on account', response_model=ResponseModel[ClientResponse])
def deposit(data: ClientDepositRequest, client: Client = Depends(get_current_client)):
    with session_maker() as session:
        client.account += data.amount

        session.add(client)
        session.commit()

        result_dto = ClientResponse.model_validate(client, from_attributes=True)

    return ResponseModel[ClientResponse](
        success=True,
        data=result_dto
    )


@clients_router.post('/approve', summary='Approve order', response_model=ResponseModel[ApprovedOrderResponse])
def approve(client: Client = Depends(get_current_client)):
    with session_maker() as session:
        order_obj = client.get_current_order(session)
        order = session.get(Order, order_obj.id)
        order_products = order.order_products

        if len(order_products):
            order.payment(session)

            order.status_id = Order.STATUS_PAID_ID
            order.approved_at = datetime.now()

            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Корзина пуста")

        result_dto = ApprovedOrderResponse.model_validate(order, from_attributes=True)

    return ResponseModel[ApprovedOrderResponse](
        success=True,
        data=result_dto
    )


@clients_router.put('/profile', summary='Save profile changes', response_model=ResponseModel[ClientResponse])
def save_profile_changes(changes: ClientUpdateRequest, client: Client = Depends(get_current_client)):
    with session_maker() as session:
        client_obj = session.get(Client, client.id)

        if not client_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

        client_obj.email = changes.email
        client_obj.phone = changes.phone
        client_obj.name = changes.name
        client_obj.surname = changes.surname

        session.commit()

        result_dto = ClientResponse.model_validate(client_obj, from_attributes=True)

    return ResponseModel[ClientResponse](
        success=True,
        data=result_dto
    )


@clients_router.get('/models', summary='Get all models', response_model=ResponseModel[ModelsResponse])
def get_models(client: Client = Depends(get_current_client)):
    with session_maker() as session:
        models_obj = session.query(Model).all()

        result_dto = [ModelResponse.model_validate(row, from_attributes=True) for row in models_obj]

    return ResponseModel[ModelsResponse](
        success=True,
        data=ModelsResponse(models=result_dto)
    )
