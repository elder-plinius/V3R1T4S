# Novelty review: OptiWindNet RouteSets r26.10-v4, Hornsea One.1_OSS, capacity 12, branched

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

Claim under review (CLAIM.md): a branched route set (object/) for nodeset `Hornsea One.1_OSS` (174 turbines, 1 substation, 25 border vertices, no obstacles) at capacity 12. Claimed total length is 307472.1191 m with 15 feeders. The claimed seed is stored set id 45373 (radial, MILP.pyomo.cplex, 309220.7062 m, feeders [15]).

## 1. Status source (fetched once, no retries)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- Time: 2026-11-07T09:06:25Z (UTC)
- Result: HTTP 301 with body `{"status": 301, "message": "Redirecting...", "location": "https://zenodo.org/api/records/23537067"}`. So the latest version of the concept is record 23537067 itself.
- I requested the redirect target once, at 2026-11-07T09:06:34Z. This was the next step of the same lookup, not a retry: https://zenodo.org/api/records/23537067 returned HTTP 200.
  - Latest record id: 23537067
  - publication_date: 2026-10-21
  - modified: 2026-10-21T15:29:56.915326+00:00
  - Single file: `optiwindnet-routesets-r26.10-v4.sqlite.xz`, 28464808 bytes, md5 85faffb2e13600b017f1b583b259edd7
- The local copy, references/optiwindnet-routesets-r26.10-v4.sqlite.xz, matches on both hashes:
  - md5 85faffb2e13600b017f1b583b259edd7
  - sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, as stated in CLAIM.md and criterion.txt
- status/zenodo-latest.json in the claim folder shows the same record id and publication date.
- The Zenodo versions listing for the concept shows exactly 2 versions: 23537067 (r26.10-v4, 2026-10-21) and 20053479 (r26.05-v4, 2026-05-06). No newer release exists.

## 2. Stored sets for the cell: release r26.10-v4, `Hornsea One.1_OSS`, capacity 12

Read with Python sqlite3 from the decompressed reference file. Lengths are recomputed from stored edges and match the stored values.

| id | topology | creator | length (m) | feeders |
|---|---|---|---|---|
| 45373 | radial | MILP.pyomo.cplex | 309220.7062 | [15] |
| 2805 | branched | MILP.pyomo.cplex | 311308.1399 | [16] |
| 9645 | radial | baselines.hgs | 312888.3176 | [15] |
| 8929 | radial | baselines.lkh | 318718.8555 | [15] |

- Best MILP bounds stored (straight-line objective): radial 300763.46 (id 45373), branched 297640.80 (id 2805). The claimed 307472.12 m is above both, which is consistent.
- Object length:
  - From object/segments.json (175 segments): 307472.11908765853 m.
  - From the packed edges in object/routeset-packed.json: 307472.1190876585 m.
  - Terminal segment endpoints all coincide with the nodeset's VertexC (0 mismatches).
- Feeders: 15 at the substation. The cap from the shortest stored set (45373) is [15], so the feeder rule is met.
- Max turbine degree is 3, so the set is genuinely branched.
- Margin over the shortest stored set: 309220.7062 − 307472.1191 = 1748.5872 m (0.565%). This is strictly better, well above the 1e-6 relative threshold, so it is not a tie.

## 3. Neighbouring cells and other published objects

**Same nodeset, other capacities (r26.10-v4).**
- A set built for capacity 11 or below is also valid at capacity 12, but none qualifies here. Every one needs at least 16 feeders, which exceeds the cap of 15, and every one is longer anyway.
- Best stored lengths: capacity 11 is 319646.12 m with [16] feeders; capacity 10 is 336086.47 m with [18] feeders.

**`Hornsea One` (3 substations, same 174 turbine coordinates).**
- Capacity 12, id 62: 247909.90 m with feeders [5,5,6].
- This is a different instance: none of its 3 substations coincides with the single `.1_OSS` substation. Deleting or merging substations is not a valid edit that yields a single-substation route set, so it is not comparable.

**Augmented `!Hornsea One.1_OSS!...` nodesets (T = 56 to 175).**
- They are procedurally generated and normalised.
- None shares any turbine coordinate with the real instance (0/174 shared turbines in every case), so deletion or restriction from them cannot give an object for this cell.

**Earlier DTU datasets.** Each was downloaded into its own folder in my work directory and read only as data. Turbine sets were matched by congruence (sorted pairwise distances, rotation, reflection and scale invariant), so the site would be found under another name or orientation.

- **r26.05-v4** (Zenodo 20053479, previous version of the same concept): its Hornsea One.1_OSS capacity-12 sets are identical to r26.10-v4 (ids 45373, 2805, 9645, 8929, same lengths). Nothing is shorter.
- **Zenodo 18864643 and its newer version 19798734** (paperdb v3/v4 and MILP_model_comparison v3/v4, "Flexible cable routing framework ..."):
  - `Hornsea One.1_OSS` is present with the identical turbines and substation, but only at capacities 2 to 5. There is no capacity-12 set.
  - No other congruent 174-turbine nodeset exists in these files.
