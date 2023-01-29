import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm.decl_api import DeclarativeMeta


class BaseTable(metaclass=DeclarativeMeta):
    __abstract__ = True

    id_ = sa.Column(
        "id",
        pg.UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    )
