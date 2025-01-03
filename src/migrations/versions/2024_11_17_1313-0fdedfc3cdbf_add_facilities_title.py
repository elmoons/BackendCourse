"""add facilities title

Revision ID: 0fdedfc3cdbf
Revises: 16f9bf6d9841
Create Date: 2024-11-17 13:13:07.659211

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0fdedfc3cdbf"
down_revision: Union[str, None] = "16f9bf6d9841"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("facilities", sa.Column("title", sa.String(length=100), nullable=False))
    op.drop_column("facilities", "tittle")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "facilities",
        sa.Column("tittle", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    )
    op.drop_column("facilities", "title")
    # ### end Alembic commands ###
