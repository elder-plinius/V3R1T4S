# Novelty review: Race Bank.1_OSS, capacity 3, radial (also counts for branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

Claim folder files are named relative to the claim folder. Scripts, downloads and outputs are in panel/work-novelty/ (scripts/, dl_*/, ref/).

## 1. Status source (fetched once, no retries)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- Time: 2026-11-09T09:14:17Z. HTTP 301, body `{"status": 301, "message": "Redirecting...", "location": "https://zenodo.org/api/records/23537067"}`, so the latest version is record 23537067.
- I followed that redirect once at 2026-11-09T09:14:32Z: https://zenodo.org/api/records/23537067 returned HTTP 200. Record id 23537067, publication_date 2026-10-21, modified 2026-10-21T15:29:56.915326+00:00, one file `optiwindnet-routesets-r26.10-v4.sqlite.xz`, 28464808 bytes, md5 85faffb2e13600b017f1b583b259edd7.
- The version list (`/api/records/23537067/versions`) shows only 23537067 (r26.10-v4, 2026-10-21) and 20053479 (r26.05-v4, 2026-05-06). No newer release exists.
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz has sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a and md5 85faffb2e13600b017f1b583b259edd7. This matches the live Zenodo file, so the claim's reference is the current table.

## 2. Stored route sets for the cell (r26.10-v4, nodeset 'Race Bank.1_OSS', T=91, R=1, capacity 3)

| id | creator | topology | length (m) | straight objective | feeders |
|---|---|---|---|---|---|
| 45770 | MILP.pyomo.cplex (radial, min_plus1, 2026-05-02) | radial | 155036.8793 | 153805.46 (bound 153293.23, relgap 0.33%) | [31] |
| 9504 | baselines.hgs (2024-06-19) | radial | 155036.8793 | 153805.46 | [31] |
| 8812 | baselines.lkh (2024-06-19) | radial | 155172.6133 | 154849.46 | [31] |
| 2743 | MILP.pyomo.cplex (branched, unlimited, 2024-01-12) | branched | 156071.6528 | 154121.46 (bound 153480.92) | [31] |

The best stored set for both X = radial and X = branched is 155036.8793 m with 31 feeders (ids 45770 and 9504, which give identical networks).

## 3. The object

I rebuilt it in optiwindnet 0.3.2 from object/routeset-packed.json against the release's nodeset row. I did not load the pickle.

- Length: 153796.9412 m. This matches the recomputed sum over the 107 segments in object/segments.json, 153796.94115396673.
- validate_routeset returns [].
- Maximum turbine degree is 2, so the set is radial. The substation has 31 feeders, which is within the cap of [31].
- It is shorter than the best stored set by 1239.9381 m (0.800% relative), well above the 1e-6 threshold.

## 4. Is it more than a trivial edit of a published object?

The claim names its seed as stored set 45770 (radial CPLEX). I compared the turbine-level topology of each stored set with the object's on the same coordinates, using S_from_G and the symmetric difference of link sets:

| stored set | links that differ from the object (out of 91) |
|---|---|
| 45770 | 14 |
| 9504 | 14 |
| 8812 | 35 |
| 2743 | 43 |

- **Deletion, restriction, relabelling, symmetry.** These do not apply. Every stored set uses the identical nodeset with the same 91 turbines and the same substation, so relabelling and mirroring are excluded by comparing coordinates directly. At least 14 links are rewired relative to the closest stored set.
- **Valid propagation from neighbouring cells:**
  - The capacity-2 sets are valid for capacity 3, but they are much longer: the best is 207371.90 m (id 8811).
  - Capacity-4 sets (best 127865.42 m) are not valid at capacity 3.
  - The 'Race Bank' nodeset (same 91 turbines but R=2, with both substations at least 2.38 km from the .1_OSS substation; capacity 3, 109178.41 m, id 231) is a different instance. Its sets cannot be converted to a one-substation set by any trivial edit.
- **Local numerical polish (re-running PathFinder).** Re-routing the detours of each stored topology with optiwindnet 0.3.2 PathFinder leaves every length unchanged: 45770 and 9504 stay at 155036.8793, 8812 at 155172.6133, 2743 at 156071.6528. Detour re-routing alone therefore gives no gain.
- **Where the gain comes from.** It is real combinatorial rewiring:
  - The straight-line objective falls from 153805.46 (seed) to 153313.91 (object). This sits just above the 2026 radial MILP lower bound of 153293.23, so it is consistent with that bound.
  - Detour length falls from about 1231 m to about 483 m.
