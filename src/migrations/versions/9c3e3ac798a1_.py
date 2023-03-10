"""empty message

Revision ID: 9c3e3ac798a1
Revises: 
Create Date: 2023-02-14 20:39:08.424433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c3e3ac798a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('short_url',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('redirect_url', sa.String(length=1024), nullable=False),
    sa.Column('short_url', sa.String(length=64), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('valid_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('short_url')
    # ### end Alembic commands ###
