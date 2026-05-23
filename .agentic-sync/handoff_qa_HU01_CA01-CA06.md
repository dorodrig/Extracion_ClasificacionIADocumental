# Handoff — QA — HU-01
## Iteración: 1-DEV-HU-1

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_qa_HU01_CA01-CA06.md`                    |
| **Rol Destino**          | Agente QA                                         |
| **HU de Origen**         | HU-01 — Configuración y Gestión de Reglas de Trabajo del Cliente |
| **CAs Asignados**        | CA-01, CA-02, CA-03, CA-04, CA-05, CA-06          |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-1                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend Testing: pytest + pytest-asyncio
- [x] Frontend Testing: Vitest + React Testing Library
- [x] E2E Testing: Playwright (opcional, foco en unit/integration por ahora)

### ISO/IEC 25010
- [x] Mantenibilidad: Pruebas unitarias independientes y mockeadas (cobertura ≥80%)
- [x] Fiabilidad: Casos de prueba exhaustivos para validaciones de BD y estado React
- [x] Seguridad: Validar que los endpoints requieran autenticación y rol correcto (Admin/Operario)

## Historia de Usuario — Contexto

> **Como** Operario de Digitalización o Administrador del sistema,
> **Quiero** crear, visualizar, editar y seleccionar Reglas de Trabajo configuradas por cliente,
> **Para que** el sistema de extracción y clasificación sepa exactamente qué campos extraer.

### Descripción Funcional
Validación de calidad de la gestión de Reglas de Trabajo (CRUD básico). Cobertura de backend (endpoints API, lógica de validación duplicada, integridad de schemas JSON) y frontend (validación en cliente, renderizado correcto según mockups, sincronización de estado local).

## Criterios de Aceptación Asignados

(El QA debe crear casos de prueba para cada uno de los siguientes CAs)
- **CA-01** — Primer acceso de cliente sin reglas previas
- **CA-02** — Visualización del listado de reglas de un cliente con reglas existentes
- **CA-03** — Carga de regla existente para edición
- **CA-04** — Creación de una nueva regla adicional
- **CA-05** — Validación de campos obligatorios al guardar
- **CA-06** — Definición dinámica de campos a extraer (Testear restricción de nombres duplicados)

## Especificaciones Técnicas — QA

### Estrategia de Testing
| Tipo de Test     | Herramienta          | Alcance                       |
|------------------|----------------------|-------------------------------|
| Unitario Backend | pytest               | Schemas Pydantic, rule_service, validation |
| Unitario Frontend| Vitest + RTL         | Formularios dinámicos, validación Zod/Yup  |
| Integración API  | pytest + TestClient  | Endpoints `/api/v1/rules`     |

### Casos de Prueba Mínimos Esperados
1. TestBackend: API rechaza creación de regla si campos obligatorios faltan (HTTP 422).
2. TestBackend: API rechaza creación si en `campos_extraer` hay nombres duplicados (HTTP 400).
3. TestFrontend: Botón "Guardar Regla" deshabilitado hasta que campos requeridos se llenen.
4. TestFrontend: Renderizado correcto de lista vacía (CA-01) vs lista con data (CA-02).
5. TestFrontend: Almacenamiento correcto de variables del FieldArray dinámico (CA-06).

### Cobertura Mínima Requerida
- Backend: ≥80% en `app/api/v1/endpoints/rules.py` y `app/services/rule_service.py`
- Frontend: ≥80% en `RuleForm.tsx` y hooks asociados.

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
   - Analiza cada CA asignado y desglosa las tareas técnicas.
   - Identifica riesgos y dependencias.
   - Estima el esfuerzo por tarea.

2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El Humano es solo un cartero. No tiene autoridad técnica para aprobar ni rechazar planes.

3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_QA.md`
   
   El archivo debe contener:
   - Resumen del plan propuesto
   - Archivos que planeas crear/modificar (con rutas absolutas)
   - Decisiones técnicas clave tomadas
   - Preguntas para el Arquitecto (si las hay)
   - Riesgos identificados

4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_QA.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."

5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación explícita del Arquitecto Líder (transmitida por el Humano Cartero), pasa a modo `EXECUTION`.

6. **En modo `EXECUTION`:**
   - Codifica siguiendo estrictamente los estándares de la Gobernanza.
   - Haz `git add`, `git commit` (con Conventional Commits) y `git push` a la rama indicada.
   - Actualiza el `task.md` con el progreso.

7. **Al terminar la ejecución:**
   - Genera un `walkthrough.md` con resumen de cambios.
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama HU1_CA1-CA6_DEVDAVID_ITEREACION1. Avísale al Arquitecto."*
