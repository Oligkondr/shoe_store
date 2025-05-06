from fastapi import FastAPI
from app.routers.admins import admins_router
from app.routers.clients import clients_router

app = FastAPI()


@app.get("/test", summary='Server test')
def test():
    return {'message': True}


app.include_router(admins_router)
app.include_router(clients_router)
