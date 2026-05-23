"""
Tests unitarios para el Prompt Builder (CA-01, CA-10).

HU-04 — Verifica:
    - CA-01: El prompt incluye regla + OCR + instrucción JSON
    - CA-10: El prompt SOLO contiene datos del documento actual
"""
import json

import pytest

from app.services.prompt_builder import (
    build_context_prompt,
    _construir_seccion_regla,
    _construir_seccion_ocr,
    _extraer_texto_pagina,
    _parsear_campos_regla,
)


# -----------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------

class FakeRegla:
    """Mock de ReglasTrabajo para tests."""

    def __init__(self, id=1, tipo_documento="Cédula de Ciudadanía", campos_extraer=None):
        self.id = id
        self.tipo_documento = tipo_documento
        self.campos_extraer = campos_extraer or json.dumps([
            {"nombre": "Número de Cédula", "tipo": "Identificación", "obligatorio": True},
            {"nombre": "Nombre Completo", "tipo": "Texto", "obligatorio": True},
            {"nombre": "Fecha de Expedición", "tipo": "Fecha", "obligatorio": False},
        ])


class FakeOcrPage:
    """Mock de OcrResultadosPaginas para tests."""

    def __init__(self, numero_pagina=1, confianza_promedio=97.5, campos_parseados=None):
        self.numero_pagina = numero_pagina
        self.confianza_promedio = confianza_promedio
        self.campos_parseados = campos_parseados or json.dumps([
            {"text": "REPÚBLICA DE COLOMBIA", "confidence": 99.1, "type": "LINE"},
            {"text": "CÉDULA DE CIUDADANÍA", "confidence": 98.5, "type": "LINE"},
            {"text": "1234567", "confidence": 97.0, "type": "WORD"},
            {"text": "DAVID RODRÍGUEZ", "confidence": 96.8, "type": "LINE"},
        ])


# -----------------------------------------------------------------------
# Tests de build_context_prompt
# -----------------------------------------------------------------------

class TestBuildContextPrompt:
    """Tests para la construcción completa del prompt."""

    def test_prompt_incluye_tipo_documento(self):
        """CA-01: El prompt incluye el tipo de documento esperado."""
        regla = FakeRegla()
        ocr_pages = [FakeOcrPage()]
        prompt = build_context_prompt(regla, ocr_pages)

        assert "Cédula de Ciudadanía" in prompt

    def test_prompt_incluye_campos_regla(self):
        """CA-01: El prompt incluye los campos a extraer de la regla."""
        regla = FakeRegla()
        ocr_pages = [FakeOcrPage()]
        prompt = build_context_prompt(regla, ocr_pages)

        assert "Número de Cédula" in prompt
        assert "Nombre Completo" in prompt
        assert "Fecha de Expedición" in prompt

    def test_prompt_incluye_obligatoriedad(self):
        """CA-01: El prompt indica qué campos son obligatorios."""
        regla = FakeRegla()
        ocr_pages = [FakeOcrPage()]
        prompt = build_context_prompt(regla, ocr_pages)

        assert "OBLIGATORIO" in prompt
        assert "opcional" in prompt

    def test_prompt_incluye_tipos_dato(self):
        """CA-01: El prompt incluye tipos de dato de cada campo."""
        regla = FakeRegla()
        ocr_pages = [FakeOcrPage()]
        prompt = build_context_prompt(regla, ocr_pages)

        assert "Identificación" in prompt
        assert "Texto" in prompt
        assert "Fecha" in prompt

    def test_prompt_incluye_texto_ocr(self):
        """CA-01: El prompt incluye el texto OCR del documento."""
        regla = FakeRegla()
        ocr_pages = [FakeOcrPage()]
        prompt = build_context_prompt(regla, ocr_pages)

        assert "REPÚBLICA DE COLOMBIA" in prompt
        assert "1234567" in prompt
        assert "DAVID RODRÍGUEZ" in prompt

    def test_prompt_incluye_confianza_ocr(self):
        """CA-01: El prompt incluye scores de confianza OCR."""
        regla = FakeRegla()
        ocr_pages = [FakeOcrPage()]
        prompt = build_context_prompt(regla, ocr_pages)

        assert "97.5%" in prompt

    def test_prompt_incluye_instruccion_json(self):
        """CA-01: El prompt incluye instrucción de retorno JSON."""
        regla = FakeRegla()
        ocr_pages = [FakeOcrPage()]
        prompt = build_context_prompt(regla, ocr_pages)

        assert "JSON" in prompt
        assert "tipo_documento_detectado" in prompt
        assert "campos_extraidos" in prompt

    def test_prompt_multiples_paginas(self):
        """Verifica que el prompt incluye múltiples páginas OCR."""
        regla = FakeRegla()
        ocr_pages = [
            FakeOcrPage(numero_pagina=1),
            FakeOcrPage(numero_pagina=2, confianza_promedio=95.0),
        ]
        prompt = build_context_prompt(regla, ocr_pages)

        assert "Página 1" in prompt
        assert "Página 2" in prompt

    def test_prompt_no_incluye_datos_otros_clientes(self):
        """CA-10: El prompt solo contiene datos del documento actual."""
        regla = FakeRegla(id=1)
        ocr_pages = [FakeOcrPage()]
        prompt = build_context_prompt(regla, ocr_pages)

        # El prompt no debe incluir IDs de otros clientes ni referencias externas
        assert "cliente_id" not in prompt.lower()
        # Solo incluye la regla y el OCR proporcionados
        assert isinstance(prompt, str)
        assert len(prompt) > 0


# -----------------------------------------------------------------------
# Tests de funciones internas
# -----------------------------------------------------------------------

class TestParsearCamposRegla:
    """Tests para _parsear_campos_regla."""

    def test_parsea_json_string(self):
        campos = _parsear_campos_regla('[{"nombre": "CC", "tipo": "Texto"}]')
        assert len(campos) == 1
        assert campos[0]["nombre"] == "CC"

    def test_json_invalido_retorna_vacio(self):
        campos = _parsear_campos_regla("esto no es json")
        assert campos == []

    def test_lista_directa(self):
        campos = _parsear_campos_regla([{"nombre": "CC"}])
        assert len(campos) == 1


class TestExtraerTextoPagina:
    """Tests para _extraer_texto_pagina."""

    def test_extrae_texto_de_bloques(self):
        data = json.dumps([
            {"text": "Hola", "confidence": 99.0},
            {"text": "Mundo", "confidence": 98.0},
        ])
        resultado = _extraer_texto_pagina(data)
        assert "Hola" in resultado
        assert "Mundo" in resultado

    def test_sin_datos_retorna_placeholder(self):
        resultado = _extraer_texto_pagina(None)
        assert "sin texto" in resultado.lower()

    def test_texto_plano(self):
        resultado = _extraer_texto_pagina("texto plano directo")
        assert resultado == "texto plano directo"
