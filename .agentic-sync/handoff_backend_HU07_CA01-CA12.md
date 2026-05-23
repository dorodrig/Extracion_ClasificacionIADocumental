# Handoff — Backend — HU-07
## Iteración: 1-DEV-HU-7

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_backend_HU07_CA01-CA12.md`               |
| **Rol Destino**          | Agente Backend                                    |
| **HU de Origen**         | HU-07 — Portal Web de Consulta para Cliente Final |
| **CAs Asignados**        | CA-01, CA-02, CA-03, CA-04, CA-05, CA-07, CA-08, CA-09, CA-12 |
| **CAs Excluidos**        | CA-06, CA-10, CA-11 (Lógica puramente Frontend)   |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-7                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: FastAPI + SQLAlchemy.
- [x] Seguridad: Validación de JWT y aislamiento de datos por `cliente_id`.
- [x] Estructura: Clean Architecture (Controllers -> Use Cases -> Repositories).

### Dependencias Críticas
> ⚠️ **ADVERTENCIA DE DEPENDENCIA (HU-08 / HU-05)**: Esta HU asume la existencia del `cliente_id` en el JWT y de los documentos clasificados. Al no haberse implementado formalmente la HU-08, el Backend debe mockear o implementar un JWT dummy para poder probar estos endpoints, o crear el esqueleto mínimo de seguridad (`@require_role`).

## Criterios de Aceptación Asignados al Backend

- **CA-01 & CA-08**: Proteger todas las rutas de `/api/cliente/*` para que requieran JWT. Validar que un cliente NO pueda consultar el ID de un documento que no le pertenezca (retornar 403 Forbidden).
- **CA-02**: Endpoint `GET /api/cliente/dashboard` que retorne métricas agregadas del cliente (conteo, tipos, último procesado, nuevos).
- **CA-03 & CA-12**: Endpoint `GET /api/cliente/carpetas` que construya un árbol JSON representando la jerarquía de carpetas del cliente.
- **CA-04**: Endpoint `GET /api/cliente/documentos` con paginación, filtros por `tipo_documento` y rango de fechas, y búsqueda de texto.
- **CA-05**: Endpoint `GET /api/cliente/documentos/{id}` que devuelva los metadatos y campos extraídos.
- **CA-07**: Endpoint `GET /api/cliente/documentos/{id}/descargar` para forzar la descarga (`Content-Disposition: attachment`).
- **CA-09**: Endpoint de dashboard debe incluir el conteo de documentos con estado "Pendiente Revisión Humana".

## Especificaciones Técnicas — Backend

### Endpoints REST a implementar
```python
# app/api/v1/endpoints/cliente.py
@router.get("/dashboard")
@router.get("/documentos")
@router.get("/documentos/{id}")
@router.get("/documentos/{id}/archivo")
@router.get("/documentos/{id}/descargar")
@router.get("/carpetas")
```

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El humano es solo un cartero.
3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."
5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación, pasa a modo `EXECUTION`.
6. **Al terminar la ejecución:** Genera un `walkthrough.md` y avisa al Humano.
