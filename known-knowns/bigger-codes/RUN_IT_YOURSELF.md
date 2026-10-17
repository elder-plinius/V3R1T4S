# Reproduce: constant-weight codes

All commands are relative to the `known-knowns/bigger-codes/` directory. Requirements: `python3` with `numpy` (any version; `numpy >= 2.0` is faster for the popcounts). No network access
is needed except for step 3.

## 1. Check every code (about 10 minutes single-threaded; the largest, A(29,6,12) with 1.9·10^9 pairs, takes a few minutes)

```sh
cd codes
for f in A*.txt; do
  set -- $(echo "$f" | sed 's/^A//; s/\.txt$//; s/_/ /g')     # n d w M
  python3 ../verify-it-yourself/cwcheck.py "$f" "$1" "$2" "$3" || echo "FAILED $f"
done
```
Each run prints the sha256, the format/weight/distinctness tests, the full pairwise-distance histogram, the t-subset
packing test and `VERDICT: VALID  A(n,d,w) >= M`. The expected sha256 of every file is in `INDEX.csv`;
`verify-it-yourself/RECEIPTS.md` has the complete output at release time.

Controls: duplicate a line, flip one bit, or change `M` in the file name; every such file is reported INVALID
(exit code 1).

## 2. Check the five Delsarte certificates (seconds, pure python)

```sh
python3 verify-it-yourself/delsarte_check.py certificates/cert_A*.json
```
Expected: five lines ending in `VALID` with the bounds 197, 380, 245, 2511, 2652 and the exact optima 8091/41,
145638/383, 26784/109, 1102464/439, 801009/302, then `ALL CERTIFICATES VALID`. Changing `U` or any `y_k` in a copy of
a certificate makes the checker report the violated constraint.

`sh verify-it-yourself/run_checks.sh` runs steps 1 and 2 and compares the sha256 values with `INDEX.csv`.

## 3. Compare with today's table

```sh
curl -sS -D headers.txt -o Andw.html https://aeb.win.tue.nl/codes/Andw.html     # one GET, default client
sha256sum Andw.html                                   # 0f1b51bf...1cee was the version recorded on 2026-10-10
python3 the-record-we-beat/parse_brouwer_table.py Andw.html the-record-we-beat/claims.csv
```
`the-record-we-beat/claims.csv` lists our 35 cells (`n,d,w,value,lb|ub`); the parser prints each cell's current text and a verdict
(STRICT_BEAT / TIE / BELOW for codes, STRICT_BELOW_UB for the Delsarte values). Any code whose cell now prints a lower
bound ≥ our size is no longer an improvement (see Corrections in `READ_BEFORE_CITING.md` at the repository root).

## 4. Regenerate

[`how-we-built-it/README.md`](how-we-built-it/README.md) lists, for every code and certificate, the archive seed file (with sha256), the script,
the random seeds and the number of rounds of each step (python3 with `numpy`, `numba`, `scipy`; versions in
`how-we-built-it/requirements.txt`). The searches are randomised but seeded, so 25 of the 30 codes and all 5
certificates are defined by deterministic command chains; we reran the short ones below and got the published files
byte for byte, but not the long chains (hours of CPU each). The five A(n,8,7) codes, n = 52..56, came from a driver
whose random stream depended on Python's per-process string hashing and cannot be replayed exactly. Smallest
example (about a minute on two cores), from this directory:

```sh
cd how-we-built-it
sh fetch_seeds.sh seeds                                     # 28 archive files, checked against SEEDS.sha256
python3 convert_seed.py seeds/d8/a34.8.7.601H 34 7 s0.npy
NUMBA_NUM_THREADS=2 python3 lb_lns_gen.py s0.npy 34 8 7 walk --seed 31 --rounds 2
python3 write_code.py A34_8_7_602.txt 34 walk_best.npy
shasum -a 256 A34_8_7_602.txt                               # 1a1d0958...1e = codes/A34_8_7_602.txt
cd delsarte && for c in "31 12 10" "31 12 11" "32 12 10" "32 12 15" "32 12 16"; do python3 make_certs.py $c out; done
# (in zsh write ${=c}); out/*.json are byte-identical to certificates/*.json
```
`how-we-built-it/SMOKE.md` has the output of this run. To see how far each code is from its seed, compare its word
set with the converted seed file; our own measurement is quoted in the README (1 %–17 % of the words changed).

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

The inventory preflight covers the original 30 codes in `codes/` and five
certificates in `certificates/`, with their root indexes. Sibling contributed
packages, including `2026-10-14-freelsgood-9e824e9f/`, are outside this
wrapper’s scope and must be checked with their own instructions.
