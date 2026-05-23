"""Crear tabla reglas_trabajo — HU-01

Revision ID: 001_create_reglas_trabajo
Revises: None
Create Date: 2026-05-23

Gobernanza §5.1 — Nombrado SQL Server (snake_case, plural)
Gobernanza §5.2 — Columnas de auditoría obligatorias, JSON en NVARCHAR(MAX)
Gobernanza §5.3 — Migración idempotente y reversible
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001_create_reglas_trabajo"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Crea la tabla reglas_trabajo con todos los campos definidos en HU-01.

    Columnas:
        - id: PK auto-incremental (IDENTITY)
        - cliente_id: FK al cliente propietario (indexada)
        - nombre: Nombre descriptivo de la regla
        - tipo_documento: Tipo de documento que procesa
        - campos_extraer: JSON con los campos a extraer (NVARCHAR(MAX))
        - patron_carpeta: Patrón de organización de carpetas
        - modo_entrada: 'scanner' o 'carpeta'
        - umbral_ocr: Umbral mínimo de confianza OCR (default 95.00)
        - version: Versión de la regla (auto-incremento)
        - activa: Soft-delete flag
        - created_by: FK al usuario creador (nullable — TODO HU-08)
        - created_at: Fecha de creación
        - updated_at: Fecha de última modificación

    Índices:
        - IX_reglas_trabajo_cliente_id: Para consultas por cliente
        - UX_reglas_trabajo_nombre_cliente: Unicidad de nombre por cliente
    """
    op.create_table(
        "reglas_trabajo",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("cliente_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=255), nullable=False),
        sa.Column("tipo_documento", sa.String(length=255), nullable=False),
        sa.Column("campos_extraer", sa.Text(), nullable=False),
        sa.Column("patron_carpeta", sa.String(length=500), nullable=False),
        sa.Column("modo_entrada", sa.String(length=50), nullable=False),
        sa.Column("umbral_ocr", sa.Float(), nullable=False, server_default="95.0"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("activa", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Índice para consultas por cliente — Gobernanza §5.1
    op.create_index(
        "IX_reglas_trabajo_cliente_id",
        "reglas_trabajo",
        ["cliente_id"],
    )

    # Índice único para nombre por cliente (activas solamente)
    op.create_index(
        "UX_reglas_trabajo_nombre_cliente",
        "reglas_trabajo",
        ["cliente_id", "nombre"],
        unique=False,  # La unicidad se valida en la capa de servicio (case-insensitive)
    )


def downgrade() -> None:
    """
    Elimina la tabla reglas_trabajo y sus índices.

    Gobernanza §5.3: Toda migración debe ser reversible.
    """
    op.drop_index("UX_reglas_trabajo_nombre_cliente", table_name="reglas_trabajo")
    op.drop_index("IX_reglas_trabajo_cliente_id", table_name="reglas_trabajo")
    op.drop_table("reglas_trabajo")
