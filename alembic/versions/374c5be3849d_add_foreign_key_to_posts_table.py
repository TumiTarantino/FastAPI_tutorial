"""Add foreign key to posts table

Revision ID: 374c5be3849d
Revises: 87abd6a2710d
Create Date: 2026-06-06 15:32:27.289256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '374c5be3849d'
down_revision = '87abd6a2710d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE' )
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
