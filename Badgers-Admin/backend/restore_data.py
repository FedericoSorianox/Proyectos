#!/usr/bin/env python3
"""
Script para restaurar datos en producción después del deploy
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar Django para producción
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'badgers_project.settings_production')
django.setup()

def restore_from_backup(backup_file):
    """Restaurar datos desde archivo de backup"""
    if not os.path.exists(backup_file):
        print(f"❌ Archivo de backup no encontrado: {backup_file}")
        return False
    
    try:
        # Usar Django loaddata para restaurar
        execute_from_command_line(['manage.py', 'loaddata', backup_file])
        print(f"✅ Datos restaurados exitosamente desde: {backup_file}")
        return True
    except Exception as e:
        print(f"❌ Error restaurando datos: {e}")
        return False

def create_sample_data():
    """Crear datos de ejemplo si no hay backup"""
    from django.contrib.auth.models import User
    from api.models import Socio, Producto, Pago, Venta, Gasto
    from datetime import datetime, timedelta
    
    print("📝 Creando datos de ejemplo...")
    
    # Crear superusuario si no existe
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'badger2025!@#')
        print("✅ Superusuario creado: admin / badger2025!@#")
    
    # Crear algunos socios de ejemplo
    socios_data = [
        {'nombre': 'Juan Pérez', 'email': 'juan@example.com', 'telefono': '123456789'},
        {'nombre': 'María García', 'email': 'maria@example.com', 'telefono': '987654321'},
        {'nombre': 'Carlos López', 'email': 'carlos@example.com', 'telefono': '555555555'},
    ]
    
    for socio_data in socios_data:
        Socio.objects.get_or_create(
            nombre=socio_data['nombre'],
            defaults=socio_data
        )
    
    print(f"✅ {len(socios_data)} socios de ejemplo creados")
    
    # Crear algunos productos de ejemplo
    productos_data = [
        {'nombre': 'Clase de Boxeo', 'precio': 25.00, 'descripcion': 'Clase individual de boxeo'},
        {'nombre': 'Clase de Muay Thai', 'precio': 30.00, 'descripcion': 'Clase individual de Muay Thai'},
        {'nombre': 'Membresía Mensual', 'precio': 150.00, 'descripcion': 'Membresía completa por mes'},
    ]
    
    for producto_data in productos_data:
        Producto.objects.get_or_create(
            nombre=producto_data['nombre'],
            defaults=producto_data
        )
    
    print(f"✅ {len(productos_data)} productos de ejemplo creados")
    
    # Crear algunos pagos de ejemplo (último mes)
    socios = list(Socio.objects.all())
    if socios:
        for i in range(5):
            fecha = datetime.now() - timedelta(days=i*7)
            Pago.objects.create(
                socio=socios[i % len(socios)],
                monto=150.00,
                fecha_pago=fecha.strftime('%Y-%m-%d'),
                metodo_pago='Efectivo'
            )
    
    print("✅ Pagos de ejemplo creados")
    
    # Crear algunas ventas de ejemplo
    productos = list(Producto.objects.all())
    if productos:
        for i in range(3):
            fecha = datetime.now() - timedelta(days=i*3)
            Venta.objects.create(
                producto=productos[i % len(productos)],
                cantidad=1,
                total_venta=productos[i % len(productos)].precio,
                fecha_venta=fecha.strftime('%Y-%m-%d'),
                cliente='Cliente Ejemplo'
            )
    
    print("✅ Ventas de ejemplo creadas")
    
    # Crear algunos gastos de ejemplo
    gastos_data = [
        {'concepto': 'Alquiler del local', 'monto': 500.00, 'categoria': 'Alquiler'},
        {'concepto': 'Luz', 'monto': 150.00, 'categoria': 'Servicios'},
        {'concepto': 'Agua', 'monto': 80.00, 'categoria': 'Servicios'},
        {'concepto': 'Equipamiento', 'monto': 300.00, 'categoria': 'Equipamiento'},
    ]
    
    for gasto_data in gastos_data:
        fecha = datetime.now() - timedelta(days=len(gastos_data))
        Gasto.objects.create(
            concepto=gasto_data['concepto'],
            monto=gasto_data['monto'],
            categoria=gasto_data['categoria'],
            fecha=fecha.strftime('%Y-%m-%d')
        )
    
    print(f"✅ {len(gastos_data)} gastos de ejemplo creados")
    print("✅ Datos de ejemplo creados exitosamente")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'restore' and len(sys.argv) > 2:
            restore_from_backup(sys.argv[2])
        elif sys.argv[1] == 'sample':
            create_sample_data()
        else:
            print("❌ Uso: python restore_data.py [restore backup_file.json | sample]")
    else:
        print("❌ Uso: python restore_data.py [restore backup_file.json | sample]")
        print("   - restore: restaurar desde archivo de backup")
        print("   - sample: crear datos de ejemplo") 