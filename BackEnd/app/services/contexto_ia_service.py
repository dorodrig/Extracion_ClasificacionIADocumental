"""
Servicio orquestador del Agente de Contexto IA.

HU-04 — Coordina el flujo completo de procesamiento de un documento:
  CA-01: Construcción del prompt (vía prompt_builder)
  CA-02: Invocación a Gemini (vía gemini_adapter)
  CA-03: Parseo y validación de respuesta JSON (reintentos x2)
  CA-04: Validación de campos obligatorios
  CA-05: Enrutamiento a revisión humana si datos_completos=false
  CA-06: Enrutamiento a clasificación si datos_completos=true
  CA-07: Detección de tipo de documento y alertas
  CA-08: Manejo de timeout/error (delegado al adapter)
  CA-09: Registro de invocaciones en log_ia_invocaciones
  CA-10: Aislamiento de contexto (delegado al adapter + prompt_builder)
  CA-11: Normalización de valores (vía normalizer)
  CA-12: Persistencia en agente_contexto_resultados

Gobernanza §3.4 — Capa de aplicación (Use Case / Service).
"""
import json
import logging

from sqlalchemy.orm import Session

from app.db.models.contexto_resultado_db import AgenteContextoResultados
from app.db.models.log_ia_invocacion_db import LogIAInvocacion
from app.db.models.ocr_db import OcrResultadosPaginas
from app.db.models.rule_db import ReglasTrabajo
from app.db.repositories.contexto_resultado_repository import ContextoResultadoRepository
from app.db.repositories.log_ia_repository import LogIARepository
from app.domain.exceptions import GRMException
from app.domain.exceptions_ia import (
    GeminiApiTimeoutException,
    GeminiInvalidResponseException,
)
from app.domain.rules.normalizer import normalizar_valor
from app.services.gemini_adapter import GeminiAdapter, GeminiResponse
from app.services.prompt_builder import build_context_prompt

logger = logging.getLogger("grm.contexto_ia")

# Constantes de estado
ESTADO_LISTO_CLASIFICACION = "listo_clasificacion"
ESTADO_PENDIENTE_HUMANO = "pendiente_humano"
ESTADO_ERROR_IA = "error_ia"

# Máximo de reintentos por JSON inválido (CA-03)
MAX_REINTENTOS_JSON = 2


