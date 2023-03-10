import sqlalchemy as sa
from sqlalchemy.orm import relationship

from api.entity.base_table import BaseTable


class AuthorTable(BaseTable):
    __tablename__ = "author"

    name = sa.Column(sa.Text, nullable=False, index=True)
    books = relationship("BookTable", back_populates="author", lazy="selectin")
