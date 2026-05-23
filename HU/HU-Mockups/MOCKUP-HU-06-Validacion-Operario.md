# MOCKUP NARRATIVO — HU-06: Validación Humana — Lista de Pendientes y Visor de Documentos (Operario)
## Documento para Agente de Maquetación UI/UX

> **Instrucciones para el Agente de Maquetación**: Este documento describe con precisión la pantalla de trabajo principal del Operario de Digitalización para la revisión y corrección de documentos que el pipeline automático no pudo clasificar. Genera mockups para los dos estados principales: la Lista de Pendientes y el Visor de Documentos. Toda la información está aquí; no hagas preguntas.

---

## 1. Contexto de la Pantalla

- **Nombre de la pantalla**: "Documentos Pendientes"
- **Ruta de navegación**: Menú lateral → "Pendientes" (con badge de conteo numérico rojo)
- **Usuarios que acceden**: Operario de Digitalización
- **Propósito**: Permite al operario ver la cola de documentos que requieren su intervención, abrirlos en un visor enriquecido y resolverlos mediante corrección directa o instrucción al agente IA.
- **Importancia visual**: Esta es la pantalla de mayor densidad de trabajo del operario. El diseño debe ser funcional, claro y reducir la fatiga visual. Dark mode es esencial.

---

## 2. Vista 1: Lista de Documentos Pendientes

### Layout General
```
┌─────────────────────────────────────────────────────────────────┐
│  CABECERA GLOBAL                                                 │
├──────────────┬──────────────────────────────────────────────────┤
│  MENÚ        │  Breadcrumb: Inicio > Documentos Pendientes        │
│  LATERAL     │                                                   │
│              │  Título: "Documentos Pendientes"    Badge: [3]    │
│  • Inicio    │  (el badge "3" es rojo, indica cantidad)          │
│  • Reglas    │                                                   │
│  • Ingresar  │  BARRA DE FILTROS Y BÚSQUEDA (ver detalle abajo)  │
│  • Pendientes│                                                   │
│    [3] ◄     │  TABLA DE DOCUMENTOS PENDIENTES                   │
│  • Historial │  (ver detalle abajo)                              │
│              │                                                   │
└──────────────┴──────────────────────────────────────────────────┘
```

**Menú lateral — ítem "Pendientes"**: Muestra un badge rojo con el número de documentos pendientes. Si hay 0, el badge no se muestra.

---

### Barra de Filtros y Búsqueda

Ubicada encima de la tabla, en una fila horizontal:

```
[🔍 Buscar por nombre de archivo...]  [Cliente ▼]  [Motivo ▼]  [Desde]─[Hasta]  [✕ Limpiar]
```

- **Campo de búsqueda**: Input de texto, placeholder "Buscar por nombre de archivo...", búsqueda en tiempo real (debounce 300ms)
- **Cliente**: Dropdown con los clientes del operario (solo los que él maneja)
- **Motivo**: Dropdown con opciones: Todos / Campo nulo / Campo incompleto / Baja confianza / Tipo incorrecto / Error de IA
- **Rango de fechas**: Dos date pickers (Desde — Hasta)
- **Limpiar filtros**: Botón con ícono ✕, visible solo si hay algún filtro activo

---

### Tabla de Documentos Pendientes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  #  │ Archivo              │ Cliente  │ Motivo de Rechazo     │ En cola │ Acciones  │
├─────┼──────────────────────┼──────────┼───────────────────────┼─────────┼───────────┤
│  1  │ 📄 endoso_juan.pdf   │ BANCORP  │ Campo "CC" nulo       │ 🔴 1h 23m │ [Revisar] │
│  2  │ 📄 carta_trabajo.pdf │ BANCORP  │ Tipo doc. incorrecto  │ 🟡 32m    │ [Revisar] │
│  3  │ 📄 pagare_008.pdf    │ BANCORP  │ Nombre incompleto     │ 🟢 5m     │ [Revisar] │
└─────┴──────────────────────┴──────────┴───────────────────────┴─────────┴───────────┘
   Mostrando 3 de 3 documentos pendientes
