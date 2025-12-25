"""
NotebookLM PDF to PPTX Converter CLI
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn
)
from rich.panel import Panel
from rich.theme import Theme

# Import inside the package
from .converter import NotebookLMToPPTX

# 커스텀 테마 (Neo-brutalism 스타일 느낌)
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "title": "bold magenta reverse",
    "panel.border": "white",
})

console = Console(theme=custom_theme)

def parse_args():
    parser = argparse.ArgumentParser(
        description="NotebookLM PDF를 스피커 노트가 포함된 PPTX로 변환합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "pdf_path",
        nargs='?',
        help="변환할 PDF 파일 경로 (업데이트 시 생략 가능)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="출력 PPTX 파일 경로 (기본값: 원본파일명.pptx)"
    )
    
    parser.add_argument(
        "-p", "--provider",
        default="gemini",
        choices=["gemini", "openai", "claude", "anthropic", "grok", "xai"],
        help="사용할 AI 프로바이더 (기본값: gemini)"
    )
    
    parser.add_argument(
        "-m", "--model",
        help="AI 모델명 (지정하지 않으면 프로바이더 기본값 사용)"
    )
    
    parser.add_argument(
        "-k", "--api-key",
        help="API 키 (환경변수보다 우선순위 높음)"
    )
    
    parser.add_argument(
        "-c", "--context",
        action="append",
        help="스피커 노트 생성을 위한 맥락 자료 파일 (.txt, .md, .pdf). 여러 번 사용 가능."
    )
    
    parser.add_argument(
        "--no-notes",
        action="store_true",
        help="AI 스피커 노트 생성을 건너뜁니다 (이미지만 변환)"
    )
    
    parser.add_argument(
        "--ui",
        action="store_true",
        help="웹 기반 GUI 모드로 실행합니다."
    )
    
    parser.add_argument(
        "--dpi",
        type=int,
        default=144,
        help="PDF 변환 해상도 (기본값: 144 DPI)"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="GitHub에서 최신 버전으로 업데이트합니다."
    )
    
    return parser.parse_args()

def perform_update():
    """GitHub에서 최신 버전으로 업데이트 수행"""
    import subprocess
    
    console.print()
    console.print(Panel("[bold cyan]🔄 업데이트 확인 중...[/bold cyan]", border_style="cyan"))
    
    # 1. Git 저장소인지 확인
    is_git = (Path(".git").exists() and Path(".git").is_dir())
    
    try:
        if is_git:
            console.print("[dim]Git 저장소가 감지되었습니다. 'git pull'을 실행합니다...[/dim]")
            subprocess.check_call(["git", "pull"])
            console.print("[dim]의존성을 업데이트합니다...[/dim]")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        else:
            console.print("[dim]pip 패키지 업데이트를 시도합니다...[/dim]")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--upgrade", 
                "git+https://github.com/reallygood83/lm-to-pptx.git"
            ])
            
        console.print(Panel(
            "[success]✨ 업데이트가 완료되었습니다![/success]\n\n"
            "[bold]프로그램을 다시 실행해주세요.[/bold]",
            title="Update Success",
            border_style="green"
        ))
        
    except subprocess.CalledProcessError as e:
        console.print(f"[error]❌ 업데이트 실패:[/error] {str(e)}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[error]❌ 알 수 없는 오류:[/error] {str(e)}")
        sys.exit(1)
    
    sys.exit(0)

def launch_ui():
    """Streamlit UI 실행"""
    import subprocess
    
    ui_path = Path(__file__).parent / "ui" / "app.py"
    if not ui_path.exists():
        console.print(f"[error]❌ UI 파일을 찾을 수 없습니다: {ui_path}[/error]")
        sys.exit(1)
        
    console.print(Panel("[bold cyan]🚀 웹 GUI를 시작합니다...[/bold cyan]", border_style="cyan"))
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(ui_path)], check=True)
    except KeyboardInterrupt:
        console.print("\n[dim]GUI 종료[/dim]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[error]❌ UI 실행 실패:[/error] {str(e)}")
        sys.exit(1)

def main():
    # .env 파일 로드
    load_dotenv()
    
    args = parse_args()
    
    # 업데이트 명령 실행
    if hasattr(args, 'update') and args.update:
        perform_update()
        
    # UI 모드 실행
    if hasattr(args, 'ui') and args.ui:
        launch_ui()
        sys.exit(0)
        
    # 타이틀 출력
    console.print()
    
    # 개발자 정보 및 링크
    youtube_url = "https://www.youtube.com/@%EB%B0%B0%EC%9B%80%EC%9D%98%EB%8B%AC%EC%9D%B8-p5v"
    x_url = "https://x.com/reallygood83"
    
    console.print(Panel.fit(
        "[title] NotebookLM PDF to PPTX Converter v0.4.0 [/title]\n"
        "[dim]Powered by AI Vision (Gemini, OpenAI, Claude, Grok)[/dim]\n\n"
        f"[bold]By 배움의 달인[/bold]\n"
        f"[red]📺 [link={youtube_url}]YouTube[/link][/red]  |  [white]𝕏 [link={x_url}]Twitter/X[/link][/white]",
        border_style="bold white",
        padding=(1, 2)
    ))
    console.print()

    # 입력 파일 확인 (업데이트/UI 모드가 아닐 때만 필수)
    if not args.pdf_path:
        console.print("[warning]사용법: nb2pptx [PDF파일경로] 또는 nb2pptx --ui / --update[/warning]")
        console.print("자세한 도움말은 [bold]nb2pptx --help[/bold]를 참고하세요.")
        sys.exit(0)

    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        console.print(f"[error]❌ 오류: 파일을 찾을 수 없습니다: {pdf_path}[/error]")
        sys.exit(1)
        
    try:
        # 컨버터 초기화
        converter = NotebookLMToPPTX(
            provider=args.provider,
            api_key=args.api_key,
            model=args.model,
            dpi=args.dpi
        )
        
        # 진행률 표시 변수
        progress_bar = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=console
        )
        
        task_id = progress_bar.add_task("준비 중...", total=100)
        
        def update_progress(current, total):
            description = f"슬라이드 변환 중... ({current}/{total})"
            percentage = (current / total) * 100
            progress_bar.update(task_id, description=description, completed=percentage)

        # 변환 시작
        with progress_bar:
            output_path = converter.convert(
                pdf_path,
                output_path=args.output,
                context_paths=args.context,
                generate_notes=not args.no_notes,
                progress_callback=update_progress
            )
            
        console.print()
        console.print(Panel(
            f"[success]✨ 변환이 완료되었습니다![/success]\n\n"
            f"[bold]📂 저장 위치:[/bold] {output_path}",
            title="Success",
            border_style="green"
        ))
        
    except ImportError as e:
        console.print(f"[error]❌ 의존성 오류:[/error] {str(e)}")
        console.print("[dim]pip install -r requirements.txt 명령어로 필요한 패키지를 설치하세요.[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[error]❌ 변환 중 오류 발생:[/error] {str(e)}")
        # 상세 오류 출력을 위해 traceback 모듈 사용 가능
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)

if __name__ == "__main__":
    main()
