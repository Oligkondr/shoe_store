from fastapi import APIRouter

clients_router = APIRouter(prefix="/api/v1", tags=["client"])


@clients_router.get('/test', summary='Test get request')
async def test():
    return {'message': 'GET from client'}

