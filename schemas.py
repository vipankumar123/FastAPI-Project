from argparse import OPTIONAL
from pydantic import BaseModel
from typing import Optional


class SignupModel(BaseModel):
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example':{
                "username":"vipan123",
                "email":"vipan@gmail.com",
                "password":"vipan",
                "is_staff":False, # True only staff members
                "is_active":True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key:str='0f3bed5e5662d193c11b4de06348fe781181cea84a4b442de0877c70d9fcf3e9'

class LoginModel(BaseModel):
    username:str
    password:str

class OrderModel(BaseModel):
    id : Optional[int]
    quantity : int
    order_status : Optional[str]="PENDING"
    pizza_size : Optional[str]='SMALL'
    user_id : Optional[int]

    class Congif:
        orm_mode = True
        schema_extra = {
            "example":{
                "quantity":2,
                "order_status":"LARGE",

            }
        }

