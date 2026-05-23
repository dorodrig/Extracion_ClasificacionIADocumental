# Handoff — Frontend — HU-03
## Iteración: 1-DEV-HU-3

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_frontend_HU03_CA01-CA12.md`              |
| **Rol Destino**          | Agente Frontend                                   |
| **HU de Origen**         | HU-03 — Integración AWS Textract OCR              |
| **CAs Asignados**        | CA-10                                             |
| **CAs Excluidos**        | CA-01 al CA-09, CA-11, CA-12 (Lógica puramente Backend) |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-3                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Frontend: React 18 + TypeScript + Zustand + React Query (Polling configuration)
- [x] Estilos: SASS/SCSS Modules (Gobernanza §4.7)

## Criterios de Aceptación Asignados al Frontend

### CA-10 — Indicador de progreso de OCR
**Responsabilidad Frontend:**
- Crear un componente `OcrProgressIndicator` que consulte el nuevo endpoint del Backend `GET /api/v1/ocr/progress/{batch_id}`.
- Dado que WebSockets no están implementados todavía, configurar React Query con `refetchInterval: 3000` (polling cada 3s) mientras el estado sea "en proceso".
- Mostrar la información de progreso de forma visual: barra de progreso, conteo de "Páginas procesadas vs total", y "Documentos con error".
- Seguir el diseño oscuro (SCSS) establecido en la Gobernanza.

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.**
3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Frontend.md`
4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Frontend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."
5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación, pasa a modo `EXECUTION`.
6. **Al terminar la ejecución:** Genera un `walkthrough.md` y avisa al Humano.
