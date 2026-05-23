# Solicitud de Aprobación — Frontend

**Para:** Arquitecto Líder
**De:** Agente Frontend
**Fecha:** 2026-05-23
**Rama:** HU1_CA1-CA6_DEVDAVID_ITEREACION1

He revisado el código actual de React en `C:\zData\ExtracionDatosIA\FrontEnd` y elaborado un plan técnico para implementar los Criterios de Aceptación CA-07 a CA-13 correspondientes a HU-01 (Parte 2).

## Resumen del Plan Técnico

1. **`RuleForm.tsx` (Formulario)**
   - **CA-07:** Agregaré un analizador regex sobre el valor `patron_carpeta` (`\{([^}]+)\}`) en tiempo real, validando los extractos encontrados contra `VARIABLES_PATRON` y la lista de `campos_extraer` definidos por el usuario en el formulario. Si hay no coincidentes, renderizaré una advertencia bajo la vista previa.
   - **CA-08:** Modificaré el bloque de "Configuración OCR" para que sea un input disabled/visual y agregaré el ícono de tooltip nativo con la explicación descrita.
   - **CA-12:** Interceptaré el objeto de error retornado por la mutación. Si corresponde a HTTP 409 (Regla Duplicada), emplearé el método `setError('nombre', ...)` de React Hook Form para enrutar visualmente el mensaje debajo del input del nombre.
   - **CA-13:** Validaré la funcionalidad actual (ya presente visualmente) de radio buttons para asegurar su correcto binding con React Hook Form.

2. **`RuleList.tsx` (Lista de Reglas)**
   - **CA-09:** Actualizaré `handleStartProcess` para redirigir/mockear hacia la vista de ingesta pasando el `rule.id` por query params, utilizando `window.location.href = "/ingesta?rule_id={id}"` provisionalmente.
   - **CA-11:** Añadiré el botón de acción "📋 Duplicar" e integraré una mutación de React Query (`useMutation`) que llamará al nuevo servicio, invalidando `['rules']` al tener éxito.

3. **`ruleService.ts` (Servicios)**
   - **CA-11:** Expondré un nuevo método asíncrono `duplicateRule(ruleId)` que apunte al endpoint `POST /api/v1/rules/{id}/duplicate`.

## Solicitud

Solicito revisión y aprobación formal para cambiar a modo EXECUTION y aplicar los cambios.

**Responde "Aprobado" para iniciar.**
