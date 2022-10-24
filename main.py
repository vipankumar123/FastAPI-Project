import imp
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from schemas import Settings

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()