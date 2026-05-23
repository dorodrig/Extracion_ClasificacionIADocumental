# Consolidación de Variables de Entorno

Al escanear el proyecto, se encontró el archivo principal `BackEnd/.env.example` que contiene las variables iniciales definidas por la arquitectura. Para un correcto funcionamiento integral basado en las Historias de Usuario (HU), a continuación se presenta la consolidación actual y las variables adicionales recomendadas.

## 1. Variables Actuales (Encontradas en el Backend)

Estas variables ya están definidas y preparadas para su uso:

> [!NOTE]
> Estas variables deben copiarse de `.env.example` a un nuevo archivo `.env` en el Backend y llenarse con los valores reales y seguros. ¡Nunca subas el `.env` real al repositorio de Git!

### 🗄️ Base de Datos (HU-10)
- `DATABASE_URL`: Cadena de conexión para la base de datos SQL Server (ej: `mssql+pyodbc://sa:TU_PASSWORD@localhost\SQLEXPRESS/GRM_DB...`).

### 🔒 Seguridad y Autenticación (HU-08)
- `SECRET_KEY`: Llave criptográfica para generar y validar los tokens JWT.
- `ALGORITHM`: Algoritmo de encriptación de los JWT (generalmente `HS256`).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de vida de la sesión del usuario (ej: 60 minutos).

### 🤖 Inteligencia Artificial (HU-04, HU-05)
- `GEMINI_API_KEY`: Llave de acceso a la API de Google Gemini, usada por los agentes para extraer contexto y clasificar documentos.

### 📄 Extracción OCR (HU-03)
- `AWS_ACCESS_KEY_ID`: ID de acceso para AWS Textract.
- `AWS_SECRET_ACCESS_KEY`: Clave secreta para AWS Textract.
- `AWS_DEFAULT_REGION`: Región por defecto donde corre el servicio de AWS (ej: `us-east-1`).

---

## 2. Variables de Entorno Recomendadas para Agregar

De acuerdo a las integraciones, procesos y flujos planteados en las Historias de Usuario (como el manejo de almacenamiento, trazabilidad y el frontend), deberías agregar las siguientes variables:

### ⚙️ Adiciones para el Backend (`BackEnd/.env`)

> [!TIP]
> Estas variables te ayudarán a independizar aún más la infraestructura del código fuente.

**Almacenamiento de Archivos (HU-02 Ingesta y HU-06 Visor):**
- `AWS_S3_BUCKET_NAME`: Nombre del bucket de AWS S3 (o su equivalente si usan otro proveedor). Necesario para guardar físicamente los PDFs que suben los clientes y las imágenes renderizadas para que el Operario las valide en pantalla.

**Auditoría y Entorno (HU-09 Trazabilidad):**
- `APP_ENVIRONMENT`: Entorno de ejecución (`development`, `staging`, `production`). Permite activar o desactivar logs más pesados o características de debug según dónde esté corriendo el sistema.
- `LOG_LEVEL`: Nivel de detalle de los logs de auditoría (ej. `INFO` para producción, `DEBUG` para desarrollo).

**Configuración Avanzada IA:**
- `GEMINI_MODEL`: Especificar la versión exacta del modelo a utilizar (ej. `gemini-1.5-pro`). Así, si en el futuro Google actualiza los modelos, puedes cambiarlo directamente aquí sin modificar el código interno de los Agentes de IA.

### 🖥️ Nuevas Variables para el Frontend (`FrontEnd/.env`)

> [!IMPORTANT]
> En aplicaciones desarrolladas con Vite (como el Frontend de este proyecto), todas las variables que necesiten estar accesibles desde el navegador **deben empezar obligatoriamente con el prefijo `VITE_`**.

El frontend actualmente necesita conectarse con los servicios del backend (para el módulo de Ingesta y Validación Humana). Debes crear un archivo `.env` en la carpeta `FrontEnd` con:

- `VITE_API_URL`: La URL raíz de tu servidor Backend. 
  - *En local:* `http://localhost:8000/api`
  - *En producción:* `https://api.tu-dominio.com/api`
  - *Por qué es vital:* El módulo de validación (HU-06) y la ingesta (HU-02) necesitan saber a dónde mandar las peticiones HTTP y los documentos escaneados.

- `VITE_APP_ENV`: Para que el cliente sepa si está corriendo en ambiente local o productivo (ej. para ocultar botones de prueba en producción).

---

## 📋 Resumen de Acción a Tomar

1. Actualizar el archivo `BackEnd/.env` (y `.env.example`) añadiendo `AWS_S3_BUCKET_NAME`, `APP_ENVIRONMENT` y `GEMINI_MODEL`.
2. Crear un archivo `FrontEnd/.env` e incluir la variable `VITE_API_URL` apuntando a tu backend.
