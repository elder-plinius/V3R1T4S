# How the object was built (exact commands)

```sh
# Python 3.14 with numpy 2.5.4 and python-flint 0.9.0 (requirements.txt). From this folder (how-we-built-it/):
python3 -m venv .v && .v/bin/pip install -r requirements.txt
curl -sS -o lita_27.npz https://raw.githubusercontent.com/khoruzhii/lita/472a79fbc8248423a97bebb3aacbc89e769b9b3e/schemes/27x27x27_r9233.npz
shasum -a 256 lita_27.npz     # f62e6272e1fbcfcb02b57b8ffc7afc1896143e22f707e5f1791d9a6174a1132d
.v/bin/python code/convert.py lita_27.npz lita_27.json
shasum -a 256 lita_27.json    # c226ef423329f4ae2487c187845ba0e13b9a0ec4509b4d9a433579d8a163bfaf
.v/bin/python code/rebuild_lita_slices.py lita_27.json step1.json step2.json     # about 1653 s (nice, shared machine), peak RSS about 2.4 GB, footprint 3.7 GB
shasum -a 256 step1.json step2.json
#   step1.json b56d064b40ce579f579e089497e1b454fdef57af43ec292bcb55e470bf82a3b6
#   step2.json 3cb8d994b1b0dcf5342abdc64e10ac1dadb6c93a1e7a8304523e0f8b771cb2bb
.v/bin/python code/export_txt.py step2.json rebuilt/                                  # u.txt, v.txt, w.txt
for w in u v w; do if [ -f ../object/$w.txt ]; then cat ../object/$w.txt; else cat ../object/$w.part?.txt; fi | cmp - rebuilt/$w.txt || echo DIFFERENT $w; done; echo compared
.v/bin/python code/slice_accounting.py lita_27.json step1.json step2.json         # the kill counts below (seconds)
```