```

**Detalle de la columna "En cola":**
- 🟢 Verde: < 15 minutos
- 🟡 Ámbar: 15–60 minutos
- 🔴 Rojo: > 60 minutos (urgente)
- Formato: "1h 23m" o "32m" o "5m"
- Al hacer hover sobre el tiempo: tooltip con fecha y hora exacta de entrada a la cola

**Columna "Acciones":**
- Botón **[Revisar]**: Azul eléctrico, abre el Visor de Documentos para ese documento

---

### Estado vacío (sin pendientes)

Cuando no hay documentos pendientes:
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│         ✅ [ícono de checkmark grande, verde, outline]           │
│                                                                  │
│     No hay documentos pendientes de revisión.                    │
│     Todo el lote fue procesado exitosamente.                     │
│                                                                  │
│              [Ver Historial de Lotes]                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Vista 2: Visor de Documentos

Al hacer clic en **[Revisar]**, la pantalla completa cambia al Visor de Documentos (full-page, no modal).

### Layout del Visor — División en dos paneles

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  CABECERA DEL VISOR                                                          │
│  ← Volver a Pendientes  │  📄 endoso_juan.pdf  │  Cliente: BANCORP  │ Pendiente [1/3] ▶│
├──────────────────────────────────────┬───────────────────────────────────────┤
│                                      │                                       │
│   PANEL IZQUIERDO (65% del ancho)    │   PANEL DERECHO (35% del ancho)       │
│   VISOR DEL DOCUMENTO                │   DATOS EXTRAÍDOS Y ACCIONES          │
│                                      │                                       │
└──────────────────────────────────────┴───────────────────────────────────────┘
```

---

### Panel Izquierdo — Visor del Documento

#### Barra de herramientas del visor (encima del documento):
```
[← Pág anterior]  Página 1 de 2  [Pág siguiente →]  │  [🔍-] [100%] [🔍+]  │  [↺ Rotar]
```

#### Área de visualización del documento:
- El PDF o imagen se renderiza en el panel izquierdo
- Fondo #0d1117 (muy oscuro) alrededor del documento
- El documento renderizado tiene sombra suave para destacarlo del fondo
- Las páginas se muestran centradas horizontalmente
- El scroll vertical funciona dentro del panel izquierdo sin afectar el panel derecho

---

### Panel Derecho — Datos Extraídos y Acciones

