@echo off
echo ============================================
echo   RyR Port Checker - Agente Local
echo   Dejá esta ventana abierta mientras usás
echo   la web. Cerrala cuando termines.
echo ============================================
echo.
python "%~dp0port_checker.py"
if errorlevel 1 (
    echo.
    echo ERROR: No se encontró Python instalado.
    echo Descargalo desde https://www.python.org
    pause
)
