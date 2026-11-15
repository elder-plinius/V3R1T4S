context: Claude Code subagent, fresh context [Sonnet 5.5 (claude-sonnet-5-5)]

# Novelty skeptic report: (7, 365), c* = 0.67046703514181086524

[Edited 2026-11-09 at the maintainer's request on the pull request: mentions of files that are not in this package were removed, the note about a truncated pull-request listing was dropped, and the arXiv responses' sha256 values are given in full. The checks, numbers and verdict are unchanged.]

All fetches: curl, User-Agent 'V3R1T4S-research (honest client; curl)', one GET each.

## Fetches (UTC time, HTTP, sha256, finding)
- https://spherical-codes.org/plain, 2026-11-08T14:58:11Z, 200, 9f26579e6f0842bb92f62f790943000afd787a1b2a0145476997b9620abbc493. Row `7,365,0.670467238587` (line 4176). Same as the saved 2026-11-03 value; no movement.
- https://spherical-codes.org/, 2026-11-08T14:58:11Z, 200, 0f9353613fea9193f1135cba56c09c0a3c9069d95b5578c5afb7466de31091ff. Row href="/data/7/365": `<a href="/data/7/365">365</a></td>` then `<td>0.670467238587</td>`. No &ast; follows the link. Reference cell does not contain "needs more optimization". Reference text: "Antoine Jay, 2026, using the program of A. Jay, M. Poberznik, M. Brut, A. Hemeryck, L.-H. Hoang, M. Gunde, N. Salles, G. Cruchon, and M. Roux, Equidistribution of points on the hypersphere including symmetries, preprint, 2026, doi:10.2139/ssrn.6427919."
- https://spherical-codes.org/data/7/365, 2026-11-08T14:58:15Z, 200, 242d7de97c8ce395b056a697cdcbde1452be5abde2ce14b4557f561eed42ad72. 365 vectors x 7 coordinates. mpmath (dps 50, normalised, all pairs, venv python -I): max inner product 0.670467238586798986004115292929, which reproduces the table's 0.670467238587 (parser sanity OK).
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, 2026-11-08T14:58:15Z, 200, 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113. 89 lines; no spherical-code, Cohn or (7,365) entry.
- gh pr list (open, limit 600): 431 open PRs. Spherical-codes PRs: #1009 (29,727), #807 (6,256), #626 (25,650), and #436 = this claim (d=7 N=365, 0.670467035142). No other (7,365) PR.
- gh api known-knowns/spherical-codes-cohn-table: merged folder exists with 5 entries (d29N60, d30N62, d27N56, (25,651), d31N64). Their INDEX.csv files hold no (7,365) value.
- arXiv API (the http URLs returned 301; I followed to https, once each): https://export.arxiv.org/api/query?search_query=all:"spherical code", 2026-11-08T14:59:15Z, 200, a975690a81bf72526b6e28a2d485a88a45ce7e62f67ba72265590490b36ef0d8; all:Tammes, 14:59:20Z, 200, b01d03707f51af7b8431cb8083dd671ee776a1d8ce551018f87c2696319f1cdc; id_list=2610.19988, 14:59:25Z, 200, 74f489a359720d49aad150748a006f3788ac6bdfca953718471fb8225f29bd5e
  - Spherical-code hits since 2024-11 reviewed by title/abstract: none other than 2610.19988 is a numerical table of codes (others are bounds, designs, kissing numbers, ML). Tammes hits are mostly unrelated physics; 2411.16038 (Tammes in R^n, LP method) is a bounds paper.
  - arXiv:2610.19988 (Vahteristo, "New spherical codes by tuning an annealing solver", 2026-10-14): the abstract does not name dimension 7 or N = 365 specifically, but it covers every N <= 1024, 3 <= D <= 32, N > 2D, which includes (7,365), and claims 4,577 improved instances. Its per-instance value for (7,365) is not given in the abstract and I did not read the code release. The live table cites Vahteristo in about 2,856 index lines, yet credits (7,365) to Antoine Jay, so the table's value (0.670467238587) is the best the table maintainers hold after ingesting it. Residual risk: if the paper's own code file for (7,365) is below c*, the row is superseded; not checkable from the abstract.

## Comparison
- Live cosine 0.670467238587 minus c* 0.67046703514181086524 = 2.03445e-7, which is at least 1e-10 (margin about 2000x the bar). Row has neither the star nor the label.
- Dim-7 rows with N > 365 (live /plain): 366 0.670923693486, 367 0.671526578995, 368 0.671586876700, 369 0.671829787739, 370 0.672135805879, 371 0.672555027738, 372 0.673529089044, and the script flagged no N > 365 row with cosine <= c* + 1e-9 (monotone upward). No subsuming code.
- Tie check: nothing known (table, PRs, merged folder, TROPHY_CASE, arXiv abstracts) is equal to or below c*.

## Verdict
The claim stands against everything visible live on 2026-11-08: strictly better by 2.03e-7, unstarred, unlabeled, no larger-N code subsumes it, no competing PR or trophy entry. The only unverified item is Vahteristo's own (7,365) number, which the table (which ingests that work) does not show as lower.

pass: true
