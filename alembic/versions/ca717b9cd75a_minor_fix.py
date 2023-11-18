"""minor fix

Revision ID: ca717b9cd75a
Revises: d25d7d8ee9b7
Create Date: 2023-11-18 20:24:23.052190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca717b9cd75a'
down_revision = 'd25d7d8ee9b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('graduates', sa.Column('picture_name', sa.String(length=2004), nullable=True))
    op.drop_column('graduates', 'user_type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('graduates', sa.Column('user_type', sa.VARCHAR(length=2004), autoincrement=False, nullable=True))
    op.drop_column('graduates', 'picture_name')
    # ### end Alembic commands ###
