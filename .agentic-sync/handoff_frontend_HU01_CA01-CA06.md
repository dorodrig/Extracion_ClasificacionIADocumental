# Handoff — Frontend — HU-01
## Iteración: 1-DEV-HU-1

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_frontend_HU01_CA01-CA06.md`              |
| **Rol Destino**          | Agente Frontend                                   |
| **HU de Origen**         | HU-01 — Configuración y Gestión de Reglas de Trabajo del Cliente |
| **CAs Asignados**        | CA-01, CA-02, CA-03, CA-04, CA-05, CA-06          |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-1                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: Python 3.12 + FastAPI 0.115 + SQLAlchemy + Alembic
- [x] Frontend: React 18 + TypeScript + Vite 5
- [x] Estilos: SASS/SCSS (preprocesador) — CSS puro como fallback justificado
- [x] Base de Datos: SQL Server 2019+ (SQLAlchemy ORM)
- [x] SDKs: google-generativeai (Gemini) + boto3 (Textract)
- [x] Cola: Celery 5 + Redis

### Patrón Arquitectónico
- [x] Clean Architecture (Ports & Adapters)
- [x] Capas: Infraestructura → Aplicación → Dominio
- [x] Inversión de Dependencias (Ports/Interfaces en capa dominio)

### Preparación Cloud-Ready
- [x] Adapters reemplazables sin cambiar dominio
- [x] Variables de entorno externalizadas (.env)
- [x] CERO credenciales hardcodeadas

### ISO/IEC 25010
- [x] Mantenibilidad: Modularidad, modificabilidad, testeabilidad
- [x] Seguridad: JWT + RBAC + aislamiento de contexto IA
- [x] Eficiencia de Desempeño: Paginación, índices, async/Celery

### Riesgos Identificados
> R-04: Gestión del estado en UI. Asegurar que las reglas del listado (CA-02) no pierdan sincronización con las ediciones (CA-03, CA-05). Utilizar React Query para invalidar y refetch de forma segura.

## Historia de Usuario — Contexto

> **Como** Operario de Digitalización o Administrador del sistema,
> **Quiero** crear, visualizar, editar y seleccionar Reglas de Trabajo configuradas por cliente,
> **Para que** el sistema de extracción y clasificación sepa exactamente qué campos extraer, con qué estructura organizar los documentos en carpetas y bajo qué parámetros operar, sin ambigüedad ni intervención manual adicional.

### Descripción Funcional
Implementación de la interfaz de usuario para listar, crear y editar reglas de trabajo por cliente. Incluye el listado de reglas en tabla y un formulario dinámico complejo donde se pueden agregar/quitar campos a extraer dinámicamente y validar inputs antes de enviar al backend.

## Criterios de Aceptación

### CA-01 — Primer acceso de cliente sin reglas previas
```gherkin
Dado que el operario ha seleccionado un cliente que NO tiene reglas registradas en el sistema
Cuando el sistema carga la sección "Reglas de Trabajo"
Entonces el sistema muestra el formulario de creación de regla completamente vacío
  Y muestra el mensaje informativo: "Este cliente no tiene reglas configuradas. Crea la primera regla."
  Y el botón "Guardar Regla" permanece deshabilitado hasta que todos los campos obligatorios estén completos
```
**Notas de implementación para el agente:**
> Frontend: Consultar `GET /api/v1/rules?cliente_id={id}`. Si el array es vacío, renderizar el estado inicial (Estado A del mockup) con el componente formulario activo. El botón "Guardar" debe estar deshabilitado por validaciones del formulario.

### CA-02 — Visualización del listado de reglas de un cliente con reglas existentes
```gherkin
Dado que el cliente seleccionado tiene una o más reglas registradas
Cuando el operario accede a la sección "Reglas de Trabajo"
Entonces el sistema muestra una tabla/listado con todas las reglas del cliente
  Y cada fila muestra: Nombre de regla, Tipo de documento, Fecha de creación, Última modificación, Versión
  Y cada fila ofrece los botones de acción: "Editar", "Iniciar Proceso", "Ver Detalle"
