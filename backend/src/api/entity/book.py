import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from api.entity.author import AuthorTable
from api.entity.base_table import BaseTable
from api.entity.category import CategoryTable
from api.entity.tag import TagTable


class BookTable(BaseTable):
    __tablename__ = "book"

    name = sa.Column(sa.Text, nullable=False, index=True, unique=True)

    category_id = sa.Column(
        pg.UUID(as_uuid=True), sa.ForeignKey(CategoryTable.id_), unique=True
    )

    author_id = sa.Column(
        pg.UUID(as_uuid=True), sa.ForeignKey(AuthorTable.id_), unique=True
    )
    author = relationship(AuthorTable, back_populates="books")  # TODO lazy

    tags = relationship(
        TagTable, secondary="tag_association", back_populates="books"
    )  # TODO lazy


tag_association = sa.Table(
    "tag_association",
    BaseTable.metadata,
    sa.Column("book_id", sa.ForeignKey("book.id")),
    sa.Column("tag_id", sa.ForeignKey("tag.id")),
    sa.UniqueConstraint("book_id", "tag_id"),
)
