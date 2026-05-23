# Handoff — Frontend — HU-01 (Parte 2)
## Iteración: 2-DEV-HU-1

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_frontend_HU01_CA07-CA13.md`              |
| **Rol Destino**          | Agente Frontend                                   |
| **HU de Origen**         | HU-01 — Configuración y Gestión de Reglas de Trabajo del Cliente |
| **CAs Asignados**        | CA-07, CA-08, CA-09, CA-11, CA-12, CA-13          |
| **CAs Excluidos**        | CA-10 (Solo lógica Backend)                       |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 2-DEV-HU-1                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Frontend: React 18 + TypeScript + Vite 5 + Zustand + React Query
- [x] Estilos: SASS/SCSS Modules (Gobernanza §4.7)

### Riesgos Identificados
> R-07: UX del patrón de carpetas (CA-07). La vista previa en tiempo real requiere parseo eficiente sin causar re-renders pesados en el formulario principal.

## Criterios de Aceptación Asignados al Frontend

### CA-07 — Configuración y validación del patrón de carpeta de salida
**Responsabilidad Frontend:**
Crear UI para insertar variables dinámicas clickeables (chips). Mostrar vista previa en tiempo real en gris claro monospace. Mostrar advertencia inline si el usuario escribe una variable `{X}` que no existe en la lista de campos.

### CA-08 — Umbral de confianza OCR fijo y visible
**Responsabilidad Frontend:**
Mostrar un progress bar/input en estado "disabled" fijado al 95%, con ícono de tooltip (información) explicando el motivo, tal como se define en el mockup.

### CA-09 — Inicio del proceso de extracción desde una regla
**Responsabilidad Frontend:**
En la tabla de reglas, el botón "Iniciar Proceso" debe pre-seleccionar el modo guardado en la regla y redirigir a la pantalla de ingesta (o mockear la redirección si HU-02 no existe).

### CA-11 — Persistencia de reglas para uso en futuros proyectos ("Duplicar Regla")
**Responsabilidad Frontend:**
Agregar la acción "Duplicar Regla" en la UI. Al hacer clic, invocar `POST /api/v1/rules/{id}/duplicate` y refetchear el listado (React Query `invalidateQueries`).

### CA-12 — Validación de nombre único de regla por cliente
**Responsabilidad Frontend:**
Capturar el HTTP 409 del Backend al guardar y mostrar el mensaje de error exactamente bajo el input del nombre de la regla en el formulario.

### CA-13 — Selección de modo de entrada de documentos en la regla
**Responsabilidad Frontend:**
Crear UI (Radio buttons u opciones visuales) para seleccionar entre "Escáner (por lotes)" y "Carpeta local (uno a uno)".

## Especificaciones Técnicas — Frontend

### Archivos a Modificar
- `src/components/Rules/RuleForm.tsx`
- `src/components/Rules/RuleList.tsx`
- `src/services/ruleService.ts` (agregar endpoint duplicate)

### Estilos SASS/SCSS
- Mantener consistencia con el Design System oscuro creado en la iteración previa.

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.**
3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Frontend.md`
4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Frontend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."
5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación, pasa a modo `EXECUTION`.
6. **Al terminar la ejecución:** Genera un `walkthrough.md` y avisa al Humano.
