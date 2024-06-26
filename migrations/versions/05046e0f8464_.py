"""empty message

Revision ID: 05046e0f8464
Revises: 
Create Date: 2024-03-03 07:38:36.215480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05046e0f8464'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cource',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('to_student', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['to_student'], ['info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('cource', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_cource_id'), ['id'], unique=False)

    op.create_table('partcourses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_course', sa.Integer(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('rypma', sa.DateTime(), nullable=True),
    sa.Column('sympfany', sa.DateTime(), nullable=True),
    sa.Column('repeated', sa.DateTime(), nullable=True),
    sa.Column('proninciation', sa.DateTime(), nullable=True),
    sa.Column('speacking', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id_course'], ['cource.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('partcourses', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_partcourses_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partcourses', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_partcourses_id'))

    op.drop_table('partcourses')
    with op.batch_alter_table('cource', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_cource_id'))

    op.drop_table('cource')
    # ### end Alembic commands ###
