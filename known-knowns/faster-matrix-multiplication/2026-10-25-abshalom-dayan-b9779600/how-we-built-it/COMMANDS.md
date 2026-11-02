# How the object was built (exact commands)

```sh
# Python 3.14 with numpy 2.5.4 and python-flint 0.9.0 (requirements.txt). From this folder (how-we-built-it/):
python3 -m venv .v && .v/bin/pip install -r requirements.txt
curl -sS -o lita_21.npz https://raw.githubusercontent.com/khoruzhii/lita/472a79fbc8248423a97bebb3aacbc89e769b9b3e/schemes/21x21x21_r4723.npz
shasum -a 256 lita_21.npz     # 9d8389744035a57e63a5eb13cd766ddbd695e2bc71e6b25f9ce5eacdbd0d6397
.v/bin/python code/convert.py lita_21.npz lita_21.json
shasum -a 256 lita_21.json    # 3b3365df780c826fd8328ce533dcc51b7001b3b0fa10e36615ce1bcb3a92cdbf
.v/bin/python code/rebuild_lita_slices.py lita_21.json step1.json step2.json     # about 244 s (nice, shared machine), peak RSS about 1.2 GB, footprint 1.2 GB
shasum -a 256 step1.json step2.json
#   step1.json 1d699e27d625308d31368071af39066f29f0aab505cc08ac5b67c2314fb67673
#   step2.json e59a38f5145baf57c7ae8192e4447cb1f5475186e3bbbe340f4fc2f89d8493ec
.v/bin/python code/export_txt.py step2.json rebuilt/                                  # u.txt, v.txt, w.txt
for w in u v w; do if [ -f ../object/$w.txt ]; then cat ../object/$w.txt; else cat ../object/$w.part?.txt; fi | cmp - rebuilt/$w.txt || echo DIFFERENT $w; done; echo compared
.v/bin/python code/slice_accounting.py lita_21.json step1.json step2.json         # the kill counts below (seconds)
```

