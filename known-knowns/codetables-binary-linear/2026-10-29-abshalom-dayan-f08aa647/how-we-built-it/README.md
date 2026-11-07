# How we built it

- `gen_tail.py CAND CODEDIR HDEP OUTBLOCKS RMAX WORKERS`: for each candidate nested pair C(D,aP) ⊂ C(D,bP) of
  one-point Hermitian codes (27 affine points of y^3 + y = x^4) and tail length l, the exact coset table mu(c)
  (minimum affine weight of each coset, capped at D = lower bound + 1, computed with `hdep` built from `hdep.c`),
  written as one block for `tailg`. (Written in an earlier V3R1T4S run; CAND is that run's candidate list, not shipped.)
- `tailg.c` (`cc -O2 -o tailg tailg.c; ./tailg < blocks`): exhaustive search for l tail columns (points of
  PG(r-1,9)) such that each hyperplane c-perp holds at most l - max(0, D - mu(c)) of them. For the pair
  C(D,16P) ⊂ C(D,19P) with l = 4 and D = 11 its output line was `16,19,4,31,17 nodes=15 sols=1 0 1 2 13` (point
  indices in lexicographic order, first nonzero coordinate 1; tailg stops at the first solution). The run that panelled this claim
  reran tailg on the same block line and got the same output.
- `build_tail.py a b idx,... OUT`: builds the Construction X matrix from a tailg solution; `to_json.py` writes the
  JSON object; `build_code.py OUT.json` runs both (`build_tail.py 16 19 0,1,2,13`) and rebuilds exactly the object in
  `object/` (same sha256), with `hermitian.py` (curve points) and `gf9lib.py` (GF(9) arithmetic).
- `hdep.c`: the dual-side exact distance check (see `RUN_IT_YOURSELF.md`).
- `PREREG.md`: the run's preregistration, written before this run rebuilt or measured the object.
