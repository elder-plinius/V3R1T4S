# NOVELTY verdict: IEA37 case study 1, 16-turbine layout (target clean-energy-records / iea37-cs1-opt16)

context: subagent (Claude Code Agent tool, fresh context, given only claim/)

## Verdict
The claim passes. As of 2026-10-20 02:24 UTC the official results table has not changed since the scout's snapshot. The claimed layout re-scores to **424131.9503 MWh** with the unmodified official evaluator. That is strictly above every value I could find for this scenario: +2570.05 MWh (+0.61 %) over participant 12's infeasible 421561.89715, and +4196.16 MWh over the best feasible literature value, 419935.7905 (DPCRO-SL). It is not a tie. Neither TROPHY_CASE.md nor the open PRs contain this scenario.

## Status source fetch (one fetch each, plain curl, `-A "V3R1T4S-research-agent"`, no retries)
| UTC time (`date -u`) | URL | HTTP |
|---|---|---|
| Tue Oct 20 02:24:14 UTC 2026 | https://api.github.com/repositories/283947278/git/trees/master?recursive=1 | 200 |
| Tue Oct 20 02:24:29 UTC 2026 | https://raw.githubusercontent.com/IEAWindSystems/iea37-wflo-casestudies/master/cs1-2/iea37-cs1-results/iea37-par12-opt16.yaml | 200 |
| Tue Oct 20 02:24:29 UTC 2026 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 200 |
| Tue Oct 20 02:24:30 UTC 2026 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 200 |
| Tue Oct 20 02:24:46 UTC 2026 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:pr+is:open+iea37+OR+turbine+OR+wflo+OR+%22wind+farm%22 | 200 |

None of the fetches was blocked or hit a challenge page.

- **Tree:** the live tree sha is `267f6e5d2906400b2ee0a8ff533da7ebcc4bb47a` (`truncated False`). It is identical to the scout's table/gh_tree.json, so nothing has been added or changed since. `cs1-2/iea37-cs1-results/` still has exactly 12 `iea37-par<k>-opt16.yaml` files (par1 to par12).
- **Table files:** the `git hash-object` of every file in table/iea37-cs1-results/ matches the live blob sha. For example, par12 is `283959cbd7c1916fac9ee87e7715ae8fef4add18`, and the freshly fetched raw par12 hashes to the same sha.
- **Evaluator files:** evaluator/iea37-aepcalc.py (`097d884c…`), iea37-windrose.yaml (`0f2d8251…`) and iea37-335mw.yaml (`4d262f7e…`) match the live `cs1-2/` blobs, so the evaluator really is the unmodified official one.

## Re-score (official evaluator/iea37-aepcalc.py and the claim's evaluator/check_constraints.py)
- **Claim:** object/iea37-v3r1t4s-opt16.yaml has sha256 `4bd4f7cf…98f4c`, which matches the claim.
  - Last line of output: `424131.9503`.
  - Constraints: `max_radius 1299.9999990000172 … min_spacing 576.2929952098602` → `FEASIBLE`.
- **Table entries, re-scored by me:**
  - par12 `421561.89715`, max_radius `1303.5181552724919` (INFEASIBLE).
  - par4 `418924.40636`, max_radius `1300.0000000000039` (INFEASIBLE).
  - par5 `414141.29376` (best FEASIBLE table entry).
  - All the others are lower (par8 412251.19, par1 411182.22, par11 409850.33, par2 409689.44, par10 408360.78, par3 402318.76, par7 392587.86, par6 388758.36, par9 388342.70).
- **Bundled papers:** a text grep of table/arxiv2212.00742.pdf finds `419935.7905`, its best 16-turbine AEP. A grep of table/nrel72935.pdf finds `418924.4064` as its top 16-turbine value. Neither reaches 424131.95.

## Literature search (last 24 months)
I ran web searches across arXiv, Wind Energy Science and general scholarly results.
- **Not comparable, or no 16-turbine value:**
  - WES 9/321/2024 uses 360 directions and says explicitly that its numbers are not comparable.
  - WES 10/1611/2025 and wes-2024-118 (alignment constraints) use the Borssele 81+ turbine case.
  - arXiv 2509.07868 uses a different site.
  - The PyWake/TOPFARM tutorial uses a simplified 12-direction version.
  - The Hexaly WFLOP template uses the IEA37 instances but reports no AEP.
- **Could not check:** an "rsi-bench" task page (rsi-bench.duckdns.org) did not resolve (ENOTFOUND). I could not see what it contains.
- **Result:** I found no AEP ≥ 424131.9503 MWh, and no value above 421561.89715, for the official 16-bin, official-evaluator, 16-turbine, 1300 m scenario. A web search cannot prove that no such value exists anywhere, so this is "not found", not "proven absent".

## Trophy case and open PRs
- **TROPHY_CASE.md (31235 bytes):** a case-insensitive grep for `iea|wind|turbine|wflo|aep|task 37` gives 0 hits. Its families are graphs, codes, matrix multiplication, Lehmer, VNN-COMP and RobustBench, so this scenario is not already claimed.
- **Open PR list:** 100 open PRs, numbers #476 to #576. Only #567 (constant-weight codes) and #534 (SAW connective constant) matched my keyword regex, and neither is about this scenario. The list is capped at 100 per page and I did not fetch a second page.
- **Repo-wide open-PR search:** `total 0` for iea37/turbine/wflo/"wind farm".

## Is it distinct from participant 12's layout?
- **Nearest-neighbour distances from each claim turbine to a par12 turbine:** 3.8, 15.6, 17.2, 18.0, 21.3, 25.3, 30.9, 35.4, 36.7, 37.2, 37.9, 38.1, 39.8, 51.8, **568.6, 569.9** m. So 14 of 16 lie within 52 m, as disclosed.
- **One-to-one (optimal assignment) displacements:** the largest three are 547.6, 571.5 and **823.2** m, so only 13 turbines stay within 52 m under that matching.
- **Against the frozen polish rule:** the maximum displacement is far above 50 m, so by the claim's own rule this is not a polish of par12. The claim also states it is more than 50 m from the DPCRO-SL layout, which I did not recompute.

My judgement: it is clearly derived from par12's basin, with most turbines nudged back so they fit inside the boundary. But two turbines are relocated by about 570 m, which makes it a distinct layout. It satisfies the constraints that par12 violates, and its score of 424131.9503 MWh beats par12 and every other known value by 2570 MWh. That is a strict beat, not a tie. It should be credited as built on participant 12's layout.

## Caveats
- The literature check is a best-effort web search and could miss non-indexed work.
- I fetched only one page of the open-PR list, though the repo-wide search covers the rest.
- Feasibility rests on a 1e-6 m margin inside the boundary (max_radius 1299.999999 m), checked in float64 with no tolerance.
- Whether the AEP itself is correct is outside the novelty remit beyond my re-score.

pass: true
