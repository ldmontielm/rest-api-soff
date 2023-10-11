"""empty message

Revision ID: 9cac146568a8
Revises: ae9747d3dda4
Create Date: 2023-10-10 14:08:48.246332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cac146568a8'
down_revision: Union[str, None] = 'ae9747d3dda4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('register_date', sa.DateTime(), nullable=False))
    op.create_unique_constraint(None, 'products', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='unique')
    op.drop_column('products', 'register_date')
    # ### end Alembic commands ###