"""
app/db/models/__init__.py
Importa todos los modelos ORM para que Alembic los detecte automáticamente.
"""
from app.db.models.batches import LoteProcesamiento, DocumentoLote  # noqa: F401
from app.db.models.usuarios import Usuario, Cliente, usuario_cliente  # noqa: F401
from app.db.models.auditoria import LogProceso, LogAuditoriaUsuario, LogIAInvocaciones  # noqa: F401
