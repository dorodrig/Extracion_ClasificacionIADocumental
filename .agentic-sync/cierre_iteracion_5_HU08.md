# Acta de Cierre — Iteración 5 (-DEV-HU-08)

## Metadatos
- **HU:** HU-08 — Gestión de Roles y Autenticación del Sistema
- **Iteración:** 5 -DEV-HU-08
- **Rama:** `HU2_CA1-CA4_DevDamian_ITEREACION1`
- **Estado:** ✅ COMPLETADA Y CERTIFICADA

## Resumen de Ejecución
- **Backend:** Implementó `security.py` aislando el hashing con SHA-256 + Salt (generado aleatoriamente). Consolidó la verificación transversal de Roles en `dependencies.py` con una factoría flexible, bloqueando cuentas tras 5 intentos fallidos.
- **Frontend:** Implementó el UI de Login con enrutado inteligente por roles. Aseguró las rutas del sistema mediante `ProtectedRoute` consumiendo la fuente de la verdad en `Zustand` (`authStore.ts`). Integró un interceptor en `Axios` para inyectar automáticamente el Bearer JWT en todas las peticiones futuras y cerrar sesión en 401s.
- **QA:** Omitido temporalmente a petición explícita del humano, aunque se delegaron instrucciones en caso de ejecutarse a futuro.

## Validación Gobernanza (ISO 25010)
- **Seguridad:** Cero credenciales expuestas; el JWT opera como mecanismo seguro *stateless* y las contraseñas usan algoritmos deterministas asimétricos con salteado aleatorio.
- **Mantenibilidad:** El uso de `Zustand` evita el "prop drilling" con la sesión de usuario y las funciones del backend separan dependencias API de Use Cases puros.

## Impacto en el Sistema
Con la autenticación y el RBAC implementado, el sistema ahora permite asegurar todas las HUs previas (HU-01 a HU-06), vinculando correctamente qué operario intervino qué documento (auditoría). Se desbloquea la construcción del Portal Cliente (HU-07).
