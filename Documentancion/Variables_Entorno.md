# Consolidación de Variables de Entorno (GRM Document Intelligence)

Este documento consolida todas las variables de entorno necesarias para el proyecto, basándose en los archivos `.env` y `.env.example` existentes en el Backend y Frontend, y proponiendo adiciones clave según las Historias de Usuario (HU).

> [!NOTE]
> Los archivos `.env` contienen información sensible y **NUNCA** deben subirse al repositorio (Git). Usa los archivos `.env.example` como plantilla.

---

## 1. Variables del Backend (`BackEnd/.env`)

Estas variables gestionan la conexión a base de datos, seguridad, integraciones de IA (Gemini/AWS) y tareas en segundo plano.

### 🗄️ Base de Datos (HU-01, HU-10)
- `DATABASE_URL`: Cadena de conexión a SQL Server. 
  - *Ejemplo*: `mssql+pyodbc://sa:Password@localhost\SQLEXPRESS:1433/GRM_DB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes`

### 🔒 Seguridad y Autenticación (HU-08)
- `SECRET_KEY`: Clave secreta y robusta para firmar los tokens JWT.
- `ALGORITHM`: Algoritmo criptográfico usado para JWT (ej. `HS256`).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de validez del token de sesión en minutos (ej. `480` para 8 horas).

### 🤖 Google Gemini - Extracción y Clasificación IA (HU-04, HU-05)
- `GEMINI_API_KEY`: Clave de acceso a la API de Google Gemini.
- `GEMINI_MODEL`: Modelo a utilizar (ej. `gemini-1.5-pro`).
- `GEMINI_TIMEOUT_SECONDS`: Tiempo de espera máximo para la respuesta de la IA (ej. `30`).
- `GEMINI_MAX_RETRIES`: Número máximo de reintentos en caso de fallo de la API (ej. `3`).

### 📄 AWS Textract - OCR (HU-03 - Futuro)
- `AWS_ACCESS_KEY_ID`: ID de clave de acceso de AWS.
- `AWS_SECRET_ACCESS_KEY`: Clave secreta de acceso de AWS.
- `AWS_DEFAULT_REGION`: Región por defecto de AWS (ej. `us-east-1`).

### ⚙️ Procesos en Segundo Plano (Celery - Futuro)
- `CELERY_BROKER_URL`: URL del broker de mensajería (Redis/RabbitMQ) para orquestar la extracción asíncrona (ej. `redis://localhost:6379/0`).

### 📁 Almacenamiento Local (HU-02)
- `STORAGE_BASE_PATH`: Ruta local o de red para almacenar los documentos ingresados temporal o permanentemente (ej. `C:\zData\GRM_Storage`).

---

## 2. Variables del Frontend (`FrontEnd/.env`)

En Vite (el framework usado), todas las variables expuestas al navegador deben tener el prefijo `VITE_`.

### 🌐 Conexión y Configuración UI (HU-06, HU-07)
- `VITE_API_BASE_URL`: URL raíz de la API del Backend. Fundamental para que el portal web y la validación se comuniquen con el servidor.
  - *Ejemplo Local*: `http://localhost:8000`
- `VITE_APP_TITLE`: Nombre de la aplicación a mostrar en la pestaña del navegador (ej. `GRM Document Intelligence`).

---

## 3. Variables Recomendadas a Agregar (Mejores Prácticas)

De acuerdo a los procesos de las Historias de Usuario, se recomienda agregar las siguientes variables a tu infraestructura para mayor control:

### Backend
> [!TIP]
> Estas variables optimizan la auditoría y despliegue del sistema.

- **Auditoría (HU-09)**:
  - `APP_ENV`: Define el entorno actual (`development`, `staging`, `production`). Útil para configurar niveles de logging.
  - `LOG_LEVEL`: Define el nivel de los logs de la aplicación (`INFO`, `DEBUG`, `ERROR`).
- **Almacenamiento Cloud (HU-02)**:
  - `AWS_S3_BUCKET_NAME`: Si deciden pasar de `STORAGE_BASE_PATH` a la nube de AWS S3 para almacenar los PDFs de manera escalable.
- **CORS y Seguridad UI**:
  - `ALLOWED_ORIGINS`: Lista de dominios del frontend permitidos para realizar peticiones al backend (ej. `http://localhost:5173,https://mi-dominio.com`), protegiendo la API de accesos no autorizados.

### Frontend
- **Modo Entorno**:
  - `VITE_APP_ENV`: Para identificar si el UI está en `development` o `production`, y así ocultar o mostrar herramientas de depuración a los operarios (HU-06).

---

## 📋 Resumen de Acción
1. **En Local:** Crea o actualiza tu archivo `BackEnd/.env` y `FrontEnd/.env` copiando las variables de los `.env.example` y poniendo tus valores (ej. tu clave de Gemini).
2. **En Despliegue:** Asegúrate de configurar todas estas variables en tu servicio de hosting (Docker, AWS, Vercel, etc.).
