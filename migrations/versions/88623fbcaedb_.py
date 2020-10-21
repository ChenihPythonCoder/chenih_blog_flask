"""empty message

Revision ID: 88623fbcaedb
Revises: bc6f22e4a08d
Create Date: 2020-10-08 13:23:25.097715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88623fbcaedb'
down_revision = 'bc6f22e4a08d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type_name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('article', sa.Column('type_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'article', 'article_type', ['type_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'article', type_='foreignkey')
    op.drop_column('article', 'type_id')
    op.drop_table('article_type')
    # ### end Alembic commands ###