"""updated food categories string size

Revision ID: c01bc8211376
Revises: d2682e013c03
Create Date: 2023-12-09 16:32:02.994535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c01bc8211376'
down_revision = 'd2682e013c03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('food_categories', schema=None) as batch_op:
        batch_op.alter_column('FoodCategoryName',
               existing_type=sa.VARCHAR(length=250),
               type_=sa.String(length=500),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('food_categories', schema=None) as batch_op:
        batch_op.alter_column('FoodCategoryName',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=250),
               existing_nullable=True)

    # ### end Alembic commands ###
