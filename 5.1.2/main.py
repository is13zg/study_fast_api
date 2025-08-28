from fastapi import FastAPI, Depends
from pydantic import BaseModel
from db.database import get_db_connection
import asyncpg
import uvicorn

app = FastAPI()

class Item(BaseModel):
    name: str

@app.post("/items")
async def create_item(item: Item, db: asyncpg.Connection = Depends(get_db_connection)):
    await db.execute('''
        INSERT INTO items(name) VALUES($1)
    ''', item.name)
    return {"message": "Item added successfully!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload= True)