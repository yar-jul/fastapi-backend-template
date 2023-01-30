from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Depends

from api.dto.catefory import CategoryCreate, CategoryRead
from api.entity.category import CategoryTable
from api.misc.dependencies import db_session

router = APIRouter()

labeled_cols = (
    CategoryTable.id_.cast(sa.String).label("id"),
    CategoryTable.name.label("name"),
)

select = sa.select(*labeled_cols)


@router.get("/id/{id_}", response_model=CategoryRead)
async def get_category_by_id(id_: UUID, session=Depends(db_session)):
    return (await session.execute(select.where(CategoryTable.id_ == id_))).one()


@router.get("/name/{name}", response_model=CategoryRead)
async def get_category_by_name(name: str, session=Depends(db_session)):
    return (await session.execute(select.where(CategoryTable.name == name))).one()


@router.get("/", response_model=list[CategoryRead])
async def list_categorys(session=Depends(db_session)):
    return (await session.execute(select)).all()


@router.post("/", response_model=CategoryRead)
async def post_category(category: CategoryCreate, session=Depends(db_session)):
    entity = CategoryTable(name=category.name)
    session.add(entity)
    await session.commit()
    return CategoryRead(
        id=entity.id_,
        name=entity.name,
    )


@router.put("/id/{id_}", response_model=CategoryRead)
async def put_category(id_: UUID, category: CategoryCreate, session=Depends(db_session)):
    query = (
        sa.update(CategoryTable)
        .returning(*labeled_cols)
        .where(CategoryTable.id_ == id_)
        .values(
            name=category.name,
        )
    )
    return (await session.execute(query)).one()


@router.delete("/id/{id_}", response_model=CategoryRead)
async def delete_category(id_: UUID, session=Depends(db_session)):
    query = sa.delete(CategoryTable).returning(*labeled_cols).where(CategoryTable.id_ == id_)
    return (await session.execute(query)).one()
