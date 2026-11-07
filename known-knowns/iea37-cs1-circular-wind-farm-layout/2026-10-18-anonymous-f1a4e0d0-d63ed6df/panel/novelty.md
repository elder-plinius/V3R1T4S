# Novelty verdict: IEA Wind Task 37 case study 1, 64 turbines (iea37-cs1-opt64)

Claimed value: 1539447.11737 MWh for object/iea37-v3r1t4s-opt64.yaml (sha256 d63ed6df76fcbf03297cdb171acda406f597bfc959b1610711dc0d68dd93c851, re-hashed by me, matches).

## 1. Status source: live fetches (one honest request each, User-Agent "V3R1T4S-research-agent", no retries)

| URL | UTC time | HTTP |
|---|---|---|
| https://api.github.com/repositories/283947278/git/trees/master?recursive=1 | 2026-10-18T03:20:29Z | 200 |
| https://raw.githubusercontent.com/IEAWindSystems/iea37-wflo-casestudies/master/cs1-2/iea37-cs1-results/iea37-par{1..12}-opt64.yaml (12 requests, one per file) | 2026-10-18T03:20:34Z to 03:20:39Z | 200 (all 12) |
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-18T03:22:03Z | 200 |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-18T03:22:03Z | 200 |

- The live tree is not truncated. It has sha256 c3a54a267ffb10a994f309ac609e4e1e572428e554739fa9057b80d92aca7bf3, the same as the scout's copy in table/gh_tree.json. So the official results folder has not changed since the scout fetched it.
- The live folder contains exactly 12 opt64 files (par1 to par12). Each live file is byte-identical to the scout's copy in table/iea37-cs1-results/.

## 2. Re-scoring with the official evaluator (claim/evaluator/iea37-aepcalc.py, unmodified, run from inside claim/evaluator)

| file (live) | AEP (MWh) |
|---|---|
| par12 | 1526474.80248 (best in folder; posted layout is about 4 mm outside the 3000 m boundary, per the claim) |
| par4 (SNOPT+WEC, the published winner) | 1513311.19361 |
| par2 | 1506388.41513 |
| par11 | 1484287.26071 |
| par10 | 1480850.97590 |
| par1 | 1476689.66268 |
| par3 | 1455075.60842 |
| par8 | 1445967.37723 |
| par9 | 1422268.71443 |
| par6 | 1364943.00774 |
| par5 | 1336164.54980 |
| par7 | 1332883.43284 |
| **claimed object** | **1539447.11737** |

- Nothing in the live folder is at or above the claimed value. The best known value is par12 at 1526474.80248. The claimed value beats it by 12972.3 MWh (+0.85 %) and beats par4 by +1.73 %.
- As a side check, claim/evaluator/check_constraints.py reports the claimed layout as FEASIBLE: 64 turbines, max radius 2999.999999 m (limit 3000), min spacing 567.69 m (limit 260). Constraint validity is not my panel's job; I only note it.

## 3. Literature, last 24 months emphasised, plus 2019-2024 follow-ups

