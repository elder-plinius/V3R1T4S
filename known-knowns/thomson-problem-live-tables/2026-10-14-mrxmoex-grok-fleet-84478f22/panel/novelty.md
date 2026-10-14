# Novelty panel — run 2026-10-14-0717
context: subagent (executor), fresh. Inputs used: claim/ only, public web, repo/TROPHY_CASE.md, open PRs on GitHub mrxmoex/V3R1T4S.
User-Agent: "V3R1T4S-panel-novelty/1.0 (research verification; single honest fetch)". Each URL fetched once, no retries. Raw pages + fetch_log.txt are in panel/novelty_work/.

| source | URL | UTC | HTTP | sha256 (prefix) |
|---|---|---|---|---|
| Deeter | https://deetour.net/oppp/thomson/ | 2026-10-14T08:56:42Z | 200 | cf138c88fc00c5e0 |
| CCD Thomson | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html | 2026-10-14T08:56:42Z | 200 | 5466173175b10a81 |
| CCD Thomson2 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html | 2026-10-14T08:56:44Z | 200 | caf24199154912eb |
| CCD Riesz s=1 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html | 2026-10-14T08:56:45Z | 200 | eeac3235eeba4835 |
| Wikipedia | https://en.wikipedia.org/wiki/Thomson_problem | 2026-10-14T08:56:46Z | 200 | 8db2fbfbf9e969b9 (changed vs scout a279d4de…; still no rows 550/1382/3552) |
| arXiv 2610.08122 | https://arxiv.org/html/2610.08122 | 2026-10-14T08:56:47Z | 200 | 24ff8b310f1a00c9 |

Other sources: web search per N (surfaced junlilab.org TP2.html mirror of Thomson2: 550 144126.0927100, 1382 926576.1175606, 3552 6191357.2579633 — none lower); repo TROPHY_CASE.md has no Thomson entries; open PRs on mrxmoex/V3R1T4S: none.

## A — N = 1382
Claimed E* = 926576.0968589705350586982.
Live cells: Riesz s=1 "926576.1030330"; Thomson2 "926576.1175606"; Deeter, CCD Thomson, Wikipedia: no 1382 row. arXiv 2610.08122 Table 4: "1382 926576.11756060 926576.10303295" (this-work value = Riesz cell).
Lowest known = 926576.10303295 (arXiv) ; margin = 6.174e-3 > 1e-6. No search hit, PR or trophy lower or equal.
Novelty verdict: PASS (strictly beats everything found; not a tie). (Certification/basin not assessed by this panelist.)

## B — N = 3552
Live Riesz s=1 cell still shows the unpolished value "6191355.6866585" (= arXiv "6191355.686658503"; claimed polished 6191355.686643545, ~1.5e-5 lower). Thomson2 cell "6191357.2579633". Condition holds: table still unpolished at fetch time; no newer lower value found.

## C — N = 550
Live Thomson2 cell "144126.0927100" (unchanged; junlilab mirror identical). Claimed own-coordinate polished energy 144126.0927999992 → cell is 8.9999e-5 LOWER than its coordinates reach (per claim; not recomputed here). No other source lists 550 lower. Finding still live and not previously reported in sources found.

pass: true
