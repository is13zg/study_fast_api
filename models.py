from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    id: int
    name: str


class CreateUser(BaseModel):
    name: str
    age: int


class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=10)
    message: str = Field(..., min_length=10, max_length=500)

    @field_validator('message')
    def check_message(cls, value: str):
        bad_words = {"редиск", "бяк", "козявка"}
        message_words = set(value.lower().split())
        for bad_word in bad_words:
            for message_word in message_words:
                if message_word.startswith(bad_word):
                    raise ValueError('Цензура')
        return value
