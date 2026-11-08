# Novelty review: claim-h27 (Hornsea Two West, capacity 7, branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

Reviewer role: novelty skeptic. Inputs: the claim folder (CLAIM.md, REPRODUCE.md, criterion.txt, object/, references/, status/) and public sources. Downloads and scripts are in panel-h27/work-novelty/ (dl-* folders hold downloaded data, scripts/ holds my own code).

## 1. Status source (fetched once, no retries)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- Fetched 2026-11-08T16:35:04Z to 16:35:08Z UTC. Final HTTP status 200, after a redirect to https://zenodo.org/api/records/23537067.
- Latest record id: 23537067. publication_date: 2026-10-21. modified: 2026-10-21T15:29:56.915326+00:00.
- Single file: optiwindnet-routesets-r26.10-v4.sqlite.xz, 28,464,808 bytes, md5:85faffb2e13600b017f1b583b259edd7.
- The local copy references/optiwindnet-routesets-r26.10-v4.sqlite.xz has the same md5 (85faffb2...edd7) and sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, matching CLAIM.md. No newer version exists. The concept version list shows only 23537067 (r26.10-v4) and 20053479 (r26.05-v4, 2026-05-06).

## 2. The object

- object/segments.json has 112 segments. Their Euclidean lengths sum to 217395.35402025303 m, the claimed value. Every endpoint is a vertex of the stored nodeset 'Hornsea Two West' (T=110, R=1, B=9).
- My own parent-pointer walk over object/routeset-packed.json finds 16 feeders and a maximum subtree load of 7. Five turbines have degree 3 (12, 15, 58, 71, 97), so the set is branched. It has two detour hops through clones of vertices 49 and 50.
- Validity checks (the validator, containment and crossings) belong to the other panel members. I only checked the facts that bear on novelty.

## 3. Stored sets for this cell (r26.10-v4, nodeset 'Hornsea Two West', capacity 7)

| id | creator | topology | length (m) | feeders |
|---|---|---|---|---|
| 3689 | baselines.hgs | radial | 217712.18494496983 | [16] |
| 44466 | MILP.pyomo.cplex (bound 212998.13, relgap 2.1%, time limit) | radial | 217712.18494496983 | [16] |
| 98 | MILP.pyomo.cplex (bound 212127.21, relgap 2.4%, time limit) | branched | 218384.3987299083 | [16] |
| 4178 | baselines.lkh | radial | 234134.8716544603 | [16] |

- The object is 316.8309 m (0.146%) shorter than the best stored set, which is far above the 1e-6 relative threshold. It also stays within the feeder cap of [16].
- r26.05-v4 (Zenodo 20053479) holds the same four rows with the same lengths.

## 4. Other published sources searched

- **DTU's earlier datasets.**
  - Zenodo 18864643 (paperdb.v3, MILP_model_comparison.v3) and 19798734 (paperdb.v4, MILP_model_comparison.v4) are the data for the EJOR "Flexible cable routing framework" paper, published 2025-03-28. Their schema is readable directly, so no migration was needed.
  - Both paperdb files contain the same 110-turbine 'Hornsea Two West' nodeset (B=10). Its stored capacities are 2-6, 11 and 12 only. There is no capacity-7 route set.
  - The capacity-7 'hornsea2w' rows in paperdb belong to augmented subsets with 50-97 turbines, which are different instances.
  - The MILP_model_comparison files have no Hornsea rows.
- **Geometric search for the same site under another name, orientation or mirroring.** In r26.10-v4, r26.05-v4, paperdb v3/v4 and both MILP_model_comparison files, I compared every nodeset with T=110 and R=1 to this instance. The test was the sorted pairwise-distance multiset after scale normalisation, which is invariant to rotation, mirroring, translation and scale. The only matches are the 'Hornsea Two West' entries themselves.
- **Supersets that a deletion edit could exploit.**
  - No real-site nodeset in r26.10-v4 or paperdb contains all 110 turbine positions, other than the instance itself.
  - None of the 118 augmented '!Hornsea Two West!...' nodesets contains them either. A scale-invariant root-distance test matched at most 2 of 110.
