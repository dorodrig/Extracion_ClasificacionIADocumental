# Handoff — Backend — HU-09
## Iteración: 6 -DEV-HU-09

| Campo                    | Valor                                                        |
|--------------------------|--------------------------------------------------------------|
| **Archivo**              | `handoff_backend_HU09_CA01-CA05.md`                          |
| **Rol Destino**          | Agente Backend                                               |
| **HU de Origen**         | HU-09 — Trazabilidad, Auditoría y Log de Procesos            |
| **CAs Asignados**        | CA-01 a CA-05                                                |
| **CAs Excluidos**        | CA-06 a CA-10 (No solicitados en esta iteración)             |
| **Rama Git**             | `HU2_CA1-CA4_DevDamian_ITEREACION1`                          |
| **Iteración**            | 6 -DEV-HU-09                                                 |
| **Fecha de Generación**  | 2026-05-23                                                   |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)                        |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md                          |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: Python 3.12 + FastAPI 0.115 + SQLAlchemy + Alembic
- [x] Base de Datos: SQL Server 2019+

### Patrón Arquitectónico
- [x] Clean Architecture: Crear servicios centralizados para Logging (`audit_service.py`) de modo que otros servicios de dominio (Textract, Gemini, Pendientes) los inyecten o invoquen sin acoplar la lógica de escritura a BD a sus procesos nativos.
- [x] APIResponse estándar.

### ISO/IEC 25010
- [x] Mantenibilidad: Desacoplamiento del Logging.
- [x] Eficiencia: Considerar escritura asíncrona de logs si es posible, o al menos no bloquear procesos críticos.

## Criterios de Aceptación a Implementar (Backend)
- **CA-01:** Tablas y métodos para registrar `log_proceso`.
- **CA-02:** Tabla y método para registrar `log_auditoria_usuario` cuando un humano interviene. Actualizar el servicio de *Pendientes* (HU-06) para que llame a este log al realizar correcciones/instrucciones.
- **CA-03, CA-04:** Tabla y métodos para registrar `log_ia_invocaciones` para AWS Textract y Google Gemini.
- **CA-05:** Endpoint `/api/v1/auditoria/documentos/{documento_id}/historial` que devuelva ordenadamente los eventos del proceso de un documento para renderizar la línea de tiempo en el UI.

## Especificaciones Técnicas — Backend

### Estructura de Directorios
Archivos principales a modificar o crear:
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\db\models\auditoria.py` (Nuevas tablas de log)
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\db\repositories\auditoria_repository.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\services\auditoria_service.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\api\v1\endpoints\auditoria.py`
- Modificar `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\services\pendientes_service.py` para disparar el log de CA-02.

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El humano es solo un cartero.
3. **Guarda tu solicitud en `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Backend.md`**
4. **Dile al Humano:** "He dejado mi solicitud de revisión en la ruta acordada: C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Backend.md Llévasela al Arquitecto Líder y regrésame su respuesta."
5. Solo tras la aprobación del Arquitecto, pasa a modo `EXECUTION`, codifica y haz git commit / push.
