# 🚀 Guía de Configuración del Proyecto Badgers Admin

## 📋 Resumen del Proyecto

Este es un proyecto full-stack que incluye:
- **Frontend**: React + Vite (puerto 5173)
- **Backend**: Django REST API (puerto 8000)
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Almacenamiento**: AWS S3 para archivos

## 🔧 Configuración Inicial

### 1. Configurar Variables de Entorno del Backend

1. Ve a la carpeta `backend/`
2. Copia el archivo `env_template.txt` como `.env`:
   ```bash
   cp env_template.txt .env
   ```
3. Edita el archivo `.env` con tus configuraciones:
   ```bash
   nano .env
   ```

### 2. Configurar Variables de Entorno del Frontend

1. En la carpeta raíz del proyecto
2. Copia el archivo `frontend_env_template.txt` como `.env`:
   ```bash
   cp frontend_env_template.txt .env
   ```
3. Edita el archivo `.env` con tus configuraciones:
   ```bash
   nano .env
   ```

## 🐍 Configuración del Backend (Django)

### 1. Crear Entorno Virtual

```bash
cd backend/
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Base de Datos

Para desarrollo local (SQLite):
```bash
python manage.py migrate
```

Para producción (PostgreSQL):
1. Instala PostgreSQL
2. Crea una base de datos
3. Configura `DATABASE_URL` en el archivo `.env`
4. Ejecuta las migraciones

### 4. Crear Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

### 5. Ejecutar el Servidor

```bash
python manage.py runserver
```

El backend estará disponible en: http://localhost:8000

## ⚛️ Configuración del Frontend (React)

### 1. Instalar Dependencias

```bash
npm install
# o
yarn install
```

### 2. Ejecutar en Modo Desarrollo

```bash
npm run dev
# o
yarn dev
```

El frontend estará disponible en: http://localhost:5173

## 🔐 Configuración de AWS S3 (Opcional)

Si quieres usar AWS S3 para almacenamiento de archivos:

### 1. Crear Bucket S3

1. Ve a AWS Console → S3
2. Crea un nuevo bucket
3. Configura los permisos necesarios

### 2. Crear Usuario IAM

1. Ve a AWS Console → IAM
2. Crea un nuevo usuario
3. Asigna permisos de S3
4. Genera Access Key y Secret Key

### 3. Configurar Variables de Entorno

En el archivo `backend/.env`:
```env
AWS_ACCESS_KEY_ID=tu_access_key_id
AWS_SECRET_ACCESS_KEY=tu_secret_access_key
AWS_STORAGE_BUCKET_NAME=nombre-de-tu-bucket
AWS_S3_REGION_NAME=us-east-2
```

## 📁 Estructura de Archivos Importantes

```
Badgers-Admin/
├── backend/
│   ├── .env                    # Variables de entorno del backend
│   ├── env_template.txt        # Template para .env
│   ├── manage.py              # Script de gestión de Django
│   ├── requirements.txt       # Dependencias de Python
│   └── badgers_project/
│       ├── settings.py        # Configuración principal
│       └── settings_local.py  # Configuración local
├── .env                       # Variables de entorno del frontend
├── frontend_env_template.txt  # Template para .env del frontend
├── package.json              # Dependencias de Node.js
└── vite.config.js           # Configuración de Vite
```

## 🚀 Comandos Útiles

### Backend
```bash
# Ejecutar migraciones
python manage.py migrate

# Crear migraciones
python manage.py makemigrations

# Ejecutar servidor
python manage.py runserver

# Shell de Django
python manage.py shell

# Crear superusuario
python manage.py createsuperuser
```

### Frontend
```bash
# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev

# Construir para producción
npm run build

# Vista previa de producción
npm run preview
```

## 🔧 Solución de Problemas Comunes

### Error de CORS
- Verifica que las URLs en `CORS_ALLOWED_ORIGINS` sean correctas
- Asegúrate de que el frontend y backend estén en los puertos correctos

### Error de Base de Datos
- Verifica que SQLite esté instalado
- Para PostgreSQL, asegúrate de que la base de datos esté creada

### Error de AWS S3
- Verifica las credenciales de AWS
- Asegúrate de que el bucket tenga los permisos correctos
- Si no tienes S3, el proyecto usará almacenamiento local

### Error de Dependencias
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs del servidor
2. Verifica que todas las variables de entorno estén configuradas
3. Asegúrate de que los puertos no estén ocupados
4. Revisa la documentación de Django y React

## 🔒 Seguridad

- **NUNCA** subas archivos `.env` al repositorio
- Regenera las claves secretas para producción
- Usa HTTPS en producción
- Configura variables de entorno en tu servidor de producción 