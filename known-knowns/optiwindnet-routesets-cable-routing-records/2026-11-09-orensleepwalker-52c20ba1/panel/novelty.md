# Novelty review: claim-so4 (Sofia, capacity 4, branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

Role: novelty skeptic. Inputs: the claim folder (read-only) and the public web. Scripts, downloads and logs are in `panel-so4/work-novelty/`.

## 1. Status source (fetched once, no retries)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- HTTP status: 200. The redirect ended at https://zenodo.org/api/records/23537067.
- Fetched at 2026-11-09T09:14:17Z (UTC).
- Latest record id: 23537067, DOI 10.5281/zenodo.23537067, publication_date 2026-10-21. It has one file, `optiwindnet-routesets-r26.10-v4.sqlite.xz`: 28,464,808 bytes, md5 85faffb2e13600b017f1b583b259edd7.
- `references/optiwindnet-routesets-r26.10-v4.sqlite.xz` matches this exactly: same md5, and sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a as stated. No newer version exists. The concept's version list shows only 23537067 (r26.10-v4) and 20053479 (r26.05-v4, 2026-05-06).

## 2. Stored sets for this cell (r26.10-v4, nodeset "Sofia", T=100, R=1, B=6, no obstacles, capacity 4)

| id | creator | topology | length (m) | feeders |
|---|---|---|---|---|
| 46020 | baselines.lkh | radial | 378587.2597 | [25] |
| 25155 | MILP.pyomo.cplex (relgap 0.5%, bound 373560.51 on straight-line objective) | branched | 378897.5658 | [25] |
| 35902 | MILP.pyomo.cplex | radial | 379237.6114 | [25] |
| 25008 | baselines.hgs | radial | 379237.7079 | [25] |

These match what CLAIM.md says: the shortest stored set is 46020 at 378587.2597 m, and the shortest stored branched set is 25155 at 378897.5658 m.

Neighbouring cells:
- Capacity 3: 458780.83 m with 34 feeders. Its sets are feasible at capacity 4, but they are much longer and exceed the 25-feeder cap.
- Capacity 5: 323250.04 m. Its sets are infeasible at capacity 4.
- The release has no other non-'!' Sofia variant (no `.1_OSS` or `.solid`).

## 3. Object as checked

- I rebuilt G from `object/routeset-packed.json` and the database nodeset. I did not unpickle `object/G.pickle`.
- `validate_routeset` returns [].
- The length from the routed graph is 377027.9309567514 m. Re-routing the bare topology with optiwindnet's PathFinder gives the same value.
- `object/segments.json` has 113 segments.
  - Their Euclidean sum is 377027.9309567514 m.
  - All endpoints are nodeset vertices.
  - No segment leaves the border polygon (shapely, 1e-6 m tolerance).
  - No two segments cross.
- The substation has 25 feeders. Every subtree holds 4 turbines. The maximum turbine degree is 3, so the set is genuinely branched.
- The straight-line objective is 375860.98 m.
- The object is 1559.3288 m (0.412%) shorter than 46020. It is 1869.6348 m (0.493%) shorter than 25155.

## 4. Earlier and other publications searched

