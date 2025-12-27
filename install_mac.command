#!/bin/bash

# ============================================================
# NotebookLM PDF to PPTX 변환기 - Mac 원클릭 설치
# ============================================================

# 스크립트 디렉토리로 이동
cd "$(dirname "$0")"
INSTALL_DIR="$(pwd)"

echo ""
echo "============================================================"
echo "  NotebookLM PDF to PPTX 변환기 - 설치 프로그램"
echo "  by 배움의 달인"
echo "============================================================"
echo ""

# ------------------------------------------------------------
# 1단계: Homebrew 설치 확인
# ------------------------------------------------------------
echo "[1/6] Homebrew 설치 확인 중..."
if ! command -v brew &> /dev/null; then
    echo ""
    echo "❌ Homebrew가 설치되어 있지 않습니다."
    echo ""
    echo "📥 Homebrew를 설치할까요? (Y/N)"
    read -r INSTALL_BREW
    if [[ "$INSTALL_BREW" =~ ^[Yy]$ ]]; then
        echo "Homebrew 설치 중..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

        # Apple Silicon Mac의 경우 PATH 설정
        if [[ $(uname -m) == 'arm64' ]]; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
    else
        echo "Homebrew 없이 계속하려면 Python이 이미 설치되어 있어야 합니다."
    fi
fi

if command -v brew &> /dev/null; then
    echo "✅ Homebrew 발견: $(brew --version | head -n 1)"
fi

# ------------------------------------------------------------
# 2단계: Python 설치 확인
# ------------------------------------------------------------
echo ""
echo "[2/6] Python 설치 확인 중..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "❌ Python이 설치되어 있지 않습니다."
    echo ""
    if command -v brew &> /dev/null; then
        echo "📥 Homebrew로 Python 설치 중..."
        brew install python
    else
        echo "Python을 수동으로 설치해주세요: https://www.python.org/downloads/"
        open "https://www.python.org/downloads/"
        exit 1
    fi
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo "✅ $PYTHON_VERSION 발견"

# ------------------------------------------------------------
# 3단계: Poppler 설치
# ------------------------------------------------------------
echo ""
echo "[3/6] Poppler 설치 확인 중..."
if ! command -v pdftoppm &> /dev/null; then
    echo "📥 Poppler 설치 중 (PDF 변환에 필요)..."
    if command -v brew &> /dev/null; then
        brew install poppler
        echo "✅ Poppler 설치 완료"
    else
        echo "⚠️  Poppler를 수동으로 설치해주세요: brew install poppler"
    fi
else
    echo "✅ Poppler 이미 설치됨"
fi

# ------------------------------------------------------------
# 4단계: pip 업그레이드
# ------------------------------------------------------------
echo ""
echo "[4/6] pip 업그레이드 중..."
python3 -m pip install --upgrade pip --quiet
echo "✅ pip 업그레이드 완료"

# ------------------------------------------------------------
# 5단계: 필수 패키지 설치
# ------------------------------------------------------------
echo ""
echo "[5/6] 필수 패키지 설치 중... (약 1-3분 소요)"
echo "    - python-pptx (PowerPoint 생성)"
echo "    - pdf2image (PDF 변환)"
echo "    - streamlit (웹 UI)"
echo "    - AI 라이브러리들..."
echo ""

python3 -m pip install python-pptx pdf2image Pillow google-generativeai openai anthropic pymupdf python-dotenv rich streamlit --quiet

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 패키지 설치 중 오류가 발생했습니다."
    echo "   다시 시도해주세요."
    exit 1
fi

python3 -m pip install -e . --quiet
echo "✅ 필수 패키지 설치 완료"

# ------------------------------------------------------------
# 6단계: 바탕화면 앱 생성
# ------------------------------------------------------------
echo ""
echo "[6/6] 바탕화면 실행 파일 생성 중..."

# 실행 스크립트 생성
cat > "$INSTALL_DIR/NotebookLM변환기.command" << 'SCRIPT'
#!/bin/bash
cd "$(dirname "$0")"
echo ""
echo "============================================================"
echo "  NotebookLM PDF to PPTX 변환기 시작 중..."
echo "============================================================"
echo ""
python3 -m streamlit run src/ui/app.py
SCRIPT

chmod +x "$INSTALL_DIR/NotebookLM변환기.command"

# 바탕화면에 복사
DESKTOP="$HOME/Desktop"
if [ -d "$DESKTOP" ]; then
    cp "$INSTALL_DIR/NotebookLM변환기.command" "$DESKTOP/"
    chmod +x "$DESKTOP/NotebookLM변환기.command"
    echo "✅ 바탕화면에 'NotebookLM변환기.command' 생성 완료!"
else
    echo "⚠️  바탕화면을 찾을 수 없습니다. 수동으로 복사해주세요."
fi

# ------------------------------------------------------------
# 완료!
# ------------------------------------------------------------
echo ""
echo "============================================================"
echo "  🎉 설치 완료!"
echo "============================================================"
echo ""
echo "  🎮 실행 방법:"
echo "  ---------------------------------------------------------"
echo "  바탕화면의 'NotebookLM변환기.command' 더블클릭!"
echo ""
echo "  또는 터미널에서:"
echo "  cd $INSTALL_DIR"
echo "  python3 -m streamlit run src/ui/app.py"
echo ""
echo "============================================================"
echo ""

# 지금 실행할지 물어보기
echo "지금 바로 프로그램을 실행할까요? (Y/N)"
read -r RUN_NOW
if [[ "$RUN_NOW" =~ ^[Yy]$ ]]; then
    echo ""
    echo "프로그램 시작 중..."
    python3 -m streamlit run src/ui/app.py
fi
