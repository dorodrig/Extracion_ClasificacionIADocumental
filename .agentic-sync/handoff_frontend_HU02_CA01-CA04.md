# Handoff — Frontend — HU-02
## Iteración: 1 -DEV-HU-2

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_frontend_HU02_CA01-CA04.md`              |
| **Rol Destino**          | Agente Frontend                                   |
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
> La conexión directa al escáner local desde la web (CA-02, CA-03) puede requerir Web TWAIN o una utilidad complementaria local. Se debe prever un fallback si el navegador bloquea accesos directos al hardware.

## Historia de Usuario — Contexto

> **Como** Operario de Digitalización,
> **Quiero** seleccionar el modo de ingesta de documentos (escáner por lotes o carpeta local) y enviar los archivos al pipeline de procesamiento,
> **Para que** el sistema inicie automáticamente el flujo de extracción OCR con los documentos correctos y en el orden adecuado, sin necesidad de intervención manual adicional.

### Descripción Funcional
Implementación UI para el proceso de Ingesta. El frontend debe presentar la pantalla de selección de ingesta (Escáner o Carpeta). Si es escáner, debe integrarse con dispositivos TWAIN. Si es carpeta, debe abrir el diálogo nativo del SO, listar archivos filtrando por tipo válido (PDF, JPG, PNG, TIFF) y preparar el lote para envío.

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
> Construir componente React principal para ingesta `IntakeDashboard.tsx` que condicionalmente carga subcomponentes `ScannerModule` o `FolderModule` según el store.

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
> Tarea exclusiva de Frontend. Si no se dispone de Web TWAIN licenciado, simular la conexión para el piloto o usar una API JS estándar para adquisición de imágenes.

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
> Obtener `batch_id` realizando POST a `/api/v1/batches` en el momento en que inicia la sesión de captura. Renderizar una tabla con los documentos.

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
> Usar un `<input type="file" webkitdirectory directory multiple>` para abrir el diálogo de carpeta. Filtrar los archivos por extensión válida en el JS. Obtener el `batch_id` desde el API REST de lotes.

## Especificaciones Técnicas — Frontend

### Estructura de Directorios
> Referencia: Gobernanza §4.1 — Estructura de directorios obligatoria del Frontend
`FrontEnd/src/components/intake/IntakeDashboard.tsx`
`FrontEnd/src/components/intake/ScannerModule.tsx`
`FrontEnd/src/components/intake/FolderModule.tsx`
`FrontEnd/src/components/intake/DocumentList.tsx`
`FrontEnd/src/store/batchStore.ts`
`FrontEnd/src/services/batchService.ts`

### Componentes React
| Componente           | Ubicación                        | Props principales        |
|----------------------|----------------------------------|--------------------------|
| `IntakeDashboard`    | `src/components/intake/`         | N/A (usa store)          |
| `ScannerModule`      | `src/components/intake/`         | `onCapture(file)`        |
| `FolderModule`       | `src/components/intake/`         | `onSelect(files)`        |

### Endpoints a Consumir (del Backend)
| Método | Ruta                  | Descripción            | Schema Respuesta   |
|--------|-----------------------|------------------------|--------------------|
| POST   | `/api/v1/batches`     | Crea sesión de lote    | `APIResponse<Batch>` |

### TypeScript Interfaces (Espejo de Schemas Pydantic)
```typescript
interface Batch {
  id: number;
  batch_id: string;
  estado: string;
}
```

### Estado Global (Zustand)
Modificar o crear `src/store/batchStore.ts` para rastrear:
- `activeBatchId`
- `documentsList` (local in-memory state before upload)
- `ingestMode` ('scanner' | 'carpeta')

### Referencia de Mockups
> `C:\zData\ExtracionDatosIA\HU\HU-Mockups\MOCKUP-HU-02-Ingesta-Documentos.md`
> `C:\zData\ExtracionDatosIA\Mockups\HU-02-Ingesta-Documentos-Desktop.png`
> El agente Frontend DEBE leerlos e interpretarlos como la referencia visual
> OBLIGATORIA para la maquetación de componentes. La fidelidad visual al mockup es un criterio de aceptación.

### Estilos SASS/SCSS
> Referencia: Gobernanza §4.3 — Estándares de estilos del Frontend

| Elemento | Convención |
|----------|------------|
| Preprocesador | SASS/SCSS (instalado vía `sass` en `devDependencies`) |
| Entry point | `src/styles/main.scss` — importa todos los parciales |
| Componentes | `ComponentName.module.scss` junto al `.tsx` — Estilos modulares con CSS Modules |
| !important | PROHIBIDO (excepto overrides de librerías externas justificados) |
| Inline styles | PROHIBIDO en componentes React |

## Estándares de Código — Referencia Gobernanza

> El agente DEBE adherirse a los estándares definidos en la Gobernanza Arquitectónica:
> Ruta: `C:\zData\ExtracionDatosIA\Documentancion\Gobernanza_Arquitectura.md`

### Estándares aplicables a este Handoff:
- §4.2 TypeScript/React: Componentes PascalCase, Props tipadas estrictamente.
- §4.3 Llamadas a la API: uso de axios con interceptores JWT (`api.ts`).
- §4.7 SCSS / Design System GRM: obligatoriedad de CSS Modules y tokens.

### Convención de Commits (Conventional Commits)
```
feat(HU-02): {descripción en español}
```

## Dependencias y Pre-condiciones

### Requiere completado antes:
- [x] HU-01 (Componentes base UI de reglas)
- [ ] Backend Handoff HU-02 (API REST de creación de lotes disponible)

### Produce entregables para:
- [ ] Handoff Frontend HU-02 CA-05 a CA-12 (Carga de archivos y envío)

### Archivos que NO debe modificar (fuera de su jurisdicción):
- Cualquier archivo en `BackEnd/`

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
   - Analiza cada CA asignado y desglosa las tareas técnicas.
   - Identifica riesgos y dependencias.
   - Estima el esfuerzo por tarea.

2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El Humano es solo un cartero. No tiene autoridad técnica para aprobar ni rechazar planes.

3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Frontend.md`
   
   El archivo debe contener:
   - Resumen del plan propuesto
   - Archivos que planeas crear/modificar (con rutas absolutas)
   - Decisiones técnicas clave tomadas
   - Preguntas para el Arquitecto (si las hay)
   - Riesgos identificados

4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Frontend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."

5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación explícita del Arquitecto Líder (transmitida por el Humano Cartero), pasa a modo `EXECUTION`.

6. **En modo `EXECUTION`:**
   - Codifica siguiendo estrictamente los estándares de la Gobernanza.
   - Haz `git add`, `git commit` (con Conventional Commits) y `git push` a la rama indicada.
   - Actualiza el `task.md` con el progreso.

7. **Al terminar la ejecución:**
   - Genera un `walkthrough.md` con resumen de cambios.
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama HU2_CA1-CA4_DevDamian_ITEREACION1. Avísale al Arquitecto."*
