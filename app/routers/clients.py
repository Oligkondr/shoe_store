from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from starlette import status

from app.auth.auth_handler import verify_password, create_access_token, get_current_client
from app.models import Client, Order, Product, OrderProduct
from app.database import session_maker
from app.requests import ClientCreateRequest, UserAuthRequest, ClientProductRequest, ClientDepositRequest
from app.responses.responses import UserLoginResponse, UserRegisterResponse, ClientProductResponse

clients_router = APIRouter(prefix="/api/v1", tags=["client"])


@clients_router.get('/test', summary='Test get request')
async def test(client: Client = Depends(get_current_client)):
    with session_maker() as session:
        order_obj = client.get_current_order()
        order = session.get(Order, order_obj.id)
        client = order.payment()

    return client


@clients_router.post('/test', summary='Test post request')
def post_test(client: Client = Depends(get_current_client)):
    return {'message': client}


@clients_router.post('/register', summary='Create new client', response_model=UserRegisterResponse)
def create_admin(client: ClientCreateRequest):
    with session_maker() as session:
        new_client = Client(
            email=client.email,
            phone=client.phone,
            name=client.name,
            surname=client.surname,
            # account=0
        )
        new_client.set_password(client.password)

        session.add(new_client)
        session.commit()
    return {'success': True}


@clients_router.post('/login', summary='Login client', response_model=UserLoginResponse)
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

    return {'token': access_token}


@clients_router.post('/product', summary='Add product to order', response_model=ClientProductResponse)
def add_product(data: ClientProductRequest, client: Client = Depends(get_current_client)):
    with session_maker() as session:
        order_obj = client.get_current_order()

        stmt = select(Product).where(Product.id == data.id)
        result = session.execute(stmt)
        product_obj = result.scalar_one_or_none()

        new_order_product = OrderProduct(
            product=product_obj,
            order=order_obj,
            quantity=data.quantity,
            price=product_obj.price,
        )

        session.add(new_order_product)

        session.commit()

        order_obj.update_price()

    return {'success': True}


@clients_router.post('/approve', summary='approve order')
def approve(client: Client = Depends(get_current_client)):
    with session_maker() as session:
        order_obj = client.get_current_order()
        order = session.get(Order, order_obj.id)
        order_products = order.order_products

        if len(order_products):
            order.payment(session)

            order.status_id = Order.STATUS_PAID_ID
            order.approved_at = datetime.now()

            session.add(order)
            session.commit()
        else:
            raise Exception("Корзина пуста")

    return {'success': True}


@clients_router.post('/deposit', summary='fill up account')
def deposit(data: ClientDepositRequest, client: Client = Depends(get_current_client)):
    with session_maker() as session:
        client.account += data.amount

        session.add(client)
        session.commit()

    return {'success': True}
