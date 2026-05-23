"""
app/db/models/__init__.py
Importa todos los modelos ORM para que Alembic los detecte automáticamente.
"""
from app.db.models.documentos_lote import LoteProcesamiento, DocumentoLote  # noqa: F401
from app.db.models.usuarios import Usuario, usuario_cliente  # noqa: F401
from app.db.models.clientes import Cliente  # noqa: F401
from app.db.models.reglas import ReglaTrabajo  # noqa: F401
from app.db.models.auditoria import LogProceso, LogAuditoriaUsuario, LogIAInvocaciones  # noqa: F401
from app.db.models.documentos_clasificados import DocumentoClasificado  # noqa: F401
from app.db.models.documentos_pendientes import DocumentoPendiente  # noqa: F401
