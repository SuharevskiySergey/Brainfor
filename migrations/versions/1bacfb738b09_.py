"""empty message

Revision ID: 1bacfb738b09
Revises: 82a550e65468
Create Date: 2024-08-28 18:00:51.957189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bacfb738b09'
down_revision = '82a550e65468'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('city', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('occupation', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('activa', sa.Boolean(), nullable=True))
        batch_op.drop_column('finish_lesson')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('finish_lesson', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('activa')
        batch_op.drop_column('occupation')
        batch_op.drop_column('city')

    # ### end Alembic commands ###
