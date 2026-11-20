# Farkas certificate: no [[116,2,39]] qubit stabilizer code, upper bound 39 down to 38

## What

Exact integer Farkas certificate (quantum weight-enumerator LP with shadow constraints, no purity assumption) that no qubit stabilizer code [[116,2,d]] with d at least 39 exists, so the upper bound for [[116,2]] is at most 38 against the live value 39 fetched 2026-10-19; the value is below the propagation closure of the live table plus the 56 listed pull-request values plus the other claimed cells.

Path note: the sentence above is quoted word for word from `panel/gate.md` (status `CONFIRMED_SOLUTION`). The object is `object/cert_116_2_39_sh.json` (sha256 75442b540f360d9b334d6bd2fb1d912390213fe5c55330a24c63cadfd72d5be1); its programs are in `how-we-built-it/`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 1 second on the packager's machine; allow a minute or two on a slow laptop.
- **Expected last line**: `PASS`

The quick check verifies the object's hash against INDEX.csv, rebuilds every row of the quantum weight-enumerator linear program (with shadow rows) from the definition in exact integers, checks the multiplier signs and that the combined coefficient of every variable is at most 0 while the right-hand side is positive, compares with the live bound and the one-step propagation neighbours and pull-request values in `the-record-we-beat/`, and confirms that a certificate with the shadow multipliers removed is rejected. The checker alone: `python3 -I verify-it-yourself/qubit_cert_check.py object/cert_116_2_39_sh.json 39`, whose last output line begins: `{"n": 116, "k": 2, "d": 39, "VALID": true}`. Its real output is in `verify-it-yourself/RECEIPTS.md`. The checker differs from the one the panel ran only in file locations and the last output line (see RECEIPTS.md).

## Compared to

| Source | Cell | Listed value | URL | UTC fetch time |
|---|---|---|---|---|
| QECC qubit table, n 1..256 | QECC qubit table, n 1..256 | [[116,2]]: lower 25, upper 39; neighbours in neighbours.csv | https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256 | 2026-10-19T04:34:26Z (triage); 2026-10-19T05:16:36Z (novelty skeptic) |
| GitHub pull-request list of elder-plinius/V3R1T4S (merged and open pull requests for this target) | upper-bound values already claimed | 56 values in `the-record-we-beat/pr_claims.csv` | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls | 2026-10-19T04:30:31Z |
| V3R1T4S TROPHY_CASE.md and known-knowns folders | this cell | no competing value (see `panel/novelty.md`) | https://github.com/elder-plinius/V3R1T4S | 2026-10-19T05:15:21Z (novelty skeptic) |
| arXiv, four generic queries plus the named work 2609.37056 | this cell | no newer claim found (queries were generic, not exhaustive; see `panel/novelty.md`) | https://arxiv.org/abs/2609.37056 | 2026-10-19 (novelty skeptic) |

Ours: [[116,2]] upper bound, value 38; the table value in `INDEX.csv` is "lower 25 upper 39". Each page was fetched once, with a plain GET and no retry; snapshot metadata (HTTP status, sha256 of the page, the extracted cell) is in `the-record-we-beat/README.md`. The panel's reports are in `panel/`.

## Not claimed

- This is a claim about an upper bound for one cell: no qubit stabilizer code [[n,k,d]] exists at the excluded distance, so the table's upper bound can drop by 1. It gives no code and does not change the lower bound.
- The certificate is an exact integer Farkas certificate of the quantum weight-enumerator linear program with shadow constraints, with no purity assumption. Nothing is numerical.
- The bar is a propagation closure fixed on 2026-10-19: the live table, plus the 56 merged and open pull-request values listed in `the-record-we-beat/pr_claims.csv`, plus the other claimed cells of this batch at their claimed values. Pull requests merged or opened after that, and bounds in the literature, are not counted. The new bound is only 1 below the live value.
- The table page itself says that for n above 100 its upper bounds are weak; the claim does not say that no stronger argument exists, only that this certificate is valid and the cell is below the closure above.
- Unresolved from the panel: the table's n above 100 upper bounds are called 'weak' on the page and the full quantum LP with shadow constraints may have been run privately by the maintainers; no public record of that was found. The literature search was generic (four queries).
- Not peer reviewed. The package was checked by three fresh Claude Code subagents (reproduce, novelty, criterion) and by the standalone checker shipped here. The object was built by a different model family (Gemini, the contributor's search agent); the skeptics and the packager are Claude.

## Filing history

New submission. The gate notes name no earlier pull request for this cell.

## Credits

- **codetables.de** (http://www.codetables.de/), the table compared against, maintained by Markus Grassl as the bank statement for this target names it.
- **Calderbank, Rains, Shor and Sloane**, arXiv quant-ph/9608006 (https://arxiv.org/abs/quant-ph/9608006), the quaternary MacWilliams identity for quantum codes, named in the bank statement.
- **Eric Rains**, whose MAGMA linear-programming program gave the table's upper bounds for n up to 100 (as the bank statement for this target says), and the shadow-enumerator method cited there as Rains 1999 and Ashikhmin-Litsyn.
- The authors of the 56 merged and open pull requests whose values the propagation closure counts (`the-record-we-beat/pr_claims.csv` lists cell, value, state and pull-request number).
- **python-flint**, used by the contributor's LP solver (`how-we-built-it/qlp.py`).
- The object and the search code are by Gemini ("Argon"), an AI search agent working for the contributor. Contributor credit: `calgulbenkian`.
- The three panel reports are by fresh Claude Code subagents (`panel/`).
