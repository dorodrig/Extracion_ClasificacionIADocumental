"""
Reglas de validación de negocio para Reglas de Trabajo.

Gobernanza §2.2 — app/domain/rules/
Estas validaciones son independientes de la infraestructura.
"""
import logging

from app.domain.exceptions import (
    DuplicateFieldNameException,
    InvalidModoEntradaException,
)

logger = logging.getLogger("grm.rule_validation")

# Modos de entrada válidos para reglas de trabajo
MODOS_ENTRADA_VALIDOS = {"scanner", "carpeta"}

# Tipos de dato válidos para campos a extraer
TIPOS_DATO_VALIDOS = {"Texto", "Número", "Fecha", "Identificación"}


def validate_campos_extraer_no_duplicados(campos: list[dict]) -> None:
    """
    Valida que no existan campos con nombres duplicados (case-insensitive).

    CA-06: El sistema valida que no existan dos campos con el mismo nombre
    dentro de la misma regla.

    Args:
        campos: Lista de diccionarios con la estructura de CampoExtraer.

    Raises:
        DuplicateFieldNameException: Si se detecta un nombre duplicado.
    """
    nombres_vistos: set[str] = set()
    for campo in campos:
        nombre_normalizado = campo["nombre"].strip().lower()
        if nombre_normalizado in nombres_vistos:
            logger.warning(
                "Nombre de campo duplicado detectado: '%s'", campo["nombre"]
            )
            raise DuplicateFieldNameException(campo["nombre"])
        nombres_vistos.add(nombre_normalizado)


def validate_modo_entrada(modo: str) -> None:
    """
    Valida que el modo de entrada sea 'scanner' o 'carpeta'.

    Args:
        modo: Valor del campo modo_entrada.

    Raises:
        InvalidModoEntradaException: Si el modo no es válido.
    """
    if modo not in MODOS_ENTRADA_VALIDOS:
        logger.warning("Modo de entrada inválido recibido: '%s'", modo)
        raise InvalidModoEntradaException(modo)


def validate_rule_data(campos_extraer: list[dict], modo_entrada: str) -> None:
    """
    Ejecuta todas las validaciones de negocio para una regla de trabajo.

    Esta función centraliza las validaciones de dominio que deben ejecutarse
    tanto en la creación como en la actualización de una regla.

    Args:
        campos_extraer: Lista de campos a extraer (como diccionarios).
        modo_entrada: Modo de entrada de la regla.

    Raises:
        DuplicateFieldNameException: Si hay campos duplicados.
        InvalidModoEntradaException: Si el modo de entrada no es válido.
    """
    validate_modo_entrada(modo_entrada)
    validate_campos_extraer_no_duplicados(campos_extraer)
