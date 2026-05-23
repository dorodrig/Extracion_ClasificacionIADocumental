"""
Adapter de infraestructura para Google Gemini SDK.

HU-04 — CA-02: Invocación vía SDK con API key desde settings.
         CA-08: Timeout (30s) + reintentos (x3) con backoff exponencial.
         CA-09: Extracción de usage_metadata (tokens entrada/salida).
         CA-10: Invocación one-shot sin historial (sesión fresca).

Gobernanza §3.4 — Clean Architecture: adapter reemplazable sin tocar dominio.
Gobernanza §6.1 — CERO credenciales hardcodeadas.
"""
import logging
import time
from dataclasses import dataclass

import google.generativeai as genai

from app.core.config import settings
from app.domain.exceptions_ia import (
    GeminiApiKeyMissingException,
    GeminiApiTimeoutException,
)

logger = logging.getLogger("grm.gemini_adapter")


@dataclass
class GeminiResponse:
    """Resultado de una invocación a Google Gemini."""

    texto: str
    tokens_entrada: int
    tokens_salida: int
    duracion_ms: int
    modelo: str


class GeminiAdapter:
    """
    Adapter para invocar Google Gemini API.

    Responsabilidades:
        - CA-02: Configurar SDK con API key desde settings.
        - CA-08: Manejar timeout y reintentos con backoff exponencial.
        - CA-09: Extraer metadata de uso (tokens) de la respuesta.
        - CA-10: Cada invocación es one-shot, sin historial previo.

    Uso:
        adapter = GeminiAdapter()
        response = adapter.invoke("Prompt aquí...")
    """

    def __init__(self):
        """
        Inicializa el adapter configurando el SDK de Gemini.

        CA-02: Lanza GeminiApiKeyMissingException si la API key
        está ausente o vacía.

        Raises:
            GeminiApiKeyMissingException: Si GEMINI_API_KEY no está configurada.
        """
        if not settings.gemini_api_key:
            raise GeminiApiKeyMissingException()

        genai.configure(api_key=settings.gemini_api_key)
        self._model_name = settings.gemini_model
        self._timeout = settings.gemini_timeout_seconds
        self._max_retries = settings.gemini_max_retries

        logger.info(
            "GeminiAdapter inicializado: modelo=%s, timeout=%ds, max_retries=%d",
            self._model_name,
            self._timeout,
            self._max_retries,
        )

    def invoke(self, prompt: str) -> GeminiResponse:
        """
        Invocación one-shot a Google Gemini (CA-10: sin historial).

        CA-08: Reintentos con backoff exponencial (2s, 4s, 8s).
        CA-09: Extrae usage_metadata para tokens de entrada/salida.

        Args:
            prompt: El prompt completo a enviar a Gemini.

        Returns:
            GeminiResponse con el texto, tokens y duración.

        Raises:
            GeminiApiTimeoutException: Si todos los reintentos fallan.
        """
        # CA-10: Crear modelo fresco en cada invocación (sin historial)
        model = genai.GenerativeModel(self._model_name)

        backoff_delays = [2, 4, 8]  # segundos
        ultimo_error = ""

        for intento in range(self._max_retries + 1):
            try:
                logger.info(
                    "Invocando Gemini (intento %d/%d), modelo=%s",
                    intento + 1,
                    self._max_retries + 1,
                    self._model_name,
                )

                start_time = time.time()

                # CA-10: generate_content() es stateless — no usa chat
                response = model.generate_content(
                    prompt,
                    request_options={"timeout": self._timeout},
                )

                elapsed_ms = int((time.time() - start_time) * 1000)

                # CA-09: Extraer usage_metadata de tokens
                tokens_entrada = 0
                tokens_salida = 0
                if hasattr(response, "usage_metadata") and response.usage_metadata:
                    tokens_entrada = getattr(
                        response.usage_metadata, "prompt_token_count", 0
                    ) or 0
                    tokens_salida = getattr(
                        response.usage_metadata, "candidates_token_count", 0
                    ) or 0

                texto_respuesta = response.text if response.text else ""

                logger.info(
                    "Gemini respondió exitosamente: tokens_in=%d, "
                    "tokens_out=%d, duracion=%dms",
                    tokens_entrada,
                    tokens_salida,
                    elapsed_ms,
                )

                return GeminiResponse(
                    texto=texto_respuesta,
                    tokens_entrada=tokens_entrada,
                    tokens_salida=tokens_salida,
                    duracion_ms=elapsed_ms,
                    modelo=self._model_name,
                )

            except Exception as e:
                ultimo_error = str(e)
                logger.warning(
                    "Error en Gemini (intento %d/%d): %s",
                    intento + 1,
                    self._max_retries + 1,
                    ultimo_error,
                )

                # CA-08: Backoff exponencial si quedan reintentos
                if intento < self._max_retries:
                    delay = backoff_delays[min(intento, len(backoff_delays) - 1)]
                    logger.info("Reintentando en %ds...", delay)
                    time.sleep(delay)

        # CA-08: Todos los reintentos agotados
        logger.error(
            "Todos los reintentos de Gemini agotados (%d intentos). "
            "Último error: %s",
            self._max_retries + 1,
            ultimo_error,
        )
        raise GeminiApiTimeoutException(
            intentos=self._max_retries + 1,
            ultimo_error=ultimo_error,
        )
