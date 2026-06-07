"""Added more columns to posts table

Revision ID: 90722fae534c
Revises: 374c5be3849d
Create Date: 2026-06-06 16:08:13.602587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90722fae534c'
down_revision = '374c5be3849d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
