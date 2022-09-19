from fastapi import APIRouter, HTTPException, status, Depends
from .model import Passwords, CreatePasswordModel
from .security import require_user

passwords_router = APIRouter()

@passwords_router.post("/")
async def insert_key(password: CreatePasswordModel, user_auth: dict = Depends(require_user)):
    user = user_auth["user_auth"]
    password_id = password.id
    del password.id

    password_dict = {
        "owner": user["key"],
        "data": password.json()
    }
    if Passwords.fetch({"key" : password_id}).items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    res = Passwords.insert(data = password_dict, key = password_id)

    return {"id": res["key"]}

@passwords_router.get("/")
async def all_keys(user_auth: dict = Depends(require_user)) -> dict:
    user = user_auth["user_auth"]
    all_keys = Passwords.fetch({"owner": user["key"]}, limit=999)
    
    response_list = []
    
    for item in all_keys.items:
        response_list.append({"id": item["key"]})

    return {"passwords": response_list}

@passwords_router.get("/{name}")
async def key_by_name(name:str, user_auth: dict = Depends(require_user)) -> dict:
    user = user_auth["user_auth"]
    password = Passwords.get(name)
    

    if password["owner"] == user["key"]:
        password_response = {
            "service": password["service"],
            "description": password["description"],
            "password": password["password"],
            "id": password["key"]
        }

        return password_response
    
    raise HTTPException(status.HTTP_404_NOT_FOUND)
    