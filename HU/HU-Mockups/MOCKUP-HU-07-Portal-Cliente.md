# MOCKUP NARRATIVO — HU-07: Portal Web de Consulta para Cliente Final
## Documento para Agente de Maquetación UI/UX

> **Instrucciones para el Agente de Maquetación**: Este documento describe el portal web que los clientes finales de GRM usarán para consultar sus documentos digitalizados. Es la cara pública del sistema — el diseño debe ser limpio, confiable y accesible. Toda la información necesaria está aquí.

---

## 1. Contexto de la Pantalla

- **Nombre del portal**: "Portal de Documentos — GRM"
- **Usuario**: Cliente Final (empresa o persona que contrató el servicio de digitalización)
- **Acceso**: URL local (ej: http://localhost:3000/cliente) — ejecución web local
- **Propósito**: Permitir al cliente final consultar, visualizar y descargar sus documentos clasificados. Es una interfaz de **solo lectura**. No puede modificar nada.
- **Tema visual**: A diferencia del panel del operario (muy oscuro), el portal del cliente puede tener un tema más limpio y profesional. Se recomienda un diseño claro (light) o dark suave (no tan oscuro como el panel operario). Paleta azul corporativo + blanco + grises claros. Sensación de confianza y profesionalismo bancario/financiero.

---

## 2. Layout General del Portal

```
┌─────────────────────────────────────────────────────────────────┐
│  CABECERA DEL PORTAL                                            │
│  [Logo GRM]   "Portal de Documentos"   "Bienvenido, BANCORP" [Salir]│
├──────────────┬──────────────────────────────────────────────────┤
│  MENÚ        │                                                   │
│  LATERAL     │   ÁREA DE CONTENIDO PRINCIPAL                     │
│  (izquierda) │                                                   │
│              │                                                   │
│  📊 Inicio   │                                                   │
│  📁 Mis Docs │                                                   │
│  🔍 Buscar   │                                                   │
│  ⬇ Descargas │                                                   │
└──────────────┴──────────────────────────────────────────────────┘
```

**Cabecera:**
- Logo GRM a la izquierda
- Centro: "Portal de Documentos GRM"
- Derecha: "Bienvenido, [NOMBRE DEL CLIENTE]" + botón [Cerrar Sesión]
- Fondo de cabecera: azul corporativo profundo (#1e3a5f) con texto blanco

**Menú lateral:**
- Fondo blanco o gris muy claro (#f8f9fa)
- Ítems con ícono + texto
- Ítem activo resaltado con barra izquierda azul y fondo azul muy claro

---

## 3. Pantalla: Dashboard / Inicio

### Tarjetas de métricas (fila superior):
```
┌─────────────────────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │     47       │  │      5       │  │      3       │  │  22 Mar 2025 │  │
│  │  Total       │  │  Pagarés     │  │  Cédulas     │  │  Último      │  │
│  │  Documentos  │  │              │  │              │  │  Procesamiento│  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```
- Cada tarjeta: fondo blanco, borde redondeado (12px), sombra suave
- Número grande centrado (azul corporativo, tamaño 36px, SemiBold)
- Etiqueta debajo del número (gris oscuro, 13px)
- Las primeras 3 tarjetas tienen un ícono de color en la esquina superior derecha

### Sección "Últimos documentos procesados":
```
┌─────────────────────────────────────────────────────────────────┐
│  ÚLTIMOS DOCUMENTOS PROCESADOS                [Ver todos →]      │
├─────────────────────────────────────────────────────────────────┤
│  📄 pagare_001.pdf    │ Pagaré  │ CC123456789  │ 22/03/2025  │ [Ver]│
│  📄 cedula_maria.jpg  │ Cédula  │ CC987654321  │ 22/03/2025  │ [Ver]│
│  📄 endoso_carlos.pdf │ Endoso  │ CC111222333  │ 22/03/2025  │ [Ver]│
└─────────────────────────────────────────────────────────────────┘
```
- Tabla simple, sin filas alternadas oscuras (fondo blanco o muy gris claro)
- Botón [Ver] azul outline pequeño que abre el visor

### Sección "Documentos en proceso" (si aplica):
Si hay documentos pendientes de revisión por el operario:
```
┌─────────────────────────────────────────────────────────────────┐
│  ⏳ En revisión por el equipo de digitalización                  │
│  2 documento(s) están siendo revisados. Estarán disponibles      │
│  en su portal en breve.                                          │
└─────────────────────────────────────────────────────────────────┘
```
- Fondo azul muy claro (#e8f4fd), borde izquierdo azul (4px)
- Ícono ⏳ + texto informativo
- Sin detalle de los documentos pendientes (el cliente no puede verlos)

---

## 4. Pantalla: Mis Documentos (Lista completa)

### Barra de filtros:
```
[🔍 Buscar por CC, nombre, archivo...]  [Tipo ▼]  [Desde]─[Hasta]  [✕ Limpiar]
```

### Tabla de documentos:
```
┌───────────────────────────────────────────────────────────────────────────────┐
│  Nombre de archivo    │ Tipo          │ Cédula       │ Nombre        │ Fecha       │ Acción  │
├───────────────────────────────────────────────────────────────────────────────┤
│  📄 pagare_001.pdf    │ 📋 Pagaré     │ 123456789    │ David Rodríguez│ 22/03/2025  │ [Ver]   │
│  📄 cedula_maria.jpg  │ 🪪 Cédula     │ 987654321    │ María García  │ 22/03/2025  │ [Ver]   │
│  📄 endoso_carlos.pdf │ 📝 Endoso     │ 111222333    │ Carlos López  │ 22/03/2025  │ [Ver]   │
│  📄 carta_trabajo.pdf │ 📄 Otro       │ 555666777    │ Pedro Martínez│ 21/03/2025  │ [Ver]   │
└───────────────────────────────────────────────────────────────────────────────┘
  Mostrando 4 de 47 documentos  [< 1 2 3 ... 5 >]
```

**Diseño de la tabla:**
- Fondo filas blanco y gris muy claro alternado (#ffffff y #f8f9fa)
- Encabezados de columna: fondo gris claro (#f1f3f5), texto gris oscuro, semibold
- Badge de tipo: chip coloreado con ícono
  - 📋 Pagaré: chip azul claro
  - 🪪 Cédula: chip verde claro
  - 📝 Endoso: chip naranja claro
  - 📄 Otro: chip gris

---

## 5. Pantalla: Explorador de Carpetas (Árbol de Documentos)

### Layout del explorador:
```
┌──────────────────────────┬──────────────────────────────────────┐
│  ÁRBOL DE CARPETAS       │  CONTENIDO DE LA CARPETA SELECCIONADA│
│  (panel izquierdo ~35%)  │  (panel derecho ~65%)                │
├──────────────────────────┼──────────────────────────────────────┤
│                          │                                       │
│  📁 CC123456789          │  [Cuando se selecciona una carpeta,   │
│    ▼ DAVID_RODRIGUEZ     │   muestra los archivos dentro]        │
│      📁 PAGARE           │                                       │
│        📄 pagare_001.pdf │  Si se selecciona un archivo,         │
│        📄 pagare_002.pdf │  muestra el visor de documento        │
│      📁 ENDOSO           │                                       │
│        📄 endoso_001.pdf │                                       │
│  📁 CC987654321          │                                       │
│    ► MARIA_GARCIA        │                                       │
│  📁 CC111222333          │                                       │
│    ► CARLOS_LOPEZ        │                                       │
│                          │                                       │
└──────────────────────────┴──────────────────────────────────────┘
```

**Panel izquierdo — Árbol:**
- Fondo blanco o gris muy claro
- Nodos expandibles/colapsables con ícono ▼ / ►
- Íconos de carpeta 📁 (azul) y archivo 📄 (gris)
- Ítem seleccionado: fondo azul muy claro (#e8f4fd), texto azul corporativo
- Animación suave al expandir/colapsar ramas (transición de altura 200ms)

**Panel derecho — Contenido:**
- Cuando se selecciona una carpeta: muestra grid de archivos en la carpeta (cards pequeñas con ícono y nombre)
- Cuando se selecciona un archivo: abre el visor de documento en el mismo panel derecho

---

## 6. Vista: Visor de Documentos del Cliente (Solo Lectura)

Al hacer clic en **[Ver]** en cualquier documento, la pantalla cambia al visor:

### Layout del visor:
```
┌─────────────────────────────────────────────────────────────────┐
│  ← Volver a Mis Documentos  │  📄 pagare_001.pdf  │  [⬇ Descargar]│
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────┬──────────────────────────┐  │
│  │                                │  INFORMACIÓN DEL         │  │
│  │   DOCUMENTO RENDERIZADO         │  DOCUMENTO               │  │
│  │   (PDF o imagen, panel izq.)   │                          │  │
│  │                                │  Tipo: Pagaré            │  │
│  │   [Controles de navegación]    │  CC: 123456789           │  │
│  │   ← Pág 1 de 3 →              │  Nombre: David Rodríguez │  │
│  │   [🔍-] 100% [🔍+]            │  Fecha: 2025-03-22       │  │
│  │                                │  (todos los campos en    │  │
│  │                                │   modo solo lectura)     │  │
│  │                                │                          │  │
│  │                                │  UBICACIÓN:              │  │
│  │                                │  📁 CC123456789          │  │
│  │                                │   └─ DAVID_RODRIGUEZ     │  │
│  │                                │      └─ PAGARE           │  │
│  │                                │         └─ pagare_001.pdf│  │
│  └────────────────────────────────┴──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Panel izquierdo (65%)** — Visor del documento:
- El documento se renderiza en un área con fondo blanco para simular papel
- Bordes sutiles y sombra alrededor del documento
- Controles de zoom y paginación encima del documento

**Panel derecho (35%)** — Información del documento:
- Fondo gris muy claro (#f8f9fa)
- Cada campo: etiqueta gris pequeño + valor texto normal
- Todos los campos en modo NO editable (sin inputs, solo texto)
- Sección "Ubicación" con mini árbol de carpetas para contexto visual
- Botón **[⬇ Descargar]** prominente en la cabecera del visor (azul corporativo)

---

## 7. Especificaciones de Colores y Tipografía

| Elemento                        | Especificación                                           |
|---------------------------------|----------------------------------------------------------|
| Tema general                    | Light mode (fondo blanco/gris claro)                    |
| Fuente principal                | Inter (Google Fonts), Regular 400 / SemiBold 600        |
| Cabecera del portal             | Fondo #1e3a5f (azul profundo), texto blanco             |
| Menú lateral                    | Fondo #f8f9fa, texto #495057                            |
| Ítem de menú activo             | Borde izq. #2f81f7 (4px), fondo #e8f4fd                 |
| Tarjetas de métricas            | Fondo #ffffff, sombra 0px 2px 8px rgba(0,0,0,0.08)     |
| Número en tarjeta               | #1e3a5f (azul profundo), tamaño 36px                    |
| Filas de tabla (par)            | Fondo #ffffff                                           |
| Filas de tabla (impar)          | Fondo #f8f9fa                                           |
| Encabezados de tabla            | Fondo #f1f3f5, texto #495057, SemiBold                  |
| Botón [Ver]                     | Outline azul #2f81f7, texto azul, hover fill azul       |
| Botón [Descargar]               | Fill #1e3a5f (azul profundo), texto blanco              |
| Árbol de carpetas — seleccionado| Fondo #e8f4fd, texto #2f81f7                            |
| Panel derecho del visor         | Fondo #f8f9fa                                           |
| Documento renderizado (fondo)   | Blanco #ffffff con sombra box-shadow                    |
| Banner "En revisión"            | Fondo #e8f4fd, borde izq. #2f81f7                       |
| Badge tipo Pagaré               | Fondo #dbeafe, texto #1d4ed8                            |
| Badge tipo Cédula               | Fondo #dcfce7, texto #166534                            |
| Badge tipo Endoso               | Fondo #fff7ed, texto #9a3412                            |
| Badge tipo Otro                 | Fondo #f3f4f6, texto #374151                            |
