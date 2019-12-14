"""ID type is BigInteger

Revision ID: e82cc2d7df75
Revises: 0c97f1e73f83
Create Date: 2019-12-14 17:06:15.490331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e82cc2d7df75'
down_revision = '0c97f1e73f83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answer', 'id_',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    op.alter_column('answer', 'question_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('answer_guess', 'answer_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('answer_guess', 'guess_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('answer_guess', 'id_',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    op.alter_column('guess', 'id_',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    op.alter_column('guess', 'quiz_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('question', 'id_',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    op.alter_column('question', 'index',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('question', 'quiz_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('quiz', 'id_',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('quiz', 'id_',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    op.alter_column('question', 'quiz_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('question', 'index',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('question', 'id_',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    op.alter_column('guess', 'quiz_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('guess', 'id_',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    op.alter_column('answer_guess', 'id_',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    op.alter_column('answer_guess', 'guess_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('answer_guess', 'answer_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('answer', 'question_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('answer', 'id_',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    # ### end Alembic commands ###
