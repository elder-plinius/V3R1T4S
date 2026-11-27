# How the certificate files were built

This folder holds the code that produced the nine files in `object/certs/` and `object/MANIFEST.json`, with the exact commands to run it again. It is the code that was run, with three kinds of edits made when this package was assembled, none of which changes a computed number: comments that named the workspace were reworded to say what the code does; two exported function names of `nine-prime-engine/r12/geometry.cpp` were renamed (`geom_register`, `geom_batch`) together with their two call sites in `r12/ladder.py`; and `main-engine/neon_r13_build_package.py`, which read `nine-finite.json` from a fixed absolute path, now takes that location as an option (`--nine PATH`, default `../nine-prime-engine/package/nine-finite.json` relative to the script). The rerun below, made after these edits, reproduces every file byte for byte. It is not needed to check the claim: the checkers in `verify-it-yourself/` read only `object/`.

Requirements: Python 3.9 or later (standard library only), a C compiler `cc` and a C++17 compiler `c++` that can build shared libraries. Tested on macOS; the libraries are loaded by path, so the `.dylib` names also work on Linux.

## What is here

- `nine-prime-engine/`: builds the nine-prime table (23 cap vectors, 736 rows, `nine-finite.json`), written by a second model.
  - `r12/ladder.py`, `r12/harvest.py`, `r12/pinned.py`, `r12/geometry.cpp`: an anchored-inequality engine and its integer geometric kernel.
  - `r13/eight.py`: the evaluator used for the nine-prime rows.
  - `r13/nine_boxes.py`: splits the 5,028 nine-prime exponent vectors into boxes until each box's cap vector passes with basic rows only (writes `r13/nine-boxes.json`).
  - `r13/merge_nine.py`: merges boxes while their union still passes (writes `r13/nine-compact.json`).
  - `r13/publish_nine.py`: checks the result and writes `package/nine-finite.json`.
  - `package/verify_scalar.py`: the census of exponent vectors (the same file as `verify-it-yourself/alternate/verify_scalar.py`).
  The folder names `r12/`, `r13/` and `package/` are kept because the scripts find each other through them.
- `main-engine/`: builds all nine certificate files and the manifest, written by the model that built the certificates.
  - `geom135_r11.c`: exact 64-bit integer kernel for the geometric maximum, loaded through `ctypes` as `libgeom135_r11.dylib`.
  - `neon_global_anchored_probe_r12.py`, `neon_exp_ladder_probe_r11.py`, `neon_fast_ladder_scan_r11.py`: the anchored engine with exponent caps.
  - `neon_global_bound_probe_r12.py`, `neon_global_L_exact_map_r12.py`: the scalar bound (PROOF.md Proposition 4.1) and the enumeration of exponent vectors.
  - `neon_certify_global_L_r12.py`: finds the 738 scalar certificates for ten to thirteen primes and the 13 anchored certificates for the 18 remaining vectors (writes `r12_global_L_scalar_cert.json` and `r12_global_L_anchored_cert.json`).
  - `neon_r13_gen_thmA.py` with `neon_r13_gen_candidates.py`: generates the eight-prime certificate for Theorem A (28,057 rows; writes `r13_cand/A8_t8_U10_V7.json`).
  - `neon_r13_build_package.py`: writes the nine TSV files and `MANIFEST.json` from those inputs. It recomputes the 736 nine-prime rows itself from the cap vectors in `nine-finite.json`, using the cutoff Ucut = 10 on F9_15, as PROOF.md Section 9.2 states, where `nine-finite.json` uses 9 (see `verify-it-yourself/alternate/BASIC-CHECK.md`; both choices give valid bounds).

The generators use floating-point search only to choose parameters (thresholds and caps); every number written to a certificate is an exact reduced fraction, and the checkers recompute every one of them in exact arithmetic.

## Commands

From the package folder, in a fresh shell. The build writes only inside a temporary copy.

