# Handoff — QA — HU-05
## Iteración: 3 -DEV-HU-5

| Campo                    | Valor                                                        |
|--------------------------|--------------------------------------------------------------|
| **Archivo**              | `handoff_qa_HU05_CA01-CA13.md`                               |
| **Rol Destino**          | Agente QA                                                    |
| **HU de Origen**         | HU-05 — Agente de Clasificación IA (Google Gemini)           |
| **CAs Asignados**        | CA-01 a CA-13                                                |
| **CAs Excluidos**        | Ninguno                                                      |
| **Rama Git**             | `HU2_CA1-CA4_DevDamian_ITEREACION1`                          |
| **Iteración**            | 3 -DEV-HU-5                                                  |
| **Fecha de Generación**  | 2026-05-23                                                   |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)                        |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md                          |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: Python 3.12 + pytest + pytest-asyncio
- [x] Mocks: unittest.mock o pytest-mock
- [x] Fixtures: pytest fixtures para inyección de DB y Mocks

### ISO/IEC 25010
- [x] Mantenibilidad: Cobertura ≥80% en `classification_agent.py` y `gemini_adapter.py`. Tests independientes sin IO real (excepto en tests específicos de storage).
- [x] Confiabilidad: Probar resiliencia ante caídas del FS o Gemini.

### Riesgos Identificados
> R-01: Ejecutar tests que creen carpetas masivamente o llamen a la API real de Google. Todo debe estar fuertemente mockeado.

## Especificaciones Técnicas — QA

### Estrategia de Testing

| Tipo de Test       | Herramienta             | Alcance                                                      |
|--------------------|-------------------------|--------------------------------------------------------------|
| Unitario Backend   | pytest + pytest-mock    | `classification_agent.py`, `gemini_adapter.py`, `local_storage.py` (updates) |
| Integración API    | N/A                     | Proceso interno de Worker, no expone endpoints directos nuevos     |
| Test de Repositorio| pytest + SQLAlchemy     | `clasificacion_repository.py` (Insert/UPSERT operations)             |

### Casos de Prueba Críticos

1. **Recepción (CA-01):** Validar rechazo con excepción cuando el paquete de entrada no tiene los campos mínimos obligatorios.
2. **Construcción de Rutas (CA-02):** Validar sanitización (ej: "José López" -> "JOSE_LOPEZ", "123.456-7" -> "1234567"). Validar el fallback "SIN_DATO".
3. **Mocks de Gemini (CA-03):** Probar que el adaptador formatea el prompt adecuadamente y parsea la respuesta JSON mockeada.
4. **Collision FS (CA-08):** Mockear `os.path.exists` para simular colisiones y probar que el nombre incrementa adecuadamente (`_001`, `_002`).
5. **UPSERT DB (CA-06 y CA-11):** Probar guardado inicial y luego reproceso. La DB debe reflejar 1 solo registro actualizado, no 2 separados.

### Cobertura Mínima Requerida
- Backend `classification_agent.py`: ≥80%
- Backend `gemini_adapter.py`: ≥80%
- Base de datos (Repository UPSERT): 100% en la lógica de conflicto.

## Estándares de Código — Referencia Gobernanza

> El agente DEBE adherirse a los estándares definidos en la Gobernanza Arquitectónica:
> Ruta: `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\Documentancion\Gobernanza_Arquitectura.md`

### Convención de Commits (Conventional Commits)
```
test(HU-05): suites de prueba para el agente de clasificación
```

## Dependencias y Pre-condiciones

### Requiere completado antes:
- [ ] Backend HU-05 CA-01 a CA-13 completado y en rama.

### Archivos que NO debe modificar:
- Código de producción en `BackEnd/app/` (solo mockear o usar en tests).

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
