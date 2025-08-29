from fastapi import FastAPI, Depends, HTTPException, status
from db.database import get_db_connection
import asyncpg
import uvicorn
from models import Todo

app = FastAPI()


@app.post("/add_task")
async def create_item(item: Todo, db: asyncpg.Connection = Depends(get_db_connection)):
    new_task = await db.fetchrow(
        """
        INSERT INTO tasks (title, description, completed)
        VALUES ($1, $2, $3)
        RETURNING *;
    """,
        item.title,
        item.description,
        item.completed,
    )

    return dict(new_task)


async def get_task_by_id(
        id: int, db: asyncpg.Connection
) -> Todo | None:
    return await db.fetchrow(
        """
                SELECT id, title, description, completed
                FROM tasks 
                WHERE id = $1;
            """,
        id,
    )


@app.get("/task/{id}")
async def get_task(id: int,  db: asyncpg.Connection = Depends(get_db_connection)):
    task = await get_task_by_id(id,db)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id = {id} not found.",
        )

    return dict(task)


@app.put("/upd_task")
async def upd_task(item: Todo, db: asyncpg.Connection = Depends(get_db_connection)):
    task = await get_task_by_id(item.id, db)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id = {item.id} not found.",
        )
    update_task = await db.fetchrow(
        """
        UPDATE tasks
        SET title = $2,
            description = $3,
            completed = $4
        WHERE id = $1
        RETURNING *
        """,
        item.id,
        item.title,
        item.description,
        item.completed,
    )

    return dict(update_task)


@app.delete("/del_task/{id}")
async def del_task(id: int, db: asyncpg.Connection = Depends(get_db_connection)):
    deleted_count = await db.execute("DELETE FROM tasks WHERE id = $1", id)

    if deleted_count == "DELETE 0":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id = {id} not found.",
        )

    else:

        return {"message": f"task with id {id} delete secusesfully."}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
