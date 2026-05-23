# MOCKUP NARRATIVO — HU-08: Login y Autenticación por Roles
## Documento para Agente de Maquetación UI/UX

> **Instrucciones para el Agente de Maquetación**: Este documento describe las pantallas de autenticación del sistema GRM, incluyendo 3 flujos diferentes post-login según el rol del usuario. El login es la primera impresión del sistema — debe transmitir confianza, profesionalismo y modernidad. Toda la información está aquí.

---

## 1. Contexto de las Pantallas de Autenticación

- **Pantallas a diseñar**: 3 pantallas — Login principal, Selección de Cliente (solo Operario), y Pantalla de error/bloqueo
- **Usuarios**: Todos (Administrador, Operario de Digitalización, Cliente Final)
- **URL de acceso**: http://localhost:3000/ (redirige al login si no hay sesión activa)
- **Tema visual**: El login debe ser una pantalla impactante y memorable. Se recomienda un diseño con fondo oscuro (dark), elementos con glassmorphism (cards con fondo semi-transparente y blur), gradiente de fondo en tonos azul marino profundo. La pantalla del cliente puede ser más clara para diferenciarse del panel del operario.

---

## 2. Pantalla 1: Login Principal (Unificado para todos los roles)

### Descripción del fondo:
- Fondo: gradiente oscuro en diagonal. Colores: de #0a192f (azul marino muy oscuro) en la esquina superior izquierda a #1a1f2e (azul-negro) en la esquina inferior derecha
- Patrón sutil superpuesto: grid de puntos o líneas muy sutiles (10% de opacidad), animación suave de movimiento (parallax muy lento)
- Alternativa más simple: imagen de fondo con overlay oscuro (70% de opacidad negro) que muestre documentos financieros estilizados

