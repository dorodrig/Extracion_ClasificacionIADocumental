# Handoff — QA — HU-01 (Parte 2)
## Iteración: 2-DEV-HU-1

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_qa_HU01_CA07-CA13.md`                    |
| **Rol Destino**          | Agente QA                                         |
| **HU de Origen**         | HU-01 — Configuración y Gestión de Reglas de Trabajo del Cliente |
| **CAs Asignados**        | CA-07, CA-08, CA-09, CA-10, CA-11, CA-12, CA-13   |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 2-DEV-HU-1                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend Testing: pytest + pytest-asyncio
- [x] Frontend Testing: Vitest + React Testing Library

## Criterios de Aceptación Asignados

(El QA debe crear casos de prueba para cada uno de los siguientes CAs)
- **CA-07** — Configuración y validación del patrón de carpeta de salida (Tests Backend y Frontend)
- **CA-08** — Umbral de confianza OCR fijo y visible (Test Frontend - Disabled state)
- **CA-09** — Inicio del proceso de extracción desde una regla (Test Frontend - Navigation/State)
- **CA-10** — Versionamiento automático al actualizar (Test Backend - PUT endpoint)
- **CA-11** — Persistencia de reglas para uso en futuros proyectos ("Duplicar Regla") (Tests Backend y Frontend)
- **CA-12** — Validación de nombre único de regla por cliente (Test Backend HTTP 409, Test Frontend display error)
- **CA-13** — Selección de modo de entrada de documentos en la regla (Test Backend/Frontend)

## Especificaciones Técnicas — QA

### Casos de Prueba Mínimos Esperados
1. TestBackend: `POST /api/v1/rules/{id}/duplicate` crea una copia exacta con nombre modificado y version 1.
2. TestBackend: `PUT /api/v1/rules/{id}` incrementa la versión.
3. TestBackend: `POST /api/v1/rules` retorna 409 si el nombre ya existe para ese cliente.
4. TestFrontend: CA-07 - El campo de patrón muestra warning si se escribe una variable no existente.
5. TestFrontend: CA-08 - El input de umbral OCR tiene propiedad `disabled` y muestra `95%`.

### Cobertura Mínima Requerida
- Mantener la cobertura general de tests unitarios/integración en ≥80%.

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
