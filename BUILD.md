## Install Dependencies
Uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
cd passifypdf
pip install uv <--- Not required if you have already installed.
uv sync

Next >>>
>>> switch to virtual env <<< 
source .venv/bin/activate
```

## Usage
Run the CLI tool using `uv run`:

```bash
source .venv/bin/activate
uv run passifypdf --help
```

Sample Run:
```bash
 uv run passifypdf -i ./passifypdf/Sample_PDF.pdf -o temp_protected.pdf -p qwe123

# -------------------------Sample output----------------------
Congratulations!
PDF file encrypted successfully and saved as 'temp_protected.pdf'

Now "temp_protected.pdf" should be under the pwd folder.

```

# Run Tests:
- Run unit tests
```shell
uv sync --all-extras
uv run pytest tests/unittests/ -v --cov=passifypdf --cov-report=xml --cov-report=term
```
- Run integration tests
```shell
uv run pytest tests/integrationtests/ -v
```
