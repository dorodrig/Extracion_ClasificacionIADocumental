# Handoff — Frontend — HU-06
## Iteración: 4 -DEV-HU-6

| Campo                    | Valor                                                        |
|--------------------------|--------------------------------------------------------------|
| **Archivo**              | `handoff_frontend_HU06_CA01-CA12.md`                         |
| **Rol Destino**          | Agente Frontend                                              |
| **HU de Origen**         | HU-06 — Validación Humana: Pendientes y Visor                |
| **CAs Asignados**        | CA-01 a CA-12                                                |
| **CAs Excluidos**        | Ninguno                                                      |
| **Rama Git**             | `HU2_CA1-CA4_DevDamian_ITEREACION1`                          |
| **Iteración**            | 4 -DEV-HU-6                                                  |
| **Fecha de Generación**  | 2026-05-23                                                   |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)                        |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md                          |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Frontend: React 18 + TypeScript + Vite 5
- [x] Estilos: SASS/SCSS (preprocesador)
- [x] Visor PDF: `react-pdf`
- [x] Estado y HTTP: Zustand + Axios
- [x] WebSockets: API nativa de WebSocket para React

### Patrón Arquitectónico
- [x] Componentes en `src/components/pending/`
- [x] Estilos modulares en `src/styles/components/` o `.module.scss`
- [x] Diseño estricto basado en `MOCKUP-HU-06-Validacion-Operario.md`

### ISO/IEC 25010
- [x] Operabilidad: Diseño UX amigable, prevención de fatiga visual (Dark Mode para el visor), atajos claros.
- [x] Confiabilidad: Manejo de pérdida de conexión WS.

## Historia de Usuario — Contexto

> **Como** Operario de Digitalización,
> **Quiero** ver una lista de documentos que el pipeline automático no pudo procesar completamente, acceder a un visor que me muestre el documento junto con los datos extraídos y el motivo del rechazo, y poder corregir campos individuales o enviar una instrucción al Agente de Clasificación para que resuelva los errores.

## Especificaciones Técnicas — Frontend

### Estructura de Directorios
Archivos a crear/modificar:
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\pages\PendientesPage.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\pending\PendingDocumentList.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\pending\PendingFilters.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\pending\DocumentViewer.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\pending\ExtractedDataPanel.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\pdf-viewer\PDFViewer.tsx` (Si aún no existe, crearlo como genérico reutilizable)
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\services\pendientesService.ts`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\store\pendientesStore.ts`
- Modulos SCSS correspondientes en `FrontEnd\src\styles\components\` o junto a los componentes.

### Referencia de Mockups
> Lee el mockup narrativo detallado en `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\HU\HU-Mockups\MOCKUP-HU-06-Validacion-Operario.md`. Es obligatorio respetar el layout de dos paneles para el visor (65% visor, 35% datos), y los colores indicados (ámbar, rojo, verde). 
> Si existen imágenes PNG en `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\Mockups\`, debes interpretarlas como referencia visual obligatoria.

### Endpoints a Consumir
| Método | Ruta                                      |
|--------|-------------------------------------------|
| GET    | `/api/v1/pendientes`                      |
| GET    | `/api/v1/pendientes/{id}/visor`           |
| PUT    | `/api/v1/pendientes/{id}/correccion`      |
| POST   | `/api/v1/pendientes/{id}/instruccion`     |
| PUT    | `/api/v1/pendientes/{id}/descarte`        |

### Estilos SASS/SCSS
- Usar variables SCSS (design tokens) predefinidas en `_variables.scss` para los colores semánticos (`$color-error`, `$color-warning`, `$color-success`).
- El visor del documento y el panel derecho deben tener un fondo oscuro (`#0d1117`) como dictan las especificaciones del mockup.
- CSS-in-JS o estilos en línea están PROHIBIDOS.

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
   - Analiza cada CA asignado y desglosa las tareas técnicas.
   - Identifica riesgos y dependencias.
   - Estima el esfuerzo por tarea.

2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El Humano es solo un cartero. No tiene autoridad técnica para aprobar ni rechazar planes.

3. **Guarda tu solicitud de revisión** en:
   `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Frontend.md`
   
   El archivo debe contener:
   - Resumen del plan propuesto
   - Archivos que planeas crear/modificar (con rutas absolutas)
   - Decisiones técnicas clave tomadas
   - Preguntas para el Arquitecto (si las hay)
   - Riesgos identificados

4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Frontend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."

5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación explícita del Arquitecto Líder (transmitida por el Humano Cartero), pasa a modo `EXECUTION`.

6. **En modo `EXECUTION`:**
   - Codifica siguiendo estrictamente los estándares de la Gobernanza.
   - Haz `git add`, `git commit` (con Conventional Commits) y `git push` a la rama indicada.
   - Actualiza el `task.md` con el progreso.

7. **Al terminar la ejecución:**
   - Genera un `walkthrough.md` con resumen de cambios.
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama HU2_CA1-CA4_DevDamian_ITEREACION1. Avísale al Arquitecto."*
