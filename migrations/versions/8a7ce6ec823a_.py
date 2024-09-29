"""empty message

Revision ID: 8a7ce6ec823a
Revises: 148051e521f1
Create Date: 2024-09-29 20:11:55.212780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a7ce6ec823a'
down_revision = '148051e521f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.drop_column('was_pay_for_lesson')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('was_pay_for_lesson', sa.INTEGER(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
