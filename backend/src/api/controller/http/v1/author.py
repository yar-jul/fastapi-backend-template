from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Depends

from api.dto.author import AuthorCreate, AuthorRead, AuthorWithID
from api.entity.author import AuthorTable
from api.entity.book import BookTable
from api.misc.dependencies import db_session

router = APIRouter()

labeled_cols = (
    AuthorTable.id_.cast(sa.String).label("id"),
    AuthorTable.name.label("name"),
)

select = sa.select(*labeled_cols)


@router.get("/id/{author_id}", response_model=AuthorRead)
async def get_author_by_id(author_id: UUID, session=Depends(db_session)):
    entity = (
        (await session.execute(sa.select(AuthorTable).where(AuthorTable.id_ == author_id)))
        .scalars()
        .one()
    )
    return AuthorRead(
        id=entity.id_,
        name=entity.name,
        books=[item.id_ for item in entity.books],
    )


@router.get("/name/{name}", response_model=list[AuthorRead])
async def get_author_by_name(name: str, session=Depends(db_session)):
    select_ = (
        sa.select(
            *labeled_cols,
            (sa.func.array_agg(BookTable.id_.cast(sa.String))).label("books"),
        )
        .join(BookTable, isouter=True)
        .where(AuthorTable.name == name)
        .group_by(AuthorTable.id_)
    )
    entity = (await session.execute(select_)).all()
    return entity


@router.get("/", response_model=list[AuthorRead])
async def list_authors(session=Depends(db_session)):
    select_ = (
        sa.select(
            *labeled_cols,
            (sa.func.array_agg(BookTable.id_.cast(sa.String))).label("books"),
        )
        .join(BookTable, isouter=True)
        .group_by(AuthorTable.id_)
    )
    entity = (await session.execute(select_)).all()
    return entity


@router.post("/", response_model=AuthorWithID)
async def post_author(author: AuthorCreate, session=Depends(db_session)):
    entity = AuthorTable(name=author.name)
    session.add(entity)
    await session.commit()
    return AuthorWithID(id=entity.id_, name=entity.name)


@router.put("/id/{author_id}", response_model=AuthorWithID)
async def put_author(author_id: UUID, author: AuthorCreate, session=Depends(db_session)):
    query = (
        sa.update(AuthorTable)
        .returning(*labeled_cols)
        .where(AuthorTable.id_ == author_id)
        .values(
            name=author.name,
        )
    )
    return (await session.execute(query)).one()


@router.delete("/id/{author_id}", response_model=AuthorWithID)
async def delete_author(author_id: UUID, session=Depends(db_session)):
    query = sa.delete(AuthorTable).returning(*labeled_cols).where(AuthorTable.id_ == author_id)
    return (await session.execute(query)).one()
