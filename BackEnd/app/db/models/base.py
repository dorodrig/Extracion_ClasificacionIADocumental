"""
app/db/models/base.py
Centraliza la importación de la Base declarativa y de todos los modelos ORM
para que Alembic pueda detectarlos correctamente.
"""
from app.db.database import Base  # noqa

# Importar todos los modelos para que Base.metadata los reconozca
from app.db.models.usuarios import Usuario, usuario_cliente  # noqa
from app.db.models.clientes import Cliente  # noqa
from app.db.models.reglas import ReglaTrabajo  # noqa
from app.db.models.documentos_lote import LoteProcesamiento, DocumentoLote  # noqa
from app.db.models.documentos_clasificados import DocumentoClasificado  # noqa
from app.db.models.documentos_pendientes import DocumentoPendiente  # noqa
from app.db.models.auditoria import LogProceso, LogAuditoriaUsuario, LogIAInvocaciones  # noqa
