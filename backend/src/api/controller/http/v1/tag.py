from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Depends

from api.dto.tag import RetrieveTag, Tag
from api.entity.tag import TagTable
from api.misc.dependencies import db_session

router = APIRouter()

labeled_cols = (
    TagTable.id_.cast(sa.String).label("id"),
    TagTable.name.label("name"),
)

select = sa.select(*labeled_cols)


@router.get("/id/{id_}", response_model=RetrieveTag)
async def get_tag_by_id(id_: UUID, session=Depends(db_session)):
    return (await session.execute(select.where(TagTable.id_ == id_))).one()


@router.get("/name/{name}", response_model=RetrieveTag)
async def get_tag_by_name(name: str, session=Depends(db_session)):
    return (await session.execute(select.where(TagTable.name == name))).one()


@router.get("/", response_model=list[RetrieveTag])
async def list_tags(session=Depends(db_session)):
    return (await session.execute(select)).all()


@router.post("/", response_model=RetrieveTag)
async def post_tag(tag: Tag, session=Depends(db_session)):
    entity = TagTable(name=tag.name)
    session.add(entity)
    await session.commit()
    return RetrieveTag(
        id=entity.id_,
        name=entity.name,
    )


@router.put("/id/{id_}", response_model=RetrieveTag)
async def put_tag(id_: UUID, tag: Tag, session=Depends(db_session)):
    query = (
        sa.update(TagTable)
        .returning(*labeled_cols)
        .where(TagTable.id_ == id_)
        .values(
            name=tag.name,
        )
    )
    return (await session.execute(query)).one()


@router.delete("/id/{id_}", response_model=RetrieveTag)
async def delete_tag(id_: UUID, session=Depends(db_session)):
    query = sa.delete(TagTable).returning(*labeled_cols).where(TagTable.id_ == id_)
    return (await session.execute(query)).one()
