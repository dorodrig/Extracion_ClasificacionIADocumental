# Handoff — Backend — HU-02
## Iteración: 1 -DEV-HU-2

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_backend_HU02_CA01-CA04.md`               |
| **Rol Destino**          | Agente Backend                                    |
| **HU de Origen**         | HU-02 — Ingesta Dual de Documentos (Escáner/Carpeta)|
| **CAs Asignados**        | CA-01, CA-02, CA-03, CA-04                        |
| **CAs Excluidos**        | Ninguno de la selección actual.                   |
| **Rama Git**             | `HU2_CA1-CA4_DevDamian_ITEREACION1`               |
| **Iteración**            | 1 -DEV-HU-2                                       |
| **Fecha de Generación**  | 2026-05-23 10:57                                  |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: Python 3.12 + FastAPI 0.115 + SQLAlchemy + Alembic
- [x] Frontend: React 18 + TypeScript + Vite 5
- [x] Estilos: SASS/SCSS (preprocesador) — CSS puro como fallback justificado
- [x] Base de Datos: SQL Server 2019+ (SQLAlchemy ORM)
- [x] SDKs: google-generativeai (Gemini) + boto3 (Textract)
- [x] Cola: Celery 5 + Redis

### Patrón Arquitectónico
- [x] Clean Architecture (Ports & Adapters)
- [x] Capas: Infraestructura → Aplicación → Dominio
- [x] Inversión de Dependencias (Ports/Interfaces en capa dominio)

### Preparación Cloud-Ready
- [x] Adapters reemplazables sin cambiar dominio
- [x] Variables de entorno externalizadas (.env)
- [x] CERO credenciales hardcodeadas

### ISO/IEC 25010
- [x] Mantenibilidad: Modularidad, modificabilidad, testeabilidad
- [x] Seguridad: JWT + RBAC + aislamiento de contexto IA
- [x] Eficiencia de Desempeño: Paginación, índices, async/Celery

### Riesgos Identificados
> El manejo de archivos grandes desde la carga local (CA-04) puede generar cuellos de botella en la memoria de la API REST. Usar UploadFile de FastAPI para streaming en disco.

## Historia de Usuario — Contexto

> **Como** Operario de Digitalización,
> **Quiero** seleccionar el modo de ingesta de documentos (escáner por lotes o carpeta local) y enviar los archivos al pipeline de procesamiento,
> **Para que** el sistema inicie automáticamente el flujo de extracción OCR con los documentos correctos y en el orden adecuado, sin necesidad de intervención manual adicional.

### Descripción Funcional
El backend debe proveer endpoints para la creación de lotes de procesamiento y el registro inicial de los documentos asociados al lote. El CA-01 a CA-04 se enfoca en la selección y validación en la UI, pero el backend requiere preparar la tabla de lotes (batch_id único) y documentos para cuando el lote se envíe.

## Criterios de Aceptación

### CA-01 — Presentación de la pantalla de ingesta según modo confirmado por el operario
```gherkin
Dado que el operario ha confirmado el modo de ingesta en la pantalla de decisión (CA-00)
Cuando el sistema carga la pantalla de ingesta
Entonces el sistema carga la pantalla correspondiente al modo confirmado por el operario (Escáner o Carpeta)
  Y muestra el nombre de la regla activa y el cliente en la cabecera de la pantalla
  Y el modo de ingesta ya no es cambiable en esta pantalla (fue confirmado en el paso anterior)
```
**Notas de implementación para el agente:**
> Responsabilidad principalmente Frontend, pero se requiere consultar la regla activa y validar el estado del lote en backend.

### CA-02 — Activación del escáner en modo "Escáner por lotes"
```gherkin
Dado que el modo de ingesta es "Escáner por lotes"
Cuando el operario hace clic en "Iniciar Escáner"
Entonces el sistema intenta conectarse con el escáner local disponible vía driver del sistema
  Y si la conexión es exitosa, muestra el estado "Escáner conectado ✓" con el nombre del dispositivo
  Y si no detecta escáner, muestra el mensaje de error: "No se detectó ningún escáner. Verifica la conexión y el driver."
  Y no avanza al siguiente paso si el escáner no está conectado
```
**Notas de implementación para el agente:**
> Tarea exclusiva de Frontend (Web TWAIN o integración nativa del navegador). Backend solo provee el endpoint para iniciar la sesión de lote.

### CA-03 — Captura de lote de documentos mediante escáner
```gherkin
Dado que el escáner está conectado y activo
Cuando el operario realiza la digitalización de los documentos
Entonces el sistema recibe los archivos generados y los lista en pantalla con: nombre de archivo, número de páginas, tamaño en MB
  Y asigna un batch_id único a toda la sesión de escaneo
  Y muestra el conteo total de documentos y páginas capturadas
  Y habilita el botón "Enviar a Procesamiento" una vez que al menos un documento ha sido capturado
