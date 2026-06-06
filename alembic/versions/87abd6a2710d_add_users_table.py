"""Add users table

Revision ID: 87abd6a2710d
Revises: 03eac5b8bd2b
Create Date: 2026-06-06 15:12:24.302382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87abd6a2710d'
down_revision = '03eac5b8bd2b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(),nullable=False),
                    sa.Column('email', sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
