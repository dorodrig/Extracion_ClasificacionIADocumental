# Handoff — QA — HU-02
## Iteración: 1 -DEV-HU-2

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_qa_HU02_CA01-CA04.md`                    |
| **Rol Destino**          | Agente QA                                         |
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
> Se requiere simulación/mock de los componentes de hardware (escáner TWAIN) en los tests de Frontend, así como validación del input del sistema de archivos local en los tests unitarios.

## Historia de Usuario — Contexto

> **Como** Operario de Digitalización,
> **Quiero** seleccionar el modo de ingesta de documentos (escáner por lotes o carpeta local) y enviar los archivos al pipeline de procesamiento,
> **Para que** el sistema inicie automáticamente el flujo de extracción OCR con los documentos correctos y en el orden adecuado, sin necesidad de intervención manual adicional.

### Descripción Funcional
Validar la funcionalidad de inicio de la ingesta en modo Escáner y Carpeta local, así como la correcta generación de Lotes (Batches) y presentación del dashboard correspondiente.

## Criterios de Aceptación

### CA-01 — Presentación de la pantalla de ingesta según modo confirmado por el operario
```gherkin
Dado que el operario ha confirmado el modo de ingesta en la pantalla de decisión (CA-00)
Cuando el sistema carga la pantalla de ingesta
Entonces el sistema carga la pantalla correspondiente al modo confirmado por el operario (Escáner o Carpeta)
  Y muestra el nombre de la regla activa y el cliente en la cabecera de la pantalla
  Y el modo de ingesta ya no es cambiable en esta pantalla (fue confirmado en el paso anterior)
```

### CA-02 — Activación del escáner en modo "Escáner por lotes"
```gherkin
Dado que el modo de ingesta es "Escáner por lotes"
Cuando el operario hace clic en "Iniciar Escáner"
Entonces el sistema intenta conectarse con el escáner local disponible vía driver del sistema
  Y si la conexión es exitosa, muestra el estado "Escáner conectado ✓" con el nombre del dispositivo
  Y si no detecta escáner, muestra el mensaje de error: "No se detectó ningún escáner. Verifica la conexión y el driver."
  Y no avanza al siguiente paso si el escáner no está conectado
```

### CA-03 — Captura de lote de documentos mediante escáner
```gherkin
Dado que el escáner está conectado y activo
Cuando el operario realiza la digitalización de los documentos
Entonces el sistema recibe los archivos generados y los lista en pantalla con: nombre de archivo, número de páginas, tamaño en MB
  Y asigna un batch_id único a toda la sesión de escaneo
  Y muestra el conteo total de documentos y páginas capturadas
  Y habilita el botón "Enviar a Procesamiento" una vez que al menos un documento ha sido capturado
```

### CA-04 — Selección de carpeta local en modo "Carpeta local"
```gherkin
Dado que el modo de ingesta es "Carpeta local (uno a uno)"
Cuando el operario hace clic en "Seleccionar Carpeta"
Entonces el sistema abre el diálogo nativo de selección de directorios del sistema operativo
  Y tras la selección, lista todos los archivos soportados (PDF, JPG, PNG, TIFF) dentro de la carpeta seleccionada
  Y muestra para cada archivo: nombre, extensión, tamaño en MB, número de páginas (si es PDF)
  Y si la carpeta no contiene archivos soportados, muestra: "La carpeta seleccionada no contiene documentos compatibles."
```

## Especificaciones Técnicas — QA

### Estrategia de Testing
| Tipo de Test     | Herramienta          | Alcance                       |
|------------------|----------------------|-------------------------------|
| Unitario Backend | pytest + pytest-asyncio | `BatchService` (Creación de lotes) |
| Unitario Frontend| Vitest + RTL         | Componentes UI (`IntakeDashboard`, `ScannerModule`, `FolderModule`) |
| Integración API  | pytest + TestClient  | POST `/api/v1/batches`        |

### Casos de Prueba por CA
- **CA-01**: Test Vitest verificando que el modo en el store renderice condicionalmente `<ScannerModule>` o `<FolderModule>`.
- **CA-02**: Test Vitest que intercepte un intento de conexión TWAIN, verifique mensaje de éxito o fallback al mensaje de error.
- **CA-03**: Test integración backend POST `/api/v1/batches` devuelve status 201 y un UUID de batch_id válido.
- **CA-04**: Test Vitest simulando un `File[]` upload con combinaciones válidas e inválidas (.txt, .docx vs .pdf, .jpg). Verificación de filtrado y mensajes.

### Validación ISO/IEC 25010
| Característica        | Verificación requerida                          |
|-----------------------|-------------------------------------------------|
| Mantenibilidad        | Cobertura unitaria superior al 80% en los módulos desarrollados |
| Seguridad             | Verificación JWT requerido para los endpoints backend de creación de lotes |
| Eficiencia Desempeño  | Tiempo de respuesta de endpoints backend bajo carga mínima |

### Cobertura Mínima Requerida
- Backend: ≥80% por servicio de dominio
- Frontend: Componentes críticos (IntakeDashboard, módulos Escáner/Carpeta)

## Estándares de Código — Referencia Gobernanza

> El agente DEBE adherirse a los estándares definidos en la Gobernanza Arquitectónica:
> Ruta: `C:\zData\ExtracionDatosIA\Documentancion\Gobernanza_Arquitectura.md`

### Convención de Commits (Conventional Commits)
```
test(HU-02): {descripción en español}
```

## Dependencias y Pre-condiciones

### Requiere completado antes:
- [ ] Desarrollo Backend HU-02 CA-01 a CA-04
- [ ] Desarrollo Frontend HU-02 CA-01 a CA-04

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
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama HU2_CA1-CA4_DevDamian_ITEREACION1. Avísale al Arquitecto."*
