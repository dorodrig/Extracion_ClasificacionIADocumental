"""
Tests de integración para los endpoints REST de Reglas de Trabajo.

Cobertura: app/api/v1/endpoints/rules.py
CAs cubiertos: CA-01, CA-02, CA-03, CA-04, CA-05, CA-06.

Usa SQLite en memoria como base de datos de prueba para evitar
dependencia de SQL Server durante los tests.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base

# ---------------------------------------------------------------------------
# Configuración de BD de prueba (SQLite en memoria)
# ---------------------------------------------------------------------------

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test,
)


def override_get_db():
    """Override de get_db para usar la BD de prueba."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Import app AFTER setting up the test DB to avoid early engine creation
from app.core.dependencies import get_db  # noqa: E402
from app.main import app  # noqa: E402

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Crea las tablas antes de cada test y las elimina después."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


client = TestClient(app)

# ---------------------------------------------------------------------------
# Datos de prueba reutilizables
# ---------------------------------------------------------------------------

VALID_RULE_DATA = {
    "cliente_id": 1,
    "nombre": "Regla Cédulas",
    "tipo_documento": "Cédula de Ciudadanía",
    "campos_extraer": [
        {"nombre": "Número de Cédula", "tipo": "Identificación", "obligatorio": True},
        {"nombre": "Nombre Completo", "tipo": "Texto", "obligatorio": True},
    ],
    "patron_carpeta": "{Número de Cédula}/{Nombre Completo}",
    "modo_entrada": "scanner",
}


def create_test_rule(data: dict | None = None) -> dict:
    """Helper: crea una regla y retorna la respuesta JSON completa."""
    payload = data or VALID_RULE_DATA
    response = client.post("/api/v1/rules", json=payload)
    return response.json()


# ---------------------------------------------------------------------------
# CA-01 — Primer acceso de cliente sin reglas previas
# ---------------------------------------------------------------------------


class TestCA01ListaVacia:
    """CA-01: El sistema retorna lista vacía si no hay reglas."""

    def test_cliente_sin_reglas_retorna_lista_vacia(self):
        """GET /rules con cliente sin reglas retorna data=[] y success=True."""
        response = client.get("/api/v1/rules", params={"cliente_id": 999})
        assert response.status_code == 200

        body = response.json()
        assert body["success"] is True
        assert body["data"] == []
        assert "no tiene reglas" in body["message"].lower()

    def test_cliente_id_requerido(self):
        """GET /rules sin cliente_id retorna 422 (validation error)."""
        response = client.get("/api/v1/rules")
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# CA-02 — Visualización del listado de reglas existentes
# ---------------------------------------------------------------------------


class TestCA02ListadoReglas:
    """CA-02: El sistema muestra listado de reglas del cliente."""

    def test_listar_reglas_existentes(self):
        """GET /rules con reglas existentes retorna la lista correcta."""
        # Crear dos reglas
        create_test_rule()
        create_test_rule({
            **VALID_RULE_DATA,
            "nombre": "Regla Pasaportes",
            "tipo_documento": "Pasaporte",
        })

        response = client.get("/api/v1/rules", params={"cliente_id": 1})
        assert response.status_code == 200

        body = response.json()
        assert body["success"] is True
        assert len(body["data"]) == 2

        # Verificar campos presentes en cada regla
        regla = body["data"][0]
        assert "nombre" in regla
        assert "tipo_documento" in regla
        assert "created_at" in regla
        assert "updated_at" in regla
        assert "version" in regla

    def test_reglas_no_se_mezclan_entre_clientes(self):
        """Las reglas de un cliente no aparecen en las de otro."""
        create_test_rule()
        create_test_rule({
            **VALID_RULE_DATA,
            "cliente_id": 2,
            "nombre": "Regla Cliente 2",
        })

        # Solo la regla del cliente 1
        response = client.get("/api/v1/rules", params={"cliente_id": 1})
        body = response.json()
        assert len(body["data"]) == 1
        assert body["data"][0]["nombre"] == "Regla Cédulas"


# ---------------------------------------------------------------------------
# CA-03 — Carga de regla existente para edición
# ---------------------------------------------------------------------------


