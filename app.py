from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Добро пожаловать в моё приложение FastAPI!"}


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
