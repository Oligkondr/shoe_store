from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.auth.auth_handler import create_access_token, verify_password, get_current_admin
from app.database import session_maker
from app.requests import AdminCreateRequest, UserAuthRequest

from app.models import Admin, Product, ModelColor, Color, Model, SizeGrid
from app.responses.responses import UserRegisterResponse, UserLoginResponse

admins_router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@admins_router.get('/test', summary='Test get request')
def get_test():
    return {'message': 'Test get request'}


@admins_router.post('/test', summary='Test post request')
def post_test(admin: Admin = Depends(get_current_admin)):
    return {'message': admin}


@admins_router.post("/register", summary='Create new admin', response_model=UserRegisterResponse)
def create_admin(admin: AdminCreateRequest):
    with session_maker() as session:
        new_admin = Admin(
            email=admin.email,
            phone=admin.phone,
            name=admin.name,
            surname=admin.surname,
            patronymic=admin.patronymic,
            is_super=admin.is_super,
        )
        new_admin.set_password(admin.password)

        session.add(new_admin)
        session.commit()
    return {'success': True}


@admins_router.post("/login", summary='Login admin', response_model=UserLoginResponse)
def login_admin(admin: UserAuthRequest):
    with session_maker() as session:
        stmt = select(Admin).where(Admin.email == admin.email)
        result = session.execute(stmt)
        admin_db = result.scalar_one_or_none()

    if admin_db is None or verify_password(plain_password=admin.password, hashed_password=admin_db.password) is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')

    access_token = create_access_token({
        'id': admin_db.id,
        'type': 'admin',
    })

    return {'token': access_token}


@admins_router.get('/products', summary='Get all products', responses={
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
    with (session_maker() as session):
        smtm = select(Product).options(
            joinedload(Product.model_color).subqueryload(ModelColor.color).subqueryload(Color.base_colors),
            joinedload(Product.model_color).subqueryload(ModelColor.model).subqueryload(Model.category),
            joinedload(Product.size_grid).subqueryload(SizeGrid.size),
        )
        result = session.execute(smtm).unique().scalars().all()
    return result


# @admins_router.post('/products', summary='Create new product')
# def get_all_products():
#     return {'message': 'Create new product'}
#
#
# @admins_router.post(f'/products/{id}', summary='Change product')
# def get_all_products():
#     return {'message': 'Change product'}
#
#
# @admins_router.delete(f'/products/{id}', summary='Delete product')
# def get_all_products():
#     return {'message': 'Delete product'}
#
#
# @admins_router.post(f'/colors', summary='Create new color')
# def get_all_products():
#     return {'message': 'Create new color'}
#
#
# @admins_router.delete(f'/colors/{id}', summary='Delete color')
# def delete_color():
#     return {'message': 'Delete color'}
#
#
# @admins_router.get(f'/orders', summary='Get all orders')
# def get_all_orders():
#     return {'message': 'Get all orders'}
#
#
# @admins_router.post(f'/orders/{id}', summary='Change order status')
# def change_order_status():
#     return {'message': 'Change order status'}
#
#
# @admins_router.get(f'/profile', summary='Get profile info')
# def get_profile_info():
#     return {'message': 'Get profile info'}
#
#
# @admins_router.post(f'/profile/{id}', summary='Change profile info')
# def change_profile_info():
#     return {'message': 'Change profile info'}
