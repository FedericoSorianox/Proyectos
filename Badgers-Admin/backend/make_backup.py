#!/usr/bin/env python3
"""
Script simple para hacer backup de la base de datos usando Django dumpdata
"""
import os
import subprocess
import sys
from datetime import datetime

def make_backup():
    """Hacer backup usando Django dumpdata"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backup_data_{timestamp}.json'
    
    try:
        # Hacer backup de todos los datos
        cmd = [
            'python', 'manage.py', 'dumpdata',
            '--indent', '2',
            '--output', backup_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Backup creado exitosamente: {backup_file}")
            print(f"📁 Archivo: {os.path.abspath(backup_file)}")
        else:
            print(f"❌ Error creando backup: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error ejecutando backup: {e}")
        return None
    
    return backup_file

def restore_backup(backup_file):
    """Restaurar backup usando Django loaddata"""
    if not os.path.exists(backup_file):
        print(f"❌ Archivo de backup no encontrado: {backup_file}")
        return False
    
    try:
        # Restaurar datos
        cmd = [
            'python', 'manage.py', 'loaddata', backup_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Backup restaurado exitosamente desde: {backup_file}")
            return True
        else:
            print(f"❌ Error restaurando backup: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando restauración: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'restore':
        if len(sys.argv) > 2:
            restore_backup(sys.argv[2])
        else:
            print("❌ Especifica el archivo de backup: python make_backup.py restore backup_file.json")
    else:
        make_backup() 