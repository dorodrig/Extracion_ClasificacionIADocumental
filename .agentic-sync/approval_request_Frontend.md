# Solicitud de Revisión — Agente Frontend
## HU-01: CA-01 a CA-06 — Configuración y Gestión de Reglas de Trabajo

| Campo | Valor |
|-------|-------|
| **Agente** | Frontend |
| **Rama** | `HU1_CA1-CA6_DEVDAVID_ITEREACION1` |
| **Fecha** | 2026-05-23 |
| **Estado** | PLANNING — Esperando aprobación del Arquitecto Líder |

---

## 1. Resumen del Plan Propuesto

Se implementará la interfaz de usuario completa para gestión de Reglas de Trabajo (HU-01, CA-01 a CA-06) sobre un proyecto **React 18 + TypeScript + Vite 5** nuevo en `FrontEnd/`. 

La solución incluye:
- **Scaffolding completo** del proyecto (Vite + React + TS)
- **Design System SCSS** alineado a Gobernanza §4.7 (dark mode, tokens del mockup)
- **3 componentes principales**: `RuleList`, `RuleForm`, `RuleDynamicFields`
- **Página contenedora**: `RulesPage` que orquesta estado A (sin reglas) y B (con reglas)
- **Layout global** con header, sidebar y breadcrumbs
- **Capa de servicios** con axios centralizado y React Query
- **Validaciones cliente** con react-hook-form + Zod
- **Mocks de API** para desarrollo independiente del backend

---

## 2. Archivos que se Planean Crear/Modificar

### Scaffolding (via Vite)
| Acción | Ruta Absoluta |
|--------|--------------|
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\package.json` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\vite.config.ts` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\tsconfig.json` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\main.tsx` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\App.tsx` |

### Design System SCSS
| Acción | Ruta Absoluta |
|--------|--------------|
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\styles\main.scss` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\styles\abstracts\_variables.scss` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\styles\abstracts\_mixins.scss` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\styles\abstracts\_functions.scss` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\styles\base\_base.scss` |

### Tipos TypeScript
| Acción | Ruta Absoluta |
|--------|--------------|
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\types\rule.types.ts` |

### Servicios API
| Acción | Ruta Absoluta |
|--------|--------------|
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\services\api.ts` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\services\ruleService.ts` |

### Componentes UI
| Acción | Ruta Absoluta |
|--------|--------------|
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\pages\RulesPage.tsx` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\components\Rules\RuleList.tsx` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\components\Rules\RuleList.module.scss` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\components\Rules\RuleForm.tsx` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\components\Rules\RuleForm.module.scss` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\components\Rules\RuleDynamicFields.tsx` |
| NEW | `C:\zData\ExtracionDatosIA\FrontEnd\src\components\common\Layout.tsx` |

### Archivos que NO se modificarán
- ❌ Ningún archivo en `BackEnd/`
- ❌ Ningún mockup en `HU-Mockups/`

---

## 3. Decisiones Técnicas Clave

| # | Decisión | Justificación |
|---|----------|---------------|
| 1 | **React Hook Form + Zod** para formularios | Gobernanza recomienda validación en cliente (Zod/Yup). RHF es óptimo para formularios complejos con FieldArrays dinámicos (CA-06). |
| 2 | **React Query (@tanstack/react-query)** para estado servidor | Handoff exige React Query para invalidación y refetch. Mitiga R-04 (sincronización de estado). |
| 3 | **SCSS Modules** para estilos | Gobernanza §4.7 obliga co-localización de estilos. CSS Modules garantiza aislamiento. |
| 4 | **Convención BEM con prefijo `grm-`** | Gobernanza §4.7 define convención de nombres CSS para prevenir colisiones. |
| 5 | **Mocks de API en capa de servicio** | Backend puede ejecutarse en paralelo. Los mocks se reemplazarán por llamadas reales cuando el backend esté listo. |
| 6 | **Dark mode por defecto** | Mockup HU-01 define tema oscuro profesional como principal (#0d1117 fondo). |
| 7 | **Zustand** para estado global mínimo (cliente activo) | Gobernanza §4.2 prescribe Zustand para estado global. |
| 8 | **No Tailwind CSS** | Gobernanza §4.7 prohíbe explícitamente Tailwind, styled-components, emotion, CSS-in-JS. |

---

## 4. Preguntas para el Arquitecto

1. **¿Existe una lista predefinida de tipos de documento** (Pagaré, Endoso, Cédula, etc.) o debe ser texto libre? El mockup sugiere un dropdown con opciones fijas.

2. **¿El `cliente_id` activo se obtiene del JWT/token decodificado o de un selector en la UI?** El mockup muestra "Cliente Activo: BANCORP" en el header con un botón "Cambiar Cliente". ¿Debo implementar la selección de cliente o asumir que viene del contexto de autenticación?

3. **¿Los endpoints del backend ya están disponibles para pruebas?** Si no, usaré mocks con datos realistas hasta que estén listos.

---

## 5. Riesgos Identificados

| ID | Riesgo | Mitigación | Probabilidad |
|----|--------|-----------|-------------|
| R-04 | Pérdida de sincronización entre listado y ediciones | React Query con invalidación automática al mutar | Media |
| R-FE-01 | FrontEnd vacío — requiere scaffolding completo | Usar template oficial de Vite (confiable) | Baja |
| R-FE-02 | Backend no disponible aún | Implementar mocks en ruleService con switchable flag | Media |
| R-FE-03 | Compilación SCSS puede fallar si tokens mal definidos | Verificar compilación SCSS como paso de validación | Baja |

---

## 6. Dependencias

- [x] Handoff leído y analizado completamente
- [x] Mockup narrativo (MOCKUP-HU-01-Reglas-Trabajo.md) analizado
- [x] Gobernanza Arquitectónica (v1.1.0) analizada
- [ ] Schemas Pydantic del backend (en investigación — se alinearán los types/)
- [x] Rama git correcta: `HU1_CA1-CA6_DEVDAVID_ITEREACION1`

---

*Generado por: Agente Frontend*  
*Fecha: 2026-05-23*  
*Esperando revisión del Arquitecto Líder*
