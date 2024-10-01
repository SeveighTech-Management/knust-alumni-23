"""Reversion to Completion

Revision ID: d1df67255e4e
Revises: c6dcaf42ec7c
Create Date: 2024-10-01 05:24:33.193098

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d1df67255e4e"
down_revision = "c6dcaf42ec7c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_courses_id", table_name="courses")
    op.drop_table("courses")
    op.drop_index("ix_chat_messages_id", table_name="chat_messages")
    op.drop_table("chat_messages")
    op.drop_index("ix_opportunities_id", table_name="opportunities")
    op.drop_table("opportunities")
    op.drop_index("ix_opportunity_type_id", table_name="opportunity_type")
    op.drop_table("opportunity_type")
    op.drop_index("ix_chat_rooms_id", table_name="chat_rooms")
    op.drop_table("chat_rooms")
    op.drop_index("ix_gender_id", table_name="gender")
    op.drop_table("gender")
    op.drop_index("ix_job_titles_id", table_name="job_titles")
    op.drop_table("job_titles")
    op.drop_index("ix_country_id", table_name="country")
    op.drop_table("country")
    op.drop_index("ix_notifications_id", table_name="notifications")
    op.drop_table("notifications")
    op.drop_index("ix_news_updates_id", table_name="news_updates")
    op.drop_table("news_updates")
    op.drop_index("ix_colleges_id", table_name="colleges")
    op.drop_table("colleges")
    op.drop_constraint("graduates_college_id_fkey", "graduates", type_="foreignkey")
    op.drop_constraint("graduates_course_id_fkey", "graduates", type_="foreignkey")
    op.drop_constraint("graduates_country_id_fkey", "graduates", type_="foreignkey")
    op.drop_constraint("graduates_gender_id_fkey", "graduates", type_="foreignkey")
    op.drop_constraint("graduates_job_id_fkey", "graduates", type_="foreignkey")
    op.drop_column("graduates", "course_id")
    op.drop_column("graduates", "graduate_reference_number")
    op.drop_column("graduates", "phone_number")
    op.drop_column("graduates", "email")
    op.drop_column("graduates", "college_id")
    op.drop_column("graduates", "otp")
    op.drop_column("graduates", "place_of_work")
    op.drop_column("graduates", "gender_id")
    op.drop_column("graduates", "password")
    op.drop_column("graduates", "job_id")
    op.drop_column("graduates", "country_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "graduates",
        sa.Column("country_id", sa.UUID(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "graduates", sa.Column("job_id", sa.UUID(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "graduates",
        sa.Column(
            "password", sa.VARCHAR(length=2004), autoincrement=False, nullable=True
        ),
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
        sa.Column("otp", sa.VARCHAR(length=2004), autoincrement=False, nullable=True),
    )
    op.add_column(
        "graduates",
        sa.Column("college_id", sa.UUID(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "graduates",
        sa.Column("email", sa.VARCHAR(length=2004), autoincrement=False, nullable=True),
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
    op.add_column(
        "graduates",
        sa.Column("course_id", sa.UUID(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "graduates_job_id_fkey", "graduates", "job_titles", ["job_id"], ["id"]
    )
    op.create_foreign_key(
        "graduates_gender_id_fkey", "graduates", "gender", ["gender_id"], ["id"]
    )
    op.create_foreign_key(
        "graduates_country_id_fkey", "graduates", "country", ["country_id"], ["id"]
    )
    op.create_foreign_key(
        "graduates_course_id_fkey", "graduates", "courses", ["course_id"], ["id"]
    )
    op.create_foreign_key(
        "graduates_college_id_fkey", "graduates", "colleges", ["college_id"], ["id"]
    )
    op.create_table(
        "colleges",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("college_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="colleges_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_colleges_id", "colleges", ["id"], unique=False)
    op.create_table(
        "news_updates",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("title", sa.VARCHAR(length=2004), autoincrement=False, nullable=True),
        sa.Column(
            "description", sa.VARCHAR(length=2004), autoincrement=False, nullable=True
        ),
        sa.Column("media", sa.VARCHAR(length=2004), autoincrement=False, nullable=True),
        sa.Column("poster_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["poster_id"], ["graduates.id"], name="news_updates_poster_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="news_updates_pkey"),
    )
    op.create_index("ix_news_updates_id", "news_updates", ["id"], unique=False)
    op.create_table(
        "notifications",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("title", sa.VARCHAR(length=2004), autoincrement=False, nullable=True),
        sa.Column(
            "details", sa.VARCHAR(length=2004), autoincrement=False, nullable=True
        ),
        sa.Column("graduate_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["graduate_id"], ["graduates.id"], name="notifications_graduate_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="notifications_pkey"),
    )
    op.create_index("ix_notifications_id", "notifications", ["id"], unique=False)
    op.create_table(
        "country",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("country_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="country_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_country_id", "country", ["id"], unique=False)
    op.create_table(
        "job_titles",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("job_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="job_titles_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_job_titles_id", "job_titles", ["id"], unique=False)
    op.create_table(
        "gender",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("gender_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="gender_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_gender_id", "gender", ["id"], unique=False)
    op.create_table(
        "chat_rooms",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "chat_name", sa.VARCHAR(length=2004), autoincrement=False, nullable=True
        ),
        sa.Column(
            "chat_description",
            sa.VARCHAR(length=2004),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "chat_picture", sa.VARCHAR(length=2004), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="chat_rooms_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_chat_rooms_id", "chat_rooms", ["id"], unique=False)
    op.create_table(
        "opportunity_type",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "type_name", sa.VARCHAR(length=2004), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="opportunity_type_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_opportunity_type_id", "opportunity_type", ["id"], unique=False)
    op.create_table(
        "opportunities",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("title", sa.VARCHAR(length=2004), autoincrement=False, nullable=True),
        sa.Column(
            "description", sa.VARCHAR(length=2004), autoincrement=False, nullable=True
        ),
        sa.Column("media", sa.VARCHAR(length=2004), autoincrement=False, nullable=True),
        sa.Column("opportunity_type_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column("poster_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["opportunity_type_id"],
            ["opportunity_type.id"],
            name="opportunities_opportunity_type_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["poster_id"], ["graduates.id"], name="opportunities_poster_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="opportunities_pkey"),
    )
    op.create_index("ix_opportunities_id", "opportunities", ["id"], unique=False)
    op.create_table(
        "chat_messages",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("chat_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column("graduate_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["chat_id"], ["chat_rooms.id"], name="chat_messages_chat_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["graduate_id"], ["graduates.id"], name="chat_messages_graduate_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="chat_messages_pkey"),
    )
    op.create_index("ix_chat_messages_id", "chat_messages", ["id"], unique=False)
    op.create_table(
        "courses",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("course_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="courses_pkey"),
    )
    op.create_index("ix_courses_id", "courses", ["id"], unique=False)
    # ### end Alembic commands ###
