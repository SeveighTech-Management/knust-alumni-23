"""Graduate description

Revision ID: ff5421c60a0c
Revises: 52f1cceb2d2c
Create Date: 2024-03-26 17:51:47.260032

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ff5421c60a0c"
down_revision = "52f1cceb2d2c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "graduates",
        sa.Column("graduate_description", sa.String(length=2004), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("graduates", "graduate_description")
    # ### end Alembic commands ###
