from uuid import UUID

from pydantic import BaseModel, Field


class Category(BaseModel):
    name: str


class RetrieveCategory(Category):
    class Config:
        orm_mode = True

    id_: UUID = Field(alias="id")
