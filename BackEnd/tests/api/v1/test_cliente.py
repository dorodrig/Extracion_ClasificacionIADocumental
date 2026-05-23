from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_get_dashboard(client: TestClient):
    response = client.get("/api/v1/cliente/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "total_documentos" in data
    assert "pendientes_revision" in data
    assert data["total_documentos"] > 0

def test_get_carpetas(client: TestClient):
    response = client.get("/api/v1/cliente/carpetas")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "root"
    assert "hijos" in data

def test_get_documentos(client: TestClient):
    response = client.get("/api/v1/cliente/documentos?page=1&size=5")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 100
    assert len(data["items"]) == 5

def test_get_documento_detail_success(client: TestClient):
    response = client.get("/api/v1/cliente/documentos/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "campos_extraidos" in data

def test_get_documento_detail_forbidden(client: TestClient):
    # Testing the mocked forbidden check (id == 999)
    response = client.get("/api/v1/cliente/documentos/999")
    assert response.status_code == 403
    data = response.json()
    assert "detail" in data

def test_descargar_documento(client: TestClient):
    response = client.get("/api/v1/cliente/documentos/1/descargar")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]
