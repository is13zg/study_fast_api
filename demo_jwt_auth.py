from fastapi import APIRouter
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from login2 import User, UserInDb
from passlib.context import CryptContext
from secrets import compare_digest
import datetime

import jwt

jwt_router = APIRouter(prefix="/jwt", tags=["Jwt"])
pwd_context = CryptContext(schemes=["bcrypt"])
main_secret = "secret_string"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/login")

USER_DATA = [
    UserInDb(
        **{"username": "user1", "hashed_password": f"{pwd_context.hash('pass1')}"}
    ),
    UserInDb(
        **{"username": "user2", "hashed_password": f"{pwd_context.hash('pass2')}"}
    ),
    UserInDb(
        **{"username": "string", "hashed_password": f"{pwd_context.hash('string')}"}
    ),
]


def get_user_from_db(username: str):
    for user in USER_DATA:
        if compare_digest(user.username, username):
            return user
    return None


def auth_user(credentials: OAuth2PasswordRequestForm = Depends()):
    user = get_user_from_db(credentials.username)

    if user is None or not pwd_context.verify(
        credentials.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(username=credentials.username, password=credentials.password)


def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now() + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, main_secret, algorithm="HS256")
    return token


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        print(token)
        payload = jwt.decode(token, main_secret, algorithm="HS256")
        print(payload)
        return payload.get("username")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token's time is up",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token 2",
            headers={"WWW-Authenticate": "Bearer"},
        )


@jwt_router.post("/login")
def login(user: User = Depends(auth_user)):
    # генерация jwt  c временем хранения
    token = create_jwt_token(user.model_dump())
    return {"access_token": token, "token_type": "bearer"}


@jwt_router.get("/protected_resource")
async def about_me(current_user: str = Depends(get_user_from_token)):
    user = get_user_from_db(current_user)
    if user:
        return {"message": "Acces to protected resource"}
    # Если пользователь не найден, возвращаем ошибку
    return {"error": "User not found"}
