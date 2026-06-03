"""create scores table

Revision ID: 0001_create_scores_table
Revises: 
Create Date: 2026-06-03
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_scores_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'scores',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('player_name', sa.String(length=3), nullable=False),
        sa.Column('clear_time_ms', sa.Integer, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )


def downgrade() -> None:
    op.drop_table('scores')