Input: the LITA scheme schemes/21x21x21_r4723.npz of Khoruzhii, Serafin, Gelss and Pokutta (https://github.com/khoruzhii/lita, commit 472a79fbc8248423a97bebb3aacbc89e769b9b3e, the repository head when fetched; fetched by the band run 2026-10-24T20:19:35Z, HTTP 200, sha256 9d8389744035a57e63a5eb13cd766ddbd695e2bc71e6b25f9ce5eacdbd0d6397, 243247 bytes). It is third-party data with no licence file in its repository, so it is not copied here; the command above fetches it.

Determinism: the band run rebuilt this cell twice (second run 2026-10-24T20:26:04Z to 2026-10-24T20:30:16Z); the step-1 and step-2 JSON files and the text exports of the two runs are byte-identical (cmp), so the rebuild is reproducible for N = 21 on that machine. Their sha256 values are the ones above.

Real output of rebuild_lita_slices.py (band run, 2026-10-24T20:22:01Z to 2026-10-24T20:26:04Z UTC; 244 s wall, peak RSS 1.20 GB, peak footprint 1.20 GB; nice, on a shared laptop):

```
input (21, 21, 21) rank 4723
step 1: slice axis 0 -> (20, 21, 21) rank 4472
step 1: absorbed 1 -> rank 4471 (143s)
step 2: slice axis 1 -> (20, 20, 21) rank 4231
step 2: absorbed 1 -> rank 4230 (242s)
wrote cells/N21/run1/step1.json cells/N21/run1/step2.json
```

The rebuild's intermediate step-1 scheme is the sibling cell <20,21,21> rank 4471 (a separate claim folder of this batch); the step-2 scheme is <20,20,21> rank 4230. The object of this claim is the step-2 scheme.

## The code

- code/convert.py: LITA's npz format (CSR rows with numerators and denominators) to JSON.
- code/engine.py: exact one-slice restriction (restrict) and exact 2-reductions (absorb_all). A 2-reduction finds a linear dependency sum_t c_t X_t (x) Y_t = 0 among the terms' paired factors (found modulo two 62-bit primes, lifted to Q by rational reconstruction, verified exactly), then shifts the third factors so one term disappears.
- code/rebuild_lita_slices.py: the two steps for any odd N (here N = 21). Slice direction e* = (1,...,1,-8 at index 10,1,...,1) on one side and e_0 on the other.
- code/export_txt.py: scheme JSON to the three plain text files; code/split_parts.py: how the files in object/ were cut into parts of under 1,000,000 bytes at line boundaries (the parts joined are byte-identical to the export).
- code/slice_accounting.py: counts which terms each slice kills and the plain coordinate projections (output below and in slice_accounting_output.txt).
- The pipeline files convert.py, engine.py, export_txt.py and rebuild_lita_slices.py are byte-identical to those of the 18x18x19 claim (PR #714), which ran them for N = 19 (cmp, checked when this folder was written). slice_accounting.py and split_parts.py are new in this batch.

## Where the removed terms go (code/slice_accounting.py, real output; the full output is slice_accounting_output.txt)

e* = (1,...,1,-8,1,...,1) with -8 at index 10; e_0 = the unit vector at index 0. A term vanishes in a slice when its factor on one side is an outer product with the slice direction on that side.

```
input <21,21,21> rank 4723

[coordinate projection, 21^3 -> 20x21x21] best row: delete index 10 -> 4681 terms (42 vanish); vanishing counts over all rows: [22, 30, 31, 42]
[coordinate projection, 21^3 -> 20x20x21] best pair: delete row 10 and column 10 -> 4639 terms (84 vanish)

star vector e*: entry -8 at index 10, 1 elsewhere; e_0 = unit vector at index 0

step 1, slice axis 0 (row index shared by A and C), e = e* on A, f = e_0 on C:
  terms with U = e* x^T (killed on the A side): 220; with W = e_0 y^T (killed on the C side): 31; both: 0; total 251
  after the slice: <20,21,21> rank 4472  (4723 - 251 = 4472)
  2-reduction(s) (saved step1.json): removed 1 -> rank 4471

[coordinate projection, 20x21x21:4471 -> 20x20x21] best column: delete index 10 -> 4439 terms (32 vanish); range of vanishing counts over all columns: (11, 32)

step 2, slice axis 1 (column index of A = row index of B), e = e_0 on A, f = e* on B:
  terms with U = x e_0^T (killed on the A side): 21; with V = e* y^T (killed on the B side): 219; both: 0; total 240
  after the slice: <20,20,21> rank 4231  (4471 - 240 = 4231)
  2-reduction(s) (saved step2.json): removed 1 -> rank 4230

summary: 4723 -[slice 1 kills 251]-> 4472 -[2-reduction]-> 4471 -[slice 2 kills 240]-> 4231 -[2-reduction]-> 4230; total removed 493
closed forms: step 1 removes (N^2+3N)/2 = 252 (measured 252); step 2 removes (N^2+2N-1)/2 = 241 (measured 241)
```

In words: 4723 (LITA <21,21,21>) - 251 (slice 1: 220 + 31) = 4472, - 1 (2-reduction) = 4471 (<20,21,21>), - 240 (slice 2: 21 + 219) = 4231, - 1 (2-reduction) = 4230 (<20,20,21>). For comparison, plain coordinate projections (deleting one index, no reductions) give 4681 from LITA 21^3 (delete row 10: 42 terms vanish); 4439 from the 4471 scheme (delete column 10: 32 vanish); 4639 from LITA 21^3 deleting one row and one column; all are above 4394 (the Lille block sum), the 4439 from the 4471 scheme and the 4639 from LITA 21^3.

## Closed forms (observed, not proved here)

Slice 1 plus its 2-reduction removed (N^2+3N)/2 = 252 terms and slice 2 plus its 2-reduction removed (N^2+2N-1)/2 = 241 terms, as for N = 15, 17 and 19 in the earlier work; they are measured counts for this N, not a theorem.
