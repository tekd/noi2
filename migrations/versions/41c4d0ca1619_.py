"""Add user_linkedin_info.

Revision ID: 41c4d0ca1619
Revises: 1520c933a172
Create Date: 2016-02-08 10:38:57.384355

"""

# revision identifiers, used by Alembic.
revision = '41c4d0ca1619'
down_revision = '1520c933a172'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_linkedin_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('access_token', sa.String(), nullable=False),
    sa.Column('access_token_expiry', sa.DateTime(), nullable=False),
    sa.Column('user_info', postgresql.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_linkedin_info')
    ### end Alembic commands ###