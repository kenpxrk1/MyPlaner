"""fixed task-tag relationship part 2

Revision ID: 3c43d7b35bd5
Revises: 9f911aaf25d7
Create Date: 2024-04-16 13:56:39.605425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c43d7b35bd5'
down_revision: Union[str, None] = '9f911aaf25d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###