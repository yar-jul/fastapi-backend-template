import sqlalchemy as sa

from api.entity.base_table import BaseTable


class CategoryTable(BaseTable):
    __tablename__ = "category"

    name = sa.Column(sa.Text, nullable=False, index=True, unique=True)
