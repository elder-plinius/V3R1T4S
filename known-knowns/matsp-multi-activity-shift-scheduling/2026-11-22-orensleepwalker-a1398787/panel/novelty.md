# Novelty review: matsp instance 80 (80_14_10_2), claimed penalty 0

context: fresh subagent started for this claim only

Reviewer role: novelty skeptic (one of three). Inputs: claim/ (read only) and the web.

## Status source (fetched once each, plain curl, User-Agent "V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)", no retries)

- https://www.schedulingbenchmarks.org/matsp/ : HTTP 200, 2026-11-22T08:06:44Z, 75849 bytes.
  Row for instance 80, verbatim cells: `80 | 14 | 10 | 2 | 6 | TRA26` (Instance, Days, Staff, Tasks, Best known, Reference).
  Neighbouring rows: 79 (14/10/1) 509 TRA26; 81 (14/20/1) 1510 TRA26; 5 (7/10/2) 0 TRA26. All 226 reference cells read TRA26.
  The page links no TRA26 solution files (links: instances zip, ProblemDefinition.pdf, verify.html, the DOI, papers); so no published roster for instance 80 exists to seed from.
- https://www.schedulingbenchmarks.org/changes.html : HTTP 200, 2026-11-22T08:06:45Z, 23627 bytes.
  Newest entries: 29-Oct-2026 (nurse history), 27-Oct-2026 and 21-Oct-2026 (Chernikov, nurse instances), 15-Oct-2026 (nurse LB), 07-Oct-2026 (multi-activity command-line verifier), 12-Sep-2026 (nurse Instance24), 01-Sep-2026 (multi-activity new solutions, Trautsch and Kovari, SA).
  No multi-activity result entry newer than the 01-Sep-2026 TRA26 one.

## Literature and code searched (last 24 months and earlier sources)

- Trautsch and Kovari, PATAT 2024 proceedings paper "A Simulated Annealing Approach to the Multi-Activity Multi-Day Shift Scheduling Problem" (patatconference.org/patat2024/proceedings/papers/125.pdf, read): per-instance table gives instance 80 (14/10/2) as VNS [Qu-Curtois] 292, SA 88. No lower bounds, no optimality claims, no code or data link.
- Trautsch and Kovari, J. Sched. 2026, doi 10.1007/s10951-026-00886-z (the TRA26 source): the Springer page redirects to an authorization page (idp.springer.com), treated as a block and not worked around. Its per-instance value for instance 80 could not be read directly; the site table (which is the TRA26 import) gives 6. Supplementary material not reachable.
- Qu and Curtois, ICORES 2020 (VNS, the original benchmark paper): instance 80 value 292 (as cited in the PATAT 2024 table). The site lists no IP/LB results for these instances.
- Romer, J. Sched. 2023/2024 (block-based state-expanded network MILPs, exact): uses the Demassey et al. (2005) and Dahmen et al. (2018) single-day sets, not the Curtois-Qu multi-day set (from abstract and indexing records; Springer full text blocked as above).
- Web searches for 2024-2026 papers or GitHub code on these instances (CP-SAT, MIP, column generation, "instances1_225", "matsp"): nothing found reporting any value for instance 80, and no lower bounds for this set.
- V3R1T4S repository (github.com/elder-plinius/V3R1T4S, via gh):
  - TROPHY_CASE.md (100 lines): no entry mentioning matsp, multi-activity, shift scheduling or schedulingbenchmarks.
  - Tree: no known-knowns/ file on matsp or shift scheduling; only the open target known-unknowns/optimization-benchmarks/matsp-multi-activity-shift-scheduling.md (and the separate Curtois NRP target). No releases.
  - PR and issue search for "matsp", "multi-activity", "shift scheduling", "schedulingbenchmarks": no relevant hits (the "multi-activity" PR hits are unrelated physics/chemistry claims). Later search-API queries ("Curtois" issues, "roster", "TRA26", "80_14_10_2", "nurse") returned HTTP 403 rate limit; not retried.
  - Instead, the full lists via the non-search API (1162 PRs, all states; 52 issues, all states) were filtered on title and body for matsp, multi-activity shift, shift scheduling, curtois, roster, schedulingbench, TRA26, 80_14_10_2: no match.

## Comparison

- Best published value for this cell: 6 (TRA26, site table); earlier 88 (SA, PATAT 2024) and 292 (VNS, Qu-Curtois). Claimed: 0. 0 < 6 strictly; not a tie.
- The penalty is a sum of squared overstaffing terms, so 0 is a lower bound; the claim is optimal, and no published object could be better.
- Neighbouring cells: instance 5 (7/10/2) is at 0 but is a different instance (different horizon and demand); it cannot be turned into an instance-80 roster by deletion, restriction, relabelling or symmetry. No published roster exists for instance 80 or its neighbours under TRA26, so trivial edits of a published object are not available as an explanation.
- From-scratch check: claim/code/cpsat_matsp.py reads only the instance file from instances1_225.zip, builds a CP-SAT model and solves with fixed seed; there is no AddHint, warm start or solution file input. The object hash (a139878...a972) equals data/selected_solution.xml as the PREREG states. The pilot log cited in CLAIM.md lies outside claim/ and was not inspected. Running the claim's own verifier gave "violations 0, penalty 0, record 6, PASS" (correctness is for the other reviewers).

## Residual risks

- The TRA26 journal article and its supplement could not be read (Springer authorization redirect). Any positive value it reports for instance 80 is still beaten by 0; only an unposted published 0 would make this a tie. The site's 01-Sep-2026 import of all TRA26 values makes this unlikely.
- Some GitHub search queries were rate limited; the full PR and issue listings cover them.

novelty: strict improvement 6 -> 0 on instance 80; nothing published at or below 6 found.

pass: true
