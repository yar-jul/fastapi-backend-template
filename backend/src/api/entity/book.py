import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from api.entity.base_table import BaseTable


class BookTable(BaseTable):
    __tablename__ = "book"

    name = sa.Column(sa.Text, nullable=False, index=True)
    author_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("author.id"))
    author = relationship("AuthorTable", back_populates="books", lazy="selectin")
    category_id = sa.Column(pg.UUID(as_uuid=True), sa.ForeignKey("category.id"))
    tags = relationship("TagTable", secondary="tag_association", back_populates="books")


tag_association = sa.Table(
    "tag_association",
    BaseTable.metadata,
    sa.Column("book_id", sa.ForeignKey("book.id")),
    sa.Column("tag_id", sa.ForeignKey("tag.id")),
    sa.UniqueConstraint("book_id", "tag_id"),
)
