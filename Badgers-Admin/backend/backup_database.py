#!/usr/bin/env python3
"""
Script para hacer backup de la base de datos SQLite local
"""
import os
import shutil
import json
from datetime import datetime
from django.core.management import execute_from_command_line
from django.conf import settings
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'badgers_project.settings')
django.setup()

from api.models import Socio, Producto, Pago, Venta, Gasto

def backup_database():
    """Hacer backup de la base de datos SQLite"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = f'backup_{timestamp}'
    
    # Crear directorio de backup
    os.makedirs(backup_dir, exist_ok=True)
    
    # Copiar archivo de base de datos
    if os.path.exists('db.sqlite3'):
        shutil.copy2('db.sqlite3', f'{backup_dir}/db.sqlite3')
        print(f"✅ Base de datos copiada a {backup_dir}/db.sqlite3")
    
    # Exportar datos como JSON
    export_data_to_json(backup_dir)
    
    print(f"✅ Backup completado en directorio: {backup_dir}")
    return backup_dir

def export_data_to_json(backup_dir):
    """Exportar todos los datos como JSON"""
    data = {}
    
    # Exportar Socios
    try:
        socios = list(Socio.objects.all().values())
        data['socios'] = socios
        print(f"✅ Exportados {len(socios)} socios")
    except Exception as e:
        print(f"❌ Error exportando socios: {e}")
    
    # Exportar Productos
    try:
        productos = list(Producto.objects.all().values())
        data['productos'] = productos
        print(f"✅ Exportados {len(productos)} productos")
    except Exception as e:
        print(f"❌ Error exportando productos: {e}")
    
    # Exportar Pagos
    try:
        pagos = list(Pago.objects.all().values())
        data['pagos'] = pagos
        print(f"✅ Exportados {len(pagos)} pagos")
    except Exception as e:
        print(f"❌ Error exportando pagos: {e}")
    
    # Exportar Ventas
    try:
        ventas = list(Venta.objects.all().values())
        data['ventas'] = ventas
        print(f"✅ Exportados {len(ventas)} ventas")
    except Exception as e:
        print(f"❌ Error exportando ventas: {e}")
    
    # Exportar Gastos
    try:
        gastos = list(Gasto.objects.all().values())
        data['gastos'] = gastos
        print(f"✅ Exportados {len(gastos)} gastos")
    except Exception as e:
        print(f"❌ Error exportando gastos: {e}")
    
    # Guardar JSON
    with open(f'{backup_dir}/data_backup.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✅ Datos exportados a {backup_dir}/data_backup.json")

def restore_from_json(backup_file):
    """Restaurar datos desde JSON (para usar después del deploy)"""
    with open(backup_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Restaurar Socios
    if 'socios' in data:
        for socio_data in data['socios']:
            # Remover campos que no se pueden crear directamente
            socio_data.pop('id', None)
            Socio.objects.get_or_create(
                nombre=socio_data['nombre'],
                defaults=socio_data
            )
        print(f"✅ Restaurados {len(data['socios'])} socios")
    
    # Restaurar Productos
    if 'productos' in data:
        for producto_data in data['productos']:
            producto_data.pop('id', None)
            Producto.objects.get_or_create(
                nombre=producto_data['nombre'],
                defaults=producto_data
            )
        print(f"✅ Restaurados {len(data['productos'])} productos")
    
    # Restaurar Pagos
    if 'pagos' in data:
        for pago_data in data['pagos']:
            pago_data.pop('id', None)
            Pago.objects.create(**pago_data)
        print(f"✅ Restaurados {len(data['pagos'])} pagos")
    
    # Restaurar Ventas
    if 'ventas' in data:
        for venta_data in data['ventas']:
            venta_data.pop('id', None)
            Venta.objects.create(**venta_data)
        print(f"✅ Restaurados {len(data['ventas'])} ventas")
    
    # Restaurar Gastos
    if 'gastos' in data:
        for gasto_data in data['gastos']:
            gasto_data.pop('id', None)
            Gasto.objects.create(**gasto_data)
        print(f"✅ Restaurados {len(data['gastos'])} gastos")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'restore':
        if len(sys.argv) > 2:
            restore_from_json(sys.argv[2])
        else:
            print("❌ Especifica el archivo de backup: python backup_database.py restore backup_file.json")
    else:
        backup_database() 