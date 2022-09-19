from fastapi import APIRouter, HTTPException, status, Depends
from .security import require_user

user_router = APIRouter()

@user_router.get("/")
def self(user_auth: dict = Depends(require_user)):
    user = user_auth["user_auth"]

    response_dict = {
        "key": user["key"],
        "name": user["name"]
    }
    return response_dict