# Novelty review: Hornsea One.1_OSS, capacity 9, branched, 351584.0138 m

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

## 1. Status source (fetched once, no retries)
- URL: https://zenodo.org/api/records/23537067/versions/latest
- Time: 2026-11-07T14:53:02Z (UTC). HTTP 301, body `{"status": 301, "message": "Redirecting...", "location": "https://zenodo.org/api/records/23537067"}`.
  The versions/latest endpoint redirects to record 23537067 itself, so the latest version is 23537067.
- I then followed that redirect once (it completes the same request; it was not a retry): https://zenodo.org/api/records/23537067 at 2026-11-07T14:53:11Z, HTTP 200.
  Latest record id 23537067, publication_date 2026-10-21, modified 2026-10-21T15:29:56Z. Its only file is optiwindnet-routesets-r26.10-v4.sqlite.xz, md5 85faffb2e13600b017f1b583b259edd7.
- The local references/optiwindnet-routesets-r26.10-v4.sqlite.xz has md5 85faffb2e13600b017f1b583b259edd7, the same as Zenodo, and sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, the same as CLAIM.md. No newer release exists. The concept's version list has only 23537067 (r26.10-v4) and 20053479 (r26.05-v4).

## 2. Stored sets for the cell (reference DB, nodeset 'Hornsea One.1_OSS', T=174, R=1, B=25, capacity 9)
| id | creator | topology | length (m) | feeders |
|---|---|---|---|---|
| 9638 | baselines.hgs | radial | 353604.6746 | [20] |
| 45718 | MILP.pyomo.cplex | radial | 353604.6746 | [20] |
| 2802 | MILP.pyomo.cplex | branched | 358653.0477 (bound 341271.12, relgap 4.0%) | [20] |
| 8925 | baselines.lkh | radial | 372903.6710 | [20] |

The object (object/G.pickle, object/routeset-packed.json, object/segments.json) has these properties:
- Its length, summed from segments.json, is 351584.0138106 m. This equals the packed length.
- It has 20 feeders, no more than the shortest stored set's 20.
- Its maximum turbine degree is 3 (branched).
- optiwindnet 0.3.2 validate_routeset returns [].
- Its VertexC is identical to the stored nodeset's (200x2).

It is 2020.66 m (0.571%) below the stored best, 353604.6746 m, with relative margin 5.7e-3, well above 1e-6.

## 3. Neighbouring cells
- Capacity 8 of the same nodeset: a cap-8 set is feasible at cap 9. The stored best is 380296.05 m. Open PR #968 in elder-plinius/V3R1T4S claims 377034.69 m (branched). Both are longer than the object.
- Capacity 10 and higher are more relaxed and so not admissible as cap-9 sets. Open PR #967 claims 332729.34 m at capacity 10, which does not bear on capacity 9.
- 'Hornsea One' (R=3, three substations) is a different instance. Its cap-9 set id 63 is 257191.48 m and is not comparable.
- The augmented '!Hornsea One.1_OSS!...' nodesets have T between 56 and 180 but never 174, so none of them is this instance.
- No nodeset in any DTU dataset I checked has these turbine coordinates under another name, scale or orientation. I searched with a rotation-, translation-, scale- and relabelling-invariant signature (sorted centroid distances) over every nodeset with T between 170 and 180. Only 'Hornsea One.1_OSS' (R=1) and 'Hornsea One' (R=3) match.

