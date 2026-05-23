# Handoff — QA — HU-03
## Iteración: 1-DEV-HU-3

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_qa_HU03_CA01-CA12.md`                    |
| **Rol Destino**          | Agente QA                                         |
| **HU de Origen**         | HU-03 — Integración AWS Textract OCR              |
| **CAs Asignados**        | CA-01 al CA-12                                    |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-3                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend Testing: pytest + Moto (Mock para AWS boto3) + Celery pytest plugin
- [x] Frontend Testing: Vitest + React Testing Library (mock de React Query timers)

## Criterios de Aceptación Asignados

(El QA debe crear casos de prueba automatizados para todos los CAs)

### Casos Mínimos Esperados Backend
- **Mock de AWS boto3:** Es **OBLIGATORIO** usar `moto` (o `botocore.stub.Stubber`) para simular las respuestas de AWS Textract. NUNCA realizar llamadas reales a AWS en la suite de tests.
- **CA-01:** Test que verifique que se lanza una excepción si faltan las variables de entorno de AWS.
- **CA-03:** Test de la función parseadora que evalúe y asigne correctamente la etiqueta "Baja confianza" cuando `score < 95%`.
- **CA-04:** Test que simule un `botocore.exceptions.ClientError` y verifique la política de reintentos con backoff.
- **CA-06:** Test que verifique el registro en el log de auditoría de un SLA superado sin que la transacción falle.

### Casos Mínimos Esperados Frontend
- **CA-10:** Test del componente `OcrProgressIndicator` verificando el renderizado correcto de la barra de progreso dado un estado simulado (ej. 50%).

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.**
3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_QA.md`
4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_QA.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."
5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación, pasa a modo `EXECUTION`.
6. **Al terminar la ejecución:** Genera un `walkthrough.md` y avisa al Humano.
