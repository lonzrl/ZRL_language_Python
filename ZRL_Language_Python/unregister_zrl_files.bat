@echo off
chcp 65001 >nul
echo === ZRL File Association Unregister Tool ===
echo.
echo This tool will unregister .z file type association
echo.
echo Administrator privileges are required to modify registry
echo.

pause

cd /d "%~dp0"

echo Unregistering .z file type...
python register_filetype.py --unregister

if %errorlevel% equ 0 (
    echo.
    echo Unregistration successful!
) else (
    echo.
    echo Unregistration failed, please run this script as Administrator
)

echo.
pause