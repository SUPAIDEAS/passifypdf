# CLI Options

The `passifypdf` tool accepts the following command-line arguments:

| Option | Long Option | Required | Description |
| :--- | :--- | :--- | :--- |
| `-i` | `--input` | Yes | Path to the input PDF file. |
| `-o` | `--output` | Yes | Path to the output (encrypted) PDF file. |
| `-p` | `--passwd` | Yes | Password to use for encryption. |
| `-v` | `--version` | No | Show the program's version number and exit. |
| `-h` | `--help` | No | Show the help message and exit. |

## Example Usage

```bash
# Using the installed CLI command
passifypdf -i input.pdf -o protected.pdf -p mySecretPassword
```

**Security Note:** Avoid passing sensitive passwords directly on the command line if possible, as they may be exposed in process listings.
```
