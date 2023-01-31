from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Depends

from api.dto.tag import TagCreate, TagRead
from api.entity.tag import TagTable
from api.misc.dependencies import db_session

router = APIRouter()

labeled_cols = (
    TagTable.id_.cast(sa.String).label("id"),
    TagTable.name.label("name"),
)

select = sa.select(*labeled_cols)


@router.get("/id/{tag_id}", response_model=TagRead)
async def get_tag_by_id(tag_id: UUID, session=Depends(db_session)):
    return (await session.execute(select.where(TagTable.id_ == tag_id))).one()


@router.get("/name/{name}", response_model=TagRead)
async def get_tag_by_name(name: str, session=Depends(db_session)):
    return (await session.execute(select.where(TagTable.name == name))).one()


@router.get("/", response_model=list[TagRead])
async def list_tags(session=Depends(db_session)):
    return (await session.execute(select)).all()


@router.post("/", response_model=TagRead, name="tag:post_tag")
async def post_tag(tag: TagCreate, session=Depends(db_session)):
    entity = TagTable(name=tag.name)
    session.add(entity)
    await session.commit()
    return TagRead(
        id=entity.id_,
        name=entity.name,
    )


@router.put("/id/{tag_id}", response_model=TagRead)
async def put_tag(tag_id: UUID, tag: TagCreate, session=Depends(db_session)):
    query = (
        sa.update(TagTable)
        .returning(*labeled_cols)
        .where(TagTable.id_ == tag_id)
        .values(
            name=tag.name,
        )
    )
    return (await session.execute(query)).one()


@router.delete("/id/{tag_id}", response_model=TagRead)
async def delete_tag(tag_id: UUID, session=Depends(db_session)):
    query = sa.delete(TagTable).returning(*labeled_cols).where(TagTable.id_ == tag_id)
    return (await session.execute(query)).one()
