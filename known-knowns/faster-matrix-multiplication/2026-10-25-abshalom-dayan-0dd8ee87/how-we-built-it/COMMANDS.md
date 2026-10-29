# How the object was built (exact commands)

```sh
# Python 3.14 with numpy 2.5.4 and python-flint 0.9.0 (requirements.txt). From this folder (how-we-built-it/):
python3 -m venv .v && .v/bin/pip install -r requirements.txt
curl -sS -o lita_25.npz https://raw.githubusercontent.com/khoruzhii/lita/472a79fbc8248423a97bebb3aacbc89e769b9b3e/schemes/25x25x25_r7507.npz
shasum -a 256 lita_25.npz     # 32b251e6933c6652dbbd5ac3037d5afea859c879b2d71c0c1433cadd5e1d5613
.v/bin/python code/convert.py lita_25.npz lita_25.json
shasum -a 256 lita_25.json    # 2ad27a50123a394a3e64e4a506b03dbb0cf8076866cdedb5911d8551db92b460
.v/bin/python code/rebuild_lita_slices.py lita_25.json step1.json step2.json     # about 922 s (nice, shared machine), peak RSS about 2.2 GB, footprint 2.5 GB
shasum -a 256 step1.json step2.json
#   step1.json f4e9c4ed64b0b5b87a024b761395f647616f9917cd3d398094dc0216b2517d2d
#   step2.json 20d0bd84c4165c00b9d58c0cb6aec0d8bf512c9f6b864db363a0bbe88fe027ba
.v/bin/python code/export_txt.py step1.json rebuilt/                                  # u.txt, v.txt, w.txt
for w in u v w; do if [ -f ../object/$w.txt ]; then cat ../object/$w.txt; else cat ../object/$w.part?.txt; fi | cmp - rebuilt/$w.txt || echo DIFFERENT $w; done; echo compared
.v/bin/python code/slice_accounting.py lita_25.json step1.json step2.json         # the kill counts below (seconds)
```

Input: the LITA scheme schemes/25x25x25_r7507.npz of Khoruzhii, Serafin, Gelss and Pokutta (https://github.com/khoruzhii/lita, commit 472a79fbc8248423a97bebb3aacbc89e769b9b3e, the repository head when fetched; fetched by the band run 2026-10-24T20:19:36Z, HTTP 200, sha256 32b251e6933c6652dbbd5ac3037d5afea859c879b2d71c0c1433cadd5e1d5613, 394063 bytes). It is third-party data with no licence file in its repository, so it is not copied here; the command above fetches it.

Determinism: the band run rebuilt this cell twice (second run 2026-10-24T21:01:16Z to 2026-10-24T21:16:42Z); the step-1 and step-2 JSON files and the text exports of the two runs are byte-identical (cmp), so the rebuild is reproducible for N = 25 on that machine. Their sha256 values are the ones above.

Real output of rebuild_lita_slices.py (band run, 2026-10-24T20:45:53Z to 2026-10-24T21:01:16Z UTC; 922 s wall, peak RSS 2.17 GB, peak footprint 2.51 GB; nice, on a shared laptop):

```
input (25, 25, 25) rank 7507
step 1: slice axis 0 -> (24, 25, 25) rank 7158
step 1: absorbed 1 -> rank 7157 (523s)
step 2: slice axis 1 -> (24, 24, 25) rank 6821
step 2: absorbed 1 -> rank 6820 (920s)
wrote cells/N25/run1/step1.json cells/N25/run1/step2.json
```

The rebuild's intermediate step-1 scheme is the sibling cell <24,25,25> rank 7157 (this claim); the step-2 scheme is <24,24,25> rank 6820. The object of this claim is the step-1 scheme.

## The code

- code/convert.py: LITA's npz format (CSR rows with numerators and denominators) to JSON.
- code/engine.py: exact one-slice restriction (restrict) and exact 2-reductions (absorb_all). A 2-reduction finds a linear dependency sum_t c_t X_t (x) Y_t = 0 among the terms' paired factors (found modulo two 62-bit primes, lifted to Q by rational reconstruction, verified exactly), then shifts the third factors so one term disappears.
- code/rebuild_lita_slices.py: the two steps for any odd N (here N = 25). Slice direction e* = (1,...,1,-10 at index 12,1,...,1) on one side and e_0 on the other.
- code/export_txt.py: scheme JSON to the three plain text files; code/split_parts.py: how the files in object/ were cut into parts of under 1,000,000 bytes at line boundaries (the parts joined are byte-identical to the export).
- code/slice_accounting.py: counts which terms each slice kills and the plain coordinate projections (output below and in slice_accounting_output.txt).
- The pipeline files convert.py, engine.py, export_txt.py and rebuild_lita_slices.py are byte-identical to those of the 18x18x19 claim (PR #714), which ran them for N = 19 (cmp, checked when this folder was written). slice_accounting.py and split_parts.py are new in this batch.

## Where the removed terms go (code/slice_accounting.py, real output; the full output is slice_accounting_output.txt)

e* = (1,...,1,-10,1,...,1) with -10 at index 12; e_0 = the unit vector at index 0. A term vanishes in a slice when its factor on one side is an outer product with the slice direction on that side.

```
input <25,25,25> rank 7507

[coordinate projection, 25^3 -> 24x25x25] best row: delete index 12 -> 7457 terms (50 vanish); vanishing counts over all rows: [26, 36, 37, 50]
[coordinate projection, 25^3 -> 24x24x25] best pair: delete row 12 and column 12 -> 7407 terms (100 vanish)

star vector e*: entry -10 at index 12, 1 elsewhere; e_0 = unit vector at index 0

step 1, slice axis 0 (row index shared by A and C), e = e* on A, f = e_0 on C:
  terms with U = e* x^T (killed on the A side): 312; with W = e_0 y^T (killed on the C side): 37; both: 0; total 349
  after the slice: <24,25,25> rank 7158  (7507 - 349 = 7158)
  2-reduction(s) (saved step1.json): removed 1 -> rank 7157

[coordinate projection, 24x25x25:7157 -> 24x24x25] best column: delete index 12 -> 7119 terms (38 vanish); range of vanishing counts over all columns: (13, 38)

step 2, slice axis 1 (column index of A = row index of B), e = e_0 on A, f = e* on B:
  terms with U = x e_0^T (killed on the A side): 25; with V = e* y^T (killed on the B side): 311; both: 0; total 336
  after the slice: <24,24,25> rank 6821  (7157 - 336 = 6821)
  2-reduction(s) (saved step2.json): removed 1 -> rank 6820

summary: 7507 -[slice 1 kills 349]-> 7158 -[2-reduction]-> 7157 -[slice 2 kills 336]-> 6821 -[2-reduction]-> 6820; total removed 687
closed forms: step 1 removes (N^2+3N)/2 = 350 (measured 350); step 2 removes (N^2+2N-1)/2 = 337 (measured 337)
```

In words: 7507 (LITA <25,25,25>) - 349 (slice 1: 312 + 37) = 7158, - 1 (2-reduction) = 7157 (<24,25,25>). For comparison, plain coordinate projections (deleting one index, no reductions) give 7457 from LITA 25^3 (delete row 12: 50 terms vanish); all are above 7507 (the Lille value).

## Closed forms (observed, not proved here)

Slice 1 plus its 2-reduction removed (N^2+3N)/2 = 350 terms and slice 2 plus its 2-reduction removed (N^2+2N-1)/2 = 337 terms, as for N = 15, 17 and 19 in the earlier work; they are measured counts for this N, not a theorem.
