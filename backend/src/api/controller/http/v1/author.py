from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Depends

from api.dto.author import AuthorCreate, AuthorPostResponse, AuthorRead
from api.entity.author import AuthorTable
from api.entity.book import BookTable
from api.misc.dependencies import db_session

router = APIRouter()

# TODO rm ?
labeled_cols = (
    AuthorTable.id_.cast(sa.String).label("id"),
    AuthorTable.name.label("name"),
    AuthorTable.books.label("books"),
)

select = sa.select(*labeled_cols)


@router.get("/id/{author_id}", response_model=AuthorRead)
async def get_author_by_id(author_id: UUID, session=Depends(db_session)):
    entity = (await session.execute(sa.select(AuthorTable).where(AuthorTable.id_ == author_id))).scalar()
    return AuthorRead(
        id=entity.id_,
        name=entity.name,
        books=[item.id_ for item in entity.books],
    )


@router.get("/name/{name}", response_model=AuthorRead)  # TODO same name
async def get_author_by_name(name: str, session=Depends(db_session)):
    entity = (await session.execute(sa.select(AuthorTable).where(AuthorTable.name == name))).scalar()
    return AuthorRead(
        id=entity.id_,
        name=entity.name,
        books=[item.id_ for item in entity.books],
    )


@router.get("/", response_model=list[AuthorRead])
async def list_authors(session=Depends(db_session)):
    # TODO select_
    select_ = sa.select(
        AuthorTable.id_.cast(sa.String).label("id"),
        AuthorTable.name.label("name"),
        (sa.func.array_agg(BookTable.id_.cast(sa.String))).label("books"),
    ).join(BookTable, isouter=True).group_by(AuthorTable.id_)
    entity = (await session.execute(select_)).all()
    return entity


@router.post("/", response_model=AuthorPostResponse)
async def post_author(author: AuthorCreate, session=Depends(db_session)):
    entity = AuthorTable(name=author.name)
    session.add(entity)
    await session.commit()
    return AuthorPostResponse(id=entity.id_, name=entity.name)


@router.put("/id/{author_id}", response_model=AuthorRead)
async def put_author(author_id: UUID, category: AuthorCreate, session=Depends(db_session)):
    pass  # TODO


@router.delete("/id/{author_id}", response_model=AuthorRead)
async def delete_author(author_id: UUID, session=Depends(db_session)):
    query = sa.delete(AuthorTable).returning(*labeled_cols).where(AuthorTable.id_ == author_id)
    return (await session.execute(query)).one()
