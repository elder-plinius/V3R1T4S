# Novelty review: Yi-2019.1_OSS, capacity 12, radial, 125848.9321 m

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

## Status source (one fetch, no retries)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- Fetched 2026-11-07T16:20:56Z. HTTP 301, body `{"status": 301, "message": "Redirecting...", "location": "https://zenodo.org/api/records/23537067"}`. The latest version is therefore record 23537067 itself.
- I followed that redirect once at 2026-11-07T16:21:10Z (https://zenodo.org/api/records/23537067). It returned HTTP 200 with id 23537067, publication_date 2026-10-21, created 2026-10-21T15:29:56Z, and one file, optiwindnet-routesets-r26.10-v4.sqlite.xz (28,464,808 bytes, md5 85faffb2e13600b017f1b583b259edd7).
- A listing of the concept's versions (conceptrecid 20053478) shows only 23537067 (r26.10-v4, 2026-10-21) and 20053479 (r26.05-v4, 2026-05-06). No newer release exists.
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz has sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, matching the claim.

## The object (independent recomputation)

- Length from object/segments.json, summed as Euclidean segment lengths: 125848.9321 m. G rebuilt from object/routeset-packed.json with optiwindnet 0.3.2 gives the same total.
- validate_routeset returns []. Maximum turbine degree in S_from_G is 2, so the set is radial. It uses 10 feeders. Its 10 strings have sizes 11 and nine of 12.
- Border and obstacle check (shapely): all 133 segments lie inside the border. Two segments (272-273 at 91.79 m and 276-277 at 219.02 m) overlap obstacles 8 and 16 only along their edges. Each has zero length inside the obstacle shrunk by 1 mm, so these are contour segments running along an edge, not segments through an obstacle.

## How radial vs branched was decided

Radial means the maximum turbine degree of S_from_G(G_from_routeset(rs)) is 2. I calibrated this on the labelled sets in the reference database. For this instance, 21567 (label radial) gives degree 2 and 21894 (label branched) gives degree 3. On the labelled augmented instances the test agreed with the label in every printed case. For unlabelled older files I applied this degree test instead of a label.

## Published radial sets for this cell and nearby cells

| source | set | topology (degree test) | length (m) | feeders | beats claim? |
|---|---|---|---|---|---|
| Zenodo 23537067, r26.10-v4 (reference) | 21567 baselines.hgs | radial (2) | 126034.6715 | [10] | no, claim shorter by 185.7394 m (0.147 %) |
| Zenodo 23537067 | 21894 MILP.pyomo.cplex | branched (3) | 121874.5797 | [11] | not radial; not claimed against |
| Zenodo 20053479, r26.05-v4 | 21567 / 21894 | radial / branched | 126034.6715 / 121874.5797 | [10] / [11] | identical to r26.10 |
| Zenodo 19798734, paperdb.v4 (also 18864643 paperdb.v3, migrated with optiwindnet.db.migrate) | 21567 baselines.hgs | **branched (3)**, unlabelled | 125938.2590 | [10] | not radial, and still 89.33 m longer than the claim |
| same, both versions | 21894 | branched (3) | 121874.5797 | [11] | not radial |
| MILP_model_comparison v3 and v4 (18864643, 19798734) | none | - | - | - | this nodeset is absent |
| Zenodo 20140812 (thesis artifacts) | none | - | - | - | notebooks and models only, no route sets, no mention of Yi-2019 |
| r26.10, all capacities <= 12 on this nodeset (a lower-capacity radial set stays valid at 12) | shortest is 21567 | radial | 126034.6715 | | no |
| next shortest radial sets: 40662 (cap 10, MILP radial), 21564 (cap 11), 21588 (cap 10) | | radial | 133766.02, 135339.38, 135448.64 | | no |
| V3R1T4S PR #964 (open), capacity 11 radial claim on this site | | radial | 129717.3657 | | no (valid at capacity 12 by restriction but longer) |
| Yi-2019.solid.1_OSS (nearby nodeset: same border, obstacles removed) | 25092 baselines.hgs | radial (2) | 123007.1651 | [12] | not a comparator: 12 feeders exceed the cap of 10, and 5 of its 124 segments violate the 1_OSS obstacles |
| OptiWindNet docs notebook p04_yi_2019 (GitHub DTUWindEnergy/OptiWindNet) | Yi-2019 with 2 substations, capacity 6 only | | 138025 (radial, cap 6) | 10+10 | different instance |
| Yi, Scutariu and Smith 2019 (IET RPG 13:1990), lengths as quoted in the OptiWindNet docs | original 2-OSS design | | radial 162300, branched 154600 | | different instance, and much longer |

Other sources searched:
- OptiWindNet GitHub releases v0.1.6 through v0.3.2 (2026-01 to 2026-10). The assets are wheels and sdists only. The v0.3.2 sdist holds layout files such as Yi-2019.yaml and no route sets.
- Preprint wes-2026-124 (posted 2026-07-28; RC1 2026-09-03; discussion open until 2026-11-18). It reports no per-instance lengths for Yi-2019, and its review comment reports no improved sets.
- V3R1T4S on GitHub: TROPHY_CASE.md (main) has no OptiWindNet entry. known-knowns/optiwindnet-routesets-cable-routing-records/ does not exist on main. The bank entry exists only as known-unknowns/optimization-benchmarks/optiwindnet-routesets-cable-routing-records.md at the pinned commit.
- V3R1T4S PRs (934 listed, open and closed) and issues (39): the only Yi-2019 item is PR #964, which is capacity 11.
- A web search for 2025-2026 literature using this 119-turbine site found no shorter radial set.

## Trivial-edit analysis

Turbine-level, the object agrees with the stored radial best 21567 on 115 of 119 edges. Eight of its 10 strings have the same turbine sets.

The 4 differing edges are:
- in the claim only: (-1,27), (10,27), (11,12), (11,28)
- in 21567 only: (-1,11), (10,11), (12,27), (27,28)

So the object is 21567 with turbines 11 and 27 swapping places in two adjacent strings. Turbine 27 becomes the feeder head before 10, and turbine 11 sits between 12 and 28. This is one 1-1 exchange (swap) local-search move from the published set. The claim's provenance says it came from an independent HGS run (seed 101, 240 s), not from a seed taken from 21567.

Checked against the kit's trivial edits:
- **Deletion and restriction** cannot shorten a set that already covers every turbine.
- **No valid propagation rule** or capacity restriction gives it, since every radial set at capacity <= 12 is longer.
- **Relabelling and symmetry**: swapping the labels 11 and 27 is not a symmetry of the instance. The turbines sit at different fixed coordinates, so the cable geometry changes and the length drops by 185.74 m. A relabelling that preserves the instance leaves length unchanged.
- **Local numerical polish**: none is possible, because turbine coordinates are fixed and the change is combinatorial.

The object is therefore not obtainable from any published radial set by the listed edits alone. Within the listed edits, the best known radial value stays at 126034.6715 m.

The improvement is small and local: one swap away from the stored HGS result, a 0.147 % margin, with the same feeder count of 10. That shows the stored HGS baseline was not 1-1-swap-optimal, but it does not make the object a trivial edit as the kit defines one.

## Verdict

- The object is a valid radial route set: validator clean, inside the border, outside obstacle interiors, 10 feeders, no more than the 10 of the shortest stored radial set.
- At 125848.9321 m it strictly beats every published radial set I found for this cell and the cells around it:
  - the stored radial best 126034.6715 m, by 185.7394 m, a relative margin of 1.47e-3, well above 1e-6;
  - every earlier DTU dataset (the shortest one there, 125938.2590 m, is branched in any case);
  - PR #964, at 129717.37 m;
  - the literature.
- It is not shorter than the branched best (121874.5797 m), and it is not claimed against it.
- It is not a tie.

novelty: NEW (radial, Yi-2019.1_OSS, capacity 12; strictly beats every known radial set; the difference from the stored best is a single two-turbine exchange, disclosed above)

pass: true
