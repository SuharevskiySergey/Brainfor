"""empty message

Revision ID: e8143b47223d
Revises: 8a7ce6ec823a
Create Date: 2024-09-30 15:33:52.507656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8143b47223d'
down_revision = '8a7ce6ec823a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.drop_column('monobank')
        batch_op.drop_column('privatbank')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('privatbank', sa.VARCHAR(length=30), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('monobank', sa.VARCHAR(length=30), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
