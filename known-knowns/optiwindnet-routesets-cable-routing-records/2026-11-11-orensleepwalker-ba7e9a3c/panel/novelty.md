# Novelty review: Noirmoutier, capacity 2 (OptiWindNet RouteSets r26.10-v4)

context: fresh-context novelty skeptic of a three-person panel; inputs were the frozen claim folder (CLAIM.md, REPRODUCE.md, criterion.txt, status/zenodo-latest.json, references/optiwindnet-routesets-r26.10-v4.sqlite.xz, object/segments.json, object/routeset-packed.json; object/G.pickle was not loaded) plus the public web. Scratch work and downloaded files are in panel/work-novelty/. Checks ran 2026-11-11 16:27-16:40 UTC with optiwindnet 0.3.2.

## 1. Status source (fetched once)

- URL: https://zenodo.org/api/records/23537067/versions/latest, requested 2026-11-11T16:27:10Z. The API answered HTTP 301 with `location: https://zenodo.org/api/records/23537067`; following that redirect (16:27:16Z) returned HTTP 200.
- Value: the latest version of concept 20053478 is still record 23537067, version "26.10-v4", publication date 2026-10-21, single file optiwindnet-routesets-r26.10-v4.sqlite.xz, 28,464,808 bytes, md5 85faffb2e13600b017f1b583b259edd7. `relations.version[0].is_last = true`.
- The claim's copy references/optiwindnet-routesets-r26.10-v4.sqlite.xz has the same md5 and the sha256 stated in CLAIM.md (c78c8f3c...05e3a). Compared with status/zenodo-latest.json the live record differs only in bookkeeping (revision 4 -> 6, modified 2026-11-11T15:08:11Z, a `version` metadata field, view counters); the file and its checksum are unchanged. The table has not moved.

## 2. What is stored for this cell and its neighbours

From the release database (nodeset "Noirmoutier", T=61, R=1, border of 5 vertices, no obstacles), capacity 2:

| id | creator | topology | length (m) | feeders | straight-line objective | MILP bound |
|---|---|---|---|---|---|---|
| 46244 | baselines.lkh | radial | 150827.0401 | [31] | 150773.86 | - |
| 27495 | baselines.hgs | radial | 150985.2106 | [31] | 149999.64 | - |
| 27564 | MILP.pyomo.cplex | branched | 150985.2106 | [31] | 149999.64 | 149573.25 |
| 36274 | MILP.pyomo.cplex | radial | 150985.2106 | [31] | 149999.64 | 149573.25 |

These are all the stored sets for the instance; the best is 150827.0401 m, as CLAIM.md says. Capacity 3 (neighbouring cell) best is 114428.29 m with 21 feeders; capacity-3 sets are not feasible at capacity 2 and share only 25-30 of 61 links with the object.

The object: 150439.9933 m recomputed three ways (sum over object/segments.json, the graph rebuilt from object/routeset-packed.json, and a fresh PathFinder run on its topology), 31 feeders, maximum turbine degree 2, `validate_routeset` returns [] on the rebuilt graph, and the 73 segments of object/segments.json are exactly the rebuilt graph's segments. Margin over the best stored set: 387.0468 m = 0.2566 %, far above the 1e-6 relative threshold. The length is above the stored MILP bound (149573.25) and above the crossing-free-agnostic matching bound I computed for 31 feeders (149999.64, equal to the stored HGS/CPLEX objective), so it contradicts no bound.

## 3. Is the object a trivial edit of a published one?

Logical links (detour vertices contracted), object versus stored sets:

- versus the named seed 46244 (LKH): 51 links common, 10 differ on each side; 6 of 31 strings regrouped, 4 feeder links differ.
- versus 27495 / 27564 / 36274 (HGS and both CPLEX sets, which are one and the same network): 57 links common, 4 differ on each side. Object-only links (-1,40), (16,28), (29,36), (40,41); stored-only (-1,41), (16,29), (28,40), (36,41). That is a cyclic re-pairing of three strings, {28,40},{36,41},{16,29} -> {40,41},{16,28},{29,36}. In addition seven strings with unchanged membership are routed with different detours.
- Two object links, (16,28) and (29,36), and two of its strings appear in no stored capacity-2 set, so the object is not a recombination of stored strings.

So the object is nearer to the HGS/CPLEX network than to the seed CLAIM.md names. CLAIM.md does name the seed it started from, and the comparison below covers both.

