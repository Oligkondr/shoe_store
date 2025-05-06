from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.config import get_auth_data
from fastapi import Request, HTTPException, status, Depends

from app.database import session_maker
from app.models import Admin, Client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


def get_token(request: Request):
    token = request.headers.get('token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token


def get_current_admin(token: str = Depends(get_token)):
    return get_current_user('admin', token)


def get_current_client(token: str = Depends(get_token)):
    return get_current_user('client', token)


def get_current_user(user_type: str, token: str):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        print('Неверный токен')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    if payload.get('type') != user_type:
        print('Неверный тип')
        print(payload.get('type'))
        print(user_type)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    user_id = payload.get('id')

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

    with session_maker() as session:
        if user_type == 'admin':
            stmt = select(Admin).where(Admin.id == user_id)
        else:
            stmt = select(Client).where(Client.id == user_id)

        result = session.execute(stmt)
        user_db = result.scalar_one_or_none()

    return user_db
