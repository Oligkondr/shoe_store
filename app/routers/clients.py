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
from app.responses import UserLoginResponse, ClientRegisterResponse

clients_router = APIRouter(prefix="/api/v1", tags=["client"])


# @clients_router.get('/test', summary='Test get request')
# async def test():
#     # response = ErrorResponseModel(success=False, error='Error')
#     # return ErrorResponseModel(success=False, error='Error')
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                         detail="Пользователь с такой почтой уже зарегистрирован")


# @clients_router.post('/test', summary='Test post request')
# def post_test(client: Client = Depends(get_current_client)):
#     return {'message': client}


@clients_router.post('/register', summary='Create new client', response_model=ClientRegisterResponse)
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

    return {
        'email': new_client.email,
        'phone': new_client.phone,
        'name': new_client.name,
        'surname': new_client.surname,
        'account': new_client.account,
    }


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


@clients_router.post('/product', summary='Add product to order', responses={
    200: {
        "description": "Удачный ответ",
        "content": {
            "application/json": {
                "example":
                    {
                        "product": {
                            "price": 3299,
                            "created_at": "2025-05-06T08:06:03.058980+00:00",
                            "model_color_id": 2,
                            "id": 2,
                            "updated_at": "2025-05-06T08:06:03.058980+00:00",
                            "size_grid": [
                                {
                                    "quantity": 32,
                                    "product_id": 2,
                                    "id": 3,
                                    "updated_at": "2025-05-06T08:07:30.048761+00:00",
                                    "size_id": 1,
                                    "created_at": "2025-05-06T08:07:30.048761+00:00",
                                    "size": {
                                        "id": 1,
                                        "cm": "28",
                                        "updated_at": "2025-05-06T07:15:30.350688+00:00",
                                        "ru": "43",
                                        "created_at": "2025-05-06T07:15:30.350688+00:00"
                                    }
                                }
                            ],
                            "model_color": {
                                "id": 2,
                                "created_at": "2025-05-06T08:05:20.068753+00:00",
                                "model_id": 2,
                                "name": "Super Red",
                                "color_id": 1,
                                "updated_at": "2025-05-06T08:05:20.068753+00:00",
                                "model": {
                                    "sex_id": 0,
                                    "category_id": 2,
                                    "created_at": "2025-05-06T08:03:51.575198+00:00",
                                    "name": "Shit Squeezers",
                                    "description": "Squeeze this shit!",
                                    "id": 2,
                                    "updated_at": "2025-05-06T08:03:51.575198+00:00",
                                    "category": {
                                        "updated_at": "2025-05-06T08:01:11.585038+00:00",
                                        "id": 2,
                                        "name": "boots",
                                        "created_at": "2025-05-06T08:01:11.585038+00:00"
                                    }
                                },
                                "color": {
                                    "name": "black, white,red",
                                    "created_at": "2025-05-06T07:10:11.435277+00:00",
                                    "id": 1,
                                    "updated_at": "2025-05-06T07:10:11.435277+00:00",
                                    "base_colors": [
                                        {
                                            "id": 1,
                                            "created_at": "2025-05-06T10:08:56+00:00",
                                            "name": "black",
                                            "hex": "000000",
                                            "updated_at": "2025-05-06T10:08:58+00:00"
                                        },
                                        {
                                            "id": 2,
                                            "created_at": "2025-05-06T07:09:33.610019+00:00",
                                            "name": "white",
                                            "hex": "ffffff",
                                            "updated_at": "2025-05-06T07:09:33.610019+00:00"
                                        },
                                        {
                                            "id": 3,
                                            "created_at": "2025-05-06T07:09:46.459870+00:00",
                                            "name": "red",
                                            "hex": "ff0000",
                                            "updated_at": "2025-05-06T07:09:46.459870+00:00"
                                        }
                                    ]
                                }
                            }
                        },
                        "order": {
                            "client_id": 1,
                            "created_at": "2025-05-06T13:17:36.015491+00:00",
                            "status_id": 0,
                            "price": 3299,
                            "approved_at": "null",
                            "id": 19,
                            "updated_at": "2025-05-06T17:04:07.310799+00:00"
                        },
                        "quantity": 1,
                        "price": 3299,
                        "order_id": 19,
                        "product_id": 2,
                        "id": 83,
                        "created_at": "2025-05-06T14:10:08.424885+00:00",
                        "updated_at": "2025-05-06T14:10:08.424885+00:00"
                    }}
        }
    }
})
def add_product(data: ClientProductRequest, client: Client = Depends(get_current_client)):
    with session_maker() as session:
        order_obj = client.get_or_create_current_order()

        stmt = select(Product).where(Product.id == data.id).options(
            joinedload(Product.model_color).subqueryload(ModelColor.color).subqueryload(Color.base_colors),
            joinedload(Product.model_color).subqueryload(ModelColor.model).subqueryload(Model.category),
            joinedload(Product.size_grid).subqueryload(SizeGrid.size),
        )

        result = session.execute(stmt).unique()
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


