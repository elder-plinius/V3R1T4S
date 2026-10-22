# Constant-weight codes: upper bound A(35,14,14) <= 837 (exact Delsarte LP certificate)

## What

The exact rational Delsarte dual certificate in object/cert_A35_14_14.json proves A(35,14,14) <= 837, which is strictly below the table-implied upper bound 1143 (margin 306; the live cell prints no upper bound) as of the Andw.html page with sha256 15b15c8d...3349 fetched 2026-10-18; it is an upper-bound certificate only (enumerated partial win p2 under the PR #350 table-implied reading) and says nothing about any lower bound or code.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only (no numpy or mpmath).
- **Rough laptop time**: a few seconds.
- **Expected last line**: `ALL CHECKS PASS`

The checker rebuilds the eigenvalues of the Johnson scheme J(35,14) from the Eberlein polynomials in exact fractions, tests their orthogonality, confirms that every dual value in `object/cert_A35_14_14.json` is nonnegative and that the dual constraint holds at every Johnson distance, and requires the floor of the exact objective to equal 837. It also runs known-answer cells and three negative controls that must be rejected. Details: `RUN_IT_YOURSELF.md`.

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Brouwer, bounds for binary constant weight codes (live table) | A(35,14,14) | lower bound only, printed as `163`; no upper bound printed | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:54:26Z |
| Table-implied upper bound, computed from the page and the repository | A(35,14,14) | **1143** | https://aeb.win.tue.nl/codes/Andw.html and https://github.com/elder-plinius/V3R1T4S | 2026-10-18T17:54:26Z |
| This certificate | A(35,14,14) | **<= 837** (margin 306 below the table-implied bound) | `object/cert_A35_14_14.json` | not applicable |

How the table-implied bound is computed: take the minimum of (a) the upper bounds printed in the table, (b) the bounds already merged into the V3R1T4S repository, and (c) the two Johnson rules A(n,d,w) <= floor(n/w * A(n-1,d,w-1)) and A(n,d,w) <= floor(n/(n-w) * A(n-1,d,w)), applied recursively, with A(n,d,w) = 1 when 2w < d, and mirror cells identified (A(n,d,w) = A(n,d,n-w)). The maintainer's ruling on V3R1T4S pull request #350 is that a bound that follows from other bounds by a standard propagation rule is not a separate record, so this is the bar. The panel's novelty skeptic computed 1143 from the page fetched at 2026-10-18T17:54:26Z (HTTP 200, sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349). The orchestrator's earlier fetch at 2026-10-18T17:39:47Z returned the same page hash; its record is in `the-record-we-beat/README.md`, with the commands to recompute the table-implied bound.

The certificate JSON's own bookkeeping fields (for example `table_upper_bound` and `table_cell_as_printed`) are the author's notes, not part of the claim, and may be stale. The checker uses only the dual vector `y`.

## Not claimed

- No code and no lower bound: nothing is claimed about how many words a code can have, only that no code can have more than 837.
- Nothing about n up to 28: the semidefinite-programming (Schrijver-type) tables there are not touched and not compared.
- The table-implied bound is a reading adopted for this comparison (see above); the live cell itself prints no upper bound, so the table has no printed number for this claim to beat.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here. A bound in an unpublished or paywalled source cannot be excluded.

## Credits

- **Andries E. Brouwer**, *Bounds for binary constant weight codes* (the table): https://aeb.win.tue.nl/codes/Andw.html
- **Philippe Delsarte**, the linear programming bound for association schemes: *An algebraic approach to the association schemes of coding theory*, Philips Research Reports Supplements 10 (1973).
- **Selmer M. Johnson**, the Johnson bound: *A new upper bound for error-correcting codes*, IRE Transactions on Information Theory 8 (1962), 203-207.
- **V3R1T4S repository** (https://github.com/elder-plinius/V3R1T4S): its merged bounds were used as inputs to the table-implied bound, and its maintainer's ruling on pull request #350 sets the bar.
- Contributor credit: `calgulbenkian` (search agent: Gemini "Argon").
