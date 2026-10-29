# How the object was built (exact commands)

```sh
# Python 3.14 with numpy 2.5.4 and python-flint 0.9.0 (requirements.txt). From this folder (how-we-built-it/):
python3 -m venv .v && .v/bin/pip install -r requirements.txt
curl -sS -o lita_23.npz https://raw.githubusercontent.com/khoruzhii/lita/472a79fbc8248423a97bebb3aacbc89e769b9b3e/schemes/23x23x23_r6009.npz
shasum -a 256 lita_23.npz     # e8741f9d13d65057c56097c65513f724ebd1b3fe007487995865d6a500a674af
.v/bin/python code/convert.py lita_23.npz lita_23.json
shasum -a 256 lita_23.json    # 9342b66ecccbd58cc4b7eb015fcc8f8483974c07af39bbc25661da4c49d57c0c
.v/bin/python code/rebuild_lita_slices.py lita_23.json step1.json step2.json     # about 452 s (nice, shared machine), peak RSS about 2.0 GB, footprint 2.1 GB
shasum -a 256 step1.json step2.json
#   step1.json 1bc458bbb2202fdae64f1ee6ea55cd5f03c6242e9f94b8e836aa3ef0d3e2b28b
#   step2.json 370144aeb4f75de8804f45a113da430c946f4609e1f3e49464f0f650581bed0e
.v/bin/python code/export_txt.py step2.json rebuilt/                                  # u.txt, v.txt, w.txt
for w in u v w; do if [ -f ../object/$w.txt ]; then cat ../object/$w.txt; else cat ../object/$w.part?.txt; fi | cmp - rebuilt/$w.txt || echo DIFFERENT $w; done; echo compared
.v/bin/python code/slice_accounting.py lita_23.json step1.json step2.json         # the kill counts below (seconds)
```

