from fastapi import FastAPI

from fastapi import FastAPI
from .auth import auth_router
from .passwords import passwords_router
from .users import user_router

api_app = FastAPI()
api_app.include_router(auth_router, prefix="/auth")
api_app.include_router(passwords_router, prefix="/keys")
api_app.include_router(user_router, prefix="/user")

@api_app.get("/")
def read_root():
    return {"Juice": "WRLD"}
