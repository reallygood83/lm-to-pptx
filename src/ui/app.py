import os
import sys
import tempfile
import platform
import webbrowser
import subprocess
from pathlib import Path
from PIL import Image
import streamlit as st

# Streamlit Cloud에서 상위 모듈을 찾을 수 있도록 루트 경로 추가
current_dir = Path(__file__).parent.absolute()
project_root = current_dir.parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import the core converter using absolute import from root
try:
    from src.converter import NotebookLMToPPTX
except ImportError:
    # Fallback for different environments
    from converter import NotebookLMToPPTX

# Neo-brutalism CSS
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        color: #1A1A2E;
    }
    
    /* Neo-brutalism Colors */
    :root {
        --bg-color: #FEF3E2;
        --card-bg: #FFFFFF;
        --accent-yellow: #FFE135;
        --accent-blue: #4A90D9;
        --accent-pink: #FF6B9D;
        --border-color: #1A1A2E;
        --shadow-offset: 5px;
    }

    /* Main Container */
    .stApp {
        background-color: var(--bg-color);
    }

    /* Cards/Containers */
    .element-container, .stMarkdown {
        background-color: transparent;
    }

    div[data-testid="stFileUploader"] {
        background-color: var(--card-bg);
        border: 3px solid var(--border-color);
        box-shadow: var(--shadow-offset) var(--shadow-offset) 0px var(--border-color);
        padding: 20px;
        border-radius: 0;
        transition: transform 0.1s;
    }

    div[data-testid="stFileUploader"]:hover {
        transform: translate(-2px, -2px);
        box-shadow: 7px 7px 0px var(--border-color);
    }

    /* Buttons */
    div.stButton > button {
        background-color: var(--accent-yellow);
        color: var(--border-color);
        border: 3px solid var(--border-color);
        box-shadow: var(--shadow-offset) var(--shadow-offset) 0px var(--border-color);
        font-weight: 700;
        border-radius: 0;
        padding: 0.5rem 2rem;
        transition: all 0.1s;
    }

    div.stButton > button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 7px 7px 0px var(--border-color);
        background-color: #FFD700;
        color: var(--border-color);
        border-color: var(--border-color);
    }

    div.stButton > button:active {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px var(--border-color);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--border-color);
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: -1px;
    }
    
    h1 {
        background-color: var(--accent-blue);
        border: 3px solid var(--border-color);
        box-shadow: var(--shadow-offset) var(--shadow-offset) 0px var(--border-color);
        padding: 20px;
        color: white;
        text-shadow: 2px 2px 0px var(--border-color);
        transform: rotate(-1deg);
        margin-bottom: 40px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--card-bg);
        border-right: 3px solid var(--border-color);
    }
    
    /* Input Fields */
    input, select, textarea {
        border: 2px solid var(--border-color) !important;
        border-radius: 0 !important;
        background-color: white !important;
    }

    /* Success/Error/Info Messages */
    .stSuccess {
        background-color: #D3F9D8;
        border: 3px solid var(--border-color);
        box-shadow: 4px 4px 0px var(--border-color);
        color: var(--border-color);
    }
    
    .stError {
        background-color: #FFC0CB;
        border: 3px solid var(--border-color);
        box-shadow: 4px 4px 0px var(--border-color);
        color: var(--border-color);
    }

