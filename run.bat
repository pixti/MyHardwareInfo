@echo off
chcp 65001 >nul

set PROJECT_DIR=%~dp0
cd /d %PROJECT_DIR%

echo [1/2] My Hardware Info 가상환경 확인 중...
set VENV_PYTHON="%PROJECT_DIR%.venv\Scripts\python.exe"

if not exist %VENV_PYTHON% (
    echo [오류] .venv 폴더를 찾을 수 없습니다. 파이참에서 가상환경을 먼저 생성해주세요.
    pause
    exit
)

echo [2/2] 프로그램 실행 중...
%VENV_PYTHON% main.py

if %errorlevel% neq 0 (
    echo.
    echo [알림] 프로그램이 비정상 종료되었습니다. 위에 표시된 에러 내용을 확인하세요.
    pause
)