### Contenido centrado — Card de login:
```
┌─────────────────────────────────────────────────────┐
│                                                      │
│   [LOGO GRM]                                         │
│   GRM Document Intelligence                          │
│   "Digitalización inteligente de documentos"         │
│                                                      │
│   ─────────────────────────────────────────          │
│                                                      │
│   Número de Cédula *                                 │
│   [ 1234567890__________________________ ]           │
│   (input numérico, sin decimales)                    │
│                                                      │
│   Contraseña *                                       │
│   [ ••••••••••••••••••••••••••••  [👁] ]            │
│   (el ícono 👁 alterna visibilidad de la contraseña) │
│                                                      │
│         [ Ingresar al Sistema → ]                    │
│         (botón azul eléctrico, ancho completo)       │
│                                                      │
│   ─────────────────────────────────────────          │
│   Sistema GRM v1.0 — Piloto                          │
│   © 2025 GRM. Acceso restringido.                   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Diseño de la card:**
- Fondo de la card: rgba(255, 255, 255, 0.05) — muy transparente (glassmorphism)
- Blur de fondo: backdrop-filter: blur(10px) — efecto vidrio esmerilado
- Borde: 1px sólido rgba(255, 255, 255, 0.1) — borde semi-transparente
- Border-radius: 16px
- Sombra: box-shadow 0 8px 32px rgba(0, 0, 0, 0.5)
- Ancho de la card: 420px (centrada horizontal y verticalmente en la pantalla)
- Padding interno: 40px

**Logo GRM:**
- Placeholder del logo: cuadrado de 60x60px con fondo azul eléctrico, texto "GRM" blanco centrado, border-radius: 12px
- Debajo del logo: "GRM Document Intelligence" en texto blanco, tamaño 20px, SemiBold
- Subtítulo: "Digitalización inteligente de documentos" en gris claro (#8b949e), tamaño 13px

**Inputs:**
- Fondo: rgba(255, 255, 255, 0.07)
- Borde en reposo: 1px rgba(255, 255, 255, 0.15)
- Borde en foco: 1px #2f81f7 + glow suave (box-shadow 0 0 0 3px rgba(47, 129, 247, 0.2))
- Texto: blanco #e6edf3
- Placeholder: gris #8b949e
- Border-radius: 8px
- Padding: 12px 16px
- Altura: 48px

**Botón "Ingresar":**
- Fondo: #2f81f7 (azul eléctrico)
- Hover: #388bfd + ligero scale (1.02) con transición 0.2s
- Active (click): #1f6feb + scale (0.98)
- Texto: blanco, SemiBold, 15px
- Width: 100% (ancho completo del formulario)
- Height: 48px
- Border-radius: 8px

**Estado con spinner (al hacer clic):**
- El botón muestra un spinner circular blanco mientras procesa (durante 1–2 segundos)
- El botón se deshabilita durante el procesamiento
- Si falla: el botón vuelve a estado normal

---

## 3. Estado de Error en el Login

### Error de credenciales incorrectas:

Debajo del botón "Ingresar", aparece un bloque de error con animación shake:
```
┌─────────────────────────────────────────────────────┐
│  ✗ Cédula o contraseña incorrectos.                  │
│    Verifica tus datos e intenta nuevamente.          │
│    Intentos restantes: 4                             │
└─────────────────────────────────────────────────────┘
```
- Fondo: rgba(248, 81, 73, 0.1) (rojo muy transparente)
- Borde izquierdo: 3px sólido #f85149 (rojo)
- Border-radius: 6px
- Texto: #f85149

### Estado de cuenta bloqueada (5 intentos fallidos):

El formulario se reemplaza por:
```
┌─────────────────────────────────────────────────────┐
│  🔒 Cuenta bloqueada temporalmente                   │
│                                                      │
│  Has superado el límite de intentos fallidos.        │
│  Tu cuenta estará desbloqueada en:                   │
│                                                      │
│          14:58  (contador regresivo)                 │
│                                                      │
│  Si crees que esto es un error, contacta al          │
│  administrador del sistema.                          │
└─────────────────────────────────────────────────────┘
```
- Ícono 🔒 grande (48px) centrado, color ámbar
- Contador regresivo en formato MM:SS, tamaño grande (36px), blanco
- El formulario de login está oculto (no visible) mientras la cuenta está bloqueada
- Cuando el contador llega a 00:00, el formulario vuelve a aparecer con animación fade-in

---

## 4. Estado de Éxito — Animación de Transición post-Login

Al autenticarse exitosamente:
1. El botón "Ingresar" muestra brevemente un ícono ✓ verde
2. La card hace un fade-out suave (0.3s)
3. Aparece brevemente: "Bienvenido, [NOMBRE COMPLETO]" centrado en pantalla (texto blanco grande)
4. Redirige a la pantalla correspondiente según el rol

---

## 5. Pantalla 2: Selección de Cliente (Solo Operario)

Esta pantalla aparece **únicamente para el rol Operario**, después del login exitoso, antes de llegar al panel de trabajo.

### Layout:
```
┌─────────────────────────────────────────────────────┐
│  [LOGO GRM]  GRM Document Intelligence              │
│  ─────────────────────────────────────              │
│                                                      │
│  Hola, [NOMBRE DEL OPERARIO] 👋                      │
│  Selecciona el cliente con el que trabajarás hoy     │
│                                                      │
│  Cliente *                                           │
│  [                                              ▼ ]  │
│  (Dropdown de búsqueda con los clientes activos)     │
│                                                      │
│  [Al seleccionar, muestra preview:]                  │
│  ┌─────────────────────────────────────┐            │
│  │  ✓ BANCORP                          │            │
│  │  NIT: 830.001.234-5                │            │
│  │  Documentos procesados: 47          │            │
│  │  Última actividad: hace 2 días     │            │
│  └─────────────────────────────────────┘            │
│                                                      │
│  [ Continuar → ]  (botón azul eléctrico, ancho 100%)│
│                                                      │
│  [← Cerrar Sesión]  (link pequeño, gris, abajo)     │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Diseño:**
- Misma card glassmorphism del login, mismo fondo de pantalla
- El dropdown de cliente es un select con búsqueda integrada (input + lista desplegable)
- La lista muestra: nombre del cliente + NIT/CC en gris debajo
- Al seleccionar un cliente, aparece la card de preview del cliente con animación fade-in

