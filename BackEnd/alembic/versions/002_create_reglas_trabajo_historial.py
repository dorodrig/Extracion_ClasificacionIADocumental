"""Crear tabla reglas_trabajo_historial — HU-01 CA-10

Revision ID: 002_create_reglas_trabajo_historial
Revises: 001_create_reglas_trabajo
Create Date: 2026-05-23

Gobernanza §5.1 — Nombrado SQL Server (snake_case, plural)
Gobernanza §5.3 — Migración idempotente y reversible
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "002_create_reglas_trabajo_historial"
down_revision: Union[str, None] = "001_create_reglas_trabajo"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crea la tabla reglas_trabajo_historial."""
    op.create_table(
        "reglas_trabajo_historial",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("regla_id", sa.Integer(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("snapshot_json", sa.Text(), nullable=False),
        sa.Column("modificado_por", sa.Integer(), nullable=True),
        sa.Column(
            "modificado_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "IX_historial_regla_id",
        "reglas_trabajo_historial",
        ["regla_id"],
    )


def downgrade() -> None:
    """Elimina la tabla reglas_trabajo_historial."""
    op.drop_index("IX_historial_regla_id", table_name="reglas_trabajo_historial")
    op.drop_table("reglas_trabajo_historial")
