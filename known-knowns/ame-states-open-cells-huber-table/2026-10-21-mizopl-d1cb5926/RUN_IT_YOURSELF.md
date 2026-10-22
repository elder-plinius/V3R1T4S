# Run It Yourself (`2026-10-21-mizopl-d1cb5926`, Part II)

1. Ensure `python3` (`>= 3.9`) and a C compiler (`clang` or `gcc`) are available in `PATH`.
2. From the root of this package directory, execute:
   ```sh
   sh verify-it-yourself/run_checks.sh
   ```
3. The script executes `verify-it-yourself/verify.py`, which verifies in exact finite-field ($\mathbb{F}_p$, $\mathbb{F}_{p^2}$, $\mathbb{F}_{2^r}$) and modular integer ($\mathbb{Z}_9$) arithmetic all **28 Part II JSON certificates** in `object/` (compiling a tiny on-the-fly C helper for the $184,756$-cut rank sweeps of `AME(20, 13)`, `AME(20, 16)`, and `AME(20, 17)` in `~0.1s`), and prints:
   ```
   VERIFIED: All 28 Part II AME & Quantum MDS Certificates PASS in 0.28s
   PASS
   ```
   in under `0.5` seconds on a standard laptop CPU.
