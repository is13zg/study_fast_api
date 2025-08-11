from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class CreateUser(BaseModel):
    name: str
    age:int