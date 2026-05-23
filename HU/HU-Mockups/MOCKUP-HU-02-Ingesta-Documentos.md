# MOCKUP NARRATIVO — HU-02: Ingesta Dual de Documentos (Escáner / Carpeta)
## Documento para Agente de Maquetación UI/UX

> **Instrucciones para el Agente de Maquetación**: Este documento es autosuficiente. Describe la pantalla de Ingesta de Documentos del sistema GRM con precisión detallada. Incluye todos los estados, flujos, comportamientos y especificaciones visuales necesarios para generar mockups sin ambigüedad.

---

## 1. Contexto de la Pantalla

- **Nombre de la pantalla**: "Ingresar Documentos"
- **Ruta de navegación**: Llega siempre desde la pantalla de decisión de modo (ver Sección 0 abajo) | Nunca se accede directamente desde el menú lateral sin haber pasado por la decisión de modo
- **Usuarios que acceden**: Operario de Digitalización (autenticado, cliente activo seleccionado)
- **Estado inicial**: El modo de ingesta ya fue confirmado por el operario en la pantalla de decisión previa (Sección 0). La pantalla de ingesta carga directamente en el modo confirmado.
- **Tema visual**: Igual al resto del sistema — dark mode profesional, misma paleta de colores.

---

## 0. Pantalla de Decisión de Modo (Paso previo obligatorio — Diamante BPMN: ¿Necesita escáner?)

Esta es la **primera pantalla que ve el operario** después de hacer clic en "Iniciar Proceso" en la pantalla de Reglas de Trabajo. Es una pantalla intermedia de decisión obligatoria antes de la pantalla de ingesta completa.

### Diseño visual de la pantalla de decisión:

```
┌─────────────────────────────────────────────────────────────────┐
│  CABECERA GLOBAL                                                  │
├──────────────┬──────────────────────────────────────────────────┤
│  MENÚ        │  Breadcrumb: Inicio > Reglas > ¿Cómo ingresar?         │
│  LATERAL     │                                                    │
│              │  ┌─────────────────────────────────────────────┐  │
│  • Inicio    │  │  REGLA ACTIVA (banner)                          │  │
│  • Reglas    │  │  📋 "Pagarés 2025" | BANCORP | Modo sugerido: Carpeta│  │
│  • Ingresar◄ │  └─────────────────────────────────────────────┘  │
│  • Pendientes│                                                    │
│  • Historial │   ¿Cómo deseas ingresar los documentos?           │
│              │   (texto centrado, blanco, H2)                      │
│              │                                                    │
│              │   ┌──────────────┐   ┌──────────────┐              │
│              │   │  🖨      │   │  📁      │              │
│              │   │ ESCANER    │   │ CARPETA    │              │
│              │   │ por lotes  │   │ local      │  ← [presel.] │
│              │   └──────────────┘   └──────────────┘              │
│              │                                                    │
│              │            [Cancelar]  [Continuar ►]               │
└──────────────┴──────────────────────────────────────────────────┘
```

**Especificaciones de la pantalla de decisión:**
- Es una pantalla completa (no un modal ni un popup)
- Breadcrumb: `Inicio > Reglas de Trabajo > ¿Cómo ingresar los documentos?`
- Título central: **"¿Cómo deseas ingresar los documentos?"** (texto blanco, H2, alineado al centro)
- Las dos tarjetas de modo están centradas horizontalmente en el área de contenido
- La tarjeta correspondiente al modo guardado en la regla aparece con borde azul eléctrico y checkmark ✔
- El operario puede cambiar la selección haciendo clic en la otra tarjeta
- Botón **[Cancelar]**: gris outline — regresa al listado de Reglas de Trabajo sin crear ningún lote
- Botón **[Continuar ►]**: azul eléctrico — siempre habilitado (hay siempre una opción preseleccionada de la regla)
- Al hacer clic en "Continuar", el sistema registra el modo definitivo en el objeto de lote (batch) y carga la pantalla de ingesta del Paso 1

---

## 2. Layout General (Pantalla de Ingesta — después de confirmar modo)