@clients_router.post('/deposit', summary='Add money on account', responses={
    200: {
        "description": "Удачный ответ",
        "content": {
            "application/json": {
                "example":
                    {
                        "email": "client1Change2@mail.com",
                        "phone": "phone1 change2",
                        "name": "name1 change2",
                        "surname": "surname1 change2",
                        "account": 25804
                    }
            }
        }
    }

})
def deposit(data: ClientDepositRequest, client: Client = Depends(get_current_client)):
    with session_maker() as session:
        client.account += data.amount

        session.add(client)
        session.commit()

    return {
        'email': client.email,
        'phone': client.phone,
        'name': client.name,
        'surname': client.surname,
        'account': client.account,
    }


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
                        "email": "client1Change2@mail.com",
                        "phone": "phone1 change2",
                        "name": "name1 change2",
                        "surname": "surname1 change2"
                    }
            }
        }
    }
})
def get_client_profile(client: Client = Depends(get_current_client)):
    with session_maker() as session:
        client_obj = session.get(Client, client.id)
        return {
            'email': client_obj.email,
            'phone': client_obj.phone,
            'name': client_obj.name,
            'surname': client_obj.surname,
            'account': client_obj.account,
        }


@clients_router.post('/approve', summary='Approve order', responses={
    200: {
        "description": "Удачный ответ",
        "content": {
            "application/json": {
                "example":
                    {
                        "id": 18,
                        "client_id": 1,
                        "status_id": 1,
                        "price": 16598,
                        "approved_at": "2025-05-06T16:11:04.498042",
                        "created_at": "2025-05-06T13:03:22.376651+00:00",
                        "updated_at": "2025-05-06T16:11:04.499042",
                        "order_products": [
                            {
                                "order_id": 18,
                                "price": 3299,
                                "created_at": "2025-05-06T13:03:22.381994+00:00",
                                "quantity": 1,
                                "product_id": 2,
                                "id": 78,
                                "updated_at": "2025-05-06T13:03:22.381994+00:00"
                            },
                            {
                                "order_id": 18,
                                "price": 5000,
                                "created_at": "2025-05-06T13:07:23.242765+00:00",
                                "quantity": 1,
                                "product_id": 1,
                                "id": 79,
                                "updated_at": "2025-05-06T13:07:23.242765+00:00"
                            },
                        ],
                        "client": {
                            "email": "client1Change2@mail.com",
                            "phone": "phone1 change2",
                            "surname": "surname1 change2",
                            "id": 1,
                            "name": "name1 change2",
                            "account": 5804,
                            "password": "$2b$12$fDSmfGwhqvaItMi89.27se0ZtnlY8OKsME1qBgh5M3wxKcKLOMKmi",
                            "created_at": "2025-05-06T08:26:40.571876+00:00",
                            "updated_at": "2025-05-06T16:11:04.496042"
                        }
                    }
            }
        }
    }
})
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


@clients_router.put('/profile', summary='Save profile changes', responses={
    200: {
        "description": "Удачный ответ",
        "content": {
            "application/json": {
                "example":
                    {
                        "email": "client1Change3@mail.com",
                        "phone": "phone1 change3",
                        "name": "name1 change3",
                        "surname": "surname1 change3"
                    }
            }
        }
    }

})
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

    return {
        'email': client_obj.email,
        'phone': client_obj.phone,
        'name': client_obj.name,
        'surname': client_obj.surname,
    }


