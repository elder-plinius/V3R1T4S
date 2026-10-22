context: Claude Code subagent, fresh context [claude-sonnet-5-5]
ROLE: novelty

Cell: sc-30-62

## Sources fetched (once; plain requests)
All requests: curl -A 'V3R1T4S-research (honest client; curl)', no retries. The log is not shipped in this package.
- https://spherical-codes.org/plain  2026-10-18T17:50:10Z  HTTP 200  sha256 8655466f3692fa9197809db2b6fb7ca4f022b605c08b0fa76d78138915e93f35 (identical to the claim's own fetch of 17:39:49Z, so the table had not changed)
- https://spherical-codes.org/  2026-10-18T17:50:11Z  HTTP 200  sha256 ad3039078a704fe0745f447d29e407554fe3b028fdf8017c617d0c7a80618190 (identical to the claim's own fetch of 17:39:51Z)
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md  2026-10-18T17:50:14Z  HTTP 200  sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 : no line mentions spherical codes or Cohn.
- https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 pages 1 to 5, all HTTP 200 (17:50:14Z to 17:50:22Z; 415 pull requests, numbers up to 425). I read every title and the body of every PR on this target.
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns  17:50:23Z  HTTP 200 : no spherical-codes folder (folders include thomson-problem-live-tables, packomania-*, bigger-codes, etc.), so no merged known value for this target.
- arXiv export API (https first; the plain http URL answered 301 with an empty body, recorded in the log): 3 searches (spherical code newest 30; Vahteristo; Tammes / kissing configuration / minimal angle) plus id_list 2610.19988, all HTTP 200, 17:50:28Z to 17:50:31Z.
Competing PRs on this target: #364 (psmoros, open) is for (6,526) only; #231 (psmoros, closed, replaced by #364) the same cell; #399 (DmitrL-dev, open) is a bank-status note that counts rows (it says the index now has 16,448 rows, 'needs more optimization' fell from 11,996 to 5,222, 4,160 rows cite Vahteristo, 3,541 cite Ozgen) and carries no coordinates. No open or merged PR names this package's cell or rows.
Literature: arXiv:2610.19988 (Vahteristo, 2026-10-14, 'New spherical codes by tuning an annealing solver': 29,670 instances N up to 1024, D 3..32, improves 4,577 instances; code https://github.com/ilmari99/Spherical-code-solver, data https://doi.org/10.5281/zenodo.23270586, named in the arXiv comment field). Other hits (arXiv:2609.21591 kissing numbers in dimensions 25 to 31, arXiv:2609.12640, arXiv:2602.10233 ImprovEvolve, arXiv:2510.23609 almost orthogonal vectors survey) concern kissing configurations or other methods; none states a cosine for the cell or rows of this package in its abstract.
unresolved: the Zenodo data set and the GitHub repository of arXiv:2610.19988 were not fetched (very large; outside the one-fetch budget). They could in principle hold an unposted code for a cell below. The table's own rows are the maintained record of what was accepted, and for the cells below the table already postdates that paper (the live table cites it, 4,160 rows). Residual risk is low but not zero.

## Cell values read
- (d=30, N=62): live /plain 0.031273236170; claimed c* (own float64 recompute) 0.031273183364; gain 5.281e-08; index row text: 'o, New spherical codes by tuning an annealing solver , preprint, 2026, arXiv: 2610.19988 .'; star mark: no; passes margin 1e-10: yes

Comparability: the row has no star mark and no 'needs more optimization' text. The reference cell is 'o, New spherical codes by tuning an annealing solver , preprint, 2026, arXiv: 2610.19988 .'. I also fetched the posted code file once (17:51:07Z to 17:51:10Z, HTTP 200) and recomputed its cosine: it matches /plain to 12 decimals (so the table value is the posted code's value, not an older number).
Verdict: the claimed code strictly beats the live table value by the gain above (far more than 1e-10); no open or merged PR, trophy entry or abstract found gives a value for this cell; unresolved caveat above.

novelty: strictly beats the live table at fetch time
pass: true
