"""empty message

Revision ID: 39132eec25ae
Revises: 97bde790a0ce
Create Date: 2024-08-28 03:59:51.444041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39132eec25ae'
down_revision = '97bde790a0ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cashflows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_info', sa.Integer(), nullable=True),
    sa.Column('sum', sa.Float(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('coment', sa.String(length=150), nullable=True),
    sa.ForeignKeyConstraint(['id_info'], ['info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('cashflows', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_cashflows_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cashflows', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_cashflows_id'))

    op.drop_table('cashflows')
    # ### end Alembic commands ###