# How the object was built (exact commands)

```sh
# Python 3.14 with numpy 2.5.4 and python-flint 0.9.0 (requirements.txt). From this folder (how-we-built-it/):
python3 -m venv .v && .v/bin/pip install -r requirements.txt
curl -sS -o lita_31.npz https://raw.githubusercontent.com/khoruzhii/lita/472a79fbc8248423a97bebb3aacbc89e769b9b3e/schemes/31x31x31_r13433.npz
shasum -a 256 lita_31.npz     # 9effecdc238c8425993e7d73e3cefd45a40e67cd3cc08caf2825493f884e7955
.v/bin/python code/convert.py lita_31.npz lita_31.json
shasum -a 256 lita_31.json    # b676bf3811c53bcd87f136719e22e93fdaaf9d9b47319b5dbb2da6f151f207ec
.v/bin/python code/rebuild_lita_slices.py lita_31.json step1.json step2.json     # about 5165 s (nice, shared machine), peak RSS about 5.5 GB, footprint 9.0 GB
shasum -a 256 step1.json step2.json
#   step1.json f834d45f072c8760e1377cb031a115b7856331a0524d817dbb738449602e726e
#   step2.json 72742f7b595a5d9edaa7d76688504b5c24739f47a75d5b297dc73681af2fbf6b
.v/bin/python code/export_txt.py step1.json rebuilt/                                  # u.txt, v.txt, w.txt
for w in u v w; do if [ -f ../object/$w.txt ]; then cat ../object/$w.txt; else cat ../object/$w.part?.txt; fi | cmp - rebuilt/$w.txt || echo DIFFERENT $w; done; echo compared
.v/bin/python code/slice_accounting.py lita_31.json step1.json step2.json         # the kill counts below (seconds)
```

Input: the LITA scheme schemes/31x31x31_r13433.npz of Khoruzhii, Serafin, Gelss and Pokutta (https://github.com/khoruzhii/lita, commit 472a79fbc8248423a97bebb3aacbc89e769b9b3e, the repository head when fetched; fetched by the band run 2026-10-24T20:19:37Z, HTTP 200, sha256 9effecdc238c8425993e7d73e3cefd45a40e67cd3cc08caf2825493f884e7955, 711170 bytes). It is third-party data with no licence file in its repository, so it is not copied here; the command above fetches it.

Determinism: NOT confirmed. N = 31 was rebuilt once (one run took 5165 s and 5.55 GB RSS; no second rebuild was run); the step JSON hashes above come from that single run. The claim's checkers do not depend on determinism: the object in object/ is what is checked, whatever the rebuild does.

Real output of rebuild_lita_slices.py (band run, 2026-10-24T23:11:08Z to 2026-10-25T00:37:15Z UTC; 5165 s wall, peak RSS 5.55 GB, peak footprint 8.97 GB; nice, on a shared laptop):

```
input (31, 31, 31) rank 13433
step 1: slice axis 0 -> (30, 31, 31) rank 12907
step 1: absorbed 1 -> rank 12906 (3143s)
step 2: slice axis 1 -> (30, 30, 31) rank 12396
step 2: absorbed 1 -> rank 12395 (5160s)
wrote cells/N31/run1/step1.json cells/N31/run1/step2.json
```

The rebuild's intermediate step-1 scheme is the sibling cell <30,31,31> rank 12906 (this claim); the step-2 scheme is <30,30,31> rank 12395. The object of this claim is the step-1 scheme.

## The code

- code/convert.py: LITA's npz format (CSR rows with numerators and denominators) to JSON.
- code/engine.py: exact one-slice restriction (restrict) and exact 2-reductions (absorb_all). A 2-reduction finds a linear dependency sum_t c_t X_t (x) Y_t = 0 among the terms' paired factors (found modulo two 62-bit primes, lifted to Q by rational reconstruction, verified exactly), then shifts the third factors so one term disappears.
- code/rebuild_lita_slices.py: the two steps for any odd N (here N = 31). Slice direction e* = (1,...,1,-13 at index 15,1,...,1) on one side and e_0 on the other.
- code/export_txt.py: scheme JSON to the three plain text files; code/split_parts.py: how the files in object/ were cut into parts of under 1,000,000 bytes at line boundaries (the parts joined are byte-identical to the export).
- code/slice_accounting.py: counts which terms each slice kills and the plain coordinate projections (output below and in slice_accounting_output.txt).
- The pipeline files convert.py, engine.py, export_txt.py and rebuild_lita_slices.py are byte-identical to those of the 18x18x19 claim (PR #714), which ran them for N = 19 (cmp, checked when this folder was written). slice_accounting.py and split_parts.py are new in this batch.

## Where the removed terms go (code/slice_accounting.py, real output; the full output is slice_accounting_output.txt)

e* = (1,...,1,-13,1,...,1) with -13 at index 15; e_0 = the unit vector at index 0. A term vanishes in a slice when its factor on one side is an outer product with the slice direction on that side.

```
input <31,31,31> rank 13433

[coordinate projection, 31^3 -> 30x31x31] best row: delete index 15 -> 13371 terms (62 vanish); vanishing counts over all rows: [32, 45, 46, 62]
[coordinate projection, 31^3 -> 30x30x31] best pair: delete row 15 and column 15 -> 13309 terms (124 vanish)

star vector e*: entry -13 at index 15, 1 elsewhere; e_0 = unit vector at index 0

step 1, slice axis 0 (row index shared by A and C), e = e* on A, f = e_0 on C:
  terms with U = e* x^T (killed on the A side): 480; with W = e_0 y^T (killed on the C side): 46; both: 0; total 526
  after the slice: <30,31,31> rank 12907  (13433 - 526 = 12907)
  2-reduction(s) (saved step1.json): removed 1 -> rank 12906

[coordinate projection, 30x31x31:12906 -> 30x30x31] best column: delete index 15 -> 12859 terms (47 vanish); range of vanishing counts over all columns: (16, 47)

step 2, slice axis 1 (column index of A = row index of B), e = e_0 on A, f = e* on B:
  terms with U = x e_0^T (killed on the A side): 31; with V = e* y^T (killed on the B side): 479; both: 0; total 510
  after the slice: <30,30,31> rank 12396  (12906 - 510 = 12396)
  2-reduction(s) (saved step2.json): removed 1 -> rank 12395

summary: 13433 -[slice 1 kills 526]-> 12907 -[2-reduction]-> 12906 -[slice 2 kills 510]-> 12396 -[2-reduction]-> 12395; total removed 1038
closed forms: step 1 removes (N^2+3N)/2 = 527 (measured 527); step 2 removes (N^2+2N-1)/2 = 511 (measured 511)
```

In words: 13433 (LITA <31,31,31>) - 526 (slice 1: 480 + 46) = 12907, - 1 (2-reduction) = 12906 (<30,31,31>). For comparison, plain coordinate projections (deleting one index, no reductions) give 13371 from LITA 31^3 (delete row 15: 62 terms vanish); all are above 13433 (the Lille value).

## Closed forms (observed, not proved here)

Slice 1 plus its 2-reduction removed (N^2+3N)/2 = 527 terms and slice 2 plus its 2-reduction removed (N^2+2N-1)/2 = 511 terms, as for N = 15, 17 and 19 in the earlier work; they are measured counts for this N, not a theorem.