```
**Notas de implementación para el agente:**
> Frontend: Renderizar la tabla de reglas (Estado B del mockup). Usar React Query para la llamada.

### CA-03 — Carga de regla existente para edición
```gherkin
Dado que el operario visualiza el listado de reglas del cliente
Cuando hace clic en el botón "Editar" sobre una regla específica
Entonces el sistema carga el formulario con todos los valores actuales de esa regla pre-rellenados
  Y todos los campos del formulario están en modo editable
  Y el botón principal del formulario muestra el texto "Actualizar Regla" (no "Guardar Regla")
```
**Notas de implementación para el agente:**
> Frontend: Al dar clic en "Editar", llenar el formulario (ideal usar react-hook-form) con los datos y cambiar a modo edición.

### CA-04 — Creación de una nueva regla adicional para cliente con reglas existentes
```gherkin
Dado que el cliente ya tiene al menos una regla registrada
Cuando el operario hace clic en el botón "Nueva Regla"
Entonces el sistema abre el formulario de regla completamente vacío
  Y genera un nuevo ID único para la nueva regla
  Y las reglas existentes del cliente no son modificadas ni sobreescritas
```
**Notas de implementación para el agente:**
> Frontend: Botón "+ Nueva Regla" reinicia los valores del formulario al estado por defecto para creación.

### CA-05 — Validación de campos obligatorios al guardar
```gherkin
Dado que el operario intenta guardar o actualizar una regla de trabajo
Cuando hace clic en "Guardar Regla" o "Actualizar Regla"
Entonces el sistema valida que los campos obligatorios estén completos:
    | Campo obligatorio                        |
    | Cliente seleccionado                     |
    | Nombre de la regla                       |
    | Tipo de documento                        |
    | Al menos 1 campo a extraer definido      |
    | Patrón de carpeta de salida              |
    | Modo de entrada seleccionado             |
  Y si algún campo obligatorio está vacío, muestra un mensaje de error inline junto al campo
  Y no persiste la regla en base de datos hasta que todos los campos obligatorios estén completos
```
**Notas de implementación para el agente:**
> Frontend: Validar en el cliente (ej. con Zod o Yup) antes del submit a `POST / PUT`. Mostrar errores inline (rojo/iconos).

### CA-06 — Definición dinámica de campos a extraer
```gherkin
Dado que el operario está configurando los campos a extraer dentro de una regla
Cuando agrega un campo mediante el componente dinámico de campos
Entonces el sistema permite agregar N campos, cada uno con:
    | Propiedad        | Descripción                                           |
    | Nombre del campo | Texto libre (ej: "Número de Cédula")                  |
    | Tipo de dato     | Texto / Número / Fecha / Identificación               |
    | Obligatorio      | Checkbox Sí/No                                        |
  Y permite eliminar cualquier campo con un botón de eliminación por fila
  Y el sistema valida que no existan dos campos con el mismo nombre dentro de la misma regla
  Y muestra un error inline si se detecta un nombre de campo duplicado
