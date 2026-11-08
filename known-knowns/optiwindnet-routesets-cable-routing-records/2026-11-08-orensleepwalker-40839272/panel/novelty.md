# Novelty review: London Array.1_OSS, capacity 9, branched

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

Claim (CLAIM.md): branched route set, total length 153957.9889 m, 20 feeders, for nodeset "London Array.1_OSS" (175 turbines, 1 substation, 9 border vertices, 0 obstacles), capacity 9, release r26.10-v4. It names its seed as stored set 44577 (MILP.pyomo.cplex, radial, 154359.1604 m), which ties with 9629 (baselines.hgs).

## 1. Status source (fetched once, no retries)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- HTTP 200, resolved to https://zenodo.org/api/records/23537067
- Fetch time (UTC): 2026-11-08T16:35:10Z
- Latest record id: 23537067. Publication date: 2026-10-21. Created/modified: 2026-10-21T15:29:56Z.
- Single file: optiwindnet-routesets-r26.10-v4.sqlite.xz, 28464808 bytes, md5 85faffb2e13600b017f1b583b259edd7.
- The claim's copy references/optiwindnet-routesets-r26.10-v4.sqlite.xz has md5 85faffb2e13600b017f1b583b259edd7, which matches. Its sha256 is c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, as stated in CLAIM.md.
- The concept 20053478 has only two versions: 23537067 (r26.10-v4, 2026-10-21) and 20053479 (r26.05-v4, 2026-05-06). There is no newer release.

## 2. The object, recomputed

- object/segments.json has 179 segments: 175 logical links plus detour pieces (D=4). Every endpoint is a VertexC coordinate of the r26.10 "London Array.1_OSS" nodeset.
- The sum of Euclidean segment lengths is 153957.98887 m, which matches the claim. The straight-line objective over logical links is 153949.51 m.
- Maximum turbine degree is 3 (4 turbines branch). The substation has degree 20, so there are 20 feeders.
- Subtree sizes are 7, 8, 8, 8 and sixteen 9s, all within capacity 9.
- I did not run validate_routeset here; the reproduction reviewer covers validity.

## 3. Stored sets for this cell and neighbouring cells

These are read from my own decompressed copy of the claim's reference file and from independently downloaded older files.

| source | London Array.1_OSS, cap 9 (best) | best at cap <= 8 (valid at cap 9) |
|---|---|---|
| r26.10-v4 (23537067) | 154359.1604 (44577 radial; 9629 ties); branched best 154403.5350 (2794) | 162086.42 (2793, cap 8) |
| r26.05-v4 (20053479) | identical rows: 44577, 9629, 2794, 8917 | 162086.42 |
| paperdb.v3 (18864643) | 154359.1604 (9629), 154403.5350 (2794) | 162086.42 |
| paperdb.v4 (19798734) | same as v3 | 162086.42 |

The claim is 401.17 m (0.260%) shorter than 154359.1604 m and 445.55 m shorter than the best stored branched set. All "London Array.1_OSS" nodesets in these files have the same digest as the claim's instance.

Every 175-turbine nodeset in r26.10, r26.05, paperdb.v3/v4 and MILP_model_comparison.v3/v4 (18864643/19798734), '!'-prefixed ones included, was compared on a distance-multiset signature. That signature is invariant to translation, rotation and mirroring. Only three geometries match the instance's turbines:
- "London Array" (2 substations) in r26.05 and r26.10: identical turbine coordinates.
- "London Array legacy" (2 substations) in MILP_model_comparison.v3/v4. After a Procrustes fit (det +1) it maps onto the instance's turbines with identity labels and a residual of 5.4 mm. Its two substations come out swapped (relabelled) and one is offset by about 100 m from the release's position.

### Transplant test: 2-substation sets onto the single substation

I took every stored 2-substation set with capacity <= 9 in these files and kept all turbine-turbine links. Each subtree was then reattached to the single substation at (395165.77, 5719457.03), the midpoint of the two original substations. Two variants were scored:
- (a) the same feeder turbines;
- (b) the best re-root per subtree: the subtree's node closest to the substation. Variant (b) uses straight lines with no crossing check, so it is a lower bound for this edit.

The results (straight-line metres; scripts/transplant.py, transplant_results.json):

- r26.10/r26.05 "London Array" id 150 (cap 9, 149449.24, feeders [10,10]): (a) 196623.17, (b) 182602.34.
- Same nodeset, id 143 (cap 8, 156127.25): (b) 196622.91.
- "London Array legacy" id 122 (cap 9, 149734.55, [11,10], which is 21 feeders): (b) 182614.86.
- "London Array legacy" id 263 (cap 9, 150561.60, [10,10]): (b) 184858.46.
- "London Array legacy" id 121 (cap 8): (b) 188726.40.
- Every other transplanted set at capacities 2-7: (b) >= 206323.78.

