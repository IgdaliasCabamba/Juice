from deta import Deta
from typing import Union
from pydantic import BaseModel

import os

class CreatePasswordModel(BaseModel):
    id: str
    service: str
    description: Union[str, None] = None
    password: str


deta = Deta(os.environ["PROJECT_KEY"])
Users = deta.Base('UserDB')
Passwords = deta.Base('KeyDB')

class Manager:
    
    @staticmethod
    def drop_users() -> bool:
        try:
            for item in Users.fetch().items:
                Users.delete(item["key"])
        except Exception as e:
            print(e)
            return False    

        return True

    @staticmethod
    def drop_passwords() -> bool:
        try:
            for item in Passwords.fetch().items:
                Passwords.delete(item["key"])
        
        except Exception as e:
            print(e)
            return False    
            
        return True