</style>
""", unsafe_allow_html=True)

# Helper function to load API keys
def load_api_keys():
    from dotenv import load_dotenv
    load_dotenv()
    return {
        'gemini': os.getenv('GOOGLE_API_KEY', ''),
        'openai': os.getenv('OPENAI_API_KEY', ''),
        'anthropic': os.getenv('ANTHROPIC_API_KEY', ''),
        'grok': os.getenv('XAI_API_KEY', ''),
    }

keys = load_api_keys()

# Sidebar
with st.sidebar:
    st.image("https://em-content.zobj.net/source/microsoft-teams/363/chart-increasing_1f4c8.png", width=80)
    # Update Function
    def ui_perform_update():
        import subprocess
        try:
            with st.status("🔄 업데이트 진행 중...", expanded=True) as status:
                st.write("Git 저장소 확인 중...")
                if (Path(".git").exists() and Path(".git").is_dir()):
                    st.write("Git Pull 실행...")
                    subprocess.check_call(["git", "pull"])
                    st.write("의존성 업데이트...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
                else:
                    st.write("PIP 업그레이드 실행...")
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", "--upgrade", 
                        "git+https://github.com/reallygood83/lm-to-pptx.git"
                    ])
                status.update(label="✅ 업데이트 완료! 앱을 재실행해주세요.", state="complete", expanded=False)
                st.success("업데이트가 완료되었습니다. 터미널에서 앱을 껐다 켜주세요.")
        except Exception as e:
            st.error(f"업데이트 실패: {str(e)}")

    if st.button("🔄 앱 업데이트 확인", use_container_width=True):
        ui_perform_update()

    st.markdown("---")
    
    # Poppler Installation Section
    st.markdown("### 🛠️ Setup (Poppler)")
    
    import shutil
    poppler_path = shutil.which("pdftoppm") or shutil.which("pdftocairo")
    
    if poppler_path:
        st.success("✅ Poppler가 설치되어 있습니다!")
    else:
        os_name = platform.system()
        if os_name == "Darwin":  # macOS
            if st.button("🍏 Poppler 설치 (Mac)", help="Homebrew를 통해 poppler를 설치합니다.", use_container_width=True):
                try:
                    with st.status("🍏 설치 진행 중...", expanded=True) as status:
                        st.write("Homebrew 확인 중...")
                        subprocess.check_call(["brew", "--version"])
                        st.write("Poppler 설치 시작 (시간이 좀 걸립니다)...")
                        subprocess.check_call(["brew", "install", "poppler"])
                        status.update(label="✅ 설치가 완료되었습니다!", state="complete", expanded=False)
                        st.success("Poppler 설치 완료!")
                        st.rerun() # Refresh to show success
                except subprocess.CalledProcessError:
                    st.error("❌ Homebrew가 없거나 설치 중 오류가 발생했습니다. 터미널에서 'brew install poppler'를 직접 실행해주세요.")
                except Exception as e:
                    st.error(f"❌ 오류: {str(e)}")
                    
        elif os_name == "Windows":
            st.warning("⚠️ Poppler가 없습니다.")
            if st.button("🪟 다운로드 페이지 열기", use_container_width=True):
                webbrowser.open("https://github.com/oschwartz10612/poppler-windows/releases/")
                st.info("💡 링크에서 최신 버전을 받아 압축을 풀고 'bin' 폴더를 환경변수 Path에 추가해주세요.")
        else:
            st.error(f"❌ Poppler가 없습니다. 서버 환경인 경우 'packages.txt'에 'poppler-utils'를 추가하세요.")

    st.markdown("---")
    
    st.markdown("### Settings")
    
    provider = st.selectbox(
        "AI Provider",
        ("gemini", "openai", "claude", "grok"),
        index=0,
        help="Select the AI intelligence to use."
    )
    
    # API Key Handling
    current_key_env = keys.get(provider, '')
    
    # Check session state for key maintenance
    if f"{provider}_key" not in st.session_state:
        st.session_state[f"{provider}_key"] = current_key_env
        
    api_key = st.text_input(
        f"{provider.capitalize()} API Key", 
        value=st.session_state[f"{provider}_key"],
        type="password",
        help=f"Enter your {provider} API key"
    )
    
    # Save API Key Button
    if st.button("💾 API 키 저장 (.env)", use_container_width=True):
        try:
            env_path = Path(".env")
            env_content = ""
            if env_path.exists():
                with open(env_path, "r", encoding="utf-8") as f:
                    env_content = f.read()
            
            # Simple parsing to replace or append
            env_map = {
                'gemini': 'GOOGLE_API_KEY',
                'openai': 'OPENAI_API_KEY',
                'anthropic': 'ANTHROPIC_API_KEY',
                'grok': 'XAI_API_KEY',
            }
            target_var = env_map.get(provider)
            
            if target_var:
                new_line = f"{target_var}={api_key}\n"
                
                # If var exists, replace it
                if target_var in env_content:
                    lines = env_content.splitlines()
                    new_lines = []
                    found = False
                    for line in lines:
                        if line.startswith(f"{target_var}="):
                            new_lines.append(f"{target_var}='{api_key}'")
                            found = True
                        else:
                            new_lines.append(line)
                    env_content = "\n".join(new_lines)
                else:
                    env_content += f"\n{new_line}"
                
                with open(env_path, "w", encoding="utf-8") as f:
                    f.write(env_content)
                
                st.success(f"{provider} API Key가 .env에 저장되었습니다!")
                # Update session state to reflect saved
                st.session_state[f"{provider}_key"] = api_key
        except Exception as e:
            st.error(f"저장 실패: {str(e)}")

    st.markdown("---")
    
    st.markdown("### Developer")
    
    # Custom Button-like Links
    st.markdown("""
    <div style="display: flex; gap: 10px; flex-direction: column;">
        <a href="https://www.youtube.com/@%EB%B0%B0%EC%9B%80%EC%9D%98%EB%8B%AC%EC%9D%B8-p5v" target="_blank" style="text-decoration: none;">
            <div style="background-color: #FF0000; color: white; padding: 10px; text-align: center; border: 2px solid #000; box-shadow: 4px 4px 0px #000; font-weight: bold; transition: all 0.1s;">
                📺 YouTube 구독하기
            </div>
        </a>
        <a href="https://x.com/reallygood83" target="_blank" style="text-decoration: none;">
            <div style="background-color: #000000; color: white; padding: 10px; text-align: center; border: 2px solid #000; box-shadow: 4px 4px 0px #888; font-weight: bold;">
                𝕏 Twitter / X 팔로우
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Main Content
st.title("NotebookLM to PPTX")

