@echo off
setlocal EnableDelayedExpansion

:: Obtener IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R "IPv4.*"') do (
    set IP=%%a
    set IP=!IP: =!
)

echo IP detectada: %IP%

:: Crear o actualizar client_responsive\.env
(
    echo REACT_APP_BACKEND_URL=http://%IP%:8000
) > client_responsive\.env

cd client_responsive

:: Instalar dependencias de React si no están
if exist package.json (
    echo Instalando dependencias del frontend...
    call npm install
)

:: Ejecutar frontend
echo Iniciando frontend...
start cmd /k "npm start"
cd ..
