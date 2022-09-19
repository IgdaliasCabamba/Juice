import src.config as _set
_set.up()

from fastapi import FastAPI, responses
from src.routes import api_app

app = FastAPI()

app.mount(path = "/api", app = api_app, name = "API")

@app.get("/")
def index():
    return responses.RedirectResponse("/api")