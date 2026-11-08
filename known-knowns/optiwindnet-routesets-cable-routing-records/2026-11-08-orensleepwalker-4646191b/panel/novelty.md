# Novelty review: London Array.1_OSS, capacity 7, branched (claim-la7)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

Reviewer role: novelty skeptic. Inputs: the claim folder (read-only) and public sources. Downloads and scripts are in `panel-la7/work-novelty/`, with each download in its own `dl-*` directory.

## 1. Status source (fetched once, no retries)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- HTTP 200 (redirected to https://zenodo.org/api/records/23537067)
- Fetched 2026-11-08T16:35:09Z (UTC)
- Latest record id 23537067, publication_date 2026-10-21, modified 2026-10-21T15:29:56Z. The record has one file, `optiwindnet-routesets-r26.10-v4.sqlite.xz` (md5 85faffb2e13600b017f1b583b259edd7, 28,464,808 bytes).
- The version list for the concept has two entries, 23537067 (r26.10-v4) and 20053479 (r26.05-v4). No newer release exists. The status matches the claim's `status/zenodo-latest.json`.
- `references/optiwindnet-routesets-r26.10-v4.sqlite.xz` has md5 85faffb2… and sha256 c78c8f3c…e3a. Its decompressed md5 is 5ad6bf0449dcbd9939f1ae03bee19016, which matches the release table on Zenodo.

## 2. The cell in the release (r26.10-v4)

Nodeset `London Array.1_OSS` (digest ed799d97227c…, T=175, R=1, B=9). Single substation at (395165.77, 5719457.03), which is the midpoint of the two substations of the `London Array` nodeset. Stored capacity-7 sets:

| id | creator | topology | length (m) | feeders | straight-line objective |
|---|---|---|---|---|---|
| 9627 | baselines.hgs | radial | 173966.4420 | [25] | 173919.86 |
| 45872 | MILP.pyomo.cplex | radial | 173966.4420 | [25] | 173919.86 (bound 170910.91) |
| 2792 | MILP.pyomo.cplex | branched | 174227.8163 | [26] | 174213.42 (bound 170760.98) |
| 8904 | baselines.lkh | radial | 188458.0326 | [25] | 186864.56 |

Claim object: total length 173753.9532 m. I recomputed it from `object/segments.json` (180 segments) and got 173753.9532. It has 25 feeders and a maximum turbine degree of 3. `validate_routeset` on `object/G.pickle` returns []. Its turbine coordinates are identical to the release nodeset. It is shorter than the best stored set by 212.4888 m (0.1221%, well above the 1e-6 relative threshold). It uses the same number of feeders as the best stored set (25 ≤ 25). It also beats the best stored branched set (2792) by 473.86 m, and 2792 uses 26 feeders.

## 3. Other published sources checked

