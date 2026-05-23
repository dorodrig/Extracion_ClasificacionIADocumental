"""
Normalización de valores extraídos por el Agente de Contexto IA.

CA-11 — HU-04: Normaliza identificaciones, fechas y texto.
Preserva el valor original para trazabilidad.
"""
import re
import logging
from datetime import datetime

logger = logging.getLogger("grm.normalizer")

# Patrones de fecha comunes en documentos colombianos y latinoamericanos
_FECHA_PATTERNS = [
    # DD/MM/YYYY o DD-MM-YYYY o DD.MM.YYYY
    (r"^(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})$", "%d/%m/%Y"),
    # YYYY/MM/DD o YYYY-MM-DD
    (r"^(\d{4})[/\-.](\d{1,2})[/\-.](\d{1,2})$", "%Y/%m/%d"),
    # DD de MES de YYYY (español)
    (r"^(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})$", "ES_LONG"),
]

_MESES_ES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}

_MONTHS_EN = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}


def normalizar_identificacion(valor: str) -> str:
    """
    CA-11: Elimina puntos, espacios, guiones de números de identificación.

    Ejemplos:
        "1.234.567" → "1234567"
        "12 345 678" → "12345678"
        "CC-1234567" → "1234567"

    Args:
        valor: Valor crudo del campo de identificación.

    Returns:
        String conteniendo solo dígitos.
    """
    if not valor:
        return ""
    return re.sub(r"[^\d]", "", valor)


def normalizar_fecha(valor: str) -> str:
    """
    CA-11: Convierte fechas a formato ISO 8601 (YYYY-MM-DD).

    Soporta formatos:
        - DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY
        - YYYY-MM-DD, YYYY/MM/DD
        - "25 de diciembre de 2024" (español)
        - "December 25, 2024" (inglés)

    Args:
        valor: Valor crudo de la fecha.

    Returns:
        Fecha en formato ISO 8601 o el valor original si no se pudo parsear.
    """
    if not valor:
        return ""

    valor_limpio = valor.strip()

    # Intentar patrones DD/MM/YYYY, YYYY-MM-DD, etc.
    for pattern, fmt in _FECHA_PATTERNS:
        match = re.match(pattern, valor_limpio, re.IGNORECASE)
        if match:
            if fmt == "ES_LONG":
                dia, mes_str, anio = match.groups()
                mes_num = _MESES_ES.get(mes_str.lower())
                if mes_num:
                    try:
                        fecha = datetime(int(anio), mes_num, int(dia))
                        return fecha.strftime("%Y-%m-%d")
                    except ValueError:
                        pass
            elif fmt == "%d/%m/%Y":
                try:
                    grupos = match.groups()
                    fecha = datetime(int(grupos[2]), int(grupos[1]), int(grupos[0]))
                    return fecha.strftime("%Y-%m-%d")
                except ValueError:
                    pass
            elif fmt == "%Y/%m/%d":
                try:
                    grupos = match.groups()
                    fecha = datetime(int(grupos[0]), int(grupos[1]), int(grupos[2]))
                    return fecha.strftime("%Y-%m-%d")
                except ValueError:
                    pass

    # Intentar formato inglés: "Month DD, YYYY" o "Month DD YYYY"
    en_match = re.match(
        r"^(\w+)\s+(\d{1,2}),?\s+(\d{4})$", valor_limpio, re.IGNORECASE
    )
    if en_match:
        mes_str, dia, anio = en_match.groups()
        mes_num = _MONTHS_EN.get(mes_str.lower())
        if mes_num:
            try:
                fecha = datetime(int(anio), mes_num, int(dia))
                return fecha.strftime("%Y-%m-%d")
            except ValueError:
                pass

    # Si ya es ISO 8601, retornarlo limpio
    iso_match = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", valor_limpio)
    if iso_match:
        return valor_limpio

    logger.warning("No se pudo normalizar la fecha: '%s'", valor)
    return valor_limpio


def normalizar_texto(valor: str) -> str:
    """
    CA-11: Trim de espacios extremos y capitalización estándar (title case).

    Args:
        valor: Valor crudo del campo de texto.

    Returns:
        Texto normalizado con title case.
    """
    if not valor:
        return ""
    return valor.strip().title()


def normalizar_valor(valor: str, tipo: str) -> tuple[str, str]:
    """
    CA-11: Normaliza un valor según su tipo, preservando el original.

    Args:
        valor: Valor crudo extraído por Gemini.
        tipo: Tipo del campo según la regla (Identificación, Fecha, Texto, Número).

    Returns:
        Tupla (valor_normalizado, valor_original).
    """
    if valor is None:
        return ("", "")

    valor_original = str(valor)
    tipo_lower = tipo.lower() if tipo else ""

    if "identificaci" in tipo_lower or "identificacion" in tipo_lower:
        return (normalizar_identificacion(valor_original), valor_original)
    elif "fecha" in tipo_lower:
        return (normalizar_fecha(valor_original), valor_original)
    elif "texto" in tipo_lower:
        return (normalizar_texto(valor_original), valor_original)
    elif "numero" in tipo_lower or "número" in tipo_lower:
        # Para números, eliminar separadores de miles pero preservar decimales
        normalizado = re.sub(r"[.\s](?=\d{3})", "", valor_original)
        return (normalizado.strip(), valor_original)
    else:
        return (valor_original.strip(), valor_original)
