"""empty message

Revision ID: ae4765ee9ca8
Revises: 1bacfb738b09
Create Date: 2024-09-15 13:38:24.075417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae4765ee9ca8'
down_revision = '1bacfb738b09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partcourses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assrep', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partcourses', schema=None) as batch_op:
        batch_op.drop_column('assrep')

    # ### end Alembic commands ###