| Source | What it holds for this cell | Shorter than 173753.95? |
|---|---|---|
| Zenodo 20053479 (r26.05-v4; decompressed md5 3aea2559… matches) | Same nodeset digest. Same four cap-7 sets with the same lengths (9627, 45872, 2792, 8904) | No |
| Zenodo 18864643, paperdb.v3 (EJOR 2025 "Flexible cable routing framework" data) | `London Array.1_OSS`, same digest ed799d97227c. Cap 7: 9627 (173966.44) and 2792 (174227.82) only | No |
| Zenodo 19798734, paperdb.v4 | Identical to v3 for this nodeset | No |
| Zenodo 18864643/19798734, MILP_model_comparison v3/v4 | Only `London Array legacy` (2 substations, T=175). Cap 7: id 120, 165754.22 m [13,13] and id 261, 166836.09 m [13,14]. No single-substation nodeset | See section 4 |
| Zenodo 20140812 (thesis notebooks: optiwindnet_routesets.zip, data_driven_hybrid.zip) | No route sets; reads r26.05-v4. No mention of London Array | No |
| The 2-substation `London Array` nodeset in r26.05-v4 and r26.10-v4 | Cap ≤7 sets, best cap 7 id 138: 165931.24 m [12,14] | See section 4 |
| Augmented `!London Array.1_OSS!A52J…` and the `!London Array!…` nodesets | Turbine sets differ: a pairwise-distance fingerprint search over all T=175 nodesets in every file found only `London Array` and `London Array.1_OSS` congruent to this instance | Different instance |
| OptiWindNet repository (GitHub mirror DTUWindEnergy/OptiWindNet, same head 664de8708a, 2026-10-16, as GitLab TOPFARM/OptiWindNet) | `optiwindnet/data/London Array.yaml` (layout only). Test cases cover the 2-substation `london` at caps 4, 8 and 10. Notebook lo14 has a 2-substation constructor heuristic at cap 7 (feeders 16\|13). Notebook p02 has legacy MILP values. Nothing for the 1_OSS variant | No |
| OptiWindNet release assets v0.1.6 to v0.3.2 (wheels and sdists, all 8 releases) | Only test fixtures for the 2-substation `london` with the EWRouter heuristic at caps 1/4/10/15/50/100. No `1_OSS` data | No |
| Preprint wes-2026-124 (PDF fetched from wes.copernicus.org) | Aggregate analyses of r26.05-v4. No London Array value found in the extracted text | No |
| V3R1T4S (github.com/elder-plinius/V3R1T4S): TROPHY_CASE.md, known-knowns/ (31 entries), 970 open and closed PRs (#1–#1019), PR and issue search for "London Array" | No OptiWindNet entry in TROPHY_CASE.md or known-knowns/. The OptiWindNet claim PRs (#962–#998) cover Hornsea One.1_OSS, Yi-2019.1_OSS and Cazzaro-2022G-210. None is for London Array | No |
| Web literature search, last 24 months | Open Research Europe 3-214 (2023/24) treats London Array with a different cost-based model on the real 2-substation farm, so it is not this cell. Nothing else found | No |

## 4. Can the 2-substation or "legacy" sets be transplanted?

`London Array legacy` has the same turbines as this instance, rotated by about 95°. A rigid alignment matches all 175 turbines one-to-one with a maximum error of 0.007 m. Its two substations sit at slightly different positions (7437 m apart, against 7452 m in the release). The single substation of `London Array.1_OSS` lies at the midpoint between the two substations.

I mapped every 2-substation set with capacity ≤7 onto this instance in two ways. (a) Each feeder is moved from its old substation to the single substation. (b) Each capacity-feasible subtree is re-rooted at the turbine nearest the single substation, which is the best re-routing that keeps the published subtrees. Both use straight-line lengths and ignore crossings and detours, so the real lengths would be no shorter.

| set | stored | (a) | (b) | feeders/subtrees |
|---|---|---|---|---|
| r26.10 London Array id 138, cap 7 | 165931.24 | 220947.48 | 206636.12 | 26 |
| legacy id 120, cap 7 | 165754.22 | 219141.10 | 206323.78 | 26 |
| legacy id 261, cap 7 | 166836.09 | 220334.32 | 208863.74 | 27 |
| best at cap 6 (legacy 119) | 177414.06 | 229835.25 | 212015.60 | 30 |

All transplants are at least 32.5 km longer than the claim, and all need more than 25 feeders. The best single-substation set at a lower capacity (cap 6 is valid at cap 7) is 190810.46 m. The 2-substation "legacy" sets beat the release only on the 2-substation cell. They give nothing competitive for this single-substation cell.

## 5. How the claim relates to its seed

CLAIM.md names the seed: the radial sets 9627 and 45872, which have the same turbine-level topology. At turbine level, after contracting detour nodes, the claim shares 169 of 175 links with the seed. It differs in 6 links, made up of two separate exchanges:

- Move A, radial reorientation of one string: add (root,35),(36,54) and remove (35,54),(root,36). Change −55.33 m.
- Move B, a branching exchange among turbines 0, 1, 2, 3, 7, 8, 9, 11, 18 and 19: add (1,9),(7,8),(8,19),(3,11) and remove (7,18),(8,9),(2,11),(0,8). Change −157.10 m. This creates a degree-3 turbine.

The straight-line total falls from 173919.86 to 173707.43, and detours add 46.53 m.

What the trivial edits alone can reach:

- Detour or PathFinder polishing of the seed is bounded below by the seed's straight-line objective of 173919.86 m. That is 165.9 m above the claim.
- Relabelling, mirroring or symmetry of any published set is length-preserving. The only published sets on this point set are the ones above.
- Deletion and restriction do not apply, because every turbine must be connected.
- No published set from any neighbouring cell transplants below 190810 m.

The improvement therefore comes from a combinatorial link exchange that the trivial-edit list does not cover. It is not a numerical polish. It is still a small local change (6 of 175 links). Move A on its own shows that the stored radial best was not 2-opt locally optimal. That matters for reading the size of the result, but it does not stop the claim from being strictly better than every known set.

## 6. Verdict

The claimed route set (173753.9532 m, 25 feeders, branched) is strictly shorter than every published route set I could find for London Array.1_OSS at capacity 7. I searched both release versions, paperdb v3/v4, the MILP_model_comparison legacy files, the thesis artifacts, the OptiWindNet repository and all 8 release assets, the wes-2026-124 preprint, and V3R1T4S's TROPHY_CASE.md, known-knowns/ and PRs. It also beats everything that relabelling, mirroring, re-routing or transplanting the 2-substation "London Array" and "London Array legacy" sets gives, and everything that detour polishing of the named seed gives. It is not a tie: it is 212.49 m (0.122%) below the best stored set and uses the same feeder count. Novelty is confirmed, with one caveat: it is a small local improvement of the named seed (6 links changed).

pass: true
