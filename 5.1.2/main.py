from fastapi import FastAPI, Depends
from db.database import get_db_connection
import asyncpg
import uvicorn
from models import Todo

app = FastAPI()


@app.post("/add_task")
async def create_item(item: Todo, db: asyncpg.Connection = Depends(get_db_connection)):
    new_task = await db.fetchrow('''
        INSERT INTO tasks (title, description, completed)
        VALUES ($1, $2, $3)
        RETURNING *;
    ''', item.title, item.description, item.completed)

    return dict(new_task)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
