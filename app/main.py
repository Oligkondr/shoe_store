from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

from app.responses import ErrorResponseModel
from app.routers.admins import admins_router
from app.routers.clients import clients_router

app = FastAPI()

app.include_router(admins_router)
app.include_router(clients_router)


@app.exception_handler(HTTPException)
def http_exception_handler(request, exc: HTTPException):
    error_response = ErrorResponseModel(success=False, error=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=error_response.dict())
