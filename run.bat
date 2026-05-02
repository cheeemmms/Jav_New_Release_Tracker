@echo off
chcp 65001 >nul
cd /d "%~dp0"

python src\main.py
if %errorlevel% neq 0 (
    py -3 src\main.py
)

pause
