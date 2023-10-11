"""empty message

Revision ID: ae9747d3dda4
Revises: 079fc58036ad
Create Date: 2023-10-10 14:03:00.470736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae9747d3dda4'
down_revision: Union[str, None] = '079fc58036ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vouchers',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('filename', sa.String(length=60), nullable=False),
    sa.Column('link', sa.String(length=500), nullable=False),
    sa.Column('sale_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['sale_id'], ['sales.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('recipe_detail', 'unit_measure')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe_detail', sa.Column('unit_measure', sa.VARCHAR(length=10), autoincrement=False, nullable=False))
    op.drop_table('vouchers')
    # ### end Alembic commands ###