"""data migration

Revision ID: 425eac3a8416
Revises: c6d73ac95136
Create Date: 2025-11-15 13:13:07.021700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '425eac3a8416'
down_revision: Union[str, Sequence[str], None] = 'c6d73ac95136'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Используем SQL для обновления всех записей сразу
    op.execute(
        """
        UPDATE product 
        SET 
            profitability_readable = profitability,
            agent_profitability_readable = agent_profitability,
            placement_period_readable = placement_period
        """
    )


def downgrade():
    # Очищаем поля _readable при откате
    op.execute(
        """
        UPDATE product 
        SET 
            profitability_readable = NULL,
            agent_profitability_readable = NULL,
            placement_period_readable = NULL
        """
    )