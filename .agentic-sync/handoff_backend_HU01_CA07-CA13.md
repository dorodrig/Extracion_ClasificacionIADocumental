# Handoff — Backend — HU-01 (Parte 2)
## Iteración: 2-DEV-HU-1

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_backend_HU01_CA07-CA13.md`               |
| **Rol Destino**          | Agente Backend                                    |
| **HU de Origen**         | HU-01 — Configuración y Gestión de Reglas de Trabajo del Cliente |
| **CAs Asignados**        | CA-07, CA-10, CA-11, CA-12, CA-13                 |
| **CAs Excluidos**        | CA-08, CA-09 (Solo UI/Frontend)                   |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 2-DEV-HU-1                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: Python 3.12 + FastAPI 0.115 + SQLAlchemy + Alembic

### Riesgos Identificados
> R-05: Lógica de duplicación (CA-11). Al duplicar una regla, el nuevo nombre debe ser único. Se debe manejar correctamente la copia profunda del JSON de `campos_extraer` y reiniciar la versión a 1.
> R-06: Validación del patrón de carpeta (CA-07). Asegurar que el backend verifique que las variables en `{...}` coincidan con los `campos_extraer` definidos.

## Criterios de Aceptación Asignados al Backend

### CA-07 — Configuración y validación del patrón de carpeta de salida
**Responsabilidad Backend:**
Validar a nivel de dominio (en `rule_validation.py`) que el patrón proporcionado contenga al menos una variable que corresponda a un campo extraíble definido en la misma regla.

### CA-10 — Versionamiento automático al actualizar una regla existente
**Responsabilidad Backend:**
En el endpoint `PUT /api/v1/rules/{id}`, incrementar automáticamente el campo `version`. Registrar la versión anterior en la tabla `reglas_trabajo_historial` (histórico/soft delete implícito). 
*Nota: Si la tabla historial no existe en los modelos de SQLAlchemy, debes crearla y generar la migración.*

### CA-11 — Persistencia de reglas para uso en futuros proyectos ("Duplicar Regla")
**Responsabilidad Backend:**
Implementar endpoint `POST /api/v1/rules/{id}/duplicate`. Debe clonar la regla existente y asignarle un sufijo al nombre (ej. "Nombre Original (Copia)") para evitar conflicto de CA-12.

### CA-12 — Validación de nombre único de regla por cliente
**Responsabilidad Backend:**
Esta validación ya fue abordada parcialmente en el Sprint anterior, pero se debe reforzar asegurando que el endpoint devuelva el error HTTP 409 Conflict con el mensaje exacto esperado por el frontend.

### CA-13 — Selección de modo de entrada de documentos en la regla
**Responsabilidad Backend:**
Validar que el `modo_entrada` recibido sea estrictamente 'scanner' o 'carpeta'.

## Especificaciones Técnicas — Backend

### Endpoints Nuevos/Modificados
| Método | Ruta                        | Descripción                          |
|--------|-----------------------------|--------------------------------------|
| POST   | `/api/v1/rules/{id}/duplicate` | Duplicar regla existente             |
| PUT    | `/api/v1/rules/{id}`        | Actualizar (debe guardar histórico)  |

### Modelo de Datos (SQLAlchemy) a extender
- Tabla `reglas_trabajo_historial`: id, regla_id, version, snapshot_json, modificado_por, modificado_at.

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.**
3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."
5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación, pasa a modo `EXECUTION`.
6. **Al terminar la ejecución:** Genera un `walkthrough.md` y avisa al Humano.
