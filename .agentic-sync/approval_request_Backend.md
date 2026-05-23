# Solicitud de Aprobación de Arquitectura — Backend
## HU-08 — Gestión de Roles y Autenticación del Sistema

**Para:** Arquitecto Líder
**De:** Agente Backend
**Rama:** `HU2_CA1-CA4_DevDamian_ITEREACION1`

### Resumen del Plan de Implementación (Fase PLANNING Completada)

He completado la fase de planificación para los Criterios de Aceptación CA-01 a CA-08 de la HU-08.

**Propuesta a implementar:**
1. **Modelos:** Se crearán las tablas `usuarios`, `clientes` y `usuarios_clientes` (SQLAlchemy) en `app/db/models/usuarios.py`. Se manejarán los campos `intentos_fallidos` y `bloqueado_hasta` para la restricción de 15 minutos en el modelo de usuario.
2. **Seguridad (Core):** Se implementará la lógica de cifrado (SHA-256 + Salt aleatorio) en `app/core/security.py`. No se usarán otros algoritmos de hashing. Se generarán JWT con los claims especificados (`usuario_id`, `rol`, `cliente_id`, `exp`).
3. **Dependencias:** Se modificará `app/core/dependencies.py` consolidando `require_role` (RBAC) y `get_current_user` para que validen y decodifiquen adecuadamente el token JWT.
4. **Servicios y Endpoints:**
   - **Auth:** Endpoint de `/login` en `app/api/v1/endpoints/auth.py`, lógica de bloqueo en `auth_service.py` (CA-02, CA-04).
   - **Usuarios:** Endpoints para crear/listar usuarios (CA-06, CA-07) y listar clientes asociados (CA-03) en `app/api/v1/endpoints/usuarios.py` y `usuarios_service.py`.

### Solicitud

Solicito formalmente la revisión y **APROBACIÓN** de este plan para proceder con la etapa de **EXECUTION** (codificación de los artefactos mencionados). 

¿El plan descrito está alineado con la arquitectura esperada y puedo proceder con la codificación? Responder con "APROBADO" o las correcciones pertinentes.