class TestCA03DetalleRegla:
    """CA-03: El sistema carga el detalle completo de una regla."""

    def test_obtener_detalle_regla(self):
        """GET /rules/{id} retorna todos los campos incluyendo campos_extraer."""
        created = create_test_rule()
        rule_id = created["data"]["id"]

        response = client.get(f"/api/v1/rules/{rule_id}")
        assert response.status_code == 200

        body = response.json()
        assert body["success"] is True
        assert body["data"]["id"] == rule_id
        assert body["data"]["nombre"] == "Regla Cédulas"
        assert len(body["data"]["campos_extraer"]) == 2
        assert body["data"]["campos_extraer"][0]["nombre"] == "Número de Cédula"

    def test_regla_no_existente_retorna_404(self):
        """GET /rules/{id} con ID inexistente retorna 404."""
        response = client.get("/api/v1/rules/99999")
        assert response.status_code == 404

        body = response.json()
        assert body["success"] is False


# ---------------------------------------------------------------------------
# CA-04 — Creación de nueva regla
# ---------------------------------------------------------------------------


class TestCA04CrearRegla:
    """CA-04: El sistema permite crear nuevas reglas con ID automático."""

    def test_crear_regla_exitosamente(self):
        """POST /rules con datos válidos retorna 201 con ID generado."""
        response = client.post("/api/v1/rules", json=VALID_RULE_DATA)
        assert response.status_code == 201

        body = response.json()
        assert body["success"] is True
        assert body["data"]["id"] is not None
        assert body["data"]["nombre"] == "Regla Cédulas"
        assert body["data"]["version"] == 1
        assert body["data"]["activa"] is True

    def test_crear_multiples_reglas_ids_diferentes(self):
        """Cada regla creada tiene un ID único diferente."""
        r1 = create_test_rule()
        r2 = create_test_rule({
            **VALID_RULE_DATA,
            "nombre": "Otra Regla",
        })
        assert r1["data"]["id"] != r2["data"]["id"]

    def test_crear_regla_no_modifica_existentes(self):
        """Crear una nueva regla no modifica las reglas existentes del cliente."""
        r1 = create_test_rule()
        original_id = r1["data"]["id"]

        create_test_rule({
            **VALID_RULE_DATA,
            "nombre": "Regla Nueva",
        })

        # Verificar que la primera regla no cambió
        response = client.get(f"/api/v1/rules/{original_id}")
        assert response.json()["data"]["nombre"] == "Regla Cédulas"


# ---------------------------------------------------------------------------
# CA-05 — Validación de campos obligatorios
# ---------------------------------------------------------------------------


class TestCA05ValidacionObligatoria:
    """CA-05: El sistema valida campos obligatorios al guardar."""

    def test_falta_nombre(self):
        """POST /rules sin nombre retorna 422."""
        data = {**VALID_RULE_DATA}
        del data["nombre"]
        response = client.post("/api/v1/rules", json=data)
        assert response.status_code == 422

    def test_falta_tipo_documento(self):
        """POST /rules sin tipo_documento retorna 422."""
        data = {**VALID_RULE_DATA}
        del data["tipo_documento"]
        response = client.post("/api/v1/rules", json=data)
        assert response.status_code == 422

    def test_falta_campos_extraer(self):
        """POST /rules sin campos_extraer retorna 422."""
        data = {**VALID_RULE_DATA}
        del data["campos_extraer"]
        response = client.post("/api/v1/rules", json=data)
        assert response.status_code == 422

    def test_campos_extraer_vacio(self):
        """POST /rules con campos_extraer=[] retorna 422 (min_length=1)."""
        data = {**VALID_RULE_DATA, "campos_extraer": []}
        response = client.post("/api/v1/rules", json=data)
        assert response.status_code == 422

    def test_falta_patron_carpeta(self):
        """POST /rules sin patron_carpeta retorna 422."""
        data = {**VALID_RULE_DATA}
        del data["patron_carpeta"]
        response = client.post("/api/v1/rules", json=data)
        assert response.status_code == 422

    def test_falta_modo_entrada(self):
        """POST /rules sin modo_entrada retorna 422."""
        data = {**VALID_RULE_DATA}
        del data["modo_entrada"]
        response = client.post("/api/v1/rules", json=data)
        assert response.status_code == 422

    def test_modo_entrada_invalido(self):
        """POST /rules con modo_entrada inválido retorna 400."""
        data = {**VALID_RULE_DATA, "modo_entrada": "usb"}
        response = client.post("/api/v1/rules", json=data)
        assert response.status_code == 400

        body = response.json()
        assert body["success"] is False
        assert "usb" in body["error"]


