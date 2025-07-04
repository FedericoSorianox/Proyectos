# 🔧 Solución para Base de Datos Borrada en Render

## 🚨 Problema
Al hacer deploy en Render, la base de datos SQLite se borra porque:
- SQLite se almacena localmente en el contenedor
- Cada vez que Render reinicia el contenedor, se pierden los datos
- No hay persistencia de datos

## ✅ Solución: Migrar a PostgreSQL

### 1. **Hacer Backup de Datos Actuales (IMPORTANTE)**

Si aún tienes acceso a tu base de datos local, haz backup inmediatamente:

```bash
cd backend
python make_backup.py
```

Esto creará un archivo `backup_data_YYYYMMDD_HHMMSS.json` con todos tus datos.

### 2. **Configurar PostgreSQL en Render**

#### Opción A: Usar render.yaml (Recomendado)
1. Sube el archivo `render.yaml` a tu repositorio
2. En Render, ve a tu servicio
3. En "Settings" → "Build & Deploy" → "Environment"
4. Selecciona "Use render.yaml"

#### Opción B: Configuración Manual
1. En Render, ve a tu servicio
2. En "Settings" → "Environment"
3. Agrega estas variables:

```
DJANGO_SETTINGS_MODULE=badgers_project.settings_production
DATABASE_URL=postgresql://... (se configura automáticamente)
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_STORAGE_BUCKET_NAME=badgersproducts
AWS_S3_REGION_NAME=us-east-2
```

### 3. **Crear Base de Datos PostgreSQL**

1. En Render, ve a "Databases"
2. Crea una nueva base de datos PostgreSQL
3. Copia la URL de conexión
4. En tu servicio web, agrega la variable `DATABASE_URL` con esa URL

### 4. **Actualizar Configuración**

Los archivos ya están configurados:
- ✅ `settings_production.py` - Configuración para PostgreSQL
- ✅ `start.sh` - Usa configuración de producción
- ✅ `requirements.txt` - Incluye dependencias necesarias

### 5. **Hacer Deploy**

```bash
git add .
git commit -m "Migrar a PostgreSQL"
git push
```

### 6. **Restaurar Datos**

#### Si tienes backup:
```bash
# En Render, en la consola del servicio:
python restore_data.py restore backup_data_YYYYMMDD_HHMMSS.json
```

#### Si no tienes backup:
```bash
# Crear datos de ejemplo:
python restore_data.py sample
```

## 🔄 Proceso Completo

### Paso 1: Backup Local
```bash
cd backend
python make_backup.py
# Guarda el archivo backup_data_*.json
```

### Paso 2: Configurar Render
1. Sube `render.yaml` al repositorio
2. En Render, conecta la base de datos PostgreSQL
3. Configura las variables de entorno de AWS S3

### Paso 3: Deploy
```bash
git add .
git commit -m "Migrar a PostgreSQL"
git push
```

### Paso 4: Restaurar Datos
```bash
# En la consola de Render:
python restore_data.py restore backup_data_YYYYMMDD_HHMMSS.json
```

## 🛠️ Comandos Útiles

### Verificar Estado de la Base de Datos
```bash
python manage.py dbshell
```

### Crear Superusuario
```bash
python manage.py createsuperuser
```

### Ver Migraciones
```bash
python manage.py showmigrations
```

### Ejecutar Migraciones
```bash
python manage.py migrate
```

## 📋 Checklist

- [ ] Hacer backup de datos actuales
- [ ] Configurar PostgreSQL en Render
- [ ] Actualizar variables de entorno
- [ ] Hacer deploy
- [ ] Restaurar datos desde backup
- [ ] Verificar que todo funcione

## 🆘 Si Algo Sale Mal

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "Database connection failed"
- Verificar que `DATABASE_URL` esté configurada correctamente
- Verificar que la base de datos PostgreSQL esté activa

### Error: "Permission denied"
- Verificar que las credenciales de AWS S3 sean correctas
- Verificar que el bucket S3 exista y tenga permisos

## 📞 Soporte

Si necesitas ayuda adicional:
1. Revisa los logs en Render
2. Verifica la configuración de variables de entorno
3. Asegúrate de que todos los archivos estén subidos al repositorio

## 🔒 Seguridad

- Nunca subas credenciales al repositorio
- Usa variables de entorno para todas las claves secretas
- Regenera las claves de AWS si se han comprometido 