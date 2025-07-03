#!/bin/bash

# Script de inicio personalizado para Render
echo "=== INICIANDO APLICACIÓN DJANGO ==="
echo "Timestamp: $(date)"

# Configurar explícitamente las variables de entorno
export DJANGO_SETTINGS_MODULE=badgers_project.settings
export PYTHONPATH=/opt/render/project/src/Badgers-Admin/backend

echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "PYTHONPATH: $PYTHONPATH"
echo "Directorio actual: $(pwd)"
echo "Contenido del directorio:"
ls -la

# Verificar que el archivo wsgi.py existe
echo "Verificando wsgi.py:"
if [ -f "badgers_project/wsgi.py" ]; then
    echo "✅ wsgi.py encontrado"
    echo "Primeras líneas de wsgi.py:"
    head -10 badgers_project/wsgi.py
else
    echo "❌ wsgi.py NO encontrado"
    echo "Buscando archivos wsgi:"
    find . -name "*wsgi*" -type f
fi

# Verificar que gunicorn está instalado
echo "Verificando gunicorn:"
which gunicorn
gunicorn --version

# Ejecutar migraciones antes de iniciar
echo "=== EJECUTANDO MIGRACIONES ==="
python manage.py migrate --noinput
echo "Migraciones completadas"

# Iniciar gunicorn con más debugging
echo "=== INICIANDO GUNICORN ==="
exec gunicorn badgers_project.wsgi:application --bind 0.0.0.0:10000 --log-level debug 
