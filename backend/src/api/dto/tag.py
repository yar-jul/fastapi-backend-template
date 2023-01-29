from uuid import UUID

from pydantic import BaseModel, Field


class Tag(BaseModel):
    name: str


class RetrieveTag(Tag):
    class Config:
        orm_mode = True

    id_: UUID = Field(alias="id")
