# QOBLIB 06-portfolio, po_a200_t10_orig, B = 50, lambda = 0.01: a portfolio with objective −691624

## What

The canonical count file claim/solution/a200_t10_orig_b050_l1e-02_solution.sol is feasible for QOBLIB class 06 instance po_a200_t10_orig (instance files as packaged in claim/instance/) with B = 50 and lambda = 0.01, and its exact objective under the class's minimised reference model (claim/definition/bqp_u3_c10.zpl with claim/definition/parameter_u3_c10.zpl, lambda set to 0.01, Zimpl rounding half away from zero) is -691624, strictly below (by 140239) the bar of -551385, which is the exactly re-evaluated objective of the PR #87 solution file copied in claim/bar/ and, per the claim's status record, the best value posted in an open QOBLIB pull request for cell a200_t10_orig_b050_l1e-02, a cell for which the official best-known table (copy in claim/bar/06-portfolio-solutions-README.md) has no row.

(Panel status: CONFIRMED_SOLUTION, `panel/gate.md`. The panel's `claim/solution/...` file is this package's
`object/a200_t10_orig_b050_l1e-02_solution.sol`, same sha256; the instance files are downloaded and pinned by sha256
in `verify-it-yourself/run_checks.sh` instead of being copied here.)

The object is `object/a200_t10_orig_b050_l1e-02_solution.sol` (sha256
3066ef033d46c6e8fdb38d20f562a6e5ff41b67e4b64881c9988a67fdfe58097), in the class's canonical count format.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (after `both evaluators: feasible, objective -691624 < bar -551385`). About 10 seconds on a
laptop, most of it downloading the public instance files from a pinned QOBLIB commit. Details: `RUN_IT_YOURSELF.md`;
real output: `verify-it-yourself/RECEIPTS.md`.

## Compared to

| what | value | source | fetched (UTC) |
|---|---|---|---|
| official best-known table, row for this cell | none (no a200 or a400 rows) | https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md (sha256 05a6d233…) | 2026-10-14T17:20:24Z |
| best posted value for this cell | **−551385** | open QOBLIB PR #87 (RestrictedChainDP), head 1772e1d7…, file `06-portfolio/submissions/20261009_RestrictedChainDP_Gupta/a200_t10_orig_b050_l1e-02/a200_t10_orig_b050_l1e-02_solution.sol` | PR list 2026-10-14T17:20:25Z |
| other posted value | −300647 | open QOBLIB PR #64 (4colors-Optimizer), head e2fefab5… | same |
| this object | **−691624** (25.4% lower) | `object/` | — |

Full snapshot with hashes: `the-record-we-beat/RECORD.md`. The panel's own fetches: `panel/novelty.md`.

## Not claimed

- Not a row of the official QOBLIB best-known table: that table has no row for this cell. The comparison is with the
  values posted in open QOBLIB pull requests, as the research charter defines the bar.
- Not optimal and not a bound: the continuous relaxation (about −836k, risk on 29 factors) and SCIP's per-period dual
  bounds (neighbours fixed) suggest room remains; neither is a certified bound for the cell.
- Not checked by QOBLIB's own Rust check programs (not installed here); checked by two independent exact evaluators
  written from the class's ZIMPL model, and by the panel's own checker.
- Nothing about other cells, other lambdas or other instances.
- Not submitted anywhere. QOBLIB added an AI-use policy and a disclosure requirement for submissions on 2026-10-13;
  anyone submitting this must follow it.

## Credits

- T. Koch et al., "Quantum Optimization Benchmarking Library — The Intractable Decathlon", arXiv:2504.03832, and the
  QOBLIB maintainers (https://github.com/ZIB-AOPT/QOBLIB): the class definition, the ZIMPL reference model, the
  instance data and the best-known table.
- The authors of open QOBLIB PR #87 (RestrictedChainDP, GitHub user mnn31) and PR #64 (4colors-Optimizer, GitHub user
  marcinjkaminski): the values compared against (https://github.com/ZIB-AOPT/QOBLIB/pull/87,
  https://github.com/ZIB-AOPT/QOBLIB/pull/64).
- Tools: HiGHS (continuous relaxation), python-flint / FLINT (LLL), NumPy, SCIP via PySCIPOpt (per-period bounds).
