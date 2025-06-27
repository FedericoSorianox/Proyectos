# 🎯 Resumen de Configuración - Badgers Admin

## ✅ Archivos Creados

He creado los siguientes archivos para facilitar la configuración:

### 📁 Archivos de Configuración
- `backend/env_template.txt` - Template para variables de entorno del backend
- `frontend_env_template.txt` - Template para variables de entorno del frontend
- `SETUP_INSTRUCTIONS.md` - Guía completa de configuración
- `QUICK_START.md` - Inicio rápido
- `setup.sh` - Script automático para macOS/Linux
- `setup.bat` - Script automático para Windows

## 🚀 Pasos para Configurar el Proyecto

### Opción 1: Configuración Automática (Recomendado)

#### En macOS/Linux:
```bash
cd Badgers-Admin
./setup.sh
```

#### En Windows:
```cmd
cd Badgers-Admin
setup.bat
```

### Opción 2: Configuración Manual

#### 1. Crear archivos .env

**Backend:**
```bash
cd Badgers-Admin/backend/
cp env_template.txt .env
```

**Frontend:**
```bash
cd Badgers-Admin/
cp frontend_env_template.txt .env
```

#### 2. Configurar Backend
```bash
cd Badgers-Admin/backend/
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### 3. Configurar Frontend
```bash
cd Badgers-Admin/
npm install  # o yarn install
npm run dev  # o yarn dev
```

## 🔧 Variables de Entorno Mínimas

### Backend (backend/.env)
```env
SECRET_KEY=django-insecure-hl!998$#)*zpak-)bamp+4$#2a1mh77zyf!$ar+gii6(8*ose4
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_DEV_MODE=true
VITE_APP_URL=http://localhost:5173
```

## 🌐 URLs de Acceso

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

## 📋 Lo que está en el .gitignore

Según el archivo `.gitignore`, los siguientes archivos NO se suben al repositorio:

### Archivos de Entorno
- `backend/badgers_project/.env`
- `backend/.env`
- `.env` (frontend)

### Archivos de Desarrollo
- `node_modules/`
- `dist/`
- `dist-ssr/`
- `*.local`
- `logs/`
- `*.log`

### Archivos del Sistema
- `.DS_Store`
- `.vscode/`
- `.idea/`
- `*.suo`
- `*.ntvs*`
- `*.njsproj`
- `*.sln`
- `*.sw?`

## 🔐 Configuración de AWS S3 (Opcional)

Si quieres usar AWS S3 para almacenamiento de archivos, agrega estas variables al archivo `backend/.env`:

```env
AWS_ACCESS_KEY_ID=tu_access_key_id
AWS_SECRET_ACCESS_KEY=tu_secret_access_key
AWS_STORAGE_BUCKET_NAME=nombre-de-tu-bucket
AWS_S3_REGION_NAME=us-east-2
```

## 📚 Documentación Disponible

- `QUICK_START.md` - Inicio rápido
- `SETUP_INSTRUCTIONS.md` - Guía completa
- `README.md` - Documentación original del proyecto
- `CSV_IMPORT_FORMATS.md` - Formatos para importar datos
- `AWS_S3_SETUP.md` - Configuración de AWS S3

## 🆘 Solución de Problemas Comunes

### Error de CORS
Verifica que `http://localhost:5173` esté en `CORS_ALLOWED_ORIGINS`

### Error de Dependencias
```bash
# Backend
cd backend/
source venv/bin/activate
pip install -r requirements.txt

# Frontend
npm install
```

### Puerto Ocupado
- Backend: `python manage.py runserver 8001`
- Frontend: Cambia en `vite.config.js`

## 🎉 ¡Listo!

Una vez configurado, podrás:
1. Ejecutar el backend en http://localhost:8000
2. Ejecutar el frontend en http://localhost:5173
3. Acceder al admin de Django en http://localhost:8000/admin
4. Importar datos usando los formatos en `CSV_IMPORT_FORMATS.md`
5. Configurar AWS S3 si es necesario

¡El proyecto está listo para usar! 🚀 