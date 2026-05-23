# Solicitud de Aprobación - QA (HU-01 Parte 2)

**Para:** Arquitecto Líder
**De:** Agente QA
**Iteración:** 2-DEV-HU-1
**Rama:** HU1_CA1-CA6_DEVDAVID_ITEREACION1
**CAs Asignados:** CA-07 al CA-13

## Resumen del Plan de Implementación de Pruebas

He evaluado los requerimientos del Handoff y el estado actual de la rama. Mi plan de ejecución para automatizar y validar los Criterios de Aceptación es el siguiente:

### Casos de Prueba Backend (pytest)
1. **CA-11 (Duplicar Regla):** Implementar prueba unitaria/integración para el endpoint `POST /api/v1/rules/{id}/duplicate` verificando que cree una copia con la convención de nombres y versión 1.
2. **CA-10 (Versionamiento):** Implementar prueba para `PUT /api/v1/rules/{id}` que asegure el incremento automático de la versión tras una actualización.
3. **CA-12 (Validación Nombre Único):** Implementar prueba para `POST /api/v1/rules` comprobando que retorne HTTP 409 cuando se intenta usar un nombre ya existente para el mismo cliente.

### Casos de Prueba Frontend (Vitest + React Testing Library)
1. **CA-07 (Validación Patrón Carpeta):** Implementar prueba de UI en el formulario de reglas que valide la aparición de un `warning` cuando el input contenga variables de patrón no reconocidas.
2. **CA-08 (Umbral OCR Fijo):** Implementar prueba de UI para asegurar que el input de OCR confidence threshold tenga el atributo `disabled` y mantenga siempre el valor visual del `95%`.
3. **Resto de CAs Frontend (CA-09, CA-13):** Ajustar y validar casos de navegación y manejo de estado según especificado, cubriendo los flujos descritos en el handoff.

## Cobertura de Código
Me aseguraré de que las pruebas creadas/modificadas mantengan o superen el 80% de cobertura requerida para el componente de Gestión de Reglas, tanto en Frontend como en Backend.

Solicito su revisión y aprobación del plan de implementación para proceder con la ejecución (escritura del código de los tests) en modo EXECUTION.
