from uuid import UUID

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str


class CategoryRead(CategoryCreate):
    class Config:
        orm_mode = True

    id_: UUID = Field(alias="id")
