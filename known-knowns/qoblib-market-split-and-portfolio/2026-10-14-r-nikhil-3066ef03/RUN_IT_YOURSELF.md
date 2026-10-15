# Run it yourself

From this folder, in a fresh shell (needs `sh`, `curl` and Python 3; the checkers use only the standard library):

```sh
sh verify-it-yourself/run_checks.sh
```

What it does: downloads the two public QOBLIB instance files of `po_a200_t10_orig` from the pinned commit
`a6b69e46763f98997da11d9b6bf0bfd34a1d8271` (about 5 MB; third-party data is not copied into this package), checks
their sha256, then evaluates `object/a200_t10_orig_b050_l1e-02_solution.sol` with two independent exact evaluators
written from the class's ZIMPL reference model (`check_portfolio.py`: exact rationals; `zimpl_literal_eval.py`: the
model's binary variables and slack bits, term by term). Expected output ends with:

```
both evaluators: feasible, objective -691624 < bar -551385
PASS
```

About 10 seconds on a laptop (most of it the download). The real output is in `verify-it-yourself/RECEIPTS.md`.

To check by hand: the solution format is the class's canonical count format (`period symbol long short`, unit counts
0..3, header lines `instance`, `budget`, `lambda`, `objective`). The object holds positions in periods 0..8 and
nothing in period 9 (t_end).

To rebuild a portfolio of similar quality (not the same bytes; the search is randomised and time-capped), follow
`how-we-built-it/COMMANDS.md`.
