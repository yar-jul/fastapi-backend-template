import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseTable(Base):
    __abstract__ = True

    metadata: MetaData

    id_ = sa.Column(
        "id",
        pg.UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
        index=True,
    )
