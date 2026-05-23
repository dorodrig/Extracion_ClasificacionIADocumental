# 📦 Guía de Instalación del Stack Tecnológico — Proyecto GRM
**Arquitectura:** FastAPI (Python 3.12) + React 18 (TypeScript/Vite) + SQL Server 2019+  
**Estilos:** SASS (SCSS) + CSS puro — Design System GRM  
**Entornos:** Antigravity IDE + Visual Studio Code  
**Alcance:** On-Premise (Piloto) con preparación para migración a AWS  
**Versión del documento:** 1.1.0  
**Fecha:** 2026-05-22  

---

> ⚠️ **ANTES DE COMENZAR:** Ejecuta todos los comandos como **Administrador** en PowerShell.  
> Nunca cierres la terminal a mitad de un proceso de instalación.  
> Cada sección incluye un **comando de verificación** (`✅ Verificar`). Ejecuta siempre la verificación antes de continuar.

---

## 📋 ÍNDICE

1. [Prerrequisitos del Sistema](#1-prerrequisitos-del-sistema)
2. [Instalación de Python 3.12](#2-instalación-de-python-312)
3. [Instalación de Node.js 20 LTS](#3-instalación-de-nodejs-20-lts)
4. [Instalación de SQL Server 2019+ (Express)](#4-instalación-de-sql-server-2019-express)
5. [Instalación de Redis (para Celery)](#5-instalación-de-redis-para-celery)
6. [Instalación y Configuración de Git](#6-instalación-y-configuración-de-git)
7. [Configuración del Entorno: Visual Studio Code](#7-configuración-del-entorno-visual-studio-code)
8. [Configuración del Entorno: Antigravity IDE](#8-configuración-del-entorno-antigravity-ide)
9. [Estructura del Proyecto GRM](#9-estructura-del-proyecto-grm)
10. [Configuración del Backend (FastAPI)](#10-configuración-del-backend-fastapi)
11. [Instalación de SDKs Obligatorios (Google + AWS)](#11-instalación-de-sdks-obligatorios-google--aws)
12. [Configuración del Frontend (React + Vite)](#12-configuración-del-frontend-react--vite)
12A. [Instalación y Configuración de SASS/SCSS](#12a-instalación-y-configuración-de-sassscss)
13. [Variables de Entorno](#13-variables-de-entorno)
14. [Configuración de la Base de Datos](#14-configuración-de-la-base-de-datos)
15. [Arranque del Sistema Completo](#15-arranque-del-sistema-completo)
16. [Verificación Final End-to-End](#16-verificación-final-end-to-end)
17. [Solución de Problemas Comunes](#17-solución-de-problemas-comunes)

---

## 1. Prerrequisitos del Sistema

### Hardware mínimo requerido (Piloto On-Premise)
| Componente | Mínimo | Recomendado |
|---|---|---|
| CPU | 4 núcleos @ 2.4 GHz | 8 núcleos @ 3.0 GHz |
| RAM | 8 GB | 16 GB |
| Almacenamiento | 50 GB SSD libre | 200 GB SSD |
| OS | Windows 10 Pro (64-bit) | Windows 11 Pro / Windows Server 2019 |
| Red | Acceso a internet (para SDKs y AWS) | — |

### Software requerido antes de comenzar
| Software | Versión | Obligatorio |
|---|---|---|
| Windows PowerShell | 5.1+ (incluido en Windows) | ✅ |
| Winget (App Installer) | 1.4+ | ✅ (viene con Windows 10/11 actualizado) |
| Navegador web moderno | Chrome/Edge (para testing) | ✅ |
| Cuenta Google Cloud | Con API Key de Gemini activa | ✅ |
| Cuenta AWS | Con credenciales IAM para Textract | ✅ |

### Verificar conectividad de red
```powershell
# Verificar acceso a internet y endpoints críticos
Test-NetConnection -ComputerName "generativelanguage.googleapis.com" -Port 443
Test-NetConnection -ComputerName "textract.us-east-1.amazonaws.com" -Port 443
```

---

## 2. Instalación de Python 3.12

### 2.1 Descarga e instalación

**URL oficial:** https://www.python.org/downloads/release/python-3120/

```powershell
# Opción 1 — Instalación vía winget (recomendada)
winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements

# Opción 2 — Descarga directa del instalador (si winget falla)
# Descargar: https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
# Ejecutar el instalador con las siguientes opciones:
# [✓] Add Python 3.12 to PATH
# [✓] Install for all users
# Seleccionar "Customize installation" → habilitar "pip", "tcl/tk", "py launcher"
```

### 2.2 Verificar instalación
```powershell
# ✅ Verificar — Ejecuta estos comandos y confirma las versiones
python --version
# Salida esperada: Python 3.12.x

pip --version
# Salida esperada: pip 24.x.x from C:\...\Python312\...

# Si python no se reconoce, reinicia PowerShell como Administrador
```

### 2.3 Actualizar pip a la última versión
```powershell
python -m pip install --upgrade pip
```

---

## 3. Instalación de Node.js 20 LTS

### 3.1 Descarga e instalación

**URL oficial:** https://nodejs.org/en/download (seleccionar LTS 20.x)

```powershell
# Opción 1 — Instalación vía winget (recomendada)
winget install -e --id OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements

# Opción 2 — Descarga directa
# Descargar: https://nodejs.org/dist/v20.18.0/node-v20.18.0-x64.msi
# Ejecutar el instalador (dejar todas las opciones por defecto)
```

### 3.2 Verificar instalación
```powershell
# ✅ Verificar
node --version
# Salida esperada: v20.x.x

npm --version
# Salida esperada: 10.x.x
```

### 3.3 Instalar pnpm (gestor de paquetes más eficiente)
```powershell
npm install -g pnpm
pnpm --version
# Salida esperada: 9.x.x
```

---

## 4. Instalación de SQL Server 2019+ (Express)

### 4.1 Descarga e instalación de SQL Server Express

**URL oficial:** https://www.microsoft.com/es-es/sql-server/sql-server-downloads

```powershell
# Descarga del instalador Express gratuito:
# https://go.microsoft.com/fwlink/p/?linkid=866658
# Ejecutar el instalador → Seleccionar "Básico" (Basic)
# Ruta de instalación sugerida: C:\Program Files\Microsoft SQL Server\

# IMPORTANTE: Durante la instalación, anotar:
# - Nombre de instancia (por defecto: SQLEXPRESS)
# - Puerto (por defecto: 1433 o dinámico)
```

### 4.2 Instalar SQL Server Management Studio (SSMS)

**URL oficial:** https://learn.microsoft.com/es-es/sql/ssms/download-sql-server-management-studio-ssms

```powershell
# Descarga directa de SSMS:
# https://aka.ms/ssmsfullsetup
# Ejecutar instalador → instalación por defecto
```

### 4.3 Habilitar autenticación mixta y TCP/IP

1. Abrir **SQL Server Configuration Manager** (buscar en inicio de Windows)
2. `SQL Server Network Configuration` → `Protocols for SQLEXPRESS`
3. Habilitar **TCP/IP** → doble clic → tab `IP Addresses` → `IPAll` → Puerto TCP: `1433`
4. Reiniciar el servicio SQL Server

```powershell
# Verificar que el servicio SQL Server está corriendo
Get-Service -Name "MSSQL*"
# Salida esperada: Status = Running

# ✅ Verificar conectividad
sqlcmd -S "localhost\SQLEXPRESS" -Q "SELECT @@VERSION"
```

### 4.4 Crear base de datos del proyecto
```sql
-- Ejecutar en SSMS o sqlcmd
CREATE DATABASE GRM_DB;
GO
USE GRM_DB;
GO
-- El schema completo se carga en el paso 14
```

---

## 5. Instalación de Redis (para Celery)

Redis se usa como broker de mensajes para el pipeline de procesamiento asíncrono (Celery).

### 5.1 Instalación de Redis en Windows

**URL oficial:** https://github.com/tporadowski/redis/releases

```powershell
# Opción 1 — Winget
winget install -e --id Redis.Redis --accept-source-agreements --accept-package-agreements

# Opción 2 — Descarga directa
# https://github.com/tporadowski/redis/releases/download/v5.0.14.1/Redis-x64-5.0.14.1.msi
# Ejecutar instalador → marcar "Add Redis to PATH" y "Start Redis as Service"
```

### 5.2 Verificar Redis
```powershell
# ✅ Verificar
redis-cli ping
# Salida esperada: PONG

# Verificar servicio
Get-Service -Name "Redis"
# Salida esperada: Status = Running
```

---

## 6. Instalación y Configuración de Git

### 6.1 Instalación de Git

**URL oficial:** https://git-scm.com/download/win

```powershell
winget install -e --id Git.Git --accept-source-agreements --accept-package-agreements
```

### 6.2 Configuración global de Git
```powershell
# ✅ Verificar
git --version
# Salida esperada: git version 2.x.x

# Configurar identidad (reemplazar con datos reales del equipo)
git config --global user.name "Tu Nombre Completo"
git config --global user.email "tu.email@empresa.com"
git config --global core.autocrlf true
git config --global init.defaultBranch main
```

---

## 7. Configuración del Entorno: Visual Studio Code

### 7.1 Instalación de VS Code

**URL oficial:** https://code.visualstudio.com/download

```powershell
winget install -e --id Microsoft.VisualStudioCode --accept-source-agreements --accept-package-agreements
```

### 7.2 Extensiones obligatorias para el proyecto GRM

Ejecutar estos comandos en PowerShell para instalar todas las extensiones de una vez:

```powershell
# Extensiones de Python (Backend)
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.debugpy
code --install-extension ms-python.black-formatter

# Extensiones de Frontend (React + TypeScript)
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension bradlc.vscode-tailwindcss
code --install-extension formulahendry.auto-rename-tag

# Base de Datos
code --install-extension ms-mssql.mssql

# Docker (para preparación Cloud)
code --install-extension ms-azuretools.vscode-docker

# Utilidades generales
code --install-extension eamodio.gitlens
code --install-extension humao.rest-client
code --install-extension yzhang.markdown-all-in-one
code --install-extension redhat.vscode-yaml

# ✅ Verificar — listar extensiones instaladas
code --list-extensions
```

### 7.3 Configuración del workspace de VS Code

Crear el archivo `C:\zData\ExtracionDatosIA\.vscode\settings.json`:

```json
{
  "python.defaultInterpreterPath": "C:\\zData\\ExtracionDatosIA\\BackEnd\\.venv\\Scripts\\python.exe",
  "python.terminal.activateEnvironment": true,
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/.venv": true,
    "**/node_modules": true,
    "**/.pytest_cache": true
  },
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "mssql.connections": [
    {
      "server": "localhost\\SQLEXPRESS",
      "database": "GRM_DB",
      "authenticationType": "Integrated",
      "profileName": "GRM_DB_Local"
    }
  ]
}
```

---

## 8. Configuración del Entorno: Antigravity IDE

Antigravity es el IDE de IA principal del proyecto. Configurar los siguientes parámetros:

### 8.1 Configuración del workspace en Antigravity

1. Abrir Antigravity IDE
2. Configurar el workspace raíz en: `C:\zData\ExtracionDatosIA`
3. Verificar que el Corpus Name está mapeado a: `c:/zData/ExtracionDatosIA`

### 8.2 Variables de contexto del proyecto para los agentes

En Antigravity, los agentes del proyecto GRM operarán con las siguientes rutas de referencia:
```
Workspace raíz:    C:\zData\ExtracionDatosIA\
Backend:           C:\zData\ExtracionDatosIA\BackEnd\
Frontend:          C:\zData\ExtracionDatosIA\FrontEnd\
Base de datos:     C:\zData\ExtracionDatosIA\ScrpitBaseDatos\
Agentes:           C:\zData\ExtracionDatosIA\Agentes\
Documentación:     C:\zData\ExtracionDatosIA\Documentancion\
Historias de HU:   C:\zData\ExtracionDatosIA\HU\
```

### 8.3 Instalar el plugin Google Antigravity SDK

El plugin `google-antigravity-sdk` ya está disponible en `C:\Users\DavidOrlandoRodrigue\.gemini\config\plugins\google-antigravity-sdk`. Verificar que esté activo en la configuración de plugins de Antigravity.

---

## 9. Estructura del Proyecto GRM

Crear la estructura de directorios del proyecto:

```powershell
# Crear estructura completa del backend
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\BackEnd\app\api\v1\endpoints"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\BackEnd\app\core"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\BackEnd\app\db\models"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\BackEnd\app\db\repositories"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\BackEnd\app\services\ocr"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\BackEnd\app\services\ai_agents"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\BackEnd\app\services\storage"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\BackEnd\app\workers"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\BackEnd\app\schemas"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\BackEnd\tests"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\BackEnd\logs"

# Crear estructura del frontend
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\FrontEnd\src\components"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\FrontEnd\src\pages"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\FrontEnd\src\hooks"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\FrontEnd\src\services"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\FrontEnd\src\store"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\FrontEnd\src\types"

# Scripts de base de datos
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\ScrpitBaseDatos\migrations"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\ScrpitBaseDatos\seeds"

Write-Host "✅ Estructura de directorios creada correctamente."
```

---

## 10. Configuración del Backend (FastAPI)

### 10.1 Crear entorno virtual Python
```powershell
# Navegar al directorio del backend
Set-Location "C:\zData\ExtracionDatosIA\BackEnd"

# Crear entorno virtual aislado
python -m venv .venv

# Activar el entorno virtual
.\.venv\Scripts\Activate.ps1

# Si PowerShell bloquea la ejecución de scripts:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Luego volver a ejecutar: .\.venv\Scripts\Activate.ps1

# ✅ Verificar activación — el prompt debe mostrar (.venv)
python --version
# Salida: Python 3.12.x desde el entorno virtual
```

### 10.2 Crear archivo de dependencias `requirements.txt`

```powershell
# Crear el archivo requirements.txt
@"
# === Framework Principal ===
fastapi==0.115.0
uvicorn[standard]==0.30.6
python-multipart==0.0.9

# === ORM y Base de Datos ===
sqlalchemy==2.0.35
alembic==1.13.3
pyodbc==5.1.0
# Driver ODBC para SQL Server — ver sección 10.3

# === Autenticación y Seguridad ===
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# === Validación y Configuración ===
pydantic==2.9.2
pydantic-settings==2.5.2
python-dotenv==1.0.1

# === SDKs Obligatorios: Google Gemini ===
google-generativeai==0.8.3
google-adk==1.0.0

# === SDKs Obligatorios: AWS Textract ===
boto3==1.35.36
botocore==1.35.36

# === Pipeline Asíncrono ===
celery==5.4.0
redis==5.1.0
kombu==5.3.4

# === Procesamiento de Documentos ===
pypdf2==3.0.1
pillow==10.4.0
pdf2image==1.17.0

# === WebSockets y Comunicación en Tiempo Real ===
websockets==13.1

# === Utilidades ===
httpx==0.27.2
aiofiles==24.1.0
python-slugify==8.0.4

# === Testing ===
pytest==8.3.3
pytest-asyncio==0.24.0
httpx==0.27.2
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8

Write-Host "✅ requirements.txt creado."
```

### 10.3 Instalar el Driver ODBC para SQL Server

**URL oficial:** https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

```powershell
# Instalar ODBC Driver 18 para SQL Server
winget install -e --id Microsoft.ODBCDriverForSQLServer --accept-source-agreements --accept-package-agreements

# ✅ Verificar el driver instalado
Get-OdbcDriver -Name "ODBC Driver*SQL Server*"
# Salida esperada: lista con "ODBC Driver 18 for SQL Server"
```

### 10.4 Instalar todas las dependencias del backend
```powershell
# Asegurar que el entorno virtual está activado
Set-Location "C:\zData\ExtracionDatosIA\BackEnd"
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# ✅ Verificar instalación de los paquetes clave
pip show fastapi google-generativeai boto3 celery sqlalchemy
# Cada paquete debe mostrar su versión instalada
```

### 10.5 Crear el archivo principal de la aplicación FastAPI

```powershell
# Crear main.py
@"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="GRM API",
    description="Sistema de Gestión y Clasificación Documental",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "GRM API"}
"@ | Out-File -FilePath "app\main.py" -Encoding UTF8

Write-Host "✅ app/main.py creado."
```

---

## 11. Instalación de SDKs Obligatorios (Google + AWS)

> Esta sección ya queda cubierta por el `requirements.txt` del paso 10.2.  
> Aquí se detalla la **verificación** y **configuración** de cada SDK.

### 11.1 SDK de Google Gemini — Verificación y prueba de conectividad
```powershell
Set-Location "C:\zData\ExtracionDatosIA\BackEnd"
.\.venv\Scripts\Activate.ps1

# Verificar instalación del SDK
python -c "import google.generativeai as genai; print('✅ google-generativeai OK:', genai.__version__)"

# Test de conectividad con API Key (reemplazar con tu clave real)
# IMPORTANTE: Solo usar para verificación. La clave real va en el .env
python -c "
import google.generativeai as genai
import os
api_key = os.getenv('GEMINI_API_KEY', 'TU_API_KEY_AQUI')
genai.configure(api_key=api_key)
models = [m.name for m in genai.list_models()]
print('✅ Modelos disponibles:', models[:3])
"
```

**Cómo obtener la API Key de Gemini:**
1. Ir a: https://aistudio.google.com/app/apikey
2. Crear un nuevo proyecto o seleccionar uno existente
3. Hacer clic en "Create API Key"
4. Copiar la clave generada (formato: `AIzaSy...`)

### 11.2 SDK de AWS (boto3) — Verificación y prueba de conectividad
```powershell
# Verificar instalación del SDK
python -c "import boto3; print('✅ boto3 OK:', boto3.__version__)"

# Test de conectividad con AWS Textract (usar credenciales de prueba)
python -c "
import boto3
import os
client = boto3.client(
    'textract',
    region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
print('✅ Cliente Textract creado correctamente.')
print('   Endpoint:', client.meta.endpoint_url)
"
```

**Cómo obtener las credenciales AWS para Textract:**
1. Ir a: https://console.aws.amazon.com/iam/
2. `Users` → `Add users` → Nombre: `grm-textract-service`
3. `Attach policies directly` → Buscar y seleccionar: `AmazonTextractFullAccess`
4. Crear usuario → `Security credentials` → `Create access key`
5. Seleccionar "Application running outside AWS" → Copiar Access Key ID y Secret

### 11.3 Instalar Google ADK (Agent Development Kit)
```powershell
# Verificar instalación del ADK
python -c "import google.adk; print('✅ google-adk OK')"

# Si no está disponible, instalar directamente
pip install google-adk==1.0.0
```

---

## 12. Configuración del Frontend (React + Vite)

### 12.1 Crear el proyecto React con Vite
```powershell
Set-Location "C:\zData\ExtracionDatosIA\FrontEnd"

# Inicializar el proyecto React + TypeScript con Vite
# Primero, verificar opciones disponibles:
npx -y create-vite@latest --help

# Crear el proyecto en el directorio actual
npx -y create-vite@latest ./ --template react-ts

# Instalar dependencias base
npm install
```

### 12.2 Instalar dependencias del Frontend
```powershell
Set-Location "C:\zData\ExtracionDatosIA\FrontEnd"

# Instalación de dependencias en un solo comando
npm install `
  react-router-dom@6 `
  axios `
  @tanstack/react-query@5 `
  react-pdf `
  pdfjs-dist `
  react-dropzone `
  zustand `
  date-fns `
  react-hot-toast `
  recharts `
  lucide-react `
  clsx

# Dependencias de desarrollo
npm install -D `
  @types/react-pdf `
  eslint `
  @typescript-eslint/eslint-plugin `
  @typescript-eslint/parser `
  prettier `
  eslint-config-prettier `
  eslint-plugin-react-hooks

# ✅ Verificar que no hay errores
npm run build
# Salida: dist/ generado sin errores
```

### 12.3 Configurar el proxy de desarrollo (Vite → FastAPI)

Editar `C:\zData\ExtracionDatosIA\FrontEnd\vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      }
    }
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
```

---

## 12A. Instalación y Configuración de SASS/SCSS

> SASS (SCSS) es la tecnología de estilos oficial del proyecto GRM. Proporciona variables de diseño,
> mixins reutilizables, anidamiento de selectores y separación por componentes. Se compila a CSS puro
> en tiempo de build. **No se usa Tailwind ni CSS-in-JS.**

### 12A.1 Instalar SASS en el proyecto Frontend

```powershell
Set-Location "C:\zData\ExtracionDatosIA\FrontEnd"

# Instalar sass como dependencia de desarrollo (compilador Dart Sass — oficial)
npm install -D sass sass-loader

# ✅ Verificar instalación
npx sass --version
# Salida esperada: 1.x.x compiled with dart2js
```

**URL oficial de SASS:** https://sass-lang.com/install

### 12A.2 Crear estructura de directorios de estilos SCSS

```powershell
# Crear árbol de directorios de estilos (patrón 7-1 simplificado para GRM)
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\FrontEnd\src\styles\abstracts"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\FrontEnd\src\styles\base"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\FrontEnd\src\styles\components"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\FrontEnd\src\styles\layouts"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\FrontEnd\src\styles\pages"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\FrontEnd\src\styles\themes"

Write-Host "✅ Estructura de estilos SCSS creada correctamente."
```

Estructura resultante:
```
C:\zData\ExtracionDatosIA\FrontEnd\src\styles\
├── abstracts\          ← Variables, mixins, funciones, placeholders SCSS
│   ├── _variables.scss ← Tokens de diseño: colores, tipografía, espaciado
│   ├── _mixins.scss    ← Mixins reutilizables (respond-to, flex-center, etc.)
│   └── _functions.scss ← Funciones SCSS puras
├── base\               ← Reset CSS, tipografía base, utilidades globales
│   ├── _reset.scss     ← Normalización cross-browser
│   ├── _typography.scss← Escala tipográfica del sistema
│   └── _utilities.scss ← Clases de utilidad CSS puras
├── components\         ← Estilos de componentes React (un .scss por componente)
│   ├── _button.scss
│   ├── _card.scss
│   ├── _modal.scss
│   ├── _table.scss
│   ├── _badge.scss
│   └── _pdf-viewer.scss
├── layouts\            ← Grids y estructuras de página
│   ├── _sidebar.scss
│   ├── _header.scss
│   └── _main-content.scss
├── pages\              ← Estilos específicos por página
│   ├── _login.scss
│   ├── _dashboard.scss
│   ├── _pendientes.scss
│   └── _portal-cliente.scss
├── themes\             ← Temas del sistema (dark mode preparado)
│   ├── _dark.scss
│   └── _light.scss     ← Tema por defecto del piloto
└── main.scss           ← Punto de entrada — importa todo el árbol
```

### 12A.3 Crear el archivo de variables SCSS (`_variables.scss`)

```powershell
@"
// ============================================================
// GRM — Design Tokens (abstracts/_variables.scss)
// REGLA: Usar SIEMPRE estas variables. Nunca colores hardcoded.
// ============================================================

// --- Paleta de colores principal ---
\$color-primary:        #1A56DB;   // Azul corporativo GRM
\$color-primary-dark:   #1239A6;
\$color-primary-light:  #4B7FE8;
\$color-secondary:      #0E9F6E;   // Verde éxito / clasificado
\$color-warning:        #E3A008;   // Amarillo pendiente / revisar
\$color-danger:         #E02424;   // Rojo error / rechazo
\$color-info:           #3F83F8;   // Azul informativo

// --- Grises del sistema ---
\$color-gray-50:        #F9FAFB;
\$color-gray-100:       #F3F4F6;
\$color-gray-200:       #E5E7EB;
\$color-gray-400:       #9CA3AF;
\$color-gray-600:       #4B5563;
\$color-gray-800:       #1F2937;
\$color-gray-900:       #111827;

// --- Superficies y fondos ---
\$color-bg-app:         #F3F4F6;   // Fondo global de la app
\$color-bg-sidebar:     #1F2937;   // Panel lateral oscuro
\$color-bg-card:        #FFFFFF;
\$color-bg-overlay:     rgba(0, 0, 0, 0.5);

// --- Tipografía ---
\$font-family-base:     'Inter', 'Segoe UI', system-ui, sans-serif;
\$font-family-mono:     'JetBrains Mono', 'Consolas', monospace;
\$font-size-xs:         0.75rem;   // 12px
\$font-size-sm:         0.875rem;  // 14px
\$font-size-base:       1rem;      // 16px
\$font-size-lg:         1.125rem;  // 18px
\$font-size-xl:         1.25rem;   // 20px
\$font-size-2xl:        1.5rem;    // 24px
\$font-size-3xl:        1.875rem;  // 30px
\$font-weight-normal:   400;
\$font-weight-medium:   500;
\$font-weight-semibold: 600;
\$font-weight-bold:     700;
\$line-height-base:     1.5;
\$line-height-tight:    1.25;

// --- Espaciado (escala 4px base) ---
\$spacing-1:  0.25rem;   // 4px
\$spacing-2:  0.5rem;    // 8px
\$spacing-3:  0.75rem;   // 12px
\$spacing-4:  1rem;      // 16px
\$spacing-5:  1.25rem;   // 20px
\$spacing-6:  1.5rem;    // 24px
\$spacing-8:  2rem;      // 32px
\$spacing-10: 2.5rem;    // 40px
\$spacing-12: 3rem;      // 48px
\$spacing-16: 4rem;      // 64px

// --- Bordes y radios ---
\$border-radius-sm:     0.25rem;   // 4px
\$border-radius-base:   0.375rem;  // 6px
\$border-radius-md:     0.5rem;    // 8px
\$border-radius-lg:     0.75rem;   // 12px
\$border-radius-xl:     1rem;      // 16px
\$border-radius-full:   9999px;    // Pill / circular
\$border-color:         \$color-gray-200;
\$border-color-focus:   \$color-primary;

// --- Sombras ---
\$shadow-sm:    0 1px 2px 0 rgba(0, 0, 0, 0.05);
\$shadow-base:  0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
\$shadow-md:    0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
\$shadow-lg:    0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
\$shadow-xl:    0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);

// --- Breakpoints responsive ---
\$breakpoint-sm:  640px;
\$breakpoint-md:  768px;
\$breakpoint-lg:  1024px;
\$breakpoint-xl:  1280px;
\$breakpoint-2xl: 1536px;

// --- Z-index ---
\$z-index-dropdown:  100;
\$z-index-sidebar:   200;
\$z-index-modal:     300;
\$z-index-toast:     400;
\$z-index-tooltip:   500;

// --- Transiciones ---
\$transition-fast:   all 0.15s ease-in-out;
\$transition-base:   all 0.2s ease-in-out;
\$transition-slow:   all 0.3s ease-in-out;
"@ | Out-File -FilePath "C:\zData\ExtracionDatosIA\FrontEnd\src\styles\abstracts\_variables.scss" -Encoding UTF8

Write-Host "✅ _variables.scss creado con Design Tokens completos."
```

### 12A.4 Crear archivo de mixins SCSS (`_mixins.scss`)

```powershell
@"
// ============================================================
// GRM — Mixins SCSS (abstracts/_mixins.scss)
// ============================================================
@use 'variables' as *;

// --- Responsive breakpoints ---
@mixin respond-to(\$breakpoint) {
  @if \$breakpoint == 'sm' { @media (min-width: \$breakpoint-sm) { @content; } }
  @else if \$breakpoint == 'md' { @media (min-width: \$breakpoint-md) { @content; } }
  @else if \$breakpoint == 'lg' { @media (min-width: \$breakpoint-lg) { @content; } }
  @else if \$breakpoint == 'xl' { @media (min-width: \$breakpoint-xl) { @content; } }
}

// --- Flexbox helpers ---
@mixin flex-center { display: flex; align-items: center; justify-content: center; }
@mixin flex-between { display: flex; align-items: center; justify-content: space-between; }
@mixin flex-start { display: flex; align-items: center; justify-content: flex-start; }

// --- Truncar texto con ellipsis ---
@mixin text-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

// --- Estilo de tarjeta (card) ---
@mixin card-base {
  background-color: \$color-bg-card;
  border: 1px solid \$border-color;
  border-radius: \$border-radius-lg;
  box-shadow: \$shadow-base;
  padding: \$spacing-6;
}

// --- Estado de foco accesible ---
@mixin focus-ring {
  outline: 2px solid \$color-primary;
  outline-offset: 2px;
}

// --- Badge de estado del pipeline ---
@mixin status-badge(\$bg, \$color) {
  display: inline-flex;
  align-items: center;
  padding: \$spacing-1 \$spacing-3;
  border-radius: \$border-radius-full;
  font-size: \$font-size-xs;
  font-weight: \$font-weight-semibold;
  background-color: \$bg;
  color: \$color;
}
"@ | Out-File -FilePath "C:\zData\ExtracionDatosIA\FrontEnd\src\styles\abstracts\_mixins.scss" -Encoding UTF8

Write-Host "✅ _mixins.scss creado."
```

### 12A.5 Crear el punto de entrada SCSS (`main.scss`)

```powershell
@"
// ============================================================
// GRM — Punto de Entrada de Estilos (styles/main.scss)
// REGLA: Este archivo solo importa. NO escribe estilos directos.
// ============================================================

// 1. Abstracts (variables, mixins, funciones) — primero siempre
@use 'abstracts/variables' as *;
@use 'abstracts/mixins' as *;
@use 'abstracts/functions' as *;

// 2. Base (reset, tipografía, utilidades globales)
@use 'base/reset';
@use 'base/typography';
@use 'base/utilities';

// 3. Layouts
@use 'layouts/sidebar';
@use 'layouts/header';
@use 'layouts/main-content';

// 4. Componentes
@use 'components/button';
@use 'components/card';
@use 'components/modal';
@use 'components/table';
@use 'components/badge';
@use 'components/pdf-viewer';

// 5. Páginas
@use 'pages/login';
@use 'pages/dashboard';
@use 'pages/pendientes';
@use 'pages/portal-cliente';

// 6. Tema activo (light por defecto en el piloto)
@use 'themes/light';
"@ | Out-File -FilePath "C:\zData\ExtracionDatosIA\FrontEnd\src\styles\main.scss" -Encoding UTF8

Write-Host "✅ main.scss creado — punto de entrada de estilos."
```

### 12A.6 Importar los estilos en la aplicación React

Editar `C:\zData\ExtracionDatosIA\FrontEnd\src\main.tsx` para importar el SCSS global:

```typescript
// src/main.tsx — Agregar esta línea ANTES de cualquier otro import de estilos
import './styles/main.scss'
// El resto de imports permanece igual
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

### 12A.7 Configurar Vite para soporte SCSS global

Agregar la configuración SCSS a `vite.config.ts` (dentro del bloque `defineConfig` existente):

```typescript
// Agregar el bloque 'css' al vite.config.ts existente
export default defineConfig({
  // ... (configuración existente de plugins, server, resolve — no modificar)
  css: {
    preprocessorOptions: {
      scss: {
        // Importar variables y mixins automáticamente en todos los archivos .scss
        // Evita tener que escribir @use en cada componente
        additionalData: `
          @use '@/styles/abstracts/variables' as *;
          @use '@/styles/abstracts/mixins' as *;
        `
      }
    }
  }
})
```

### 12A.8 Agregar extensión VS Code para SASS

```powershell
# Extensión de SASS para VS Code (autocompletado, lint, goto definition)
code --install-extension syler.sass-indented
code --install-extension mrmlnc.vscode-scss

# ✅ Verificar
code --list-extensions | Select-String "sass"
# Salida esperada: syler.sass-indented y mrmlnc.vscode-scss
```

### 12A.9 Agregar script de compilación SASS al `package.json`

```powershell
# El build de SASS se ejecuta automáticamente con Vite.
# Agregar script auxiliar para validación de SCSS standalone:

# Editar package.json — agregar en la sección "scripts":
# "sass:check": "sass --no-source-map src/styles/main.scss dist/styles.css"
# "sass:watch": "sass --watch src/styles/main.scss dist/styles.css"

# ✅ Verificar compilación SCSS
npx sass src/styles/main.scss --no-source-map --style=compressed
# Salida esperada: compilación exitosa sin errores
```

### 12A.10 Agregar SCSS al `.gitignore`

```powershell
# Agregar al .gitignore existente en C:\zData\ExtracionDatosIA\
@"

# SASS compilado (generado automáticamente por Vite/SASS)
dist/styles.css
dist/styles.css.map
*.css.map
"@ | Add-Content -FilePath "C:\zData\ExtracionDatosIA\.gitignore" -Encoding UTF8

Write-Host "✅ Entradas SASS agregadas al .gitignore."
```

---

## 13. Variables de Entorno

### 13.1 Archivo `.env` del Backend

Crear el archivo `C:\zData\ExtracionDatosIA\BackEnd\.env`:

```powershell
@"
# ==============================================
# GRM Backend — Variables de Entorno
# CRÍTICO: NUNCA commitear este archivo a Git
# ==============================================

# --- Base de Datos SQL Server ---
DATABASE_URL=mssql+pyodbc://localhost\SQLEXPRESS/GRM_DB?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes
DB_ECHO=False

# --- JWT y Seguridad ---
SECRET_KEY=CAMBIAR_POR_CLAVE_ALEATORIA_MINIMO_32_CHARS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=8
CLIENT_TOKEN_EXPIRE_MINUTES=30

# --- Google Gemini SDK ---
GEMINI_API_KEY=TU_GEMINI_API_KEY_AQUI
GEMINI_MODEL=gemini-1.5-pro
GEMINI_TIMEOUT_SECONDS=30
GEMINI_MAX_RETRIES=3

# --- AWS Textract SDK ---
AWS_ACCESS_KEY_ID=TU_AWS_ACCESS_KEY_AQUI
AWS_SECRET_ACCESS_KEY=TU_AWS_SECRET_KEY_AQUI
AWS_DEFAULT_REGION=us-east-1

# --- Celery + Redis ---
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# --- Almacenamiento Local ---
STORAGE_BASE_PATH=C:\zData\ExtracionDatosIA\Storage
TEMP_BASE_PATH=C:\zData\ExtracionDatosIA\Storage\temp

# --- Configuración OCR ---
OCR_CONFIDENCE_THRESHOLD=95.0
OCR_MAX_RETRIES=3

# --- Servidor ---
ENVIRONMENT=development
DEBUG=True
API_V1_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:5173
"@ | Out-File -FilePath "C:\zData\ExtracionDatosIA\BackEnd\.env" -Encoding UTF8

Write-Host "✅ Archivo .env creado. IMPORTANTE: Reemplaza los valores placeholder con tus credenciales reales."
```

### 13.2 Generar SECRET_KEY aleatorio
```powershell
# Generar una clave secreta criptográficamente segura
python -c "import secrets; print('SECRET_KEY =', secrets.token_hex(32))"
# Copiar el valor generado y reemplazarlo en el .env
```

### 13.3 Archivo `.env` del Frontend
```powershell
@"
# GRM Frontend — Variables de Entorno Vite
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_BASE_URL=ws://localhost:8000/ws
VITE_APP_TITLE=GRM — Sistema de Gestión Documental
"@ | Out-File -FilePath "C:\zData\ExtracionDatosIA\FrontEnd\.env.local" -Encoding UTF8
```

### 13.4 Configurar `.gitignore` para proteger credenciales
```powershell
@"
# Python
__pycache__/
*.pyc
.venv/
*.egg-info/
dist/
build/

# Variables de entorno — NUNCA a Git
.env
.env.local
.env.*.local

# Node.js
node_modules/
dist/
*.log

# IDE
.vscode/settings.json
.idea/

# Logs y temporales
logs/
*.log
temp/
"@ | Out-File -FilePath "C:\zData\ExtracionDatosIA\.gitignore" -Encoding UTF8
```

---

## 14. Configuración de la Base de Datos

### 14.1 Inicializar Alembic para migraciones

```powershell
Set-Location "C:\zData\ExtracionDatosIA\BackEnd"
.\.venv\Scripts\Activate.ps1

# Inicializar Alembic
alembic init alembic

Write-Host "✅ Alembic inicializado. Configurar alembic.ini con la URL de la base de datos."
```

### 14.2 Ejecutar el script de schema inicial

Los scripts SQL están en `C:\zData\ExtracionDatosIA\ScrpitBaseDatos\migrations\`.

```powershell
# Ejecutar el script de creación del schema completo en SQL Server
# (El script V1__initial_schema.sql debe existir en esa carpeta)
sqlcmd -S "localhost\SQLEXPRESS" -d "GRM_DB" -i "C:\zData\ExtracionDatosIA\ScrpitBaseDatos\migrations\V1__initial_schema.sql"

# ✅ Verificar tablas creadas
sqlcmd -S "localhost\SQLEXPRESS" -d "GRM_DB" -Q "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME"
```

### 14.3 Crear directorio de almacenamiento de documentos
```powershell
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\Storage\documentos"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\Storage\temp"
New-Item -ItemType Directory -Force -Path "C:\zData\ExtracionDatosIA\Storage\salida"

Write-Host "✅ Directorios de almacenamiento creados."
```

---

## 15. Arranque del Sistema Completo

### 15.1 Arranque del Backend (FastAPI + Uvicorn)
```powershell
# Terminal 1 — Backend FastAPI
Set-Location "C:\zData\ExtracionDatosIA\BackEnd"
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Salida esperada:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Application startup complete.
```

### 15.2 Arranque del Worker de Celery
```powershell
# Terminal 2 — Celery Worker
Set-Location "C:\zData\ExtracionDatosIA\BackEnd"
.\.venv\Scripts\Activate.ps1
celery -A app.workers.celery_app worker --loglevel=info --concurrency=4

# Salida esperada:
# [config]
# .> transport: redis://localhost:6379//
# [queues]
# .> celery           exchange=celery(direct) key=celery
```

### 15.3 Arranque del Frontend (React + Vite)
```powershell
# Terminal 3 — Frontend Vite Dev Server
Set-Location "C:\zData\ExtracionDatosIA\FrontEnd"
npm run dev

# Salida esperada:
# VITE v5.x.x  ready in XXX ms
# ➜  Local:   http://localhost:5173/
```

### 15.4 Script de arranque integrado (todos los servicios)

```powershell
# Crear script de inicio único: start_grm.ps1
@"
# GRM — Script de Inicio del Sistema Completo
Write-Host "🚀 Iniciando GRM Sistema de Gestión Documental..." -ForegroundColor Cyan

# Verificar que Redis está corriendo
$redisService = Get-Service -Name "Redis" -ErrorAction SilentlyContinue
if ($redisService.Status -ne "Running") {
    Start-Service -Name "Redis"
    Write-Host "✅ Redis iniciado." -ForegroundColor Green
} else {
    Write-Host "✅ Redis ya está corriendo." -ForegroundColor Green
}

# Verificar SQL Server
$sqlService = Get-Service -Name "MSSQL`$SQLEXPRESS" -ErrorAction SilentlyContinue
if ($sqlService.Status -ne "Running") {
    Start-Service -Name "MSSQL`$SQLEXPRESS"
    Write-Host "✅ SQL Server iniciado." -ForegroundColor Green
} else {
    Write-Host "✅ SQL Server ya está corriendo." -ForegroundColor Green
}

# Iniciar Backend FastAPI en nueva ventana
Start-Process powershell -ArgumentList "-NoExit -Command `"Set-Location 'C:\zData\ExtracionDatosIA\BackEnd'; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`"" -WindowStyle Normal

# Iniciar Celery Worker en nueva ventana
Start-Process powershell -ArgumentList "-NoExit -Command `"Set-Location 'C:\zData\ExtracionDatosIA\BackEnd'; .\.venv\Scripts\Activate.ps1; celery -A app.workers.celery_app worker --loglevel=info`"" -WindowStyle Normal

# Iniciar Frontend en nueva ventana
Start-Process powershell -ArgumentList "-NoExit -Command `"Set-Location 'C:\zData\ExtracionDatosIA\FrontEnd'; npm run dev`"" -WindowStyle Normal

Write-Host ""
Write-Host "✅ GRM Sistema iniciado correctamente." -ForegroundColor Green
Write-Host "   Backend API:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "   API Docs:     http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "   Frontend:     http://localhost:5173" -ForegroundColor Yellow
"@ | Out-File -FilePath "C:\zData\ExtracionDatosIA\start_grm.ps1" -Encoding UTF8

Write-Host "✅ Script de inicio creado: C:\zData\ExtracionDatosIA\start_grm.ps1"
```

---

## 16. Verificación Final End-to-End

```powershell
# ✅ Verificación 1 — Backend health check
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
# Salida esperada: @{status=ok; service=GRM API}

# ✅ Verificación 2 — Documentación interactiva de la API
Start-Process "http://localhost:8000/docs"
# Se abre la interfaz Swagger UI de FastAPI

# ✅ Verificación 3 — Frontend accesible
Start-Process "http://localhost:5173"
# Se abre la aplicación React

# ✅ Verificación 4 — Conectividad con Redis
redis-cli ping
# PONG

# ✅ Verificación 5 — Base de datos
sqlcmd -S "localhost\SQLEXPRESS" -d "GRM_DB" -Q "SELECT COUNT(*) as tablas FROM INFORMATION_SCHEMA.TABLES"

# ✅ Verificación 6 — Compilación SASS/SCSS
Set-Location "C:\zData\ExtracionDatosIA\FrontEnd"
npx sass --version
# Salida esperada: versión 1.x.x compiled with dart2js

npx sass src/styles/main.scss --no-source-map --dry-run 2>&1
# Salida esperada: compilación sin errores (puede retornar vacío si el archivo no está poblado aún)

Write-Host "✅✅✅ Verificación End-to-End completada. El sistema GRM (incluida capa de estilos SASS) está listo para desarrollo."
```

---

## 17. Solución de Problemas Comunes

### Error: `python` no se reconoce como comando
```powershell
# Agregar Python al PATH manualmente
$pythonPath = "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python312"
$env:PATH += ";$pythonPath;$pythonPath\Scripts"
# O reinstalar Python con la opción "Add to PATH" marcada
```

### Error: `uvicorn` no se encuentra
```powershell
# Asegurar que el entorno virtual está activado
Set-Location "C:\zData\ExtracionDatosIA\BackEnd"
.\.venv\Scripts\Activate.ps1
pip install uvicorn[standard]
```

### Error: Conexión rechazada a SQL Server
```powershell
# Verificar que el servicio está corriendo
Start-Service -Name "MSSQL$SQLEXPRESS"
# Verificar que TCP/IP está habilitado en SQL Server Configuration Manager
# Verificar que el firewall de Windows permite el puerto 1433
netsh advfirewall firewall add rule name="SQL Server 1433" protocol=TCP dir=in localport=1433 action=allow
```

### Error: `google-generativeai` import falla
```powershell
.\.venv\Scripts\Activate.ps1
pip install --upgrade google-generativeai
python -c "import google.generativeai; print('OK')"
```

### Error: `boto3` no puede conectar con AWS
```powershell
# Verificar que las variables de entorno están cargadas
python -c "import os; print('KEY:', os.getenv('AWS_ACCESS_KEY_ID', 'NO CONFIGURADO'))"
# Si dice NO CONFIGURADO, el .env no está siendo cargado correctamente
```

### Error: Redis no inicia en Windows
```powershell
# Iniciar Redis manualmente
Start-Process "C:\Program Files\Redis\redis-server.exe" -ArgumentList "C:\Program Files\Redis\redis.windows.conf"
# O reinstalar desde: https://github.com/tporadowski/redis/releases
```

### Error: SASS no compila — `Cannot find module 'sass'`
```powershell
Set-Location "C:\zData\ExtracionDatosIA\FrontEnd"
# Reinstalar sass como dependencia de desarrollo
npm install -D sass
# Verificar que está instalado
npx sass --version
# Salida esperada: 1.x.x compiled with dart2js
```

### Error: SASS — `Can't find stylesheet to import`
```powershell
# Verificar que la ruta del alias @ está configurada en vite.config.ts
# El alias '@' debe apuntar a '/src'
# Verificar que el archivo main.scss existe:
Test-Path "C:\zData\ExtracionDatosIA\FrontEnd\src\styles\main.scss"
# Salida esperada: True
```

### Error: SASS — `Undefined variable` al usar `$color-primary`
```scss
// Asegurarse de que el additionalData en vite.config.ts está configurado (sección 12A.7)
// O agregar manualmente en el archivo .scss que falla:
@use '@/styles/abstracts/variables' as *;
// Luego sí puede usar $color-primary, $spacing-4, etc.
```

---

*Documento generado por Arquitecto de Software Senior — Proyecto GRM*  
*Stack: FastAPI 0.115 + React 18 + SQL Server 2019 + Google Gemini SDK + AWS Textract SDK*  
*Estilos: SASS (SCSS) 1.x + CSS puro — Design System GRM v1.1.0*
