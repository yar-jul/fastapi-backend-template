from uuid import UUID

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    name: str


class TagRead(TagCreate):
    class Config:
        orm_mode = True

    id_: UUID = Field(alias="id")
