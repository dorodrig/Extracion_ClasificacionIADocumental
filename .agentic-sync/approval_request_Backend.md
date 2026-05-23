# Solicitud de Aprobación - Backend HU-02

## Resumen del plan propuesto
Se implementarán los Criterios de Aceptación 05, 06, 07 y 08 para el backend correspondientes a la HU-02. Esto incluye la validación de extensiones permitidas, la creación de los adaptadores y puertos correspondientes para interactuar con el file system y segmentar PDFs, la orquestación en `ingestion_service.py` y la exposición de los endpoints REST `/prepare` y `/status`.

## Archivos que planeo crear/modificar
- **Nuevos:**
  - `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\domain\rules\document_rules.py`
  - `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\domain\ports\pdf_splitter_port.py`
  - `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\domain\ports\storage_port.py`
  - `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\services\storage\local_storage.py`
  - `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\services\storage\pdf_splitter.py`
  - `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\services\ingestion_service.py`
- **Modificados:**
  - `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\requirements.txt`
  - `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\core\config.py`
  - `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\core\exceptions.py`
  - `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\domain\ports\batch_repository.py`
  - `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\db\repositories\batch_repository.py`
  - `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\api\v1\endpoints\batches.py`

## Decisiones técnicas clave tomadas
- Se actualizará `config.py` para incluir `temp_dir` e inyectar la variable de entorno `TEMP_DIR`.
- En `pdf_splitter.py` se utilizará `pypdf` para fragmentar los PDFs de manera secuencial.
- Se crearán las excepciones `InvalidDocumentFormatException`, `PDFSplittingException`, `StorageException` en la capa centralizada según Gobernanza.

## Riesgos identificados
- Falta de configuración local de `TEMP_DIR` en `.env` (se mitigará usando validación si hace falta, aunque `pydantic-settings` lo exigirá).

## Preguntas para el Arquitecto
Ninguna. Todo claro en base al documento handoff.
