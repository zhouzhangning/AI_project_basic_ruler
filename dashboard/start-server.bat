@echo off
chcp 65001 >nul 2>&1
title AI Dev System Dashboard

cd /d "D:\test\AI_project_basic_ruler"

echo.
echo ==============================================
echo   AI Dev System — Dashboard Server
echo ==============================================
echo.
echo   Starting http://127.0.0.1:8765 ...
echo.

REM 尝试多个 Python 路径
set PYTHON=
if exist "C:\Users\HUAWEI\.workbuddy\binaries\python\versions\3.13.12\python.exe" (
    set "PYTHON=C:\Users\HUAWEI\.workbuddy\binaries\python\versions\3.13.12\python.exe"
) else if exist "C:\Python314\python.exe" (
    set "PYTHON=C:\Python314\python.exe"
) else (
    set "PYTHON=python"
)

echo   Python: %PYTHON%
echo.

"%PYTHON%" -c "import flask" 2>nul
if errorlevel 1 (
    echo   正在安装 Flask...
    "%PYTHON%" -m pip install flask --quiet
)

echo   正在启动...
echo.
"%PYTHON%" dashboard\server.py

pause
