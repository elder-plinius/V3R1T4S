# Reproduce: fast matrix multiplication schemes

All commands are relative to the `known-knowns/faster-matrix-multiplication/` directory. Requirements: `python3` with `numpy`
(the absorption step in section 4 also needs `numba`).

## 1. Integrity

```sh
sha256sum schemes/*.json      # macOS: shasum -a 256; expected values in INDEX.csv
```

## 2. Brent equations and rank (the proof)

```sh
python3 verify-it-yourself/fmmcheck.py schemes/14x15x15_r1842_Q.json schemes/13x14x14_r1558_Q.json \
        schemes/15x16x16_r2180_Q.json schemes/14x14x15_r1716_Q.json schemes/13x14x15_r1677_Q.json
```
Expected, per scheme: `mod p: violated Brent equations = 0` for each prime, the line comparing log2 of the product of
the primes with log2(2·L·(S+1)), and a last line
`FMMCHECK PASS ... rank_nonzero_terms=<rank> sha256=<as in INDEX.csv>` with ranks 1842, 1558, 2180, 1716, 1677.
Runtime: seconds to a few minutes per scheme (the <15,16,16> scheme is the slowest). The superseded
`schemes/14x15x15_r1843_Q.json` and `schemes/15x16x16_r2196_Q.json` (parents of the 1842 and 2180) pass the same way
with ranks 1843 and 2196.

Negative controls:
```sh
mkdir -p mutants && python3 verify-it-yourself/mutate.py schemes/13x14x15_r1677_Q.json mutants
for m in drop_term bump_coeff swap_vw; do python3 verify-it-yourself/fmmcheck.py mutants/$m.json | tail -1; done   # each FMMCHECK FAIL
```
`sh verify-it-yourself/run_checks.sh` does all of the above for all seven files and compares sha256 and rank with
`INDEX.csv`.

## 3. Compare with today's catalogues

One GET per source, with a User-Agent that says who you are, and no retries:
```sh
mkdir -p today && cd today
UA="your-name-or-project (single GET)"
curl -sS -A "$UA" -o fmm_sota.json             https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json
curl -sS -A "$UA" -o perminov_README.md        https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md
curl -sS -A "$UA" -o merlijn_SHA256SUMS        https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS
curl -sS -A "$UA" -o matmulcatalog_COVERAGE.md https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md
cd ..
python3 the-record-we-beat/parse_sources.py today 14x15x15=1842 13x14x14=1558 15x16x16=2180 14x14x15=1716 13x14x15=1677
```
Each format prints the value listed by each source, the minimum (`bar_min_of_four_sources`) and
`strictly_below_bar`. If a source has since listed a rank ≤ ours, that format is no longer an improvement (see the
Corrections in `READ_BEFORE_CITING.md` at the repository root). The values recorded for this release are in
`the-record-we-beat/sources_2026-10-10T19-25-52Z.json`; the 2026-10-12 re-check for the two new records is in
`the-record-we-beat/live_recheck_2026-10-12.json`.

## 4. Regenerating the schemes

The schemes are restrictions of LITA's public square schemes (github.com/khoruzhii/lita, `schemes/15x15x15_r1977.npz`
sha256 94515288…2a33, `14x14x14_r1593.npz` e8039025…1110, `16x16x16_r2236.npz` af5fd100…67da as fetched by our agents)
along the direction pairs listed in `README.md`. LITA's files are not redistributed here; the code downloads them at a
pinned commit and checks their sha256, then rebuilds the five schemes:
```sh
cd how-we-built-it
sh fetch_lita.sh lita                 # one GET per file, sha256 checked
sh regenerate_all.sh lita regen       # prints IDENTICAL for each scheme whose sha256 matches INDEX.csv
python3 ../verify-it-yourself/fmmcheck.py regen/*.json
```
Expected: `IDENTICAL` five times. Runtime: a few minutes. Then the two absorptions (needs `numba`), from the shipped
parents or from `regen/`:
```sh
python3 absorb_exact.py ../schemes/14x15x15_r1843_Q.json regen/14x15x15_r1842.json
python3 maxkill.py ../schemes/15x16x16_r2196_Q.json uv regen/15x16x16_r2180.json regen/15x16x16_r2180_cert.json
python3 ../verify-it-yourself/fmmcheck.py regen/14x15x15_r1842.json regen/15x16x16_r2180.json
```
Expected: `r_new 1842` and `final_r 1842`; `"n_killed": 16`, `"r_new": 2180`; `FMMCHECK PASS` with ranks 1842 and 2180.
The outputs equal `schemes/14x15x15_r1842_Q.json` and `schemes/15x16x16_r2180_Q.json` term for term (the JSON header
fields differ, so the sha256 does not). Details, the sweep that chose the direction pairs, and
the single commands per scheme: `how-we-built-it/README.md`; a recorded run: `how-we-built-it/SMOKE.md`.

## Wrapper contract dependency

`verify-it-yourself/run_checks.sh` requires the standard-library helper
`../check_harness_contract.py`, relative to this family directory. Keep the normal
repository layout, or copy `known-knowns/check_harness_contract.py` beside any
standalone family copy. A missing helper fails explicitly with exit 2. The helper
validates completed negative-control evidence and/or indexed inventory; it does
not replace the scientific checker or independently prove its result.

For lightweight orchestration regressions from the repository root (Python 3.9+,
no scientific dependencies, downloads, or compiler):

```sh
python3 known-knowns/tests/harness_contracts/run_regressions.py --output /tmp/veritas-harness-results
```

These tests mock scientific commands and execute only the standard-library
contract helper. Root `SHA256SUMS` edits remain a maintainer-only step. Before merging, maintainers
must refresh entries for the changed wrappers/documents and add the helper and
regression files. The pinned 91419e28 manifest already has stale kit entries;
regenerate and verify the manifest against the final complete tree, rather than
assuming unchanged entries are current.
