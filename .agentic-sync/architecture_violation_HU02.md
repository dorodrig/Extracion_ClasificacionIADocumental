# Violación de Arquitectura — HU-02

**Agente:** Backend
**Fecha:** 2026-05-23
**Iteración:** 1 -DEV-HU-2
**Rama:** `HU2_CA1-CA4_DevDamian_ITEREACION1`

## Resumen de la Violación
Durante la auditoría de código Post-Ejecución, se ha detectado una violación a la **Clean Architecture** (Criterio de Evaluación §7.1 del SKILL).

## Detalle del Hallazgo
En el archivo `app/services/batch_service.py`, el servicio de dominio `BatchService` está inyectando directamente `sqlalchemy.orm.Session` y manipulando modelos ORM (`LoteProcesamiento`) con `self.db.add()` y `self.db.commit()`.

Según la Gobernanza (Diagrama §2.1 y Directorios §2.2) y el checklist de auditoría del SKILL:
- `[ ] Servicios no acceden directamente a la BD (usan Repository)`

Los casos de uso de la capa de Aplicación (Services) no deben conocer el ORM ni la sesión de base de datos directamente. Deben depender de una abstracción en la capa de dominio (Ports) y usar una implementación concreta de Repositorio (Adapter) inyectado.

## Corrección Requerida
1. Crear una interfaz (Port) en `app/domain/ports/batch_repository.py`.
2. Crear un repositorio (Adapter) en `app/db/repositories/batch_repository.py` que maneje el acceso a datos y devuelva el modelo de dominio.
3. Modificar `BatchService` para que reciba el Repositorio inyectado en lugar de `Session`, eliminando el uso de `self.db.add()` de la capa de servicio.

## Estado
**MERGE BLOQUEADO**. 
Reintentos restantes: 1/2.
El agente Backend debe corregir esto y realizar un nuevo push.
