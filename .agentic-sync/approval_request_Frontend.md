# Solicitud de Aprobación - Frontend (HU-02, CA-05 y CA-08)

**Resumen del plan propuesto:**
Se implementará el componente `OmittedFilesAlert` para notificar al usuario sobre extensiones inválidas filtradas localmente y desde el backend. Se creará `IngestionProgress` para gestionar el polling de estado durante el proceso de preparación del batch y mostrar feedback en la UI. Adicionalmente, se migrarán todos los inline styles de los componentes correspondientes a sus archivos SCSS para saldar la deuda técnica de la iteración 1.

**Archivos a crear/modificar:**
- [NUEVO] `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\intake\OmittedFilesAlert.tsx`
- [NUEVO] `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\intake\OmittedFilesAlert.module.scss`
- [NUEVO] `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\intake\IngestionProgress.tsx`
- [NUEVO] `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\intake\IngestionProgress.module.scss`
- [MODIFICAR] `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\intake\DocumentList.tsx`
- [MODIFICAR] `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\intake\IntakeDashboard.tsx`
- [MODIFICAR] `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\intake\ScannerModule.tsx`
- [MODIFICAR] `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\intake\FolderModule.tsx`
- [MODIFICAR] `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\services\batchService.ts`
- [MODIFICAR] `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\store\batchStore.ts`

**Decisiones técnicas clave tomadas:**
- Se utilizará `setInterval` en un `useEffect` dentro de `IngestionProgress` para el polling de estado cada 1.5s, manejando un clean-up correcto en el desmontaje.
- El estado del polling será guardado en el store global de Zustand (`batchProgress`) para asegurar persistencia visual aunque otros componentes requieran actualizarse.
- El arreglo de archivos omitidos retornados por el endpoint `/prepare` se renderizará combinándose o complementando el de `FolderModule`.

**Riesgos identificados:**
- El intervalo de polling podría no limpiarse si hay desmontajes no controlados del componente, el `useEffect` será estricto al retornarlo.
- Mockear los endpoints de `prepare` y `status` si el backend aún no está disponible para probar la funcionalidad localmente.

**Preguntas para el Arquitecto:**
- Ninguna. Cumple con todos los lineamientos indicados en el handoff.
