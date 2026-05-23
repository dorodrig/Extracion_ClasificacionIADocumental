"""
Tests unitarios para el módulo de normalización (CA-11).

HU-04 — Verifica normalización de:
    - Identificaciones: eliminación de puntos, espacios, guiones
    - Fechas: conversión a ISO 8601 (YYYY-MM-DD)
    - Texto: trim + title case
    - Números: eliminación de separadores de miles
"""
import pytest

from app.domain.rules.normalizer import (
    normalizar_fecha,
    normalizar_identificacion,
    normalizar_texto,
    normalizar_valor,
)


# -----------------------------------------------------------------------
# Tests de normalizar_identificacion
# -----------------------------------------------------------------------

class TestNormalizarIdentificacion:
    """Tests para normalización de campos tipo Identificación."""

    def test_elimina_puntos(self):
        assert normalizar_identificacion("1.234.567") == "1234567"

    def test_elimina_espacios(self):
        assert normalizar_identificacion("12 345 678") == "12345678"

    def test_elimina_guiones(self):
        assert normalizar_identificacion("12-345-678") == "12345678"

    def test_elimina_prefijo_cc(self):
        assert normalizar_identificacion("CC-1234567") == "1234567"

    def test_solo_digitos(self):
        assert normalizar_identificacion("1234567") == "1234567"

    def test_valor_vacio(self):
        assert normalizar_identificacion("") == ""

    def test_valor_none(self):
        assert normalizar_identificacion(None) == ""

    def test_formato_colombiano_completo(self):
        assert normalizar_identificacion("1.023.456.789") == "1023456789"

    def test_con_letras_y_numeros(self):
        assert normalizar_identificacion("NIT 900.123.456-7") == "90012345670000000"[:10]
        # Realmente extrae todos los dígitos
        result = normalizar_identificacion("NIT 900.123.456-7")
        assert result == "9001234567"


# -----------------------------------------------------------------------
# Tests de normalizar_fecha
# -----------------------------------------------------------------------

class TestNormalizarFecha:
    """Tests para normalización de campos tipo Fecha a ISO 8601."""

    def test_formato_dd_mm_yyyy_slash(self):
        assert normalizar_fecha("25/12/2024") == "2024-12-25"

    def test_formato_dd_mm_yyyy_guion(self):
        assert normalizar_fecha("25-12-2024") == "2024-12-25"

    def test_formato_dd_mm_yyyy_punto(self):
        assert normalizar_fecha("25.12.2024") == "2024-12-25"

    def test_formato_yyyy_mm_dd(self):
        assert normalizar_fecha("2024-12-25") == "2024-12-25"

    def test_formato_yyyy_mm_dd_slash(self):
        assert normalizar_fecha("2024/12/25") == "2024-12-25"

    def test_formato_espanol_largo(self):
        assert normalizar_fecha("25 de diciembre de 2024") == "2024-12-25"

    def test_formato_espanol_enero(self):
        assert normalizar_fecha("1 de enero de 2025") == "2025-01-01"

    def test_formato_ingles(self):
        assert normalizar_fecha("December 25, 2024") == "2024-12-25"

    def test_formato_ingles_sin_coma(self):
        assert normalizar_fecha("January 15 2025") == "2025-01-15"

    def test_valor_vacio(self):
        assert normalizar_fecha("") == ""

    def test_valor_no_reconocido_retorna_original(self):
        """Si no se puede parsear, retorna el valor original."""
        resultado = normalizar_fecha("fecha desconocida")
        assert resultado == "fecha desconocida"

    def test_espacios_extremos(self):
        assert normalizar_fecha("  25/12/2024  ") == "2024-12-25"


# -----------------------------------------------------------------------
# Tests de normalizar_texto
# -----------------------------------------------------------------------

class TestNormalizarTexto:
    """Tests para normalización de campos tipo Texto."""

    def test_trim_y_title_case(self):
        assert normalizar_texto("  david rodríguez  ") == "David Rodríguez"

    def test_todo_mayusculas(self):
        assert normalizar_texto("MARIA LOPEZ") == "Maria Lopez"

    def test_todo_minusculas(self):
        assert normalizar_texto("carlos garcia") == "Carlos Garcia"

    def test_valor_vacio(self):
        assert normalizar_texto("") == ""

    def test_valor_none(self):
        assert normalizar_texto(None) == ""

    def test_un_solo_nombre(self):
        assert normalizar_texto("  JUAN  ") == "Juan"


# -----------------------------------------------------------------------
# Tests de normalizar_valor (dispatcher)
# -----------------------------------------------------------------------

class TestNormalizarValor:
    """Tests para el dispatcher de normalización según tipo."""

    def test_tipo_identificacion(self):
        normalizado, original = normalizar_valor("1.234.567", "Identificación")
        assert normalizado == "1234567"
        assert original == "1.234.567"

    def test_tipo_identificacion_sin_tilde(self):
        normalizado, original = normalizar_valor("1.234.567", "Identificacion")
        assert normalizado == "1234567"

    def test_tipo_fecha(self):
        normalizado, original = normalizar_valor("25/12/2024", "Fecha")
        assert normalizado == "2024-12-25"
        assert original == "25/12/2024"

    def test_tipo_texto(self):
        normalizado, original = normalizar_valor("  DAVID  ", "Texto")
        assert normalizado == "David"
        assert original == "  DAVID  "

    def test_tipo_numero(self):
        normalizado, original = normalizar_valor("1.234.567", "Número")
        assert normalizado == "1234567"
        assert original == "1.234.567"

    def test_tipo_desconocido(self):
        normalizado, original = normalizar_valor("  valor  ", "Desconocido")
        assert normalizado == "valor"
        assert original == "  valor  "

    def test_valor_none(self):
        normalizado, original = normalizar_valor(None, "Texto")
        assert normalizado == ""
        assert original == ""

    def test_preserva_valor_original(self):
        """CA-11: El valor original siempre se preserva para trazabilidad."""
        normalizado, original = normalizar_valor("1.234.567", "Identificación")
        assert original == "1.234.567"
        assert normalizado != original