## 4. Published sources searched (last 24 months)
Every downloaded file sits in its own directory under work-novelty/dl-*.
- **Zenodo 20053479 (r26.05-v4, 2026-05-06; the dataset the wes-2026-124 preprint page cites):** cap-9 sets are the same four, minimum 353604.6746. No set at capacity 9 or below is shorter than 351584.0138.
- **Zenodo 18864643 / 19798734 (paperdb v3/v4 and MILP_model_comparison v3/v4, EJOR "Flexible cable routing framework" 2025):** 'Hornsea One.1_OSS' appears only at capacities 2-5. There is no cap-9 set and nothing shorter at capacity 9 or below.
- **Zenodo 20140812 (thesis code, 2026-05-12):** contains notebooks and models only. No route sets, and no mention of Hornsea.
- **wes-2026-124 preprint page:** received 2026-07-14, discussion opened 2026-07-28. One referee comment (RC1). No supplement, and no Hornsea cap-9 figure on the page. Data and code links point to the two records above.
- **DTUWindEnergy/OptiWindNet on GitHub:**
  - Main tree: no route-set data for Hornsea. The docs/notebooks/data/*.pkl files are Cazzaro and Taylor sets.
  - Notebooks: Hornsea appears only in lo21_hgs (R=3, capacity 7), hi12_locations and the p03 table.
  - Releases v0.1.6 to v0.3.2: the assets are only the wheel and sdist. The v0.3.2 sdist holds no route sets, only the site yaml.
  - GitHub code search for "Hornsea": no third-party cable-routing result.
- **Web searches** for Hornsea One cable-routing optimisation, "Hornsea One.1_OSS", and new-best OptiWindNet claims: no published shorter route set for this instance.
- **elder-plinius/V3R1T4S** (main at 6bb0dcf, 2026-11-06, and pinned commit f3b19b4):
  - TROPHY_CASE.md does not mention optiwindnet or Hornsea.
  - known-knowns/optiwindnet-routesets-cable-routing-records/ does not exist at either commit.
  - The bank entry known-unknowns/optimization-benchmarks/... lists no cap-9 result.
  - All open and closed PRs and issues: the optiwindnet claims are #962, #963, #964 (other sites) and #967 and #968 (Hornsea capacities 10 and 8). None is for capacity 9.

## 5. Is it more than a trivial edit of a published object?
- **Seed:** CLAIM.md names its seed, stored set 9638 (tied with 45718), which is radial with length 353604.6746 m.
- **Differences from the seed:** turbine-level links were compared with clones mapped to primes and border-vertex detour paths contracted. The object differs from 9638 (and 45718) in 9 removed and 9 added links.
  - Added: (17,21) (62,71) (64,65) (73,74) (106,111) (142,143) (162,163) (167,169) (168,171).
  - Removed: (17,23) (61,71) (65,72) (66,74) (111,112) (138,143) (159,163) (168,173) (169,170).
  - These are subtree re-attachments that turn the radial seed into a branched tree with degree-3 turbines.
- **Against stored branched set 2802:** the object differs in about 51-53 links.
- **Can a trivial edit reach it?**
  - Deletion, restriction, relabelling and symmetry cannot shorten a set on fixed coordinates.
  - The only continuous polish available is re-routing detours. The seed's straight-line objective is already 353391.99 m (misc.objective), so even zero detour overhead leaves the seed 1807.98 m above the object.
  - The improvement therefore comes from a combinatorial re-optimisation: a fix-and-optimise CP-SAT LNS, the method CLAIM.md states. It is not a propagation or polish of the seed, and it beats everything those edits give, which is at best 353391.99 m.
- **Caveat:** this rewiring is a moderate local change (9 links out of about 174). It is a genuine new object, but a near-variant of the seed in structure.

## 6. Verdict
- For Hornsea One.1_OSS at capacity 9, no published route set of any topology is shorter than 351584.0138 m. The sources checked are the latest release r26.10-v4 (confirmed latest at fetch time), r26.05-v4, DTU's earlier Zenodo datasets, OptiWindNet code and releases, the wes-2026-124 preprint, the web, and V3R1T4S trophy case, known-knowns, PRs and issues.
- The object names its seed. It is not reachable by trivial edits of the seed or of any other stored set, and it strictly beats the best known, 353604.6746 m, by 2020.66 m. It is not a tie.
- Scope: this verdict covers novelty only. Containment in the border and obstacles, crossings and length are for the other reviewers. Here I only confirmed that validate_routeset returns [] and that the recomputed length matches.

novelty: confirmed new (strictly below all known, margin 2020.66 m / 0.571%)
pass: true