```
┌─────────────────────────────────────────────────────────────────┐
│  CABECERA GLOBAL                                                 │
│  Logo | Operario: Juan Pérez | Cliente: BANCORP | [Cambiar][Salir]│
├──────────────┬──────────────────────────────────────────────────┤
│              │  Breadcrumb: Inicio > Ingresar Documentos         │
│  MENÚ        │                                                   │
│  LATERAL     │  ┌─────────────────────────────────────────────┐ │
│              │  │  REGLA ACTIVA (banner informativo)           │ │
│  • Inicio    │  │  📋 Regla: "Pagarés 2025" | Tipo: Pagaré    │ │
│  • Reglas    │  │  Modo preseleccionado: 📁 Carpeta Local      │ │
│  • Ingresar◄ │  │  [Cambiar Regla]                            │ │
│  • Pendientes│  └─────────────────────────────────────────────┘ │
│  • Historial │                                                   │
│              │  [PASO 1: Selección de Modo]                      │
│              │  [PASO 2: Carga de Documentos]                    │
│              │  [PASO 3: Confirmación y Envío]                   │
└──────────────┴──────────────────────────────────────────────────┘
```

---

## 3. Banner de Regla Activa

Al tope del área de contenido, siempre visible:
- Fondo: azul oscuro semi-transparente con borde izquierdo azul eléctrico (4px)
- Ícono 📋 + texto: "Regla activa: [NOMBRE REGLA] | Tipo: [TIPO DOCUMENTO] | Modo: [MODO]"
- Botón pequeño [Cambiar Regla] a la derecha — regresa a la pantalla de Reglas de Trabajo con confirmación

---

## 4. Paso 1 — Selección del Modo de Entrada

### Diseño visual — Tarjetas de selección:
Dos tarjetas grandes una al lado de la otra (o apiladas en pantallas angostas):

```
┌──────────────────────────┐   ┌──────────────────────────┐
│                          │   │                          │
│      🖨️                  │   │      📁                  │
│    [ícono escáner        │   │    [ícono carpeta         │
│     grande, outline]     │   │     grande, outline]     │
│                          │   │                          │
│  Escáner por Lotes       │   │  Carpeta Local           │
│                          │   │                          │
│  Digitaliza múltiples    │   │  Selecciona una carpeta  │
│  documentos en una sola  │   │  local y procesa los     │
│  sesión de escaneo.      │   │  archivos uno a uno.     │
│                          │   │                          │
│  Formatos: PDF           │   │  Formatos: PDF, JPG,     │
│                          │   │  PNG, TIFF               │
└──────────────────────────┘   └──────────────────────────┘
```

**Estados de las tarjetas:**
- **No seleccionada**: Borde #30363d (gris oscuro), fondo #161b22
- **Hover**: Borde #2f81f7 (azul), transformación leve (scale: 1.02) con transición suave (0.2s)
- **Seleccionada**: Borde azul eléctrico (3px), fondo #1c2333 (azul muy oscuro), ícono cambia a azul eléctrico, checkmark ✓ en la esquina superior derecha

Si la regla activa tiene un modo preseleccionado, la tarjeta correspondiente inicia en estado "Seleccionada". El operario puede cambiarla.

---

## 5. Paso 2A — Modo Escáner: Pantalla de Conexión y Captura

### Sub-estado 2A.1: Conectar Escáner
```
┌─────────────────────────────────────────────────────────────────┐
│  CONECTAR ESCÁNER                                                │
│                                                                  │
│  Dispositivos detectados:                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  🖨 HP ScanJet Pro 3600        [Seleccionar]             │    │
│  │  🖨 Canon DR-C230              [Seleccionar]             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                              [↻ Buscar Escáneres]│
│                                                                  │
│  ⚠ Si no aparece tu escáner, verifica la conexión USB/red        │
│    y que el driver esté instalado.                               │
└─────────────────────────────────────────────────────────────────┘
```

### Sub-estado 2A.2: Escáner conectado — Listo para escanear
```
┌─────────────────────────────────────────────────────────────────┐
│  🖨 HP ScanJet Pro 3600   ●  Conectado                    [Desconectar]│
│                                                                  │
│  Documentos capturados: 0                                        │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │           [ícono de escáner grande animado]             │    │
│  │                                                         │    │
│  │      Coloca los documentos en el escáner y              │    │
│  │       presiona el botón de inicio de escáner            │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│                         [▶ Iniciar Escaneo]                      │
└─────────────────────────────────────────────────────────────────┘
```

