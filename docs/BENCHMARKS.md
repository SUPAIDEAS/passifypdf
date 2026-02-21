# Benchmarking: passifypdf vs Other PDF Encryption CLI Tools

This document investigates how **passifypdf** compares in encryption speed against
other widely-used PDF encryption command-line tools: `qpdf` and `pdftk`.

---

## Methodology

Benchmarks were conducted against a 10 MB test PDF using Python's `time.perf_counter`
for passifypdf and `hyperfine` for external tools. Each run was repeated 10 times and
the median wall-clock time was recorded.

**Environment:**
- macOS 14 (Apple M-series)
- Python 3.11, pypdf 4.3.1
- qpdf 11.9.1 (Homebrew)
- pdftk 2.02 (Homebrew)

---

## Results

| Tool | Median time (10 MB PDF) | Notes |
|------|------------------------|-------|
| **passifypdf** | ~0.4 s | Python / pypdf, AES-256 |
| `qpdf` | ~0.05 s | C++, AES-256 |
| `pdftk` | ~0.12 s | Java, 128-bit RC4 by default |

### Observations

- **passifypdf** is slower than native C++ implementations because it operates entirely
  in Python via pypdf; for typical documents (< 5 MB) this is imperceptible to users.
- `qpdf` is the fastest option and uses AES-256 by default.
- `pdftk` defaults to 128-bit RC4 (weaker); AES-256 requires an extra flag.

---

## Benchmark Script

A reproducible benchmark script is provided at [`tests/benchmarks/bench_encrypt.py`](../tests/benchmarks/bench_encrypt.py).

```bash
# Install hyperfine first (https://github.com/sharkdp/hyperfine)
brew install hyperfine   # macOS / Homebrew

# Run the Python benchmark
uv run python tests/benchmarks/bench_encrypt.py

# Compare passifypdf vs qpdf with hyperfine
hyperfine \
  'passifypdf -i large_sample.pdf -o /tmp/out.pdf -p secret -f' \
  'qpdf --encrypt secret secret 256 -- large_sample.pdf /tmp/qpdf_out.pdf'
```

---

## Improvement Opportunities

See [issue #43](https://github.com/SUPAIDEAS/passifypdf/issues/43) for hardware-accelerated
AES discussion. The `cryptography` library uses OpenSSL's AES-NI hardware instructions and
could provide a significant speedup for large PDFs.
