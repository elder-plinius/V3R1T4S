# Criterion skeptic report

context: target `optiwindnet-routesets-cable-routing-records`, run 2026-11-10-1803; claim = FULL success criterion for instance (nodeset "Noirmoutier", capacity 2), topology X = radial (hence also branched); checked 2026-11-11 with my own scripts in `panel/work-criterion/` (`check_own.py` without optiwindnet, `check_official.py` and `null_reroute.py` with optiwindnet 0.3.2), reading only the claim folder and the bank entry; `object/G.pickle` was not loaded; the Zenodo status was not re-fetched (no network use), so latest-ness rests on `status/zenodo-latest.json` as frozen.

confirmed_scope: For the OptiWindNet RouteSets r26.10-v4 instance (nodeset "Noirmoutier", 61 turbines, 1 substation, no obstacles; capacity 2), the route set in `object/routeset-packed.json` / `object/segments.json` is a radial network with 31 feeders, on the same turbine and substation coordinates, of total Euclidean length 150439.9933 m, which is 387.0468 m (0.2566%) shorter than the shortest of the four route sets stored for that instance (id 46244, radial, baselines.lkh, 150827.0401 m, 31 feeders), passes `validate_routeset` of optiwindnet 0.3.2 with no violations, and lies entirely inside the site border; nothing is established about optimality or any other instance.

## Clause-by-clause (all recomputed, none taken from the claim text)

| Clause | Result | Evidence |
|---|---|---|
| Instance of r26.10-v4, nodeset name without '!' | met | Nodeset row `Noirmoutier` exists (T=61, R=1, B=5, digest bcf6aba7...); 4 stored route sets at capacity 2. The 115 `!Noirmoutier!...` augmented nodesets are different rows and were not used. |
| Route set of topology X | met for radial and branched | Own decode of `edges`: 61 turbines each with one parent, no cycle, all reach root -1; turbine degrees: 31 of degree 1, 30 of degree 2, max 2; 30 strings of 2 turbines + 1 of 1 (sum 61, max load 2 = capacity). |
| Strictly shorter than EVERY stored set of X or more restrictive, by > 1e-6 relative | met | Stored (recomputed = stored length for all four): 46244 radial LKH 150827.0401; 27495 radial HGS 150985.2106; 36274 radial CPLEX 150985.2106; 27564 branched CPLEX 150985.2106. No row has a null topology. Claim 150439.9933: margin 387.0468 m, relative 2.566e-3 (about 2,566 times the 1e-6 threshold). Same comparison set minimum for X=radial (3 sets) and X=branched (4 sets); no tie at the minimum. |
| Feeders at EACH substation <= shortest such stored set's feeders_per_root | met | One substation; claim 31 (both as turbines whose parent is the root and as segments incident to the root); cap [31] from id 46244. 31 = ceil(61/2) is also the minimum possible. |
| Same nodeset | met, with a caveat | Every endpoint in `object/segments.json` equals the DB VertexC coordinate bitwise (max difference 0); all 61 turbines and the substation appear; `segments.json` edge set equals the packed `edges`; optiwindnet's digest check accepts the rebuild and rejects a wrong digest. Caveat: the two shipped JSON objects do not themselves carry the border polygon or a nodeset digest (binding is by name/handle and coordinates); the border is used by no route (C=0). |
| validate_routeset, no violations | met | G rebuilt from `object/routeset-packed.json` + DB nodeset: `[]` when declared radial and `[]` when declared branched (the validator only applies the degree<=2 test under a radial declaration, and the packed object declares "branched", so both were run). Controls: validator returns `[]` for all four stored sets; reports capacity/radial/crossing violations on an overloaded mutant; reports 10 crossings when the 12 detour nodes are removed. |
| Every segment inside border, outside obstacles | met | shapely: all 73 segments covered by the 5-vertex border polygon; minimum segment-to-border distance 875.8 m; the nodeset has no obstacles (constraint_groups = [5]). Own crossing check: no proper interior crossing, no T-touch, no route splitting a turbine's own links. |
| Length = Euclidean sum, and that is the value compared | met | 150439.9933339 m from `segments.json` coordinates, from packed edges + DB coordinates, and from the rebuilt G; equals the packed `length` field; no zero-length segment. |
| Release identity and latest-ness | met as far as the frozen file shows | `.xz` sha256 c78c8f3c...e3a (= bank), md5 85faffb2... (= the file checksum in `status/zenodo-latest.json`); record 23537067, published 2026-10-21, `relations.version[0].is_last = true`; DB totals 49,204 route sets / 13,954 instances match the release description. The status file carries no retrieval timestamp. |

## Null models and stretched definitions

- Re-routing null: re-running the package's detour router (PathFinder, 0.3.2) on each stored topology returns exactly the stored lengths (150827.0401, 150985.2106 x3), and on the claim's topology returns 150439.9933. The gain is therefore not a detour-router or package-version artefact; the claim's topology differs from the LKH set in 10 of 61 links and from the HGS/CPLEX sets in 4 of 61.
- Corridor stacking: 12 detour nodes sit on turbine positions (5 routes pass turbine 28, 2 pass turbine 29) and several cables share collinear runs (e.g. six along the 540 m from turbine 28 to the substation). This is the benchmark's own convention, not a stretch: the stored HGS/CPLEX sets do the same (11 detour nodes, 3 each on turbines 28 and 29), and the official validator accepts it.
- Where the gain comes from: the claim's straight-line (no-detour) objective is 150069.158 m, which is worse than the stored HGS/CPLEX topology's 149999.638 m; it wins only on detoured length (detour overhead 0.25% vs 0.66%). The criterion compares detoured lengths, so this is legitimate, but it should be described that way.
- No contradiction with stored bounds: the stored MILP bound 149573.25 m (on the straight-line objective) is below the claim's objective.
- Partial win p2 does not apply (a radial MILP bound exists in the release, id 36274) and is not claimed.

## Wording and metadata defects (do not change the verdict; fix before any publication)

1. Misleading metadata in `object/routeset-packed.json`: `misc.termination = "OPTIMAL"`, `misc.relgap = 2.6e-11`, `misc.bound = 150069.158`, `solver_details.strategy = "OPTIMAL"`, `runtime = 0.0536` s, `creator = "MILP.ortools.cp_sat"`, `warmstart = "baselines.lkh"`. These describe the last windowed sub-solve with most links pinned, not the instance. Read as a release-style record they assert proven optimality, which is false: three stored feasible radial 31-feeder sets have straight-line objective 149999.638 m, below the stated "bound" of 150069.158 m. The true runtime was 37 minutes per `CLAIM.md`. `CLAIM.md` itself says optimality is not claimed, so the claim text is not overstated, but the packed object is.
2. Inconsistent topology label: `CLAIM.md` and `object/segments.json` say radial; `criterion.txt` and `REPRODUCE.md` step 4 say X = branched; the packed object declares `"topology": "branched"`. Both hold, but one label should be used (radial is the stronger and verified one).
3. `handle` is "Noirmoutier" in the packed object and "noirmoutier" in the release rows.
4. `CLAIM.md` wording "strictly shorter than every stored route set for that instance of any topology" is accurate (four sets). The margin is small (0.257%); no wider reading (other capacities, optimality, method merit) is supported.

## Verdict

Every clause of the full success criterion is literally met for (Noirmoutier, capacity 2) with X = radial, and the win is not explained by the re-routing null model. The claim folder was not modified (no `__pycache__`).

pass: true
