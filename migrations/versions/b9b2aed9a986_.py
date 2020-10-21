"""empty message

Revision ID: b9b2aed9a986
Revises: 
Create Date: 2020-10-06 18:35:12.351409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9b2aed9a986'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('icon', sa.String(length=100), nullable=True),
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('registerdatetime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('article',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('pdatetime', sa.DateTime(), nullable=True),
    sa.Column('click_num', sa.Integer(), nullable=True),
    sa.Column('save_num', sa.Integer(), nullable=True),
    sa.Column('love_num', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article')
    op.drop_table('user')
    # ### end Alembic commands ###
