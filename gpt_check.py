from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from secrets import compare_digest
import datetime
import jwt

jwt_router2 = APIRouter(prefix="/jwt", tags=["Jwt"])
pwd_context = CryptContext(schemes=["bcrypt"])
main_secret = "secret_string"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Увеличил время для тестирования
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/login")  # Исправил URL


# Модели данных
class User(BaseModel):
    username: str


class UserInDb(User):
    hashed_password: str


# Тестовые пользователи
USER_DATA = [
    UserInDb(username="user1", hashed_password=pwd_context.hash("pass1")),
    UserInDb(username="user2", hashed_password=pwd_context.hash("pass2")),
    UserInDb(username="string", hashed_password=pwd_context.hash("string")),
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
    return User(username=user.username)


def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, main_secret, algorithm="HS256")
    return token


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, main_secret, algorithms=["HS256"])
        username = payload.get("username")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@jwt_router2.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Аутентификация пользователя
    user = auth_user(form_data)

    # Генерация JWT токена
    token = create_jwt_token({"username": user.username})

    return {"access_token": token, "token_type": "bearer"}


@jwt_router2.get("/protected_resource")
async def about_me(current_user: str = Depends(get_user_from_token)):
    user = get_user_from_db(current_user)
    if user:
        return {"message": "Access to protected resource", "user": user.username}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
