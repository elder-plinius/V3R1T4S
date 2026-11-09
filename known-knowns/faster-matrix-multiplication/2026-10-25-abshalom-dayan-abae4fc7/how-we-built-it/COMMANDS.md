# How the object was built (exact commands)

Python 3.14 with numpy 2.5.4 and python-flint 0.9.0 (requirements.txt). From this folder:

```sh
python3 -m venv .v && .v/bin/pip install -r requirements.txt
curl -sS -o lita_15.npz https://raw.githubusercontent.com/khoruzhii/lita/HEAD/schemes/15x15x15_r1977.npz
shasum -a 256 lita_15.npz   # 94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33
.v/bin/python code/convert.py lita_15.npz lita_15.json
.v/bin/python code/rebuild_chain.py lita_15.json rebuilt.json \
  0/1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1/-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1/5001/6 \
  1/1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1/1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1/1030/6
.v/bin/python code/export_txt.py rebuilt.json rebuilt/                # u.txt, v.txt, w.txt
cat ../object/u.part1.txt ../object/u.part2.txt | cmp - rebuilt/u.txt && cat ../object/v.part1.txt ../object/v.part2.txt | cmp - rebuilt/v.txt && cmp ../object/w.txt rebuilt/w.txt && echo SAME
```

`rebuild_chain.py` prints (1 min 30 s wall clock at low priority on a shared laptop):

```
parent <15,15,15> rank 1977
step 1: slice axis 0 with e=1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1 f=-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 -> (14, 15, 15) rank 1865
step 1: flat absorption (seed 5001, restarts 6) removed 29 -> rank 1836
step 2: slice axis 1 with e=1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1 f=1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1 -> (14, 14, 15) rank 1731
step 2: flat absorption (seed 1030, restarts 6) removed 22 -> rank 1709
```

and the comparison prints SAME. The run's self-break session reproduced exactly these lines and SAME (SELF_BREAK.md);
this package's own code and object files were re-run the same way at packaging time with python-flint 0.9.0 and numpy 2.5.4
and gave the same five lines and SAME.

- `code/engine.py`: exact one-slice restriction of a scheme (`restrict`) and exact 2-reduction machinery (linear
  dependencies among the terms' paired factors, found modulo primes, lifted to Q, and every reduced scheme re-verified
  exactly before it is kept).
- `code/flat.py`: the "flat" (consensus) absorption used after each slice: exact linear dependencies among terms,
  removed by shifting the third factor; seeded, so the result is deterministic.
- `code/rebuild_chain.py`: the chain used here. Step 1 slices the row index i shared by A and C, with
  e = (1,...,1,-5,1,...,1) (-5 at index 7) on the A side and f = (-1,1,...,1) on the C side: 112 terms vanish
  (1977 -> 1865), flat absorption removes 29 (-> 1836, a <14,15,15> scheme). Step 2 slices the inner index j shared by
  A and B with e = f = (1,...,1,-5,1,...,1): 105 terms vanish (-> 1731), absorption removes 22 (-> 1709).
- `code/convert.py`: LITA's npz format to the JSON the engine reads. `code/export_txt.py`: the JSON to the three
  plain text factor files (object/).
- `PREREG.md`: the run's pre-registration (criterion, checker, threshold, one cell per claim), frozen at
  2026-10-25T03:51:33Z before any scored output.
- `SELF_BREAK.md`: summary of the run's own attempt to refute the claim (verdict SURVIVES).
- `CLAIM.md` and `REPRODUCE.md`: the claim file and the reproduction notes the panel was given (see README, "Notes
  on the panel files"). REPRODUCE.md is the claim-folder original, so its paths (`rebuild/...`, `object/u.txt`) refer
  to the claim folder, not to this package.

The LITA scheme itself is third-party data and is not copied into this package.
