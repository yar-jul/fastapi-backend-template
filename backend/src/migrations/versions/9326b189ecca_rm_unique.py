"""rm_unique

Revision ID: 9326b189ecca
Revises: ba3f769e7a4c
Create Date: 2023-01-30 18:38:15.618004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9326b189ecca'
down_revision = 'ba3f769e7a4c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_author_name', table_name='author')
    op.create_index(op.f('ix_author_name'), 'author', ['name'], unique=False)
    op.drop_constraint('book_author_id_key', 'book', type_='unique')
    op.drop_constraint('book_category_id_key', 'book', type_='unique')
    op.drop_index('ix_book_name', table_name='book')
    op.create_index(op.f('ix_book_name'), 'book', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_book_name'), table_name='book')
    op.create_index('ix_book_name', 'book', ['name'], unique=False)
    op.create_unique_constraint('book_category_id_key', 'book', ['category_id'])
    op.create_unique_constraint('book_author_id_key', 'book', ['author_id'])
    op.drop_index(op.f('ix_author_name'), table_name='author')
    op.create_index('ix_author_name', 'author', ['name'], unique=False)
    # ### end Alembic commands ###
