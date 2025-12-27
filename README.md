# 📊 NotebookLM PDF → PPTX 변환기 (nb2pptx)

> **"NotebookLM의 똑똑한 지식을 가장 완벽한 발표 자료로 만드는 방법"**

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

NotebookLM에서 생성된 PDF는 훌륭하지만, 실제 발표에서 사용하기엔 **수정이 불가능**하고 **발표 대본(말할 거리)**이 없다는 단점이 있습니다. 이 도구는 그 문제를 완벽하게 해결합니다.

---

## 🔥 핵심 가치 (Why nb2pptx?)

1.  **말랑말랑한 PPTX**: 꽁꽁 얼어있는 PDF 슬라이드를 파워포인트에서 마음껏 수정 가능한 PPTX 파일로 바꿔드립니다.
2.  **AI 발표 작가**: Gemini, GPT-4, Claude 등 최고의 AI들이 슬라이드 한 장 한 장을 분석하여 품격 있는 발표자 노트를 자동으로 써줍니다.
3.  **전문가급 퀄리티**: 16:9 표준 규격 지원 및 Neo-brutalism 디자인의 깔끔한 사용자 인터페이스를 제공합니다.

---

## 🚀 설치 가이드

### 📌 운영체제별 바로가기
- [🪟 **Windows 사용자**](#-windows-설치)
- [🍎 **Mac 사용자**](#-mac-설치)

---

## 🪟 Windows 설치

### 1단계: Python 설치 (필수)

👉 **[Python 다운로드 페이지 바로가기](https://www.python.org/downloads/)**

1. 위 링크에서 **Download Python 3.x.x** 클릭
2. 다운로드된 파일 실행
3. ⚠️ **중요!** 설치 화면 하단 **"Add Python to PATH"** 반드시 체크! ⚠️
4. **Install Now** 클릭

### 2단계: 프로그램 다운로드

👉 **[ZIP 파일 직접 다운로드](https://github.com/reallygood83/lm-to-pptx/archive/refs/heads/main.zip)**

1. 위 링크 클릭하여 ZIP 다운로드
2. 바탕화면에 압축 해제
3. 폴더명을 `lm-to-pptx`로 변경

### 3단계: 원클릭 설치 ⭐

1. `lm-to-pptx` 폴더 열기
2. **`install_windows.bat`** 더블클릭!
3. 자동으로 모든 패키지 설치됨
4. **바탕화면에 `NotebookLM변환기.bat` 생성!**

### 4단계: Poppler 설치 (필수)

👉 **[Poppler 다운로드 페이지](https://github.com/oschwartz10612/poppler-windows/releases)**

1. 위 링크에서 **Release-xx.xx.x-x.zip** 다운로드
2. 압축 해제 → `C:\poppler` 폴더로 이동
3. 환경변수 PATH에 `C:\poppler\Library\bin` 추가
   - `Win + S` → "환경 변수" 검색 → Path 편집 → 새로 만들기

### 🎮 실행 방법 (Windows)
바탕화면의 **`NotebookLM변환기.bat`** 더블클릭!

---

## 🍎 Mac 설치

### 1단계: 원클릭 설치 ⭐

👉 **[ZIP 파일 직접 다운로드](https://github.com/reallygood83/lm-to-pptx/archive/refs/heads/main.zip)**

1. 위 링크에서 ZIP 다운로드 후 바탕화면에 압축 해제
2. `lm-to-pptx` 폴더 열기
3. **`install_mac.command`** 더블클릭!
4. 자동으로 Homebrew, Python, Poppler, 패키지 모두 설치됨
5. **바탕화면에 `NotebookLM변환기.command` 생성!**

> ⚠️ "확인되지 않은 개발자" 경고 시: `시스템 설정` → `개인정보 보호 및 보안` → **"확인 없이 열기"**

### 🎮 실행 방법 (Mac)
바탕화면의 **`NotebookLM변환기.command`** 더블클릭!

---

## 🔧 첫 실행 설정

앱이 브라우저에서 열리면 왼쪽 **[사이드바]**에서 설정:

1. **Poppler 상태 확인**: ✅ 초록색이면 OK
2. **API 키 입력**: [Google AI Studio](https://aistudio.google.com/app/apikey)에서 무료 발급 → 입력 → **[💾 저장]**

---

## 💻 수동 설치 (고급 사용자용)

터미널/CMD에서:

```bash
git clone https://github.com/reallygood83/lm-to-pptx.git
cd lm-to-pptx
pip install -e .
nb2pptx --ui
```

---

## 🌐 서버에 배포하여 웹 서비스로 만들기 (고수용)

내 컴퓨터뿐만 아니라 **다른 사람들도 링크만 있으면 접속**하게 하고 싶나요? **Streamlit Cloud**를 이용하면 1분 만에 무료로 웹 서비스를 만들 수 있습니다.

1.  **GitHub에 소스 코드 올리기**: (이미 이 저장소를 포크하셨다면 완료!)
2.  **Streamlit Cloud 가입**: [share.streamlit.io](https://share.streamlit.io/)에 접속하여 깃허브 계정으로 로그인합니다.
3.  **New App 생성**: 내 저장소를 선택하고 메인 파일 경로를 `src/ui/app.py`로 지정합니다.
4.  **배포 완료**: 잠시 기다리면 전용 URL(예: `https://nb2pptx.streamlit.app`)이 생성됩니다!

> **팁 💡**: 이미 프로젝트 루트에 `packages.txt` 파일을 만들어 두었기 때문에, 서버가 알아서 Poppler(PDF 전용 엔진)를 설치해줍니다. 여러분은 그냥 배포 버튼만 누르면 됩니다!

---

## 🎮 주요 기능 가이드

### 1. 웹 GUI 모드 (가장 추천!)
*   드래그 앤 드롭으로 PDF 업로드
*   참고할 보조 자료(텍스트/PDF) 추가 가능
*   AI 모델(Gemini, Claude, GPT-4 등) 자유 선택
*   버튼 클릭 한 번으로 최신 버전 업데이트

### 2. 터미널(CLI) 모드 (고수용)
빠르게 대량 작업을 하고 싶을 때 유용합니다.
```bash
# 기본 변환
nb2pptx 내자료.pdf

# 특정 AI 지정 및 참고자료 포함
nb2pptx 내자료.pdf -p gemini --context 보조자료.txt
```

---

## 🔑 AI API 키 발급 받는 법 (처음이라면!)

1.  **Google Gemini (강력 추천/무료)**: [Google AI Studio](https://aistudio.google.com/app/apikey)에서 발급
2.  **OpenAI (GPT-4)**: [OpenAI Platform](https://platform.openai.com/api-keys)에서 발급
3.  **Anthropic (Claude)**: [Anthropic Console](https://console.anthropic.com/)에서 발급

---

## ❓ 자주 묻는 질문 (FAQ)

**Q: 갑자기 작동이 안 돼요!**  
A: `nb2pptx --ui` 실행 후 왼쪽 메뉴의 **[🔄 앱 업데이트 확인]** 버튼을 눌러 최신 버전으로 업데이트 해보세요.

**Q: 윈도우에서 'Poppler' 설정이 너무 어려워요.**  
A: 유튜브에 "윈도우 poppler 환경변수"라고 검색하시거나, `nb2pptx --ui` 왼쪽 하단의 안내 링크를 차근차근 따라 해보세요. 한번만 설정하면 평생 편합니다!

---

## 🆘 문제 해결 (Troubleshooting)

| 발생한 메시지 | 원인 | 해결책 |
| :--- | :--- | :--- |
| `Poppler not found` | PDF 렌즈 미설치 | macOS: `brew install poppler` / Win: 바이너리 다운로드 후 Path 등록 |
| `API key missing` | AI 출입증 없음 | 사이드바에 API 키를 넣고 '저장' 버튼을 누르세요 |
| `Command not found` | 설치 미완료 | `pip install -e .` 명령어를 다시 실행해보세요 |

---

## 📬 커뮤니티 & 지원

만든 사람: **배움의 달인**  
이 도구가 도움이 되셨다면 유튜브 구독과 트위터 팔로우로 응원해주세요!

*   📺 **YouTube**: [@배움의달인](https://www.youtube.com/@%EB%B0%B0%EC%9B%80%EC%9D%98%EB%8B%AC%EC%9D%B8-p5v)
*   𝕏 **X (Twitter)**: [@reallygood83](https://x.com/reallygood83)

---

> *"여러분의 발표가 더 쉽고 즐거워지길 응원합니다!"*
