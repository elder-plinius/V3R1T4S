# Novelty panel — run 2026-10-14-0717 (claims D–I)
context: subagent (executor), fresh
Inputs used: claim/ (D_534 E_548 F_777 G_542 H_743 I_745) only, public web, repo/TROPHY_CASE.md, open PRs on elder-plinius/V3R1T4S and mrxmoex/V3R1T4S.
User-Agent: `V3R1T4S-panel-novelty/1.0 (research verification; single honest fetch)`. Each URL fetched once, no retries. Raw pages + fetch_log.txt in panel/novelty_work_DI/.

## Fetch table (panel re-fetch)

| source | URL | UTC | HTTP | sha256 (prefix) | claim-N cells |
|---|---|---|---|---|---|
| Deeter | https://deetour.net/oppp/thomson/ | 2026-10-14T14:28:41Z | 200 | cf138c88fc00c5e0 | max e.N.txt = 524; no rows for 534/542/548/743/745/777 |
| CCD Thomson | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html | 2026-10-14T14:28:42Z | 200 | 5466173175b10a81 | no rows for claim Ns |
| CCD Thomson2 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html | 2026-10-14T14:28:43Z | 200 | caf24199154912eb | no rows for claim Ns |
| CCD Riesz s=1 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html | 2026-10-14T14:28:44Z | 200 | eeac3235eeba4835 | see per-claim live cells below |
| Wikipedia | https://en.wikipedia.org/wiki/Thomson_problem | 2026-10-14T14:28:46Z | 200 | 039f8984f662f89d | table through N=470; no claim Ns |
| arXiv 2610.08122 | https://arxiv.org/html/2610.08122 | 2026-10-14T14:28:46Z | 200 | 24ff8b310f1a00c9 | Table 2/3 “this work” cells below |

Other sources: web search per N (last ~24 months + older Altschuler/Wales tables); junlilab TP2.html not re-fetched (CCD Thomson2 already covers those Ns: absent). repo TROPHY_CASE.md: no Thomson/Riesz/sphere-energy rows. Open PRs: elder-plinius/V3R1T4S has draft #78 for N=1382 only (not these Ns); mrxmoex/V3R1T4S: zero open PRs. No open PR posts a lower or equal energy for any claim N.

Pass rule: claimed E* strictly below every live/literature value found by ≥ 1e-6 (tie = fail). Certification/basin not assessed here.

## D — N = 534
Claimed E* = 135762.8145401324761574878.
Live Riesz s=1 cell: **135762.9050570** (URL above, fetch 2026-10-14T14:28:44Z).
arXiv 2610.08122: ref 135763.57340729 / this-work 135762.91066161.
Deeter / CCD Thomson / Thomson2 / Wikipedia: no row. Web search: no lower published energy.
Lowest known = 135762.9050570 (live Riesz). Margin = 9.05168675e-02 ≥ 1e-6.
Novelty verdict: **PASS** (strictly beats everything found; not a tie).

## E — N = 548
Claimed E* = 143066.8793744849140468194.
Live Riesz s=1 cell: **143067.0064628** (same fetch).
arXiv this-work: 143067.00646283; ref 143068.03051847.
Other tables: no row. Web search: no lower published energy.
Lowest known = 143067.0064628 (live Riesz). Margin = 1.27088315e-01 ≥ 1e-6.
Novelty verdict: **PASS**.

## F — N = 777
Claimed E* = 289900.778533909713618485.
Live Riesz s=1 cell: **289900.8082430**.
arXiv this-work: **289900.80824298** (slightly below rounded Riesz print); ref 289902.13212320.
Other tables: no row. Web search cites arXiv this-work as best known; none lower than claim.
Lowest known = 289900.80824298 (arXiv this-work). Margin = 2.97090703e-02 ≥ 1e-6.
Novelty verdict: **PASS**.

## G — N = 542
Claimed E* = 139913.0793830909490116457.
Live Riesz s=1 cell: **139913.1454539**.
arXiv this-work: 139913.14545394; ref 139913.59874297.
Altschuler et al. 2005 (cond-mat/0408355): ~139913.69461 (higher).
Other tables: no row. Web search: no lower published energy.
Lowest known = 139913.1454539 (live Riesz). Margin = 6.60708091e-02 ≥ 1e-6.
Novelty verdict: **PASS**.

## H — N = 743
Claimed E* = 264837.5287041150044362828.
Live Riesz s=1 cell: **264837.5858504**.
arXiv this-work: **264837.58585036** (slightly below rounded Riesz print); ref 264837.70097130.
Other tables: no row. Web search: no lower than claim.
Lowest known = 264837.58585036 (arXiv this-work). Margin = 5.71462450e-02 ≥ 1e-6.
Novelty verdict: **PASS**.

## I — N = 745
Claimed E* = 266280.2015165256924341327.
Live Riesz s=1 cell: **266280.2589229**.
arXiv this-work: 266280.25892291; ref 266280.73119190.
Other tables: no row. Web search: no lower published energy.
Lowest known = 266280.2589229 (live Riesz). Margin = 5.74063743e-02 ≥ 1e-6.
Novelty verdict: **PASS**.

## Summary
All six claims (D–I) strictly beat the minimum of live CCD Riesz s=1 and arXiv 2610.08122 (and any other literature hit) by ≫ 1e-6. No competing open PR or TROPHY_CASE entry. Novelty skeptic does not certify energy recomputation or Hessian/basin (other panel roles).

pass: true
