# Handoff — Frontend — HU-06
## Iteración: 1-DEV-HU-6

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_frontend_HU06_CA01-CA12.md`              |
| **Rol Destino**          | Agente Frontend                                   |
| **HU de Origen**         | HU-06 — Validación Humana                         |
| **CAs Asignados**        | CA-01 al CA-12                                    |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-6                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Frontend: React 18 + TS + Vite + Zustand + React Query + SCSS Modules.
- [x] Referencia Visual: `MOCKUP-HU-06-Validacion-Operario.md`. Theme DARK.

### Criterios de Aceptación Asignados al Frontend
- **CA-01 & CA-02**: Lista de pendientes con filtros, búsqueda, estado vacío, y columna "En cola" (colores semaforizados según CA-09).
- **CA-03 & CA-10**: Visor de documentos dividido 65% (PDF) / 35% (Datos). Cabecera del panel derecho con motivo de rechazo. Tarjetas de campos extraídos indicando confianza.
- **CA-04**: Controles de navegación y zoom en el visor.
- **CA-05**: Lógica condicional: si 1 error, activar "Corrección directa" (inputs editables).
- **CA-06**: Lógica condicional: si 2+ errores, activar modo "Enviar al agente" (textarea libre).
- **CA-07 & CA-05**: Estado UI de "⟳ En reprocesamiento...".
- **CA-08**: Botón y modal de confirmación para descartar.
- **CA-11**: Enlace para ver resumen rápido del lote desde el visor.
- **CA-12**: Recepción de nuevos documentos (SSE / polling / WebSocket) con toast notification discreta.

## Especificaciones Técnicas — Frontend
- **Theme**: Sigue las directrices del Mockup, que especifica un tema Dark (fondos `#0d1117`, bordes `#30363d`) propio de las pantallas de Operario.
- Usa los endpoints `/api/v1/pendientes/*`.
- Aprovecha Zustand para el estado global y React Query para el polling / invalidación de lista.

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El humano es solo un cartero.
3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Frontend.md`
4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Frontend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."
5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación, pasa a modo `EXECUTION`.
