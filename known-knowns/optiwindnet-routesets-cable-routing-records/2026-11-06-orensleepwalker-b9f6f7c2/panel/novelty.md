# Novelty skeptic report: claim-ho8 (OptiWindNet RouteSets, Hornsea One.1_OSS, capacity 8, branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

## 1. Status source (fetched once, no retries)
- URL: https://zenodo.org/api/records/23537067/versions/latest (curl -L, redirected to https://zenodo.org/api/records/23537067)
- HTTP status: 200
- Time (UTC): request started 2026-11-06T16:06:46Z, finished 2026-11-06T16:06:47Z
- Latest record id: 23537067 (DOI 10.5281/zenodo.23537067, concept 20053478), `versions.is_last = true`, index 1 of the new-style record; publication_date 2026-10-21, modified 2026-10-21T15:29:56Z
- Only file: optiwindnet-routesets-r26.10-v4.sqlite.xz, md5 85faffb2e13600b017f1b583b259edd7, 28,464,808 bytes. The claim folder's references/optiwindnet-routesets-r26.10-v4.sqlite.xz has the same md5 and sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, as stated. So the reference is the current latest release, and no newer version has replaced the table.
- The versions list (https://zenodo.org/api/records/23537067/versions) shows only 23537067 (r26.10-v4, 2026-10-21) and 20053479 (r26.05-v4, 2026-05-06).

## 2. Stored sets for the instance (from the reference DB, read-only copy in my work folder)
Nodeset 'Hornsea One.1_OSS' (no '!' prefix): T=174, R=1, B=25. Capacity 8:

| id | solver | topology | length (m) | feeders | misc.objective (straight) |
|---|---|---|---|---|---|
| 45794 | pyomo.cplex | radial | 380296.0542 | [22] | 379332.04 |
| 2800 | pyomo.cplex | branched | 381105.3514 | [22] | 378439.66 (bound 362862.42) |
| 9636 | HGS-CVRP | radial | 383497.6637 | [22] | 380561.61 |
| 8923 | LKH-3 | radial | 385884.6735 | [22] | 385093.92 |

These match CLAIM.md exactly. The previous release r26.05-v4 (downloaded from Zenodo 20053479, md5 38d4b0e9...fd7da as listed) holds the same four sets with the same lengths, so it has no shorter set.

## 3. The claimed object
- object/segments.json: 188 segments. The Euclidean sum I recomputed is 377034.6925 m. Every endpoint is a vertex of the stored nodeset (0 mismatches).
- I rebuilt object/routeset-packed.json with optiwindnet 0.3.2 TerseLinks on the stored nodeset (no pickle loaded). G.size(length) = 377034.6925, which matches.
- Contracted turbine tree: 174 edges, root degree 22 (= cap [22] of id 45794), max turbine degree 3 (branched). The 22 subtrees have sizes 21x8 + 1x6 = 174, all <= 8.
- Margin over the best stored set (id 45794): 3261.36 m (0.858%), far above 1e-6 relative.
- I did not re-run validate_routeset or the border/obstacle containment check. Those belong to the other panel roles. My judgement here assumes they pass.

## 4. Trivial-edit / seeding analysis
CLAIM.md names the seed as stored branched set id 2800 (MILP.pyomo.cplex). It does name it.
- Edit distance from the seed: 22 of the 174 contracted turbine-tree edges differ (22 removed, 22 added), touching 41 turbines. The changed turbines span 29.6 km x 13.5 km of a 38.1 km x 17.6 km site, so the changes are many reassignments across the whole site, not one local fix. Against the other stored sets: 56 edges differ vs 45794, 58 vs 9636, 64 vs 8923.
- Detour / re-routing polish: this is the only "local numerical polish" available, because vertex positions are fixed. Re-routing a topology can at best remove its detours, so the straight-line length of a topology is a lower bound for any re-routing of it. The smallest straight-line length among stored capacity-8 topologies is 378439.66 m (id 2800, misc.objective; my own contraction gives 378793.71). That is above the claimed detour-included length of 377034.69 m. So no detour polish of any stored set, alone or combined, reaches the claim. (The claim's own straight-line objective is 376712.81 m.)
- Valid propagation rule: any capacity <= 7 set is feasible at capacity 8. The best of those is 408102.58 m (id 45791, cap 7), which is far worse. Capacity >= 9 sets are not feasible at capacity 8.
- Deletion/restriction from neighbouring nodesets: I checked every nodeset in the DB for turbine-coordinate overlap. Only 'Hornsea One' (T=174, R=3) contains all 174 turbines, and its three substations are at different locations from the single 1_OSS substation, so its sets do not carry over. Its stored cap-8 branched set (264150.76 m, feeders [7,7,8]) belongs to a different instance with three roots. No augmented '!Hornsea One.1_OSS!...' nodeset is a superset (T = 56-173), so deleting turbines cannot produce the 174-turbine object.
- Relabelling/symmetry: the geometry is fixed, so these cannot change length.
- Conclusion: the object is a genuine re-optimisation (CP-SAT large-neighbourhood search) seeded from id 2800, which it names. It beats everything the listed edits give, including the lower bound for any polish of any stored topology.

## 5. Literature / code / repo search (last 24 months)
- V3R1T4S (github.com/elder-plinius/V3R1T4S, main pushed 2026-11-05T18:59:11Z; fetched via GitHub REST API 2026-11-06 ~16:08Z):
  - TROPHY_CASE.md has no OptiWindNet or Hornsea entry.
  - known-knowns/ has no optiwindnet-routesets-cable-routing-records directory (404; the known-knowns listing does not include it). The target exists only as known-unknowns/optimization-benchmarks/optiwindnet-routesets-cable-routing-records.md, which lists Hornsea One.1_OSS cap 8 (380,296.05 m) as open.
  - Issues/PRs: I scanned all 964 (open and closed) for optiwindnet/hornsea/routeset. Only three PRs match, all open (#962, #963 Cazzaro-2022G-210.solid.1_OSS cap 6/7 radial; #964 Yi-2019.1_OSS cap 11 radial). None is about Hornsea One.1_OSS cap 8.
  - The full repo tree (6796 entries, not truncated) has no other optiwindnet/Hornsea files.
- OptiWindNet code: GitHub mirror DTUWindEnergy/OptiWindNet. Releases v0.1.6 to v0.3.2 (latest 2026-10-12) carry only wheel/sdist assets, with no route-set files. The repo tree has only Hornsea input data (Hornsea One.yaml, Hornsea Two West.yaml, Hornsea 2.osm.pbf). DTU GitLab returns no releases. PyPI latest is 0.3.2.
- DTU papers/artifacts: preprint wes-2026-124 (landing page: discussion open to 18 Nov 2026; only RC1, with no Hornsea numbers; links dataset 10.5281/zenodo.20053479 and code 10.5281/zenodo.20140812). Zenodo 20140812, optiwindnet_routesets.zip, contains only analysis notebooks, SVGs and db_access.py, and does not mention Hornsea.
- Web searches ("Hornsea One.1_OSS"; Hornsea One inter-array cable length, MILP/branched 2025-2026; LNS/CP-SAT cable routing 2026) found no published Hornsea One single-OSS capacity-8 route set or length below 380296.05 m.

## 6. Verdict
The claimed 377034.6925 m strictly beats every known route set for (Hornsea One.1_OSS, capacity 8) of branched or more restrictive topology: the stored minimum is 380296.0542 m (id 45794), it beats it by 0.858%, and it uses the same 22 feeders. It is not reachable by trivial edits of any published object. It names its seed (id 2800) and beats the lower bound for any polish of that seed by more than 1.4 km. I found no shorter published set in the latest Zenodo release, the earlier release, the V3R1T4S repo (trophy case, known-knowns, PRs/issues), OptiWindNet code and releases, or the literature. This verdict is on novelty only and depends on the validator and containment checks passing in the other panel roles.

novelty: NEW (strictly beats all known; not a trivial edit of the named seed id 2800)
pass: true
