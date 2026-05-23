# Handoff — Backend — HU-05
## Iteración: 1-DEV-HU-5

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_backend_HU05_CA01-CA13.md`               |
| **Rol Destino**          | Agente Backend                                    |
| **HU de Origen**         | HU-05 — Agente de Clasificación IA                |
| **CAs Asignados**        | CA-01 al CA-13                                    |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-5                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: FastAPI + Celery (Workers) + SDK Google Gemini + SQLAlchemy.
- [x] DB: SQL Server (Tabla `documentos_clasificados`).

### Criterios de Aceptación Asignados al Backend
- **CA-01**: Recepción de datos limpios de HU-04.
- **CA-02**: Construcción de ruta de destino usando patrón de regla (`/{CC}/{NOMBRE_COMPLETO}/{TIPO_DOCUMENTO}/{NOMBRE_ARCHIVO}`).
- **CA-03**: Invocar a Gemini para desambiguar variables del patrón.
- **CA-04 & CA-05**: Gestión en sistema de archivos (crear carpetas, copiar archivos).
- **CA-06**: Persistencia (UPSERT) en BD (`documentos_clasificados`).
- **CA-07 & CA-08**: Agrupación inteligente y manejo de duplicados de archivo (sufijos).
- **CA-09 & CA-10**: Actualización de estado en lote y generación de resumen.
- **CA-11**: Reprocesamiento mediante instrucción correctiva (viene de HU-06).
- **CA-12**: Manejo de errores de disco (mover a pendientes).
- **CA-13**: Trazabilidad en BD.

## Especificaciones Técnicas — Backend
- **Celery Worker**: Esta lógica debe residir primariamente en un worker asíncrono para no bloquear, o como un servicio interno invocado al finalizar HU-04.
- **Modelo BD**: Crea o actualiza `documentos_clasificados` según las notas técnicas de HU-05.
- **Integración con Gemini**: Utiliza `google-generativeai`. No dejes la API KEY hardcodeada (usa variables de entorno).

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El humano es solo un cartero.
3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."
5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación, pasa a modo `EXECUTION`.
6. **Al terminar la ejecución:** Genera un `walkthrough.md` y avisa al Humano.
