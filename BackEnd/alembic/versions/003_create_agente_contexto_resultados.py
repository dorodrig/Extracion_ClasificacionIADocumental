"""
003 — Crear tablas agente_contexto_resultados y log_ia_invocaciones.

HU-04 — Agente de Contexto IA (Google Gemini).
CA-12: Tabla de resultados del agente de contexto.
CA-09: Tabla de log de invocaciones IA para control de costos.

Revision ID: 003
Revises: 002
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Crear tablas agente_contexto_resultados y log_ia_invocaciones."""

    # --- agente_contexto_resultados (CA-12) ---
    op.create_table(
        "agente_contexto_resultados",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False,
                  comment="PK auto-incremental (IDENTITY)"),
        sa.Column("documento_id", sa.Integer(), nullable=False,
                  comment="FK al documento procesado"),
        sa.Column("regla_id", sa.Integer(), nullable=False,
                  comment="FK a la regla de trabajo aplicada"),
        sa.Column("tipo_doc_detectado", sa.String(length=100), nullable=True,
                  comment="Tipo de documento detectado por Gemini"),
        sa.Column("campos_extraidos_json", sa.Text(), nullable=True,
                  comment="JSON del paquete de datos limpios con campos extraídos"),
        sa.Column("datos_completos", sa.Boolean(), nullable=False,
                  comment="True si todos los campos obligatorios están presentes y válidos"),
        sa.Column("motivo_rechazo", sa.String(length=500), nullable=True,
                  comment="Motivo del rechazo si datos_completos=false"),
        sa.Column("modelo_ia", sa.String(length=100), nullable=False,
                  comment="Nombre del modelo IA utilizado"),
        sa.Column("tokens_entrada", sa.Integer(), nullable=True,
                  comment="Cantidad de tokens de entrada consumidos"),
        sa.Column("tokens_salida", sa.Integer(), nullable=True,
                  comment="Cantidad de tokens de salida generados"),
        sa.Column("duracion_ms", sa.Integer(), nullable=True,
                  comment="Duración de la invocación en milisegundos"),
        sa.Column("estado", sa.String(length=50), nullable=False,
                  comment="Estado: listo_clasificacion | pendiente_humano | error_ia"),
        sa.Column("processed_at", sa.DateTime(), nullable=False,
                  server_default=sa.func.now(),
                  comment="Timestamp del procesamiento"),
        sa.ForeignKeyConstraint(["documento_id"], ["documentos_lote.id"]),
        sa.ForeignKeyConstraint(["regla_id"], ["reglas_trabajo.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_agente_contexto_resultados_documento_id",
        "agente_contexto_resultados",
        ["documento_id"],
    )
    op.create_index(
        "ix_agente_contexto_resultados_regla_id",
        "agente_contexto_resultados",
        ["regla_id"],
    )

    # --- log_ia_invocaciones (CA-09) ---
    op.create_table(
        "log_ia_invocaciones",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False,
                  comment="PK auto-incremental (IDENTITY)"),
        sa.Column("documento_id", sa.Integer(), nullable=False,
                  comment="FK al documento que originó la invocación"),
        sa.Column("modelo", sa.String(length=100), nullable=False,
                  comment="Nombre del modelo IA invocado"),
        sa.Column("tokens_entrada", sa.Integer(), nullable=True,
                  comment="Tokens de entrada consumidos"),
        sa.Column("tokens_salida", sa.Integer(), nullable=True,
                  comment="Tokens de salida generados"),
        sa.Column("duracion_ms", sa.Integer(), nullable=True,
                  comment="Duración de la invocación en milisegundos"),
        sa.Column("exitoso", sa.Boolean(), nullable=False,
                  comment="True si la invocación fue exitosa"),
        sa.Column("error_mensaje", sa.String(length=500), nullable=True,
                  comment="Mensaje de error si la invocación falló"),
        sa.Column("invocado_at", sa.DateTime(), nullable=False,
                  server_default=sa.func.now(),
                  comment="Timestamp de la invocación"),
        sa.ForeignKeyConstraint(["documento_id"], ["documentos_lote.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_log_ia_invocaciones_documento_id",
        "log_ia_invocaciones",
        ["documento_id"],
    )


def downgrade() -> None:
    """Eliminar tablas log_ia_invocaciones y agente_contexto_resultados."""
    op.drop_table("log_ia_invocaciones")
    op.drop_table("agente_contexto_resultados")
