# Solicitud de Revisión: Backend HU-07

Se ha generado el plan de implementación para la HU-07 (Portal Web de Consulta para Cliente Final), el cual abarca los siguientes Criterios de Aceptación:
CA-01, CA-02, CA-03, CA-04, CA-05, CA-07, CA-08, CA-09, CA-12.

## Resumen del Plan
1. **Seguridad Mockeada**: Implementación de un dependencia `get_current_cliente` que devuelve un `cliente_id` simulado, de acuerdo a la instrucción de que la HU-08 está pendiente.
2. **Endpoints en `/api/v1/cliente/`**:
   - `/dashboard`: Métricas, incluyendo "Pendiente Revisión Humana".
   - `/carpetas`: Árbol JSON jerárquico.
   - `/documentos`: Paginación, filtros y búsqueda.
   - `/documentos/{id}`: Metadatos y campos.
   - `/documentos/{id}/descargar`: Descarga con `Content-Disposition`.

Por favor, Arquitecto Líder, revisa y aprueba el plan para proceder con la ejecución.
# Solicitud de Revisión: Backend HU-06

## Resumen del plan propuesto
Se implementarán los componentes backend (Models, Repositories, Schemas, Services y Endpoints) para soportar la validación humana de documentos pendientes. Esto incluye operaciones CRUD paginadas y endpoints de acción (corrección, instrucción, descarte) además de un WebSocket para actualización en tiempo real, conforme a los CA-01 a CA-12 de la HU-06.

## Archivos que se planean crear/modificar
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\db\models\documentos_pendientes.py` (Crear)
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\db\repositories\pendientes_repository.py` (Crear)
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\schemas\pendientes.py` (Crear)
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\services\pendientes_service.py` (Crear)
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\api\v1\endpoints\pendientes.py` (Crear)
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\api\v1\router.py` (Modificar)

## Decisiones técnicas clave tomadas
- Se usará SQLAlchemy para el modelo `DocumentoPendiente`.
- La lógica de negocio estará encapsulada en `PendientesService`.
- Se creará un endpoint WebSocket dentro de `pendientes.py` para notificar al frontend en tiempo real sobre cambios de estado.
- Se seguirá el estándar de `APIResponse` unificado para todas las respuestas JSON, en línea con la Gobernanza §3.2.

## Preguntas para el Arquitecto
- ¿La tabla `documentos_pendientes` se relaciona explícitamente mediante Foreign Key con alguna tabla de clientes y lotes o se maneja lógicamente?
- ¿Existen esquemas de autenticación listos para importar (para la restricción de rol "Operario"), o por ahora se omite hasta que se implemente la HU-08?

## Riesgos identificados
- Riesgo de desconexión en WebSockets: se debe considerar la lógica de reconexión desde el Frontend, mientras que el Backend debe gestionar adecuadamente las caídas de conexión.
# Solicitud de Aprobación - Backend HU-10

**A:** Arquitecto Líder (Orquestador)
**De:** Agente Backend (DBA)
**Fecha:** 2026-05-23
**Referencia:** HU-10 — Esquema de Base de Datos (CA-01 a CA-08)
**Rama:** `HU2_CA1-CA4_DevDamian_ITEREACION1`

## Resumen del Plan de Implementación

He finalizado la fase de planificación según el Handoff `handoff_backend_HU10_CA01-CA08.md`. Las acciones principales propuestas son:
1. Crear `base.py` y centralizar la inicialización y registro de modelos para Alembic.
2. Separar `Cliente` de `usuarios.py` a `clientes.py`.
3. Crear el modelo `ReglaTrabajo` en `reglas.py`.
4. Renombrar y refactorizar `batches.py` a `documentos_lote.py`.
5. Asegurar índices non-clustered, columnas JSON y la preparación de `contenido_b64` en `documentos_clasificados.py` y `documentos_pendientes.py`.
6. Modificar `auditoria.py` cambiando las ForeignKeys afectadas (documento_id, usuario_id) para habilitar `ON DELETE SET NULL`, cambiando dichas columnas a `nullable=True`.
7. Inicializar Alembic y generar la primera migración `Initial schema`.

## Estado
El agente se encuentra actualmente en modo `PLANNING`. 

## Solicitud
Se solicita revisión y aprobación formal para proceder a la fase de `EXECUTION` y realizar las modificaciones en el código y operaciones en Git correspondientes.
