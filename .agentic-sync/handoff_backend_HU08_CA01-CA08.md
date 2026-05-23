# Handoff — Backend — HU-08
## Iteración: 5 -DEV-HU-08

| Campo                    | Valor                                                        |
|--------------------------|--------------------------------------------------------------|
| **Archivo**              | `handoff_backend_HU08_CA01-CA08.md`                          |
| **Rol Destino**          | Agente Backend                                               |
| **HU de Origen**         | HU-08 — Gestión de Roles y Autenticación del Sistema         |
| **CAs Asignados**        | CA-01 a CA-08                                                |
| **CAs Excluidos**        | CA-09 a CA-12 (No solicitados en esta iteración)             |
| **Rama Git**             | `HU2_CA1-CA4_DevDamian_ITEREACION1`                          |
| **Iteración**            | 5 -DEV-HU-08                                                 |
| **Fecha de Generación**  | 2026-05-23                                                   |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)                        |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md                          |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: Python 3.12 + FastAPI 0.115 + SQLAlchemy + Alembic
- [x] Seguridad: JWT, SHA-256 + Salt (No bcrypt, ceñirse a SHA-256+Salt según HU)
- [x] Base de Datos: SQL Server 2019+

### Patrón Arquitectónico
- [x] Clean Architecture: Auth debe ser agnóstico, pero aquí implementaremos los repositorios en Infraestructura y la validación en Use Cases / Services.

### ISO/IEC 25010
- [x] Seguridad: Cero credenciales hardcodeadas, protección estricta por RBAC. JWT de corta vida / inactividad administrada.
- [x] Mantenibilidad: Aislamiento del módulo `auth` en la Clean Architecture.

## Historia de Usuario — Contexto
Controlar el acceso mediante autenticación por Cédula + contraseña (SHA-256) y gestionar tres roles diferenciados (Administrador, Operario, Cliente Final) para que cada usuario acceda únicamente a sus funcionalidades.

## Criterios de Aceptación a Implementar (Backend)
- **CA-02, CA-04:** Endpoint de Login que valide SHA-256+Salt, maneje intentos fallidos (bloqueo 15 min a los 5 fallos) y genere JWT con claims (usuario_id, rol, cliente_id, exp).
- **CA-03:** Endpoint para listar clientes asociados a un operario y actualizar el cliente_id en el token/sesión si es necesario (o el front envía el cliente en las peticiones).
- **CA-05:** Implementar o consolidar la dependencia `require_role` en `app.core.dependencies` para leer el JWT y retornar 403 Forbidden si no coincide.
- **CA-06, CA-07:** Endpoints para que el Administrador liste usuarios y cree nuevos usuarios, validando que la cédula sea única y encriptando con SHA-256+Salt.

## Especificaciones Técnicas — Backend

### Estructura de Directorios
Archivos principales a modificar o crear:
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\core\security.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\core\dependencies.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\api\v1\endpoints\auth.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\api\v1\endpoints\usuarios.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\services\auth_service.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\services\usuarios_service.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\db\models\usuarios.py` (Crear tabla de acuerdo a las Notas Técnicas de la HU)

### Notas SQL Server
De acuerdo a las Notas Técnicas de la HU, debes crear los modelos para:
- `usuarios`
- `clientes`
- `usuarios_clientes`

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El humano es solo un cartero.
3. **Guarda tu solicitud en `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Backend.md`**
4. **Dile al Humano:** "He dejado mi solicitud de revisión en la ruta acordada: C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Backend.md Llévasela al Arquitecto Líder y regrésame su respuesta."
5. Solo tras la aprobación del Arquitecto, pasa a modo `EXECUTION`, codifica y haz git commit / push.
