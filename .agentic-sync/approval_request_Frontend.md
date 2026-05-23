# Solicitud de Revisión — Frontend HU-08

## Resumen del plan propuesto
Implementación de la HU-08 (Gestión de Roles y Autenticación del Sistema). Se construirán e integrarán:
1. **Páginas de Autenticación**: `LoginPage` para credenciales y `SeleccionClientePage` obligatoria para el rol Operario.
2. **Panel de Administración**: `GestionUsuariosPage` para la visualización y creación de usuarios.
3. **Seguridad y Enrutamiento**: Interceptores de Axios para el token JWT (renovado desde authStore en lugar del localStorage directamente) y manejo de errores 401. Componente `ProtectedRoute` para controlar acceso por rol, expiración de sesión por inactividad y asegurar contexto de cliente.
4. **Estado (Zustand)**: Implementación de `authStore.ts` para centralizar la sesión del usuario.

## Archivos a crear/modificar
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\pages\auth\LoginPage.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\pages\auth\SeleccionClientePage.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\pages\admin\GestionUsuariosPage.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\store\authStore.ts`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\services\api.ts`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\components\auth\ProtectedRoute.tsx`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\FrontEnd\src\App.tsx`

## Decisiones técnicas clave tomadas
- Uso de Zustand (`authStore`) como única fuente de verdad para el estado de autenticación y redirección.
- Implementación de expiración global de sesión monitoreando la actividad del usuario a nivel App.

## Riesgos identificados
- Las rutas del backend para autenticación deben coincidir con la integración. Hardcodearemos la base URL según Iteración 1 pero se necesitará validar el esquema JWT exacto devuelto por backend.

## Preguntas para el Arquitecto
Ninguna por ahora.
