# Handoff — Frontend — HU-08
## Iteración: 5 -DEV-HU-08

| Campo                    | Valor                                                        |
|--------------------------|--------------------------------------------------------------|
| **Archivo**              | `handoff_frontend_HU08_CA01-CA08.md`                         |
| **Rol Destino**          | Agente Frontend                                              |
| **HU de Origen**         | HU-08 — Gestión de Roles y Autenticación del Sistema         |
| **CAs Asignados**        | CA-01 a CA-08                                                |
| **CAs Excluidos**        | CA-09 a CA-12                                                |
| **Rama Git**             | `HU2_CA1-CA4_DevDamian_ITEREACION1`                          |
| **Iteración**            | 5 -DEV-HU-08                                                 |
| **Fecha de Generación**  | 2026-05-23                                                   |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)                        |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md                          |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Frontend: React 18 + TypeScript + Vite 5
- [x] Estado y HTTP: Zustand + Axios (Interceptor para JWT)
- [x] Rutas: React Router DOM (Manejo de rutas protegidas)

### Patrón Arquitectónico
- [x] Interceptor de Axios para inyectar automáticamente el JWT Bearer token en todas las llamadas API seguras.
- [x] Contexto / Zustand para mantener la sesión global (`useAuthStore`).

## Criterios de Aceptación a Implementar (Frontend)
- **CA-01:** UI de la Pantalla de Login. Cédula + Contraseña con toggle de visibilidad. Validación de inputs no vacíos.
- **CA-02, CA-05:** Captura del JWT, guardado seguro (localStorage/sessionStorage), y redirección basada en roles (`/admin/dashboard`, `/operario/seleccion-cliente`, `/cliente/dashboard`).
- **CA-03:** Pantalla de Selección de Cliente obligatoria para el rol Operario (impide navegar a `/operario/reglas` sin un cliente en contexto).
- **CA-04:** Mostrar mensajes de error de backend en UI, incluyendo bloqueo de cuenta.
- **CA-06, CA-07:** Panel de gestión de usuarios para el Admin (Lista y Formulario de creación).
- **CA-08:** Expiración por inactividad. Implementar temporizador en frontend que al detectar X tiempo sin interacción invalide sesión y redirija al login.

## Especificaciones Técnicas — Frontend

### Estructura de Directorios
Archivos principales a modificar o crear:
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\pages\auth\LoginPage.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\pages\auth\SeleccionClientePage.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\pages\admin\GestionUsuariosPage.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\store\authStore.ts`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\services\api.ts` (Configurar Axios Interceptors)
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\auth\ProtectedRoute.tsx`

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El humano es solo un cartero.
3. **Guarda tu solicitud en `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Frontend.md`**
4. **Dile al Humano:** "He dejado mi solicitud de revisión en la ruta acordada: C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Frontend.md Llévasela al Arquitecto Líder y regrésame su respuesta."
5. Solo tras la aprobación del Arquitecto, pasa a modo `EXECUTION`, codifica y haz git commit / push.