### Sub-estado 2A.3: Documentos capturados
```
┌─────────────────────────────────────────────────────────────────┐
│  Documentos capturados: 5                    [+ Agregar más]     │
├─────────────────────────────────────────────────────────────────┤
│  #  │ Nombre              │ Páginas │ Tamaño   │ Estado    │     │
│  1  │ scan_001.pdf        │ 3       │ 1.2 MB   │ ✓ Listo   │ [🗑]│
│  2  │ scan_002.pdf        │ 1       │ 0.4 MB   │ ✓ Listo   │ [🗑]│
│  3  │ scan_003.pdf        │ 2       │ 0.9 MB   │ ✓ Listo   │ [🗑]│
│  4  │ scan_004.pdf        │ 4       │ 1.8 MB   │ ✓ Listo   │ [🗑]│
│  5  │ scan_005.pdf        │ 1       │ 0.3 MB   │ ⚠ Ilegible│ [🗑]│
├─────────────────────────────────────────────────────────────────┤
│  Total: 5 documentos | 11 páginas | 4.6 MB                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Paso 2B — Modo Carpeta Local: Selector y Listado

### Sub-estado 2B.1: Selección de carpeta
```
┌─────────────────────────────────────────────────────────────────┐
│  SELECCIONAR CARPETA DE DOCUMENTOS                               │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │  📁 [ícono de carpeta grande, outline]                  │    │
│  │                                                         │    │
│  │  Haz clic para seleccionar la carpeta que               │    │
│  │  contiene los documentos a procesar.                    │    │
│  │  Formatos soportados: PDF, JPG, PNG, TIFF               │    │
│  │                                                         │    │
│  │            [📁 Seleccionar Carpeta]                     │    │
│  │              (botón azul eléctrico)                     │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Sub-estado 2B.2: Carpeta seleccionada — Listado de archivos
```
┌─────────────────────────────────────────────────────────────────┐
│  📁 C:\Documentos\BANCORP\Lote_Mayo2025\     [Cambiar Carpeta]   │
│  Archivos encontrados: 8 compatibles | 2 omitidos               │
├─────────────────────────────────────────────────────────────────┤
│  ⚠ Se omitieron 2 archivos no compatibles: contrato.docx, datos.xlsx│
├─────────────────────────────────────────────────────────────────┤
│  #  │ Nombre archivo        │ Ext. │ Páginas │ Tamaño  │        │
│  1  │ pagare_001.pdf        │ PDF  │ 3       │ 1.1 MB  │  [ ✓ ] │
│  2  │ cedula_maria.jpg      │ JPG  │ 1       │ 0.2 MB  │  [ ✓ ] │
│  3  │ endoso_carlos.pdf     │ PDF  │ 2       │ 0.8 MB  │  [ ✓ ] │
│  4  │ pagare_002.pdf        │ PDF  │ 1       │ 0.5 MB  │  [ ✓ ] │
│  5  │ cedula_pedro.png      │ PNG  │ 1       │ 0.3 MB  │  [ ✓ ] │
│  6  │ endoso_juan.pdf       │ PDF  │ 2       │ 0.7 MB  │  [ ✓ ] │
│  7  │ pagare_003.tiff       │ TIFF │ 1       │ 0.9 MB  │  [ ✓ ] │
│  8  │ carta_trabajo.pdf     │ PDF  │ 4       │ 1.5 MB  │  [ ✓ ] │
├─────────────────────────────────────────────────────────────────┤
│  Seleccionados: 8 | Total páginas: 15 | Tamaño: 6.0 MB          │
└─────────────────────────────────────────────────────────────────┘
```
- Los checkboxes de la última columna permiten excluir archivos individuales
- Un checkbox global en la cabecera permite seleccionar/deseleccionar todos
- Los archivos omitidos no tienen checkbox (aparecen en el aviso de advertencia amarillo)

---

## 7. Paso 3 — Panel de Confirmación y Resumen antes del Envío

Antes de enviar, el sistema muestra un panel de resumen (aparece con animación slide-down):

```
┌─────────────────────────────────────────────────────────────────┐
│  ✅ RESUMEN DE ENVÍO                                             │
│                                                                  │
│  Regla activa:     Pagarés 2025                                  │
│  Cliente:          BANCORP                                       │
│  Modo:             📁 Carpeta local                              │
│  Documentos:       8                                             │
│  Total páginas:    15                                            │
│  Tamaño total:     6.0 MB                                        │
│  Tiempo estimado:  ~2 minutos (basado en SLA del sistema)        │
│                                                                  │
│                     [Cancelar]   [✓ Confirmar y Enviar]          │
└─────────────────────────────────────────────────────────────────┘
```
- **[Cancelar]**: Botón gris outline — no hace nada, cierra el panel de resumen
- **[✓ Confirmar y Enviar]**: Botón verde filled — inicia el pipeline