Input: the LITA scheme schemes/23x23x23_r6009.npz of Khoruzhii, Serafin, Gelss and Pokutta (https://github.com/khoruzhii/lita, commit 472a79fbc8248423a97bebb3aacbc89e769b9b3e, the repository head when fetched; fetched by the band run 2026-10-24T20:19:35Z, HTTP 200, sha256 e8741f9d13d65057c56097c65513f724ebd1b3fe007487995865d6a500a674af, 314180 bytes). It is third-party data with no licence file in its repository, so it is not copied here; the command above fetches it.

Determinism: the band run rebuilt this cell twice (second run 2026-10-24T20:38:16Z to 2026-10-24T20:45:41Z); the step-1 and step-2 JSON files and the text exports of the two runs are byte-identical (cmp), so the rebuild is reproducible for N = 23 on that machine. Their sha256 values are the ones above.

Real output of rebuild_lita_slices.py (band run, 2026-10-24T20:30:43Z to 2026-10-24T20:38:16Z UTC; 452 s wall, peak RSS 2.04 GB, peak footprint 2.12 GB; nice, on a shared laptop):

```
input (23, 23, 23) rank 6009
step 1: slice axis 0 -> (22, 23, 23) rank 5711
step 1: absorbed 1 -> rank 5710 (263s)
step 2: slice axis 1 -> (22, 22, 23) rank 5424
step 2: absorbed 1 -> rank 5423 (450s)
wrote cells/N23/run1/step1.json cells/N23/run1/step2.json
```

The rebuild's intermediate step-1 scheme is the sibling cell <22,23,23> rank 5710 (a separate claim folder of this batch); the step-2 scheme is <22,22,23> rank 5423. The object of this claim is the step-2 scheme.

## The code

- code/convert.py: LITA's npz format (CSR rows with numerators and denominators) to JSON.
- code/engine.py: exact one-slice restriction (restrict) and exact 2-reductions (absorb_all). A 2-reduction finds a linear dependency sum_t c_t X_t (x) Y_t = 0 among the terms' paired factors (found modulo two 62-bit primes, lifted to Q by rational reconstruction, verified exactly), then shifts the third factors so one term disappears.
- code/rebuild_lita_slices.py: the two steps for any odd N (here N = 23). Slice direction e* = (1,...,1,-9 at index 11,1,...,1) on one side and e_0 on the other.
- code/export_txt.py: scheme JSON to the three plain text files; code/split_parts.py: how the files in object/ were cut into parts of under 1,000,000 bytes at line boundaries (the parts joined are byte-identical to the export).
- code/slice_accounting.py: counts which terms each slice kills and the plain coordinate projections (output below and in slice_accounting_output.txt).
- The pipeline files convert.py, engine.py, export_txt.py and rebuild_lita_slices.py are byte-identical to those of the 18x18x19 claim (PR #714), which ran them for N = 19 (cmp, checked when this folder was written). slice_accounting.py and split_parts.py are new in this batch.

## Where the removed terms go (code/slice_accounting.py, real output; the full output is slice_accounting_output.txt)

e* = (1,...,1,-9,1,...,1) with -9 at index 11; e_0 = the unit vector at index 0. A term vanishes in a slice when its factor on one side is an outer product with the slice direction on that side.

```
input <23,23,23> rank 6009

[coordinate projection, 23^3 -> 22x23x23] best row: delete index 11 -> 5963 terms (46 vanish); vanishing counts over all rows: [24, 33, 34, 46]
[coordinate projection, 23^3 -> 22x22x23] best pair: delete row 11 and column 11 -> 5917 terms (92 vanish)

star vector e*: entry -9 at index 11, 1 elsewhere; e_0 = unit vector at index 0

step 1, slice axis 0 (row index shared by A and C), e = e* on A, f = e_0 on C:
  terms with U = e* x^T (killed on the A side): 264; with W = e_0 y^T (killed on the C side): 34; both: 0; total 298
  after the slice: <22,23,23> rank 5711  (6009 - 298 = 5711)
  2-reduction(s) (saved step1.json): removed 1 -> rank 5710

[coordinate projection, 22x23x23:5710 -> 22x22x23] best column: delete index 11 -> 5675 terms (35 vanish); range of vanishing counts over all columns: (12, 35)

step 2, slice axis 1 (column index of A = row index of B), e = e_0 on A, f = e* on B:
  terms with U = x e_0^T (killed on the A side): 23; with V = e* y^T (killed on the B side): 263; both: 0; total 286
  after the slice: <22,22,23> rank 5424  (5710 - 286 = 5424)
  2-reduction(s) (saved step2.json): removed 1 -> rank 5423

summary: 6009 -[slice 1 kills 298]-> 5711 -[2-reduction]-> 5710 -[slice 2 kills 286]-> 5424 -[2-reduction]-> 5423; total removed 586
closed forms: step 1 removes (N^2+3N)/2 = 299 (measured 299); step 2 removes (N^2+2N-1)/2 = 287 (measured 287)
```

In words: 6009 (LITA <23,23,23>) - 298 (slice 1: 264 + 34) = 5711, - 1 (2-reduction) = 5710 (<22,23,23>), - 286 (slice 2: 23 + 263) = 5424, - 1 (2-reduction) = 5423 (<22,22,23>). For comparison, plain coordinate projections (deleting one index, no reductions) give 5963 from LITA 23^3 (delete row 11: 46 terms vanish); 5675 from the 5710 scheme (delete column 11: 35 vanish); 5917 from LITA 23^3 deleting one row and one column; all are above 5625 (the Lille block sum), the 5675 from the 5710 scheme and the 5917 from LITA 23^3.

## Closed forms (observed, not proved here)

Slice 1 plus its 2-reduction removed (N^2+3N)/2 = 299 terms and slice 2 plus its 2-reduction removed (N^2+2N-1)/2 = 287 terms, as for N = 15, 17 and 19 in the earlier work; they are measured counts for this N, not a theorem.
