@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: ============================================================
:: NotebookLM PDF to PPTX 변환기 - Windows 원클릭 설치
:: ============================================================

title NotebookLM 변환기 설치

echo.
echo ============================================================
echo   NotebookLM PDF to PPTX 변환기 - 설치 프로그램
echo   by 배움의 달인
echo ============================================================
echo.

:: ------------------------------------------------------------
:: 1단계: Python 설치 확인
:: ------------------------------------------------------------
echo [1/5] Python 설치 확인 중...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python이 설치되어 있지 않습니다!
    echo.
    echo 📥 Python 다운로드 페이지를 열겠습니다.
    echo    설치 시 반드시 "Add Python to PATH" 체크박스를 선택하세요!
    echo.
    start https://www.python.org/downloads/
    echo Python 설치 후 이 파일을 다시 실행해주세요.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% 발견

:: ------------------------------------------------------------
:: 2단계: pip 업그레이드
:: ------------------------------------------------------------
echo.
echo [2/5] pip 업그레이드 중...
python -m pip install --upgrade pip --quiet
echo ✅ pip 업그레이드 완료

:: ------------------------------------------------------------
:: 3단계: 필수 패키지 설치
:: ------------------------------------------------------------
echo.
echo [3/5] 필수 패키지 설치 중... (약 1-3분 소요)
echo     - python-pptx (PowerPoint 생성)
echo     - pdf2image (PDF 변환)
echo     - streamlit (웹 UI)
echo     - AI 라이브러리들...
echo.

python -m pip install python-pptx pdf2image Pillow google-generativeai openai anthropic pymupdf python-dotenv rich streamlit --quiet

if %errorlevel% neq 0 (
    echo.
    echo ❌ 패키지 설치 중 오류가 발생했습니다.
    echo    다시 시도해주세요.
    pause
    exit /b 1
)
echo ✅ 필수 패키지 설치 완료

:: ------------------------------------------------------------
:: 4단계: 현재 폴더에 설치
:: ------------------------------------------------------------
echo.
echo [4/5] 프로그램 설치 중...
python -m pip install -e . --quiet
echo ✅ 프로그램 설치 완료

:: ------------------------------------------------------------
:: 5단계: 바탕화면 바로가기 생성
:: ------------------------------------------------------------
echo.
echo [5/5] 바탕화면 바로가기 생성 중...

:: 현재 디렉토리 저장
set "INSTALL_DIR=%cd%"

:: 바탕화면 경로
set "DESKTOP=%USERPROFILE%\Desktop"

:: 실행 스크립트 생성
echo @echo off > "%INSTALL_DIR%\NotebookLM변환기.bat"
echo chcp 65001 ^>nul >> "%INSTALL_DIR%\NotebookLM변환기.bat"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\NotebookLM변환기.bat"
echo echo. >> "%INSTALL_DIR%\NotebookLM변환기.bat"
echo echo ============================================================ >> "%INSTALL_DIR%\NotebookLM변환기.bat"
echo echo   NotebookLM PDF to PPTX 변환기 시작 중... >> "%INSTALL_DIR%\NotebookLM변환기.bat"
echo echo ============================================================ >> "%INSTALL_DIR%\NotebookLM변환기.bat"
echo echo. >> "%INSTALL_DIR%\NotebookLM변환기.bat"
echo python -m streamlit run src/ui/app.py >> "%INSTALL_DIR%\NotebookLM변환기.bat"
echo pause >> "%INSTALL_DIR%\NotebookLM변환기.bat"

:: 바탕화면에 복사
copy "%INSTALL_DIR%\NotebookLM변환기.bat" "%DESKTOP%\NotebookLM변환기.bat" >nul 2>&1

if exist "%DESKTOP%\NotebookLM변환기.bat" (
    echo ✅ 바탕화면에 'NotebookLM변환기.bat' 바로가기가 생성되었습니다!
) else (
    echo ⚠️  바탕화면 바로가기 생성 실패. 수동으로 복사해주세요.
    echo    위치: %INSTALL_DIR%\NotebookLM변환기.bat
)

:: ------------------------------------------------------------
:: 완료!
:: ------------------------------------------------------------
echo.
echo ============================================================
echo   🎉 설치 완료!
echo ============================================================
echo.
echo   📌 중요: Poppler 설치가 필요합니다!
echo   ---------------------------------------------------------
echo   PDF를 이미지로 변환하려면 Poppler가 필요합니다.
echo.
echo   1. 아래 링크에서 poppler-xx.xx.x_x.zip 다운로드:
echo      https://github.com/oschwartz10612/poppler-windows/releases
echo.
echo   2. 압축 해제 후 bin 폴더를 환경변수 PATH에 추가
echo      (예: C:\poppler\bin)
echo.
echo   🎮 실행 방법:
echo   ---------------------------------------------------------
echo   바탕화면의 'NotebookLM변환기.bat' 더블클릭!
echo.
echo   또는 이 폴더에서:
echo   python -m streamlit run src/ui/app.py
echo.
echo ============================================================
echo.

:: Poppler 다운로드 페이지 열기
set /p OPEN_POPPLER="Poppler 다운로드 페이지를 열까요? (Y/N): "
if /i "%OPEN_POPPLER%"=="Y" (
    start https://github.com/oschwartz10612/poppler-windows/releases
)

echo.
set /p RUN_NOW="지금 바로 프로그램을 실행할까요? (Y/N): "
if /i "%RUN_NOW%"=="Y" (
    echo.
    echo 프로그램 시작 중...
    python -m streamlit run src/ui/app.py
)

pause
