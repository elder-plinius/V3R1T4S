# How the object was built (exact commands)

Python 3.14 with numpy 2.5.4 and python-flint 0.9.0 (requirements.txt). From this folder (how-we-built-it/):

```sh
python3 -m venv .v && .v/bin/pip install -r requirements.txt
curl -sS -o lita_19.npz https://raw.githubusercontent.com/khoruzhii/lita/472a79fbc8248423a97bebb3aacbc89e769b9b3e/schemes/19x19x19_r3633.npz
shasum -a 256 lita_19.npz    # 72633df65c1da7195d1a3284845cf82bf70c5e11c969895a33b7167bd978889b
.v/bin/python code/convert.py lita_19.npz lita_19.json
.v/bin/python code/rebuild_lita_slices.py lita_19.json step1.json step2.json     # about 2.5 minutes, under 0.7 GB
.v/bin/python code/export_txt.py step2.json rebuilt/                              # u.txt, v.txt, w.txt
cmp rebuilt/u.txt ../object/u.txt && cat ../object/v.part1.txt ../object/v.part2.txt | cmp - rebuilt/v.txt && cmp rebuilt/w.txt ../object/w.txt && echo SAME
```

Input: the LITA scheme schemes/19x19x19_r3633.npz of Khoruzhii, Serafin, Gelss and Pokutta
(https://github.com/khoruzhii/lita, commit 472a79fbc8248423a97bebb3aacbc89e769b9b3e, the repository head on
2026-10-24; git blob 397b9f9d6e99d3105b1464e5f4f0a04679d71fee; 185669 bytes). It is third-party data with no licence
file in its repository, so it is not copied here; the command above fetches it.

Real output of rebuild_lita_slices.py (this run, 2026-10-24T19:05:42Z to 19:08:01Z; 138 s, peak memory 0.69 GB):

```
input (19, 19, 19) rank 3633
step 1: slice axis 0 -> (18, 19, 19) rank 3425
step 1: absorbed 1 -> rank 3424 (78s)
step 2: slice axis 1 -> (18, 18, 19) rank 3226
step 2: absorbed 1 -> rank 3225 (137s)
```

The rebuild is deterministic (the 2-reduction uses fixed primes and fixed random seeds): the step-2 JSON
(sha256 b0201deab3266b2bf3b69790931babcbdc0dd15ca697bfce734ad142356df69c) is byte-identical to the scheme first built
on 2026-10-24 at 17:37:31Z by the earlier run, and export_txt.py turns it into exactly the three files in ../object/
(v.txt split into two parts at a line boundary).

## The code

- code/convert.py: LITA's npz format (CSR rows with numerators and denominators) to JSON.
- code/engine.py: exact one-slice restriction (restrict) and exact 2-reductions (absorb_all). A 2-reduction finds a
  linear dependency sum_t c_t X_t (x) Y_t = 0 among the terms' paired factors (found modulo two 62-bit primes, lifted
  to Q by rational reconstruction, verified exactly), then shifts the third factors so one term disappears.
- code/rebuild_lita_slices.py: the two steps for any odd N (here N = 19).
- code/drop_accounting.py: replays both steps and counts which terms each slice kills (below).
- code/predict_p1_band.py and trackB_predict_p1_band.txt: the earlier run's closed-form prediction (3225 for N = 19),
  saved there at 17:42:29Z, after the build at 17:37:31Z (see PREREG.md for the timing).

## Where the 408 removed terms go (code/drop_accounting.py, real output)

e* = (1,...,1,-7,1,...,1) with -7 at index 9; e_0 = the unit vector at index 0. A term vanishes in a slice when its
factor on one side is an outer product with the slice direction on that side.

```
input <19,19,19> rank 3633

[coordinate projection, 19^3 -> 18x19x19] best row: delete index 9 -> 3595 terms (38 vanish); other rows: [20, 27, 28, 38]
[coordinate projection, 19^3 -> 18x18x19] best pair: delete row 9 and column 9 -> 3557 terms (76 vanish)

star vector e*: entry -7 at index 9, 1 elsewhere; e_0 = unit vector at index 0

step 1, slice axis 0 (row index shared by A and C), e = e* on A, f = e_0 on C:
  terms with U = e* x^T (killed on the A side): 180; with W = e_0 y^T (killed on the C side): 28; both: 0; total 208
  after the slice: <18,19,19> rank 3425  (3633 - 208 = 3425)
  2-reduction: dependency among the v (B side) and w (C side) factors, removed 1 term -> rank 3424
  step 1 result: <18,19,19> rank 3424

[coordinate projection, 18x19x19:3424 -> 18x18x19] best column: delete index 9 -> 3395 terms (29 vanish); range of vanishing counts over all columns: (10, 29)

step 2, slice axis 1 (column index of A = row index of B), e = e_0 on A, f = e* on B:
  terms with U = x e_0^T (killed on the A side): 19; with V = e* y^T (killed on the B side): 179; both: 0; total 198
  after the slice: <18,18,19> rank 3226  (3424 - 198 = 3226)
  2-reduction: dependency among the u (A side) and w (C side) factors, removed 1 term -> rank 3225
  step 2 result: <18,18,19> rank 3225

replayed scheme identical (term by term, exact) to rebuilt.step2.json: True

summary: 3633 -[slice 1 kills 208]-> 3425 -[2-reduction]-> 3424 -[slice 2 kills 198]-> 3226 -[2-reduction]-> 3225
```

In words: 3633 (LITA <19,19,19>) - 208 (slice 1: 180 + 28) = 3425, - 1 (2-reduction) = 3424 (<18,19,19>),
- 198 (slice 2: 19 + 179) = 3226, - 1 (2-reduction) = 3225 (<18,18,19>). For comparison, plain coordinate
projections (deleting one index, no reductions) give 3557 from LITA 19^3 (delete row 9 and column 9: 76 terms vanish)
and 3395 from the 3424 scheme (delete column 9: 29 vanish); both are above the table value 3355.
