# Handoff — QA — HU-07
## Iteración: 1-DEV-HU-7

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_qa_HU07_CA01-CA12.md`                    |
| **Rol Destino**          | Agente QA                                         |
| **HU de Origen**         | HU-07 — Portal Web de Consulta para Cliente Final |
| **CAs Asignados**        | CA-01 al CA-12                                    |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-7                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend Testing: pytest.
- [x] Frontend Testing: Vitest + React Testing Library.

## Criterios de Aceptación Asignados

(El QA debe crear casos de prueba automatizados para todos los CAs)

### Casos Mínimos Esperados
- **Backend (CA-08)**: Test que asegure que si un token de cliente 1 intenta acceder a `/api/cliente/documentos/ID_CLIENTE_2`, devuelva 403.
- **Frontend (CA-02, CA-03, CA-04)**: Renderizado de las vistas (Dashboard, Tabla, Explorador).
- **Frontend (CA-05)**: Test que asegure que los inputs/paneles del visor no son editables (readonly).
- **Cobertura:** ≥80% obligatorio en los componentes Frontend y Endpoints Backend.

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
