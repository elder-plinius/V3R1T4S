# QOBLIB 06-portfolio, po_a200_t10_s00, B = 50, lambda = 0.01: a portfolio with objective −644342

## What

The frozen solution file (sha256 8650bc1e...efe62) is feasible for QOBLIB class 06 instance po_a200_t10_s00 with B = 50 and lambda = 0.01 under the reference model bqp_u3_c10.zpl and has exact minimised objective −644342, strictly below the best value posted in the open-PR files supplied for this cell (PR #87, −401535; PR #64, −192428), a cell for which the official best-known table has no row.

(Panel status: CONFIRMED_SOLUTION, `panel/gate.md`. The panel's `claim/solution/...` file is this package's
`object/a200_t10_s00_b050_l1e-02_solution.sol`, same sha256; the instance files are downloaded and pinned by sha256
in `verify-it-yourself/run_checks.sh` instead of being copied here.)

The object is `object/a200_t10_s00_b050_l1e-02_solution.sol` (sha256
8650bc1e720ff19bd4f17cedefb5b4021dbcd1a3315c8a79abd6d79cf82efe62), in the class's canonical count format.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (after `both evaluators: feasible, objective -644342 < bar -401535`). About 10 seconds on a
laptop, most of it downloading the public instance files from a pinned QOBLIB commit. Details: `RUN_IT_YOURSELF.md`;
real output: `verify-it-yourself/RECEIPTS.md`.

## Compared to

| what | value | source | fetched (UTC) |
|---|---|---|---|
| official best-known table, row for this cell | none (no a200 or a400 rows) | https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md (sha256 05a6d233…) | 2026-10-15T09:01:05Z |
| best posted value for this cell | **−401535** | open QOBLIB PR #87 (RestrictedChainDP), head 1772e1d7…, file `06-portfolio/submissions/20261009_RestrictedChainDP_Gupta/a200_t10_s00_b050_l1e-02/a200_t10_s00_b050_l1e-02_solution.sol` | PR list 2026-10-15T09:01:06Z |
| other posted value | −192428 | open QOBLIB PR #64 (4colors-Optimizer), head e2fefab5… | same |
| QOBLIB paper (arXiv:2504.03832 v1, Table 6, a200_t10_s00, lambda 0.01) | −36277 (ABS2), 136536 (Gurobi incumbent) | https://arxiv.org/html/2504.03832v1 | 2026-10-15T09:05:40Z (panel) |
| this object | **−644342** (60.5% lower than the bar) | `object/` | — |

Full snapshot with hashes: `the-record-we-beat/RECORD.md`. The panel's own fetches: `panel/novelty.md`.

## Not claimed

- Not a row of the official QOBLIB best-known table: that table has no row for this cell. The comparison is with the
  values posted in open QOBLIB pull requests (and any other public source found), as the research charter defines
  the bar.
- Not optimal and not a bound: the continuous relaxation of the factor model (about −815k) suggests room remains; it
  is not a certified bound for the cell.
- Not checked by QOBLIB's own Rust check programs (not installed here); checked by two independent exact evaluators
  written from the class's ZIMPL model, and by the panel's own checkers.
- The exact value uses ZIMPL's round-half-away-from-zero: 200 coefficients are exact ties (5/2, the t = 0 short cost).
  Under half-to-even the object scores −644365 and the bar −401558; the comparison does not change.
- Nothing about other cells, other lambdas or other instances.
- Not submitted anywhere. QOBLIB added an AI-use policy and a disclosure requirement for submissions on 2026-10-13;
  anyone submitting this must follow it.

## Credits

- T. Koch et al., "Quantum Optimization Benchmarking Library — The Intractable Decathlon", arXiv:2504.03832, and the
  QOBLIB maintainers (https://github.com/ZIB-AOPT/QOBLIB): the class definition, the ZIMPL reference model, the
  instance data and the best-known table.
- The authors of open QOBLIB PR #87 (RestrictedChainDP, GitHub user mnn31) and PR #64 (4colors-Optimizer, GitHub user
  marcinjkaminski): the values compared against (https://github.com/ZIB-AOPT/QOBLIB/pull/87,
  https://github.com/ZIB-AOPT/QOBLIB/pull/64). KenWuqianghao/qoblib-solvers
  (https://github.com/KenWuqianghao/qoblib-solvers) was checked for other posted values.
- Tools: HiGHS (continuous relaxation), NumPy.
