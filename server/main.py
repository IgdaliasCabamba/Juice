from fastapi import FastAPI
import src.config as _set
_set.up()

from src.routes import api_app

app = FastAPI()

app.mount(path = "/api", app = api_app, name = "API")