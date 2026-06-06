"""Add content column to posts table

Revision ID: 03eac5b8bd2b
Revises: 110e7fea5a85
Create Date: 2026-06-06 14:58:25.060524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03eac5b8bd2b'
down_revision = '110e7fea5a85'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
