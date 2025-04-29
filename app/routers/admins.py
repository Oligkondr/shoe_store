from types import new_class

from fastapi import APIRouter, Body
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import session_maker
from app.requests import AdminCreateRequest, Item

from app.auth.auth_handler import sign_jwt
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
def post_test(item: Item):
    return item


@admins_router.post("/signup", summary='Create new admin')
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
    return new_admin
