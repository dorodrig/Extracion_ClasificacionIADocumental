"""
Tests de integración para ContextoIAService.

HU-04 — Tests con mock del GeminiAdapter para verificar:
    CA-03: Parseo JSON con reintentos
    CA-04: Validación de campos obligatorios
    CA-05: Enrutamiento a revisión humana
    CA-06: Enrutamiento a clasificación
    CA-07: Detección de tipo de documento
    CA-08: Manejo de timeout/error API
    CA-09: Registro en log_ia_invocaciones
    CA-11: Normalización de valores
    CA-12: Persistencia en agente_contexto_resultados
"""
import json
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.db.models.contexto_resultado_db import AgenteContextoResultados
from app.db.models.documento_db import DocumentosLote
from app.db.models.log_ia_invocacion_db import LogIAInvocacion
from app.db.models.ocr_db import OcrResultadosPaginas
from app.db.models.rule_db import ReglasTrabajo
from app.domain.exceptions_ia import GeminiApiTimeoutException
from app.services.contexto_ia_service import (
    ESTADO_ERROR_IA,
    ESTADO_LISTO_CLASIFICACION,
    ESTADO_PENDIENTE_HUMANO,
    ContextoIAService,
)
from app.services.gemini_adapter import GeminiResponse


# -----------------------------------------------------------------------
# Fixtures de BD en memoria
# -----------------------------------------------------------------------

