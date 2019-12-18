"""empty message

Revision ID: 5c09a309a338
Revises: 61655bc3c0bd
Create Date: 2019-12-18 21:33:28.176005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c09a309a338'
down_revision = '61655bc3c0bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answer', sa.Column('image', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('answer', 'image')
    # ### end Alembic commands ###
