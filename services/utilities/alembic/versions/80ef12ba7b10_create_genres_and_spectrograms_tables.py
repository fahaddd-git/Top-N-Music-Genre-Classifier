"""Create genres and spectrograms tables

Revision ID: 80ef12ba7b10
Revises:
Create Date: 2022-10-26 15:15:24.042421

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "80ef12ba7b10"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text, nullable=False, unique=True),
    )
    op.create_table(
        "spectrograms",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("genre_id", sa.Integer, sa.ForeignKey("genres.id")),
        sa.Column("image_data", sa.LargeBinary, nullable=False),
        sa.Column("last_modified", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("spectrograms")
    op.drop_table("genres")