```sh
PKG=$(pwd)
WORK=$(mktemp -d)
cp -R how-we-built-it/. "$WORK/"
export PYTHONDONTWRITEBYTECODE=1

# 1. The nine-prime table
cd "$WORK/nine-prime-engine"
c++ -O3 -std=c++17 -fPIC -shared r12/geometry.cpp -o r12/geometry.dylib
python3 -B r13/nine_boxes.py
python3 -B r13/merge_nine.py
python3 -B r13/publish_nine.py
cmp package/nine-finite.json "$PKG/verify-it-yourself/alternate/nine-finite.json" && echo "nine-finite.json IDENTICAL"

# 2. Scalar certificates and the ten- and eleven-prime anchored certificates
cd "$WORK/main-engine"
cc -O3 -fPIC -shared geom135_r11.c -o libgeom135_r11.dylib
python3 -B neon_certify_global_L_r12.py

# 3. The eight-prime certificate for Theorem A (4 processes)
mkdir -p r13_cand
python3 -B -c "from fractions import Fraction; import neon_r13_gen_thmA as g; g.gen_thmA('A8_t8_U10_V7', (4, 4, 8, 8, 12), 10, 7, thresh=Fraction(0), procs=4, save_path='r13_cand/A8_t8_U10_V7.json')"

# 4. The nine TSV files and the manifest
python3 -B neon_r13_build_package.py --nine "$WORK/nine-prime-engine/package/nine-finite.json"
cd "$WORK"
for f in MANIFEST.json certs/global_anchored.tsv certs/nine_finite.tsv certs/scalar_lemma_u.tsv certs/thmA_8p.part01.tsv certs/thmA_8p.part02.tsv certs/thmA_8p.part03.tsv certs/thmA_8p.part04.tsv certs/thmA_8p.part05.tsv certs/thmA_8p.part06.tsv; do
    cmp -s "main-engine/package/$f" "$PKG/object/$f" && echo "IDENTICAL $f" || echo "DIFFERENT $f"
done
cd "$PKG"
```

The script `neon_r13_gen_thmA.py`, run as a program, tries three parameter choices with 6 processes; step 3 runs only the choice that was issued (thresholds (4, 4, 8, 8, 12) for the primes 11 to 23, cutoffs 10 and 7), with 4 processes.

## Result of a real run of these commands (2026-11-27 UTC, after the edits described at the top)

NUMERICAL, measured on a 28-core desktop (Apple M3 Ultra) that was heavily loaded by other jobs at the time (load average about 30); the whole sequence ran under `nice -n 10` with a time limit. Times are from `date +%s` between the steps.

| step | time | result |
|---|---:|---|
| 1. nine-prime table | 14 s | 23 models, 736 rows, 5,028 vectors; `nine-finite.json IDENTICAL` |
| 2. scalar and ten/eleven-prime certificates | 37 s | 738 scalar certificates (603, 120, 14, 1 at 10, 11, 12, 13 primes); 13 anchored certificates, 692 rows |
| 3. eight-prime certificate | 67 s | 28,057 rows (basic 16, basic75 4, mixed 604, coarse 25,840, spatial 1,003, pure3 506, fixed165 84), least surplus 0.002004 |
| 4. TSV files and manifest | 27 s | all 10 files byte-identical to `object/` |

Total 145 s (finished 2026-11-27T01:53:31Z). A first run before the edits (with an unchanged copy of the scripts) gave the same ten identical files in 148 s. The last lines printed by step 4 were:

```text
Total: 9 files, 5,604,948 bytes.
IDENTICAL MANIFEST.json
IDENTICAL certs/global_anchored.tsv
IDENTICAL certs/nine_finite.tsv
IDENTICAL certs/scalar_lemma_u.tsv
IDENTICAL certs/thmA_8p.part01.tsv
IDENTICAL certs/thmA_8p.part02.tsv
IDENTICAL certs/thmA_8p.part03.tsv
IDENTICAL certs/thmA_8p.part04.tsv
IDENTICAL certs/thmA_8p.part05.tsv
IDENTICAL certs/thmA_8p.part06.tsv
```

`object/PROOF.md` and `verify-it-yourself/FORMAT.md` were written by hand, not generated.