#### Sección 1: Cabecera del panel derecho
```
┌─────────────────────────────────────┐
│  ⚠ PENDIENTE DE REVISIÓN            │
│  Motivo: Campo "CC" nulo            │
│  Ingresó a cola: hace 1h 23m        │
└─────────────────────────────────────┘
```
- Fondo ámbar muy oscuro (#2d2200) con borde izquierdo ámbar (#d29922, 4px)
- Ícono ⚠ ámbar + texto claro

#### Sección 2: Campos Extraídos (tabla del panel derecho)
```
┌─────────────────────────────────────┐
│  CAMPOS EXTRAÍDOS                   │
├─────────────────────────────────────┤
│  Número de Cédula  * (Obligatorio)  │
│  [______________]  ← Campo editable │
│  ✗ No encontrado  │ OCR: —          │
│                                     │
│  Nombre Completo   * (Obligatorio)  │
│  [Juan Carlos Martínez___]          │
│  ✓ Validado       │ OCR: 97.2%      │
│                                     │
│  Tipo de Documento                  │
│  [Endoso_______________________]    │
│  ✓ Validado       │ OCR: 95.8%      │
│                                     │
│  Fecha del Documento                │
│  [2025-03-15___________________]    │
│  ✓ Validado       │ OCR: 98.1%      │
└─────────────────────────────────────┘
```

**Diseño por campo:**
Cada campo ocupa un bloque independiente con:
- **Nombre del campo** (gris claro, pequeño, uppercase)
- Indicador de obligatorio (asterisco rojo + texto "Obligatorio" si aplica)
- **Input de texto** (editable si el operario lo activa; ver lógica a continuación)
- **Indicador de estado** (línea debajo del input):
  - ✓ verde "Validado" + "OCR: 97.2%" para campos OK
  - ✗ rojo "No encontrado" + "OCR: —" para campos fallidos
  - ⚠ ámbar "Baja confianza" + "OCR: 87.3%" para campos dudosos

**Comportamiento de los inputs en el panel derecho:**
- **Por defecto**: Los inputs están en modo lectura (cursor no editable, borde neutro)
- **Al hacer clic**: El campo con ✗ se activa automáticamente (borde azul, cursor de texto visible)
- **Al hacer clic en un campo ✓**: Un tooltip aparece: "Este campo fue validado correctamente. ¿Deseas editarlo igualmente? [Sí, editar]"

#### Sección 3: Acciones de Resolución

```
┌─────────────────────────────────────┐
│  RESOLVER DOCUMENTO                 │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  ✎ Corrección directa       │    │
│  │  (1 campo con problema)     │    │
│  │  [Guardar corrección ▶]     │    │
│  └─────────────────────────────┘    │
│           ── O ──                   │
│  ┌─────────────────────────────┐    │
│  │  🤖 Enviar al Agente        │    │
│  │  [_________________________]│    │
│  │  Escribe la instrucción... │    │
│  │  [Enviar al Agente ▶]      │    │
│  └─────────────────────────────┘    │
│                                     │
│  [🗑 Descartar documento]           │
│  (botón pequeño, rojo outline)      │
└─────────────────────────────────────┘
```

**Lógica de la sección de acciones:**

**Caso A — 1 campo con problema:**
- La tarjeta "Corrección directa" está activa (resaltada con borde azul)
- El campo problemático en la sección 2 ya está activado para edición
- Botón **[Guardar corrección ▶]** verde, habilitado cuando el campo tiene un valor válido ingresado
- La tarjeta "Enviar al Agente" está disponible pero en estado secundario (no resaltada)

**Caso B — 2+ campos con problema:**
- La tarjeta "Corrección directa" está disponible pero no resaltada
- La tarjeta "Enviar al Agente" está activa y resaltada (borde azul)
- Textarea para la instrucción: fondo #0d1117, borde #30363d, placeholder: "Ej: El CC del titular es 987654321. El nombre correcto es MARIA GARCIA. El tipo de documento es Pagaré."
- Botón **[Enviar al Agente ▶]** azul eléctrico, habilitado cuando la instrucción tiene al menos 20 caracteres
- Contador de caracteres debajo del textarea: "45 / 500"

**Botón "Descartar documento":**
- Siempre visible al fondo del panel derecho
- Al hacer clic: modal de confirmación aparece con campo de texto obligatorio "Motivo de descarte"
- Solo se confirma si el motivo tiene contenido

---

## 4. Cabecera de Navegación del Visor

La cabecera del visor permite navegar entre documentos pendientes sin volver a la lista:
```
← Volver a Pendientes | 📄 endoso_juan.pdf | [◄ Anterior]  Pendiente 1 de 3  [Siguiente ►]
```
- **← Volver a Pendientes**: Link que regresa a la lista
- **[◄ Anterior] / [Siguiente ►]**: Navegan al documento pendiente anterior/siguiente en la cola
- El nombre del archivo actual está centrado en la cabecera

---

## 5. Estado "En Reprocesamiento" en la lista de pendientes

Cuando el operario envía un documento al agente, su fila en la lista cambia:

```
│  1  │ 📄 endoso_juan.pdf   │ BANCORP  │ ⟳ En reprocesamiento...  │ —       │ [Ver estado]│
```
- La celda de "Motivo de Rechazo" muestra "⟳ En reprocesamiento..." con el ícono animado en azul
- El botón de acción cambia a **[Ver estado]** (gris, solo lectura)
- Cuando el agente termina, la fila actualiza automáticamente (polling o WebSocket):
  - Si exitoso: desaparece de la lista con animación fade-out + toast "✓ endoso_juan.pdf clasificado"
  - Si falla de nuevo: la fila vuelve a estado ⚠ con el nuevo motivo de rechazo del agente

---

## 6. Notificación de Nuevo Documento Pendiente (en tiempo real)

Mientras el operario trabaja, si llega un nuevo documento a la cola, aparece una notificación no intrusiva:

```
┌──────────────────────────────────────────────────────┐
│  🔔 Nuevo documento pendiente                         │
│  pagare_009.pdf — Motivo: Nombre incompleto          │
│  [Ver ahora]                            [Descartar]   │
└──────────────────────────────────────────────────────┘
```
- Aparece en la esquina inferior derecha (toast notification)
- Permanece visible 8 segundos, luego desaparece con fade-out
- El badge del menú lateral se actualiza simultáneamente

---

## 7. Especificaciones de Colores y Tipografía

| Elemento                                  | Especificación                                             |
|-------------------------------------------|------------------------------------------------------------|
| Tiempo en cola — urgente (>60 min)        | 🔴 Texto #f85149                                           |
| Tiempo en cola — advertencia (15–60 min)  | 🟡 Texto #d29922                                           |
| Tiempo en cola — OK (<15 min)             | 🟢 Texto #3fb950                                           |
| Campo con error ✗                         | Borde rojo #f85149, texto estado rojo                      |
| Campo validado ✓                          | Texto estado verde #3fb950 (no cambia el borde del input) |
| Campo baja confianza ⚠                    | Texto estado ámbar #d29922                                 |
| Panel del visor (fondo documento)         | #0d1117                                                    |
| Barra de herramientas del visor           | #161b22, borde inferior #21262d                            |
| Panel derecho (fondo)                     | #0d1117 (mismo que visor para cohesión)                    |
| Separador entre paneles                   | Línea vertical #21262d (1px)                               |
| Textarea de instrucción al agente         | Borde #30363d, fondo #0d1117, texto #e6edf3                |
| Botón "Enviar al Agente" activo           | Fondo #2f81f7, hover #388bfd                               |
| Botón "Guardar corrección" activo         | Fondo #238636, hover #2ea043                               |
| Botón "Descartar documento"               | Outline #f85149, texto #f85149, fondo transparente         |
