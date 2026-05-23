# Handoff — QA — HU-05 y HU-06
## Iteración: 1-DEV-HU-5/6

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_qa_HU05_HU06.md`                         |
| **Rol Destino**          | Agente QA                                         |
| **HU de Origen**         | HU-05 y HU-06                                     |
| **CAs Asignados**        | Todos los CAs (05 y 06)                           |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-5/6                                      |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend Testing: pytest.
- [x] Frontend Testing: Vitest + React Testing Library.

## Criterios de Aceptación Asignados

### Casos Mínimos Esperados
- **Backend (HU-05)**: Testear lógica de construcción de rutas de archivo y persistencia mockeando a Gemini.
- **Backend (HU-06)**: Testear Endpoints CRUD y lógica de "reprocesamiento" entre las tablas pendientes y clasificadas.
- **Frontend (HU-06)**: Renderizado de la lista de pendientes y la lógica del panel del visor (activar "Corrección directa" vs "Instrucción al Agente" según número de errores).
- **Cobertura:** ≥80% obligatorio.

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
