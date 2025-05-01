from types import new_class

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.auth.auth_handler import create_access_token, verify_password, get_current_admin
from app.database import session_maker
from app.requests import AdminCreateRequest, AdminAuthRequest

from app.models import Admin
from app.config import get_db_url

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


@admins_router.post("/register", summary='Create new admin')
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


@admins_router.post("/login", summary='Login admin')
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
