# Run It Yourself

All commands below run from this package folder in a fresh POSIX shell.
The proof uses no rank or descent computation; it is the self-contained Lean file.

## 1. Full automated verification (ISO C99 + Python 3 stdlib + Core Lean 4 compiler)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output summary:
1. `C99_VERIFIER: unified_parametrizations=1 excluded_fibrations=2 lean_theorems=12 PASS`
2. `PROVED_SUMMARY` through `PYTHON_VERIFIER: PASS` (pure-stdlib Python 3 symbolic polynomial verification, certificate hashes, forbidden-token scan of the Lean file, and 500-fiber `math.isqrt` audit)
3. Twelve `#print axioms PerfectCuboidDGH...` blocks from the Core Lean 4 compiler, verified against the strict allowlist `{propext, Classical.choice, Quot.sound}`
4. Final line: `PASS` (exit status `0`); on any failure the final line is `FAIL` (non-zero exit status)

## 2. Standalone Core Lean 4 check

```sh
lean -j 2 object/dgh_internal_edge_cuboids_proof.lean
```

(If using `elan` without a configured default toolchain, run `lean +v4.35.0 -j 2 object/dgh_internal_edge_cuboids_proof.lean`.)

Expected output: twelve `#print axioms` blocks listing only `[propext, Classical.choice, Quot.sound]` (no imports, no unproved placeholders, no compiler-trusted reflection tactics, no axioms beyond the three standard ones).

## 3. Symbolic exploration and rebuilding `object/certificate.json` from scratch

Requires Python 3 with `sympy`.

To re-run the symbolic algebraic derivation:

```sh
python3 how-we-built-it/probe_dgh_families.py
```

To regenerate `object/certificate.json` byte-for-byte from the symbolic definitions and the hash of `object/dgh_internal_edge_cuboids_proof.lean`:

```sh
python3 how-we-built-it/build_certificate.py
```
