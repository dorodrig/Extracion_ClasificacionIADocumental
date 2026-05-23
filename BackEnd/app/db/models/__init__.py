# db.models package
from .rule_db import ReglasTrabajo
from .documento_db import DocumentosLote
from .ocr_db import OcrResultadosPaginas
from .contexto_resultado_db import AgenteContextoResultados
from .log_ia_invocacion_db import LogIAInvocacion
"""
app/db/models/__init__.py
Importa todos los modelos ORM para que Alembic los detecte automáticamente.
"""
from app.db.models.batches import LoteProcesamiento, DocumentoLote  # noqa: F401