---

## 8. Paso 3 (En curso) — Pantalla de Progreso del Procesamiento

Tras confirmar, la pantalla se transforma en el monitor de progreso en tiempo real:

```
┌─────────────────────────────────────────────────────────────────┐
│  PROCESAMIENTO EN CURSO                                          │
│  Lote ID: GRM-20250522-001                                       │
│                                                                  │
│  Progreso general: [████████████░░░░░░░░] 60% (9 de 15 páginas) │
│                                                                  │
│  Documento actual: pagare_003.tiff                               │
│  Etapa: ⚙ OCR — Procesando página 1 de 1...                     │
│                                                                  │
│  Estado por documento:                                           │
│  ✓  pagare_001.pdf      → Clasificado exitosamente               │
│  ✓  cedula_maria.jpg    → Clasificado exitosamente               │
│  ✓  endoso_carlos.pdf   → Clasificado exitosamente               │
│  ✓  pagare_002.pdf      → Clasificado exitosamente               │
│  ✓  cedula_pedro.png    → Clasificado exitosamente               │
│  ⚠  endoso_juan.pdf     → Pendiente revisión humana              │
│  ⟳  pagare_003.tiff     → Procesando...                          │
│  ○  carta_trabajo.pdf   → En cola                                │
│                                                                  │
│  Tiempo transcurrido: 00:47                                      │
│                                                                  │
│  [Ver Pendientes (1)]      [Cancelar Lote]                       │
└─────────────────────────────────────────────────────────────────┘
```

**Leyenda de íconos de estado:**
- ✓ Verde: Clasificado exitosamente
- ⚠ Ámbar: Pendiente revisión humana
- ✗ Rojo: Error en el procesamiento
- ⟳ Azul (animado): En proceso actualmente
- ○ Gris: En cola, pendiente

---

## 9. Pantalla Final — Resumen de Lote Completado

```
┌─────────────────────────────────────────────────────────────────┐
│  ✅ LOTE PROCESADO                                               │
│  Completado a las 15:23:45 — Duración total: 01:42              │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │      6      │  │      1      │  │      1      │             │
│  │  Clasificados│  │  Pendientes │  │   Errores   │             │
│  │  ✓           │  │  ⚠          │  │  ✗          │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                  │
│  Carpetas creadas:                                               │
│  📁 CC123456789 / DAVID_RODRIGUEZ / PAGARE / (2 archivos)       │
│  📁 CC987654321 / MARIA_GARCIA / CEDULA / (1 archivo)           │
│  📁 CC111222333 / CARLOS_LOPEZ / ENDOSO / (1 archivo)           │
│  📁 CC555666777 / PEDRO_MARTINEZ / CEDULA / (1 archivo)         │
│  ...                                                            │
│                                                                  │
│     [Ver Pendientes (1)]    [Nuevo Lote]    [Ver Historial]     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Especificaciones de Colores y Estados de UI

| Elemento                           | Color / Estilo                                           |
|------------------------------------|----------------------------------------------------------|
| Tarjeta de modo seleccionada       | Borde #2f81f7 (3px), fondo #1c2333                       |
| Barra de progreso                  | Relleno #2f81f7, fondo #21262d, animación shimmer        |
| Estado "Clasificado" en lista      | Ícono ✓ verde #3fb950, texto gris claro                  |
| Estado "Pendiente" en lista        | Ícono ⚠ ámbar #d29922, texto ámbar                       |
| Estado "Error" en lista            | Ícono ✗ rojo #f85149, texto rojo                         |
| Estado "Procesando" (ícono)        | Ícono ⟳ azul #2f81f7, animación de rotación continua    |
| Chips de archivos omitidos         | Fondo #2d1b1b, texto #f85149, borde #f85149 suave        |
| Botón "Confirmar y Enviar"         | Fondo #238636 (verde), texto blanco, hover #2ea043       |
| Tarjeta de resumen de lote (cards) | Fondo #161b22, borde redondeado, número grande centrado  |
