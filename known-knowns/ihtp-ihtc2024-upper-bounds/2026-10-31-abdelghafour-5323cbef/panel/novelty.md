# NOVELTY skeptic: ihtp-ihtc2024-upper-bounds, cell m19 (claimed 21752)

context: subagent (Claude Code Agent tool, fresh context)
Input: only the folder `panel-staging/m19_novelty/claim/` (CLAIM.md, sol_m19.json, published_sol_m19.json, m19.json, IHTP_Validator.cc, json.hpp, ihtp_table.html).

## 1. Status page (one plain fetch, no retries)
- URL: https://ihtc2024.github.io/ihtp/index.html
- Command: `curl -sS -A 'V3R1T4S-research-agent (+https://github.com/elder-plinius/V3R1T4S)' -w '%{http_code}' <URL>`
- Fetch time (date -u): 2026-10-31T09:45:14Z (finished 09:45:16Z)
- HTTP status: 200 (not blocked)
- Listed m19 value: **21776** (row `<td>m19</td><td class="text-right">21776</td>`, solution link sol_m19.json)
- sha256 of the fetched page: 2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363. This is byte-identical to the scout's claim/ihtp_table.html.
- Table history (GitHub API, ihtc2024/ihtc2024.github.io, ihtp/index.html): m19 was 21790 at cbe61b8905 (2026-08-25) and fbab27b5c2 (2026-10-23 08:48Z). It became 21776 at c078cf5788 (2026-10-23 10:07Z, "updated batch of UB"). That batch updated exactly m05, m10, m15, m17, m18, m19, m20, m21, m23, m24, m26-m30, the same 15 m-instances that V3R1T4S PR #431 says it improved. So 21776 almost certainly already includes that contributor's m19 result.
- The seed claim/published_sol_m19.json has sha256 a096c6f0...519c. This matches the organisers' current assets/files/solutions/hidden/IHTP/sol_m19.json.

## 2. Sources checked for an m19 cost <= 21752
| Source | m19 value found |
|---|---|
| Organisers' live table (above) | 21776 |
| arXiv 2511.04685v2 (Guericke, Walter et al., v2 2026-05-01), Table 5 | LB 19761; BKS 21790 (website, retrieved 2025-10-01); own runs 23298 (10 min), 22395 (1 h); Table 7: 23298 / 22707 |
| arXiv 2610.00044v1 (2026-09-03, nurse-layer exact reoptimization) | no m19 (improves only i02, i05, m01, m03, m04) |
| arXiv API search "healthcare timetabling" (sorted by date) | only the two papers above |
| Web search: 2025-2026 ORDAL special issue on IHTP, Ceschia et al. competition paper (air.uniud.it), ORTEC/KU Leuven/Twente pages, competitor GitHub repos | no m19 value found below 21776; no special-issue article with per-instance m19 results surfaced |
| V3R1T4S PRs, all states (`gh pr list --state all --limit 2000`: 834 PRs; `gh search prs m19`, `ihtp`) | 14 IHTP PRs (#358, #359, #416, #431, #786-#790, #794-#798). I read the full diff text and body of each. Only #431 mentions m19: README/body say its solver "strictly improved" m19 among 15 m-instances, but no m19 value is stated and there is no m19 file. The 2026-10-23 table batch matches that list, so this is consistent with it being the listed 21776. #358 lists other per-instance values but none for m19. No PR shows any m19 value <= 21752. |
| V3R1T4S TROPHY_CASE.md (main) | no IHTP/IHTC/m19 entry |
| V3R1T4S known-knowns/ (main tree) | no IHTP entry. Only known-unknowns target pages exist, quoting m26 69730 and m01 3380, nothing for m19 |
| Organisers' repo release assets | 0 releases |
| Neighbouring cells (m18, m20; the i-set) | different instances, not comparable to an m19 object |

Nothing found at or below 21752. The best known value is 21776.

## 3. Object versus its published seed (claim names the seed: published_sol_m19.json, 21776)
Both solutions were re-scored with the claim's IHTP_Validator.cc (built with g++ -O2 -std=c++17):
- published: 0 violations, cost 21776 (AgeMix 260, Skill 216, Continuity 1003, Workload 177, OpenOT 1320, SurgeonTransfer 60, Delay 7490, Unscheduled 11250)
- claimed: 0 violations, cost 21752 (260, 177, 979, 176, 1350, 70, 7490, 11250). That is 24 below the table (-0.11%).

Structural diff:
- Admission days and the set of unscheduled patients are identical (25 unscheduled in both).
- 66 of 213 patients change room. 159 change operating theatre.
- 391 of 395 nurse shift-assignments differ.

Trivial-edit tests:
- Not a relabelling or symmetry. The theatre mapping per (day, old theatre) splits in 23 of 44 groups. The room mapping splits in 17 of 18 rooms. Only 74 of 153 room-day cohabitation groups survive unchanged, so the patient-to-room partition really changed.
- Not deletion or restriction. The patient set and the admissions are unchanged, and the cost falls.
- Nurse-layer-only polish (the arXiv 2610.00044 edit type, with rooms, theatres and admissions fixed from the published solution) does not reach the claim. A simulated-annealing check written for this audit uses an evaluator that matches the validator: 1396 on the seed and 1332 on the claim. Seven runs of 60-90 s (seeds 1-4, several temperatures, about 20-30M moves each) gave at best a 7-point improvement, to 21769. The claim needs 24. This is heuristic evidence, not an exact proof, because no MIP solver was available.
- The gain comes from a joint room-and-nurse re-assignment: Skill -39, Continuity -24, Workload -1, against OpenOT +30 and SurgeonTransfer +10. That is a multi-layer re-optimisation that none of the listed trivial edits gives alone.

Caveats:
- The margin is small (24 points).
- The method is seeded simulated annealing (150 s + 300 s per CLAIM.md).
- PR #431's solver code was not executed (it is untrusted code), so its exact m19 output is inferred from the organisers' table rather than reproduced.

## Verdict
21752 is strictly below every m19 value found (live table 21776, arXiv 2511.04685v2 BKS 21790, all PRs, TROPHY_CASE, known-knowns, literature). The change from the named published seed is more than relabelling, symmetry, deletion, restriction or nurse-layer polish.
novelty: PASS
pass: true