st.markdown("""
<div style='background: white; border: 3px solid black; padding: 20px; box-shadow: 5px 5px 0 black; margin-bottom: 30px;'>
    <h3>👋 Welcome!</h3>
    <p><b>NotebookLM PDF</b>를 업로드하면 <b>편집 가능한 PPTX</b>로 변환해드립니다.<br>
    AI가 슬라이드를 분석해 <b>발표자 노트</b>까지 작성해줍니다.</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📂 PDF 파일 업로드", type="pdf")
context_files = st.file_uploader("📚 컨텍스트 자료 (선택사항)", type=["txt", "md", "pdf"], accept_multiple_files=True)

col1, col2, col3 = st.columns(3)
with col1:
    no_notes = st.checkbox("AI 노트 생성 안 함", value=False)
with col2:
    remove_watermark = st.checkbox("워터마크 제거", value=True, help="우측 하단의 NotebookLM 워터마크를 가립니다.")
with col3:
    dpi = st.slider("화질 (DPI)", 72, 300, 144)

if uploaded_file and st.button("🚀 PPTX로 변환 시작", use_container_width=True):
    if not api_key and not no_notes:
        st.error("⚠️ AI API 키가 필요합니다! 사이드바에서 입력하거나 노트 생성을 끄세요.")
    else:
        with st.status("🛠️ 변환 작업 진행 중...", expanded=True) as status:
            try:
                # Save uploaded PDF to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                    tmp_pdf.write(uploaded_file.getvalue())
                    pdf_path = tmp_pdf.name
                
                # Save context files
                context_paths = []
                if context_files:
                    st.write("📚 맥락 자료 처리 중...")
                    for cf in context_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{cf.name.split('.')[-1]}") as tmp_ctx:
                            tmp_ctx.write(cf.getvalue())
                            context_paths.append(tmp_ctx.name)

                # Initialize Converter
                st.write(f"🤖 AI ({provider}) 연결 중...")
                converter = NotebookLMToPPTX(
                    provider=provider,
                    api_key=api_key,
                    dpi=dpi,
                    remove_watermark=remove_watermark
                )

                # Convert
                # Progress bar wrapper
                progress_bar = st.progress(0, text="준비 중...")
                
                def update_progress(current, total):
                    pct = current / total
                    progress_bar.progress(pct, text=f"슬라이드 변환 중... ({current}/{total})")

                st.write("🔄 PDF 변환 및 분석 시작...")
                output_path = converter.convert(
                    pdf_path,
                    output_path=pdf_path.replace(".pdf", ".pptx"),
                    context_paths=context_paths if context_paths else None,
                    generate_notes=not no_notes,
                    progress_callback=update_progress
                )
                
                status.update(label="✅ 변환 프로세스 완료!", state="complete", expanded=False)
                
                # Show results in a Neo-brutalism box
                st.markdown(f"""
                <div style='background: #A3FFAC; border: 3px solid black; padding: 20px; box-shadow: 5px 5px 0 black; margin-top: 20px; margin-bottom: 20px;'>
                    <h3 style='margin-top:0;'>🎉 변환 성공!</h3>
                    <p style='margin-bottom:0;'>파일이 성공적으로 생성되었습니다. 아래 버튼을 눌러 저장하세요.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Download Button
                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 PPTX 파일 저장하기 (여기를 클릭!)",
                        data=f,
                        file_name=f"{uploaded_file.name.replace('.pdf', '')}.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True
                    )
                
                st.info("💡 **어디에 파일이 저장되나요?**\n\n웹 브라우저를 쓰고 계시다면 컴퓨터의 **'다운로드(Downloads)'** 폴더에 저장됩니다. (로컬 터미널에서 실행 시에는 원본 PDF와 같은 폴더에 저장됩니다.)")

                # Cleanup
                try:
                    os.unlink(pdf_path)
                    for p in context_paths:
                        os.unlink(p)
                    os.unlink(output_path)
                except:
                    pass

            except Exception as e:
                st.error(f"❌ 오류가 발생했습니다: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

