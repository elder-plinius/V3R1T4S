# Novelty review: Hornsea One.1_OSS, capacity 7, branched (claim-ho7)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

## 1. Status source (fetched once, no retries)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- Fetched 2026-11-07T14:53:03Z (UTC). HTTP status: 301. Body: `{"status": 301, "message": "Redirecting...", "location": "https://zenodo.org/api/records/23537067"}`. The "latest version" endpoint redirects to record 23537067 itself, so 23537067 is the latest version.
- I followed that redirect target once at 2026-11-07T14:53:14Z: https://zenodo.org/api/records/23537067 returned HTTP 200. Record id 23537067, publication_date 2026-10-21, updated 2026-10-21T15:29:56.915326+00:00. It has one file, optiwindnet-routesets-r26.10-v4.sqlite.xz (28,464,808 bytes, md5 85faffb2e13600b017f1b583b259edd7).
- The version listing (https://zenodo.org/api/records/23537067/versions) has two versions: 23537067 (2026-10-21, r26.10-v4) and 20053479 (2026-05-06, r26.05-v4). No newer release exists.
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz has sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a and md5 85faffb2e13600b017f1b583b259edd7, which matches the live Zenodo file.

## 2. Stored sets for the cell (r26.10-v4, nodeset 'Hornsea One.1_OSS', T=174, R=1, capacity 7)

| id | length (m) | feeders | creator | topology |
|---|---|---|---|---|
| 45791 | 408102.5795 | [26] | MILP.pyomo.cplex | radial |
| 2801 | 411304.2676 | [25] | MILP.pyomo.cplex | branched (relgap 3.46%, bound 393633.86) |
| 9637 | 414178.6097 | [25] | baselines.hgs | radial |
| 8924 | 419780.0637 | [25] | baselines.lkh | radial |

Neighbouring cells on the same nodeset:
- Capacity 6: best 450092.35 m. Any capacity-6 set is also valid at capacity 7, but it is longer, so it is not a competitor.
- Capacity 8: best 380296.05 m. These sets are not valid at capacity 7, so they are not a competitor.
- 'Hornsea One': the same 174 turbine positions, but with 3 substations. That is a different instance, because its substations are not congruent with the single substation here.
- Turbine positions: I compared every nodeset with T=174 in all databases by its sorted pairwise-distance invariant. Only 'Hornsea One.1_OSS' matches both the turbines and the substation. 'Hornsea One' (3 OSS) matches the turbines only. No relabelled, rotated or translated copy exists under another name.

## 3. The object

- object/segments.json: 195 segments. Recomputed sum of Euclidean segment lengths = 407209.0156 m, which matches object/routeset-packed.json (407209.01555364137).
- object/G.pickle passes optiwindnet 0.3.2 `validate_routeset` with an empty result `[]`.
- Feeders: [26]. That is not more than the 26 of the shortest stored set.
- Topology: maximum turbine degree 3, with 4 branch points.
- Margin: 893.5640 m (0.219%) shorter than id 45791, and 4095.25 m shorter than the best stored branched set, id 2801.
- I did not check border or obstacle containment, or crossings beyond the validator; those belong to the other panel reviews.

## 4. Relation to the named seed (id 45791) and to the trivial-edit classes

Comparison is on the topological turbine/substation edge sets, with detours removed via `S_from_G`:

| stored set | edges shared with the object (of 174) |
|---|---|
| 45791 | 170 |
| 2801 | 118 |
| 9637 | 155 |
| 8924 | 111 |

The object is the seed 45791 with exactly four edge exchanges. Each exchange, applied alone to 45791, gives a valid tree that respects capacity, and shortens it:

| out of 45791 | into object | straight-line change |
|---|---|---|
| (63,72) | (64,72) | -522.46 m |
| (111,112) | (106,111) | -162.99 m |
| (159,163) | (162,163) | -78.27 m |
| (169,170) | (167,169) | -124.11 m |

- Total straight-line change: -887.83 m.
- Detour overhead is 1233.29 m in the object against 1239.02 m in 45791 (-5.73 m).
- Together these give the full -893.56 m.

The claim names its seed (45791), as the rule requires.

None of the listed trivial-edit classes changes the topological edge set of 45791: deletion, restriction, a valid propagation rule, relabelling, symmetry, or a local numerical polish (of the detour geometry). Applied alone or combined, they cannot get below roughly 408102.58 m minus a detour polish. Even the whole 1239 m detour budget would not explain the result, since the object keeps 1233 m of detours. The 887.8 m gain comes entirely from four combinatorial re-attachments that turn the radial seed into a branched tree. That is the change the cell's topology (branched) allows and the radial seed could not make.

Caveat: these four moves are simple one-edge exchanges that a basic local search would find. The improvement is real but shallow. It is not covered by the listed trivial-edit classes, so under the stated rule it counts as new.

## 5. Literature and code search (last 24 months)

- **V3R1T4S (github.com/elder-plinius/V3R1T4S, main pushed 2026-11-06T20:24:58Z).**
  - TROPHY_CASE.md has no OptiWindNet or wind-cable entry.
  - known-knowns/optiwindnet-routesets-cable-routing-records/ does not exist on main or at the pinned commit f3b19b4 (HTTP 404). The tree has only known-unknowns/optimization-benchmarks/optiwindnet-routesets-cable-routing-records.md, which lists the target as open and names only Hornsea One.1_OSS capacity 8.
  - PRs and issues, all states: I listed 500 PRs and 39 issues and ran searches for "hornsea" and "optiwindnet". There are five OptiWindNet claim PRs (#962, #963, #964, #967, #968, all open). For Hornsea One.1_OSS they cover capacity 8 (#968, 377034.69 m) and capacity 10 (#967, 332729.34 m). No PR or issue covers capacity 7.
- **Zenodo 18864643 and 19798734** (paper "Flexible cable routing framework...", paperdb v3/v4 and MILP_model_comparison v3/v4; downloaded and scanned). Hornsea One.1_OSS appears there only at capacities 2-5. There is no capacity-7 set, and no congruent nodeset under another name.
- **Zenodo 20053479** (RouteSets r26.05-v4; downloaded and scanned). Its capacity-7 sets are identical to r26.10-v4 (45791, 2801, 9637, 8924), with the same lengths.
- **Zenodo 20140812** (thesis artifacts). optiwindnet_routesets.zip holds notebooks, scripts and figures over the RouteSets DB. data_driven_hybrid.zip holds ML models and id lists. Neither contains a route-set database or a per-instance Hornsea route set.
- **github.com/DTUWindEnergy/OptiWindNet** (main pushed 2026-10-19).
  - Releases v0.1.6 to v0.3.2 contain only wheel and sdist assets.
  - The repo tree holds 'Hornsea One.yaml', which is a location only.
  - Notebooks lo21_hgs, p03_detours_hgs_crossings, hi12_locations and lo12_locations use the 3-substation Hornsea One, a different instance, and give no capacity-7 route set for the 1_OSS variant.
  - A GitHub-wide code search for "Hornsea One" found no other cable-routing data.
- **Preprint wes-2026-124** (discussion since 2026-07-28, page updated 2026-11-06). It does not mention Hornsea One or report per-instance lengths.
- **Web searches** for "Hornsea One.1_OSS" and for OptiWindNet RouteSets improved solutions found no published route set for this instance.

Nothing published is shorter than 408102.5795 m for this instance at capacity 7.

## 6. Verdict

- The object is 407209.0156 m with feeders [26].
- That strictly beats every known route set for Hornsea One.1_OSS at capacity 7: the stored best 408102.5795 m (id 45791, radial) by 893.56 m (0.219%, far above 1e-6 relative), and the stored best branched set 411304.2676 m (id 2801).
- It is not a tie.
- It names its seed (45791) and beats what the listed trivial edits of that seed could give, through four branch-creating edge exchanges.
- I found no shorter set in DTU's earlier datasets, the OptiWindNet repository and releases, the preprint, or V3R1T4S PRs and issues.

Side note (not a novelty issue): the `misc` fields in object/routeset-packed.json (bound 406663.29, relgap ~1.7e-11, termination OPTIMAL, runtime 0.82 s) describe only the last pinned CP-SAT sub-solve. They are not a bound or optimality certificate for this route set, and the claim does not claim one.

novelty: PASS (strict improvement over everything known; seed named; more than trivial edits)
pass: true
