from hmac import new
import imp
from operator import ne
import re
from urllib import response
from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from auth_routes import Session
from models import User, Order
from schemas import OrderModel
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from database import session, engine


order_router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)

Session = session(bind=engine)


@order_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    return {'message': 'hello guys2!'}


@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order:OrderModel, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    current_user = Authorize.get_jwt_subject()

    user = Session.query(User).filter(User.username==current_user).first()

    new_order=Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity

    )

    new_order.user=user

    Session.add(new_order)

    Session.commit()

    response={
        "pizza_size":new_order.pizza_size,
        "quanity":new_order.quantity,
        "id":new_order.id,
        "order_status":new_order.order_status
    }

    return jsonable_encoder(response)