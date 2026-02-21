# passifypdf
Use passifypdf to protect your PDF files with a password of your choice. 
Same as encrypt or lock your PDF via a password.

## Before & After:
<img width="1534" alt="Pasted Graphic 100" src="https://github.com/user-attachments/assets/ee2ead62-6480-4312-af8b-762ec240cc10">

# How to use ?

## Clone
```bash
git clone https://github.com/SUPAIDEAS/passifypdf.git
```

## Install Dependencies
Uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
cd passifypdf
pip install poetry
poetry install
```

## Usage
Run the CLI tool using `poetry run`:

```bash
poetry run passifypdf --help
```

Or activate the shell:
```bash
poetry shell
passifypdf --help
```


Sample Run:
```bash
passifypdf -i input.pdf -o protected.pdf -p mySecretPassword

# -------------------------Sample output----------------------
# Congratulations!
# PDF file encrypted successfully and saved as 'protected.pdf'
```

## Known Issues
If you have any special chars (example: an emoji like Star 🌟) in the PDF file, it gives a minor complaint during execution.
But it still does the job, so you can ignore that "char or object error" which you see in the output.

## Web UI (Streamlit)

A local web interface is available for users who prefer a graphical workflow:

```bash
# Install web UI dependencies
pip install -r requirements-webui.txt

# Launch the app
streamlit run app/streamlit_app.py
```

Open the URL shown in your terminal (usually `http://localhost:8501`), upload a PDF, enter a password and download the protected file — no command line needed.

## Download Pre-built Binaries

Standalone executables for Linux, macOS, and Windows are built automatically on every tagged release via GitHub Actions. Visit the [Releases page](https://github.com/SUPAIDEAS/passifypdf/releases) to download the binary for your platform — no Python installation required.

## Note:
In general you can use passifypdf to protect your PDF files against chance attackers.
But you should not rely on this for mission-critical data or situations.
