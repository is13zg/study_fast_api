from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from models import User, CreateUser

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r", encoding="utf-8") as f:
        data = f.read()
        return data


@app.post("/calculate")
async def calc(num1: int, num2: int):
    return {"num1": num1, "num2": num2, "result": num1 + num2}


@app.get("/users")
async def get_user():
    user = User(id=1, name="Joh Do")
    return user


@app.post("/add_users")
async def add_user(user: CreateUser):
    return {"age": user.age, "name": user.name, "is_adult": user.age>=18}


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