What the listed trivial edits give, tested directly (panel/work-novelty/a3.py):

- Local polish of the detours: re-running PathFinder 0.3.2 on each stored topology returns exactly the stored lengths (150985.2106 and 150827.0401). The seed's straight-line objective alone (150773.86) already exceeds the object's full length, so no re-routing of the seed's detours can reach it.
- Relabelling (which turbine of a string takes the feeder): greedy single flips from 27495 and from 46244, 30 evaluations each, no improvement.
- Beyond the kit's list, as a shallowness probe: every single two-string re-pairing of 27495 and of 46244 within +2500 m straight-line cost (313 and 312 routed candidates) gives no valid set shorter than the stored one. The improvement needs the three-string move together with the detour changes it enables.
- Deletion, restriction, symmetry: not applicable (same nodeset, all 61 turbines; no other stored nodeset is a rotation, reflection or scaling of this layout: the closest other 61-turbine nodeset differs by 2.7 % in normalised pairwise-distance signature).

The object is therefore a small but genuine combinatorial change (3 of 31 strings re-paired, straight-line objective +69.5 m, detour overhead down from 0.66 % to 0.25 %) and beats everything the trivial edits give by the full 387 m.

## 4. Prior art search (last 24 months)

- Previous release r26.05-v4 (Zenodo 20053479, 2026-05-06, downloaded): same four capacity-2 sets, same ids and lengths. Nothing shorter was ever stored and dropped.
- Zenodo 18864643 and 19798734 (paperdb v3/v4 and MILP_model_comparison v3/v4, EJOR "Flexible cable routing framework" data, downloaded and scanned): no nodeset named Noirmoutier, Yeu or Vendee, and none of the 102 nodesets with 61 turbines is similar to this layout under rotation, reflection or scaling.
- Zenodo 20140812 (PhD thesis artifacts, both zip archives read): notebooks and code only, no mention of the site.
- OptiWindNet repository (github.com/DTUWindEnergy/OptiWindNet, mirror of the DTU GitLab; last push 2026-10-19): 8 releases up to v0.3.2, assets are only wheels and sdists; the tree holds the site as location data (optiwindnet/data/Noirmoutier.osm.pbf, added per CHANGELOG) and uses it in tests at capacity 8 only; no stored route set for it in the docs or test pickles (byte search). No pull requests, 4 issues, none on this site. GitLab project has no releases. The one recently pushed fork is identical to upstream.
- Preprint wes-2026-124 (landing page and PDF fetched): describes the dataset; no mention of the site and no improved solutions.
- Crossref and web searches for the site with cable routing, and for work on the RouteSets benchmark (2024-11 onward): general cable-routing papers only (e.g. 10.1016/j.ejor.2025.07.069, 10.1088/1742-6596/3346/1/012032, 10.5753/jbcs.2026.7304, 10.1007/s12667-026-00827-x); none reports a Noirmoutier capacity-2 network.
- github.com/elder-plinius/V3R1T4S (read 2026-11-11T16:32Z): all 1009 pull requests, open and closed, listed; 21 concern optiwindnet-routesets-cable-routing-records (Hornsea One.1_OSS, Hornsea Two West, London Array.1_OSS, Sofia, Race Bank.1_OSS, Yi-2019.1_OSS, Cazzaro-2022G-210.solid.1_OSS), all open, none for Noirmoutier at any capacity (title and body search, plus the issue search API: 0 hits). TROPHY_CASE.md has no entry for this target; known-knowns/ (6176 paths) has no directory for it; the bank entry known-unknowns/optimization-benchmarks/optiwindnet-routesets-cable-routing-records.md lists no solved cells.

No published or filed route set for Noirmoutier at capacity 2 is shorter than, or equal to, 150439.9933 m.

## 5. Caveats

- The margin is small (0.26 %) and the object sits three strings away from the stored HGS/CPLEX network. At capacity 2 the problem is close to a matching problem and the stored sets are already optimal for the straight-line model; the gain comes from accounting for detours. This is a legitimate strict improvement under the criterion, not a method result, and CLAIM.md claims no more.
- Border containment and the independent checker are the other reviewers' remit; here only the official validator and the length recomputation were run.
- The status endpoint answered with a redirect to the record itself rather than a body; the redirect was followed once and is reported above.

novelty: strictly shorter than every known route set for the cell; not a trivial edit of a published one
pass: true
