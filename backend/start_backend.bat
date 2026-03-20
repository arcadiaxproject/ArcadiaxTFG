@echo off
setlocal EnableDelayedExpansion

:: Ir al directorio donde está este archivo .bat
cd /d "%~dp0"

:: 1. Obtener IP local automáticamente
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R "IPv4.*"') do (
    set IP=%%a
    set IP=!IP: =!
)

echo IP detectada: %IP%

:: 2. Ruta absoluta al .env del backend
set ENV_PATH=backend\.env

:: 3. Crear o sobrescribir backend\.env
(
    echo IP=%IP%
    echo FRONTEND_ORIGINS=http://%IP%:3000,http://localhost:3000
) > %ENV_PATH%

echo backend\.env creado correctamente con:
type %ENV_PATH%



:: 5. Instalar dependencias si hay requirements.txt
if exist requirements.txt (
    echo Instalando dependencias de Python...
    pip install -r requirements.txt
)

:: 6. Ejecutar backend con Uvicorn
echo Iniciando FastAPI en http://%IP%:8000 ...
start cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"

cd ..
pause
