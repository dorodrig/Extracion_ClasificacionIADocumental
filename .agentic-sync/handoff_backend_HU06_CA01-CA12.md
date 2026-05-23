# Handoff — Backend — HU-06
## Iteración: 1-DEV-HU-6

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_backend_HU06_CA01-CA12.md`               |
| **Rol Destino**          | Agente Backend                                    |
| **HU de Origen**         | HU-06 — Validación Humana                         |
| **CAs Asignados**        | CA-01 al CA-12 (Porción de API / BD)              |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-6                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: FastAPI + SQLAlchemy.
- [x] DB: SQL Server (Tabla `documentos_pendientes`).

### Criterios de Aceptación Asignados al Backend
- **CA-01 & CA-02**: Endpoint `GET /api/v1/pendientes` con paginación y filtros (cliente, motivo, rango de fechas).
- **CA-03 & CA-10**: Endpoint `GET /api/v1/pendientes/{id}/visor` que devuelva documento y JSON de campos con confianzas y motivos de rechazo.
- **CA-05**: Endpoint `PUT /api/v1/pendientes/{id}/correccion` para recibir la corrección del operario.
- **CA-06**: Endpoint `POST /api/v1/pendientes/{id}/instruccion-agente` para recibir instrucciones en texto libre hacia Gemini (HU-05).
- **CA-08**: Endpoint `PUT /api/v1/pendientes/{id}/descartar` (guardando motivo).
- **CA-12**: (Opcional si es difícil vía WebSocket, usar Polling) Endpoint para SSE o WebSocket para actualizaciones en tiempo real a la cola de pendientes. Si es muy complejo por tiempo, un endpoint liviano de polling es aceptable.
- **Base de Datos**: Crear modelo `documentos_pendientes`.

## Especificaciones Técnicas — Backend
- Respeta la estructura Clean Architecture (Router -> Service -> Repository).
- Los endpoints deben estar protegidos por rol de "Operario" (usa la dependencia de HU-08 que ya fue mergeada).

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md` considerando los requisitos de esta HU.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El humano es solo un cartero.
3. **Guarda tu solicitud de revisión** en (si lo haces junto con la HU-05, usa un solo archivo o agrégalo):
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."
5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación, pasa a modo `EXECUTION`.
