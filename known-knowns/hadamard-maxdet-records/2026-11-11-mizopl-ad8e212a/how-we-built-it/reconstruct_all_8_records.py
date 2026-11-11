#!/usr/bin/env python3
"""
Compact Algebraic Reconstruction Script for the 8 Record Matrices
(n = 81, 89, 93, 97, 101, 105, 109, 117).

Rebuilds every n x n {+1, -1} matrix in `object/M081.txt` .. `object/M117.txt`
directly from the compact generator parameters (`vA, vB, vC, vD` for Goethals-Seidel
cores on n = 93, 97, 105, 109, 117; `core_hex` for switched Hadamard cores on n = 81, 89, 101)
stored in `object/hadamard_maxdet_8_records.json`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
sys.path.insert(0, str(PKG_ROOT / "verify-it-yourself"))

from verify import reconstruct_and_check_params  # noqa: E402


def main() -> None:
    cert = json.loads((PKG_ROOT / "object" / "hadamard_maxdet_8_records.json").read_text(encoding="utf-8"))
    for rec in cert["records"]:
        n = rec["n"]
        rows = reconstruct_and_check_params(n, rec["generator_params"])
        assert rows == rec["matrix_rows"], f"Reconstruction mismatch at n={n}"
        print(f"Reconstructed n={n:>3d} ({rec['generator_params']['kind']}) -> {rec['factored_D_norm']}")
    print("Reconstructed 8/8 matrices bit-for-bit.")


if __name__ == "__main__":
    main()
