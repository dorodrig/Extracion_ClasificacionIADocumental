# MOCKUP NARRATIVO — HU-01: Configuración y Gestión de Reglas de Trabajo
## Documento para Agente de Maquetación UI/UX

> **Instrucciones para el Agente de Maquetación**: Este documento describe con precisión quirúrgica el comportamiento, estructura visual, estados y flujos de interacción de la pantalla de Reglas de Trabajo del sistema GRM. Lee cada sección completa antes de generar el mockup. No hagas preguntas; toda la información está aquí.

---

## 1. Contexto de la Pantalla

- **Nombre de la pantalla**: "Reglas de Trabajo"
- **Ruta de navegación**: Menú lateral → "Reglas de Trabajo"
- **Usuarios que acceden**: Operario de Digitalización (ya autenticado y con un cliente seleccionado activo)
- **Propósito**: Esta pantalla permite al operario gestionar las reglas de configuración del proceso de extracción para el cliente activo. Es la pantalla de configuración central antes de iniciar cualquier procesamiento.
- **Tema visual**: Aplicación web de escritorio local. Diseño oscuro (dark mode) profesional, colores corporativos sobrios (azul oscuro, grises, acentos en azul eléctrico o verde teal). Sin elementos decorativos excesivos. UX empresarial/industrial.

---

## 2. Layout General de la Pantalla

### Estructura de la página:
```
┌─────────────────────────────────────────────────────────────────┐
│  CABECERA (Header Global)                                        │
│  Logo GRM | "Operario: Juan Pérez" | "Cliente Activo: BANCORP"  │
│  [Cambiar Cliente] [Cerrar Sesión]                               │
├──────────────┬──────────────────────────────────────────────────┤
│  MENÚ        │  ÁREA DE CONTENIDO PRINCIPAL                      │
│  LATERAL     │                                                   │
│  (izquierda) │  Breadcrumb: Inicio > Reglas de Trabajo           │
│              │                                                   │
│  • Inicio    │  Título: "Reglas de Trabajo — Cliente: BANCORP"   │
│  • Reglas ◄  │                                                   │
│  • Ingresar  │  [ESTADO A: Sin reglas]  O  [ESTADO B: Con reglas]│
│  • Pendientes│                                                   │
│  • Historial │                                                   │
└──────────────┴──────────────────────────────────────────────────┘
```

---

## 3. Estado A — Cliente sin reglas previas

### Descripción visual:
- Área de contenido muestra un ícono grande centrado (documento + engranaje, estilo outline/lineal)
- Debajo del ícono: Título "Sin reglas configuradas" (texto gris claro, tamaño H3)
- Subtítulo: "Este cliente no tiene reglas de trabajo. Crea la primera para comenzar el proceso."
- Botón principal centrado: **[+ Crear Primera Regla]** (botón azul eléctrico, tamaño grande, ancho 280px)
- Al hacer clic en el botón, la pantalla hace scroll hacia abajo o abre el formulario en la misma página (no modal)

---

## 4. Estado B — Cliente con reglas existentes

### Cabecera de sección (parte superior del área de contenido):
```
"Reglas de Trabajo — Cliente: BANCORP"          [+ Nueva Regla]
```
El botón **[+ Nueva Regla]** está en la esquina superior derecha. Es azul eléctrico con ícono de "+".

### Tabla de reglas existentes:
Tabla con las siguientes columnas:

| # | Columna           | Tipo              | Descripción                                                          |
|---|-------------------|-------------------|----------------------------------------------------------------------|
| 1 | Nombre de Regla   | Texto + badge     | Nombre de la regla. Badge "v2" (versión) en gris oscuro a la derecha |
| 2 | Tipo de Documento | Texto             | Ej: "Pagaré", "Cédula de Ciudadanía", "Endoso"                      |
| 3 | Modo de Entrada   | Badge con ícono   | "📄 Carpeta" o "🖨 Escáner"                                         |
| 4 | Última Modificación | Fecha           | Formato: "Hace 2 días" (hover muestra fecha exacta)                  |
| 5 | Acciones          | Botones           | Tres botones por fila (ver detalle más abajo)                        |

