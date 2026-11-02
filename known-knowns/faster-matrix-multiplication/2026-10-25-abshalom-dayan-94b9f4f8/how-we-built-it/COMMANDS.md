# How the object was built (exact commands)

```sh
# Python 3.14 with numpy 2.5.4 and python-flint 0.9.0 (requirements.txt). From this folder (how-we-built-it/):
python3 -m venv .v && .v/bin/pip install -r requirements.txt
curl -sS -o lita_29.npz https://raw.githubusercontent.com/khoruzhii/lita/472a79fbc8248423a97bebb3aacbc89e769b9b3e/schemes/29x29x29_r11203.npz
shasum -a 256 lita_29.npz     # d54f4f3c63b67dacb3504821fc30d9b5a2b83f3cd45c707683c92b0b7525d1f7
.v/bin/python code/convert.py lita_29.npz lita_29.json
shasum -a 256 lita_29.json    # 77dfd55c26afbe8bbc64ffcba2c492c21b3ee0d6ec61916531629a84f580c734
.v/bin/python code/rebuild_lita_slices.py lita_29.json step1.json step2.json     # about 2727 s (nice, shared machine), peak RSS about 4.9 GB, footprint 8.0 GB
shasum -a 256 step1.json step2.json
#   step1.json f0b07bbbb14356d32532d60f35f0ea51e7cb46b0ff947a297edab88d6fd9f6da
#   step2.json 35714603ae5cc7c8abcacec99150caf5b1edc2a532394877e4f4efa7a8051710
.v/bin/python code/export_txt.py step1.json rebuilt/                                  # u.txt, v.txt, w.txt
for w in u v w; do if [ -f ../object/$w.txt ]; then cat ../object/$w.txt; else cat ../object/$w.part?.txt; fi | cmp - rebuilt/$w.txt || echo DIFFERENT $w; done; echo compared
.v/bin/python code/slice_accounting.py lita_29.json step1.json step2.json         # the kill counts below (seconds)
```

Input: the LITA scheme schemes/29x29x29_r11203.npz of Khoruzhii, Serafin, Gelss and Pokutta (https://github.com/khoruzhii/lita, commit 472a79fbc8248423a97bebb3aacbc89e769b9b3e, the repository head when fetched; fetched by the band run 2026-10-24T20:19:36Z, HTTP 200, sha256 d54f4f3c63b67dacb3504821fc30d9b5a2b83f3cd45c707683c92b0b7525d1f7, 587377 bytes). It is third-party data with no licence file in its repository, so it is not copied here; the command above fetches it.

Determinism: NOT confirmed. N = 29 was rebuilt once (one run took 2727 s and 4.93 GB RSS; no second rebuild was run); the step JSON hashes above come from that single run. The claim's checkers do not depend on determinism: the object in object/ is what is checked, whatever the rebuild does.

Real output of rebuild_lita_slices.py (band run, 2026-10-24T22:25:18Z to 2026-10-24T23:10:46Z UTC; 2727 s wall, peak RSS 4.93 GB, peak footprint 8.00 GB; nice, on a shared laptop):

```
input (29, 29, 29) rank 11203
step 1: slice axis 0 -> (28, 29, 29) rank 10740
step 1: absorbed 1 -> rank 10739 (1516s)
step 2: slice axis 1 -> (28, 28, 29) rank 10291
step 2: absorbed 1 -> rank 10290 (2723s)
wrote cells/N29/run1/step1.json cells/N29/run1/step2.json
```

The rebuild's intermediate step-1 scheme is the sibling cell <28,29,29> rank 10739 (this claim); the step-2 scheme is <28,28,29> rank 10290. The object of this claim is the step-1 scheme.

## The code

- code/convert.py: LITA's npz format (CSR rows with numerators and denominators) to JSON.
- code/engine.py: exact one-slice restriction (restrict) and exact 2-reductions (absorb_all). A 2-reduction finds a linear dependency sum_t c_t X_t (x) Y_t = 0 among the terms' paired factors (found modulo two 62-bit primes, lifted to Q by rational reconstruction, verified exactly), then shifts the third factors so one term disappears.
- code/rebuild_lita_slices.py: the two steps for any odd N (here N = 29). Slice direction e* = (1,...,1,-12 at index 14,1,...,1) on one side and e_0 on the other.
- code/export_txt.py: scheme JSON to the three plain text files; code/split_parts.py: how the files in object/ were cut into parts of under 1,000,000 bytes at line boundaries (the parts joined are byte-identical to the export).
- code/slice_accounting.py: counts which terms each slice kills and the plain coordinate projections (output below and in slice_accounting_output.txt).
- The pipeline files convert.py, engine.py, export_txt.py and rebuild_lita_slices.py are byte-identical to those of the 18x18x19 claim (PR #714), which ran them for N = 19 (cmp, checked when this folder was written). slice_accounting.py and split_parts.py are new in this batch.

## Where the removed terms go (code/slice_accounting.py, real output; the full output is slice_accounting_output.txt)

e* = (1,...,1,-12,1,...,1) with -12 at index 14; e_0 = the unit vector at index 0. A term vanishes in a slice when its factor on one side is an outer product with the slice direction on that side.

```
input <29,29,29> rank 11203

[coordinate projection, 29^3 -> 28x29x29] best row: delete index 14 -> 11145 terms (58 vanish); vanishing counts over all rows: [30, 42, 43, 58]
[coordinate projection, 29^3 -> 28x28x29] best pair: delete row 14 and column 14 -> 11087 terms (116 vanish)

star vector e*: entry -12 at index 14, 1 elsewhere; e_0 = unit vector at index 0

step 1, slice axis 0 (row index shared by A and C), e = e* on A, f = e_0 on C:
  terms with U = e* x^T (killed on the A side): 420; with W = e_0 y^T (killed on the C side): 43; both: 0; total 463
  after the slice: <28,29,29> rank 10740  (11203 - 463 = 10740)
  2-reduction(s) (saved step1.json): removed 1 -> rank 10739

[coordinate projection, 28x29x29:10739 -> 28x28x29] best column: delete index 14 -> 10695 terms (44 vanish); range of vanishing counts over all columns: (15, 44)

step 2, slice axis 1 (column index of A = row index of B), e = e_0 on A, f = e* on B:
  terms with U = x e_0^T (killed on the A side): 29; with V = e* y^T (killed on the B side): 419; both: 0; total 448
  after the slice: <28,28,29> rank 10291  (10739 - 448 = 10291)
  2-reduction(s) (saved step2.json): removed 1 -> rank 10290

summary: 11203 -[slice 1 kills 463]-> 10740 -[2-reduction]-> 10739 -[slice 2 kills 448]-> 10291 -[2-reduction]-> 10290; total removed 913
closed forms: step 1 removes (N^2+3N)/2 = 464 (measured 464); step 2 removes (N^2+2N-1)/2 = 449 (measured 449)
```

In words: 11203 (LITA <29,29,29>) - 463 (slice 1: 420 + 43) = 10740, - 1 (2-reduction) = 10739 (<28,29,29>). For comparison, plain coordinate projections (deleting one index, no reductions) give 11145 from LITA 29^3 (delete row 14: 58 terms vanish); all are above 11203 (the Lille value).

## Closed forms (observed, not proved here)

Slice 1 plus its 2-reduction removed (N^2+3N)/2 = 464 terms and slice 2 plus its 2-reduction removed (N^2+2N-1)/2 = 449 terms, as for N = 15, 17 and 19 in the earlier work; they are measured counts for this N, not a theorem.
