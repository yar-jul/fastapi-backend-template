from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Depends

from api.dto.book import BookCreate, BookRead
from api.entity.book import BookTable, tag_association
from api.entity.tag import TagTable
from api.misc.dependencies import db_session

router = APIRouter()

labeled_cols = (
    BookTable.id_.cast(sa.String).label("id"),
    BookTable.name.label("name"),
    BookTable.category_id.cast(sa.String).label("category_id"),
    BookTable.author_id.cast(sa.String).label("author_id"),
)

subquery = (
    sa.select(
        tag_association.c.book_id.label("book_id"),
        tag_association.c.tag_id.label("tag_id"),
        TagTable.name.label("tag_name"),
    )
    .join(TagTable)
    .subquery()
)

select = (
    sa.select(
        *labeled_cols,
        (sa.func.array_agg(subquery.c.tag_name.cast(sa.String))).label("tags"),
    )
    .join(BookTable)
    .group_by(BookTable.id_)
)


@router.get("/id/{book_id}", response_model=BookRead)
async def get_book_by_id(book_id: UUID, session=Depends(db_session)):
    entity = (
        (await session.execute(sa.select(BookTable).where(BookTable.id_ == book_id)))
        .scalars()
        .one()
    )
    return BookRead(
        id=entity.id_,
        name=entity.name,
        category_id=entity.category_id,
        author_id=entity.author_id,
        tags=[item.name for item in entity.tags],
    )


@router.get("/name/{name}", response_model=list[BookRead])
async def get_book_by_name(name: str, session=Depends(db_session)):
    return (await session.execute(select.where(BookTable.name == name))).all()


@router.get("/", response_model=list[BookRead])
async def list_books(session=Depends(db_session)):
    return (await session.execute(select)).all()


@router.post("/", response_model=BookRead)
async def post_book(book: BookCreate, session=Depends(db_session)):
    tags = (
        (await session.execute(sa.select(TagTable).where(TagTable.name == sa.func.any(book.tags))))
        .scalars()
        .all()
    )
    entity = BookTable(
        name=book.name,
        category_id=book.category_id,
        author_id=book.author_id,
        tags=tags,
    )
    session.add(entity)
    await session.commit()

    return BookRead(
        id=entity.id_,
        name=entity.name,
        category_id=entity.category_id,
        author_id=entity.author_id,
        tags=book.tags,
    )
