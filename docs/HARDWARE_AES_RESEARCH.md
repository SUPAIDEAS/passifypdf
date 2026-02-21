# Hardware-Accelerated AES Encryption — Research Notes

This document summarises the research into hardware-accelerated AES encryption
for passifypdf, as requested in [issue #43](https://github.com/SUPAIDEAS/passifypdf/issues/43).

---

## Current Implementation

passifypdf uses [pypdf](https://github.com/py-pdf/pypdf) for all PDF operations.
pypdf's `PdfWriter.encrypt()` implements AES-256 in pure Python (via the `cryptography`
package on newer versions, or a built-in implementation on older ones).

---

## Hardware AES-NI

Modern x86-64 and ARM CPUs include dedicated AES hardware instructions (AES-NI / ARMv8
Crypto Extensions). The Python [`cryptography`](https://cryptography.io) library (backed
by OpenSSL) automatically uses these instructions when available.

### Does pypdf already benefit?

- **pypdf >= 4.x** delegates its AES implementation to the `cryptography` library when
  it is installed (`pip install cryptography`).
- `cryptography` uses OpenSSL, which auto-selects AES-NI at runtime.
- Therefore, **no code change is required** — just ensuring `cryptography` is installed
  gives passifypdf hardware acceleration.

### Verification

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# If this returns without error, AES-NI is in use via OpenSSL
cipher = Cipher(algorithms.AES(b"0" * 32), modes.CBC(b"0" * 16), backend=default_backend())
```

---

## Recommendation

1. **Add `cryptography` as an explicit optional dependency** so that users who install
   `passifypdf[fast]` automatically get hardware-accelerated encryption.
2. **Detect and warn** at startup if `cryptography` is not present (pure-Python fallback
   is significantly slower for large files).

### Proposed `pyproject.toml` change

```toml
[project.optional-dependencies]
fast = ["cryptography>=41.0"]
```

Install with:
```bash
pip install "passifypdf[fast]"
```

---

## Profiling Large PDFs

For files > 50 MB, the encryption step is the bottleneck. To profile:

```bash
uv run python -m cProfile -o profile.out -s cumulative \
  -c "from passifypdf.encryptpdf import encrypt_pdf; encrypt_pdf('large.pdf', 'out.pdf', 'pw')"
pstats profile.out
```

---

## Conclusion

Hardware acceleration is already available via the `cryptography` package; the main
actionable item is making it a well-documented optional dependency to ensure all users
benefit automatically.
