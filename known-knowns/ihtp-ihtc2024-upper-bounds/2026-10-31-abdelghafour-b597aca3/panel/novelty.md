# Novelty check: IHTC-2024 instance i16 (claimed cost 10054)

context: subagent (Claude Code Agent tool, fresh context)
role: NOVELTY skeptic. Inputs: only the claim folder (CLAIM.md, i16.json, sol_i16.json, published_sol_i16.json, IHTP_Validator.cc, json.hpp, ihtp_table.html), plus the public web and GitHub.

## 1. Status fetch (one plain fetch, no retries)
- Command: `curl -sS -A 'V3R1T4S-research-agent (+https://github.com/elder-plinius/V3R1T4S)' -w '%{http_code}' https://ihtc2024.github.io/ihtp/index.html`
- URL: https://ihtc2024.github.io/ihtp/index.html
- Fetch time (date -u): 2026-10-31T00:20:56Z
- HTTP status: 200 (not blocked)
- Body sha256: 2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363. This matches the scout snapshot claim/ihtp_table.html byte for byte.
- Listed value for i16 is **10139** (row `<td>i16</td><td class="text-right">10139</td>`, solution sol_i16.json). The page says the bounds come from IHTC-2024 participants "as well as other researchers".
- History of ihtc2024/ihtc2024.github.io ihtp/index.html: i16 was 10139 in every revision (7056e1d9 on 2025-06-30, 33462aaf on 2026-03-03, cbe61b89 on 2026-08-25, fbab27b5 and c078cf57 on 2026-10-23).

## 2. Sources checked for any i16 value at or below 10054
| Source | i16 value found | At or below 10054? |
|---|---|---|
| Organisers' UB table (live, above) | 10139 | no |
| elder-plinius/V3R1T4S PRs: `gh pr list --state all --limit 2000` gave 828 PRs. Title or body hits for i16/IHTP/IHTC: #358, #359, #416, #431, #786-#790, #794-#798 (instances i19, i23, i26, i27, m09, m21, m24, m26-m30). `gh search prs` for "i16" and "10054" returned nothing. | none for i16 | no |
| V3R1T4S TROPHY_CASE.md: no IHTP/IHTC/i16 entries. known-knowns/: no IHTP folder. known-unknowns/optimization-benchmarks/ihtp-ihtc2024-upper-bounds.md has no i16 value. | none | no |
| arXiv 2511.04685v2, Guericke, van der Hulst, Karimpour, Schrader, Walter (Team Twente), Table 5 | BKS 10139 (cited from the website). Own runs 10527 (10 min) and 10568 (1 h). LB 8678. | no |
| arXiv 2610.00044v1, Gippini Requeijo (Sep 2026), new UBs for i02, i05, m01, m03, m04 only (Zenodo 10.5281/zenodo.22061899) | none for i16 | no |
| ORDAL special issue on the IHTP (sciencedirect special-issue 322179) | page returned HTTP 403. I covered it through its papers' code: Gioia et al. (ORDAL 2026) repo DanieleGioia/HealthcarePredictiveTimetabling, i16 solutions validated at 12488 to 16967. | no |
| SSRN 5768118 (Ciccarelli, Di Biase, Furini, two-phase matheuristic) | page returned HTTP 403. Web search found no i16 value. | not found |
| Ceschia et al. competition overview, supporting repo cristianbelfiore/ihtc | only plots, no i16 cost at or below 10139 | no |
| GitHub competitor repos, each solution re-validated with the claim's IHTP_Validator: Arthod/ihtc2024-imada-submission 10983; pchtsp/ihtc2024 15165; emfrea/ihtc2024-evolved-solvers-main 11789 best feasible (CSV best 10755); ahmedelhefnawy21/ihtp-matheuristic 11485 (its reference copy 10139); davidvanbulck/IHTC2024_Multi_Neighborhood_Hybrid (COR 2026), Echtzeitsysteme ihtp-paper-2025/2026-resources, Stiren22, t8qmwk6am3h, jkinyi-gite, davidgit0001: no i16 cost found. None of these repos has release assets. | best known after the table is 10139 | no |
| `gh search code sol_i16`: only the organisers' pages | none | no |

The lowest published i16 cost I found anywhere is **10139** (organisers' table, 2025-06-30 to now). Nothing at or below 10054 was found.

## 3. Seed comparison (claim/published_sol_i16.json vs claim/sol_i16.json)
- I compiled the claim's validator (`g++ -O2 -std=c++17`) and ran it. The published seed gives 0 violations and cost 10139. The claimed sol_i16.json gives **0 violations and cost 10054**, which is 85 less (-0.84%).
- The claim names its seed: the organisers' published i16 solution, improved by simulated annealing.
- Differences between the two files:
  - The same 146 patients are scheduled, with the same admission days (0 changed).
  - 73 patients changed room and 81 changed operating theatre (117 of 146 changed at least one of the two).
  - Nurse room-shift assignments differ by 942 pairs (symmetric difference), against 714 pairs in the seed.
  - sol_i16.json lists 154 patient entries against 146 in the seed. The extra 8 are unscheduled ("none") entries, and the validator accepts the file.
- Trivial-edit test:
  - Relabelling and symmetry keep the cost the same, so they cannot produce the 85-point drop.
  - Deletion or restriction does not apply: the same patients are admitted.
  - There is no continuous "numerical polish" in this integer assignment problem.
  - The change is a large re-optimisation of room, theatre and nurse assignments. It strictly beats what the trivial edits of the seed give, which is at best 10139.
  - So the result is more than a trivial edit.

## Verdict
10054 < 10139, the lowest value found in the live table, its history, the V3R1T4S PRs, TROPHY_CASE.md, known-knowns, the literature and the competitor code. That is a strict improvement, not a tie. The two sources I could not open (the ORDAL special-issue page and SSRN 5768118, both HTTP 403) were covered indirectly: one through its code and one through search, and neither showed an i16 value at or below 10139.

pass: true
