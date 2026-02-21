"""Benchmark script comparing passifypdf encryption speed.

Run with:
    uv run python tests/benchmarks/bench_encrypt.py

Requires the tests/resources/Sample_PDF.pdf file to exist.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SAMPLE_PDF = Path(__file__).parent.parent / "resources" / "Sample_PDF.pdf"
PASSWORD = "benchmark_password_123"
ITERATIONS = 10


def benchmark_passifypdf(input_path: Path, output_dir: Path) -> float:
    """Benchmark passifypdf encrypt_pdf() directly."""
    from passifypdf.encryptpdf import encrypt_pdf

    times = []
    for i in range(ITERATIONS):
        output = output_dir / f"out_passifypdf_{i}.pdf"
        start = time.perf_counter()
        encrypt_pdf(input_path, output, PASSWORD)
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return _median(times)


def benchmark_qpdf(input_path: Path, output_dir: Path) -> float | None:
    """Benchmark qpdf if available on PATH."""
    if not shutil.which("qpdf"):
        return None

    times = []
    for i in range(ITERATIONS):
        output = output_dir / f"out_qpdf_{i}.pdf"
        start = time.perf_counter()
        subprocess.run(
            [
                "qpdf",
                f"--encrypt={PASSWORD}",
                PASSWORD,
                "256",
                "--",
                str(input_path),
                str(output),
            ],
            check=True,
            capture_output=True,
        )
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return _median(times)


def benchmark_pdftk(input_path: Path, output_dir: Path) -> float | None:
    """Benchmark pdftk if available on PATH."""
    if not shutil.which("pdftk"):
        return None

    times = []
    for i in range(ITERATIONS):
        output = output_dir / f"out_pdftk_{i}.pdf"
        start = time.perf_counter()
        subprocess.run(
            [
                "pdftk",
                str(input_path),
                "output",
                str(output),
                "user_pw",
                PASSWORD,
            ],
            check=True,
            capture_output=True,
        )
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return _median(times)


def _median(data: list[float]) -> float:
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    return (sorted_data[mid] if n % 2 else (sorted_data[mid - 1] + sorted_data[mid]) / 2)


def main() -> None:
    if not SAMPLE_PDF.exists():
        print(f"ERROR: Sample PDF not found at {SAMPLE_PDF}", file=sys.stderr)
        sys.exit(1)

    print(f"Benchmarking with {SAMPLE_PDF} ({SAMPLE_PDF.stat().st_size / 1024:.1f} KB), {ITERATIONS} iterations each\n")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        pp_time = benchmark_passifypdf(SAMPLE_PDF, tmp_path)
        qpdf_time = benchmark_qpdf(SAMPLE_PDF, tmp_path)
        pdftk_time = benchmark_pdftk(SAMPLE_PDF, tmp_path)

    print(f"{'Tool':<20} {'Median time':>15}")
    print("-" * 38)
    print(f"{'passifypdf':<20} {pp_time * 1000:>12.1f} ms")
    if qpdf_time is not None:
        print(f"{'qpdf':<20} {qpdf_time * 1000:>12.1f} ms")
    else:
        print(f"{'qpdf':<20} {'(not installed)':>15}")
    if pdftk_time is not None:
        print(f"{'pdftk':<20} {pdftk_time * 1000:>12.1f} ms")
    else:
        print(f"{'pdftk':<20} {'(not installed)':>15}")


if __name__ == "__main__":
    main()
