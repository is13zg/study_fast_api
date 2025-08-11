from fastapi import FastAPI
from  fastapi.responses import HTMLResponse
import uvicorn


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r", encoding="utf-8") as f:
        data = f.read()
        return data

@app.post("/calculate")
async def calc(num1: int, num2: int):
    return {"num1": num1, "num2": num2, "result":num1 + num2}

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