**Botones de acción por fila:**
- **[▶ Iniciar Proceso]**: Botón verde (outline o filled) — inicia el proceso con esa regla
- **[✏ Editar]**: Botón gris oscuro (outline) — abre el formulario con los datos de la regla
- **[👁 Ver Detalle]**: Botón transparente con ícono — abre un panel lateral (drawer) solo lectura

**Diseño de la tabla:**
- Filas con fondo alterno (dark: #1a1f2e y #151a27)
- Fila hover: resaltado sutil en azul oscuro semi-transparente
- Tabla con borde exterior redondeado (border-radius: 8px)
- Máximo 10 filas visibles, paginación simple debajo

---

## 5. Formulario de Creación / Edición de Regla

El formulario aparece debajo de la tabla (en Estado B) o es el único elemento de la pantalla (en Estado A). NO es un modal.

### Sección 1: Información General
```
┌─────────────────────────────────────────────────┐
│  Nombre de la Regla *                            │
│  [________________________]  Ej: "Pagarés Q1 2025" │
│                                                  │
│  Tipo de Documento *                             │
│  [ Dropdown: Pagaré / Endoso / Cédula / Otro ] ▼│
│                                                  │
│  Modo de Entrada *                               │
│  ⦿ 🖨 Escáner (por lotes)                        │
│  ○  📁 Carpeta local (uno a uno)                 │
└─────────────────────────────────────────────────┘
```

### Sección 2: Campos a Extraer
```
┌─────────────────────────────────────────────────────────────────┐
│  CAMPOS A EXTRAER *                              [+ Agregar Campo]│
├──────────────────────┬─────────────────┬────────────────────────┤
│  Nombre del campo    │  Tipo de dato   │  Obligatorio   │  Eliminar│
├──────────────────────┼─────────────────┼────────────────┼────────┤
│  [Número de Cédula_] │ [Identificación▼]│    [✓]         │  [🗑]  │
├──────────────────────┼─────────────────┼────────────────┼────────┤
│  [Nombre Completo__] │ [Texto_________▼]│    [✓]         │  [🗑]  │
├──────────────────────┼─────────────────┼────────────────┼────────┤
│  [Fecha del Pagaré_] │ [Fecha_________▼]│    [ ]         │  [🗑]  │
└──────────────────────┴─────────────────┴────────────────┴────────┘
  Nota: Mínimo 1 campo requerido
```
- Tipos disponibles en el dropdown: Texto, Número, Fecha, Identificación
- El checkbox "Obligatorio" es un toggle visual (encendido = azul, apagado = gris)
- El botón "Agregar Campo" está en la esquina superior derecha de esta sección
- Al agregar una nueva fila, aparece con animación suave (fade in + slide down)

### Sección 3: Patrón de Carpeta de Salida
```
┌─────────────────────────────────────────────────────────────────┐
│  PATRÓN DE CARPETA DE SALIDA *                                   │
│                                                                  │
│  Variables disponibles: [CC] [NOMBRE_COMPLETO] [TIPO_DOCUMENTO] [NOMBRE_ARCHIVO]│
│  (chips clickeables que insertan la variable en el campo)        │
│                                                                  │
│  Patrón: [/{CC}/{NOMBRE_COMPLETO}/{TIPO_DOCUMENTO}/{NOMBRE_ARCHIVO}]│
│                                                                  │
│  Vista previa en tiempo real:                                    │
│  📁 /CC123456789/DAVID_RODRIGUEZ/PAGARE/pagare_001.pdf           │
│     (gris claro, fuente monospace, actualización en tiempo real) │
└─────────────────────────────────────────────────────────────────┘
```

### Sección 4: Configuración OCR (Solo lectura)
```
┌─────────────────────────────────────────────────────────────────┐
│  CONFIGURACIÓN OCR                                               │
│                                                                  │
│  Umbral de Confianza OCR:  [████████████████████] 95%           │
│                            (barra de progreso bloqueada, no editable)│
│  ℹ El sistema descartará campos con confianza inferior al 95%.  │
│    Este valor es estándar del proceso GRM.                       │
└─────────────────────────────────────────────────────────────────┘
```

### Pie del formulario (botones de acción)
```
                               [Cancelar]  [Guardar Regla ▶]
```
- **[Cancelar]**: Botón gris outline — descarta los cambios y regresa a la tabla
- **[Guardar Regla ▶]**: Botón azul eléctrico filled — deshabilitado si hay campos obligatorios vacíos
- Al hacer hover sobre "Guardar" con campos vacíos: tooltip "Completa los campos obligatorios marcados con *"

---

## 6. Panel Lateral de Detalle (Drawer — Solo Lectura)

Al hacer clic en "Ver Detalle", se abre un panel deslizante desde la derecha (width: 480px) sin salir de la pantalla:

- Cabecera del drawer: nombre de la regla + badge de versión + botón [✕ Cerrar]
- Muestra TODOS los campos de la regla en modo solo lectura
- Formato: etiqueta (gris claro, tamaño pequeño) + valor (blanco, tamaño normal)
- Al final del drawer: botón [✏ Editar esta Regla] que cierra el drawer y abre el formulario de edición

---

## 7. Mensajes de Error y Validación

| Tipo de error                              | Dónde se muestra                  | Estilo                              |
|--------------------------------------------|-----------------------------------|-------------------------------------|
| Campo obligatorio vacío                    | Debajo del input                  | Texto rojo + ícono ⚠ + borde rojo  |
| Nombre de regla duplicado                  | Debajo del input de nombre        | Texto rojo                          |
| Nombre de campo duplicado en la tabla      | Debajo de la celda del campo      | Texto amarillo (advertencia)        |
| Variable del patrón no definida como campo | Debajo del input del patrón       | Texto amarillo + ícono ⚠            |

---

## 8. Estados de la Pantalla y Transiciones

| Acción del usuario              | Transición visual                                             |
|---------------------------------|---------------------------------------------------------------|
| Clic en "Nueva Regla"           | Scroll suave hasta el formulario vacío (si ya existe abajo)  |
| Guardar regla exitosamente      | Toast notification verde ✓ "Regla guardada exitosamente"     |
| Error al guardar                | Toast notification rojo ✗ con descripción del error          |
| Clic en "Iniciar Proceso"       | Botón muestra spinner por 0.5s, luego redirige a Ingesta     |
| Clic en "Editar"                | Formulario aparece con animación fade-in, pre-relleno        |

---

## 9. Especificaciones de Tipografía y Color

| Elemento                        | Especificación                                         |
|---------------------------------|--------------------------------------------------------|
| Fuente principal                | Inter (Google Fonts), Regular 400 / SemiBold 600       |
| Fuente monospace (patrón)       | JetBrains Mono o Fira Code                             |
| Fondo de página                 | #0d1117 (muy oscuro)                                   |
| Fondo de tarjetas/paneles       | #161b22                                                |
| Fondo de tabla filas alternadas | #1a1f2e y #151a27                                      |
| Texto principal                 | #e6edf3 (blanco suave)                                 |
| Texto secundario / etiquetas    | #8b949e (gris medio)                                   |
| Acento principal                | #2f81f7 (azul eléctrico)                               |
| Acento exitoso                  | #3fb950 (verde)                                        |
| Acento error                    | #f85149 (rojo)                                         |
| Acento advertencia              | #d29922 (ámbar)                                        |
| Borde de inputs                 | #30363d (gris oscuro), enfoque: #2f81f7                |
