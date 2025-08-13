from fastapi import APIRouter, Response, Cookie, Request
from models import UserLogin, MessageResponse
from hashlib import sha256
from uuid import uuid4

login_router = APIRouter()

users_db = [UserLogin(username="Vasya", password=sha256("paasword1".encode()).hexdigest()),
            UserLogin(username="Masha", password=sha256("paasword2".encode()).hexdigest()),
            UserLogin(username="string", password=sha256("string".encode()).hexdigest())
            ]

# имитируем хранилище сессий
sessions: dict = {}  # это можно хранить в кэше, например в Redis


@login_router.post("/login", tags=["login", ])
async def login(user_login: UserLogin, response: Response) -> MessageResponse:
    for user in users_db:
        if user.username == user_login.username:
            if user.password == sha256(user_login.password.encode()).hexdigest():
                session_token = uuid4()
                response.set_cookie(key="session_token", value=session_token, httponly=True)
                sessions[str(session_token)] = user
                return {"message": f"Login sucses."}
    return {"message": f"User {user_login.username} not registred."}


@login_router.get("/check_user", tags=["login", ])
async def user_info(request: Request):
    session_token = request.cookies.get("session_token")
    user = sessions.get(session_token)
    if user:
        return user

    return {"message": f"Unathorized"}