The 2-substation sets are shorter in their own cell (149449 m) but say nothing about this cell. Their trivial transplants are at least 28.6 km longer than the claim.

### Other published sources (last 24 months)

- Zenodo 20140812 (PhD thesis artifacts, 2026-05-12): optiwindnet_routesets.zip and data_driven_hybrid.zip contain notebooks, figures, ML models and id lists. They hold no route sets, and no file mentions London.
- OptiWindNet (github.com/DTUWindEnergy/OptiWindNet, a mirror of the DTU GitLab; pushed 2026-10-19):
  - Releases v0.1.6 to v0.3.2 contain only wheel and sdist assets.
  - Zenodo 23321367 (v0.3.2) is the source archive.
  - The tree holds no London Array route sets. "London Array.yaml" is the site geometry. tests/cases.py and tests/sweep.py use the 2-substation 'london' site at capacities 4, 8 and 10 for heuristic and MILP test cases, with no stored lengths.
  - tests/milp_references.pkl, tests/pathfinder_golden.pkl and docs/figuredata/routers_summary.pkl contain no "London" string.
- Preprint wes-2026-124 (posted 28 Jul 2026; one referee comment, 3 Sep 2026): its links are dataset 20053479 and code 20140812, both checked above. The landing page gives no per-instance London Array value.
- EJOR 2026, vol. 329(3), 1037-1051 ("Flexible cable routing framework..."): this paper's data are paperdb.v3/v4, checked above.
- Web searches found other London Array cable studies only on the real 2-substation farm: a TU Delft floating-wind thesis, a reliability study (PMC11440233), and the arXiv 1907.02371 global-optimisation paper. None found a single-substation capacity-9 value.

### V3R1T4S repository (github.com/elder-plinius/V3R1T4S, HEAD 850aa9c, 2026-11-08T14:04:40Z)

- TROPHY_CASE.md: no OptiWindNet, cable or London entry.
- known-knowns/: no OptiWindNet directory on main.
- Pull requests: 970 listed, numbers 1-1019, open and closed. The 12 OptiWindNet claim PRs are #962-964, #967-968, #977-982 and #998. They cover Cazzaro-2022G-210.solid.1_OSS, Yi-2019.1_OSS and Hornsea One.1_OSS only.
- None of those PRs mentions London in its title, body or file list. GitHub search finds "London Array" in no PR and no code.

## 4. Trivial-edit test against the named seed

- Seed 44577 compared with the object: 13 links differ (13 removed, 13 added). 26 turbines change a link. 14 of 20 subtrees keep the same turbine set and 6 are rebuilt. The object has 4 branching turbines and the seed has none.
- I ran a best-improvement local search on the seed until it converged (scripts/localsearch.py). Each move cuts one link and re-hangs or re-roots the detached subtree on any node or the substation. Moves respect capacity 9, at most 20 feeders and no crossings. Lengths are straight-line and the border is ignored, which favours the edits.
  - 44577 and 9629 reach 154130.49 m after 2 moves.
  - 2794 has no improving move (154403.44 m).
- Adding leaf exchanges between subtrees (scripts/ls2.py) gives no further gain: 154130.49 m.
- Claim (straight-line objective): 153949.51 m, which is 180.98 m below the best result of trivial edits of the seed. The claim is longer than plain polish and genuinely restructures six strings.

Note: simple polish of the seed (154130.49 m straight-line) is itself already below the stored 154359.16 m, so beating the release in this cell needs little. The object still beats that easy result by a clear margin.

## 5. Verdict

The object is a valid-looking branched route set at 153957.99 m (Euclidean, detours included), using 20 feeders, no more than the seed's 20. It is strictly shorter than:
- every published route set I found for this instance in r26.10, r26.05, paperdb.v3/v4, the OptiWindNet repository and releases, and the 20140812 artifacts;
- every transplant of the 2-substation "London Array" and "London Array legacy" sets after relabelling, mirroring or re-rooting (>= 182602 m);
- every V3R1T4S PR, trophy and known-knowns entry (none covers this instance).

The object names its seed (44577) and beats what single-subtree and leaf-exchange polish of that seed gives by about 181 m. The margin over the best stored set is 401.17 m (relative 2.6e-3, well above 1e-6), so this is not a tie.

Caveat: I did not run the official validator or the border-containment check. Those belong to the reproduction and criterion reviewers. This pass is about novelty only.

novelty: CONFIRMED (strictly beats all known published sets for London Array.1_OSS cap 9; not a trivial edit of the named seed)

pass: true
