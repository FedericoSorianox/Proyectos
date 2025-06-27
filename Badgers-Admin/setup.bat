@echo off
REM 🚀 Script de Configuración Automática - Badgers Admin (Windows)
REM Este script configura automáticamente el proyecto en Windows

echo 🚀 Iniciando configuración del proyecto Badgers Admin...

REM Verificar si estamos en el directorio correcto
if not exist "package.json" (
    echo ❌ No se encontró package.json. Asegúrate de estar en el directorio raíz del proyecto.
    pause
    exit /b 1
)

if not exist "backend" (
    echo ❌ No se encontró carpeta backend. Asegúrate de estar en el directorio raíz del proyecto.
    pause
    exit /b 1
)

echo ✅ Directorio del proyecto verificado

REM 1. Configurar variables de entorno del backend
echo ℹ️  Configurando variables de entorno del backend...

if not exist "backend\.env" (
    if exist "backend\env_template.txt" (
        copy "backend\env_template.txt" "backend\.env" >nul
        echo ✅ Archivo .env del backend creado desde template
    ) else (
        echo ⚠️  No se encontró env_template.txt. Creando .env básico...
        (
            echo # Variables de entorno para desarrollo local
            echo SECRET_KEY=django-insecure-hl!998$#)*zpak-)bamp+4$#2a1mh77zyf!$ar+gii6(8*ose4
            echo DEBUG=True
            echo ALLOWED_HOSTS=localhost,127.0.0.1
            echo CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
        ) > "backend\.env"
        echo ✅ Archivo .env del backend creado con configuración básica
    )
) else (
    echo ⚠️  El archivo backend\.env ya existe
)

REM 2. Configurar variables de entorno del frontend
echo ℹ️  Configurando variables de entorno del frontend...

if not exist ".env" (
    if exist "frontend_env_template.txt" (
        copy "frontend_env_template.txt" ".env" >nul
        echo ✅ Archivo .env del frontend creado desde template
    ) else (
        echo ⚠️  No se encontró frontend_env_template.txt. Creando .env básico...
        (
            echo # Variables de entorno para el frontend
            echo VITE_API_URL=http://localhost:8000
            echo VITE_DEV_MODE=true
            echo VITE_APP_URL=http://localhost:5173
        ) > ".env"
        echo ✅ Archivo .env del frontend creado con configuración básica
    )
) else (
    echo ⚠️  El archivo .env del frontend ya existe
)

REM 3. Verificar Python
echo ℹ️  Verificando instalación de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado. Por favor instala Python 3.8 o superior.
    pause
    exit /b 1
)

echo ✅ Python encontrado

REM 4. Verificar Node.js
echo ℹ️  Verificando instalación de Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js no está instalado. Por favor instala Node.js 16 o superior.
    pause
    exit /b 1
)

echo ✅ Node.js encontrado

REM 5. Verificar npm/yarn
echo ℹ️  Verificando gestor de paquetes...
yarn --version >nul 2>&1
if errorlevel 1 (
    set PACKAGE_MANAGER=npm
    echo ✅ NPM encontrado
) else (
    set PACKAGE_MANAGER=yarn
    echo ✅ Yarn encontrado
)

REM 6. Configurar entorno virtual del backend
echo ℹ️  Configurando entorno virtual del backend...
cd backend

if not exist "venv" (
    python -m venv venv
    echo ✅ Entorno virtual creado
) else (
    echo ⚠️  El entorno virtual ya existe
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Instalar dependencias del backend
echo ℹ️  Instalando dependencias del backend...
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo ✅ Dependencias del backend instaladas
) else (
    echo ⚠️  No se encontró requirements.txt
)

REM Ejecutar migraciones
echo ℹ️  Ejecutando migraciones de la base de datos...
python manage.py migrate
echo ✅ Migraciones ejecutadas

cd ..

REM 7. Instalar dependencias del frontend
echo ℹ️  Instalando dependencias del frontend...
%PACKAGE_MANAGER% install
echo ✅ Dependencias del frontend instaladas

REM 8. Mostrar resumen
echo.
echo 🎉 ¡Configuración completada!
echo.
echo 📋 Resumen de la configuración:
echo    ✅ Variables de entorno configuradas
echo    ✅ Entorno virtual de Python creado
echo    ✅ Dependencias del backend instaladas
echo    ✅ Dependencias del frontend instaladas
echo    ✅ Base de datos configurada
echo.
echo 🚀 Para ejecutar el proyecto:
echo.
echo    Backend (puerto 8000):
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python manage.py runserver
echo.
echo    Frontend (puerto 5173):
echo    %PACKAGE_MANAGER% dev
echo.
echo 📖 Para más información, consulta SETUP_INSTRUCTIONS.md
echo.
echo ⚠️  IMPORTANTE: Revisa y edita los archivos .env con tus configuraciones específicas
pause 