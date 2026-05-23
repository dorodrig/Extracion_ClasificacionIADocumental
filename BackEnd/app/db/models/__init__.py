# db.models package
from .rule_db import ReglasTrabajo
# from .documento_db import DocumentosLote # Disabled due to conflict with batches.py
from .ocr_db import OcrResultadosPaginas
from .contexto_resultado_db import AgenteContextoResultados
from .log_ia_invocacion_db import LogIAInvocacion

from app.db.models.batches import LoteProcesamiento, DocumentoLote  # noqa: F401

# HU-07: Modelos necesarios para portal de cliente
from .documentos_clasificados import DocumentoClasificado  # noqa: F401
from .documentos_pendientes import DocumentoPendiente  # noqa: F401

# Stubs de auth — TODO(HU-08): Reemplazar con modelos reales
from .auth_stubs import Cliente, Usuario  # noqa: F401
