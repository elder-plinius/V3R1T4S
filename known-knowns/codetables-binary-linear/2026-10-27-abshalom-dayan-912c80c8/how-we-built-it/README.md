# How we built it

- `parse_range.py RANGE.html OUT.json`: reads the codetables.de range page (q = 9, n = 28..36) into a dict
  "n,k" -> [lower, upper].
- `candidates.py RANGE.json PLAIN_D...`: lists the nested pairs C(D,aP) ⊂ C(D,bP) (27 affine points of
  y^3 + y = x^4) and tail lengths l whose Construction X upper estimate exceeds the table's lower bound at
  (27 + l, dim C(D,bP)).
- `gen_tail.py CAND CODEDIR HDEP OUTBLOCKS RMAX WORKERS`: for each candidate, the exact coset table mu(c) (minimum
  affine weight of each coset of C(D,aP) in C(D,bP), capped at D = lower bound + 1, computed with `hdep` built from
  `hdep.c`), written as one block for `tailg`.
- `tailg.c` (`cc -O2 -o tailg tailg.c; ./tailg < blocks`): exhaustive search for l tail columns (points of
  PG(r-1,9)) such that each hyperplane c-perp holds at most l - max(0, D - mu(c)) of them. Its output line for this
  code was `19,21,2,29,19 nodes=3 sols=1 0 2` (tailg stops at the first solution, so sols is 0 or 1).
- `build_code.py OUT.json`: rebuilds exactly the object in `object/` (same sha256) from the construction, with
  `hermitian.py` (curve points, one-point codes) and `gf9lib.py` (GF(9) arithmetic).
- `dualenum.c` + `macwilliams.py`, `hdep.c`: the dual-side exact distance checks (see `RUN_IT_YOURSELF.md`).
- `PREREG.md`: the run's preregistration for its first cell, [32,18] (no claim there). `PREREG.v2.md`: the
  preregistration for this cell, written after the d = 8 result was seen (it says so), with the same thresholds.