```
**Notas de implementación para el agente:**
> Frontend: Crear componente FieldArray dinámico. Lógica custom o de react-hook-form para chequear nombres duplicados en tiempo real.

## Especificaciones Técnicas — Frontend

### Estructura de Directorios
> Referencia: Gobernanza §4.1 — Estructura de directorios obligatoria del Frontend
- `src/pages/RulesPage.tsx`
- `src/components/Rules/RuleList.tsx`
- `src/components/Rules/RuleList.module.scss`
- `src/components/Rules/RuleForm.tsx`
- `src/components/Rules/RuleForm.module.scss`
- `src/components/Rules/RuleDynamicFields.tsx`
- `src/services/ruleService.ts`
- `src/types/rule.types.ts`

### Endpoints a Consumir (del Backend)
| Método | Ruta                        | Descripción                          | Schema Respuesta     |
|--------|-----------------------------|--------------------------------------|----------------------|
| GET    | `/api/v1/rules?cliente_id=` | Listar reglas de cliente             | `APIResponse<Rule[]>`|
| GET    | `/api/v1/rules/{id}`        | Detalle de una regla                 | `APIResponse<Rule>`  |
| POST   | `/api/v1/rules`             | Crear regla                          | `APIResponse<Rule>`  |
| PUT    | `/api/v1/rules/{id}`        | Actualizar regla                     | `APIResponse<Rule>`  |

### Referencia de Mockups
> Mockup Narrativo MD: `C:\zData\ExtracionDatosIA\HU\HU-Mockups\MOCKUP-HU-01-Reglas-Trabajo.md`
> **Nota de Mockups de Imagen (PNG):** Sin mockup imagen disponible. Usar mockup textual (MD) y criterio del agente para la maquetación.

### Estilos SASS/SCSS
> Referencia: Gobernanza §4.3 — Estándares de estilos del Frontend

| Elemento | Convención |
|----------|------------|
| Preprocesador | SASS/SCSS (instalado vía `sass` en `devDependencies`) |
| Entry point | `src/styles/main.scss` — importa todos los parciales |
| Variables | `src/styles/_variables.scss` — Design tokens (colores, tipografía, espaciado, bordes, sombras) |
| Componentes | `ComponentName.module.scss` junto al `.tsx` — Estilos modulares con CSS Modules |
| Nombrado clases | kebab-case (`class="card-header"`) |
| Inline styles | PROHIBIDO en componentes React |

## Estándares de Código — Referencia Gobernanza

> El agente DEBE adherirse a los estándares definidos en la Gobernanza Arquitectónica:
> Ruta: `C:\zData\ExtracionDatosIA\Documentancion\Gobernanza_Arquitectura.md`

### Estándares aplicables a este Handoff:
- §4.2 Nombrado Frontend (PascalCase, camelCase)
- Componentes funcionales usando React Hooks.
- Tipado estricto con interfaces de TypeScript (sin `any`).
- CSS Modules en SCSS para aislamiento de estilos.

### Convención de Commits (Conventional Commits)
```
feat(HU-01): implementación UI y lógica cliente para gestión de reglas
```

## Dependencias y Pre-condiciones

### Requiere completado antes:
- [x] Backend HU-01 CA 1-6 (Los endpoints son el insumo, puedes mockearlos en frontend si se ejecutan en paralelo).

### Archivos que NO debe modificar (fuera de su jurisdicción):
- Cualquier archivo en `BackEnd/`
- Mockups en `HU-Mockups/`

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
   - Analiza cada CA asignado y desglosa las tareas técnicas.
   - Identifica riesgos y dependencias.
   - Estima el esfuerzo por tarea.

2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El Humano es solo un cartero. No tiene autoridad técnica para aprobar ni rechazar planes.

3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Frontend.md`
   
   El archivo debe contener:
   - Resumen del plan propuesto
   - Archivos que planeas crear/modificar (con rutas absolutas)
   - Decisiones técnicas clave tomadas
   - Preguntas para el Arquitecto (si las hay)
   - Riesgos identificados

4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Frontend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."

5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación explícita del Arquitecto Líder (transmitida por el Humano Cartero), pasa a modo `EXECUTION`.

6. **En modo `EXECUTION`:**
   - Codifica siguiendo estrictamente los estándares de la Gobernanza.
   - Haz `git add`, `git commit` (con Conventional Commits) y `git push` a la rama indicada.
   - Actualiza el `task.md` con el progreso.

7. **Al terminar la ejecución:**
   - Genera un `walkthrough.md` con resumen de cambios.
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama HU1_CA1-CA6_DEVDAVID_ITEREACION1. Avísale al Arquitecto."*
