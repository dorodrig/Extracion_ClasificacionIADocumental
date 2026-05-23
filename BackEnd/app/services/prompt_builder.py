"""
Prompt Builder para el Agente de Contexto IA.

HU-04, CA-01 — Construye un prompt dinámico mezclando:
  - Reglas de negocio del cliente (HU-01: campos_extraer, tipo_documento)
  - Datos OCR consolidados del documento (HU-03: texto, confianza)
  - Instrucciones de retorno JSON estricto

CA-10 — El prompt SOLO incluye datos del documento actual.
        NUNCA incluye datos de otros clientes ni otros documentos.
"""
import json
import logging

from app.db.models.ocr_db import OcrResultadosPaginas
from app.db.models.rule_db import ReglasTrabajo

logger = logging.getLogger("grm.prompt_builder")


def build_context_prompt(
    regla: ReglasTrabajo,
    ocr_pages: list[OcrResultadosPaginas],
) -> str:
    """
    CA-01: Construye el prompt para el Agente de Contexto IA.

    El prompt incluye:
        1. Instrucción del sistema (rol del agente)
        2. Regla del cliente (tipo_documento, campos a extraer)
        3. Datos OCR del documento (texto + confianza por página)
        4. Instrucción de formato de respuesta (JSON estricto)

    CA-10: Solo incluye datos del documento actual y la regla asociada.

    Args:
        regla: La regla de trabajo activa del cliente.
        ocr_pages: Lista de páginas OCR procesadas del documento.

    Returns:
        Prompt completo como string para enviar a Gemini.
    """
    # Parsear campos_extraer de la regla (almacenado como JSON string)
    campos_regla = _parsear_campos_regla(regla.campos_extraer)

    # Construir sección de regla
    seccion_regla = _construir_seccion_regla(regla, campos_regla)

    # Construir sección de datos OCR
    seccion_ocr = _construir_seccion_ocr(ocr_pages)

    # Construir instrucción de formato de respuesta
    seccion_formato = _construir_seccion_formato(campos_regla)

    prompt = f"""Eres un agente de extracción de datos documentales del sistema GRM. Tu tarea es analizar el texto OCR de un documento y extraer los campos solicitados según la regla de trabajo del cliente.

INSTRUCCIONES:
1. Analiza cuidadosamente todo el texto OCR proporcionado.
2. Identifica y extrae cada campo solicitado en la regla.
3. Determina si el tipo de documento del texto coincide con el tipo esperado.
4. Valida que los valores extraídos sean coherentes con el tipo de dato esperado.
5. Retorna ÚNICAMENTE un JSON válido con la estructura indicada. Sin texto adicional.

{seccion_regla}

{seccion_ocr}

{seccion_formato}"""

    logger.info(
        "Prompt construido para regla_id=%d, páginas_ocr=%d, longitud=%d chars",
        regla.id,
        len(ocr_pages),
        len(prompt),
    )

    return prompt


def _parsear_campos_regla(campos_extraer_json: str) -> list[dict]:
    """Parsea el JSON de campos_extraer de la regla."""
    try:
        if isinstance(campos_extraer_json, str):
            return json.loads(campos_extraer_json)
        return campos_extraer_json
    except (json.JSONDecodeError, TypeError):
        logger.warning("No se pudo parsear campos_extraer: %s", campos_extraer_json)
        return []


def _construir_seccion_regla(regla: ReglasTrabajo, campos: list[dict]) -> str:
    """Construye la sección del prompt con la regla del cliente."""
    campos_desc = []
    for campo in campos:
        nombre = campo.get("nombre", "")
        tipo = campo.get("tipo", "Texto")
        obligatorio = campo.get("obligatorio", False)
        flag = "OBLIGATORIO" if obligatorio else "opcional"
        campos_desc.append(f"  - {nombre} (tipo: {tipo}, {flag})")

    campos_text = "\n".join(campos_desc) if campos_desc else "  (sin campos definidos)"

    return f"""--- REGLA DE TRABAJO DEL CLIENTE ---
Tipo de documento esperado: {regla.tipo_documento}
Campos a extraer:
{campos_text}"""


def _construir_seccion_ocr(ocr_pages: list[OcrResultadosPaginas]) -> str:
    """Construye la sección del prompt con los datos OCR del documento."""
    paginas_text = []

    for pagina in ocr_pages:
        page_num = pagina.numero_pagina
        confianza = pagina.confianza_promedio or 0.0

        # Extraer texto de campos_parseados (JSON con bloques de texto)
        texto_pagina = _extraer_texto_pagina(pagina.campos_parseados)

        paginas_text.append(
            f"--- Página {page_num} (confianza promedio: {confianza:.1f}%) ---\n"
            f"{texto_pagina}"
        )

    if not paginas_text:
        return "--- DATOS OCR DEL DOCUMENTO ---\n(sin datos OCR disponibles)"

    return "--- DATOS OCR DEL DOCUMENTO ---\n" + "\n\n".join(paginas_text)


def _extraer_texto_pagina(campos_parseados: str | None) -> str:
    """Extrae el texto legible de los campos parseados de una página OCR."""
    if not campos_parseados:
        return "(sin texto extraído)"

    try:
        bloques = json.loads(campos_parseados)
        lineas = []
        for bloque in bloques:
            if isinstance(bloque, dict):
                texto = bloque.get("text", "")
                if texto:
                    lineas.append(texto)
            elif isinstance(bloque, str):
                lineas.append(bloque)
        return "\n".join(lineas) if lineas else "(sin texto extraído)"
    except (json.JSONDecodeError, TypeError):
        # Si no es JSON, tratar como texto plano
        return str(campos_parseados)


def _construir_seccion_formato(campos: list[dict]) -> str:
    """Construye la instrucción de formato de respuesta JSON."""
    campos_ejemplo = []
    for campo in campos:
        nombre = campo.get("nombre", "campo")
        campos_ejemplo.append(
            f'    {{"nombre": "{nombre}", "valor": "VALOR_EXTRAIDO", '
            f'"confianza_ocr": 0.0, "validado_ia": true}}'
        )

    campos_json = ",\n".join(campos_ejemplo) if campos_ejemplo else '    {"nombre": "ejemplo", "valor": "", "confianza_ocr": 0.0, "validado_ia": false}'

    return f"""--- FORMATO DE RESPUESTA REQUERIDO ---
Responde ÚNICAMENTE con el siguiente JSON válido. No incluyas texto adicional, explicaciones ni markdown.

{{
  "tipo_documento_detectado": "TIPO_DETECTADO_EN_EL_DOCUMENTO",
  "confianza_tipo": 0.0,
  "campos_extraidos": [
{campos_json}
  ],
  "observaciones": "OBSERVACIONES_OPCIONALES"
}}

Reglas del JSON de respuesta:
- tipo_documento_detectado: El tipo de documento que identificas en el texto OCR.
- confianza_tipo: Tu nivel de confianza (0-100) de que el documento es del tipo detectado.
- campos_extraidos: Array con cada campo solicitado. Si no encuentras un valor, usa null.
- confianza_ocr: El score de confianza OCR del texto donde encontraste el valor (0-100).
- validado_ia: true si el valor extraído es coherente con el tipo de dato esperado.
- observaciones: Cualquier nota relevante sobre la extracción."""
