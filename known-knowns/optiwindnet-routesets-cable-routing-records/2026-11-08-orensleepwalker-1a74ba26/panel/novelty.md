# Novelty review: OptiWindNet RouteSets r26.10-v4, Hornsea Two West, capacity 9, branched

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

Claimed object: `object/routeset-packed.json` / `object/segments.json`, total length 191786.9545 m, branched (max turbine degree 3), 13 feeders, seeded from stored routeset id 4305 (baselines.hgs, radial, 192886.7293 m). CLAIM.md names the seed.

## 1. Status source (fetched once, no retries)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- Time (UTC): 2026-11-08T16:35:08Z. HTTP status: 301. Body: `{"status": 301, "message": "Redirecting...", "location": "https://zenodo.org/api/records/23537067"}`. The latest version therefore resolves to record 23537067 itself.
- I followed that redirect target once (one request, no retry) at 2026-11-08T16:35:18Z: https://zenodo.org/api/records/23537067 returned HTTP 200, id 23537067, publication_date 2026-10-21, created 2026-10-21T15:29:56Z, one file `optiwindnet-routesets-r26.10-v4.sqlite.xz` (28464808 bytes, md5 85faffb2e13600b017f1b583b259edd7).
- The claim's `references/optiwindnet-routesets-r26.10-v4.sqlite.xz` has the same md5 (85faffb2...) and the sha256 that CLAIM.md states (c78c8f3c...5e3a). No newer version exists. The version list for the concept shows only 23537067 (r26.10-v4, 2026-10-21) and 20053479 (r26.05-v4, 2026-05-06).

## 2. The instance's own cell in r26.10-v4

Nodeset 'Hornsea Two West' (T=110, R=1, B=9, no obstacles). Every stored capacity-9 set:

| id | creator | topology | length (m) | feeders |
|---|---|---|---|---|
| 4305 | baselines.hgs | radial | 192886.7293 | [13] |
| 44553 | MILP.pyomo.cplex | radial | 192886.7293 | [13] |
| 100 | MILP.pyomo.cplex | branched | 193222.8342 (bound 186907.20, relgap 3.2%, time limit) | [13] |
| 4181 | baselines.lkh | radial | 194384.9991 | [13] |

The object was rebuilt from `object/routeset-packed.json` with optiwindnet 0.3.2: its length is 191786.95446995908 m, `validate_routeset` returns [], and the sum of Euclidean lengths over `object/segments.json` is the same value. All prime endpoints match the nodeset's VertexC exactly, and all 112 segments lie inside the border (the site has no obstacles). The object is 1099.7748 m (0.570%) shorter than the best stored set, with feeders 13 <= 13. It is also above the branched MILP bound of 186907.20 m, so nothing contradicts it.

## 3. Neighbouring cells (restriction or propagation from other capacities)

On the same nodeset I rebuilt every stored set for capacities 2-8 and 10-12 and computed each feeder subtree's load:
- Capacities 2-8: every set is valid at capacity 9, but the shortest is 202942.44 m (capacity 8, id 99), which is longer than both the object and the stored capacity-9 best.
- Capacities 10-12: every set has a subtree with more than 9 turbines (max load 10/11/12) and uses only 10-12 feeders, so none is valid at capacity 9.

None of the neighbouring cells gives a shorter valid capacity-9 set.

## 4. Same site under another name, orientation or mirroring (DTU datasets)

I downloaded these into `panel/work-novelty/dl-files/` and read them only as data:
- r26.05-v4 (Zenodo 20053479).
- paperdb v3 and MILP_model_comparison v3 (Zenodo 18864643).
- paperdb v4 and MILP_model_comparison v4 (Zenodo 19798734).
- `optiwindnet_routesets.zip` and `data_driven_hybrid.zip` (Zenodo 20140812).

