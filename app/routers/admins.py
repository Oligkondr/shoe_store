from types import new_class

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, joinedload

from app.auth.auth_handler import create_access_token, verify_password, get_current_admin
from app.database import session_maker
from app.requests import AdminCreateRequest, AdminAuthRequest

from app.models import Admin, Product, ModelColor, Color, Model
from app.config import get_db_url
from app.responses.responses import AdminLoginResponse, AdminRegisterResponse

admins_router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@admins_router.get('/test', summary='Test get request')
def get_test():
    engine = create_engine(get_db_url())
    session_maker = sessionmaker(engine, expire_on_commit=False)
    with session_maker() as session:
        new_admin = Admin(
            email='admin.email',
            password='admin.password',
            phone='admin.phone',
            name='admin.name',
            surname='admin.surname',
            patronymic='admin.patronymic',
            is_super=True,
        )
        session.add(new_admin)
        session.commit()

    return new_admin


@admins_router.post('/test', summary='Test post request')
def post_test(admin: Admin = Depends(get_current_admin)):
    return {'message': admin}


@admins_router.post("/register", summary='Create new admin', response_model=AdminRegisterResponse)
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


@admins_router.post("/login", summary='Login admin', response_model=AdminLoginResponse)
def login_admin(admin: AdminAuthRequest):
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

    return {'access_token': access_token}


@admins_router.get('/products', summary='Get all products', responses={
    200: {
        "description": "Удачный ответ",
        "content": {
            "application/json": {
                "example":
                    [
                        {
                            "model_color_id": 1,
                            "quantity": 5000,
                            "created_at": "2025-05-03T09:24:38.461000+00:00",
                            "size_id": 1,
                            "price": 5490,
                            "id": 1,
                            "updated_at": "2025-05-03T09:24:39.278000+00:00",
                            "model_color": {
                                "name": "bloody black",
                                "id": 1,
                                "updated_at": "2025-05-03T09:21:26.522000+00:00",
                                "model_id": 1,
                                "color_id": 1,
                                "created_at": "2025-05-03T09:21:24.919000+00:00",
                                "model": {
                                    "name": "super_sneaker",
                                    "category_id": 1,
                                    "created_at": "2025-05-03T09:17:49.297000+00:00",
                                    "description": "best shoes",
                                    "sex_id": 2,
                                    "id": 1,
                                    "updated_at": "2025-05-03T09:17:50.654000+00:00",
                                    "category": {
                                        "name": "sneakers",
                                        "updated_at": "2025-05-03T09:15:40.093000+00:00",
                                        "id": 1,
                                        "created_at": "2025-05-03T09:15:38.225000+00:00"
                                    }
                                },
                                "color": {
                                    "created_at": "2025-05-03T09:14:25.981000+00:00",
                                    "id": 1,
                                    "name": "black, white, red",
                                    "updated_at": "2025-05-03T09:14:27.501000+00:00",
                                    "base_colors": [
                                        {
                                            "id": 1,
                                            "hex": "000000",
                                            "updated_at": "2025-05-03T09:12:30.148000+00:00",
                                            "created_at": "2025-05-03T09:12:28.622000+00:00",
                                            "name": "black"
                                        },
                                        {
                                            "id": 2,
                                            "hex": "ffffff",
                                            "updated_at": "2025-05-03T09:12:48.892000+00:00",
                                            "created_at": "2025-05-03T09:12:46.043000+00:00",
                                            "name": "white"
                                        },
                                        {
                                            "id": 3,
                                            "hex": "ff3333",
                                            "updated_at": "2025-05-03T09:23:13.681000+00:00",
                                            "created_at": "2025-05-03T09:23:12.290000+00:00",
                                            "name": "red"
                                        }
                                    ]
                                }
                            },
                            "size": {
                                "cm": "28",
                                "id": 1,
                                "updated_at": "2025-05-03T09:11:37.359000+00:00",
                                "created_at": "2025-05-03T09:11:35.912000+00:00",
                                "ru": "43"
                            }
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
            joinedload(Product.size),
        )
        result = session.execute(smtm).unique().scalars().all()
    return result


@admins_router.post('/products', summary='Create new product')
def get_all_products():
    return {'message': 'Create new product'}


@admins_router.post(f'/products/{id}', summary='Change product')
def get_all_products():
    return {'message': 'Change product'}


@admins_router.delete(f'/products/{id}', summary='Delete product')
def get_all_products():
    return {'message': 'Delete product'}


@admins_router.post(f'/colors', summary='Create new color')
def get_all_products():
    return {'message': 'Create new color'}


@admins_router.delete(f'/colors/{id}', summary='Delete color')
def delete_color():
    return {'message': 'Delete color'}


@admins_router.get(f'/orders', summary='Get all orders')
def get_all_orders():
    return {'message': 'Get all orders'}


@admins_router.post(f'/orders/{id}', summary='Change order status')
def change_order_status():
    return {'message': 'Change order status'}


@admins_router.get(f'/profile', summary='Get profile info')
def get_profile_info():
    return {'message': 'Get profile info'}


@admins_router.post(f'/profile/{id}', summary='Change profile info')
def change_profile_info():
    return {'message': 'Change profile info'}