- **Zenodo 20140812** (PhD thesis artefacts: optiwindnet_routesets.zip, data_driven_hybrid.zip): analysis notebooks, figures, models and id lists only. There are no stored route sets and no Hornsea-specific results.

**OptiWindNet code.**
- GitHub DTUWindEnergy/OptiWindNet: the tree contains only `optiwindnet/data/Hornsea One.yaml` (layout) and `Hornsea 2.osm.pbf`. The only stored route sets are the Cazzaro/Taylor paper pickles in docs/notebooks/data.
- Release assets for v0.1.6 to v0.3.2 are only wheel and sdist files.
- The predecessor repo mdealencar/interarray has a layout YAML only.
- The documentation's Hornsea example (HGS notebook) uses capacity 7 and prints no lengths.

**Preprint wes-2026-124** (Souza de Alencar, Göçmen, Cutululis; posted 28 Jul 2026, discussion open until 18 Nov 2026, one referee comment RC1). The landing page has no supplements beyond the dataset and code DOIs above, and no Hornsea-specific numbers.

**Literature and code from the last 24 months.**
- Web searches (Hornsea One cable routing, OptiWindNet RouteSets records) found no published Hornsea One single-substation capacity-12 route set or length.
- GitHub code search for "Hornsea One.1_OSS" and "Hornsea_One_1_OSS" returned nothing.
- Cable-routing repos (mdeapedro/tr-wfcrp, LAGOS2025/SupplementaryMaterial, skyoon1109/Offshore-windfarm-cable-routing-optimization) have no Hornsea data in their trees or releases.

**V3R1T4S repo (github.com/elder-plinius/V3R1T4S, main at 6bb0dcfd, 2026-11-06).**
- TROPHY_CASE.md (100 lines) has no OptiWindNet, Hornsea or cable-routing entry.
- `known-knowns/optiwindnet-routesets-cable-routing-records/` does not exist on main or at the pinned commit f3b19b47. Only the target file `known-unknowns/optimization-benchmarks/optiwindnet-routesets-cable-routing-records.md` exists.
- I listed all PRs (924) and issues and grepped them. The only target-related items are open claim PRs #962, #963, #964 (other nodesets), #967 (Hornsea One.1_OSS capacity 10, 332729.3443 m, 18 feeders) and #968 (Hornsea One.1_OSS capacity 8, 377034.6925 m, 22 feeders).
- No PR or issue, open or closed, claims capacity 12 for this instance.
- The capacity-10 and capacity-8 sets would also be valid at capacity 12, but they are longer and exceed the 15-feeder cap.

## 4. Is the object more than a trivial edit of its seed?

Compared at the level of logical links (each turbine's link to the next turbine or the substation, with contour points collapsed):

| stored set | links shared with the object | links that differ |
|---|---|---|
| 45373 (seed) | 161 | 13 |
| 2805 | 123 | 51 |
| 9645 | 145 | 29 |
| 8929 | 113 | 61 |

- The object is not a relabelling or symmetry image: the coordinates are identical and the links differ.
- It is not a deletion or restriction: same instance, all 174 turbines.
- No continuous numerical polish is available here, because the vertex coordinates are fixed. The seed's length equals its objective, and the 1748.59 m gain comes from changed links, not from detour re-routing.

Test of the cheapest local combinatorial edit (script in my work folder, scripts/onemove.py):
- Edit: re-hang one turbine's link to another turbine or the substation, keeping the network acyclic, every subtree at 12 or fewer turbines and at most 15 feeders. Crossings and border detours are ignored, so the test is optimistic.
- Starting point: the seed's straight-line length of 308636.23 m.
- The best single move gains 243.02 m.
- A greedy hill climb of such moves stops after 4 moves at 307938.76 m (straight-line, relaxed).
- The object's full length, detours included, is 307472.12 m. That is 466.64 m below even this relaxed bound.
- So the object beats what the trivial edits give, and it names its seed (id 45373) as the kit requires.

## 5. Verdict

- The status source confirms r26.10-v4 (record 23537067, 2026-10-21) is the latest release, and the reference file matches it.
- In that release, the claimed object (307472.1191 m, 15 feeders) is strictly shorter than every stored set for Hornsea One.1_OSS at capacity 12, of any topology: by 1748.5872 m over the best radial set (45373) and by 3836.02 m over the best branched set (2805).
- I found no published or proposed route set for this cell that is shorter or equal:
  - the earlier release r26.05-v4;
  - DTU's earlier datasets (Zenodo 18864643/19798734, 20140812), searched under any name or orientation;
  - the OptiWindNet repo and its releases;
  - the wes-2026-124 preprint;
  - the literature and code searches;
  - V3R1T4S TROPHY_CASE.md, known-knowns and its PRs and issues.
- The object names its seed and goes beyond what single-link re-hang edits of the seed can reach.

Limits of this review:
- Validity (validate_routeset, crossings, border containment, nodeset identity) is outside the novelty remit and was not checked here.
- Non-indexed private results cannot be excluded.

novelty: CONFIRMED (strictly beats all known published route sets for the cell; not a trivial edit of its named seed)

pass: true
