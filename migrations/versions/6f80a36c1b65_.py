"""empty message

Revision ID: 6f80a36c1b65
Revises: 592e67023629
Create Date: 2024-10-06 22:47:49.841192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f80a36c1b65'
down_revision = '592e67023629'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lessons', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.drop_column('lessons')

    # ### end Alembic commands ###
