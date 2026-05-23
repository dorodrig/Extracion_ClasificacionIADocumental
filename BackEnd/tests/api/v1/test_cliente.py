"""
Tests para los endpoints del portal de cliente (HU-07).

CAs cubiertos: CA-01, CA-02, CA-03, CA-04, CA-05, CA-07, CA-08, CA-09, CA-12.
"""
import pytest
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.models.documentos_clasificados import DocumentoClasificado
from app.db.models.documentos_pendientes import DocumentoPendiente


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _seed_clasificados(db: Session, cliente_id: int = 1, count: int = 3):
    """Inserta documentos clasificados de prueba."""
    for i in range(count):
        doc = DocumentoClasificado(
            cliente_id=cliente_id,
            batch_id=f"batch-test-{i}",
            regla_id=1,
            documento_id=1000 + i,
            campos_extraidos_json={"campo_a": f"valor_{i}", "monto": {"valor": i * 100, "confianza": 95.0}},
            ruta_destino_final=f"Facturas/2026/doc_{i}.pdf",
            tipo_documento="Factura" if i % 2 == 0 else "Contrato",
        )
        db.add(doc)
    db.commit()


def _seed_clasificado_otro_cliente(db: Session):
    """Inserta un documento que pertenece a otro cliente (cliente_id=999)."""
    doc = DocumentoClasificado(
        cliente_id=999,
        batch_id="batch-otro",
        regla_id=1,
        documento_id=9999,
        campos_extraidos_json={"secreto": "valor"},
        ruta_destino_final="Privado/secreto.pdf",
        tipo_documento="Privado",
    )
    db.add(doc)
    db.commit()
    return doc


# ---------------------------------------------------------------------------
# CA-02 & CA-09 — Dashboard
# ---------------------------------------------------------------------------

class TestDashboard:
    def test_dashboard_returns_200(self, client: TestClient):
        """CA-02: El endpoint de dashboard responde con 200."""
        response = client.get("/api/v1/cliente/dashboard")
        assert response.status_code == 200

    def test_dashboard_has_expected_fields(self, client: TestClient):
        """CA-02 / CA-09: El JSON contiene todas las métricas requeridas."""
        response = client.get("/api/v1/cliente/dashboard")
        data = response.json()
        assert "total_documentos" in data
        assert "documentos_nuevos" in data
        assert "pendientes_revision" in data
        assert "ultimo_procesado" in data
        assert "tipos_conteo" in data

    def test_dashboard_conteo_tipos_is_dict(self, client: TestClient):
        """CA-02: tipos_conteo es un diccionario."""
        response = client.get("/api/v1/cliente/dashboard")
        data = response.json()
        assert isinstance(data["tipos_conteo"], dict)

    def test_dashboard_pendientes_is_int(self, client: TestClient):
        """CA-09: pendientes_revision es un entero."""
        response = client.get("/api/v1/cliente/dashboard")
        data = response.json()
        assert isinstance(data["pendientes_revision"], int)


# ---------------------------------------------------------------------------
# CA-03 & CA-12 — Carpetas
# ---------------------------------------------------------------------------

class TestCarpetas:
    def test_carpetas_returns_200(self, client: TestClient):
        """CA-03: El endpoint de carpetas responde con 200."""
        response = client.get("/api/v1/cliente/carpetas")
        assert response.status_code == 200

    def test_carpetas_has_root_node(self, client: TestClient):
        """CA-12: El árbol tiene un nodo raíz con id y nombre."""
        response = client.get("/api/v1/cliente/carpetas")
        data = response.json()
        assert "id" in data
        assert "nombre" in data
        assert "hijos" in data
        assert data["id"] == "root"

    def test_carpetas_hijos_is_list(self, client: TestClient):
        """CA-12: hijos es una lista."""
        response = client.get("/api/v1/cliente/carpetas")
        data = response.json()
        assert isinstance(data["hijos"], list)


# ---------------------------------------------------------------------------
# CA-04 — Listado paginado de documentos
# ---------------------------------------------------------------------------

class TestDocumentos:
    def test_documentos_returns_200(self, client: TestClient):
        """CA-04: El endpoint responde con 200."""
        response = client.get("/api/v1/cliente/documentos")
        assert response.status_code == 200

    def test_documentos_has_pagination_fields(self, client: TestClient):
        """CA-04: Respuesta incluye total, page, size, items."""
        response = client.get("/api/v1/cliente/documentos")
        data = response.json()
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert "items" in data

    def test_documentos_pagination_params(self, client: TestClient):
        """CA-04: Respeta parámetros de paginación."""
        response = client.get("/api/v1/cliente/documentos?page=2&size=5")
        data = response.json()
        assert data["page"] == 2
        assert data["size"] == 5

    def test_documentos_filter_tipo(self, client: TestClient):
        """CA-04: Acepta filtro tipo_documento sin error."""
        response = client.get("/api/v1/cliente/documentos?tipo_documento=Factura")
        assert response.status_code == 200

    def test_documentos_filter_busqueda(self, client: TestClient):
        """CA-04: Acepta filtro de búsqueda."""
        response = client.get("/api/v1/cliente/documentos?busqueda=test")
        assert response.status_code == 200

    def test_documentos_items_is_list(self, client: TestClient):
        """CA-04: items es una lista."""
        response = client.get("/api/v1/cliente/documentos")
        data = response.json()
        assert isinstance(data["items"], list)


# ---------------------------------------------------------------------------
# CA-05 — Detalle de documento
# ---------------------------------------------------------------------------

class TestDocumentoDetail:
    def test_detail_not_found_returns_404(self, client: TestClient):
        """CA-05: Documento inexistente retorna 404."""
        response = client.get("/api/v1/cliente/documentos/99999")
        assert response.status_code == 404

    def test_detail_forbidden_returns_403(self, client: TestClient, db_session: Session):
        """CA-01 / CA-08: Documento de otro cliente retorna 403."""
        doc = _seed_clasificado_otro_cliente(db_session)
        response = client.get(f"/api/v1/cliente/documentos/{doc.id}")
        assert response.status_code == 403

    def test_detail_success_returns_200(self, client: TestClient, db_session: Session):
        """CA-05: Documento del cliente retorna 200 con campos extraídos."""
        _seed_clasificados(db_session, cliente_id=1, count=1)
        doc = db_session.query(DocumentoClasificado).filter_by(cliente_id=1).first()
        response = client.get(f"/api/v1/cliente/documentos/{doc.id}")
        assert response.status_code == 200
        data = response.json()
        assert "campos_extraidos" in data
        assert "id" in data


# ---------------------------------------------------------------------------
# CA-07 — Descarga
# ---------------------------------------------------------------------------

class TestDescarga:
    def test_descargar_not_found_returns_404(self, client: TestClient):
        """CA-07: Descarga de documento inexistente retorna 404."""
        response = client.get("/api/v1/cliente/documentos/99999/descargar")
        assert response.status_code == 404

    def test_descargar_returns_pdf_content(self, client: TestClient, db_session: Session):
        """CA-07: Descarga retorna contenido con Content-Disposition."""
        _seed_clasificados(db_session, cliente_id=1, count=1)
        doc = db_session.query(DocumentoClasificado).filter_by(cliente_id=1).first()
        response = client.get(f"/api/v1/cliente/documentos/{doc.id}/descargar")
        assert response.status_code == 200
        assert "content-disposition" in response.headers

    def test_archivo_not_found_returns_404(self, client: TestClient):
        """Visualización de archivo inexistente retorna 404."""
        response = client.get("/api/v1/cliente/documentos/99999/archivo")
        assert response.status_code == 404
