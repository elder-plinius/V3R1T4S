# Certified re-evaluation of Kim-Nguyen Tables 1-2 (Mertens first-counterexample bound)

Submission id: 2026-11-24-blocksavvy-829395f6. Bank target: mertens-smallest-counterexample-upper-bound,
partial win p1. This is a re-evaluation of printed table values, not a new bound on the first counterexample,
and not the bank's main win.

## What

For all 19 rows of Kim-Nguyen's arXiv:2502.21021v1 Tables 1-2 (5 for h_P, 14 for h_StR), the claim gives certified 320-bit ball values of h at the exact published y, computed from separately computed Arb zeros and well defined at 3 decimals under both rounding and truncation; at 3 decimals they agree with the print for 15 rows under both conventions, for Table 2 row 5 only at its printed 2 decimals, and convention-dependently for Table 2 rows 4, 7 and 9; and at printed precision Table 2 rows 1, 4, 12 and 14 are wrong under either convention.

In short: all 19 best-y rows of Kim-Nguyen, arXiv:2502.21021v1, Tables 1-2 (5 values of h_P, 14 of h_StR) were
recomputed in certified ball arithmetic from separately computed zeta zeros (complete lists: 14,950 zeros with
gamma < 14000, 98,625 with gamma < 74000). The paper mixes rounding and truncation, including in its y+sqrt(y)
column, so the comparison is reported under both conventions: 8 mismatches under rounding and 6 under truncation
at printed precision. Only Table 2 rows 1, 4, 12 and 14 are wrong under either convention; those four are
corrections at printed precision, not to 3 decimals. Table 2 rows 2, 7, 9 and 10 are convention-dependent at
printed precision; Table 2 row 4 is convention-dependent at 3 decimals. The record cell (Table 2 row 3) matches
the print, and |h_StR| > 1 + 6e-8 holds rigorously there. It is not claimed as new.

## Check it yourself

From this folder (python3 >= 3.8, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Rough time: under a second. The checker re-parses the 19 shipped balls and the
printed excerpt, recomputes the comparison under both conventions, and checks the object against
verify-it-yourself/expected.json, so a changed digit in the object is rejected. It does not recompute the zeta
zeros (that takes about 20 minutes with python-flint; see RUN_IT_YOURSELF.md and how-we-built-it/COMMANDS.md).

## Compared to

| table | cell | our value | table value | source | fetched (UTC) | HTTP | sha256 of fetched page |
|---|---|---|---|---|---|---|---|
| Wikipedia, Mertens conjecture | first-counterexample bound (status source) | re-evaluation of KN Tables 1-2; no new bound | exp(1.96e19) (Kim-Nguyen 2024) | https://en.wikipedia.org/wiki/Mertens_conjecture | 2026-11-24T12:13:59Z (NOVELTY; scout 07:39:50Z, same hash) | 200 | 6f5b7e5234e1e9f6283599b0d800c6ed393e98851e7538b6b5c2122b15f54b26 |
| Kim-Nguyen arXiv:2502.21021v1 | Tables 1-2 printed (y, h) pairs | 19 certified balls; 4 corrections at printed precision | the 19 printed h values | https://arxiv.org/pdf/2502.21021v1 | 2026-11-24T13:05:06Z (REPRODUCE; CRITERION 12:14:02Z, same hash) | 200 | 3141e044428b0ec955407ef0ef44682faed61c36cc8b8cfec3b26587b5818f54 |

The peer-reviewed record bound is unchanged. Re-fetch the status page immediately before submitting.

## Not claimed

- No new upper bound on the first counterexample, and no check of the Saouter-te Riele theorem's hypotheses.
- Not an independent zero-finding method: the zeros come from the same Arb library (FLINT acb.zeta_zeros) that
  Kim-Nguyen used for h_StR. For h_P they used Hurst's zeros, so Table 1 is the more source-independent check.
- The four corrections are at printed precision, not to 3 decimals. Table 2 rows 7 and 9 (and row 4 at 3 decimals)
  are convention-dependent, not established misprints at 3 decimals.
- The typeset journal tables (Res. Number Theory 11 (2025)) were not compared (paywall). The HAL post-referee
  copy (hal-05016898) prints the same digits as arXiv v1.
- The record cell is not new (see Credits). Bi and Hou's "Peak1" is a different polished point near Table 2 row 2
  (about -0.99590, uncertified), not a re-evaluation of that row.

## Credits

- **Contributor:** [BlockSavvy](https://github.com/BlockSavvy). Found with a V3R1T4S agent run, checked by a three-skeptic panel of fresh subagent contexts.
- **Seungki Kim and Phong Q. Nguyen:** the y values, the printed Tables 1-2, and their Arb evaluator. arXiv:2502.21021; ANTS XVI (2024); Zenodo 10775723; HAL [hal-05016898](https://hal.science/hal-05016898).
- **L. H. Gallego:** independent re-evaluation of the record cell, Zenodo [10.5281/zenodo.23700211](https://doi.org/10.5281/zenodo.23700211) (2026-10-27), section 4 "Control": -1.00745, ball arithmetic.
- **Zhenyu Bi and Enze Hou:** independent re-evaluation of the record cell, HAL [hal-05838582](https://hal.science/hal-05838582) (2026-10-26) and [github.com/bzyzz/mertens_bound](https://github.com/bzyzz/mertens_bound), path1_report.txt: -1.0074515722 (256-bit MPFR).
- **Yannick Saouter and Herman te Riele** (h_StR); **Janos Pintz** (h_P). **FLINT/Arb** and python-flint.