- **Seed disclosure.** The claim names its seed (45770) and beats what trivial edits of it give, as shown above.

Side observation, not affecting novelty: the object's straight-line objective (153313.91) is below the bound stored with the 2024 branched run 2743 (153480.92). That bound came from an older model and package version, and its stored objective differs from the straight-line length recomputed now (155313.97). Cross-version bounds are indicative only, as the target statement itself says. The object is consistent with the 2026 radial bound.

## 5. Search for other published sets for this instance (last 24 months, plus older DTU datasets)

**Earlier DTU Zenodo datasets.** I downloaded each into its own directory and read it only as data.

- Records searched:
  - r26.05-v4 (record 20053479), the version cited by wes-2026-124.
  - paperdb.v3 and MILP_model_comparison.v3 (record 18864643).
  - paperdb.v4 and MILP_model_comparison.v4 (record 19798734).
- Method: I matched every T=91 nodeset geometrically (sorted pairwise turbine distances with scale normalisation, which is invariant to translation, rotation, mirroring and scale), then checked the substation's distances to the turbines.
- Results, which are the only matches:
  - r26.05: 'Race Bank.1_OSS' with the same 4 capacity-3 sets as r26.10 (best 155036.8793).
  - paperdb v3 and v4: 'Race Bank.1_OSS' with ids 9504 (155036.8793) and 2743 (156071.6528).
  - MILP_model_comparison v3 and v4: no match.
- Older augmented names ('!Race Bank!…') use other turbine counts or layouts. Among the r26.10 'Race Bank' nodesets, only 'Race Bank.1_OSS' and 'Race Bank' (R=2) contain the 91 turbine positions.
- No stored set anywhere is shorter than 155036.8793.

**Thesis artifacts (record 20140812).** optiwindnet_routesets.zip and data_driven_hybrid.zip contain notebooks, figures, code and models but no route sets. Text search finds no Race Bank instance results.

**OptiWindNet GitHub (DTUWindEnergy/OptiWindNet).**
- Releases v0.1.6 to v0.3.2 (latest 2026-10-12) carry only wheel and sdist assets.
- The repository tree's only route-set data is Cazzaro and Taylor paper route sets (docs/notebooks/data/*.pkl).
- The docs CPLEX example solves 'Race Bank' (R=2) at capacity 5, which is a different instance.

**Preprint wes-2026-124.** The landing page (fetched 2026-11-09) gives aggregate statistics only, with no Race Bank or per-instance lengths. It links the r26.05 dataset and the thesis record, both checked above.

**Web literature search.** Searches for Race Bank cable routing, OptiWindNet Race Bank and 91-turbine capacity-3 benchmarks found no published route set or length for this instance.

**V3R1T4S repository (elder-plinius/V3R1T4S).**
- TROPHY_CASE.md: no mention of OptiWindNet, Race Bank or cable routing.
- known-knowns/: no OptiWindNet entry. The target exists only at known-unknowns/optimization-benchmarks/optiwindnet-routesets-cable-routing-records.md, last changed in f3b19b4.
- Pull requests: I reviewed 442 open and 538 closed. The OptiWindNet claims concern London Array.1_OSS, Hornsea Two West, Hornsea One.1_OSS, Yi-2019.1_OSS and Cazzaro-2022G-210.solid.1_OSS. None concerns Race Bank, and searches of PRs and issues for "Race Bank" return nothing.
- Code search for "Race Bank" in the repository returns 0 hits.

## 6. Verdict

The object is a valid radial capacity-3 route set for Race Bank.1_OSS at 153796.9412 m with 31 feeders.

- **Beats every known set.** It is strictly shorter, by 1239.94 m (0.80%), than every stored set of any topology in the current release (r26.10-v4, confirmed latest on 2026-11-09), in the previous release, in the earlier DTU datasets and in any public source found. It also beats the best stored branched set (156071.6528) by 2274.71 m.
- **More than a trivial edit.** It differs from its named seed (45770) in 14 of 91 links, and detour re-routing of any stored set gives no improvement.
- **No tie.** It is not a tie with any known set.

novelty: CONFIRMED for Race Bank.1_OSS, capacity 3, X = radial (and X = branched)

pass: true
