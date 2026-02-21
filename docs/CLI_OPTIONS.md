# CLI Options

The `passifypdf` tool accepts the following command-line arguments:

| Option | Long Option | Required | Description |
| :--- | :--- | :--- | :--- |
| `-i` | `--input` | Yes | Path to the input PDF file. |
| `-o` | `--output` | Yes | Path to the output (encrypted) PDF file. |
| `-p` | `--passwd` | Yes | Password to use for encryption. **Avoid passing sensitive passwords directly on the command line, as they may be exposed via process listings and shell history.** |
| `-f` | `--force` | No | Overwrite the output file without prompting if it already exists. |
| `-v` | `--version` | No | Show the program's version number and exit. |
| `-h` | `--help` | No | Show the help message and exit. |

## Example Usage

```bash
# Using the installed CLI command
passifypdf -i input.pdf -o protected.pdf -p mySecretPassword

# Or via uv run (useful during local development)
uv run passifypdf -i input.pdf -o protected.pdf -p mySecretPassword
```

## Exit Codes

| Code | Meaning |
| :--- | :--- |
| `0` | Success — the PDF was encrypted and saved successfully, or the user cancelled the operation. |
| `1` | Failure — an error occurred (e.g., input file not found, I/O error, encryption failure). |
