# Solicitud de Revisión - QA - HU-01

**Resumen del Plan Propuesto:**
Se implementará la cobertura de pruebas automatizadas para la HU-01 (Gestión de Reglas de Trabajo). En el Backend, se validarán los endpoints y la lógica de validación de esquemas (pytest). En el Frontend, se probarán los componentes principales (`RuleForm` y la lista de reglas) asegurando el renderizado condicional, la validación de campos requeridos y el manejo dinámico del `FieldArray` usando Vitest y React Testing Library.

**Archivos a Crear/Modificar:**
- `C:\zData\ExtracionDatosIA\BackEnd\tests\test_rules_api.py` (Modificar/Crear)
- `C:\zData\ExtracionDatosIA\BackEnd\tests\test_rule_validation.py` (Modificar/Crear)
- `C:\zData\ExtracionDatosIA\FrontEnd\src\components\RuleForm.test.tsx` (Crear)
- `C:\zData\ExtracionDatosIA\FrontEnd\src\components\RuleList.test.tsx` (Crear)

**Decisiones Técnicas Clave:**
- Se utilizará `pytest` junto con un cliente de pruebas de FastAPI (`TestClient`) y simulación de la Base de Datos para el backend.
- En el frontend, se empleará `@testing-library/react` (RTL) para simular las interacciones del usuario (llenado de formulario, clics) y validar los estados de los botones.

**Preguntas para el Arquitecto:**
- ¿Existe alguna configuración de Vitest base definida en la Gobernanza, o procedo a instalar las dependencias (`vitest`, `@testing-library/react`, `jsdom`) usando la configuración estándar de Vite?
- ¿El backend ya cuenta con un `conftest.py` configurado para mockear la BD o debo crearlo en esta iteración?

**Riesgos Identificados:**
- La integración de RTL con formularios complejos (como un FieldArray) puede requerir configuración adicional de act() si los componentes tienen renderizados asíncronos pesados.
- Dependencia de que los componentes Frontend (`RuleForm`, `RuleList`) existan y estén accesibles para probarlos.
