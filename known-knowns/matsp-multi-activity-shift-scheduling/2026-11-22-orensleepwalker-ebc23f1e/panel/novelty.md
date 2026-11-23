# Novelty review: instance 155 (155_28_10_2), claimed penalty 0 vs best known 24 (TRA26)

context: fresh subagent started for this claim only

Inputs read: claim/CLAIM.md, claim/target.md (and, for the seeding question only, claim/PREREG.md, claim/REPRODUCE.md, claim/code/). Nothing else in the workspace.

## Status source (fetched once each, plain curl, UA "V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)", no retries)

- https://www.schedulingbenchmarks.org/matsp/ : HTTP 200, 75849 bytes, 2026-11-22T08:06:45Z.
  Columns: Instance | Days | Staff | Tasks | Best known | Reference. Row 155: `155 | 28 | 10 | 2 | 24 | TRA26`
  (neighbours: `154 | 28 | 10 | 1 | 1285 | TRA26`, `156 | 28 | 20 | 1 | 3359 | TRA26`). There is no lower-bound column, and the page links to no per-instance rosters (the only "solutions" link is commented out and points at the nurse instances 1-24 zip).
- https://www.schedulingbenchmarks.org/changes.html : HTTP 200, 23627 bytes, 2026-11-22T08:06:45Z.
  The newest multi-activity entries are 01-Sep-2026 (new solutions by Trautsch and Kovari, multi-neighbourhood SA) and 07-Oct-2026 (command-line verifier released). The later entries (15-Oct, 21-Oct, 27-Oct and 29-Oct-2026) all concern the nurse rostering instances. No multi-activity update is newer than the one crediting TRA26.

## Literature and code searched (last 24 months and earlier sources)

- Trautsch and Kovari, PATAT 2024 proceedings, pp. 125-138, "A Simulated Annealing Approach to the Multi-Activity Multi-Day Shift Scheduling Problem" (patatconference.org/patat2024/proceedings/papers/125.pdf, fetched once). Appendix Table 4, row 155: `155 28 10 2 | VNS: - | SA: 255`. VNS (Qu and Curtois) found no feasible solution, and SA found 255. The paper claims no lower bounds and no optimality for this instance.
- TRA26 journal version (doi 10.1007/s10951-026-00886-z): the DOI resolves to link.springer.com, which redirected to an idp.springer.com authorization/cookie flow. I did not work around this, so the article body and supplementary material were NOT read. The site's table credits TRA26 with 24 for instance 155, and that is the value compared here.
- Qu and Curtois, ICORES 2020, VNS for MASSP (the benchmark paper). According to the PATAT Table 4 VNS column, it has no value for 155. Its earlier IP model/results link on the site is commented out and concerns the nurse instances.
- Web searches (Trautsch Kovari J. Sched. 2026; Curtois Qu MASSP lower bounds 2025-2026; schedulingbenchmarks matsp GitHub solver; MASSP 225 instances CP-SAT/MIP optimal 2025-2026). These turned up Römer (J. Sched. 2023, MILP formulations on other MASSP instance sets), Salvagnin and Walsh 2012, Quimper and Rousseau 2010, Shariat theses, OR-Tools employee-scheduling examples. None of them reports a value at or below 24, or any optimality or lower bound, for Curtois-Qu instance 155. I found no public code or release asset with rosters for these instances.
- V3R1T4S repository (gh CLI, HEAD 5db3547, committed 2026-11-19T22:48:58Z):
  - TROPHY_CASE.md (100 lines): no match for matsp, multi-activity, shift sched or schedulingbench.
  - known-knowns/: no directory or file for matsp or shift scheduling. The only match in the repo tree is the target file known-unknowns/optimization-benchmarks/matsp-multi-activity-shift-scheduling.md.
  - PR/issue search (open and closed) for "matsp", "shift scheduling", "schedulingbenchmarks", "Curtois", "roster": 0 results. "multi-activity" matched only unrelated PRs (#824, #843, #818, #813, #568, #817, #1200, about lattice activity and MMLIB). The PR search for "TRA26" returned 0.
  - Blocked: the GitHub search API returned 403 (rate limit) on the supplementary queries (TRA26 issues, "staff scheduling", "nurse"). These were not retried. All the required search terms had already returned.

## Comparison with published objects

- Published values for this cell: 255 (SA, PATAT 2024) and 24 (TRA26, site table). No roster for instance 155 (or any other MATSP instance from TRA26) is published, so the claimed roster cannot be a trivial edit (deletion, restriction, relabelling, symmetry, local polish) of a published object.
- Neighbouring cells (154, 156 and others) have much larger best known values, and no published rosters exist to transfer from. A 0-penalty roster for 155 does not follow from any published object.
- Seeding: claim/code/cpsat_matsp.py builds the model from the instance file alone. It contains no AddHint or solution-file input (grep for "hint" gives 0), and it uses a fixed random seed of 1. This matches the statement "found from scratch by an exact solver".
- Sanity check (not a reproduction review): claim/code/verify_claim.py on the object gives "violations 0, penalty 0, record 24, PASS". The object is byte-identical to data/selected_solution.xml.
- Penalty 0 < 24, so this is a strict improvement and not a tie. Because the objective is a sum of squares, 0 is also a lower bound, so the result is optimal.

## Caveat

The TRA26 article and its ESM could not be read (Springer auth redirect). However, the site's table is the curated record for TRA26, and it lists 24 for this instance.

novelty: confirmed. The claimed penalty 0 strictly beats every published value found (24 TRA26, 255 SA PATAT 2024, none from VNS), and it is not derivable from any published roster.

pass: true
