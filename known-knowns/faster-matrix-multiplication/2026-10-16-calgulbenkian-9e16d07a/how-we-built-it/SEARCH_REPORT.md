# Candidate: <5,5,5> rank 93 with 332 reduced additions (Perminov's minimum: 383)

Status: PROMISING (builder opus-add, team addcomp). Not confirmed; the orchestrator's panel decides.

## What it is
`scheme.json` is a straight-line program in Perminov's reduced-scheme layout (`n`, `m`, `u_fresh`, `u`, `v_fresh`, `v`,
`w_fresh`, `w`; fresh variable k of a map gets index (#inputs of that map + k); every form is a list of index/value terms
with values +-1, so his own counter can recount it). It uses exactly the 93 products of Perminov's ternary scheme
`schemes/results/addition_reduced_ZT/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json` (fetched 2026-10-15 ~09:20Z): the expanded U, V, W matrices are
unchanged; only the programs that compute the three linear maps are new. All intermediate values are ternary
combinations of the inputs (no other scalars anywhere).

| map | Perminov | ours | how ours was found |
|---|---|---|---|
| U | 103 | 87 | cancellation search (src/bpopt*.c) on the map (`work/top150/5x5x5_m93/u_p_bp5b.graph`) |
| V | 105 | 88 | cancellation search (src/bpopt*.c) on the map (`work/top150/5x5x5_m93/v_p_bp5a.graph`) |
| W | 175 | 157 | cancellation search (src/bpopt*.c) on W^T, transposed back (transposition principle) (`work/top150/5x5x5_m93/w_t_bp6s.graph`) |
| total | 383 | 332 | margin 51 |

Program statistics (tools/stats.py): `{"u": {"fresh": 87, "cancelling_steps": 24, "max_abs_coeff": 1}, "v": {"fresh": 88, "cancelling_steps": 25, "max_abs_coeff": 1}, "w": {"fresh": 55, "cancelling_steps": 22, "max_abs_coeff": 1}}` (cancelling_steps = forms whose terms overlap and partly cancel;
max_abs_coeff = largest coefficient of any intermediate value over the map's inputs; 1 means every intermediate is a
ternary combination). Perminov's own programs have no cancelling steps.


## Other contributor's result
Per the orchestrator (2026-10-15): PR #186 by another contributor was merged with 358 reduced additions for
<5,5,5> rank 93. 332 is below both that and Perminov's 383.

## How it was checked (real output in check_output.txt)
- `check_slp.py` (mine, standard library): coefficients all +-1, straight-line order, exact expansion of every map over Z
  and the full tensor identity sum_q U_q (x) V_q (x) W_q = <5,5,5> (output C[i][k] at index k*n+i,
  Perminov's layout), plus evaluation of the program on 50 random integer matrix pairs; count = sum over all forms of
  (length - 1), Perminov's 'reduced' convention.
- `sym_check.py` (mine, sympy): runs the program on symbolic matrices, expands each output and compares it with A*B.
- Counter calibration: the same counter reproduces the `cr` of all 49 addition_reduced_ZT files at the Lille best rank
  with max side <= 8 (NOTES.md).

```
$ python check_slp.py scheme.json
{"file": "scheme.json", "format": "5x5x5", "rank": 93, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 87, "adds_V": 88, "adds_W": 157, "adds_total": 332, "naive_total": 843, "declared_reduced": 332, "VALID": true}

$ python sym_check.py scheme.json
{"file": "scheme.json", "format": "5x5x5", "rank": 93, "products": 93, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 332}
```

## What it would beat
- Perminov's live repository (tree fetched 2026-10-15 09:19Z), addition_reduced_ZT files for 5x5x5 rank 93: 5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json (cr 383).
  Minimum cr = 383. reduced_known.json, README and CHANGELOG (fetched 09:20Z) list nothing lower for this format and rank.
- Rank 93 is the best rank for 5x5x5 in fmm_sota.json (fetched 09:19Z).
- The orchestrator's literature scout (data/literature_bars.md, 2026-10-15) found no published comparable count below
  Perminov's repository for this format and rank (sources: Perminov arXiv:2512.13365 Tables 1-6, Martensson-Wagner ACDA25,
  matmulcatalog COVERAGE.md naive counts, Lille page without commentary). Open gap named there: IACR ePrint 2026/849
  could not be read.
- NOT checked by me (my brief allows no other fetches): the Lille per-format page's complexity variant and matmulcatalog's
  COVERAGE.md 'adds' column. The orchestrator must re-fetch those and Perminov's tree before any claim.

## How it was found
tools/opt_scheme.py splits the scheme into its three maps and runs, per map, (a) a Boyar-Peralta-style distance-guided
search with cancellation over ternary vectors (src/bpopt.c) on the tall maps U, V and W^T (the W program is then obtained
by the transposition principle, cost(W) = cost(W^T) + r - n*p), and (b) randomized iterated pair-greedy CSE on the
transposed maps (src/slpopt.c), keeping Perminov's own program for any map where ours is not strictly better.

## Credits
Splitting into three maps and optimising the transposed map (transposition principle) is from another contributor's
PR #149 on the V3R1T4S repo (DrZuzzjen, <4,6,7> 503 vs 517). The cancellation heuristic follows Boyar and Peralta's
shortest-linear-program heuristic. The base scheme is Perminov's (github.com/dronperminov/FastMatrixMultiplication).
All code here is opus-add's own.
