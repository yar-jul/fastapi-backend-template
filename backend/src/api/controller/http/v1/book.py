from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Depends

from api.dto.book import BookCreate, BookRead
from api.entity.author import AuthorTable
from api.entity.book import BookTable
from api.entity.tag import TagTable
from api.misc.dependencies import db_session

router = APIRouter()

labeled_cols = (
    BookTable.id_.cast(sa.String).label("id"),
    BookTable.name.label("name"),
    BookTable.category_id.cast(sa.String).label("category_id"),
    BookTable.author_id.cast(sa.String).label("author_id"),
    BookTable.tags.label("tags"),
)

select = sa.select(*labeled_cols)


@router.get("/id/{book_id}", response_model=BookRead)
async def get_book_by_id(book_id: UUID, session=Depends(db_session)):
    return (await session.execute(select.where(BookTable.id_ == book_id))).one()


@router.get("/name/{name}", response_model=BookRead)  # TODO same name
async def get_book_by_name(name: str, session=Depends(db_session)):
    return (await session.execute(select.where(BookTable.name == name))).one()


@router.get("/", response_model=list[BookRead])
async def list_books(session=Depends(db_session)):
    return (await session.execute(select)).all()


@router.post("/", response_model=BookRead)
async def post_book(book: BookCreate, session=Depends(db_session)):
    tags = (
        (await session.execute(sa.select(TagTable).where(TagTable.id_ == sa.func.any(book.tags))))
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


@router.put("/id/{book_id}", response_model=BookRead)
async def put_book(book_id: UUID, category: BookCreate, session=Depends(db_session)):
    pass  # TODO


@router.delete("/id/{book_id}", response_model=BookRead)
async def delete_book(book_id: UUID, session=Depends(db_session)):
    query = sa.delete(BookTable).returning(*labeled_cols).where(BookTable.id_ == book_id)
    return (await session.execute(query)).one()
