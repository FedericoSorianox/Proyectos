# 🚀 Inicio Rápido - Badgers Admin

## ⚡ Configuración Automática (Recomendado)

### Para macOS/Linux:
```bash
./setup.sh
```

### Para Windows:
```cmd
setup.bat
```

## 🔧 Configuración Manual

Si prefieres configurar manualmente o el script automático no funciona:

### 1. Variables de Entorno

#### Backend (Django)
```bash
cd backend/
cp env_template.txt .env
# Edita el archivo .env con tus configuraciones
```

#### Frontend (React)
```bash
cp frontend_env_template.txt .env
# Edita el archivo .env con tus configuraciones
```

### 2. Backend (Django)

```bash
cd backend/

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
python manage.py migrate

# Ejecutar servidor
python manage.py runserver
```

### 3. Frontend (React)

```bash
# Instalar dependencias
npm install
# o
yarn install

# Ejecutar en desarrollo
npm run dev
# o
yarn dev
```

## 🌐 URLs de Acceso

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

## 📋 Variables de Entorno Mínimas

### Backend (.env)
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

## 🔧 Solución de Problemas

### Error: "No module named 'django'"
```bash
cd backend/
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Cannot find module"
```bash
npm install
# o
yarn install
```

### Error de CORS
Verifica que las URLs en `CORS_ALLOWED_ORIGINS` incluyan `http://localhost:5173`

### Puerto ocupado
- Backend: Cambia el puerto con `python manage.py runserver 8001`
- Frontend: Cambia el puerto en `vite.config.js`

## 📚 Documentación Completa

Para información detallada, consulta:
- `SETUP_INSTRUCTIONS.md` - Guía completa de configuración
- `README.md` - Documentación del proyecto original
- `CSV_IMPORT_FORMATS.md` - Formatos para importar datos
- `AWS_S3_SETUP.md` - Configuración de AWS S3

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs del servidor
2. Verifica que todas las variables de entorno estén configuradas
3. Asegúrate de que los puertos no estén ocupados
4. Consulta la documentación completa en `SETUP_INSTRUCTIONS.md` 