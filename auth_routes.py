from logging import exception
from os import access
from urllib import response
from fastapi import APIRouter, status, Depends
from database import session, engine
from schemas import SignupModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException


auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

Session = session(bind=engine)

@auth_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    return {'message': 'hello guys!'}

@auth_router.post('/signup', response_model=SignupModel, status_code=status.HTTP_201_CREATED)
async def signup(user:SignupModel):
    """
        This router is used for register a user
    """
    db_email = Session.query(User).filter(User.email==user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with this email is already exists"
        )

    db_username = Session.query(User).filter(User.username==user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with this username is already exists"
        )

    new_user = User(
        username = user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_active = user.is_active,
        is_staff = user.is_staff
    )

    Session.add(new_user)

    Session.commit()

    return new_user