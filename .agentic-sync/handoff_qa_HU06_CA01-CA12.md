# Handoff — QA — HU-06
## Iteración: 4 -DEV-HU-6

| Campo                    | Valor                                                        |
|--------------------------|--------------------------------------------------------------|
| **Archivo**              | `handoff_qa_HU06_CA01-CA12.md`                               |
| **Rol Destino**          | Agente QA                                                    |
| **HU de Origen**         | HU-06 — Validación Humana: Pendientes y Visor                |
| **CAs Asignados**        | CA-01 a CA-12                                                |
| **CAs Excluidos**        | Ninguno                                                      |
| **Rama Git**             | `HU2_CA1-CA4_DevDamian_ITEREACION1`                          |
| **Iteración**            | 4 -DEV-HU-6                                                  |
| **Fecha de Generación**  | 2026-05-23                                                   |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)                        |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md                          |

## Alineación Arquitectónica

### Estrategia de Testing
| Tipo de Test     | Herramienta          | Alcance                       |
|------------------|----------------------|-------------------------------|
| Unitario Backend | pytest + pytest-asyncio | Servicios de validación humana |
| Unitario Frontend| Vitest + RTL         | Componentes: Visor, Filtros, Formularios |
| Integración API  | pytest + TestClient  | Endpoints `/api/v1/pendientes/*` |

### Casos de Prueba Críticos (Por CA)
- **CA-01, CA-02 (Backend/Frontend):** Filtros en API y rendering de tabla en Frontend. Casos vacíos.
- **CA-03, CA-10 (Frontend):** Mocking del visor con estados ✓, ✗, ⚠ en base a la respuesta del backend.
- **CA-05 (Integración):** Validar payload enviado y que la base de datos se actualice sin errores, devolviendo el código 200.
- **CA-06 (Integración):** Validar payload de instrucción y que el backend desencadene la tarea de reclasificación o encole.
- **CA-09 (Frontend):** Lógica visual (colores semánticos) calculando la fecha actual vs fecha de entrada (menos 15m, 15-60m, +60m).

### ISO/IEC 25010
- [x] Mantenibilidad: Cobertura Frontend y Backend en módulos creados para HU-06.

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
   - Analiza cada CA asignado y desglosa las tareas técnicas.
   - Identifica riesgos y dependencias.
   - Estima el esfuerzo por tarea.

2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El Humano es solo un cartero. No tiene autoridad técnica para aprobar ni rechazar planes.

3. **Guarda tu solicitud de revisión** en:
   `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_QA.md`
   
   El archivo debe contener:
   - Resumen del plan propuesto
   - Archivos que planeas crear/modificar (con rutas absolutas)
   - Decisiones técnicas clave tomadas
   - Preguntas para el Arquitecto (si las hay)
   - Riesgos identificados

4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_QA.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."

5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación explícita del Arquitecto Líder (transmitida por el Humano Cartero), pasa a modo `EXECUTION`.

6. **En modo `EXECUTION`:**
   - Codifica siguiendo estrictamente los estándares de la Gobernanza.
   - Haz `git add`, `git commit` (con Conventional Commits) y `git push` a la rama indicada.
   - Actualiza el `task.md` con el progreso.

7. **Al terminar la ejecución:**
   - Genera un `walkthrough.md` con resumen de cambios.
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama HU2_CA1-CA4_DevDamian_ITEREACION1. Avísale al Arquitecto."*