# ---------------------------------------------------------------------------
# CA-06 — Definición dinámica de campos a extraer
# ---------------------------------------------------------------------------


class TestCA06CamposDinamicos:
    """CA-06: El sistema valida campos dinámicos a extraer."""

    def test_campos_duplicados_exactos(self):
        """POST /rules con campos duplicados exactos retorna 400."""
        data = {
            **VALID_RULE_DATA,
            "campos_extraer": [
                {"nombre": "Cédula", "tipo": "Identificación", "obligatorio": True},
                {"nombre": "Cédula", "tipo": "Texto", "obligatorio": False},
            ],
        }
        response = client.post("/api/v1/rules", json=data)
        assert response.status_code == 400

        body = response.json()
        assert body["success"] is False
        assert "duplicado" in body["error"].lower()

    def test_campos_duplicados_case_insensitive(self):
        """POST /rules con campos duplicados case-insensitive retorna 400."""
        data = {
            **VALID_RULE_DATA,
            "campos_extraer": [
                {"nombre": "Cédula", "tipo": "Identificación", "obligatorio": True},
                {"nombre": "cédula", "tipo": "Texto", "obligatorio": False},
            ],
        }
        response = client.post("/api/v1/rules", json=data)
        assert response.status_code == 400

    def test_multiples_campos_validos(self):
        """POST /rules con N campos únicos es exitoso."""
        data = {
            **VALID_RULE_DATA,
            "campos_extraer": [
                {"nombre": "Campo 1", "tipo": "Texto", "obligatorio": True},
                {"nombre": "Campo 2", "tipo": "Número", "obligatorio": False},
                {"nombre": "Campo 3", "tipo": "Fecha", "obligatorio": False},
                {"nombre": "Campo 4", "tipo": "Identificación", "obligatorio": True},
            ],
            "patron_carpeta": "{Campo 1}",
        }
        response = client.post("/api/v1/rules", json=data)
        assert response.status_code == 201
        assert len(response.json()["data"]["campos_extraer"]) == 4


# ---------------------------------------------------------------------------
# Tests de actualización (PUT)
# ---------------------------------------------------------------------------


class TestUpdateRegla:
    """Tests para el endpoint PUT /rules/{id}."""

    def test_actualizar_regla_exitosamente(self):
        """PUT /rules/{id} actualiza los datos y incrementa version."""
        created = create_test_rule()
        rule_id = created["data"]["id"]

        update_data = {
            "nombre": "Regla Actualizada",
            "tipo_documento": "Pasaporte",
            "campos_extraer": [
                {"nombre": "Número Pasaporte", "tipo": "Identificación", "obligatorio": True},
            ],
            "patron_carpeta": "{Número Pasaporte}/{mes}",
            "modo_entrada": "carpeta",
        }

        response = client.put(f"/api/v1/rules/{rule_id}", json=update_data)
        assert response.status_code == 200

        body = response.json()
        assert body["success"] is True
        assert body["data"]["nombre"] == "Regla Actualizada"
        assert body["data"]["version"] == 2  # Incremento automático
        assert body["data"]["modo_entrada"] == "carpeta"

    def test_actualizar_regla_inexistente(self):
        """PUT /rules/{id} con ID inexistente retorna 404."""
        update_data = {
            "nombre": "No importa",
            "tipo_documento": "No importa",
            "campos_extraer": [
                {"nombre": "Campo", "tipo": "Texto", "obligatorio": True},
            ],
            "patron_carpeta": "{Campo}/importa",
            "modo_entrada": "scanner",
        }
        response = client.put("/api/v1/rules/99999", json=update_data)
        assert response.status_code == 404

    def test_actualizar_con_campos_duplicados(self):
        """PUT /rules/{id} con campos duplicados retorna 400."""
        created = create_test_rule()
        rule_id = created["data"]["id"]

        update_data = {
            "nombre": "Regla X",
            "tipo_documento": "Doc",
            "campos_extraer": [
                {"nombre": "Campo", "tipo": "Texto", "obligatorio": True},
                {"nombre": "campo", "tipo": "Número", "obligatorio": False},
            ],
            "patron_carpeta": "{Campo}",
            "modo_entrada": "scanner",
        }
        response = client.put(f"/api/v1/rules/{rule_id}", json=update_data)
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# CA-07 — Validación de patrón de carpeta
# ---------------------------------------------------------------------------