**El botón "Continuar":**
- Deshabilitado (gris, cursor not-allowed) hasta que se seleccione un cliente
- Al habilitarse: transición suave de color gris → azul eléctrico (0.3s)

**Card de preview del cliente seleccionado:**
- Fondo: rgba(47, 129, 247, 0.1) — azul muy transparente
- Borde izquierdo: 3px sólido #2f81f7
- Muestra: nombre del cliente (texto grande blanco), NIT, total documentos, última actividad

---

## 6. Pantalla 3: Redirección por Rol (Pantallas de destino post-login)

| Rol                          | Pantalla de destino                          | URL              |
|------------------------------|----------------------------------------------|------------------|
| Administrador                | Panel de Administración (dashboard completo) | /admin/dashboard |
| Operario (tras elegir cliente)| Panel de Trabajo del Operario               | /operario/reglas |
| Cliente Final                | Portal de Consulta del Cliente               | /cliente/inicio  |

---

## 7. Comportamiento Responsivo

La pantalla de login está diseñada para escritorio (1024px+). Sin embargo:
- En pantallas de 768px–1023px (tablets): la card reduce su ancho a 90% de la pantalla
- En pantallas < 768px: la card ocupa el 95% del ancho, padding interno reducido a 24px

---

## 8. Especificaciones de Animaciones

| Animación                                | Descripción                                                     |
|------------------------------------------|-----------------------------------------------------------------|
| Fondo de la página                       | Gradiente con ligero movimiento lento (animación CSS 30s loop)  |
| Error de login                           | Animación shake horizontal (±5px, 3 ciclos, 0.5s total)         |
| Aparición de la card de preview (cliente)| Fade-in + slide-up (translateY de 10px a 0, 200ms)             |
| Botón "Ingresar" en clic                 | Scale 0.98 + 0.1s, luego vuelve con spring effect               |
| Contador de bloqueo                      | Actualización cada segundo, color cambia a rojo en últimos 30s  |
| Transición de login exitoso              | Fade-out de la card (300ms), aparece mensaje de bienvenida      |

---

## 9. Especificaciones de Colores y Tipografía

| Elemento                             | Especificación                                                |
|--------------------------------------|---------------------------------------------------------------|
| Fondo de pantalla                    | Gradiente: #0a192f → #1a1f2e (diagonal 135deg)               |
| Card glassmorphism (fondo)           | rgba(255, 255, 255, 0.05) + backdrop-filter blur(10px)        |
| Card border                          | 1px solid rgba(255, 255, 255, 0.1)                            |
| Card shadow                          | 0 8px 32px rgba(0, 0, 0, 0.5)                                |
| Fuente principal                     | Inter (Google Fonts), pesos 400 y 600                         |
| Título del sistema                   | Blanco #ffffff, 20px, SemiBold                               |
| Subtítulo del sistema                | #8b949e, 13px, Regular                                        |
| Labels de inputs                     | #c9d1d9, 13px, SemiBold, uppercase                           |
| Inputs (fondo)                       | rgba(255, 255, 255, 0.07)                                     |
| Inputs (texto)                       | #e6edf3                                                       |
| Inputs (placeholder)                 | #8b949e                                                       |
| Inputs (borde foco)                  | #2f81f7 + glow                                                |
| Botón principal                      | Fondo #2f81f7, texto blanco, SemiBold                        |
| Botón deshabilitado                  | Fondo #21262d, texto #484f58, cursor not-allowed              |
| Texto de versión/copyright           | #484f58, 11px                                                 |
| Spinner en botón                     | Blanco, border-width 2px, animación rotation 1s linear        |
