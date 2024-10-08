"""Reversion to Completion

Revision ID: 5a9a0af3620e
Revises: d1df67255e4e
Create Date: 2024-10-01 05:30:51.441879

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5a9a0af3620e"
down_revision = "d1df67255e4e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("graduates", "graduate_reference_number")
    op.drop_column("graduates", "phone_number")
    op.drop_column("graduates", "college_id")
    op.drop_column("graduates", "otp")
    op.drop_column("graduates", "job_id")
    op.drop_column("graduates", "course_id")
    op.drop_column("graduates", "email")
    op.drop_column("graduates", "password")
    op.drop_column("graduates", "place_of_work")
    op.drop_column("graduates", "gender_id")
    op.drop_column("graduates", "country_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "graduates",
        sa.Column("country_id", sa.UUID(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "graduates",
        sa.Column("gender_id", sa.UUID(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "graduates",
        sa.Column(
            "place_of_work", sa.VARCHAR(length=2004), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "graduates",
        sa.Column(
            "password", sa.VARCHAR(length=2004), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "graduates",
        sa.Column("email", sa.VARCHAR(length=2004), autoincrement=False, nullable=True),
    )
    op.add_column(
        "graduates",
        sa.Column("course_id", sa.UUID(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "graduates", sa.Column("job_id", sa.UUID(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "graduates",
        sa.Column("otp", sa.VARCHAR(length=2004), autoincrement=False, nullable=True),
    )
    op.add_column(
        "graduates",
        sa.Column("college_id", sa.UUID(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "graduates",
        sa.Column(
            "phone_number", sa.VARCHAR(length=2004), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "graduates",
        sa.Column(
            "graduate_reference_number",
            sa.VARCHAR(length=2004),
            autoincrement=False,
            nullable=True,
        ),
    )
    # ### end Alembic commands ###
