# Handoff — QA — HU-04
## Iteración: 1-DEV-HU-4

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_qa_HU04_CA01-CA12.md`                    |
| **Rol Destino**          | Agente QA                                         |
| **HU de Origen**         | HU-04 — Agente de Contexto IA (Google Gemini)     |
| **CAs Asignados**        | CA-01 al CA-12                                    |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-4                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend Testing: pytest + Moto/Responses para Mockear API HTTP (Google Gemini REST endpoint) o un mock directo del SDK.

## Criterios de Aceptación Asignados

(El QA debe crear casos de prueba automatizados para todos los CAs)

### Casos Mínimos Esperados Backend
- **Mock de Gemini:** NUNCA realizar llamadas reales a la API de Gemini en la suite de pruebas unitarias. Se DEBEN mockear las respuestas.
- **CA-03:** Simular una respuesta malformada de Gemini y verificar el mecanismo de reintento.
- **CA-04/05/06:** Test unitario para la lógica de validación (el validador puro sin dependencias de red): Inyectar un JSON extraído simulado y asegurar que si falta un campo obligatorio, `datos_completos = false` y se asigna motivo de rechazo.
- **CA-11:** Test unitario para las funciones de normalización de cadenas (puntos, fechas ISO).
- **Cobertura:** ≥80% obligatorio en el nuevo módulo o servicio de IA.

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El humano es solo un cartero.
3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_QA.md`
4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_QA.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."
5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación, pasa a modo `EXECUTION`.
6. **Al terminar la ejecución:** Genera un `walkthrough.md` y avisa al Humano.
