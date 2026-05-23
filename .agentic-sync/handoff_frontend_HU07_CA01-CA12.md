# Handoff — Frontend — HU-07
## Iteración: 1-DEV-HU-7

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_frontend_HU07_CA01-CA12.md`              |
| **Rol Destino**          | Agente Frontend                                   |
| **HU de Origen**         | HU-07 — Portal Web de Consulta para Cliente Final |
| **CAs Asignados**        | CA-01 al CA-12                                    |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-7                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Frontend: React 18 + TS + Vite + Zustand + React Query + Axios.
- [x] Estilos: SASS/SCSS Modules. Light Theme / Corporativo (azul, blanco, gris).
- [x] Maquetación: Guiada por `MOCKUP-HU-07-Portal-Cliente.md`.

## Criterios de Aceptación Asignados al Frontend

- **CA-01**: Pantalla de Login y redirección al Dashboard.
- **CA-02**: Maquetar Dashboard con 4 tarjetas de métricas y la tabla "Últimos documentos".
- **CA-03**: Maquetar Explorador de Documentos. Árbol de carpetas colapsable a la izquierda, contenido a la derecha.
- **CA-04**: Tabla paginada de todos los documentos con select de tipo, input date range y barra de búsqueda.
- **CA-05 & CA-06**: Visor de documento (PDF o IMG renderizado). Panel lateral con metadatos solo lectura. Controles de Zoom y Paginación.
- **CA-07**: Botón "Descargar" en el visor.
- **CA-08**: (Manejo de errores) Si alguna API retorna 403, mostrar pantalla "Acceso Denegado".
- **CA-09**: Banner azul informativo de "Documentos en proceso" en el Dashboard.
- **CA-10**: Inactividad de sesión. Timer local o verificación de token expirado (30 mins). Redirigir a Login.
- **CA-11**: Responsive Design. Uso de Mixins SCSS para medias queries (Desktop y Tablet).
- **CA-12**: Renderizar un mini-árbol visual en el panel lateral del visor para indicar la "Ubicación" del archivo.

## Especificaciones Técnicas — Frontend

- **Fuente de Verdad Visual**: Lee `C:\zData\ExtracionDatosIA\HU\HU-Mockups\MOCKUP-HU-07-Portal-Cliente.md`. **DEBES MAQUETAR EXACTAMENTE COMO SE INDICA ALLÍ**.
- **Manejo de Estado**: Usa `React Query` para todo el data fetching de los endpoints `/api/cliente/*`. Usa `Zustand` para el estado global (ej. sesión, documento abierto en visor).
- **Styling**: Crea variables SCSS para la paleta de colores: `#1e3a5f` (azul profundo), `#2f81f7` (azul highlight), `#f8f9fa` (gris fondo).

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
6. **Al terminar la ejecución:** Genera un `walkthrough.md` y avisa al Humano.
