# How the object was built (exact commands)

Python 3.14 with numpy 2.5.4 and python-flint 0.9.0 (requirements.txt). From this folder:

```sh
python3 -m venv .v && .v/bin/pip install -r requirements.txt
curl -sS -o lita_19.npz https://raw.githubusercontent.com/khoruzhii/lita/HEAD/schemes/19x19x19_r3633.npz
shasum -a 256 lita_19.npz   # 72633df65c1da7195d1a3284845cf82bf70c5e11c969895a33b7167bd978889b
.v/bin/python code/convert.py lita_19.npz lita_19.json
.v/bin/python code/rebuild_18x19x19.py lita_19.json rebuilt.json      # slice -> 3425, absorbed 1 -> 3424
.v/bin/python code/export_txt.py rebuilt.json rebuilt/                # u.txt, v.txt, w.txt
cat ../object/u.part1.txt ../object/u.part2.txt | cmp - rebuilt/u.txt && cmp ../object/v.txt rebuilt/v.txt && cmp ../object/w.txt rebuilt/w.txt && echo SAME
```

- `code/engine.py`: exact one-slice restriction of a scheme (`restrict`), and exact 2-reductions (`absorb_all`):
  linear dependencies among the terms' paired factors are found mod two 62-bit primes, lifted to Q by rational
  reconstruction, and every reduced scheme is re-verified exactly before it is kept.
- `code/rebuild_18x19x19.py`: the one step used here (slice of the row index shared by A and C with
  e = (1,...,1,-7,1,...,1), -7 at index 9, on the A side and f = e_0 on the C side; then 2-reductions).
- `code/rebuild_lita_slices.py`: the same for any odd N, plus a second slice (gives <18,18,19> 3225 from N = 19).
- `code/predict_p1_band.py`: the closed-form prediction for every odd N from 13 to 31, compared with the tables.
- `code/convert.py`: LITA's npz format to the JSON the engine reads.
- `PREREG.md`: the run's pre-registration (criterion, checker, threshold, one cell per claim), frozen at
  2026-10-24T16:14:48Z before any scored output.

The LITA scheme itself is third-party data and is not copied into this package.
