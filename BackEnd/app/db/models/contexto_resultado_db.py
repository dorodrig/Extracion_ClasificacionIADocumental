"""
Modelo SQLAlchemy ORM para la tabla agente_contexto_resultados.

HU-04, CA-12 — Almacena los paquetes de datos limpios generados
por el Agente de Contexto IA tras procesar documentos con Gemini.

Gobernanza §5.1 — Nombrado SQL (snake_case, plural, español).
Gobernanza §5.2 — Columnas de auditoría.
"""
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class AgenteContextoResultados(Base):
    """
    ORM Model para la tabla agente_contexto_resultados.

    Almacena los resultados del procesamiento del Agente de Contexto IA,
    incluyendo los campos extraídos, estado de validación y metadata de
    la invocación a Gemini.

    Estados posibles:
        - listo_clasificacion: datos_completos=true, listo para HU-05
        - pendiente_humano: datos_completos=false, requiere HU-06
        - error_ia: fallo en la invocación o parseo de Gemini
    """

    __tablename__ = "agente_contexto_resultados"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="PK auto-incremental (IDENTITY)",
    )
    documento_id = Column(
        Integer,
        ForeignKey("documentos_lote.id"),
        nullable=False,
        index=True,
        comment="FK al documento procesado",
    )
    regla_id = Column(
        Integer,
        ForeignKey("reglas_trabajo.id"),
        nullable=False,
        index=True,
        comment="FK a la regla de trabajo aplicada",
    )
    tipo_doc_detectado = Column(
        String(100),
        nullable=True,
        comment="Tipo de documento detectado por Gemini",
    )
    campos_extraidos_json = Column(
        Text,  # NVARCHAR(MAX) en SQL Server
        nullable=True,
        comment="JSON del paquete de datos limpios con campos extraídos",
    )
    datos_completos = Column(
        Boolean,
        nullable=False,
        comment="True si todos los campos obligatorios están presentes y válidos",
    )
    motivo_rechazo = Column(
        String(500),
        nullable=True,
        comment="Motivo del rechazo si datos_completos=false",
    )
    modelo_ia = Column(
        String(100),
        nullable=False,
        comment="Nombre del modelo IA utilizado (ej: gemini-1.5-pro)",
    )
    tokens_entrada = Column(
        Integer,
        nullable=True,
        comment="Cantidad de tokens de entrada consumidos",
    )
    tokens_salida = Column(
        Integer,
        nullable=True,
        comment="Cantidad de tokens de salida generados",
    )
    duracion_ms = Column(
        Integer,
        nullable=True,
        comment="Duración de la invocación en milisegundos",
    )
    estado = Column(
        String(50),
        nullable=False,
        comment="Estado del resultado: listo_clasificacion | pendiente_humano | error_ia",
    )
    processed_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        comment="Timestamp del procesamiento",
    )

    # Relaciones
    documento = relationship("DocumentosLote", backref="contexto_resultados")
    regla = relationship("ReglasTrabajo", backref="contexto_resultados")

    def __repr__(self) -> str:
        return (
            f"<AgenteContextoResultados(id={self.id}, "
            f"documento_id={self.documento_id}, "
            f"estado='{self.estado}', "
            f"datos_completos={self.datos_completos})>"
        )
