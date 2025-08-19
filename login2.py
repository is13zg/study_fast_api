from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from secrets import compare_digest


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)


class User(UserBase):
    password: str = Field(..., min_length=3, max_length=30)


class UserInDb(UserBase):
    hashed_password: str = Field(..., max_length=250)


login_router2 = APIRouter(prefix="/login2", tags=["Login 2"])
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"])


# Симуляция базы данных в виде списка объектов пользователей
USER_DATA = [
    UserInDb(
        **{"username": "user1", "hashed_password": f"{pwd_context.hash('pass1')}"}),
    UserInDb(
        **{"username": "user2", "hashed_password": f"{pwd_context.hash('pass2')}"})
]


def get_user_from_db(username: str):
    for user in USER_DATA:
        if compare_digest(user.username, username):
            return user
    return None


def auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)

    if user is None or not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Basic"})
    return UserBase(username=user.username)


@login_router2.post("/register")
def register_user(user: User):
    found_user = get_user_from_db(user.username)
    if found_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,  # Или 400
            detail="User with this username already exists",
            headers={"X-Error": "User conflict"}
        )
    USER_DATA.append(UserInDb(username=user.username, hashed_password=pwd_context.hash(user.password)))
    return {"message": "register suceses"}


@login_router2.get("/login")
def login_user(current_user: UserBase = Depends(auth_user)):
    return {"message": f"Welcome {current_user.username}"}