Input: the LITA scheme schemes/27x27x27_r9233.npz of Khoruzhii, Serafin, Gelss and Pokutta (https://github.com/khoruzhii/lita, commit 472a79fbc8248423a97bebb3aacbc89e769b9b3e, the repository head when fetched; fetched by the band run 2026-10-24T20:19:36Z, HTTP 200, sha256 f62e6272e1fbcfcb02b57b8ffc7afc1896143e22f707e5f1791d9a6174a1132d, 485407 bytes). It is third-party data with no licence file in its repository, so it is not copied here; the command above fetches it.

Determinism: NOT confirmed. N = 27 was rebuilt once (a second rebuild was started and aborted by the operator after about 20 s because one run alone took 1653 s and 2.44 GB RSS); the step JSON hashes above come from that single run. The claim's checkers do not depend on determinism: the object in object/ is what is checked, whatever the rebuild does.

Real output of rebuild_lita_slices.py (band run, 2026-10-24T21:17:04Z to 2026-10-24T21:44:37Z UTC; 1653 s wall, peak RSS 2.44 GB, peak footprint 3.72 GB; nice, on a shared laptop):

```
input (27, 27, 27) rank 9233
step 1: slice axis 0 -> (26, 27, 27) rank 8829
step 1: absorbed 1 -> rank 8828 (927s)
step 2: slice axis 1 -> (26, 26, 27) rank 8438
step 2: absorbed 1 -> rank 8437 (1650s)
wrote cells/N27/run1/step1.json cells/N27/run1/step2.json
```

The rebuild's intermediate step-1 scheme is the sibling cell <26,27,27> rank 8828 (a separate claim folder of this batch); the step-2 scheme is <26,26,27> rank 8437. The object of this claim is the step-2 scheme.

## The code

- code/convert.py: LITA's npz format (CSR rows with numerators and denominators) to JSON.
- code/engine.py: exact one-slice restriction (restrict) and exact 2-reductions (absorb_all). A 2-reduction finds a linear dependency sum_t c_t X_t (x) Y_t = 0 among the terms' paired factors (found modulo two 62-bit primes, lifted to Q by rational reconstruction, verified exactly), then shifts the third factors so one term disappears.
- code/rebuild_lita_slices.py: the two steps for any odd N (here N = 27). Slice direction e* = (1,...,1,-11 at index 13,1,...,1) on one side and e_0 on the other.
- code/export_txt.py: scheme JSON to the three plain text files; code/split_parts.py: how the files in object/ were cut into parts of under 1,000,000 bytes at line boundaries (the parts joined are byte-identical to the export).
- code/slice_accounting.py: counts which terms each slice kills and the plain coordinate projections (output below and in slice_accounting_output.txt).
- The pipeline files convert.py, engine.py, export_txt.py and rebuild_lita_slices.py are byte-identical to those of the 18x18x19 claim (PR #714), which ran them for N = 19 (cmp, checked when this folder was written). slice_accounting.py and split_parts.py are new in this batch.

## Where the removed terms go (code/slice_accounting.py, real output; the full output is slice_accounting_output.txt)

e* = (1,...,1,-11,1,...,1) with -11 at index 13; e_0 = the unit vector at index 0. A term vanishes in a slice when its factor on one side is an outer product with the slice direction on that side.

```
input <27,27,27> rank 9233

[coordinate projection, 27^3 -> 26x27x27] best row: delete index 13 -> 9179 terms (54 vanish); vanishing counts over all rows: [28, 39, 40, 54]
[coordinate projection, 27^3 -> 26x26x27] best pair: delete row 13 and column 13 -> 9125 terms (108 vanish)

star vector e*: entry -11 at index 13, 1 elsewhere; e_0 = unit vector at index 0

step 1, slice axis 0 (row index shared by A and C), e = e* on A, f = e_0 on C:
  terms with U = e* x^T (killed on the A side): 364; with W = e_0 y^T (killed on the C side): 40; both: 0; total 404
  after the slice: <26,27,27> rank 8829  (9233 - 404 = 8829)
  2-reduction(s) (saved step1.json): removed 1 -> rank 8828

[coordinate projection, 26x27x27:8828 -> 26x26x27] best column: delete index 13 -> 8787 terms (41 vanish); range of vanishing counts over all columns: (14, 41)

step 2, slice axis 1 (column index of A = row index of B), e = e_0 on A, f = e* on B:
  terms with U = x e_0^T (killed on the A side): 27; with V = e* y^T (killed on the B side): 363; both: 0; total 390
  after the slice: <26,26,27> rank 8438  (8828 - 390 = 8438)
  2-reduction(s) (saved step2.json): removed 1 -> rank 8437

summary: 9233 -[slice 1 kills 404]-> 8829 -[2-reduction]-> 8828 -[slice 2 kills 390]-> 8438 -[2-reduction]-> 8437; total removed 796
closed forms: step 1 removes (N^2+3N)/2 = 405 (measured 405); step 2 removes (N^2+2N-1)/2 = 391 (measured 391)
```

In words: 9233 (LITA <27,27,27>) - 404 (slice 1: 364 + 40) = 8829, - 1 (2-reduction) = 8828 (<26,27,27>), - 390 (slice 2: 27 + 363) = 8438, - 1 (2-reduction) = 8437 (<26,26,27>). For comparison, plain coordinate projections (deleting one index, no reductions) give 9179 from LITA 27^3 (delete row 13: 54 terms vanish); 8787 from the 8828 scheme (delete column 13: 41 vanish); 9125 from LITA 27^3 deleting one row and one column; all are above 8727 (the Lille block sum), the 8787 from the 8828 scheme and the 9125 from LITA 27^3.

## Closed forms (observed, not proved here)

Slice 1 plus its 2-reduction removed (N^2+3N)/2 = 405 terms and slice 2 plus its 2-reduction removed (N^2+2N-1)/2 = 391 terms, as for N = 15, 17 and 19 in the earlier work; they are measured counts for this N, not a theorem.
