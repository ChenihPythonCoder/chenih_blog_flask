"""empty message

Revision ID: 6c42276a57ac
Revises: cf46ea89f7be
Create Date: 2020-10-20 16:31:12.963776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c42276a57ac'
down_revision = 'cf46ea89f7be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('about_me',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.BLOB(), nullable=False),
    sa.Column('pdatetime', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'article', 'article_type', ['type_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'article', type_='foreignkey')
    op.drop_table('about_me')
    # ### end Alembic commands ###
