# Novelty review: IHTP i20, claimed cost 28812

context: subagent (Claude Code Agent tool, fresh context)
role: NOVELTY skeptic. I read only the claim folder (`claim/`) plus public web and GitHub sources.

## 1. Primary table: one plain fetch, no retries
- Command: `curl -sS -A 'V3R1T4S-research-agent (+https://github.com/elder-plinius/V3R1T4S)' -w '%{http_code}' https://ihtc2024.github.io/ihtp/index.html`
- URL: https://ihtc2024.github.io/ihtp/index.html
- Fetch time (`date -u`): 2026-10-31T00:27:12Z
- HTTP status: 200 (not blocked)
- Listed value for i20: **29042** (row `<td>i20</td><td class="text-right">29042</td>`, solution link sol_i20.json)
- Body sha256 2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363. It matches the scout's saved claim/ihtp_table.html byte for byte.
- Table history: organiser commit c078cf5788, 2026-10-23T10:07:15Z, "updated batch of UB". It changed i20 from 29098 to 29042. The organisers' current sol_i20.json has sha256 ec56e142…a24c, which is identical to claim/published_sol_i20.json.

## 2. Sources checked for an i20 value at or below 28812
| Source | i20 value found | At or below 28812? |
|---|---|---|
| Organiser upper-bound table (live, above) | 29042 | no |
| arXiv 2511.04685v2, Guericke et al. (Team Twente; journal version in ORDAL vol. 46, 2026, IHTP special issue) | LB 26006; "best sol" 29098; their runs 29543–29758 | no |
| arXiv 2610.00044, Gippini Requeijo (2026-09), nurse-layer exact reoptimisation | reports only i02, i05, m01, m03, m04; no i20 | n/a |
| Gioia et al., "Healthcare Predictive Timetabling" (ORDAL vol. 47, IHTP special issue); repo DanieleGioia/HealthcarePredictiveTimetabling | 4 i20 files, which I validated at 30748–33670 | no |
| Othman & Chiarandini (SDU/IMADA, 2nd place; ORDAL special issue); repo Arthod/ihtc2024-imada-submission | score.csv 30819 (validated: 0 violations, 30819) | no |
| Ceschia, Rosati, Schaerf, Zanazzo competition overview | competition-round results; no i20 below the table | no |
| GIPS (Echtzeitsysteme/gips-ihtc-2024-submission) scores.csv | 54742 | no |
| emfrea/ihtc2024-evolved-solvers-main (6 solvers, final/48h/all checkpoints) | min 29734 | no |
| ahmedelhefnawy21/ihtp-matheuristic… | own 30098; their BKS file 29098 | no |
| pchtsp/ihtc2024 | 35714 (validated) | no |
| Mattmandav/IHTC2024 | 44924 | no |
| AntonioPalma95/ihtc2024-heuristic-scheduler | 44018–45522 (validated) | no |
| angelaluiss/ihtc2024-tfg | 35853 | no |
| manongerard2002, massiung, davidgit0001, and about 15 other `ihtc` repos found by `gh search repos` | nothing below 29042; most have no i20 cost | no |
| V3R1T4S PRs: `gh pr list --state all --limit 2000` (828 PRs, open and closed) plus `gh search prs` for IHTP, IHTC, i20, sol_i20, 29042, 28812, 28851 | No i20 claim PR exists. PRs #358 (open) and #359 (closed) mention "i20: 29098 -> 28851" in the body text | no (28851 > 28812) |
| V3R1T4S TROPHY_CASE.md | no IHTP entry | n/a |
| V3R1T4S known-knowns/ (27 folders) | no IHTP entry. known-unknowns/optimization-benchmarks/ihtp-ihtc2024-upper-bounds.md is the open target and gives no i20 value | n/a |
| GitHub release assets of the repos above | none of these repos has a release | n/a |

The lowest known i20 value is 28851, mentioned in V3R1T4S PR #358/#359 body text. The lowest published value is 29042 (organiser table). The claimed **28812** is strictly below both.

## 3. Seed comparison: is the change more than a trivial edit?
CLAIM.md says the solution was seeded from published_sol_i20.json (the organisers' solution, 29042) and improved by simulated annealing. I compiled the official validator from claim/ in a scratch copy and ran it on both files:

| Component | published (29042) | claim (28812) |
|---|---|---|
| Violations | 0 | 0 |
| ElectiveUnscheduled | 20500 | 20500 |
| PatientDelay | 3480 | 3480 |
| OpenOperatingTheater | 1400 | 1400 |
| SurgeonTransfer | 17 | 22 |
| RoomAgeMix | 80 | 79 |
| RoomSkillLevel | 2040 | 1890 |
| ExcessiveNurseWorkload | 560 | 460 |
| ContinuityOfCare | 965 | 981 |

Structural diff:
- The same 147 patients are admitted on the same days.
- 61 patients are in a different room and 104 have a different operating theatre.
- 480 of 630 nurse room-shift slots changed.

The room and OT changes are not a relabelling or symmetry. No consistent global map exists, the per-day maps are inconsistent (78 of 100 for rooms, 9 of 35 for OTs), and the sets of roommates differ. Rooms also have unequal capacities (2/3/4). Nothing was deleted or restricted. RoomAgeMix changes, so the change is not confined to the nurse layer.

The trivial-edit baseline is reoptimising the nurse layer only, with all other layers held at the published values (the edit class used by arXiv 2610.00044). To reach 28812 that way, the published solution's nurse-layer cost would have to fall from 3565 to 3335 or less, a drop of 230.
- Single-slot nurse-reassignment SA (4 seeds × 150 s, about 25M moves each) found no improvement at all on the published solution (best 3565).
- 2610.00044 reports nurse-layer gains of only 0.075–0.125% on other instances. This would need 0.79%.
- Limitation: no MIP/CP solver was available here, so I could not run an exact nurse-layer reoptimisation. My valid lower bound (663) is too weak to rule it out formally.

The seed is named and the edit is non-trivial. On the evidence available, the result beats what trivial edits of the published object give.

## Verdict
28812 is strictly below every value found: the table's 29042, the literature's 29098, the V3R1T4S PR body text's 28851, and every competitor repository at 29734 or above. The claim is not a tie and not a trivial edit of the named seed. Caveat: an exact nurse-layer-only reoptimisation of the seed was not run.

pass: true
