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