class TestCA07ValidacionPatronCarpeta:
    """CA-07: Validación del patrón de carpeta."""
    
    def test_patron_sin_variables_retorna_400(self):
        """POST /rules con patrón sin variables retorna 400."""
        data = {**VALID_RULE_DATA, "patron_carpeta": "salida"}
        response = client.post("/api/v1/rules", json=data)
        assert response.status_code == 400
        assert "patrón de carpeta" in response.json()["error"].lower()

    def test_patron_con_variable_invalida_retorna_400(self):
        """POST /rules con variable no definida en campos retorna 400."""
        data = {**VALID_RULE_DATA, "patron_carpeta": "{CampoFalso}"}
        response = client.post("/api/v1/rules", json=data)
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# CA-11 — Duplicar regla
# ---------------------------------------------------------------------------

class TestCA11DuplicarRegla:
    """CA-11: Duplicar regla existente."""
    
    def test_duplicar_regla_exitosamente(self):
        """POST /rules/{id}/duplicate crea copia con sufijo."""
        created = create_test_rule({
            "cliente_id": 88,
            "nombre": "Regla Base",
            "tipo_documento": "doc",
            "campos_extraer": [{"nombre": "C", "tipo": "Texto", "obligatorio": True}],
            "patron_carpeta": "{C}",
            "modo_entrada": "scanner"
        })
        rule_id = created["data"]["id"]
        
        response = client.post(f"/api/v1/rules/{rule_id}/duplicate")
        assert response.status_code == 201
        
        body = response.json()
        assert body["data"]["nombre"] == "Regla Base (Copia)"
        assert body["data"]["version"] == 1
        assert len(body["data"]["campos_extraer"]) == 1
        
    def test_duplicar_multiples_veces(self):
        """Múltiples duplicaciones incrementan el sufijo."""
        created = create_test_rule({
            "cliente_id": 99, 
            "nombre": "MultiDupla", 
            "tipo_documento": "doc", 
            "campos_extraer": [{"nombre": "C", "tipo": "Texto", "obligatorio": True}], 
            "patron_carpeta": "{C}", 
            "modo_entrada": "scanner"
        })
        rule_id = created["data"]["id"]
        
        r1 = client.post(f"/api/v1/rules/{rule_id}/duplicate")
        assert r1.json()["data"]["nombre"] == "MultiDupla (Copia)"
        
        r2 = client.post(f"/api/v1/rules/{rule_id}/duplicate")
        assert r2.json()["data"]["nombre"] == "MultiDupla (Copia 2)"

    def test_duplicar_inexistente_retorna_404(self):
        """POST /rules/99999/duplicate retorna 404."""
        response = client.post("/api/v1/rules/99999/duplicate")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# CA-12 — Nombre único retorna 409 Conflict
# ---------------------------------------------------------------------------

class TestCA12NombreUnico:
    """CA-12: Validación de nombre único."""
    
    def test_crear_nombre_duplicado_retorna_409(self):
        """Crear regla con nombre que ya existe retorna 409 Conflict."""
        create_test_rule({
            "cliente_id": 100, 
            "nombre": "Regla Unica", 
            "tipo_documento": "doc", 
            "campos_extraer": [{"nombre": "C", "tipo": "Texto", "obligatorio": True}], 
            "patron_carpeta": "{C}", 
            "modo_entrada": "scanner"
        })
        response = client.post("/api/v1/rules", json={
            "cliente_id": 100, 
            "nombre": "Regla Unica", 
            "tipo_documento": "doc", 
            "campos_extraer": [{"nombre": "C", "tipo": "Texto", "obligatorio": True}], 
            "patron_carpeta": "{C}", 
            "modo_entrada": "scanner"
        })
        assert response.status_code == 409
        assert "Ya existe una regla con el nombre" in response.json()["error"]


# ---------------------------------------------------------------------------
# Tests de Health Check
# ---------------------------------------------------------------------------


class TestHealthCheck:
    """Test del endpoint de health check."""

    def test_health_check(self):
        """GET /health retorna status healthy."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
