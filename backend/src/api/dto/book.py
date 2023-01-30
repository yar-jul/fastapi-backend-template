from uuid import UUID

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    name: str
    category_id: UUID
    author_id: UUID
    tags: list[str]


class BookRead(BookCreate):
    class Config:
        orm_mode = True

    id_: UUID = Field(alias="id")
