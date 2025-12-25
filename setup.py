from setuptools import setup, find_packages

setup(
    name="notebooklm-pptx",
    version="0.4.0",
    description="Convert NotebookLM PDF slides to editable PPTX with AI-generated speaker notes.",
    author="배움의 달인",
    packages=find_packages(),
    install_requires=[
        "pdf2image>=1.17.0",
        "python-pptx>=0.6.23",
        "Pillow>=10.0.0",
        "google-generativeai>=0.8.0",
        "openai>=1.60.0",
        "anthropic>=0.45.0",
        "pymupdf>=1.25.0",
        "python-dotenv>=1.0.0",
        "rich>=13.9.0",
        "streamlit>=1.30.0",
    ],
    entry_points={
        "console_scripts": [
            "nb2pptx=src.cli:main",
            "nb2pptx-ui=src.cli:launch_ui",
            "notebooklm-pptx=src.cli:main",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
