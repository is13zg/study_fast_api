from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float


class MessageResponse(BaseModel):
    message: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = Field(default=None, gt=0, lt=130)
    is_subscribed: Optional[bool]


class User(BaseModel):
    id: int
    name: str


class CreateUser(BaseModel):
    name: str
    age: int


class UserContact(BaseModel):
    email: EmailStr = Field(...)
    phone: str = Field(min_length=7, max_length=15)

    @field_validator('phone')
    def check_phone(cls, phone: str):
        if all(x.isdigit() for x in phone):
            return phone
        else:
            raise ValueError('Некоректный номер')


class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=10)
    message: str = Field(..., min_length=10, max_length=500)
    contacts: UserContact

    @field_validator('message')
    def check_message(cls, value: str):
        bad_words = {"редиск", "бяк", "козявка"}
        message_words = set(value.lower().split())
        for bad_word in bad_words:
            for message_word in message_words:
                if message_word.startswith(bad_word):
                    raise ValueError('Цензура')
        return value
