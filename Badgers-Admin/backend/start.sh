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




echo "=== EJECUTANDO MIGRACIONES ==="
python manage.py migrate --noinput
echo "Migraciones completadas"

# --- LÍNEA NUEVA PARA CREAR EL SUPERUSUARIO ---
echo "=== CREANDO SUPERUSUARIO (SI NO EXISTE) ==="
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'badger2025!@#')"
echo "Proceso de superusuario completado"


# Iniciar gunicorn
echo "=== INICIANDO GUNICORN ==="
exec gunicorn badgers_project.wsgi:application --bind 0.0.0.0:10000 --log-level debug