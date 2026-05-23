# 📐 Gobernanza y Arquitectura — Proyecto GRM
**Sistema:** GRM — Gestión y Clasificación Documental con IA  
**Stack:** FastAPI (Python 3.12) + React 18 (TypeScript) + SQL Server 2019+  
**Estilos:** SASS (SCSS) + CSS puro — Design System GRM  
**Autor:** Arquitecto de Software Senior  
**Versión:** 1.1.0 — Documento Ley del Proyecto  
**Fecha:** 2026-05-22  

---

> ⚠️ **DOCUMENTO LEY**: Este archivo es la autoridad técnica máxima del proyecto GRM.  
> Todos los agentes (Frontend, Backend, Base de Datos) y desarrolladores humanos deben  
> alinearse estrictamente a las reglas aquí definidas. Las desviaciones requieren aprobación  
> explícita del Arquitecto Senior y deben ser documentadas como excepciones versionadas.

---

## 📋 ÍNDICE

1. [Mapa Arquitectónico del Sistema](#1-mapa-arquitectónico-del-sistema)
2. [Patrón Arquitectónico: Clean Architecture](#2-patrón-arquitectónico-clean-architecture)
3. [Reglas de Alineación — Agente Backend](#3-reglas-de-alineación--agente-backend)
4. [Reglas de Alineación — Agente Frontend](#4-reglas-de-alineación--agente-frontend)
   - 4.7 [Estándares SCSS / Design System](#47-estándares-scss--design-system-grm)
5. [Reglas de Alineación — Agente Base de Datos](#5-reglas-de-alineación--agente-base-de-datos)
6. [Estándares Transversales](#6-estándares-transversales)
7. [Arquitectura de Integración de SDKs (Google + AWS)](#7-arquitectura-de-integración-de-sdks-google--aws)
8. [Pipeline de Procesamiento Documental](#8-pipeline-de-procesamiento-documental)
9. [Estrategia de Migración Local → AWS Cloud](#9-estrategia-de-migración-local--aws-cloud)
10. [Cumplimiento ISO/IEC 25010](#10-cumplimiento-isoiec-25010)
11. [Matriz de Dependencias entre Agentes](#11-matriz-de-dependencias-entre-agentes)
12. [Control de Versiones y Branching Strategy](#12-control-de-versiones-y-branching-strategy)

---

## 1. Mapa Arquitectónico del Sistema

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ARQUITECTURA SISTEMA GRM — PILOTO ON-PREMISE             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    CAPA DE PRESENTACIÓN (Frontend)                  │    ║
║  │           React 18 + TypeScript + Vite 5 → localhost:5173           │    ║
║  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │    ║
║  │  │ Login /  │ │ Panel    │ │ Ingesta  │ │Pendientes│ │ Portal   │ │    ║
║  │  │ Auth     │ │ Admin    │ │Documentos│ │ Visor    │ │ Cliente  │ │    ║
║  │  │ (HU-08)  │ │ (HU-09)  │ │ (HU-02)  │ │ (HU-06)  │ │ (HU-07)  │ │    ║
║  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │    ║
║  └─────────────────────────┬───────────────────────────────────────────┘    ║
║                            │ HTTP/REST + WebSockets                         ║
║  ┌─────────────────────────▼───────────────────────────────────────────┐    ║
║  │                    CAPA DE APLICACIÓN (Backend)                     │    ║
║  │              FastAPI 0.115 + Uvicorn → localhost:8000               │    ║
║  │  ┌─────────────────────────────────────────────────────────────┐   │    ║
║  │  │                  API REST (v1)                              │   │    ║
║  │  │  /auth  /rules  /batches  /documents  /pendientes  /logs   │   │    ║
║  │  └──────────────────────────┬──────────────────────────────────┘   │    ║
║  │                             │                                       │    ║
║  │  ┌──────────────────────────▼──────────────────────────────────┐   │    ║
║  │  │              CAPA DE DOMINIO (Servicios + Agentes)          │   │    ║
║  │  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐  │   │    ║
║  │  │  │  AuthSvc  │ │  RulesSvc │ │  OCR Svc  │ │ StorageSvc│  │   │    ║
║  │  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘  │   │    ║
║  │  │  ┌────────────────────┐  ┌────────────────────────────┐    │   │    ║
║  │  │  │ Agente Contexto IA │  │ Agente Clasificación IA    │    │   │    ║
║  │  │  │ (Google Gemini SDK)│  │ (Google Gemini SDK)        │    │   │    ║
║  │  │  └────────────────────┘  └────────────────────────────┘    │   │    ║
║  │  └──────────────────────────────────────────────────────────────┘   │    ║
║  │                                                                     │    ║
║  │  ┌──────────────────────────────────────────────────────────────┐   │    ║
║  │  │              COLA DE PROCESAMIENTO (Celery + Redis)          │   │    ║
║  │  │     Workers: OCR Worker | ContextAgent Worker | ClassAgent  │   │    ║
║  │  └──────────────────────────────────────────────────────────────┘   │    ║
║  └─────────────────────────┬─────────────────┬───────────────────────┘    ║
║                            │                 │                              ║
║  ┌─────────────────────────▼───┐  ┌──────────▼──────────────────────────┐  ║
║  │    SQL Server 2019 (GRM_DB)  │  │   SERVICIOS EXTERNOS (APIs Cloud)   │  ║
║  │    localhost\SQLEXPRESS:1433 │  │  ┌──────────────┐ ┌──────────────┐  │  ║
║  │    15 tablas normalizadas    │  │  │ Google Gemini│ │ AWS Textract │  │  ║
║  │    SQLAlchemy ORM + Alembic  │  │  │ API (HTTPS)  │ │ API (HTTPS)  │  │  ║
║  └──────────────────────────────┘  │  └──────────────┘ └──────────────┘  │  ║
║                                    └────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Puertos y servicios
| Servicio | Puerto | Protocolo |
|---|---|---|
| FastAPI (Backend) | 8000 | HTTP/WebSocket |
| Vite Dev Server (Frontend) | 5173 | HTTP |
| SQL Server Express | 1433 | TCP |
| Redis (Broker Celery) | 6379 | TCP |

---

## 2. Patrón Arquitectónico: Clean Architecture

El sistema GRM implementa **Clean Architecture** (también denominada Arquitectura Hexagonal o Ports & Adapters), adaptada al stack FastAPI + React.

### 2.1 Diagrama de capas

```
╔══════════════════════════════════════════════════════════════╗
║                 CLEAN ARCHITECTURE — GRM BACKEND             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │  CAPA INFRAESTRUCTURA (Adapters)                     │   ║
║  │  app/api/       → Endpoints FastAPI (Controllers)    │   ║
║  │  app/db/        → SQLAlchemy Repositories            │   ║
║  │  app/workers/   → Celery Tasks                       │   ║
║  │  app/services/ocr/      → Adapter AWS Textract       │   ║
║  │  app/services/storage/  → Adapter Filesystem/S3      │   ║
║  └──────────────────────┬───────────────────────────────┘   ║
║                         │ Dependency Injection               ║
║  ┌──────────────────────▼───────────────────────────────┐   ║
║  │  CAPA APLICACIÓN (Use Cases)                         │   ║
║  │  app/services/rules_service.py                       │   ║
║  │  app/services/batch_service.py                       │   ║
║  │  app/services/classification_service.py              │   ║
║  │  app/services/ai_agents/context_agent.py             │   ║
║  │  app/services/ai_agents/classification_agent.py      │   ║
║  └──────────────────────┬───────────────────────────────┘   ║
║                         │ Pure Business Logic                ║
║  ┌──────────────────────▼───────────────────────────────┐   ║
║  │  CAPA DOMINIO (Entities + Business Rules)            │   ║
║  │  app/domain/models/   → Entidades de dominio puras   │   ║
║  │  app/domain/rules/    → Reglas de negocio            │   ║
║  │  app/domain/ports/    → Interfaces (Ports)           │   ║
║  └──────────────────────────────────────────────────────┘   ║
╚══════════════════════════════════════════════════════════════╝
```

### 2.2 Estructura de directorios obligatoria del Backend

```
C:\zData\ExtracionDatosIA\BackEnd\
├── app\
│   ├── main.py                         ← Entry point FastAPI
│   ├── api\
│   │   └── v1\
│   │       ├── __init__.py
│   │       ├── router.py               ← Registro de todos los routers
│   │       └── endpoints\
│   │           ├── auth.py             ← HU-08
│   │           ├── rules.py            ← HU-01
│   │           ├── batches.py          ← HU-02
│   │           ├── documents.py        ← HU-03, HU-05
│   │           ├── pendientes.py       ← HU-06
│   │           ├── client_portal.py    ← HU-07
│   │           └── admin_logs.py       ← HU-09
│   ├── core\
│   │   ├── config.py                   ← Settings (pydantic-settings)
│   │   ├── security.py                 ← JWT + hashing
│   │   └── dependencies.py             ← FastAPI Depends
│   ├── domain\
│   │   ├── models\                     ← Entidades puras (sin ORM)
│   │   ├── ports\                      ← Interfaces abstractas
│   │   └── rules\                      ← Validaciones de negocio
│   ├── db\
│   │   ├── database.py                 ← Engine + SessionLocal
│   │   ├── models\                     ← SQLAlchemy ORM Models
│   │   └── repositories\              ← Repositorios (acceso a datos)
│   ├── services\
│   │   ├── auth_service.py
│   │   ├── rules_service.py
│   │   ├── batch_service.py
│   │   ├── ocr\
│   │   │   └── textract_adapter.py     ← Adapter AWS Textract
│   │   ├── ai_agents\
│   │   │   ├── context_agent.py        ← HU-04 (Gemini)
│   │   │   └── classification_agent.py ← HU-05 (Gemini)
│   │   └── storage\
│   │       └── local_storage.py        ← Adapter filesystem (reemplazable por S3)
│   ├── schemas\
│   │   ├── auth.py                     ← Pydantic schemas de entrada/salida
│   │   ├── rules.py
│   │   ├── batches.py
│   │   └── documents.py
│   └── workers\
│       ├── celery_app.py               ← Configuración Celery
│       ├── ocr_worker.py               ← Task: procesamiento OCR
│       ├── context_worker.py           ← Task: Agente Contexto
│       └── classification_worker.py   ← Task: Agente Clasificación
├── alembic\                            ← Migraciones de BD
├── tests\                              ← Tests unitarios y de integración
├── .env                                ← Variables de entorno (NO a Git)
├── requirements.txt
└── .venv\                              ← Entorno virtual Python
```

---

## 3. Reglas de Alineación — Agente Backend

### 3.1 Estándares de Código Python

**Nombrado de variables y funciones:**
```python
# ✅ CORRECTO — snake_case para funciones y variables
def get_rules_by_client(client_id: int) -> list[RuleSchema]:
    batch_id = uuid.uuid4()
    campos_extraidos = []

# ❌ INCORRECTO — camelCase, PascalCase para funciones
def getRulesByClient(clientId):
    BatchId = uuid.uuid4()
```

**Nombrado de clases:**
```python
# ✅ CORRECTO — PascalCase para clases
class TextractAdapter:
class ContextAgentService:
class DocumentRepository:

# ❌ INCORRECTO
class textract_adapter:
class context_agent_service:
```

**Nombrado de constantes:**
```python
# ✅ CORRECTO — SCREAMING_SNAKE_CASE
OCR_CONFIDENCE_THRESHOLD = 95.0
MAX_RETRY_ATTEMPTS = 3
GEMINI_MODEL_DEFAULT = "gemini-1.5-pro"
```

**Nombrado de archivos:**
```
# ✅ CORRECTO — snake_case para módulos Python
context_agent.py
textract_adapter.py
batch_service.py

# ❌ INCORRECTO
ContextAgent.py
TextractAdapter.py
BatchService.py
```

### 3.2 Estándares de Endpoints API REST

**Ruta base obligatoria:** `/api/v1/`

| Recurso | GET (listar) | GET (uno) | POST | PUT | DELETE |
|---|---|---|---|---|---|
| Reglas | `/api/v1/rules` | `/api/v1/rules/{id}` | `/api/v1/rules` | `/api/v1/rules/{id}` | N/A (soft delete) |
| Lotes | `/api/v1/batches` | `/api/v1/batches/{id}` | `/api/v1/batches` | N/A | N/A |
| Documentos | `/api/v1/documents` | `/api/v1/documents/{id}` | N/A | N/A | N/A |
| Pendientes | `/api/v1/pendientes` | `/api/v1/pendientes/{id}` | N/A | `/api/v1/pendientes/{id}` | N/A |

**Reglas de nombrado de endpoints:**
```
✅ CORRECTO — plural, kebab-case, sustantivos
  GET  /api/v1/reglas-trabajo
  POST /api/v1/lotes-procesamiento
  PUT  /api/v1/documentos-pendientes/{id}/correccion

❌ INCORRECTO — verbos, camelCase, singular
  GET  /api/v1/obtenerRegla
  POST /api/v1/crearLote
  PUT  /api/v1/documento/{id}/hacerCorreccion
```

**Estructura de respuesta de la API (obligatoria):**
```python
# TODAS las respuestas de la API deben usar este wrapper
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[str] = None

# ✅ Respuesta exitosa
return APIResponse(success=True, data=rule_schema, message="Regla creada exitosamente")

# ✅ Respuesta de error
return APIResponse(success=False, error="La regla no existe", message="Recurso no encontrado")
```

**Códigos HTTP obligatorios:**
| Situación | Código HTTP |
|---|---|
| Creación exitosa | 201 Created |
| Operación exitosa | 200 OK |
| Recurso no encontrado | 404 Not Found |
| Error de validación | 422 Unprocessable Entity |
| No autorizado (sin token) | 401 Unauthorized |
| Sin permisos (token inválido para la ruta) | 403 Forbidden |
| Error interno del servidor | 500 Internal Server Error |

### 3.3 Estándares de Manejo de Excepciones

```python
# ✅ OBLIGATORIO — Usar excepciones de dominio propias
class GRMException(Exception):
    """Excepción base del proyecto GRM"""
    pass

class RuleNotFoundException(GRMException):
    pass

class OCRConfidenceBelowThresholdException(GRMException):
    pass

class GeminiAPIException(GRMException):
    pass

# ✅ OBLIGATORIO — Exception Handler global en FastAPI
@app.exception_handler(GRMException)
async def grm_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=APIResponse(success=False, error=str(exc)).model_dump()
    )

# ❌ INCORRECTO — Capturar Exception genérica sin relanzar
try:
    result = await gemini_client.generate(prompt)
except Exception as e:
    pass  # Nunca silenciar excepciones
```

### 3.4 Estándares de Seguridad del Backend

```python
# ✅ OBLIGATORIO — Cargar configuración desde variables de entorno
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str
    secret_key: str
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()

# ❌ INCORRECTO — Credenciales hardcodeadas (VIOLACIÓN CRÍTICA DE SEGURIDAD)
GEMINI_API_KEY = "AIzaSy_TU_CLAVE_AQUI"  # NUNCA ESTO
AWS_SECRET = "wJalrXUtn..."              # NUNCA ESTO
```

**Validación de autorización en cada endpoint:**
```python
# ✅ OBLIGATORIO — Decorator de rol en cada endpoint protegido
from app.core.dependencies import require_role, get_current_user

@router.get("/rules")
async def list_rules(
    client_id: int,
    current_user: User = Depends(require_role(["admin", "operario"]))
):
    # El usuario ya está autenticado y tiene el rol correcto
    pass

# ✅ OBLIGATORIO — Validar que el documento pertenece al cliente en cada consulta
@router.get("/client/documents/{doc_id}")
async def get_document(
    doc_id: int,
    current_user: User = Depends(require_role(["cliente"]))
):
    document = await doc_repo.get_by_id(doc_id)
    if document.cliente_id != current_user.cliente_id:
        raise HTTPException(status_code=403, detail="Acceso denegado")
```

### 3.5 Estándares de Logging (HU-09)

```python
# ✅ OBLIGATORIO — Usar el logger del proyecto en cada servicio
import logging
logger = logging.getLogger("grm.{module_name}")

# ✅ OBLIGATORIO — Niveles de log correctos
logger.debug("Construyendo prompt para Gemini: {doc_id}")
logger.info("OCR completado: doc_id={doc_id}, confianza={confidence}%")
logger.warning("Confianza OCR baja: {confidence}% < {threshold}%")
logger.error("Error API Textract: {error_code} - {error_message}")
logger.critical("Credenciales AWS no configuradas — sistema no operativo")

# ❌ INCORRECTO — print() para debugging
print("Procesando documento", doc_id)  # NUNCA en producción
```

---

## 4. Reglas de Alineación — Agente Frontend

### 4.1 Estructura de directorios obligatoria del Frontend

```
C:\zData\ExtracionDatosIA\FrontEnd\src\
├── components\
│   ├── common\          ← Componentes reutilizables (Button, Modal, Table)
│   ├── auth\            ← Login, AuthGuard
│   ├── rules\           ← Formulario de Reglas (HU-01)
│   ├── intake\          ← Ingesta de documentos (HU-02)
│   ├── pending\         ← Lista y visor de pendientes (HU-06)
│   ├── portal\          ← Portal del cliente (HU-07)
│   ├── admin\           ← Panel administrativo (HU-09)
│   └── pdf-viewer\      ← Componente visor PDF reutilizable
├── pages\
│   ├── LoginPage.tsx
│   ├── AdminDashboard.tsx
│   ├── OperadorDashboard.tsx
│   ├── ClientePortal.tsx
│   └── NotFoundPage.tsx
├── styles\              ← [CAPA DE DISEÑO] SASS/SCSS — Design System GRM
│   ├── abstracts\       ← Variables, mixins, funciones (Design Tokens)
│   │   ├── _variables.scss  ← Todos los tokens de diseño (colores, espaciado, etc.)
│   │   ├── _mixins.scss     ← Mixins reutilizables (respond-to, flex-center...)
│   │   └── _functions.scss  ← Funciones SCSS puras
│   ├── base\            ← Reset CSS, tipografía, utilidades globales
│   ├── components\      ← Un .scss por cada componente React
│   ├── layouts\         ← Grids y estructuras de página (sidebar, header)
│   ├── pages\           ← Estilos específicos por página
│   ├── themes\          ← Temas light/dark
│   └── main.scss        ← Punto de entrada — solo importaciones
├── hooks\               ← Custom hooks (useAuth, useBatch, usePendientes)
├── services\            ← Capa de API (axios instances + endpoints)
│   ├── api.ts           ← Instancia axios configurada
│   ├── authService.ts
│   ├── rulesService.ts
│   └── documentService.ts
├── store\               ← Estado global (Zustand)
│   ├── authStore.ts
│   └── batchStore.ts
├── types\               ← TypeScript interfaces (espejo de los schemas Pydantic)
│   ├── auth.ts
│   ├── rules.ts
│   ├── batch.ts
│   └── documents.ts
└── utils\               ← Funciones de utilidad puras
```

### 4.2 Estándares de Código TypeScript/React

**Nombrado de componentes:**
```tsx
// ✅ CORRECTO — PascalCase para componentes React
export const DocumentViewer: React.FC<DocumentViewerProps> = ({ documentId }) => {}
export const RuleFormModal: React.FC<RuleFormModalProps> = () => {}

// ❌ INCORRECTO
export const documentViewer = () => {}
export const rule_form_modal = () => {}
```

**Nombrado de archivos:**
```
✅ CORRECTO — PascalCase para componentes
  DocumentViewer.tsx
  RuleFormModal.tsx
  PendingDocumentList.tsx

✅ CORRECTO — camelCase para hooks, servicios y utilidades
  useDocumentViewer.ts
  rulesService.ts
  formatDate.ts

❌ INCORRECTO
  document-viewer.tsx
  RulesService.ts
  FormatDate.ts
```

**TypeScript — Tipado obligatorio:**
```tsx
// ✅ OBLIGATORIO — Tipar TODOS los props de componentes
interface DocumentViewerProps {
  documentId: number;
  mode: 'readonly' | 'editable';
  onClose: () => void;
}

// ✅ OBLIGATORIO — Tipar respuestas de API (espejo de schemas Pydantic)
interface APIResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

// ❌ INCORRECTO — any type
const handleResponse = (data: any) => {}  // NUNCA usar any
```

**Gestión de estado:**
```tsx
// ✅ CORRECTO — Zustand para estado global del pipeline
import { create } from 'zustand'

interface BatchStore {
  activeBatchId: string | null;
  batchStatus: 'idle' | 'processing' | 'completed' | 'error';
  setActiveBatch: (batchId: string) => void;
}

export const useBatchStore = create<BatchStore>((set) => ({
  activeBatchId: null,
  batchStatus: 'idle',
  setActiveBatch: (batchId) => set({ activeBatchId: batchId }),
}))

// ✅ CORRECTO — React Query para estado del servidor
import { useQuery } from '@tanstack/react-query'

const { data: rules, isLoading } = useQuery({
  queryKey: ['rules', clientId],
  queryFn: () => rulesService.getByClient(clientId),
})
```

### 4.3 Estándares de Llamadas a la API

```tsx
// ✅ OBLIGATORIO — Instancia axios centralizada con interceptors
// src/services/api.ts
import axios from 'axios'
import { useAuthStore } from '@/store/authStore'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
})

// Interceptor: agregar JWT automáticamente
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Interceptor: manejar 401 globalmente
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

### 4.4 Estándares de Seguridad del Frontend

```tsx
// ✅ OBLIGATORIO — Protección de rutas por rol
// src/components/auth/AuthGuard.tsx
interface AuthGuardProps {
  allowedRoles: ('admin' | 'operario' | 'cliente')[];
  children: React.ReactNode;
}

export const AuthGuard: React.FC<AuthGuardProps> = ({ allowedRoles, children }) => {
  const { user, isAuthenticated } = useAuthStore()
  
  if (!isAuthenticated) return <Navigate to="/login" replace />
  if (!allowedRoles.includes(user.rol)) return <Navigate to="/unauthorized" replace />
  
  return <>{children}</>
}

// ✅ OBLIGATORIO — Uso en rutas
<Route path="/admin" element={
  <AuthGuard allowedRoles={['admin']}>
    <AdminDashboard />
  </AuthGuard>
} />

// ❌ INCORRECTO — Rutas sin protección
<Route path="/admin" element={<AdminDashboard />} />
```

### 4.5 Estándares para el Visor de Documentos (HU-06, HU-07)

```tsx
// ✅ OBLIGATORIO — Componente visor reutilizable
// src/components/pdf-viewer/PDFViewer.tsx
import { Document, Page, pdfjs } from 'react-pdf'

// Configuración del worker de PDF.js
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`

interface PDFViewerProps {
  documentId: number;
  mode: 'readonly' | 'editable';  // 'editable' para Operario, 'readonly' para Cliente
}
```

### 4.6 Estándares para WebSockets (HU-06 CA-12)

```tsx
// ✅ OBLIGATORIO — Hook de WebSocket para actualizaciones en tiempo real
// src/hooks/usePendientesSocket.ts
export const usePendientesSocket = (clienteId: number) => {
  const wsUrl = `${import.meta.env.VITE_WS_BASE_URL}/pendientes/${clienteId}`
  
  useEffect(() => {
    const ws = new WebSocket(wsUrl)
    ws.onmessage = (event) => {
      const newPendiente = JSON.parse(event.data)
      // Actualizar lista de pendientes con toast de notificación
    }
    return () => ws.close()
  }, [clienteId])
}
```

### 4.7 Estándares SCSS / Design System GRM

> La capa de diseño visual del proyecto GRM se implementa con **SASS (SCSS)**.
> El Agente Frontend es el único responsable de los archivos dentro de `src/styles/`.
> **El Agente Backend no tiene responsabilidad ni acceso a esta capa.**

**Tecnología oficial:**
```
Compilador: Dart Sass 1.x (paquete npm 'sass')
Preprocesador: SCSS (superset de CSS — sintaxis con llaves)
Integración: Vite css.preprocessorOptions (compilación automática)
NO permitido: Tailwind CSS, styled-components, emotion, CSS-in-JS
```

**Nombrado de archivos SCSS:**
```scss
// ✅ CORRECTO — prefijo guion bajo para parciales (no generan archivo CSS propio)
_variables.scss
_button.scss
_login.scss

// ✅ CORRECTO — sin guion bajo para el punto de entrada
main.scss

// ❌ INCORRECTO
Variables.scss
button.css       // Nunca CSS puro en la carpeta de componentes
styles.scss      // Nombre genérico no permitido
```

**Reglas de uso de variables SCSS:**
```scss
// ✅ OBLIGATORIO — Usar Design Tokens del sistema para todo valor de diseño
.grm-button--primary {
  background-color: $color-primary;      // ✅ Token definido en _variables.scss
  color: $color-gray-50;                 // ✅
  padding: $spacing-3 $spacing-6;        // ✅
  border-radius: $border-radius-base;    // ✅
  transition: $transition-base;          // ✅
  font-family: $font-family-base;        // ✅

  &:hover {
    background-color: $color-primary-dark; // ✅ Variante del token
  }

  &:focus {
    @include focus-ring; // ✅ Mixin definido en _mixins.scss
  }
}

// ❌ INCORRECTO — Valores hardcoded (VIOLACIÓN del Design System)
.grm-button--primary {
  background-color: #1A56DB;   // ❌ Nunca color literal
  padding: 12px 24px;          // ❌ Nunca valor literal de espaciado
  border-radius: 6px;          // ❌ Nunca valor literal de radio
}
```

**Convención de nombres de clases CSS (BEM simplificado):**
```scss
// ✅ CORRECTO — Prefijo grm- + bloque__elemento--modificador
.grm-card { }                        // Bloque
.grm-card__title { }                 // Elemento
.grm-card__title--highlighted { }    // Modificador
.grm-badge--classified { }           // Bloque con modificador de estado
.grm-pipeline-status--error { }      // Estado del pipeline

// ❌ INCORRECTO
.card { }                // Sin prefijo grm- (colisión con librerías)
.CardTitle { }           // PascalCase en clases CSS
.card-title-hl { }       // Abreviaciones cripíticas
```

**SCSS por componente React (co-localización obligatoria):**
```scss
// ✅ CORRECTO — Cada componente tiene su archivo SCSS en styles/components/
// styles/components/_document-viewer.scss
.grm-document-viewer {
  @include card-base;           // Mixin del sistema
  height: 100vh;
  overflow: hidden;

  &__toolbar {
    @include flex-between;
    padding: $spacing-4;
    border-bottom: 1px solid $border-color;
    background-color: $color-gray-50;
  }

  &__canvas {
    flex: 1;
    overflow-y: auto;
  }

  &__page {
    margin: $spacing-4 auto;
    box-shadow: $shadow-md;

    @include respond-to('lg') {
      max-width: 900px;
    }
  }
}

// ❌ INCORRECTO — Estilos inline en el componente React
const style = { backgroundColor: '#1A56DB', padding: '16px' } // NUNCA
<div style={{ color: 'red' }}>...</div>                        // NUNCA
```

**Estados de color del pipeline (variables semánticas):**
```scss
// ✅ OBLIGATORIO — Badge de estado del pipeline con mixin
.grm-status-badge {
  &--pendiente-ingesta    { @include status-badge(#FEF3C7, #92400E); }
  &--procesando-ocr       { @include status-badge(#DBEAFE, #1E40AF); }
  &--agente-contexto      { @include status-badge(#EDE9FE, #5B21B6); }
  &--clasificado          { @include status-badge(#D1FAE5, #065F46); }
  &--pendiente-revision   { @include status-badge(#FEE2E2, #991B1B); }
  &--error                { @include status-badge(#FEE2E2, #7F1D1D); }
}
// Los valores de color deben estar definidos como variables en _variables.scss
// Esta sección usa valores literales solo como ejemplo — en el código real usar tokens
```

**Restricciones absolutas del Agente Frontend en la capa de estilos:**
```
❌ NUNCA instalar ni usar Tailwind CSS, UnoCSS o similar
❌ NUNCA instalar styled-components, emotion, @stitches o CSS-in-JS
❌ NUNCA usar style={} inline en componentes React (excepto valores dinámicos de JS)
❌ NUNCA usar !important (excepto como excepción documentada y aprobada)
❌ NUNCA hardcodear colores, tamaños o espaciados — usar siempre variables SCSS
❌ NUNCA crear archivos .css puros en la carpeta src/styles (solo .scss)
❌ NUNCA modificar el archivo main.scss para escribir estilos — solo importaciones
❌ NUNCA usar @import en SCSS (obsoleto) — usar siempre @use o @forward
```

---

## 5. Reglas de Alineación — Agente Base de Datos

### 5.1 Estándares de nomenclatura SQL Server

**Tablas:**
```sql
-- ✅ CORRECTO — snake_case, plural, español del dominio
reglas_trabajo
lotes_procesamiento
documentos_clasificados
log_ia_invocaciones

-- ❌ INCORRECTO
ReglasDeTrabajo
tbl_reglas
Batch_Processing
```

**Columnas:**
```sql
-- ✅ CORRECTO — snake_case
cliente_id, nombre_completo, created_at, updated_at
campos_extraidos_json, ruta_destino_final, datos_completos

-- ❌ INCORRECTO
ClienteId, NombreCompleto, CreatedAt
camposExtraidos, rutaDestinoFinal
```

**Índices:**
```sql
-- ✅ CORRECTO — prefijo IX_ + tabla + columna(s)
CREATE INDEX IX_documentos_clasificados_cliente_id ON documentos_clasificados(cliente_id)
CREATE INDEX IX_log_proceso_documento_etapa ON log_proceso(documento_id, etapa)
CREATE UNIQUE INDEX UX_usuarios_cedula ON usuarios(cedula)

-- ❌ INCORRECTO
CREATE INDEX idx1 ON documentos_clasificados(cliente_id)
```

**Foreign Keys:**
```sql
-- ✅ CORRECTO — prefijo FK_ + tabla_hija + tabla_padre
CONSTRAINT FK_reglas_trabajo_clientes FOREIGN KEY (cliente_id) REFERENCES clientes(id)
CONSTRAINT FK_documentos_lote_lotes FOREIGN KEY (lote_id) REFERENCES lotes_procesamiento(id)
```

**Stored Procedures y Views (si aplican):**
```sql
-- ✅ CORRECTO — prefijo sp_ para procedures, vw_ para views
CREATE PROCEDURE sp_GetDocumentosByCliente
CREATE VIEW vw_DocumentosPendientesActivos
```

### 5.2 Reglas de Diseño de Schema

**Columnas de auditoría obligatorias en TODAS las tablas:**
```sql
-- ✅ OBLIGATORIO en todas las tablas del dominio
created_at   DATETIME DEFAULT GETDATE() NOT NULL,
updated_at   DATETIME NULL,
created_by   INT NULL REFERENCES usuarios(id)

-- ✅ OBLIGATORIO para entidades con soft delete
activo       BIT DEFAULT 1 NOT NULL
```

**Almacenamiento de JSON:**
```sql
-- ✅ CORRECTO — NVARCHAR(MAX) para JSON con documentación de estructura
campos_extraidos_json NVARCHAR(MAX) NULL,
-- Estructura esperada: [{"nombre": "CC", "valor": "...", "confianza_ocr": 98.5}]

-- ❌ INCORRECTO — TEXT (obsoleto en SQL Server moderno)
campos_extraidos TEXT NULL
```

**Identificadores únicos para trazabilidad:**
```sql
-- ✅ OBLIGATORIO para lotes — usar UNIQUEIDENTIFIER
batch_id UNIQUEIDENTIFIER DEFAULT NEWID() NOT NULL

-- ✅ OBLIGATORIO para PKs — usar IDENTITY
id INT IDENTITY(1,1) PRIMARY KEY
```

### 5.3 Reglas de Migración con Alembic

```python
# ✅ OBLIGATORIO — Cada migración debe ser idempotente y reversible
"""
Versión: V2
Descripción: Agregar columna modelo_ia a agente_contexto_resultados
Autor: [nombre del desarrollador]
Fecha: YYYY-MM-DD
"""

def upgrade():
    op.add_column('agente_contexto_resultados',
        sa.Column('modelo_ia_version', sa.String(100), nullable=True))

def downgrade():
    op.drop_column('agente_contexto_resultados', 'modelo_ia_version')

# ❌ INCORRECTO — Migración sin downgrade
def downgrade():
    pass  # NUNCA vacío
```

### 5.4 Reglas de Repositorios (Patrón Repository)

```python
# ✅ OBLIGATORIO — Un repositorio por entidad de dominio
class RuleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_client(self, client_id: int) -> list[ReglasTrabajo]:
        return self.db.query(ReglasTrabajo)\
            .filter(ReglasTrabajo.cliente_id == client_id,
                    ReglasTrabajo.activa == True)\
            .order_by(ReglasTrabajo.created_at.desc())\
            .all()

    def create(self, rule_data: dict) -> ReglasTrabajo:
        db_rule = ReglasTrabajo(**rule_data)
        self.db.add(db_rule)
        self.db.commit()
        self.db.refresh(db_rule)
        return db_rule

# ❌ INCORRECTO — SQL raw en los endpoints
@router.get("/rules")
async def get_rules(db: Session = Depends(get_db)):
    return db.execute("SELECT * FROM reglas_trabajo").fetchall()  # NUNCA SQL raw en endpoints
```

---

## 6. Estándares Transversales

### 6.1 Variables de Entorno

```
✅ REGLA ABSOLUTA: CERO credenciales en código fuente.

Toda configuración sensible va en .env y se carga vía pydantic-settings.
El archivo .env NUNCA se commitea a Git (verificar .gitignore).

Variables obligatorias del proyecto:
  Backend:
    GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TIMEOUT_SECONDS
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
    DATABASE_URL, SECRET_KEY, ALGORITHM
    CELERY_BROKER_URL, STORAGE_BASE_PATH

  Frontend:
    VITE_API_BASE_URL, VITE_WS_BASE_URL, VITE_APP_TITLE
```

### 6.2 Manejo de Errores Transversal

| Capa | Estrategia |
|---|---|
| Frontend | React Error Boundaries + Toast notifications (react-hot-toast) |
| API Gateway | FastAPI Exception Handlers globales → APIResponse unificado |
| Servicios | Excepciones de dominio tipadas (GRMException hierarchy) |
| Workers Celery | Retry con backoff exponencial (max 3 intentos) + Dead Letter Queue |
| SDKs externos | Try/except + registro en log_ia_invocaciones + alerta al pipeline |

### 6.3 Comentarios y Documentación del Código

```python
# ✅ OBLIGATORIO — Docstrings en todos los servicios y funciones de negocio
class ContextAgent:
    """
    Agente de Contexto IA (HU-04).
    
    Responsabilidad: Interpretar datos OCR crudos de AWS Textract usando 
    Google Gemini para producir un Paquete de Datos Limpios estructurado.
    
    Entradas:
        - ocr_data: Datos consolidados de AWS Textract (por página)
        - work_rule: Regla de trabajo activa del cliente
    
    Salidas:
        - CleanDataPackage: JSON validado con campos extraídos y normalizados
    
    En caso de fallo: Envía el documento a cola de revisión humana (HU-06).
    """
    pass

# ✅ OBLIGATORIO — Comentarios en lógica de negocio compleja
# Umbral fijo definido en HU-01 CA-08: el sistema descarta campos con
# confianza OCR inferior al 95%. No modificable por el rol Operario.
OCR_CONFIDENCE_THRESHOLD = 95.0
```

### 6.4 Pruebas Automatizadas

| Tipo de test | Herramienta | Cobertura mínima requerida |
|---|---|---|
| Backend unitario | pytest + pytest-asyncio | 80% por servicio de dominio |
| Backend integración | pytest + TestClient | Todos los endpoints críticos (auth, rules, batches) |
| Frontend unitario | Vitest + React Testing Library | Componentes críticos (AuthGuard, DocumentViewer) |
| E2E (futuro) | Playwright | Flujos principales del pipeline |

```python
# ✅ EJEMPLO DE TEST OBLIGATORIO — Verificación de umbral de confianza OCR
# tests/test_context_agent.py
import pytest
from app.services.ai_agents.context_agent import ContextAgent

def test_document_marked_for_review_when_confidence_below_threshold():
    """HU-04 CA-04: Documentos con campos bajo confianza van a revisión humana."""
    agent = ContextAgent()
    result = agent.validate_confidence({
        "campo": "CC",
        "valor": "123456",
        "confianza_ocr": 94.9  # Justo por debajo del threshold
    })
    assert result.datos_completos == False
    assert "baja_confianza" in result.motivo_rechazo
```

---

## 7. Arquitectura de Integración de SDKs (Google + AWS)

### 7.1 Patrón Adapter para SDKs externos

Los SDKs externos (Google Gemini y AWS Textract) se envuelven en **Adapters** para garantizar el principio de inversión de dependencias (D de SOLID) y facilitar la migración Cloud.

```python
# ✅ PATRÓN OBLIGATORIO — Definir una interfaz (Port) primero
# app/domain/ports/ocr_port.py
from abc import ABC, abstractmethod
from app.domain.models.ocr_result import OCRResult

class OCRPort(ABC):
    """Interface abstracta para el servicio de OCR.
    Permite reemplazar AWS Textract por cualquier otro servicio sin cambiar el dominio."""
    
    @abstractmethod
    async def process_page(self, page_bytes: bytes, doc_type: str) -> OCRResult:
        pass

# ✅ PATRÓN OBLIGATORIO — Implementar el Adapter concreto
# app/services/ocr/textract_adapter.py
import boto3
from app.domain.ports.ocr_port import OCRPort
from app.core.config import settings

class TextractAdapter(OCRPort):
    """Adapter concreto para AWS Textract.
    Para migrar a Google Document AI: crear un nuevo Adapter sin tocar el dominio."""
    
    def __init__(self):
        self._client = boto3.client(
            'textract',
            region_name=settings.aws_default_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

    async def process_page(self, page_bytes: bytes, doc_type: str) -> OCRResult:
        # Implementación concreta de la llamada a Textract
        response = self._client.detect_document_text(
            Document={'Bytes': page_bytes}
        )
        return self._parse_textract_response(response)
```

### 7.2 Configuración del Agente de Contexto (Google Gemini)

```python
# app/services/ai_agents/context_agent.py
import google.generativeai as genai
from app.core.config import settings
from app.domain.models.clean_data_package import CleanDataPackage

class ContextAgent:
    """HU-04 — Agente de Contexto IA con Google Gemini."""
    
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self._model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",  # Forzar salida JSON
                temperature=0.1,  # Baja temperatura para respuestas deterministas
            )
        )

    def _build_extraction_prompt(self, ocr_data: dict, work_rule: dict) -> str:
        """
        Construye el prompt estructurado para Gemini.
        REGLA: El prompt NUNCA debe incluir datos de otros clientes (HU-04 CA-10).
        """
        campos = "\n".join([
            f"- {c['nombre']} ({c['tipo']}) {'[OBLIGATORIO]' if c['obligatorio'] else '[OPCIONAL]'}"
            for c in work_rule['campos_extraer']
        ])
        
        return f"""
        Eres un experto en extracción de datos de documentos. 
        Analiza el siguiente texto OCR y extrae EXACTAMENTE los campos solicitados.
        
        TIPO DE DOCUMENTO ESPERADO: {work_rule['tipo_documento']}
        
        CAMPOS A EXTRAER:
        {campos}
        
        TEXTO OCR DEL DOCUMENTO:
        {ocr_data['texto_completo']}
        
        INSTRUCCIONES:
        - Retorna ÚNICAMENTE un JSON válido con la estructura solicitada.
        - Si un campo no se encuentra, usa null como valor.
        - Para campos tipo Identificación: retorna solo dígitos, sin puntos ni espacios.
        - Para campos tipo Fecha: retorna en formato YYYY-MM-DD.
        
        FORMATO DE RESPUESTA REQUERIDO:
        {{
            "tipo_documento_detectado": "...",
            "campos_extraidos": [
                {{"nombre": "...", "valor": "...", "confianza_ia": 0.95}}
            ],
            "datos_completos": true/false,
            "motivo_rechazo": null
        }}
        """
```

### 7.3 Flujo de Reintentos para SDKs externos

```python
# ✅ OBLIGATORIO — Implementar backoff exponencial para llamadas externas
import asyncio
from app.core.config import settings

async def call_with_retry(coro_func, max_retries: int = 3, base_delay: float = 1.0):
    """
    Ejecuta una corutina con reintentos y backoff exponencial.
    Documenta cada intento en log_ia_invocaciones (HU-09 CA-03/CA-04).
    """
    last_exception = None
    for attempt in range(1, max_retries + 1):
        try:
            return await coro_func()
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                wait_time = base_delay * (2 ** (attempt - 1))  # 1s, 2s, 4s
                logger.warning(f"Intento {attempt}/{max_retries} fallido. Reintentando en {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                logger.error(f"Todos los reintentos agotados: {str(e)}")
    raise last_exception
```

---

## 8. Pipeline de Procesamiento Documental

### 8.1 Diagrama de flujo del pipeline

```
DOCUMENTO INGRESADO (HU-02)
         │
         ▼
┌────────────────────┐
│  Segmentación PDF  │  Celery Task: split_pdf_task
│  (página por pág.) │  → Archivos en /temp/{batch_id}/
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  OCR AWS Textract  │  Celery Task: ocr_page_task
│  (síncrono/pág.)   │  → Guarda en ocr_resultados_paginas
└─────────┬──────────┘
          │
    ¿Todas las págs.?
    NO → Siguiente página
    SÍ ↓
          │
          ▼
┌────────────────────┐
│ Agente Contexto IA │  Celery Task: context_agent_task
│ (Google Gemini)    │  → Paquete de Datos Limpios
└─────────┬──────────┘
          │
   ¿datos_completos?
   NO → Cola Revisión Humana (HU-06)
   SÍ ↓
          │
          ▼
┌────────────────────┐
│ Agente Clasif. IA  │  Celery Task: classification_agent_task
│ (Google Gemini)    │  → Organiza carpetas + inserta en BD
└─────────┬──────────┘
          │
          ▼
   DOCUMENTO CLASIFICADO
   → Disponible en Portal Cliente (HU-07)
```

### 8.2 Gestión de estados del documento

```python
# Estados válidos del pipeline — usar SIEMPRE estas constantes
class DocumentStatus:
    PENDING_INTAKE    = "pendiente_ingesta"
    SPLITTING_PDF     = "segmentando_pdf"
    OCR_PROCESSING    = "procesando_ocr"
    OCR_COMPLETED     = "ocr_completado"
    CONTEXT_AGENT     = "agente_contexto"
    PENDING_REVIEW    = "pendiente_revision_humana"
    CLASSIFICATION    = "clasificando"
    CLASSIFIED        = "clasificado"
    ERROR             = "error"
    DISCARDED         = "descartado"
```

---

## 9. Estrategia de Migración Local → AWS Cloud

### 9.1 Principio de diseño: "Cloud-Ready desde el día 1"

Cada decisión arquitectónica tomada durante el piloto On-Premise debe permitir la migración a AWS **sin cambiar el código de dominio (Business Logic)**, cambiando únicamente los adaptadores de infraestructura.

### 9.2 Mapa de migración de componentes

| Componente (Piloto) | Componente (Cloud AWS) | Impacto en código |
|---|---|---|
| SQL Server Express local | **Amazon RDS for SQL Server** | CERO — Solo cambiar `DATABASE_URL` en `.env` |
| Redis local (Celery broker) | **Amazon ElastiCache (Redis)** | CERO — Solo cambiar `CELERY_BROKER_URL` en `.env` |
| Sistema de archivos local | **Amazon S3** | BAJO — Reemplazar `LocalStorageAdapter` por `S3StorageAdapter` |
| FastAPI en localhost | **Amazon ECS Fargate** (contenedor Docker) | BAJO — Agregar `Dockerfile` + task definition |
| Frontend Vite localhost | **Amazon S3 + CloudFront** | CERO — `npm run build` → subir `dist/` a S3 |
| Celery Workers locales | **AWS SQS + Lambda** (o ECS Workers) | BAJO — Adaptar el broker de Celery a SQS |
| Google Gemini SDK | Google Gemini SDK (sin cambio) | CERO — Es un servicio externo ya HTTPS |
| AWS Textract SDK | AWS Textract SDK (sin cambio) | CERO — Ya es cloud-native |
| SASS/SCSS + Design System | SASS/SCSS + Design System (sin cambio) | CERO — Se compila a CSS estático en `dist/` |

### 9.3 Preparación durante el piloto

```python
# ✅ OBLIGATORIO DESDE EL PILOTO — Interfaz de storage abstracta
# app/domain/ports/storage_port.py
from abc import ABC, abstractmethod

class StoragePort(ABC):
    """Port para el sistema de almacenamiento.
    Implementación Local: LocalStorageAdapter
    Implementación Cloud: S3StorageAdapter (reemplazar en migración)"""
    
    @abstractmethod
    async def save_document(self, file_bytes: bytes, path: str) -> str:
        """Guarda un archivo y retorna su ruta/URL de acceso."""
        pass

    @abstractmethod
    async def get_document_url(self, path: str) -> str:
        """Retorna la URL de acceso al documento (ruta local o URL S3)."""
        pass

# app/services/storage/local_storage.py (PILOTO)
class LocalStorageAdapter(StoragePort):
    async def save_document(self, file_bytes: bytes, path: str) -> str:
        full_path = Path(settings.storage_base_path) / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(file_bytes)
        return str(full_path)

# app/services/storage/s3_storage.py (CLOUD — crear al migrar)
class S3StorageAdapter(StoragePort):
    async def save_document(self, file_bytes: bytes, path: str) -> str:
        s3_client.put_object(Bucket=settings.s3_bucket, Key=path, Body=file_bytes)
        return f"s3://{settings.s3_bucket}/{path}"
```

### 9.4 Checklist de migración a AWS

```
PRE-MIGRACIÓN (completar durante el piloto):
  ☐ Todos los accesos a filesystem van a través de StoragePort
  ☐ Dockerfile creado para el backend FastAPI
  ☐ Variables de entorno externalizadas en .env (sin hardcoding)
  ☐ Health check endpoint implementado (/health)
  ☐ Logs estructurados en JSON (para CloudWatch)

MIGRACIÓN:
  ☐ Crear VPC + subnets en AWS
  ☐ Crear RDS SQL Server → copiar datos desde local
  ☐ Crear ElastiCache Redis → actualizar CELERY_BROKER_URL
  ☐ Crear S3 Bucket → implementar S3StorageAdapter
  ☐ Crear ECR Repository → push de imagen Docker
  ☐ Crear ECS Cluster + Task Definition + Service
  ☐ Crear CloudFront Distribution + S3 Bucket para Frontend
  ☐ Configurar Application Load Balancer
  ☐ Configurar Route 53 (dominio personalizado)
  ☐ Activar AWS WAF + SSL/TLS (ACM)
```

---

## 10. Cumplimiento ISO/IEC 25010

La norma **ISO/IEC 25010** define el modelo de calidad de software. A continuación se documenta cómo la arquitectura GRM garantiza cada característica de calidad.

### 10.1 Escalabilidad (Subcaracterística de Eficiencia de Desempeño)

| Mecanismo Arquitectónico | Implementación en GRM |
|---|---|
| **Procesamiento asíncrono** | Celery Workers desacoplan la API del pipeline OCR/IA. La API responde en <100ms mientras el procesamiento ocurre en background |
| **Stateless Backend** | FastAPI no mantiene estado de sesión en memoria. El JWT lleva el contexto del usuario. Permite escalar horizontalmente agregando más instancias |
| **Paginación obligatoria** | Todos los listados (documentos, logs, pendientes) usan OFFSET/FETCH NEXT. SLA: <500ms para hasta 10.000 registros (HU-10 CA-04/CA-09) |
| **Índices de BD optimizados** | 8 índices non-clustered en columnas de consulta frecuente (HU-10 CA-06) |
| **Reintentos con backoff** | Evita saturar APIs externas (Textract, Gemini) ante fallas transitorias |
| **Preparación Cloud** | La arquitectura soporta migración a ECS (múltiples contenedores) + ALB sin refactorización |

### 10.2 Mantenibilidad (ISO/IEC 25010 — Maintainability)

| Subcaracterística | Implementación en GRM |
|---|---|
| **Modularidad** | Clean Architecture con 4 capas explícitas. Cada HU tiene su endpoint, servicio, repositorio y schema independientes |
| **Reutilizabilidad** | Adapters (OCR, Storage) son reemplazables sin cambiar el dominio. Componentes React reutilizables (PDFViewer, AuthGuard). Design Tokens SCSS centralizados en `_variables.scss` |
| **Analizabilidad** | Logging estructurado en 4 tablas de log (HU-09). Docstrings obligatorios en servicios. TypeScript elimina ambigüedad en Frontend. Patrón 7-1 en SCSS permite localizar cualquier estilo en segundos |
| **Modificabilidad** | Patrón Repository: cambios en el schema de BD no afectan a los servicios de negocio. Cambiar un token de color en `_variables.scss` se propaga automáticamente a toda la UI |
| **Testeabilidad** | Inyección de dependencias en FastAPI permite mocking de adapters. Cobertura mínima 80% en servicios de dominio |
| **Versionamiento de API** | Ruta base `/api/v1/`. Futuras versiones en `/api/v2/` sin romper clientes existentes |

### 10.3 Seguridad (ISO/IEC 25010 — Security)

| Subcaracterística | Implementación en GRM |
|---|---|
| **Confidencialidad** | JWT con expiración diferenciada por rol (8h/30min). HTTPS obligatorio en Cloud. CERO credenciales en código |
| **Integridad** | Hash SHA-256 + salt único por usuario (HU-08 CA-12). Validación Pydantic en TODAS las entradas de la API |
| **No repudio** | Log completo de todas las acciones (log_auditoria_usuario). Cada intervención humana queda firmada con usuario_id + timestamp |
| **Responsabilidad** | 4 tablas de log con retención mínima 1 año (HU-09 CA-10). Trazabilidad completa del ciclo de vida del documento |
| **Autenticación** | Autenticación por Cédula + Password con bloqueo automático tras 5 intentos (HU-08 CA-04) |
| **Autorización** | RBAC (Role-Based Access Control) con 3 roles. Validación en cada endpoint: el cliente SOLO ve sus propios documentos (HU-07 CA-08) |
| **Aislamiento de contexto IA** | Cada invocación a Gemini es independiente (sin historial compartido entre documentos) — HU-04 CA-10 |

### 10.4 Integrabilidad (ISO/IEC 25010 — Compatibility & Interoperability)

| Subcaracterística | Implementación en GRM |
|---|---|
| **Interoperabilidad** | API REST estándar con OpenAPI 3.0 (Swagger auto-generado por FastAPI). Cualquier cliente HTTP puede integrarse |
| **Coexistencia** | El sistema On-Premise coexiste con servicios cloud externos (Gemini, Textract) sin conflictos. El Storage Adapter permite usar local y S3 simultáneamente durante la migración |
| **Compatibilidad** | SQL Server 2019+ soporta JSON functions requeridas. Python 3.12 soporta todos los SDKs. Node.js 20 LTS tiene soporte oficial hasta 2026 |
| **Portabilidad Cloud** | Patrón Adapter + variables de entorno garantizan que el código fuente es idéntico entre On-Premise y AWS. Solo cambian las variables de configuración |
| **Extensibilidad de agentes** | La arquitectura de agentes (ContextAgent, ClassificationAgent) permite agregar nuevos agentes Gemini sin modificar el pipeline existente |

---

## 11. Matriz de Dependencias entre Agentes

Esta matriz define qué agente es responsable de qué componente y evita colisiones de trabajo.

| Componente del Sistema | Agente Responsable | HU Asociadas |
|---|---|---|
| Autenticación + JWT + Roles | **Agente Backend** | HU-08 |
| Gestión de Reglas de Trabajo | **Agente Backend** + **Agente Frontend** | HU-01 |
| Ingesta de Documentos (lógica) | **Agente Backend** | HU-02 |
| Integración AWS Textract | **Agente Backend** | HU-03 |
| Agente Contexto IA (Gemini) | **Agente Backend** | HU-04 |
| Agente Clasificación IA (Gemini) | **Agente Backend** | HU-05 |
| Lista y visor de pendientes (UI) | **Agente Frontend** | HU-06 |
| Portal cliente web (UI) | **Agente Frontend** | HU-07 |
| Schema y migraciones SQL | **Agente Base de Datos** | HU-10 |
| Tablas de log y auditoría | **Agente Base de Datos** + **Agente Backend** | HU-09 |
| Componente PDFViewer | **Agente Frontend** | HU-06, HU-07 |
| WebSockets (tiempo real) | **Agente Backend** (servidor) + **Agente Frontend** (cliente) | HU-06 CA-12 |
| **Design System / SCSS** | **Agente Frontend** (propietario exclusivo) | Todas las HU con UI |
| **Design Tokens** (`_variables.scss`) | **Agente Frontend** | Todas las HU con UI |

### Protocolo de comunicación entre agentes

```
Cuando el Agente Backend modifica un schema Pydantic:
  → Debe notificar al Agente Frontend para actualizar los types/ correspondientes
  → El Agente Frontend NUNCA debe asumir la estructura de respuesta sin consultar el schema

Cuando el Agente Base de Datos modifica el schema SQL:
  → Debe notificar al Agente Backend para actualizar los SQLAlchemy Models correspondientes
  → La migración Alembic debe ser revisada por el Agente Backend antes de aplicarse

Cuando el Agente Frontend necesita un nuevo endpoint:
  → Debe solicitar al Agente Backend la creación del endpoint
  → NUNCA debe consultar directamente la BD desde el Frontend (no hay acceso directo)
```

---

## 12. Control de Versiones y Branching Strategy

### 12.1 Estructura de branches

```
main          ← Rama de producción (solo código aprobado y verificado)
develop       ← Rama de integración continua
├── feature/HU-01-reglas-trabajo     ← Por Historia de Usuario
├── feature/HU-02-ingesta-documentos
├── feature/HU-03-aws-textract
├── feature/HU-04-agente-contexto
└── hotfix/fix-jwt-expiration        ← Solo para bugs críticos en main
```

### 12.2 Convención de commits (Conventional Commits)

```bash
# ✅ FORMATO OBLIGATORIO
git commit -m "tipo(alcance): descripción breve en español"

# Tipos válidos:
feat:     Nueva funcionalidad (HU implementada)
fix:      Corrección de bug
docs:     Solo documentación
style:    Formato, sin cambios de lógica
refactor: Refactorización sin cambio de comportamiento
test:     Agregar o modificar tests
chore:    Cambios de build, dependencias

# ✅ EJEMPLOS CORRECTOS
git commit -m "feat(HU-01): agregar validación de campos duplicados en reglas"
git commit -m "fix(HU-08): corregir expiración de token para rol cliente"
git commit -m "feat(HU-04): implementar agente contexto con Google Gemini SDK"
git commit -m "docs: actualizar guía de instalación con ODBC driver 18"

# ❌ INCORRECTO
git commit -m "fix"
git commit -m "cambios varios"
git commit -m "WIP"
```

### 12.3 Pull Request — Checklist obligatorio

Antes de hacer merge a `develop`, verificar:

```markdown
## Checklist de PR — GRM

### Código
- [ ] Los tests pasan (pytest / vitest)
- [ ] Cobertura de tests ≥ 80% en el módulo modificado
- [ ] No hay credenciales hardcodeadas
- [ ] No hay console.log() ni print() de debug en el código
- [ ] Los docstrings están actualizados

### Base de Datos
- [ ] Si hay cambios en el schema, existe la migración Alembic correspondiente
- [ ] La migración tiene función downgrade() implementada
- [ ] Los nuevos índices están documentados en HU-10

### Seguridad
- [ ] El .env NO está incluido en el commit
- [ ] Los nuevos endpoints tienen decorador de rol (@require_role)
- [ ] Las respuestas de error no exponen información sensible

### Documentación
- [ ] Los nuevos endpoints están en la colección REST Client (.http)
- [ ] Los cambios de API están reflejados en los types/ del Frontend

### Estilos SCSS
- [ ] Los nuevos componentes tienen su archivo `.scss` en `styles/components/`
- [ ] No hay colores, espaciados ni radios hardcoded (usar tokens de `_variables.scss`)
- [ ] No hay estilos `inline` en los componentes React
- [ ] No se usaron `@import` (solo `@use` o `@forward`)
- [ ] Los nombres de clase siguen la convención `grm-bloque__elemento--modificador`
- [ ] Se verificó la compilación SCSS sin errores: `npx sass src/styles/main.scss --no-source-map`
```

---

*Documento generado por Arquitecto de Software Senior — Proyecto GRM*  
*Versión 1.1.0 — Ley de la Arquitectura*  
*Stack: FastAPI 0.115 + React 18 + SQL Server 2019 + Clean Architecture + ISO/IEC 25010*  
*Estilos: SASS (SCSS) 1.x + CSS puro — Design System GRM*