@pytest.fixture
def db_session():
    """Crea una BD SQLite en memoria con todas las tablas."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def sample_regla(db_session):
    """Crea una regla de trabajo de prueba."""
    regla = ReglasTrabajo(
        id=1,
        cliente_id=1,
        nombre="Regla Test Cédulas",
        tipo_documento="Cédula de Ciudadanía",
        campos_extraer=json.dumps([
            {"nombre": "Número de Cédula", "tipo": "Identificación", "obligatorio": True},
            {"nombre": "Nombre Completo", "tipo": "Texto", "obligatorio": True},
            {"nombre": "Fecha de Expedición", "tipo": "Fecha", "obligatorio": False},
        ]),
        patron_carpeta="{cliente}/{tipo_doc}/{año}",
        modo_entrada="scanner",
    )
    db_session.add(regla)
    db_session.commit()
    return regla


@pytest.fixture
def sample_documento(db_session):
    """Crea un documento de prueba."""
    doc = DocumentosLote(
        id=1,
        nombre_archivo="cedula_test.pdf",
        estado="OCR_COMPLETADO",
    )
    db_session.add(doc)
    db_session.commit()
    return doc


@pytest.fixture
def sample_ocr_pages(db_session, sample_documento):
    """Crea páginas OCR de prueba."""
    page = OcrResultadosPaginas(
        documento_id=sample_documento.id,
        numero_pagina=1,
        bloques_raw_json="{}",
        campos_parseados=json.dumps([
            {"text": "REPÚBLICA DE COLOMBIA", "confidence": 99.1, "type": "LINE"},
            {"text": "CÉDULA DE CIUDADANÍA", "confidence": 98.5, "type": "LINE"},
            {"text": "1.234.567", "confidence": 97.0, "type": "WORD"},
            {"text": "DAVID RODRÍGUEZ LÓPEZ", "confidence": 96.8, "type": "LINE"},
            {"text": "15/03/2020", "confidence": 95.2, "type": "WORD"},
        ]),
        confianza_promedio=97.5,
        estado="OCR Completado",
        tiempo_proceso_ms=450,
    )
    db_session.add(page)
    db_session.commit()
    return [page]


def _make_mock_adapter(response_text: str) -> MagicMock:
    """Crea un mock del GeminiAdapter con respuesta predefinida."""
    adapter = MagicMock()
    adapter.invoke.return_value = GeminiResponse(
        texto=response_text,
        tokens_entrada=150,
        tokens_salida=80,
        duracion_ms=1200,
        modelo="gemini-1.5-pro",
    )
    return adapter


def _valid_gemini_response() -> str:
    """Retorna una respuesta JSON válida de Gemini."""
    return json.dumps({
        "tipo_documento_detectado": "Cédula de Ciudadanía",
        "confianza_tipo": 95.0,
        "campos_extraidos": [
            {"nombre": "Número de Cédula", "valor": "1.234.567", "confianza_ocr": 97.0, "validado_ia": True},
            {"nombre": "Nombre Completo", "valor": "DAVID RODRÍGUEZ LÓPEZ", "confianza_ocr": 96.8, "validado_ia": True},
            {"nombre": "Fecha de Expedición", "valor": "15/03/2020", "confianza_ocr": 95.2, "validado_ia": True},
        ],
        "observaciones": "Documento legible con alta confianza."
    })


def _incomplete_gemini_response() -> str:
    """Retorna una respuesta donde un campo obligatorio está vacío."""
    return json.dumps({
        "tipo_documento_detectado": "Cédula de Ciudadanía",
        "confianza_tipo": 92.0,
        "campos_extraidos": [
            {"nombre": "Número de Cédula", "valor": "1.234.567", "confianza_ocr": 97.0, "validado_ia": True},
            {"nombre": "Nombre Completo", "valor": "", "confianza_ocr": 0.0, "validado_ia": False},
        ],
        "observaciones": "No se pudo extraer el nombre completo."
    })


def _wrong_type_response() -> str:
    """Retorna una respuesta con tipo de documento completamente diferente."""
    return json.dumps({
        "tipo_documento_detectado": "Recibo de agua",
        "confianza_tipo": 88.0,
        "campos_extraidos": [
            {"nombre": "Número de Cédula", "valor": "1.234.567", "confianza_ocr": 97.0, "validado_ia": True},
            {"nombre": "Nombre Completo", "valor": "DAVID RODRÍGUEZ", "confianza_ocr": 96.8, "validado_ia": True},
        ],
        "observaciones": ""
    })


# -----------------------------------------------------------------------
# Tests CA-03: Parseo JSON y reintentos
# -----------------------------------------------------------------------

class TestCA03ParseoJSON:
    """CA-03: Parseo de respuesta JSON y reintentos."""

    @pytest.mark.asyncio
    async def test_json_valido_primer_intento(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """JSON válido en el primer intento → procesamiento exitoso."""
        adapter = _make_mock_adapter(_valid_gemini_response())
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        assert resultado is not None
        assert resultado.estado != ESTADO_ERROR_IA
        assert adapter.invoke.call_count == 1

    @pytest.mark.asyncio
    async def test_json_invalido_reintentos_agotan(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """JSON inválido → reintentos x2 → estado error_ia."""
        adapter = _make_mock_adapter("esto no es JSON válido")
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        assert resultado.estado == ESTADO_ERROR_IA
        assert resultado.motivo_rechazo == "Error de IA - Respuesta inválida"
        # 1 intento inicial + 2 reintentos = 3 invocaciones
        assert adapter.invoke.call_count == 3

    @pytest.mark.asyncio
    async def test_json_con_markdown_wrapper(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """JSON envuelto en ```json...``` → parseo exitoso."""
        json_wrapped = f"```json\n{_valid_gemini_response()}\n```"
        adapter = _make_mock_adapter(json_wrapped)
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        assert resultado.estado != ESTADO_ERROR_IA
        assert resultado.datos_completos is True


# -----------------------------------------------------------------------
# Tests CA-04: Validación de campos obligatorios
# -----------------------------------------------------------------------

class TestCA04ValidacionCampos:
    """CA-04: Validación de campos obligatorios."""

    @pytest.mark.asyncio
    async def test_todos_campos_presentes_datos_completos_true(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """Todos los campos obligatorios presentes → datos_completos=true."""
        adapter = _make_mock_adapter(_valid_gemini_response())
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        assert resultado.datos_completos is True

    @pytest.mark.asyncio
    async def test_campo_obligatorio_vacio_datos_completos_false(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """Campo obligatorio vacío → datos_completos=false."""
        adapter = _make_mock_adapter(_incomplete_gemini_response())
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        assert resultado.datos_completos is False
        assert "Nombre Completo" in resultado.motivo_rechazo


# -----------------------------------------------------------------------
# Tests CA-05 / CA-06: Enrutamiento por estado
# -----------------------------------------------------------------------

class TestCA05CA06Enrutamiento:
    """CA-05 y CA-06: Enrutamiento según datos_completos."""

    @pytest.mark.asyncio
    async def test_datos_completos_true_listo_clasificacion(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """CA-06: datos_completos=true → estado listo_clasificacion."""
        adapter = _make_mock_adapter(_valid_gemini_response())
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        assert resultado.estado == ESTADO_LISTO_CLASIFICACION
        assert resultado.motivo_rechazo is None

    @pytest.mark.asyncio
    async def test_datos_completos_false_pendiente_humano(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """CA-05: datos_completos=false → estado pendiente_humano + motivo."""
        adapter = _make_mock_adapter(_incomplete_gemini_response())
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        assert resultado.estado == ESTADO_PENDIENTE_HUMANO
        assert resultado.motivo_rechazo is not None
        assert len(resultado.motivo_rechazo) > 0


# -----------------------------------------------------------------------
# Tests CA-07: Detección de tipo de documento
# -----------------------------------------------------------------------

class TestCA07DeteccionTipo:
    """CA-07: Detección y comparación de tipo de documento."""

    @pytest.mark.asyncio
    async def test_tipo_coincide_sin_alerta(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """Tipo detectado = tipo esperado → sin alertas."""
        adapter = _make_mock_adapter(_valid_gemini_response())
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        assert resultado.datos_completos is True
        assert resultado.tipo_doc_detectado == "Cédula de Ciudadanía"

    @pytest.mark.asyncio
    async def test_tipo_completamente_diferente_datos_incompletos(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """CA-07: Tipo totalmente diferente → datos_completos=false."""
        adapter = _make_mock_adapter(_wrong_type_response())
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        assert resultado.datos_completos is False
        assert "Tipo de documento incorrecto" in resultado.motivo_rechazo


# -----------------------------------------------------------------------
# Tests CA-08: Timeout y error de API
# -----------------------------------------------------------------------

class TestCA08TimeoutAPI:
    """CA-08: Manejo de timeout/error de la API Gemini."""

    @pytest.mark.asyncio
    async def test_api_timeout_estado_error_ia(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """API timeout → estado error_ia."""
        adapter = MagicMock()
        adapter.invoke.side_effect = GeminiApiTimeoutException(
            intentos=4,
            ultimo_error="Connection timeout after 30s",
        )
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        assert resultado.estado == ESTADO_ERROR_IA
        assert resultado.datos_completos is False


# -----------------------------------------------------------------------
# Tests CA-09: Registro de invocaciones
# -----------------------------------------------------------------------

class TestCA09LogInvocaciones:
    """CA-09: Registro en log_ia_invocaciones."""

    @pytest.mark.asyncio
    async def test_invocacion_exitosa_registrada(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """Invocación exitosa → registro en log con exitoso=true."""
        adapter = _make_mock_adapter(_valid_gemini_response())
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        logs = db_session.query(LogIAInvocacion).all()
        assert len(logs) >= 1
        log_exitoso = [l for l in logs if l.exitoso is True]
        assert len(log_exitoso) >= 1
        assert log_exitoso[0].modelo == "gemini-1.5-pro"
        assert log_exitoso[0].tokens_entrada == 150
        assert log_exitoso[0].tokens_salida == 80

    @pytest.mark.asyncio
    async def test_invocacion_fallida_registrada(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """Invocación fallida → registro en log con exitoso=false."""
        adapter = MagicMock()
        adapter.invoke.side_effect = GeminiApiTimeoutException(
            intentos=4, ultimo_error="timeout"
        )
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        logs = db_session.query(LogIAInvocacion).all()
        assert len(logs) >= 1
        log_fallido = [l for l in logs if l.exitoso is False]
        assert len(log_fallido) >= 1


# -----------------------------------------------------------------------
# Tests CA-11: Normalización de valores
# -----------------------------------------------------------------------

class TestCA11Normalizacion:
    """CA-11: Normalización de valores extraídos."""

    @pytest.mark.asyncio
    async def test_identificacion_normalizada(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """Identificación con puntos → normalizada a solo dígitos."""
        adapter = _make_mock_adapter(_valid_gemini_response())
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        # Parsear campos del resultado
        paquete = json.loads(resultado.campos_extraidos_json)
        campos = paquete["campos_extraidos"]
        campo_cedula = next(
            (c for c in campos if "Cédula" in c["nombre"]), None
        )

        assert campo_cedula is not None
        assert campo_cedula["valor"] == "1234567"  # Sin puntos
        assert campo_cedula["valor_original"] == "1.234.567"  # Original preservado

    @pytest.mark.asyncio
    async def test_fecha_normalizada_iso(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """Fecha DD/MM/YYYY → normalizada a ISO 8601."""
        adapter = _make_mock_adapter(_valid_gemini_response())
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        paquete = json.loads(resultado.campos_extraidos_json)
        campos = paquete["campos_extraidos"]
        campo_fecha = next(
            (c for c in campos if "Expedición" in c["nombre"]), None
        )

        assert campo_fecha is not None
        assert campo_fecha["valor"] == "2020-03-15"  # ISO 8601
        assert campo_fecha["valor_original"] == "15/03/2020"


# -----------------------------------------------------------------------
# Tests CA-12: Persistencia en agente_contexto_resultados
# -----------------------------------------------------------------------

class TestCA12Persistencia:
    """CA-12: Consolidación en agente_contexto_resultados."""

    @pytest.mark.asyncio
    async def test_resultado_persistido_en_bd(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """El resultado se persiste correctamente en la BD."""
        adapter = _make_mock_adapter(_valid_gemini_response())
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        # Verificar persistencia
        from_db = (
            db_session.query(AgenteContextoResultados)
            .filter(AgenteContextoResultados.id == resultado.id)
            .first()
        )

        assert from_db is not None
        assert from_db.documento_id == sample_documento.id
        assert from_db.regla_id == sample_regla.id
        assert from_db.modelo_ia == "gemini-1.5-pro"
        assert from_db.tokens_entrada == 150
        assert from_db.tokens_salida == 80
        assert from_db.duracion_ms == 1200
        assert from_db.campos_extraidos_json is not None

    @pytest.mark.asyncio
    async def test_resultado_incluye_todos_campos_paquete(
        self, db_session, sample_regla, sample_documento, sample_ocr_pages
    ):
        """CA-12: El paquete JSON incluye todos los campos requeridos."""
        adapter = _make_mock_adapter(_valid_gemini_response())
        service = ContextoIAService(db_session, gemini_adapter=adapter)

        resultado = await service.procesar_documento(
            documento_id=sample_documento.id,
            regla_id=sample_regla.id,
        )

        paquete = json.loads(resultado.campos_extraidos_json)

        assert "campos_extraidos" in paquete
        assert "tipo_documento_detectado" in paquete
        assert "confianza_tipo" in paquete

        # Cada campo debe tener la estructura correcta
        for campo in paquete["campos_extraidos"]:
            assert "nombre" in campo
            assert "valor" in campo
            assert "valor_original" in campo
            assert "confianza_ocr" in campo
            assert "validado_ia" in campo
