from uuid import UUID

from pydantic import BaseModel, Field


class Book(BaseModel):
    name: str
    category_id: UUID
    author_id: UUID
    tags: list[str]


class RetrieveBook(Book):
    class Config:
        orm_mode = True

    id_: UUID = Field(alias="id")
