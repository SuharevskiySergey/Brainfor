"""empty message

Revision ID: 7283c7a5f184
Revises: a4115c826251
Create Date: 2024-02-13 14:25:15.988114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7283c7a5f184'
down_revision = 'a4115c826251'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('graficks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('weekday', sa.Integer(), nullable=True),
    sa.Column('hour', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('graficks', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_graficks_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('graficks', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_graficks_id'))

    op.drop_table('graficks')
    # ### end Alembic commands ###
