# Contributing to passifypdf

First off, thank you for considering contributing to passifypdf! It's people like you that make open source such a great community.

## Development Environment Setup

This project uses `uv` for dependency management and running tools.

### 1. Install `uv`
If you haven't already, install [uv](https://github.com/astral-sh/uv).
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Fork and Clone
Fork the repository and clone it to your local machine:
```bash
git clone https://github.com/YOUR_USERNAME/passifypdf.git
cd passifypdf
```

### 3. Install Dependencies
You can install the dependencies using `uv`.
```bash
uv sync
```
This will set up the virtual environment with all required run and development dependencies.

## Testing

We use `pytest` for running our test suite.

To run tests:
```bash
uv run pytest
```

To run tests with coverage reporting:
```bash
uv run pytest --cov=passifypdf
```
Please make sure all existing tests pass and write new tests for your newly added code before submitting a Pull Request.

## Code Quality

### Pre-commit Hooks

This project uses [`pre-commit`](https://pre-commit.com/) to enforce code quality automatically before each commit. The configuration lives in [`.pre-commit-config.yaml`](.pre-commit-config.yaml) and runs `ruff` (linter + formatter) plus standard file hygiene checks.

To set it up locally:

```bash
# Install pre-commit (using uv)
uv run pre-commit install

# Or using pip
pip install pre-commit
pre-commit install
```

Once installed, hooks run automatically on `git commit`. To run them manually across all files:

```bash
uv run pre-commit run --all-files
```

## Code Constraints and Formatting

Currently, the project strives for PEP 8 compliance. While we may add automated pre-commit formatting hooks in the future, please try to:
- Follow standard Python styling conventions (use `flake8` or `ruff` to identify issues).
- Include standard docstrings for all new functions/classes.
- Ensure your typed logic has appropriate type-hints.

## Submitting a Pull Request

1. Create a feature branch from your fork: `git checkout -b feature/your-feature-name`.
2. Commit your changes: `git commit -m "feat: Add your feature text"`.
3. Push to your branch: `git push origin feature/your-feature-name`.
4. Submit a Pull Request on the main repository via GitHub.

Please link any relevant open issues to your Pull Request explicitly (e.g. "Closes #123"). 
CodeRabbit / Copilot AI might review your PR; please address any review feedback they provide.

Thank you!
