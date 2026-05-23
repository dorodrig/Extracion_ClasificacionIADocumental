# HU-08 — Gestión de Roles y Autenticación del Sistema

## Metadatos

| Campo                        | Valor                                                                |
| ---------------------------- | -------------------------------------------------------------------- |
| **ID**                       | HU-08                                                                |
| **Épica**                    | Seguridad y Control de Acceso                                        |
| **Esfuerzo Principal**       | 🖥️ Frontend UI (Login) + ⚙️ Backend (Auth, JWT, Roles)               |
| **Prioridad**                | 🔴 Alta — Bloqueante para todas las demás HU con interfaz de usuario |
| **Story Points Estimados**   | 8                                                                    |
| **Sprint Sugerido**          | Sprint 1                                                             |
| **Roles Involucrados**       | Administrador, Operario de Digitalización, Cliente Final             |

---

## Historia de Usuario

> **Como** Sistema GRM,
> **Quiero** controlar el acceso mediante autenticación por Cédula + contraseña (SHA-256) y gestionar tres roles diferenciados (Administrador, Operario de Digitalización, Cliente Final),
> **Para que** cada usuario acceda únicamente a las funcionalidades y datos que le corresponden según su rol, garantizando la seguridad y privacidad de la información de los clientes.

---

## Descripción Funcional

### Roles del sistema

| Rol                         | Acceso                                                                                   |
|-----------------------------|------------------------------------------------------------------------------------------|
| **Administrador**           | Panel completo: gestión de usuarios, clientes, reglas, logs, todos los lotes y reportes |
| **Operario de Digitalización** | Selección de cliente obligatoria al login → Reglas, Ingesta, Pendientes, Visor          |
| **Cliente Final**            | Portal de consulta exclusivo: solo sus documentos, solo lectura                          |

### Flujo de login diferenciado

**Cliente Final:**
```
[Pantalla Login] → Cédula + Contraseña → Dashboard del cliente
```

**Operario:**
```
[Pantalla Login] → Cédula + Contraseña → [Selección de Cliente OBLIGATORIA] → Panel del Operario
```

**Administrador:**
```
[Pantalla Login] → Cédula + Contraseña → Panel de Administración (acceso a todos los clientes)
```

### Seguridad del piloto
- Contraseñas almacenadas con hash SHA-256 + salt
- Sesiones gestionadas mediante JWT (JSON Web Token) con expiración de 8 horas (operario/admin) o 30 minutos de inactividad (cliente)
- Sin recuperación de contraseña por email en el piloto (el Admin resetea manualmente)

---

## Criterios de Aceptación (BDD / Gherkin)

### CA-01 — Pantalla de login unificada para todos los roles
```gherkin
Dado que cualquier usuario accede a la URL del sistema GRM
Cuando el sistema muestra la pantalla de login
Entonces presenta un formulario con dos campos: "Número de Cédula" (numérico) y "Contraseña" (oculta con toggle de visibilidad)
  Y muestra el logo de GRM y el nombre del sistema
  Y el botón "Ingresar" está deshabilitado si alguno de los dos campos está vacío
```

### CA-02 — Autenticación exitosa y redirección por rol
```gherkin
Dado que el usuario ingresa Cédula y Contraseña válidas
Cuando hace clic en "Ingresar"
Entonces el sistema valida las credenciales comparando el hash SHA-256 de la contraseña con el valor almacenado
  Y si las credenciales son válidas, genera un JWT con claims: usuario_id, rol, cliente_id (si aplica), exp
  Y redirige al usuario según su rol:
    | Rol                         | Redirección                                      |
    | Administrador               | /admin/dashboard                                  |
    | Operario de Digitalización  | /operario/seleccion-cliente                       |
    | Cliente Final               | /cliente/dashboard                                |
```

### CA-03 — Selección de cliente obligatoria para el Operario tras el login
```gherkin
Dado que el Operario de Digitalización ha sido autenticado exitosamente
Cuando el sistema redirige al paso "Selección de Cliente"
Entonces muestra una pantalla con un dropdown o lista de búsqueda de clientes disponibles
  Y el dropdown es de selección obligatoria (no tiene opción vacía ni "todos")
  Y el botón "Continuar" está deshabilitado hasta que el operario seleccione un cliente
  Y tras seleccionar el cliente y hacer clic en "Continuar", el sistema actualiza el contexto de sesión con el cliente_id seleccionado
  Y redirige al panel de trabajo del operario: /operario/reglas
```

### CA-04 — Manejo de credenciales incorrectas
```gherkin
Dado que un usuario ingresa Cédula o Contraseña incorrectas
Cuando hace clic en "Ingresar"
Entonces el sistema muestra el mensaje de error: "Cédula o contraseña incorrectos. Verifica tus datos."
  Y NO especifica cuál de los dos campos es incorrecto (por seguridad)
  Y incrementa el contador de intentos fallidos para esa cédula
  Y si el contador supera 5 intentos fallidos consecutivos, bloquea la cuenta por 15 minutos y muestra: "Cuenta bloqueada temporalmente por seguridad. Intenta nuevamente en 15 minutos."
```

### CA-05 — Protección de rutas por rol (Authorization)
```gherkin
Dado que un usuario autenticado intenta acceder a una ruta que no corresponde a su rol
Cuando el sistema recibe la petición con el JWT del usuario
Entonces valida el claim de rol en el JWT contra la ruta solicitada
  Y si el rol no tiene permiso para esa ruta, retorna HTTP 403 Forbidden
  Y redirige al usuario a su dashboard correspondiente según su rol
  Y registra el intento de acceso no autorizado en el log de seguridad
```

