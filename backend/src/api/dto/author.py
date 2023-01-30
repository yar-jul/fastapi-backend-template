from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class AuthorCreate(BaseModel):
    name: str


class AuthorWithID(AuthorCreate):
    class Config:
        orm_mode = True

    id_: UUID = Field(alias="id")


class AuthorRead(AuthorWithID):
    books: Optional[list[Optional[UUID]]]

    @validator("books")
    def books_empty_list(cls, value):
        if value == [None]:
            return []
        return value
