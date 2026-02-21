#!/bin/bash

echo "Creating Buf issues..."
# Bugs
gh issue create --repo SUPAIDEAS/passifypdf --title "Bug: Special characters and emojis in PDF file paths cause minor complaints" --body "As mentioned in the README, if the user has special characters like an emoji in the PDF file name, the shell gives a minor complain during execution. This should be gracefully handled by encoding the paths correctly or catching the exception and returning a friendly error." --label bug
gh issue create --repo SUPAIDEAS/passifypdf --title "Bug: Validate if the input file is actually a valid PDF format" --body "Currently, the script might attempt to encrypt non-PDF files if passed with a .pdf extension or no extension. We should use a magic byte checker or a try-catch block during the PdfReader initialization to provide a clear error message that the file is not a valid PDF." --label bug
gh issue create --repo SUPAIDEAS/passifypdf --title "Bug: High memory consumption on very large PDF files" --body "The current approach iterates through all pages and adds them to the writer using reader.pages, holding everything in memory. For a multi-gigabyte PDF, this might lead to Out Of Memory (OOM) errors. We should explore optimizing memory usage." --label bug
gh issue create --repo SUPAIDEAS/passifypdf --title "Bug: Output path collision should prompt before overwriting" --body "If the user specifies an output path that already exists, the script silently overwrites it. It should prompt the user (e.g., 'File exists, overwrite? [y/N]') unless a --force flag is provided." --label bug
gh issue create --repo SUPAIDEAS/passifypdf --title "Bug: Handle encrypted PDFs gracefully if passed as input" --body "If the input PDF is already encrypted, pypdf will throw an error when trying to read the pages. The script should catch this specific error and inform the user." --label bug

echo "Creating Enhancement issues..."
# Enhancements
gh issue create --repo SUPAIDEAS/passifypdf --title "Enhancement: Add an option to decrypt an already protected PDF" --body "It would be useful if passifypdf could also act as a decryption tool if the user provides the correct password and a --decrypt flag." --label enhancement
gh issue create --repo SUPAIDEAS/passifypdf --title "Enhancement: Support setting 256-bit AES encryption explicitly" --body "By default, pypdf might use 128-bit encryption based on the version. We should allow advanced users to specify the encryption algorithm explicitly, e.g., --encryption-level 256." --label enhancement
gh issue create --repo SUPAIDEAS/passifypdf --title "Enhancement: Add a --quiet or -q flag for silent execution" --body "For scripting and CI/CD pipelines, users might not want the 'Congratulations!' message printed to the console. A --quiet flag should suppress all non-error output." --label enhancement
gh issue create --repo SUPAIDEAS/passifypdf --title "Enhancement: Add batch processing support for directories" --body "Allow the input -i to be a directory instead of a file, parsing all .pdf files and creating protected versions in the output directory." --label enhancement
gh issue create --repo SUPAIDEAS/passifypdf --title "Enhancement: Display progress bar during encryption" --body "For PDFs with thousands of pages, the script might take a while. Adding a simple progress bar using tqdm or rich would improve the UX considerably." --label enhancement

echo "Creating Documentation issues..."
# Documentation
gh issue create --repo SUPAIDEAS/passifypdf --title "Docs: Add a comprehensive CONTRIBUTING.md guide" --body "We need a standard setup guide for contributors, detailing how to set up the local environment, run tests with pytest, and linting rules." --label documentation
gh issue create --repo SUPAIDEAS/passifypdf --title "Docs: Update README with GitHub Actions Status Badges" --body "Adding visually appealing badges for CI/CD status, PyPI version, and License will make the project look more professional." --label documentation
gh issue create --repo SUPAIDEAS/passifypdf --title "Docs: Write a SECURITY.md explaining PDF encryption limits" --body "As noted in the README, PDF encryption should not be relied upon for mission-critical data. A SECURITY.md file detailing the exact cryptographic standards used would help users." --label documentation
gh issue create --repo SUPAIDEAS/passifypdf --title "Docs: Provide examples of using passifypdf programmatically" --body "While the CLI is documented, other Python developers might want to import encrypt_pdf directly in their code. Add a small Python API section to the README." --label documentation
gh issue create --repo SUPAIDEAS/passifypdf --title "Docs: Document expected exit codes and error scenarios" --body "CLI tools should ideally document their exit codes (e.g., 0 for success, 1 for generic error, 2 for missing file). Please add a section in docs/CLI_OPTIONS.md for this." --label documentation

echo "Creating Good First issues..."
# Good First Issue
gh issue create --repo SUPAIDEAS/passifypdf --title "Refactoring: Migrate argparse to click or typer" --body "The current CLI uses standard library argparse. Migrating to typer or click would provide better automatic help generation, colors, and type enforcement." --label "good first issue"
gh issue create --repo SUPAIDEAS/passifypdf --title "Feature: Add --version / -v flag to CLI" --body "Currently, there is no quick way to check the installed tool version. A standard --version flag should be added reading the version from pyproject.toml or __init__.py." --label "good first issue"
gh issue create --repo SUPAIDEAS/passifypdf --title "Refactoring: Use standard logging module instead of print" --body "All console output is currently using print(). We should initialize a basic logging configuration and use logger.info(), logger.error() instead." --label "good first issue"
gh issue create --repo SUPAIDEAS/passifypdf --title "CI: Add pre-commit hooks for code formatting" --body "To maintain code quality, we should add a .pre-commit-config.yaml file configuring ruff, black, or flake8 and add instructions on how to set it up." --label "good first issue"
gh issue create --repo SUPAIDEAS/passifypdf --title "Tests: Add type hints to all test fixtures and functions" --body "The main codebase uses type hints nicely, but the test suite (tests/unittests/test_encryptpdf.py) lacks them. This is a great starting issue to get familiar with the codebase." --label "good first issue"

echo "Creating Help Wanted issues..."
# Help Wanted
gh issue create --repo SUPAIDEAS/passifypdf --title "Research: Implement hardware-accelerated AES encryption" --body "For large PDFs, standard pypdf encryption might be slow. We are looking for help to profile and possibly integrate hardware-accelerated AES via cryptography or natively." --label "help wanted"
gh issue create --repo SUPAIDEAS/passifypdf --title "Build: Implement cross-platform native binaries using PyInstaller" --body "Not all users have Python installed. Creating a GitHub Actions pipeline to publish standalone binaries for Windows, macOS, and Linux using PyInstaller would be a fantastic addition." --label "help wanted"
gh issue create --repo SUPAIDEAS/passifypdf --title "UX: Create a Streamlit or Gradio based web UI wrapper" --body "Some users prefer graphical interfaces. We need help building a simple, local Web UI wrapper around passifypdf using Streamlit or Gradio." --label "help wanted"
gh issue create --repo SUPAIDEAS/passifypdf --title "UX: Integrate into right-click OS context menus" --body "It would be amazing if users could right-click a PDF on Windows/macOS and select 'Protect with passifypdf'. We need contributors familiar with OS registries/automator to add this." --label "help wanted"
gh issue create --repo SUPAIDEAS/passifypdf --title "Benchmarking: Compare encryption speeds against other CLI tools" --body "We want to know how passifypdf performs against tools like qpdf or pdftk. We need help writing a benchmark suite and documenting the results." --label "help wanted"

