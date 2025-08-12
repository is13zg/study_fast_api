from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from models import User, CreateUser, Feedback

app = FastAPI()

# Пример пользовательских данных (для демонстрационных целей)
fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
    3: {"username": "alice_jones", "email": "alice@example.com"},
    4: {"username": "bob_white", "email": "bob@example.com"},
}

fake_feedbacks = [{
    "name": "Alice",
    "message": "Отличный курс, я многое узнаю, а также закрепляю знания на практике!"
}]


@app.post("/feedback")
async def put_feeedback(fd: Feedback):
    fake_feedbacks.append(fd)
    return {
        "message": f"Feedback received. Thank you, {fd.name}."
    }


@app.get("/feedbacks")
async def get_feeedbacks():
    return {
        "feedbacks": fake_feedbacks
    }


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
    return {"age": user.age, "name": user.name, "is_adult": user.age >= 18}


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
