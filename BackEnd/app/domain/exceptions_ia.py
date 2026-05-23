"""
Excepciones de dominio para el Agente de Contexto IA (HU-04).

Gobernanza §3.3 — Todas heredan de GRMException.
"""
from app.domain.exceptions import GRMException


class GeminiApiKeyMissingException(GRMException):
    """CA-02: La variable de entorno GEMINI_API_KEY está ausente o vacía."""

    def __init__(self):
        super().__init__("Clave de API de Gemini no configurada")


class GeminiInvalidResponseException(GRMException):
    """CA-03: Gemini retornó JSON inválido tras los reintentos permitidos."""

    def __init__(self, documento_id: int, intentos: int):
        self.documento_id = documento_id
        self.intentos = intentos
        super().__init__(
            f"Error de IA - Respuesta inválida para documento id={documento_id} "
            f"tras {intentos} intentos."
        )


class GeminiApiTimeoutException(GRMException):
    """CA-08: La API de Gemini no respondió tras los reintentos con backoff."""

    def __init__(self, intentos: int, ultimo_error: str = ""):
        self.intentos = intentos
        self.ultimo_error = ultimo_error
        super().__init__(
            f"Error de IA - API no disponible tras {intentos} reintentos. "
            f"Último error: {ultimo_error}"
        )


class DocumentoTipoIncorrectoException(GRMException):
    """CA-07: El tipo de documento detectado difiere completamente del esperado."""

    def __init__(self, tipo_esperado: str, tipo_detectado: str):
        self.tipo_esperado = tipo_esperado
        self.tipo_detectado = tipo_detectado
        super().__init__(
            f"Tipo de documento incorrecto. "
            f"Esperado: '{tipo_esperado}', detectado: '{tipo_detectado}'."
        )
