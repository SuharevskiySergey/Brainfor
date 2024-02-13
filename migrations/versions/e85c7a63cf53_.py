"""empty message

Revision ID: e85c7a63cf53
Revises: 
Create Date: 2024-01-26 05:42:31.858985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e85c7a63cf53'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_id'), ['id'], unique=False)

    op.create_table('info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('country', sa.String(length=150), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('speed', sa.String(length=120), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('source', sa.String(length=100), nullable=True),
    sa.Column('pay_already', sa.Integer(), nullable=True),
    sa.Column('pass_lesson', sa.Integer(), nullable=True),
    sa.Column('finish_lesson', sa.Integer(), nullable=True),
    sa.Column('was_pay_for_lesson', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_info_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_info_id'))

    op.drop_table('info')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_id'))

    op.drop_table('user')
    # ### end Alembic commands ###
