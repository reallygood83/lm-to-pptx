import streamlit as st
import os
import sys
import tempfile
from pathlib import Path
from PIL import Image

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.converter import NotebookLMToPPTX

# Page Config
st.set_page_config(
    page_title="NotebookLM to PPTX",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

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
    st.title("Settings")
    
    st.markdown("---")
    
    provider = st.selectbox(
        "AI Provider",
        ("gemini", "openai", "claude", "grok"),
        index=0,
        help="Select the AI intelligence to use."
    )
    
    api_key_env = keys.get(provider, '')
    api_key = st.text_input(
        f"{provider.capitalize()} API Key", 
        value=api_key_env,
        type="password",
        help=f"Enter your {provider} API key if not set in .env"
    )

    st.markdown("---")
    
    st.markdown("### Developer")
    st.markdown("""
    <div style='background: #fff; border: 2px solid #000; padding: 10px; box-shadow: 4px 4px 0 #000;'>
        <b>배움의 달인</b><br>
        <a href='https://www.youtube.com/@%EB%B0%B0%EC%9B%80%EC%9D%98%EB%8B%AC%EC%9D%B8-p5v' style='text-decoration:none; color: red;'>📺 YouTube</a><br>
        <a href='https://x.com/reallygood83' style='text-decoration:none; color: black;'>𝕏 Twitter/X</a>
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

col1, col2 = st.columns(2)
with col1:
    no_notes = st.checkbox("AI 노트 생성 안 함 (빠른 변환)", value=False)
with col2:
    dpi = st.slider("PDF 화질 (DPI)", 72, 300, 144)

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
                    dpi=dpi
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
                
                st.success("✨ 변환 완료!")
                status.update(label="✅변환이 완료되었습니다!", state="complete", expanded=False)
                
                # Download Button
                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 PPTX 다운로드",
                        data=f,
                        file_name=f"{uploaded_file.name.replace('.pdf', '')}.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True
                    )

                # Cleanup
                os.unlink(pdf_path)
                for p in context_paths:
                    os.unlink(p)
                os.unlink(output_path)  # Clean up temp output after reading into memory

            except Exception as e:
                st.error(f"❌ 오류가 발생했습니다: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