@clients_router.get('/orders', summary='Get client orders', responses={
    200: {
        "description": "Удачный ответ",
        "content": {
            "application/json": {
                "example":
                    [
                        {
                            "client_id": 2,
                            "created_at": "2025-05-06T14:23:34.353986+00:00",
                            "status_id": 1,
                            "price": 13299,
                            "approved_at": "2025-05-06T17:24:32.780266+00:00",
                            "id": 20,
                            "updated_at": "2025-05-06T17:24:32.781264+00:00",
                            "order_products": [
                                {
                                    "order_id": 20,
                                    "price": 3299,
                                    "created_at": "2025-05-06T14:23:34.364307+00:00",
                                    "quantity": 1,
                                    "product_id": 2,
                                    "id": 84,
                                    "updated_at": "2025-05-06T14:23:34.364307+00:00",
                                    "product": {
                                        "price": 3299,
                                        "created_at": "2025-05-06T08:06:03.058980+00:00",
                                        "model_color_id": 2,
                                        "id": 2,
                                        "updated_at": "2025-05-06T08:06:03.058980+00:00",
                                        "size_grid": [
                                            {
                                                "product_id": 2,
                                                "quantity": 32,
                                                "id": 3,
                                                "updated_at": "2025-05-06T08:07:30.048761+00:00",
                                                "size_id": 1,
                                                "created_at": "2025-05-06T08:07:30.048761+00:00",
                                                "size": {
                                                    "cm": "28",
                                                    "id": 1,
                                                    "updated_at": "2025-05-06T07:15:30.350688+00:00",
                                                    "created_at": "2025-05-06T07:15:30.350688+00:00",
                                                    "ru": "43"
                                                }
                                            }
                                        ],
                                        "model_color": {
                                            "id": 2,
                                            "created_at": "2025-05-06T08:05:20.068753+00:00",
                                            "model_id": 2,
                                            "name": "Super Red",
                                            "color_id": 1,
                                            "updated_at": "2025-05-06T08:05:20.068753+00:00",
                                            "model": {
                                                "sex_id": 0,
                                                "category_id": 2,
                                                "created_at": "2025-05-06T08:03:51.575198+00:00",
                                                "name": "Shit Squeezers",
                                                "description": "Squeeze this shit!",
                                                "id": 2,
                                                "updated_at": "2025-05-06T08:03:51.575198+00:00",
                                                "category": {
                                                    "updated_at": "2025-05-06T08:01:11.585038+00:00",
                                                    "name": "boots",
                                                    "created_at": "2025-05-06T08:01:11.585038+00:00",
                                                    "id": 2
                                                }
                                            },
                                            "color": {
                                                "name": "black, white,red",
                                                "created_at": "2025-05-06T07:10:11.435277+00:00",
                                                "id": 1,
                                                "updated_at": "2025-05-06T07:10:11.435277+00:00",
                                                "base_colors": [
                                                    {
                                                        "id": 1,
                                                        "created_at": "2025-05-06T10:08:56+00:00",
                                                        "name": "black",
                                                        "hex": "000000",
                                                        "updated_at": "2025-05-06T10:08:58+00:00"
                                                    },
                                                    {
                                                        "id": 2,
                                                        "created_at": "2025-05-06T07:09:33.610019+00:00",
                                                        "name": "white",
                                                        "hex": "ffffff",
                                                        "updated_at": "2025-05-06T07:09:33.610019+00:00"
                                                    },
                                                    {
                                                        "id": 3,
                                                        "created_at": "2025-05-06T07:09:46.459870+00:00",
                                                        "name": "red",
                                                        "hex": "ff0000",
                                                        "updated_at": "2025-05-06T07:09:46.459870+00:00"
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                },
                                {
                                    "order_id": 20,
                                    "price": 5000,
                                    "created_at": "2025-05-06T14:23:45.417513+00:00",
                                    "quantity": 2,
                                    "product_id": 1,
                                    "id": 85,
                                    "updated_at": "2025-05-06T14:23:45.417513+00:00",
                                    "product": {
                                        "price": 5000,
                                        "created_at": "2025-05-06T07:12:51.945606+00:00",
                                        "model_color_id": 1,
                                        "id": 1,
                                        "updated_at": "2025-05-06T12:04:56.285405+00:00",
                                        "size_grid": [
                                            {
                                                "product_id": 1,
                                                "quantity": 200,
                                                "id": 1,
                                                "updated_at": "2025-05-06T07:34:42.153756+00:00",
                                                "size_id": 1,
                                                "created_at": "2025-05-06T07:34:42.153756+00:00",
                                                "size": {
                                                    "cm": "28",
                                                    "id": 1,
                                                    "updated_at": "2025-05-06T07:15:30.350688+00:00",
                                                    "created_at": "2025-05-06T07:15:30.350688+00:00",
                                                    "ru": "43"
                                                }
                                            },
                                            {
                                                "product_id": 1,
                                                "quantity": 159,
                                                "id": 2,
                                                "updated_at": "2025-05-06T07:41:46.584329+00:00",
                                                "size_id": 2,
                                                "created_at": "2025-05-06T07:41:46.584329+00:00",
                                                "size": {
                                                    "cm": "29",
                                                    "id": 2,
                                                    "updated_at": "2025-05-06T07:41:28.958393+00:00",
                                                    "created_at": "2025-05-06T07:41:28.958393+00:00",
                                                    "ru": "44"
                                                }
                                            }
                                        ],
                                        "model_color": {
                                            "id": 1,
                                            "created_at": "2025-05-06T07:12:35.862637+00:00",
                                            "model_id": 1,
                                            "name": "Bloody Black",
                                            "color_id": 1,
                                            "updated_at": "2025-05-06T07:12:35.862637+00:00",
                                            "model": {
                                                "sex_id": 2,
                                                "category_id": 1,
                                                "created_at": "2025-05-06T07:11:44.646189+00:00",
                                                "name": "Sneakers",
                                                "description": "Super sneakers",
                                                "id": 1,
                                                "updated_at": "2025-05-06T07:11:44.646189+00:00",
                                                "category": {
                                                    "updated_at": "2025-05-06T07:11:40.030859+00:00",
                                                    "name": "sneakers",
                                                    "created_at": "2025-05-06T07:11:40.030859+00:00",
                                                    "id": 1
                                                }
                                            },
                                            "color": {
                                                "name": "black, white,red",
                                                "created_at": "2025-05-06T07:10:11.435277+00:00",
                                                "id": 1,
                                                "updated_at": "2025-05-06T07:10:11.435277+00:00",
                                                "base_colors": [
                                                    {
                                                        "id": 1,
                                                        "created_at": "2025-05-06T10:08:56+00:00",
                                                        "name": "black",
                                                        "hex": "000000",
                                                        "updated_at": "2025-05-06T10:08:58+00:00"
                                                    },
                                                    {
                                                        "id": 2,
                                                        "created_at": "2025-05-06T07:09:33.610019+00:00",
                                                        "name": "white",
                                                        "hex": "ffffff",
                                                        "updated_at": "2025-05-06T07:09:33.610019+00:00"
                                                    },
                                                    {
                                                        "id": 3,
                                                        "created_at": "2025-05-06T07:09:46.459870+00:00",
                                                        "name": "red",
                                                        "hex": "ff0000",
                                                        "updated_at": "2025-05-06T07:09:46.459870+00:00"
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                }
                            ]
                        },
                        {
                            "client_id": 2,
                            "created_at": "2025-05-06T14:25:38.682100+00:00",
                            "status_id": 1,
                            "price": 5000,
                            "approved_at": "2025-05-06T17:25:45.726998+00:00",
                            "id": 21,
                            "updated_at": "2025-05-06T17:25:45.727998+00:00",
                            "order_products": [
                                {
                                    "order_id": 21,
                                    "price": 5000,
                                    "created_at": "2025-05-06T14:25:38.687292+00:00",
                                    "quantity": 1,
                                    "product_id": 1,
                                    "id": 86,
                                    "updated_at": "2025-05-06T14:25:38.687292+00:00",
                                    "product": {
                                        "price": 5000,
                                        "created_at": "2025-05-06T07:12:51.945606+00:00",
                                        "model_color_id": 1,
                                        "id": 1,
                                        "updated_at": "2025-05-06T12:04:56.285405+00:00",
                                        "size_grid": [
                                            {
                                                "product_id": 1,
                                                "quantity": 200,
                                                "id": 1,
                                                "updated_at": "2025-05-06T07:34:42.153756+00:00",
                                                "size_id": 1,
                                                "created_at": "2025-05-06T07:34:42.153756+00:00",
                                                "size": {
                                                    "cm": "28",
                                                    "id": 1,
                                                    "updated_at": "2025-05-06T07:15:30.350688+00:00",
                                                    "created_at": "2025-05-06T07:15:30.350688+00:00",
                                                    "ru": "43"
                                                }
                                            },
                                            {
                                                "product_id": 1,
                                                "quantity": 159,
                                                "id": 2,
                                                "updated_at": "2025-05-06T07:41:46.584329+00:00",
                                                "size_id": 2,
                                                "created_at": "2025-05-06T07:41:46.584329+00:00",
                                                "size": {
                                                    "cm": "29",
                                                    "id": 2,
                                                    "updated_at": "2025-05-06T07:41:28.958393+00:00",
                                                    "created_at": "2025-05-06T07:41:28.958393+00:00",
                                                    "ru": "44"
                                                }
                                            }
                                        ],
                                        "model_color": {
                                            "id": 1,
                                            "created_at": "2025-05-06T07:12:35.862637+00:00",
                                            "model_id": 1,
                                            "name": "Bloody Black",
                                            "color_id": 1,
                                            "updated_at": "2025-05-06T07:12:35.862637+00:00",
                                            "model": {
                                                "sex_id": 2,
                                                "category_id": 1,
                                                "created_at": "2025-05-06T07:11:44.646189+00:00",
                                                "name": "Sneakers",
                                                "description": "Super sneakers",
                                                "id": 1,
                                                "updated_at": "2025-05-06T07:11:44.646189+00:00",
                                                "category": {
                                                    "updated_at": "2025-05-06T07:11:40.030859+00:00",
                                                    "name": "sneakers",
                                                    "created_at": "2025-05-06T07:11:40.030859+00:00",
                                                    "id": 1
                                                }
                                            },
                                            "color": {
                                                "name": "black, white,red",
                                                "created_at": "2025-05-06T07:10:11.435277+00:00",
                                                "id": 1,
                                                "updated_at": "2025-05-06T07:10:11.435277+00:00",
                                                "base_colors": [
                                                    {
                                                        "id": 1,
                                                        "created_at": "2025-05-06T10:08:56+00:00",
                                                        "name": "black",
                                                        "hex": "000000",
                                                        "updated_at": "2025-05-06T10:08:58+00:00"
                                                    },
                                                    {
                                                        "id": 2,
                                                        "created_at": "2025-05-06T07:09:33.610019+00:00",
                                                        "name": "white",
                                                        "hex": "ffffff",
                                                        "updated_at": "2025-05-06T07:09:33.610019+00:00"
                                                    },
                                                    {
                                                        "id": 3,
                                                        "created_at": "2025-05-06T07:09:46.459870+00:00",
                                                        "name": "red",
                                                        "hex": "ff0000",
                                                        "updated_at": "2025-05-06T07:09:46.459870+00:00"
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    ]
            }
        }
    }
})
def get_orders(client: Client = Depends(get_current_client)):
    with session_maker() as session:
        orders_obj = session.query(Order).options(
            joinedload(Order.order_products).subqueryload(OrderProduct.product).subqueryload(
                Product.model_color).subqueryload(ModelColor.color).subqueryload(Color.base_colors),
            joinedload(Order.order_products).subqueryload(OrderProduct.product).subqueryload(
                Product.model_color).subqueryload(ModelColor.model).subqueryload(Model.category),
            joinedload(Order.order_products).subqueryload(OrderProduct.product).subqueryload(
                Product.size_grid).subqueryload(SizeGrid.size),
        ).filter(
            Order.client_id == client.id,
            Order.status_id != Order.STATUS_NEW_ID,
        ).all()
    return orders_obj


@clients_router.get('/order', summary='Get client active order', responses={
    200: {
        "description": "Удачный ответ",
        "content": {
            "application/json": {
                "example":
                    {
                        "client_id": 2,
                        "created_at": "2025-05-06T16:19:29.574851+00:00",
                        "status_id": 0,
                        "price": 8299,
                        "approved_at": "null",
                        "id": 22,
                        "updated_at": "2025-05-06T19:33:57.452965+00:00",
                        "order_products": [
                            {
                                "order_id": 22,
                                "price": 5000,
                                "created_at": "2025-05-06T16:19:29.584804+00:00",
                                "product_id": 1,
                                "quantity": 1,
                                "id": 87,
                                "updated_at": "2025-05-06T16:19:29.584804+00:00",
                                "product": {
                                    "price": 5000,
                                    "created_at": "2025-05-06T07:12:51.945606+00:00",
                                    "model_color_id": 1,
                                    "id": 1,
                                    "updated_at": "2025-05-06T12:04:56.285405+00:00",
                                    "size_grid": [
                                        {
                                            "quantity": 200,
                                            "product_id": 1,
                                            "id": 1,
                                            "updated_at": "2025-05-06T07:34:42.153756+00:00",
                                            "size_id": 1,
                                            "created_at": "2025-05-06T07:34:42.153756+00:00",
                                            "size": {
                                                "id": 1,
                                                "cm": "28",
                                                "updated_at": "2025-05-06T07:15:30.350688+00:00",
                                                "ru": "43",
                                                "created_at": "2025-05-06T07:15:30.350688+00:00"
                                            }
                                        },
                                        {
                                            "quantity": 159,
                                            "product_id": 1,
                                            "id": 2,
                                            "updated_at": "2025-05-06T07:41:46.584329+00:00",
                                            "size_id": 2,
                                            "created_at": "2025-05-06T07:41:46.584329+00:00",
                                            "size": {
                                                "id": 2,
                                                "cm": "29",
                                                "updated_at": "2025-05-06T07:41:28.958393+00:00",
                                                "ru": "44",
                                                "created_at": "2025-05-06T07:41:28.958393+00:00"
                                            }
                                        }
                                    ],
                                    "model_color": {
                                        "id": 1,
                                        "created_at": "2025-05-06T07:12:35.862637+00:00",
                                        "model_id": 1,
                                        "name": "Bloody Black",
                                        "color_id": 1,
                                        "updated_at": "2025-05-06T07:12:35.862637+00:00",
                                        "model": {
                                            "sex_id": 2,
                                            "category_id": 1,
                                            "created_at": "2025-05-06T07:11:44.646189+00:00",
                                            "name": "Sneakers",
                                            "description": "Super sneakers",
                                            "id": 1,
                                            "updated_at": "2025-05-06T07:11:44.646189+00:00",
                                            "category": {
                                                "updated_at": "2025-05-06T07:11:40.030859+00:00",
                                                "id": 1,
                                                "name": "sneakers",
                                                "created_at": "2025-05-06T07:11:40.030859+00:00"
                                            }
                                        },
                                        "color": {
                                            "name": "black, white,red",
                                            "created_at": "2025-05-06T07:10:11.435277+00:00",
                                            "id": 1,
                                            "updated_at": "2025-05-06T07:10:11.435277+00:00",
                                            "base_colors": [
                                                {
                                                    "id": 1,
                                                    "created_at": "2025-05-06T10:08:56+00:00",
                                                    "name": "black",
                                                    "hex": "000000",
                                                    "updated_at": "2025-05-06T10:08:58+00:00"
                                                },
                                                {
                                                    "id": 2,
                                                    "created_at": "2025-05-06T07:09:33.610019+00:00",
                                                    "name": "white",
                                                    "hex": "ffffff",
                                                    "updated_at": "2025-05-06T07:09:33.610019+00:00"
                                                },
                                                {
                                                    "id": 3,
                                                    "created_at": "2025-05-06T07:09:46.459870+00:00",
                                                    "name": "red",
                                                    "hex": "ff0000",
                                                    "updated_at": "2025-05-06T07:09:46.459870+00:00"
                                                }
                                            ]
                                        }
                                    }
                                }
                            },
                            {
                                "order_id": 22,
                                "price": 3299,
                                "created_at": "2025-05-06T16:33:57.422188+00:00",
                                "product_id": 2,
                                "quantity": 1,
                                "id": 88,
                                "updated_at": "2025-05-06T16:33:57.422188+00:00",
                                "product": {
                                    "price": 3299,
                                    "created_at": "2025-05-06T08:06:03.058980+00:00",
                                    "model_color_id": 2,
                                    "id": 2,
                                    "updated_at": "2025-05-06T08:06:03.058980+00:00",
                                    "size_grid": [
                                        {
                                            "quantity": 32,
                                            "product_id": 2,
                                            "id": 3,
                                            "updated_at": "2025-05-06T08:07:30.048761+00:00",
                                            "size_id": 1,
                                            "created_at": "2025-05-06T08:07:30.048761+00:00",
                                            "size": {
                                                "id": 1,
                                                "cm": "28",
                                                "updated_at": "2025-05-06T07:15:30.350688+00:00",
                                                "ru": "43",
                                                "created_at": "2025-05-06T07:15:30.350688+00:00"
                                            }
                                        }
                                    ],
                                    "model_color": {
                                        "id": 2,
                                        "created_at": "2025-05-06T08:05:20.068753+00:00",
                                        "model_id": 2,
                                        "name": "Super Red",
                                        "color_id": 1,
                                        "updated_at": "2025-05-06T08:05:20.068753+00:00",
                                        "model": {
                                            "sex_id": 0,
                                            "category_id": 2,
                                            "created_at": "2025-05-06T08:03:51.575198+00:00",
                                            "name": "Shit Squeezers",
                                            "description": "Squeeze this shit!",
                                            "id": 2,
                                            "updated_at": "2025-05-06T08:03:51.575198+00:00",
                                            "category": {
                                                "updated_at": "2025-05-06T08:01:11.585038+00:00",
                                                "id": 2,
                                                "name": "boots",
                                                "created_at": "2025-05-06T08:01:11.585038+00:00"
                                            }
                                        },
                                        "color": {
                                            "name": "black, white,red",
                                            "created_at": "2025-05-06T07:10:11.435277+00:00",
                                            "id": 1,
                                            "updated_at": "2025-05-06T07:10:11.435277+00:00",
                                            "base_colors": [
                                                {
                                                    "id": 1,
                                                    "created_at": "2025-05-06T10:08:56+00:00",
                                                    "name": "black",
                                                    "hex": "000000",
                                                    "updated_at": "2025-05-06T10:08:58+00:00"
                                                },
                                                {
                                                    "id": 2,
                                                    "created_at": "2025-05-06T07:09:33.610019+00:00",
                                                    "name": "white",
                                                    "hex": "ffffff",
                                                    "updated_at": "2025-05-06T07:09:33.610019+00:00"
                                                },
                                                {
                                                    "id": 3,
                                                    "created_at": "2025-05-06T07:09:46.459870+00:00",
                                                    "name": "red",
                                                    "hex": "ff0000",
                                                    "updated_at": "2025-05-06T07:09:46.459870+00:00"
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                        ]
                    }
            }
        }
    }
})
def get_orders(client: Client = Depends(get_current_client)):
    with session_maker() as session:
        order_obj = session.query(Order).options(
            joinedload(Order.order_products).subqueryload(OrderProduct.product).subqueryload(
                Product.model_color).subqueryload(ModelColor.color).subqueryload(Color.base_colors),
            joinedload(Order.order_products).subqueryload(OrderProduct.product).subqueryload(
                Product.model_color).subqueryload(ModelColor.model).subqueryload(Model.category),
            joinedload(Order.order_products).subqueryload(OrderProduct.product).subqueryload(
                Product.size_grid).subqueryload(SizeGrid.size),
        ).filter_by(client_id=client.id, status_id=Order.STATUS_NEW_ID).one_or_none()
    return order_obj

# @clients_router.delete("/product", summary='Remove product from order')
# def remove_product(client: Client = Depends(get_current_client)):
#     with session_maker() as session:
#         order_obj = client.get_current_order()
#     return order_obj

# @clients_router.patch("/product", summary='Change quantity of product in order')
# def change_product_quantity(client: Client = Depends(get_current_client)):
#     with session_maker() as session:
#         pass
