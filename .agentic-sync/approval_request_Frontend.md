# Solicitud de Revisión: Frontend

Hola Arquitecto Líder,

He completado el análisis y elaborado el plan de implementación para el **CA-10 (Indicador de progreso de OCR)** de la **HU-03**.

El plan incluye:
- Componente `OcrProgressIndicator` con SCSS Modules (modo oscuro).
- Hook `useOcrProgress` usando React Query con `refetchInterval: 3000` para polling mientras el estado sea "en proceso".
- Servicio para conectar con el endpoint `GET /api/v1/ocr/progress/{batch_id}`.

Por favor, revisa el plan de implementación y confirma si puedo proceder con la fase de ejecución.

Quedo a la espera de tu aprobación.

Saludos,
Agente Frontend
# Solicitud de Revisión — Frontend HU-06

## Resumen del plan propuesto
Implementación de la HU-06 (Validación Humana: Pendientes y Visor). Se construirán dos vistas principales integradas en `PendientesPage.tsx`:
1. **Lista de Documentos Pendientes**: Incluye filtros de búsqueda y la tabla con tiempos de espera semaforizados (verde, ámbar, rojo).
2. **Visor de Documentos (Split Screen 65/35)**: Integración de `react-pdf` en el panel izquierdo (dark mode #0d1117) y un panel derecho reactivo para validación, edición y envío de instrucciones al agente de IA.

## Archivos a crear/modificar
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\pages\PendientesPage.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\pending\PendingDocumentList.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\pending\PendingFilters.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\pending\DocumentViewer.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\pending\ExtractedDataPanel.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\pdf-viewer\PDFViewer.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\services\pendientesService.ts`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\store\pendientesStore.ts`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\styles\components\_pendientes.scss`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\styles\components\_visor.scss`

## Decisiones técnicas clave tomadas
- Se utilizará `Zustand` para el manejo del estado (ej. documento activo, lista de pendientes) para evitar prop drilling entre el visor y la lista.
- Se implementará el visor a pantalla completa (full-page) tal como indica el mockup narrativo, gestionando la visibilidad condicional dentro de `PendientesPage.tsx`.
- Se respetará estrictamente el uso de tokens semánticos definidos en `_variables.scss` (`$color-error`, `$color-warning`, `$color-success`) para la semaforización.

## Riesgos identificados
- Rendimiento en el renderizado del visor PDF si los archivos son muy pesados; mitigaremos limitando el renderizado solo a la página activa usando paginación en `react-pdf`.
- Manejo de WebSockets para notificaciones (requiere coordinación con backend si no están disponibles aún).

## Preguntas para el Arquitecto
Ninguna. Todo claro en los lineamientos y mockups.
