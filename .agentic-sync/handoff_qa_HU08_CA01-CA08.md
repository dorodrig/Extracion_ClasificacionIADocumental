# Handoff — QA — HU-08
## Iteración: 5 -DEV-HU-08

| Campo                    | Valor                                                        |
|--------------------------|--------------------------------------------------------------|
| **Archivo**              | `handoff_qa_HU08_CA01-CA08.md`                               |
| **Rol Destino**          | Agente QA                                                    |
| **HU de Origen**         | HU-08 — Gestión de Roles y Autenticación del Sistema         |
| **CAs Asignados**        | CA-01 a CA-08                                                |
| **CAs Excluidos**        | CA-09 a CA-12                                                |
| **Rama Git**             | `HU2_CA1-CA4_DevDamian_ITEREACION1`                          |
| **Iteración**            | 5 -DEV-HU-08                                                 |
| **Fecha de Generación**  | 2026-05-23                                                   |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)                        |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md                          |

## Alineación Arquitectónica

### Estrategia de Testing
- Pruebas de integración sobre `/api/v1/auth/login` validando la generación correcta de JWT.
- Pruebas de seguridad intentando acceder a endpoints con un rol no autorizado (validar HTTP 403 Forbidden).
- Mocking del temporizador de inactividad en frontend.

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El humano es solo un cartero.
3. **Guarda tu solicitud en `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_QA.md`**
4. **Dile al Humano:** "He dejado mi solicitud de revisión en la ruta acordada: C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_QA.md Llévasela al Arquitecto Líder y regrésame su respuesta."
5. Solo tras la aprobación del Arquitecto, pasa a modo `EXECUTION`, codifica y haz git commit / push.
