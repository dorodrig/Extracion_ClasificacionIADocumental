# Solicitud de Revisión — Frontend HU-02 (CA-01 al CA-04)

**De:** Agente Frontend
**Para:** Arquitecto Líder

## Resumen del Plan Propuesto
Implementación de la interfaz de Ingesta Dual (Escáner/Carpeta) mediante React 18, TypeScript, SASS y Zustand. Se crearán los módulos `IntakeDashboard`, `ScannerModule` y `FolderModule` que reflejarán fielmente el MOCKUP-HU-02-Ingesta-Documentos.md.

## Decisiones Técnicas Clave
1. **Mock de Escáner TWAIN:** Puesto que los navegadores no tienen acceso nativo directo a escáneres por motivos de seguridad sin uso de plugins (ej. Dynamsoft Web TWAIN), se simulará la experiencia de escaneo (estado de conexión, simulación de captura de páginas y generación de archivos mock) para cumplir la validación visual y funcional del CA-02 y CA-03.
2. **Selección de Directorio (Carpeta):** Se utilizará el atributo `webkitdirectory` en un input tipo file para el CA-04, que es ampliamente soportado en navegadores basados en Chromium.

## Riesgos y Preguntas para el Arquitecto
1. **[CRÍTICO] Ausencia del Proyecto Base Vite:** La rama actual no contiene la carpeta `FrontEnd`. Aunque el Handoff menciona que la HU-01 (Componentes base) está completada, los archivos no se encuentran en este branch. **¿Debo inicializar el proyecto Vite desde cero con `npm create vite@latest` e instalar zustand/axios/sass, o hay algún error de merge/ramas que deba resolverse primero?**
2. **Integración Backend:** ¿El endpoint `/api/v1/batches` ya está mockeado en algún servidor o debo manejar de forma silente (catch y mock local) el POST para poder avanzar con la UI?

## Archivos Principales a Crear
- `FrontEnd/src/store/batchStore.ts`
- `FrontEnd/src/services/batchService.ts`
- `FrontEnd/src/components/intake/IntakeDashboard.tsx`
- `FrontEnd/src/components/intake/ScannerModule.tsx`
- `FrontEnd/src/components/intake/FolderModule.tsx`
- `FrontEnd/src/components/intake/DocumentList.tsx`
