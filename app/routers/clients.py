from fastapi import APIRouter

from app.models import Client
from app.database import session_maker
from app.requests import ClientCreateRequest

clients_router = APIRouter(prefix="/api/v1", tags=["client"])


@clients_router.get('/test', summary='Test get request')
async def test():
    return {'message': 'GET from client'}


@clients_router.post("/register", summary='Create new client')
def create_admin(client: ClientCreateRequest):
    with session_maker() as session:
        new_client = Client(
            email=client.email,
            phone=client.phone,
            name=client.name,
            surname=client.surname,
        )
        new_client.set_password(client.password)

        session.add(new_client)
        session.commit()
    return {'success': True}