```
**Notas de implementación para el agente:**
> El backend debe generar un UUID de lote (`batch_id`) cuando el operario inicie la sesión (POST `/api/v1/batches`).

### CA-04 — Selección de carpeta local en modo "Carpeta local"
```gherkin
Dado que el modo de ingesta es "Carpeta local (uno a uno)"
Cuando el operario hace clic en "Seleccionar Carpeta"
Entonces el sistema abre el diálogo nativo de selección de directorios del sistema operativo
  Y tras la selección, lista todos los archivos soportados (PDF, JPG, PNG, TIFF) dentro de la carpeta seleccionada
  Y muestra para cada archivo: nombre, extensión, tamaño en MB, número de páginas (si es PDF)
  Y si la carpeta no contiene archivos soportados, muestra: "La carpeta seleccionada no contiene documentos compatibles."
```
**Notas de implementación para el agente:**
> Igual que en CA-03, Backend debe inicializar un lote en modo `carpeta`. Frontend enviará la lista de archivos soportados después de la selección local.

## Especificaciones Técnicas — Backend

### Estructura de Directorios
> Referencia: Gobernanza §2.2 — Estructura de directorios obligatoria del Backend
`BackEnd/app/api/v1/endpoints/batches.py`
`BackEnd/app/services/batch_service.py`
`BackEnd/app/db/models/batches.py`
`BackEnd/app/schemas/batches.py`
`BackEnd/app/domain/models/batch.py`

### Endpoints API REST
| Método | Ruta                  | Descripción            | Auth    |
|--------|-----------------------|------------------------|---------|
| POST   | `/api/v1/batches`     | Crea un nuevo lote con UUID `batch_id` para iniciar la sesión | `operario`, `admin` |

### Schemas Pydantic (Entrada/Salida)
- `BatchCreate`: `regla_id: int`, `cliente_id: int`, `modo_ingesta: str ("scanner" | "carpeta")`
- `BatchResponse`: `id: int`, `batch_id: UUID`, `estado: str`, `created_at: datetime`

### Modelo de Datos (SQLAlchemy)
- Tabla `lotes_procesamiento` y `documentos_lote` según `HU-02-Ingesta-Documentos-Dual.md`.

### Reglas de Negocio
- El modo de ingesta debe ser estrictamente validado ("scanner" o "carpeta").
- El UUID debe generarse en la base de datos o en la capa de servicio al crear el lote.

## Estándares de Código — Referencia Gobernanza

> El agente DEBE adherirse a los estándares definidos en la Gobernanza Arquitectónica:
> Ruta: `C:\zData\ExtracionDatosIA\Documentancion\Gobernanza_Arquitectura.md`

### Estándares aplicables a este Handoff:
- §3.1 Nombrado Python (snake_case, plural en endpoints).
- §3.2 Endpoints REST (uso de `APIResponse`).
- §3.3 Excepciones de dominio personalizadas.
- §3.4 Seguridad (Validación RBAC de endpoints).

### Convención de Commits (Conventional Commits)
```
feat(HU-02): {descripción en español}
```

## Dependencias y Pre-condiciones

### Requiere completado antes:
- [ ] HU-01 (Reglas de Trabajo)
- [ ] HU-08 (Auth)
- [ ] HU-10 (Schema BD inicializado para las tablas de lotes)

### Produce entregables para:
- [ ] Handoff Frontend HU-02 (consumo de la API de lotes)

### Archivos que NO debe modificar (fuera de su jurisdicción):
- Cualquier archivo en `FrontEnd/`
- Mockups

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
   - Analiza cada CA asignado y desglosa las tareas técnicas.
   - Identifica riesgos y dependencias.
   - Estima el esfuerzo por tarea.

2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El Humano es solo un cartero. No tiene autoridad técnica para aprobar ni rechazar planes.

3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
   
   El archivo debe contener:
   - Resumen del plan propuesto
   - Archivos que planeas crear/modificar (con rutas absolutas)
   - Decisiones técnicas clave tomadas
   - Preguntas para el Arquitecto (si las hay)
   - Riesgos identificados

4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."

5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación explícita del Arquitecto Líder (transmitida por el Humano Cartero), pasa a modo `EXECUTION`.

6. **En modo `EXECUTION`:**
   - Codifica siguiendo estrictamente los estándares de la Gobernanza.
   - Haz `git add`, `git commit` (con Conventional Commits) y `git push` a la rama indicada.
   - Actualiza el `task.md` con el progreso.

7. **Al terminar la ejecución:**
   - Genera un `walkthrough.md` con resumen de cambios.
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama HU2_CA1-CA4_DevDamian_ITEREACION1. Avísale al Arquitecto."*
