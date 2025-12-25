# NotebookLM PDF to PPTX Converter v0.4.0

A powerful tool to convert NotebookLM-generated PDF slides into editable PowerPoint presentations (`.pptx`) with **AI-generated speaker notes**.

## Features

- **High-Quality Conversion**: Converts PDF slides to high-resolution full-slide images in PowerPoint.
- **AI Speaker Notes**: Automatically analyzes each slide using AI Vision to generate detailed speaker notes.
  - Supports **Gemini** (default), **OpenAI** (GPT-4o), **Claude** (Sonnet), and **Grok**.
- **Context Materials**: usage of additional context files (`.txt`, `.md`, `.pdf`) to guide the AI for better quality notes.
- **CLI Interface**: Robust command-line interface with progress tracking.

## Installation

### Option 1: Install from Source (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/notebooklm-to-pptx.git
   cd notebooklm-to-pptx
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Mac/Linux
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

4. Install system dependencies for PDF conversion:
   - **macOS**: `brew install poppler`
   - **Ubuntu**: `sudo apt-get install poppler-utils`
   - **Windows**: Download and add poppler to PATH.

### Option 2: Install via pip (once published)

```bash
pip install notebooklm-pptx
```

## Configuration

Copy `.env.example` to `.env` and add your API keys:
```bash
cp .env.example .env
```
Edit `.env` with your API key for the chosen provider (e.g., `GOOGLE_API_KEY`).

## Usage

After installation, you can use the `nb2pptx` command from anywhere:

```bash
nb2pptx slides.pdf
```

Specify provider and context materials:
```bash
nb2pptx slides.pdf --provider openai --context notes.txt
```

No speaker notes (only convert images):
```bash
nb2pptx slides.pdf --no-notes
```

## Options

| Option | Description |
|--------|-------------|
| `--provider`, `-p` | AI provider: `gemini` (default), `openai`, `claude`, `grok` |
| `--context`, `-c` | Context file paths (can be used multiple times) |
| `--no-notes` | Skip AI speaker note generation |
| `--model`, `-m` | Specify a custom model name |
| `--dpi` | PDF rendering resolution (default: 144) |

## License

MIT