In every SQLite file I compared each nodeset with T=110 against Hornsea Two West. The test was the sorted multiset of pairwise turbine distances, which is invariant to rotation, mirroring, translation and scale.
- The only congruent nodeset in any file is 'Hornsea Two West' itself. The '!Hornsea Two West!...' augmented sets have different T.
- r26.05-v4 holds the same four capacity-9 sets (ids 4305, 44553, 100, 4181, same lengths).
- paperdb v3/v4 hold Hornsea Two West (B=10) only at capacities 2-6, 11 and 12, with no capacity-9 set.
- The MILP_model_comparison files contain no congruent nodeset.
- The 20140812 zips contain notebooks, code and figures, but no Hornsea Two West route set.

## 5. Code, releases, literature, this repo

- **OptiWindNet GitHub repository** (DTUWindEnergy/OptiWindNet; last push 2026-10-19):
  - Releases v0.1.6 to v0.3.2 carry only wheels and sdists. The data folder has location files ('Hornsea Two West.yaml', 'Hornsea 2.osm.pbf') but no route sets.
  - The notebooks that mention hornsea2w (hi12_locations, lo12_locations) only list locations. Stored notebook pickles exist only for the Cazzaro and Taylor sites.
- **Preprint wes-2026-124** (posted 2026-07-28, in review, comments open until 2026-11-18): the landing page does not mention Hornsea Two West and reports no per-instance capacity-9 result. Its data links are Zenodo 20053479 and 20140812, both checked above.
- **Web searches** for 'Hornsea Two West' and hornsea2w cable routing, and for 2025-2026 cable-routing or branched-CVRP best-known solutions, found nothing for this instance.
- **github.com/elder-plinius/V3R1T4S**:
  - TROPHY_CASE.md (main) has no OptiWindNet, Hornsea or cable entry.
  - known-knowns/ has no OptiWindNet entry.
  - The target file on main still reads 'open as of 2026-10-30', and its last commit is f3b19b4 (the pinned commit).
  - I listed all 970 open and closed PRs. Twelve OptiWindNet claim PRs exist (Hornsea One.1_OSS, Yi-2019.1_OSS, Cazzaro-2022G-210). None concerns Hornsea Two West. Searches for 'Two West', 'hornsea2w' and 'Hornsea_Two_West' in PRs, issues and code return nothing.

## 6. Is it more than a trivial edit of the seed?

Against seed 4305, the object keeps 104 of 111 prime links and the identical detour feeders (35 and 47 via border vertices). It changes 7 links:
- Removed: (2,3), (5,14), (18,26), (43,38), (77,78), (104,93), (104,103); 11056.6 m in total.
- Added: (3,12), (14,15), (17,26), (33,43), (84,77), (96,104), (104,97); 9956.8 m in total.

How the trivial edits compare:
- Relabelling, symmetry, deletion and restriction keep the length at 192886.73 m or make the set invalid.
- The turbine and substation positions are fixed and the detours are unchanged, so no numerical polish applies.
- The neighbouring-cell propagation (section 3) gives nothing shorter.

I also tested a stronger baseline than the kit's list, a greedy best-improvement hill-climb from id 4305. Each step re-parents a single subtree, under capacity 9, at most 13 feeders, no crossings and staying inside the border (script: `panel/work-novelty/scripts/hillclimb.py`). It stops at 192073.54 m after 5 moves. That is still 286.59 m longer than the object. I checked this baseline only with my own geometry checks, not with optiwindnet's validator. The same hill-climb from id 100 finds no improving move. So the object beats what trivial edits of the published seed give, and also a simple local search from it.

## Verdict

- The status source resolves to 23537067 (r26.10-v4, published 2026-10-21) as of 2026-11-08T16:35Z.
- No published route set for Hornsea Two West at capacity 9 is shorter than 191786.9545 m. That covers this release, the earlier release r26.05-v4, DTU's paperdb and MILP_model_comparison sets, the thesis artifacts, the OptiWindNet repository and releases, the preprint, this repo's TROPHY_CASE.md, known-knowns/ and its PRs.
- Congruent or relabelled copies of the site and neighbouring capacities give nothing shorter.
- The object names its seed (id 4305) and beats it by 1099.77 m (0.570%). That is far above the 1e-6 relative threshold, so this is not a tie.
- It also beats a single-relink local search from the seed by 286.59 m.

novelty: NEW (strictly shorter than everything known for this cell)

pass: true
