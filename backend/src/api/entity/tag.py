import sqlalchemy as sa
from sqlalchemy.orm import relationship

from api.entity.base_table import BaseTable


class TagTable(BaseTable):
    __tablename__ = "tag"

    name = sa.Column(sa.Text, nullable=False, index=True, unique=True)
    books = relationship(
        "BookTable", secondary="tag_association", back_populates="tags"
    )  # TODO lazy
