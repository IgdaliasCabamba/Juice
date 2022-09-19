import json
import os

def up():
    with open("core/secrets.json", "r") as fp:
        data = json.load(fp)
        os.environ["API_AUTH_TOKEN"] = data["api_token"]
        os.environ["PROJECT_KEY"] = data["project_key"]
        os.environ["CRYPT_KEY"] = data["fernet_key"]