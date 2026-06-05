"""Create Posts Table

Revision ID: 110e7fea5a85
Revises: 
Create Date: 2026-06-05 17:53:45.357503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '110e7fea5a85'
down_revision = None
branch_labels = None
depends_on = None

#If confused, check alembic docs

def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False) )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
