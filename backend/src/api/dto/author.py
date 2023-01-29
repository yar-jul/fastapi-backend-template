from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    name: str
    books: Optional[list[UUID]]


class RetrieveUser(User):
    class Config:
        orm_mode = True

    id_: UUID = Field(alias="id")
