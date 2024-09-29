"""empty message

Revision ID: 148051e521f1
Revises: ae4765ee9ca8
Create Date: 2024-09-29 20:09:56.521370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '148051e521f1'
down_revision = 'ae4765ee9ca8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('monobank', sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column('privatbank', sa.String(length=30), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.drop_column('privatbank')
        batch_op.drop_column('monobank')

    # ### end Alembic commands ###
