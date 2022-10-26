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


#login route

@auth_router.post('/login')
async def login(user:LoginModel, Authorize:AuthJWT=Depends()):
    """
        This router is used for login a user
    """
    db_user = Session.query(User).filter(User.username==user.username).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)
    
        response={
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="invalid username and password!") 

#refresh token

@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="please provide a valid refresh token!")
    
    current_user = Authorize.get_jwt_subject()

    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access": access_token})

