from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette import status

from app.auth.auth_handler import verify_password, create_access_token, get_current_client
from app.models import Client, Order, Product, OrderProduct, ModelColor, SizeGrid, Color, Model
from app.database import session_maker
from app.requests import ClientCreateRequest, UserAuthRequest, ClientProductRequest, ClientDepositRequest, \
    ClientUpdateRequest
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
        if session.query(Client).filter_by(email=client.email).first() is not None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Client already registered")

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


@clients_router.post('/product', summary='Add product to order')
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

    return new_order_product


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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Корзина пуста")

    return order


@clients_router.post('/deposit', summary='fill up account')
def deposit(data: ClientDepositRequest, client: Client = Depends(get_current_client)):
    with session_maker() as session:
        client.account += data.amount

        session.add(client)
        session.commit()

    return client


@clients_router.get('/products', summary='Get all products', responses={
    200: {
        "description": "Удачный ответ",
        "content": {
            "application/json": {
                "example":
                    [
                        {
                            "model_color_id": 1,
                            "id": 1,
                            "updated_at": "2025-05-06T07:12:51.945606+00:00",
                            "price": 5490,
                            "created_at": "2025-05-06T07:12:51.945606+00:00",
                            "model_color": {
                                "name": "Bloody Black",
                                "model_id": 1,
                                "color_id": 1,
                                "updated_at": "2025-05-06T07:12:35.862637+00:00",
                                "id": 1,
                                "created_at": "2025-05-06T07:12:35.862637+00:00",
                                "color": {
                                    "id": 1,
                                    "created_at": "2025-05-06T07:10:11.435277+00:00",
                                    "updated_at": "2025-05-06T07:10:11.435277+00:00",
                                    "name": "black, white,red",
                                    "base_colors": [
                                        {
                                            "name": "black",
                                            "created_at": "2025-05-06T10:08:56+00:00",
                                            "hex": "000000",
                                            "updated_at": "2025-05-06T10:08:58+00:00",
                                            "id": 1
                                        },
                                        {
                                            "name": "white",
                                            "created_at": "2025-05-06T07:09:33.610019+00:00",
                                            "hex": "ffffff",
                                            "updated_at": "2025-05-06T07:09:33.610019+00:00",
                                            "id": 2
                                        },
                                        {
                                            "name": "red",
                                            "created_at": "2025-05-06T07:09:46.459870+00:00",
                                            "hex": "ff0000",
                                            "updated_at": "2025-05-06T07:09:46.459870+00:00",
                                            "id": 3
                                        }
                                    ]
                                },
                                "model": {
                                    "description": "Super sneakers",
                                    "name": "Sneakers",
                                    "id": 1,
                                    "updated_at": "2025-05-06T07:11:44.646189+00:00",
                                    "sex_id": 2,
                                    "category_id": 1,
                                    "created_at": "2025-05-06T07:11:44.646189+00:00",
                                    "category": {
                                        "updated_at": "2025-05-06T07:11:40.030859+00:00",
                                        "name": "sneakers",
                                        "id": 1,
                                        "created_at": "2025-05-06T07:11:40.030859+00:00"
                                    }
                                }
                            },
                            "size_grid": [
                                {
                                    "size_id": 1,
                                    "created_at": "2025-05-06T07:34:42.153756+00:00",
                                    "quantity": 200,
                                    "product_id": 1,
                                    "id": 1,
                                    "updated_at": "2025-05-06T07:34:42.153756+00:00",
                                    "size": {
                                        "created_at": "2025-05-06T07:15:30.350688+00:00",
                                        "ru": "43",
                                        "cm": "28",
                                        "id": 1,
                                        "updated_at": "2025-05-06T07:15:30.350688+00:00"
                                    }
                                },
                                {
                                    "size_id": 2,
                                    "created_at": "2025-05-06T07:41:46.584329+00:00",
                                    "quantity": 159,
                                    "product_id": 1,
                                    "id": 2,
                                    "updated_at": "2025-05-06T07:41:46.584329+00:00",
                                    "size": {
                                        "created_at": "2025-05-06T07:41:28.958393+00:00",
                                        "ru": "44",
                                        "cm": "29",
                                        "id": 2,
                                        "updated_at": "2025-05-06T07:41:28.958393+00:00"
                                    }
                                }
                            ]
                        }
                    ]
            }
        }
    }
})
def get_all_products():
    with session_maker() as session:
        smtm = select(Product).options(
            joinedload(Product.model_color).subqueryload(ModelColor.color).subqueryload(Color.base_colors),
            joinedload(Product.model_color).subqueryload(ModelColor.model).subqueryload(Model.category),
            joinedload(Product.size_grid).subqueryload(SizeGrid.size),
        )
        result = session.execute(smtm).unique().scalars().all()
    return result


@clients_router.get('/profile', summary='Get client profile', responses={
    200: {
        "description": "Удачный ответ",
        "content": {
            "application/json": {
                "example":
                    {
                        "email": "client1@mail.com",
                        "phone": "phone1",
                        "surname": "surname1",
                        "id": 1,
                        "updated_at": "2025-05-06T14:36:47.253135+00:00",
                        "name": "name1",
                        "password": "$2b$12$fDSmfGwhqvaItMi89.27se0ZtnlY8OKsME1qBgh5M3wxKcKLOMKmi",
                        "account": 5701,
                        "created_at": "2025-05-06T08:26:40.571876+00:00"
                    }
            }
        }
    }
})
def get_client_profile(client: Client = Depends(get_current_client)):
    with session_maker() as session:
        client_obj = session.get(Client, client.id)
    return client_obj


@clients_router.post('/profile', summary='Save profile changes')
def save_profile_changes(changes: ClientUpdateRequest, client: Client = Depends(get_current_client)):
    with session_maker() as session:
        client_obj = session.get(Client, client.id)

        if not client_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        client_obj.email = changes.email
        client_obj.phone = changes.phone
        client_obj.name = changes.name
        client_obj.surname = changes.surname

        session.commit()

    return client_obj


@clients_router.get('/orders', summary='Get client`s orders')
def get_orders(client: Client = Depends(get_current_client)):
    with (session_maker() as session):
        orders_obj = session.query(Order).options(
            joinedload(Order.order_products).subqueryload(OrderProduct.product).subqueryload(
                Product.model_color).subqueryload(ModelColor.color).subqueryload(Color.base_colors),
            joinedload(Order.order_products).subqueryload(OrderProduct.product).subqueryload(
                Product.model_color).subqueryload(ModelColor.model).subqueryload(Model.category),
            joinedload(Order.order_products).subqueryload(OrderProduct.product).subqueryload(
                Product.size_grid).subqueryload(SizeGrid.size),
        ).filter(
            Order.client_id == client.id).all()
    return orders_obj
