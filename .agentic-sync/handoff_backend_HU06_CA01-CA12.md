# Handoff — Backend — HU-06
## Iteración: 4 -DEV-HU-6

| Campo                    | Valor                                                        |
|--------------------------|--------------------------------------------------------------|
| **Archivo**              | `handoff_backend_HU06_CA01-CA12.md`                          |
| **Rol Destino**          | Agente Backend                                               |
| **HU de Origen**         | HU-06 — Validación Humana: Pendientes y Visor                |
| **CAs Asignados**        | CA-01 a CA-12                                                |
| **CAs Excluidos**        | Ninguno                                                      |
| **Rama Git**             | `HU2_CA1-CA4_DevDamian_ITEREACION1`                          |
| **Iteración**            | 4 -DEV-HU-6                                                  |
| **Fecha de Generación**  | 2026-05-23                                                   |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)                        |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md                          |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: Python 3.12 + FastAPI 0.115 + SQLAlchemy + Alembic
- [x] Base de Datos: SQL Server 2019+
- [x] WebSockets: FastAPI WebSockets

### Patrón Arquitectónico
- [x] Clean Architecture (Ports & Adapters)
- [x] Capas: Infraestructura → Aplicación → Dominio

### ISO/IEC 25010
- [x] Mantenibilidad: Separación de endpoints y servicios para operaciones de validación humana.
- [x] Seguridad: JWT requerido y RBAC (solo rol operario y admin).
- [x] Eficiencia: Endpoint GET con soporte para paginación y filtrado nativo.

## Historia de Usuario — Contexto

> **Como** Operario de Digitalización,
> **Quiero** ver una lista de documentos que el pipeline automático no pudo procesar completamente, acceder a un visor que me muestre el documento junto con los datos extraídos y el motivo del rechazo, y poder corregir campos individuales o enviar una instrucción al Agente de Clasificación para que resuelva los errores.

## Criterios de Aceptación

*(Incluyendo especificaciones Gherkin desde CA-01 a CA-12 de HU-06. Ver HU original para detalles completos)*
- **CA-01, CA-02, CA-09:** Endpoint para listar y buscar documentos pendientes con filtros.
- **CA-03, CA-10, CA-11:** Endpoint para obtener el detalle de un documento para el visor.
- **CA-05:** Endpoint PUT para corrección directa.
- **CA-06:** Endpoint POST para enviar instrucción de reprocesamiento.
- **CA-07, CA-12:** Websocket o polling setup para actualizar a la UI del frontend.
- **CA-08:** Endpoint PUT para descartar el documento.

## Especificaciones Técnicas — Backend

### Estructura de Directorios
Archivos a crear/modificar:
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\api\v1\endpoints\pendientes.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\services\pendientes_service.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\schemas\pendientes.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\db\models\documentos_pendientes.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\db\repositories\pendientes_repository.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\api\v1\router.py` (Actualizar router)

### Endpoints API REST
| Método | Ruta                                      | Descripción                                           | Auth |
|--------|-------------------------------------------|-------------------------------------------------------|------|
| GET    | `/api/v1/pendientes`                      | Listar documentos pendientes (con filtros q, cliente) | Operario |
| GET    | `/api/v1/pendientes/{id}/visor`           | Obtener datos completos para el visor                 | Operario |
| PUT    | `/api/v1/pendientes/{id}/correccion`      | Enviar corrección directa de campo                    | Operario |
| POST   | `/api/v1/pendientes/{id}/instruccion`     | Enviar instrucción al Agente de Clasificación         | Operario |
| PUT    | `/api/v1/pendientes/{id}/descarte`        | Descartar documento con motivo                        | Operario |

### Modelo de Datos (SQLAlchemy)
Crear la tabla `documentos_pendientes` de acuerdo a las Notas Técnicas de la HU-06. 

## Estándares de Código — Referencia Gobernanza
- §3.1 Nombrado Python
- §3.2 Endpoints REST y respuestas unificadas `APIResponse`
- §3.3 Excepciones

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
   - Analiza cada CA asignado y desglosa las tareas técnicas.
   - Identifica riesgos y dependencias.
   - Estima el esfuerzo por tarea.

2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El Humano es solo un cartero. No tiene autoridad técnica para aprobar ni rechazar planes.

3. **Guarda tu solicitud de revisión** en:
   `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Backend.md`
   
   El archivo debe contener:
   - Resumen del plan propuesto
   - Archivos que planeas crear/modificar (con rutas absolutas)
   - Decisiones técnicas clave tomadas
   - Preguntas para el Arquitecto (si las hay)
   - Riesgos identificados

4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Backend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."

5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación explícita del Arquitecto Líder (transmitida por el Humano Cartero), pasa a modo `EXECUTION`.

6. **En modo `EXECUTION`:**
   - Codifica siguiendo estrictamente los estándares de la Gobernanza.
   - Haz `git add`, `git commit` (con Conventional Commits) y `git push` a la rama indicada.
   - Actualiza el `task.md` con el progreso.

7. **Al terminar la ejecución:**
   - Genera un `walkthrough.md` con resumen de cambios.
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama HU2_CA1-CA4_DevDamian_ITEREACION1. Avísale al Arquitecto."*