| Source | What it reports | Comparable? |
|---|---|---|
| Baker et al. 2019, AIAA 2019-0540, https://docs.nrel.gov/docs/fy19osti/72935.pdf (table/nrel72935.pdf) | Table 4: best 64-turbine value is 1513.31 GWh (SNOPT+WEC). | Yes. Below the claim. |
| Pérez-Rúa & Cutululis, "A neighborhood search integer programming approach...", Wind Energ. Sci. 8, 1453 (2023), https://wes.copernicus.org/articles/8/1453/2023/ (table/wes-8-1453-2023.pdf) | Table 2, case III (64 turbines): SNOPT+WEC is 0.85 % above their method, so their result is about 1500 GWh. | Yes (same benchmark). Below the claim. |
| Quaeghebeur et al., "Wind farm layout optimization using pseudo-gradients", Wind Energ. Sci. 6, 815 (2021), https://doi.org/10.5194/wes-6-815-2021 (table/quaeghebeur2021.pdf) | Results for the 36/64-turbine sites are given only as wake-loss percentages (Fig. 13). Described as "decent performance" and not claimed to beat the participants. | Yes. Not higher. |
| Valotta Rodrigues et al., Wind Energ. Sci. 9, 321 (2024), https://wes.copernicus.org/articles/9/321/2024/ (table/wes-9-321-2024.pdf) | Multi-start and SMAST on an IEA37 64-turbine site, but with 360 wind directions. The paper says its absolute AEPs are not consistent with the original IEA 37. | No (360 directions). |
| arXiv 2212.00742 (DPCRO-SL), https://arxiv.org/pdf/2212.00742 (table/arxiv2212.00742.pdf) | IEA37 CS1 with 16 turbines (1300 m) only. | No 64-turbine value. |
| Thomas et al., "A comparison of eight optimization methods...", Wind Energ. Sci. 8, 865 (2023), https://wes.copernicus.org/articles/8/865/2023/ | IEA37 case study 3 (Borssele, 81 turbines). | No (different case). |
| "Offshore wind farm layout optimization with alignment constraints", Wind Energ. Sci. 10, 1611 (2025), https://wes.copernicus.org/articles/10/1611/2025/ | Borssele (CS3/4) benchmark, +0.41 % over its own baseline. | No (different case). |
| Thomas & Ning, WEC method, https://scholarsarchive.byu.edu/facpub/2117 | Cases with 16 and 38 turbines. | No 64-turbine CS1 value. |
| arXiv 2502.00476, arXiv 2509.07868, arXiv 2309.01387, arXiv 2203.13525 (topology optimization) | No IEA37 CS1 64-turbine AEP reported (other sites, or a 3.4 MW turbine with a different setup). | No. |
| Energies 18(11) 2999 (2025), https://ideas.repec.org/a/gam/jeners/v18y2025i11p2999-d1672948.html | LES wake-expansion study, no layout AEP. | No. |
| DTU TopFarm/PyWake IEA37 examples, https://topfarm.pages.windenergy.dtu.dk/PyWake/notebooks/Optimization.html | Tooling for the IEA37 problem, no record value posted. | Not a record. |

Searches I ran (web, standard and extended):
- general IEA37 CS1 64-turbine AEP improvements
- 2025/2026 arXiv new-best searches
- exact-number searches for "1526474", "1526.47" and "1539447" (no hits outside unrelated American Electric Power finance pages)
- WEC/continuation follow-ups
- integer programming, pseudo-gradient and metaheuristic searches
- GitHub opt64 YAML layouts and theses

I also tried one benchmark-aggregator page, https://rsi-bench.duckdns.org/tasks/windfarm_wake_layout.html, but it failed on DNS (ENOTFOUND), so I could not check its content. I found no comparable published 64-turbine CS1 value above 1526474.8 MWh, let alone 1539447 MWh.

Limits: web search can miss theses, paywalled papers and unindexed GitHub repos. A comparable unpublished higher layout cannot be ruled out absolutely.

## 4. This project's trophy case and open pull requests

- TROPHY_CASE.md (89 non-empty lines) has no entry matching iea, wind, turbine, wflo, aep, energy or clean-energy.
- The repo has 66 open PRs. I searched each PR's title, body and branch name for iea37, IEA Wind, turbine, wflo, clean-energy and wake, and found no matches. So there is no duplicate or competing IEA37 claim.

## Verdict

The claimed value, 1539447.11737 MWh, is strictly above everything comparable I could find:
- the best value in the live official folder, 1526474.80248 (par12)
- the published winner, 1513311.19361 (SNOPT+WEC)
- every comparable literature value, the best being about 1500 GWh (Pérez-Rúa 2023)
- no entry in this repo's trophy case or open PRs

It is not a tie. Papers using modified setups (360 directions, other cases) were excluded as not comparable. Novelty is confirmed to the extent that public sources can be searched.

context: subagent (Claude Code Agent tool, fresh context)

---
Note added 2026-11-07 (UTC) at the maintainer's request on V3R1T4S PR #938, after the gate.
The text above is unchanged, and so is the closing pass line, which was moved below this note because the kit
reads it as the file's last line. Its paths are relative to the run folder runs/2026-10-18-0107/, not to this package.
In this package, claim/object/iea37-v3r1t4s-opt64.yaml and claim/object/layout64.json are object/iea37-v3r1t4s-opt64.yaml
and object/layout64.json. These are not in this package, by design: claim/evaluator/ (the official IEA37 files,
including iea37-aepcalc.py; RUN_IT_YOURSELF.md says where to download them) and the run's check_constraints.py (this
package's own checker is verify-it-yourself/check_layout.py); claim/table/ (the results-folder snapshot, whose URL,
fetch times and sha256 are in the-record-we-beat/record.md); claim/scratch/; and the run's CLAIM.md and REPRODUCE.md
(README.md and RUN_IT_YOURSELF.md cover the same ground).

pass: true
