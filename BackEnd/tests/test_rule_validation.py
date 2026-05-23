"""
Tests unitarios para las validaciones de dominio de Reglas de Trabajo.

Cobertura: app/domain/rules/rule_validation.py
CAs cubiertos: CA-05 (modo_entrada), CA-06 (campos duplicados).
"""
import pytest

from app.domain.exceptions import (
    DuplicateFieldNameException,
    InvalidModoEntradaException,
)
from app.domain.rules.rule_validation import (
    validate_campos_extraer_no_duplicados,
    validate_modo_entrada,
    validate_rule_data,
)


# ---------------------------------------------------------------------------
# Tests de validate_modo_entrada
# ---------------------------------------------------------------------------


class TestValidateModoEntrada:
    """Tests para la validación del modo de entrada."""

    def test_modo_scanner_valido(self):
        """Modo 'scanner' es aceptado sin error."""
        validate_modo_entrada("scanner")  # No debe lanzar excepción

    def test_modo_carpeta_valido(self):
        """Modo 'carpeta' es aceptado sin error."""
        validate_modo_entrada("carpeta")  # No debe lanzar excepción

    def test_modo_invalido_lanza_excepcion(self):
        """Un modo de entrada no reconocido lanza InvalidModoEntradaException."""
        with pytest.raises(InvalidModoEntradaException) as exc_info:
            validate_modo_entrada("email")
        assert "email" in str(exc_info.value)

    def test_modo_vacio_lanza_excepcion(self):
        """Un modo de entrada vacío lanza InvalidModoEntradaException."""
        with pytest.raises(InvalidModoEntradaException):
            validate_modo_entrada("")

    def test_modo_case_sensitive(self):
        """El modo de entrada es case-sensitive: 'Scanner' no es válido."""
        with pytest.raises(InvalidModoEntradaException):
            validate_modo_entrada("Scanner")


# ---------------------------------------------------------------------------
# Tests de validate_campos_extraer_no_duplicados
# ---------------------------------------------------------------------------


class TestValidateCamposExtraer:
    """Tests para la validación de campos duplicados (CA-06)."""

    def test_campos_sin_duplicados(self):
        """Lista de campos con nombres únicos pasa sin error."""
        campos = [
            {"nombre": "Número de Cédula", "tipo": "Identificación", "obligatorio": True},
            {"nombre": "Nombre Completo", "tipo": "Texto", "obligatorio": True},
            {"nombre": "Fecha de Expedición", "tipo": "Fecha", "obligatorio": False},
        ]
        validate_campos_extraer_no_duplicados(campos)  # No debe lanzar

    def test_campos_duplicados_exactos(self):
        """Dos campos con el mismo nombre exacto lanzan DuplicateFieldNameException."""
        campos = [
            {"nombre": "Cédula", "tipo": "Identificación", "obligatorio": True},
            {"nombre": "Cédula", "tipo": "Texto", "obligatorio": False},
        ]
        with pytest.raises(DuplicateFieldNameException) as exc_info:
            validate_campos_extraer_no_duplicados(campos)
        assert "Cédula" in str(exc_info.value)

    def test_campos_duplicados_case_insensitive(self):
        """CA-06: La comparación de nombres es case-insensitive."""
        campos = [
            {"nombre": "Número de Cédula", "tipo": "Identificación", "obligatorio": True},
            {"nombre": "número de cédula", "tipo": "Texto", "obligatorio": False},
        ]
        with pytest.raises(DuplicateFieldNameException):
            validate_campos_extraer_no_duplicados(campos)

    def test_campos_duplicados_con_espacios(self):
        """Nombres con espacios extra se normalizan antes de comparar."""
        campos = [
            {"nombre": "  Cédula  ", "tipo": "Identificación", "obligatorio": True},
            {"nombre": "Cédula", "tipo": "Texto", "obligatorio": False},
        ]
        with pytest.raises(DuplicateFieldNameException):
            validate_campos_extraer_no_duplicados(campos)

    def test_un_solo_campo(self):
        """Una lista con un solo campo siempre pasa."""
        campos = [
            {"nombre": "Cédula", "tipo": "Identificación", "obligatorio": True},
        ]
        validate_campos_extraer_no_duplicados(campos)  # No debe lanzar

    def test_lista_vacia(self):
        """Una lista vacía pasa sin error (la validación min_length=1 es en Pydantic)."""
        validate_campos_extraer_no_duplicados([])  # No debe lanzar


# ---------------------------------------------------------------------------
# Tests de validate_rule_data (integración de validaciones)
# ---------------------------------------------------------------------------


class TestValidateRuleData:
    """Tests de la función combinada que ejecuta todas las validaciones."""

    def test_datos_validos(self):
        """Datos completamente válidos pasan sin error."""
        campos = [
            {"nombre": "Campo1", "tipo": "Texto", "obligatorio": True},
            {"nombre": "Campo2", "tipo": "Número", "obligatorio": False},
        ]
        validate_rule_data(campos, "scanner")  # No debe lanzar

    def test_modo_invalido_con_campos_validos(self):
        """Modo inválido lanza excepción aunque los campos sean correctos."""
        campos = [
            {"nombre": "Campo1", "tipo": "Texto", "obligatorio": True},
        ]
        with pytest.raises(InvalidModoEntradaException):
            validate_rule_data(campos, "usb")

    def test_campos_duplicados_con_modo_valido(self):
        """Campos duplicados lanzan excepción aunque el modo sea válido."""
        campos = [
            {"nombre": "Campo1", "tipo": "Texto", "obligatorio": True},
            {"nombre": "campo1", "tipo": "Número", "obligatorio": False},
        ]
        with pytest.raises(DuplicateFieldNameException):
            validate_rule_data(campos, "carpeta")
