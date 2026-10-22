# Quartic (z = 4) Feigenbaum constants alpha_4 and delta_4 to about 1085 agreeing decimals

## What

The coefficient file defines a quartic (z=4) Feigenbaum fixed point and its dominant eigenfunction satisfying the defining equations to about 1e-1092 and 1e-1100 at 31 points, with alpha_4 = -1.6903029714... and delta_4 = 7.2846862170... agreeing between 1070 and 1100 coefficients to 1085 and 1084 decimals (not proven correct to that many digits), exceeding the 49 digits of A195102 and the 331 and 325 proven digits of Thurlby.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about one to two minutes (decimal arithmetic at 1300 digits).
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| OEIS A195102 (decimal expansion of the reduction parameter for the biquadratic solution of the Feigenbaum-Cvitanovic equation) | data field | 49 digits of alpha_4 = 1.6903029714052448533437801503241613482282780597095619666824... (leading digits) | https://oeis.org/search?q=id:A195102&fmt=json | 2026-10-19T05:37:36Z (HTTP 200, novelty skeptic; triage fetch 04:47:07Z, same sha256) |
| Thurlby, PhD thesis, University of Portsmouth, 2021, Table 4.6 (page 86) | alpha_4 and delta_4 | 331 digits of alpha_4 and 325 digits of delta_4, proven correct (truncation degree N = 640) | https://pure.port.ac.uk/ws/portalfiles/portal/43264172/Thesis_Final_Judi_Thurlby_September_2021.pdf | 2026-10-19T04:50:22Z (HTTP 200, triage fetch; not refetched by the panel) |
| OEIS search for further biquadratic Feigenbaum sequences | delta_4 | no sequence for delta_4; the only hit is A195102 | https://oeis.org/search?q=Feigenbaum+biquadratic&fmt=json | 2026-10-19T05:39:34Z (HTTP 200) |
| arXiv 2409.20457 (validated Chebyshev enclosures of renormalization fixed points) | quartic eigenvalue | about 41 digits (7.28468621707334336430893056799555306947804 plus or minus 1e-41), in the novelty report's reading; it agrees with the first 41 digits here | https://arxiv.org/pdf/2409.20457v2 | 2026-10-19T05:39:13Z (HTTP 200) |
| V3R1T4S `TROPHY_CASE.md`, known-knowns, pull requests | z = 4 Feigenbaum | no entry; no folder; no pull request mentions Feigenbaum | https://github.com/elder-plinius/V3R1T4S | 2026-10-19T05:37:22Z (HTTP 200) |

This package: alpha_4 = -1.6903029714052448533437801503241613482282780597095619666824... and delta_4 = 7.2846862170733433643089305679955530694780466197997906590721..., the two resolutions (1070 and 1100 coefficients) agreeing to 1085 decimals (alpha_4) and 1084 decimals (delta_4) as measured by the panel (the contributor claimed 1085 and 1082). Snapshot metadata with HTTP status and page sha256: `the-record-we-beat/README.md`. The panel's novelty report is `panel/novelty.md`.

## Not claimed

- The digits are not proven. The count is the agreement between two resolutions of the same method, together with residuals of the defining equations at 31 points in decimal arithmetic at 1300 digits (about 1e-1092 and 1e-1100). It is a numerical result, not a rigorous error bound; the step from small residuals to a number of correct decimals is an argument, not a theorem. Thurlby's 331 and 325 digits are proven; ours are not, so the comparison is of agreeing digits against proven digits.
- Partial win p2 only (the quartic constants to at least 1000 decimals with two resolutions agreeing). The target's main criterion, more than 10,022 decimals of the quadratic Feigenbaum constants (Molteni 2016), is not claimed, and nothing is claimed for the accumulation points of the logistic or quadratic maps (the p1 cell).
- The checker verifies that the second function is an eigenfunction of the linearized renormalization operator with eigenvalue delta_4. That delta_4 is the dominant (unstable) eigenvalue rests on the panel's double-precision spectrum of the operator built from the file (leading eigenvalue 7.2847, the next ones 1, 0.29 and 0.26 in magnitude) and on agreement with Thurlby's digits; it is not proven here.
- The defining equations were written by the builder from the standard setting. They reproduce the 49 digits of OEIS A195102 and all printed digits of Thurlby's table; the panel recovered the file's convention independently and checked the fixed-point equation at 60 digits.
- The sign convention: with g(x) = alpha g(g(x / alpha)), alpha_4 is negative (-1.6903...); the object prints the magnitude, as OEIS does.
- Literature: only OEIS, Thurlby's thesis and an arXiv search were looked at. The older work on the quartic case that OEIS cites was not read; nothing found carries more than about 330 digits. A newer source could exist.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Judi Thurlby**, PhD thesis, University of Portsmouth, 2021, Table 4.6 (page 86), https://pure.port.ac.uk/ws/portalfiles/portal/43264172/Thesis_Final_Judi_Thurlby_September_2021.pdf: the proven digits of alpha_4 and delta_4 compared against; the checker compares every printed digit of the table with its own computation.
- **OEIS A195102**, https://oeis.org/A195102: the 49-digit expansion compared against (the entry's contributors are not named here).
- **Andrea Molteni**, arXiv:1602.02357 (2016), https://arxiv.org/abs/1602.02357: according to the target's text, the Chebyshev collocation method with a Krylov eigensolver for the quadratic Feigenbaum fixed point; the same family of method (Chebyshev collocation of the fixed point and its eigenfunction) is used here for z = 4. The quadratic records are not claimed.
- arXiv 2409.20457 (validated enclosures of renormalization fixed points), https://arxiv.org/abs/2409.20457: compared against (41 digits for the quartic eigenvalue, in the novelty report's reading).
- The Feigenbaum-Cvitanovic fixed-point equation, whose name OEIS uses.
- Software the search code uses: GNU MPFR and GMP (https://www.mpfr.org/), gmpy2, numpy and scipy.
- Contributor credit: `calgulbenkian`. The solver was written by an AI search agent (Gemini) working for the contributor.