### CA-06 — Gestión de usuarios por el Administrador
```gherkin
Dado que el Administrador accede a la sección "Gestión de Usuarios"
Cuando el sistema carga la sección
Entonces muestra una tabla con todos los usuarios del sistema: nombre, cédula, rol, estado (activo/inactivo), fecha de creación
  Y permite al administrador crear nuevos usuarios con: nombre completo, cédula, rol, contraseña temporal
  Y permite activar/desactivar usuarios sin eliminarlos de la BD
  Y permite resetear la contraseña de un usuario (establece una contraseña temporal que el usuario debe cambiar en su próximo login)
```

### CA-07 — Creación de nuevo usuario por el Administrador
```gherkin
Dado que el Administrador hace clic en "Crear Usuario"
Cuando completa el formulario de nuevo usuario
Entonces los campos obligatorios son: nombre completo, número de cédula, rol (dropdown), contraseña temporal
  Y el sistema valida que la cédula no esté ya registrada en el sistema
  Y el sistema aplica hash SHA-256 + salt a la contraseña antes de almacenarla
  Y al guardar exitosamente, muestra confirmación: "Usuario {nombre} creado exitosamente con rol {rol}"
```

### CA-08 — Expiración de sesión por inactividad
```gherkin
Dado que un usuario (cualquier rol) tiene una sesión activa
Cuando no realiza ninguna acción durante el período de inactividad:
    | Rol              | Tiempo de inactividad máximo |
    | Cliente Final    | 30 minutos                   |
    | Operario         | 8 horas                      |
    | Administrador    | 8 horas                      |
Entonces el sistema invalida el JWT de la sesión
  Y redirige al usuario al login con el mensaje: "Tu sesión ha expirado. Inicia sesión nuevamente."
```

### CA-09 — Cambio de cliente activo por el Operario durante la sesión
```gherkin
Dado que el Operario está trabajando con un cliente seleccionado
Cuando hace clic en "Cambiar Cliente" en la cabecera del panel del operario
Entonces el sistema muestra el diálogo de selección de cliente (igual que en CA-03)
  Y si hay un proceso activo (lote en curso), muestra advertencia: "Cambiar de cliente cancelará el proceso actual. ¿Deseas continuar?"
  Y si el operario confirma, descarta el proceso activo y actualiza el cliente_id en la sesión
  Y si el operario cancela, mantiene el cliente actual sin cambios
```

### CA-10 — Gestión de clientes por el Administrador
```gherkin
Dado que el Administrador accede a la sección "Gestión de Clientes"
Cuando el sistema carga la sección
Entonces muestra una tabla con todos los clientes registrados: nombre de empresa/persona, NIT/CC, estado, fecha de registro
  Y permite crear nuevos clientes con: nombre, NIT o CC, datos de contacto, estado (activo/inactivo)
  Y permite asociar usuarios de tipo "Operario" a un cliente específico (relación N:N)
  Y permite ver el historial de lotes procesados por cliente
```

### CA-11 — Cierre de sesión explícito
```gherkin
Dado que el usuario está autenticado y hace clic en "Cerrar Sesión"
Cuando el sistema procesa la acción
Entonces invalida el JWT actual en el servidor (blacklist o revocación)
  Y limpia la sesión en el cliente (localStorage/sessionStorage)
  Y redirige al usuario a la pantalla de login
  Y muestra el mensaje: "Has cerrado sesión exitosamente."
```

### CA-12 — Hash SHA-256 de contraseñas con salt
```gherkin
Dado que el sistema almacena o verifica una contraseña de usuario
Cuando procesa la contraseña
Entonces genera un salt aleatorio único por usuario (mínimo 32 bytes)
  Y aplica SHA-256 al concatenado (contraseña + salt) antes de almacenar
  Y almacena salt y hash en campos separados de la tabla usuarios
  Y NUNCA almacena ni registra en logs la contraseña en texto plano
```

---

## Notas Técnicas

### Base de Datos (SQL Server)
```sql
CREATE TABLE usuarios (
    id              INT IDENTITY PRIMARY KEY,
    nombre_completo NVARCHAR(200) NOT NULL,
    cedula          NVARCHAR(20) NOT NULL UNIQUE,
    rol             NVARCHAR(50) NOT NULL,  -- 'admin' | 'operario' | 'cliente'
    password_hash   NVARCHAR(256) NOT NULL,
    password_salt   NVARCHAR(100) NOT NULL,
    activo          BIT DEFAULT 1,
    intentos_fallidos INT DEFAULT 0,
    bloqueado_hasta DATETIME,
    ultimo_acceso   DATETIME,
    created_at      DATETIME DEFAULT GETDATE()
);

CREATE TABLE clientes (
    id              INT IDENTITY PRIMARY KEY,
    nombre          NVARCHAR(200) NOT NULL,
    nit_cc          NVARCHAR(20) NOT NULL UNIQUE,
    activo          BIT DEFAULT 1,
    created_at      DATETIME DEFAULT GETDATE()
);

CREATE TABLE usuarios_clientes (
    usuario_id      INT FOREIGN KEY REFERENCES usuarios(id),
    cliente_id      INT FOREIGN KEY REFERENCES clientes(id),
    PRIMARY KEY (usuario_id, cliente_id)
);
```

### Dependencias
- **Bloquea a**: TODAS las demás HU (sin autenticación, el sistema no es operable)
- **Ninguna HU puede iniciar sin la autenticación implementada**