- **Zenodo 20140812** (PhD thesis code and artifacts, 2026-05-12) contains notebooks, figures and ML models but no route-set data. A text search for Hornsea Two West, hornsea2w and lengths around 217 km found nothing.
- **OptiWindNet repository** (github.com/DTUWindEnergy/OptiWindNet, mirror of the DTU GitLab):
  - Releases v0.1.6 to v0.3.2 carry only wheel and sdist assets.
  - The tree has optiwindnet/data/Hornsea Two West.yaml, which is a layout and not a route set. Its stored route-set pickles cover only Cazzaro/Taylor.
  - tests/sweep.py references hornsea2w only at capacities 4 and 5. tests/milp_references.pkl has no Hornsea strings.
- **wes-2026-124 preprint.** I extracted text from all 13 pages of https://wes.copernicus.org/preprints/wes-2026-124/wes-2026-124.pdf. It contains no Hornsea Two West value. It points to the Zenodo datasets.
- **V3R1T4S** (github.com/elder-plinius/V3R1T4S, main pushed 2026-11-08T14:04:42Z):
  - TROPHY_CASE.md has no OptiWindNet or Hornsea entry.
  - known-knowns/ has no optiwindnet-routesets folder.
  - I listed all 970 PRs (open and closed) and searched them by text. The OptiWindNet claim PRs are #962-#964, #967, #968, #977-#982 and #998. They cover Cazzaro-2022G-210.solid.1_OSS, Yi-2019.1_OSS and Hornsea One.1_OSS. None covers Hornsea Two West, and searches for 'hornsea2w' and '"Two West"' return nothing.
- **Web search** for "Hornsea Two West" cable routing, and for OptiWindNet Hornsea 2 results in 2025-2026, found no published inter-array route set for this 110-turbine instance.

## 5. Trivial-edit analysis

The claim names its seed: stored sets 3689 and 44466, which have identical link sets. Compared with the seed, the object differs in exactly 7 links.

- Removed: (root,63), (2,11), (5,14), (55,62), (59,60), (64,72), (93,104). Total length 16826.401 m.
- Added: (root,55), (11,12), (14,15), (58,60), (59,71), (62,63), (97,104). Total length 16509.570 m.
- Difference: 316.831 m. The detour hops are identical, so all the gain comes from re-linking.
- The 7 changes fall in three separate regions of the farm. They introduce turbines of degree 3, so they use the branched freedom.

What the kit's trivial edits give for this cell:

- **Relabelling or symmetry:** the length stays at 217712.18.
- **Deletion or restriction:** a cell instance must cover all 110 turbines, and no published superset exists (section 4).
- **Propagation rules:**
  - Radial to branched gives 217712.18, already counted.
  - A capacity-6 set is valid at capacity 7, but the best is 237431.00, which is longer.
  - All stored sets at capacities 8-12 have a maximum subtree load above 7, so none of them is valid at capacity 7.
- **Local numerical polish:** there are no continuous variables. Re-routing the detours does not apply, because the object's detours equal the seed's.

The best any of these edits reaches is therefore 217712.18 m. The object beats that by 316.83 m through a combinatorial re-linking, which is not on the trivial list.

## 6. Caveats

- The improvement is small (0.146%). It came from a generic CP-SAT large-neighbourhood search on an instance where the only stored branched effort is a 2023 CPLEX run that stopped at its time limit with a 2.4% gap. The record therefore reflects a weak stored branched baseline more than a hard-won result. That does not change the kit's novelty rule.
- The packed object's misc fields (termination OPTIMAL, relgap 9e-12, bound 217262.67) describe the last restricted sub-solve, not the whole instance. They must not be read as an optimality certificate. CLAIM.md correctly disclaims optimality.
- Residual gaps in the search:
  - The PhD thesis PDF itself was not located online.
  - The EJOR article was checked only through its data records.
  - GitHub numeric code searches for 217712.18, 218384.39 and 217395.35 timed out with HTTP 408.
  - The DTU GitLab was checked only through its GitHub mirror.

## Verdict

- The status source is current: 23537067, published 2026-10-21, read on 2026-11-08.
- No published route set for Hornsea Two West at capacity 7, of any topology, under this or any other name, orientation or mirroring, is shorter than 217712.18494 m.
- The object (217395.35402 m, 16 feeders, branched) beats it by 316.83 m. It is seeded from a named published object (3689/44466) and goes beyond everything the trivial edits give.

novelty: strictly beats everything known; not a trivial edit of a published object.

pass: true