class ContextoIAService:
    """
    Orquestador principal del Agente de Contexto IA.

    Coordina el flujo completo: prompt → Gemini → parseo → validación →
    normalización → persistencia.
    """

    def __init__(self, db: Session, gemini_adapter: GeminiAdapter | None = None):
        """
        Inicializa el servicio con sus dependencias.

        Args:
            db: Sesión de base de datos.
            gemini_adapter: Adapter de Gemini (inyectable para testing).
        """
        self.db = db
        self.gemini = gemini_adapter or GeminiAdapter()
        self.resultado_repo = ContextoResultadoRepository(db)
        self.log_ia_repo = LogIARepository(db)

    async def procesar_documento(
        self,
        documento_id: int,
        regla_id: int,
    ) -> AgenteContextoResultados:
        """
        Procesa un documento con el Agente de Contexto IA.

        Flujo completo:
            1. Obtener documento + páginas OCR
            2. Obtener regla de trabajo
            3. Construir prompt (CA-01)
            4. Invocar Gemini (CA-02, CA-08, CA-10)
            5. Parsear JSON (CA-03)
            6. Validar campos (CA-04)
            7. Detectar tipo documento (CA-07)
            8. Normalizar valores (CA-11)
            9. Determinar estado (CA-05/CA-06)
            10. Registrar invocación (CA-09)
            11. Persistir resultado (CA-12)

        Args:
            documento_id: ID del documento a procesar.
            regla_id: ID de la regla de trabajo a aplicar.

        Returns:
            AgenteContextoResultados persistido con el paquete de datos limpios.

        Raises:
            GRMException: Si el documento o la regla no existen.
        """
        logger.info(
            "Iniciando procesamiento IA: documento_id=%d, regla_id=%d",
            documento_id,
            regla_id,
        )

        # 1. Obtener documento + páginas OCR
        ocr_pages = self._obtener_paginas_ocr(documento_id)

        # 2. Obtener regla de trabajo
        regla = self._obtener_regla(regla_id)

        # 3. Construir prompt (CA-01)
        prompt = build_context_prompt(regla, ocr_pages)

        # 4-5. Invocar Gemini y parsear respuesta (CA-02, CA-03, CA-08, CA-10)
        gemini_response, parsed_data = await self._invocar_y_parsear(
            prompt, documento_id
        )

        # Si no se pudo parsear → error_ia
        if parsed_data is None:
            return self._crear_resultado_error(
                documento_id=documento_id,
                regla_id=regla_id,
                gemini_response=gemini_response,
                motivo="Error de IA - Respuesta inválida",
            )

        # 6. Validar campos obligatorios (CA-04)
        campos_regla = self._parsear_campos_regla(regla.campos_extraer)
        datos_completos, campos_faltantes = self._validar_campos_obligatorios(
            parsed_data, campos_regla
        )

        # 7. Detectar tipo de documento (CA-07)
        tipo_detectado = parsed_data.get("tipo_documento_detectado", "")
        confianza_tipo = parsed_data.get("confianza_tipo", 0.0)
        alerta_tipo, tipo_incorrecto = self._detectar_tipo_documento(
            tipo_detectado, confianza_tipo, regla.tipo_documento
        )

        if tipo_incorrecto:
            datos_completos = False
            campos_faltantes.append("Tipo de documento incorrecto")

        # 8. Normalizar valores (CA-11)
        campos_extraidos = self._normalizar_campos(
            parsed_data.get("campos_extraidos", []),
            campos_regla,
        )

        # Agregar alerta al paquete si aplica (CA-07)
        observaciones = parsed_data.get("observaciones", "")
        if alerta_tipo:
            observaciones = f"[ALERTA TIPO DOC] {alerta_tipo}. {observaciones}"

        # 9. Determinar estado (CA-05, CA-06)
        estado, motivo_rechazo = self._determinar_estado(
            datos_completos, campos_faltantes
        )

        # 10. Registrar invocación en log (CA-09)
        self._registrar_invocacion(
            documento_id=documento_id,
            gemini_response=gemini_response,
            exitoso=True,
        )

        # 11. Persistir resultado (CA-12)
        paquete_json = json.dumps(
            {
                "campos_extraidos": campos_extraidos,
                "observaciones": observaciones,
                "tipo_documento_detectado": tipo_detectado,
                "confianza_tipo": confianza_tipo,
            },
            ensure_ascii=False,
        )

        resultado = AgenteContextoResultados(
            documento_id=documento_id,
            regla_id=regla_id,
            tipo_doc_detectado=tipo_detectado,
            campos_extraidos_json=paquete_json,
            datos_completos=datos_completos,
            motivo_rechazo=motivo_rechazo,
            modelo_ia=gemini_response.modelo if gemini_response else "",
            tokens_entrada=gemini_response.tokens_entrada if gemini_response else None,
            tokens_salida=gemini_response.tokens_salida if gemini_response else None,
            duracion_ms=gemini_response.duracion_ms if gemini_response else None,
            estado=estado,
        )

        resultado = self.resultado_repo.crear(resultado)

        logger.info(
            "Procesamiento IA completado: documento_id=%d, estado=%s, "
            "datos_completos=%s",
            documento_id,
            estado,
            datos_completos,
        )

        return resultado

    # -------------------------------------------------------------------
    # Métodos internos
    # -------------------------------------------------------------------

    def _obtener_paginas_ocr(self, documento_id: int) -> list[OcrResultadosPaginas]:
        """Obtiene las páginas OCR de un documento."""
        paginas = (
            self.db.query(OcrResultadosPaginas)
            .filter(OcrResultadosPaginas.documento_id == documento_id)
            .order_by(OcrResultadosPaginas.numero_pagina)
            .all()
        )
        if not paginas:
            raise GRMException(
                f"No se encontraron páginas OCR para el documento id={documento_id}. "
                f"Asegúrese de que el documento ha sido procesado por OCR (HU-03)."
            )
        logger.info(
            "Páginas OCR obtenidas: documento_id=%d, páginas=%d",
            documento_id,
            len(paginas),
        )
        return paginas

    def _obtener_regla(self, regla_id: int) -> ReglasTrabajo:
        """Obtiene la regla de trabajo activa."""
        regla = (
            self.db.query(ReglasTrabajo)
            .filter(ReglasTrabajo.id == regla_id, ReglasTrabajo.activa == True)
            .first()
        )
        if not regla:
            raise GRMException(
                f"No se encontró la regla de trabajo activa con id={regla_id}."
            )
        return regla

    async def _invocar_y_parsear(
        self, prompt: str, documento_id: int
    ) -> tuple[GeminiResponse | None, dict | None]:
        """
        CA-02, CA-03, CA-08, CA-10: Invoca Gemini y parsea la respuesta JSON.

        CA-03: Si el JSON es inválido, reintenta hasta 2 veces con el mismo prompt.
        CA-08: Los errores de API son manejados por el GeminiAdapter (backoff).

        Returns:
            Tupla (GeminiResponse, parsed_dict) o (GeminiResponse, None) si falló.
        """
        gemini_response = None

        # Intentar invocación + parseo (CA-03: hasta MAX_REINTENTOS_JSON reintentos)
        for intento in range(MAX_REINTENTOS_JSON + 1):
            try:
                # CA-02, CA-08, CA-10: Invocación one-shot vía adapter
                gemini_response = self.gemini.invoke(prompt)

                # CA-03: Intentar parsear como JSON
                parsed = self._parsear_respuesta_json(gemini_response.texto)
                if parsed is not None:
                    return (gemini_response, parsed)

                logger.warning(
                    "Respuesta de Gemini no es JSON válido (intento %d/%d): %s",
                    intento + 1,
                    MAX_REINTENTOS_JSON + 1,
                    gemini_response.texto[:200],
                )

                # Registrar intento fallido en log (CA-09)
                self._registrar_invocacion(
                    documento_id=documento_id,
                    gemini_response=gemini_response,
                    exitoso=False,
                    error_mensaje="JSON inválido en respuesta",
                )

            except GeminiApiTimeoutException as e:
                logger.error(
                    "API de Gemini no disponible para documento_id=%d: %s",
                    documento_id,
                    str(e),
                )
                # Registrar error de API en log (CA-09)
                self._registrar_invocacion(
                    documento_id=documento_id,
                    gemini_response=None,
                    exitoso=False,
                    error_mensaje=str(e),
                )
                return (None, None)

        # CA-03: Todos los reintentos de parseo agotados
        logger.error(
            "JSON inválido tras %d reintentos para documento_id=%d",
            MAX_REINTENTOS_JSON + 1,
            documento_id,
        )
        return (gemini_response, None)

    def _parsear_respuesta_json(self, texto: str) -> dict | None:
        """
        CA-03: Intenta parsear la respuesta de Gemini como JSON.

        Maneja casos donde Gemini envuelve el JSON en markdown (```json...```).

        Args:
            texto: Texto de respuesta de Gemini.

        Returns:
            Dict parseado o None si no es JSON válido.
        """
        if not texto:
            return None

        # Limpiar posible envoltorio markdown
        texto_limpio = texto.strip()
        if texto_limpio.startswith("```json"):
            texto_limpio = texto_limpio[7:]
        elif texto_limpio.startswith("```"):
            texto_limpio = texto_limpio[3:]
        if texto_limpio.endswith("```"):
            texto_limpio = texto_limpio[:-3]
        texto_limpio = texto_limpio.strip()

        try:
            parsed = json.loads(texto_limpio)
            if isinstance(parsed, dict):
                return parsed
            logger.warning("Respuesta JSON no es un objeto: %s", type(parsed))
            return None
        except json.JSONDecodeError as e:
            logger.warning("Error parseando JSON de Gemini: %s", str(e))
            return None

    def _parsear_campos_regla(self, campos_extraer_json: str) -> list[dict]:
        """Parsea el JSON de campos_extraer de la regla."""
        try:
            if isinstance(campos_extraer_json, str):
                return json.loads(campos_extraer_json)
            return campos_extraer_json
        except (json.JSONDecodeError, TypeError):
            return []

    def _validar_campos_obligatorios(
        self, parsed_data: dict, campos_regla: list[dict]
    ) -> tuple[bool, list[str]]:
        """
        CA-04: Valida que todos los campos obligatorios estén presentes y válidos.

        Verifica:
            - Presencia de cada campo obligatorio
            - Valor no nulo y no vacío
            - Tipo coherente (Identificación → solo dígitos post-normalización)

        Args:
            parsed_data: Respuesta parseada de Gemini.
            campos_regla: Campos definidos en la regla de trabajo.

        Returns:
            Tupla (datos_completos, lista_campos_faltantes).
        """
        campos_extraidos = parsed_data.get("campos_extraidos", [])
        campos_faltantes = []

        # Crear mapa de campos extraídos por nombre (case-insensitive)
        mapa_extraidos = {}
        for campo in campos_extraidos:
            if isinstance(campo, dict):
                nombre = campo.get("nombre", "").strip().lower()
                mapa_extraidos[nombre] = campo

        for campo_regla in campos_regla:
            es_obligatorio = campo_regla.get("obligatorio", False)
            if not es_obligatorio:
                continue

            nombre_regla = campo_regla.get("nombre", "").strip().lower()
            tipo_regla = campo_regla.get("tipo", "Texto")

            campo_encontrado = mapa_extraidos.get(nombre_regla)

            if campo_encontrado is None:
                campos_faltantes.append(
                    f"Campo obligatorio ausente: '{campo_regla.get('nombre', '')}'"
                )
                continue

            valor = campo_encontrado.get("valor")
            if valor is None or str(valor).strip() == "":
                campos_faltantes.append(
                    f"Campo obligatorio vacío: '{campo_regla.get('nombre', '')}'"
                )
                continue

            # Validar tipo (CA-04)
            if not self._validar_tipo_campo(str(valor), tipo_regla):
                campos_faltantes.append(
                    f"Campo '{campo_regla.get('nombre', '')}' tiene valor "
                    f"incoherente con tipo '{tipo_regla}'"
                )

        datos_completos = len(campos_faltantes) == 0
        return (datos_completos, campos_faltantes)

    def _validar_tipo_campo(self, valor: str, tipo: str) -> bool:
        """Valida que un valor sea coherente con su tipo esperado."""
        tipo_lower = tipo.lower() if tipo else ""

        if "identificaci" in tipo_lower or "identificacion" in tipo_lower:
            # Debe contener al menos dígitos
            digitos = "".join(c for c in valor if c.isdigit())
            return len(digitos) >= 3  # Mínimo 3 dígitos para una identificación

        if "fecha" in tipo_lower:
            # Debe contener dígitos (cualquier formato de fecha los tiene)
            return any(c.isdigit() for c in valor)

        if "numero" in tipo_lower or "número" in tipo_lower:
            # Debe contener al menos un dígito
            return any(c.isdigit() for c in valor)

        # Texto: cualquier valor no vacío es válido
        return len(valor.strip()) > 0

    def _detectar_tipo_documento(
        self,
        tipo_detectado: str,
        confianza_tipo: float,
        tipo_esperado: str,
    ) -> tuple[str, bool]:
        """
        CA-07: Compara el tipo detectado vs el esperado.

        Returns:
            Tupla (alerta_mensaje, es_totalmente_diferente).
            - alerta_mensaje: String con la alerta o "" si no hay.
            - es_totalmente_diferente: True si el tipo es completamente diferente.
        """
        if not tipo_detectado or not tipo_esperado:
            return ("", False)

        tipo_det_lower = tipo_detectado.strip().lower()
        tipo_esp_lower = tipo_esperado.strip().lower()

        # Si coinciden, no hay problema
        if tipo_det_lower == tipo_esp_lower:
            return ("", False)

        # Filtrar stopwords para comparación significativa
        stopwords = {"de", "del", "la", "el", "los", "las", "y", "en",
                     "con", "para", "por", "un", "una"}
        palabras_det = set(tipo_det_lower.split()) - stopwords
        palabras_esp = set(tipo_esp_lower.split()) - stopwords
        hay_interseccion = bool(palabras_det & palabras_esp)

        if confianza_tipo > 90 and hay_interseccion:
            # CA-07: Confianza alta pero diferencia parcial → alerta
            alerta = (
                f"Tipo detectado '{tipo_detectado}' difiere del esperado "
                f"'{tipo_esperado}' (confianza: {confianza_tipo}%)"
            )
            logger.warning("CA-07 Alerta tipo documento: %s", alerta)
            return (alerta, False)

        if not hay_interseccion:
            # CA-07: Totalmente diferente → datos_completos=false
            alerta = (
                f"Tipo de documento completamente diferente. "
                f"Esperado: '{tipo_esperado}', detectado: '{tipo_detectado}'"
            )
            logger.warning("CA-07 Tipo documento incorrecto: %s", alerta)
            return (alerta, True)

        # Diferencia menor sin alta confianza → solo alerta
        alerta = (
            f"Diferencia en tipo de documento: esperado '{tipo_esperado}', "
            f"detectado '{tipo_detectado}'"
        )
        return (alerta, False)

    def _normalizar_campos(
        self,
        campos_extraidos: list[dict],
        campos_regla: list[dict],
    ) -> list[dict]:
        """
        CA-11: Normaliza los valores extraídos según su tipo.

        Preserva valor_original para trazabilidad.

        Args:
            campos_extraidos: Campos extraídos por Gemini.
            campos_regla: Definición de campos en la regla.

        Returns:
            Lista de campos con valores normalizados.
        """
        # Crear mapa de tipos por nombre de campo
        tipos_por_nombre = {}
        for campo in campos_regla:
            nombre = campo.get("nombre", "").strip().lower()
            tipos_por_nombre[nombre] = campo.get("tipo", "Texto")

        campos_normalizados = []
        for campo in campos_extraidos:
            if not isinstance(campo, dict):
                continue

            nombre = campo.get("nombre", "")
            valor = campo.get("valor")
            confianza = campo.get("confianza_ocr", 0.0)
            validado = campo.get("validado_ia", False)

            # Obtener tipo del campo según la regla
            tipo = tipos_por_nombre.get(nombre.strip().lower(), "Texto")

            # CA-11: Normalizar el valor
            if valor is not None:
                valor_normalizado, valor_original = normalizar_valor(str(valor), tipo)
            else:
                valor_normalizado = None
                valor_original = None

            campos_normalizados.append({
                "nombre": nombre,
                "valor": valor_normalizado,
                "valor_original": valor_original,
                "confianza_ocr": confianza,
                "validado_ia": validado,
            })

        return campos_normalizados

    def _determinar_estado(
        self, datos_completos: bool, campos_faltantes: list[str]
    ) -> tuple[str, str | None]:
        """
        CA-05 / CA-06: Determina el estado del resultado.

        CA-05: datos_completos=false → pendiente_humano + motivo_rechazo
        CA-06: datos_completos=true → listo_clasificacion

        Returns:
            Tupla (estado, motivo_rechazo).
        """
        if datos_completos:
            return (ESTADO_LISTO_CLASIFICACION, None)
        else:
            motivo = "; ".join(campos_faltantes) if campos_faltantes else "Datos incompletos"
            return (ESTADO_PENDIENTE_HUMANO, motivo)

    def _registrar_invocacion(
        self,
        documento_id: int,
        gemini_response: GeminiResponse | None,
        exitoso: bool,
        error_mensaje: str | None = None,
    ) -> None:
        """
        CA-09: Registra la invocación en log_ia_invocaciones.

        Args:
            documento_id: ID del documento procesado.
            gemini_response: Respuesta de Gemini (None si falló antes de recibir).
            exitoso: True si la invocación fue exitosa.
            error_mensaje: Mensaje de error si falló.
        """
        log_entry = LogIAInvocacion(
            documento_id=documento_id,
            modelo=gemini_response.modelo if gemini_response else "N/A",
            tokens_entrada=gemini_response.tokens_entrada if gemini_response else None,
            tokens_salida=gemini_response.tokens_salida if gemini_response else None,
            duracion_ms=gemini_response.duracion_ms if gemini_response else None,
            exitoso=exitoso,
            error_mensaje=error_mensaje[:500] if error_mensaje else None,
        )
        self.log_ia_repo.registrar(log_entry)

    def _crear_resultado_error(
        self,
        documento_id: int,
        regla_id: int,
        gemini_response: GeminiResponse | None,
        motivo: str,
    ) -> AgenteContextoResultados:
        """
        Crea y persiste un resultado con estado error_ia.

        Usado cuando:
            - CA-03: JSON inválido tras reintentos
            - CA-08: API no disponible tras reintentos
        """
        # Registrar invocación fallida (CA-09)
        self._registrar_invocacion(
            documento_id=documento_id,
            gemini_response=gemini_response,
            exitoso=False,
            error_mensaje=motivo,
        )

        resultado = AgenteContextoResultados(
            documento_id=documento_id,
            regla_id=regla_id,
            tipo_doc_detectado=None,
            campos_extraidos_json=None,
            datos_completos=False,
            motivo_rechazo=motivo,
            modelo_ia=gemini_response.modelo if gemini_response else "N/A",
            tokens_entrada=gemini_response.tokens_entrada if gemini_response else None,
            tokens_salida=gemini_response.tokens_salida if gemini_response else None,
            duracion_ms=gemini_response.duracion_ms if gemini_response else None,
            estado=ESTADO_ERROR_IA,
        )

        resultado = self.resultado_repo.crear(resultado)

        logger.error(
            "Resultado error_ia creado: documento_id=%d, motivo=%s",
            documento_id,
            motivo,
        )

        return resultado
