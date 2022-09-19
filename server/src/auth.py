from fastapi import APIRouter, Response, HTTPException, status
import os
from .model import Users
from .security import Security

auth_router = APIRouter()

@auth_router.post("/signup")
def signup(api_token: str, name: str, password: str) -> dict:

    if os.environ["API_AUTH_TOKEN"] != api_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    
    users_res = Users.fetch({"name":name})

    if users_res.items:
        raise HTTPException(status.HTTP_409_CONFLICT,
                            detail="user already exist")

    Users.insert({"password": Security.hash_password(password), "name": name})

    user = Users.fetch({"name": name}).items[0]

    response_dict = {
        "key": user["key"],
        "name": user["name"]
    }

    return response_dict

@auth_router.post("/login")
def login(response: Response, name: str, password: str) -> dict:
    user_res = Users.fetch({"name": name})
    
    if not user_res.items:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    user_key = user_res.items[0]["key"]
    user:dict = Users.get(user_key)

    if not Security.verify_password(password, user["password"]):
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    
    encrypted_user_key = Security.encrypt_cookie(user_key)

    response.set_cookie(key="user", value=encrypted_user_key, httponly=True)
    return {"token": encrypted_user_key}

@auth_router.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="user")
    return {"user": None}