| Source | Result |
|---|---|
| Zenodo 20053479 (r26.05-v4, previous version of the same concept) | Sofia capacity 4 holds the same 4 sets with identical lengths. Shortest is 378587.2597 m. |
| Zenodo 18864643 (paperdb.v3, MILP_model_comparison.v3) and 19798734 (v4 of the same, 2025-03-28) | There is no "Sofia" nodeset. I also matched shapes against Sofia's 100 turbines, using sorted pairwise distances so rotation, translation, mirroring and scaling are covered. No nodeset in either file matches, under any name. The only name hit is a base64 false positive ("!Moray East!…ofia…", T=66). The v3/v4 files read directly with sqlite3, so no migration was needed. |
| Zenodo 20140812 (PhD thesis artifacts, 2026-05-12) | The two zips hold notebooks, figures and ML code. They contain no route-set databases and do not mention Sofia. |
| GitHub DTUWindEnergy/OptiWindNet (mirror of the DTU GitLab) at HEAD 664de87 (2026-10-16), and the v0.3.2 release wheel (releases v0.1.6 to v0.3.2 carry only wheel and sdist assets) | Sofia appears only as a location file (`optiwindnet/data/Sofia.yaml`) and as a capacity-9 NBEW/radial_EW example in `docs/notebooks/lo90_removed_heuristics.ipynb`. The repository has no capacity-4 route set. |
| mdealencar/interarray (pre-rebrand, release 0.0.1) | No Sofia and no route-set data. |
| Preprint wes-2026-124 (one version, posted 2026-07-28; RC1 2026-09-03; page updated 2026-11-08), PDF text searched | Reports aggregate analyses only. There is no per-instance length, and the text never mentions Sofia. |
| Web search, last 24 months | No published capacity-4 Sofia route set. The operator reports an as-built array of about 360 km, 109 cables and 18 strings. That is a different design: about 18 feeders implies a higher per-string capacity than 4. It is not a comparable route set under this cell's rules. |
| V3R1T4S: TROPHY_CASE.md, known-knowns/, tree, and all open and closed PRs and issues (searched for Sofia and optiwindnet) | TROPHY_CASE.md does not mention OptiWindNet. known-knowns/ has no entry for it. The only bank entry is `known-unknowns/optimization-benchmarks/optiwindnet-routesets-cable-routing-records.md` at pinned commit f3b19b4. There are 16 OptiWindNet claim PRs (Hornsea One, Hornsea Two West, London Array, Yi-2019, Cazzaro). None is for Sofia. A search for "Sofia" returns 0 issues or PRs. |

## 5. Trivial-edit comparison (CLAIM.md names its seed: 46020, radial, baselines.lkh)

How far the object is from its seed:
- 24 of 100 turbine parent links differ.
- Only 16 of 25 feeder groups (turbine partitions) are the same.
- Against the stored MILP and HGS sets, only 7 of 25 groups are the same.

So the object is not a relabelling, a deletion or restriction, or a per-group re-arrangement of any stored set. The site has fixed coordinates, so a symmetry or a numerical polish cannot apply.

To see what trivial edits alone achieve, I ran two baselines. Each was scored by optiwindnet's own PathFinder length and kept only if `validate_routeset` returned [].

| Starting set | Edit | Valid length (m) |
|---|---|---|
| 46020 (seed) | Re-tree each of its 25 groups with the optimal branched tree (all spanning trees × gateway choices), keeping the partition | 377839.5685 |
| 46020 (seed) | Additional hill-climb: swap or relocate turbines between neighbouring groups (8 nearest), each group re-treed | No further gain; stays 377839.5685 |
| 25155 | Same group re-treeing | No gain (378897.5658) |
| 25155 | Swap/relocate hill-climb | 378577.7332 |
| 25008 / 35902 | Group re-treeing hill-climb | 378897.5658 |

Two further checks:
- I recombined whole groups taken from all stored partitions (exact cover by CP-SAT). The best straight-line value is 375437.37. That is CPLEX's own partition, whose routed length is 378897.57, so recombination gives nothing better.
- The best trivial-edit result is 377839.5685 m. That set is itself shorter than every stored set. The object beats it by 811.64 m (0.215%), so the object beats what those edits alone give, as the rule requires for a seeded result.

## 6. Verdict

- The status was read successfully, and r26.10-v4 is still the latest version.
- No published route set for Sofia at capacity 4 (radial or branched, with 25 or fewer feeders) is shorter than or equal to 377027.9310 m. This holds across the current release, the previous release, DTU's 2025 datasets (checked under any name, orientation or mirroring), the thesis artifacts, the OptiWindNet repository and releases, the wes-2026-124 preprint, and the V3R1T4S repository and PRs.
- The object names its seed and is substantially different from it.
- The object strictly beats the best result I could get from trivial or local edits of the stored sets.

Limits of this review:
- Unpublished results cannot be ruled out.
- My trivial-edit baselines are bounded local searches, not exhaustive ones.
- Validity checks were done here only to confirm the object is what it claims. The full validity verdict belongs to the other panel members.

novelty: NEW. Strictly shorter than everything known, by 1559.3288 m (0.412%) against the best published set and by 811.64 m against the best trivial edit of it.

pass: true
