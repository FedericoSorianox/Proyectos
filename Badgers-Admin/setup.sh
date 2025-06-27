#!/bin/bash

# 🚀 Script de Configuración Automática - Badgers Admin
# Este script configura automáticamente el proyecto

echo "🚀 Iniciando configuración del proyecto Badgers Admin..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_message() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar si estamos en el directorio correcto
if [ ! -f "package.json" ] || [ ! -d "backend" ]; then
    print_error "No se encontró package.json o carpeta backend. Asegúrate de estar en el directorio raíz del proyecto."
    exit 1
fi

print_message "Directorio del proyecto verificado"

# 1. Configurar variables de entorno del backend
print_info "Configurando variables de entorno del backend..."

if [ ! -f "backend/.env" ]; then
    if [ -f "backend/env_template.txt" ]; then
        cp backend/env_template.txt backend/.env
        print_message "Archivo .env del backend creado desde template"
    else
        print_warning "No se encontró env_template.txt. Creando .env básico..."
        cat > backend/.env << EOF
# Variables de entorno para desarrollo local
SECRET_KEY=django-insecure-hl!998$#)*zpak-)bamp+4$#2a1mh77zyf!$ar+gii6(8*ose4
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
EOF
        print_message "Archivo .env del backend creado con configuración básica"
    fi
else
    print_warning "El archivo backend/.env ya existe"
fi

# 2. Configurar variables de entorno del frontend
print_info "Configurando variables de entorno del frontend..."

if [ ! -f ".env" ]; then
    if [ -f "frontend_env_template.txt" ]; then
        cp frontend_env_template.txt .env
        print_message "Archivo .env del frontend creado desde template"
    else
        print_warning "No se encontró frontend_env_template.txt. Creando .env básico..."
        cat > .env << EOF
# Variables de entorno para el frontend
VITE_API_URL=http://localhost:8000
VITE_DEV_MODE=true
VITE_APP_URL=http://localhost:5173
EOF
        print_message "Archivo .env del frontend creado con configuración básica"
    fi
else
    print_warning "El archivo .env del frontend ya existe"
fi

# 3. Verificar Python
print_info "Verificando instalación de Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    print_error "Python no está instalado. Por favor instala Python 3.8 o superior."
    exit 1
fi

print_message "Python encontrado: $($PYTHON_CMD --version)"

# 4. Verificar Node.js
print_info "Verificando instalación de Node.js..."
if ! command -v node &> /dev/null; then
    print_error "Node.js no está instalado. Por favor instala Node.js 16 o superior."
    exit 1
fi

print_message "Node.js encontrado: $(node --version)"

# 5. Verificar npm/yarn
print_info "Verificando gestor de paquetes..."
if command -v yarn &> /dev/null; then
    PACKAGE_MANAGER="yarn"
    print_message "Yarn encontrado: $(yarn --version)"
elif command -v npm &> /dev/null; then
    PACKAGE_MANAGER="npm"
    print_message "NPM encontrado: $(npm --version)"
else
    print_error "No se encontró npm ni yarn. Por favor instala uno de ellos."
    exit 1
fi

# 6. Configurar entorno virtual del backend
print_info "Configurando entorno virtual del backend..."
cd backend

if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    print_message "Entorno virtual creado"
else
    print_warning "El entorno virtual ya existe"
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias del backend
print_info "Instalando dependencias del backend..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_message "Dependencias del backend instaladas"
else
    print_warning "No se encontró requirements.txt"
fi

# Ejecutar migraciones
print_info "Ejecutando migraciones de la base de datos..."
$PYTHON_CMD manage.py migrate
print_message "Migraciones ejecutadas"

cd ..

# 7. Instalar dependencias del frontend
print_info "Instalando dependencias del frontend..."
$PACKAGE_MANAGER install
print_message "Dependencias del frontend instaladas"

# 8. Mostrar resumen
echo ""
echo "🎉 ¡Configuración completada!"
echo ""
echo "📋 Resumen de la configuración:"
echo "   ✅ Variables de entorno configuradas"
echo "   ✅ Entorno virtual de Python creado"
echo "   ✅ Dependencias del backend instaladas"
echo "   ✅ Dependencias del frontend instaladas"
echo "   ✅ Base de datos configurada"
echo ""
echo "🚀 Para ejecutar el proyecto:"
echo ""
echo "   Backend (puerto 8000):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "   Frontend (puerto 5173):"
echo "   $PACKAGE_MANAGER dev"
echo ""
echo "📖 Para más información, consulta SETUP_INSTRUCTIONS.md"
echo ""
print_warning "⚠️  IMPORTANTE: Revisa y edita los archivos .env con tus configuraciones específicas" 