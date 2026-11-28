# Novelty skeptic: runs/2026-11-03-2153-orglabel
context: subagent (novelty)
fetched: 2026-11-03 ~16:58 EST (America/New_York), live, once each

Claim under test: A131449 flattened index 66 (T(6,2)) = 360; row 6 in claim/object/ROW6.txt.

## OEIS entry (https://oeis.org/A131449, internal text format)
- %I #12, last edit Aug 29 2019; %K nonn,more,tabf (keyword more present); %O 0,3.
- DATA ends ...,3,3,2,1,720, so index 65 = 720 = T(6,1). There is no 360 after 720, and no row-6 values beyond 6! anywhere in %C/%e/%H.
- No %F/%Y/extension/program lines give row 6.

## b-file (https://oeis.org/A131449/b131449.txt)
- Ends `65 720`. It is byte-identical to claim/table/preclaim_b131449.txt (diff clean). Index 66 is absent.

## History (https://oeis.org/history?seq=A131449 and &start=10)
- Revisions #1 (2007) through #12 (2019): link URL edits (Lang -> LANGCHANGE), author-line edits, approvals. No pending or draft revision, and no added terms. No row-6 values appear.

## Lang's linked files
- a131449.txt ("First 6 rows"): rows 0..5 only, then ". . ." and e.o.f. No row 6.
- a131449fig5.pdf: n=5 trees only (42 trees, 20 classes, sum 945). No 720 or 360 for n=6.

## OEIS value searches (fmt=text, live)
- 720,360,360,360,360,360,240: No results.
- 720,360,360,360,360,360: No results.
- 2,1,720,360,360,360,360,360,240: No results.
- 720,360,360,360,360,360,240,240,240,240,180: No results.
- 1,720,360,360: No results.
These agree with claim/table/vs_datatail_row6.txt and claim/table/vs_row6_head.txt.

## Web (2026)
- Search "A131449 organic increasing labelings rooted ordered trees 2026" returned only the OEIS entry, Lang's two files, and arXiv 2510.03039 / Discrete Math 2026 ("Labeled Plane Trees and Increasing Plane Trees"). That paper covers totals (2n-1)!! and root-degree refinements, not the per-tree row-6 list. I found no published row 6 in A131449's order.

## Repo / bank / PRs (repo at origin/HEAD 7712cc8, Nov 3 2026)
- `git grep A131449 origin/HEAD`: no hits in TROPHY_CASE.md, known-knowns/, bank/targets.json, or bank/proposed/. The only substring hits for "131449" are digits inside unrelated codetables cert JSON floats.
- GitHub issue/PR search repo:elder-plinius/V3R1T4S "A131449": 0. Open PRs (pages 1-3, 300 checked): none mention 131449.
- A131449 is not in the criterion's excluded list.

## Caveat (for criterion skeptic, not a novelty defect)
- Row order within a row is not defined by %N, so "index 66" depends on the non-increasing convention. Under that convention T(6,2) = 360. Novelty holds either way: no row-6 term is published anywhere checked.

pass: true
