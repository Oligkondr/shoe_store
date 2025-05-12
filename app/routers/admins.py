from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.auth.auth_handler import create_access_token, verify_password
from app.database import session_maker
from app.requests import AdminCreateRequest, UserAuthRequest

from app.models import Admin, Product, ModelColor, Color, Model, ProductSize
from app.responses import UserRegisterResponse, UserLoginResponse

admins_router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


# @admins_router.get('/test', summary='Test get request')
# def get_test():
#     return {'message': 'Test get request'}
#
#
# @admins_router.post('/test', summary='Test post request')
# def post_test(admin: Admin = Depends(get_current_admin)):
#     return {'message': admin}


@admins_router.get('/products', summary='Get all products')
def get_all_products():
    with (session_maker() as session):
        smtm = select(Product)
        result = session.execute(smtm).unique().scalars().all()
    return result


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
