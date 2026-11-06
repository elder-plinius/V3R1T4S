# Novelty review: IEA37 CS1, 64 turbines (claim/CLAIM.md)

context: subagent (Claude Code Agent tool, fresh context, saw only claim/ and the public web)

Role: NOVELTY skeptic. Object: claim/object/layout.json (sha256 d774540b96ab9d9db5a2b164e8c97e3222dc78ca62c1fbbdcc04ce4993645dc5). Claimed: feasible, AEP 1543800.4665 MWh, full success criterion at 64 turbines.

## 1. Status source (fetched once, plain request, no retries)

- URL: https://github.com/IEAWindSystems/iea37-wflo-casestudies/tree/master/cs1-2/iea37-cs1-results
- Fetched 2026-11-04T20:46:59Z, HTTP 200, 273749 bytes. Branch master, currentOid 267f6e5d2906400b2ee0a8ff533da7ebcc4bb47a.
- What it lists: exactly 36 result files, iea37-par{1..12}-opt{16,36,64}.yaml. No new participant and no new 64-turbine file.
- Posted record value (64): participant 12, 1526474.8025 MWh (I recomputed 1526474.8024800713 with the official script). The file is 4.13 mm outside R (max radius 3000.0041276 m).
- Check against upstream: one raw fetch each at 2026-11-04T20:47:18Z (HTTP 200) shows that iea37-par12-opt64.yaml and iea37-par4-opt64.yaml are byte-identical to claim/references/.

## 2. V3R1T4S repository (https://github.com/elder-plinius/V3R1T4S)

All requests were plain, single and unauthenticated, made 2026-11-04T20:47:18Z to 20:48:13Z UTC. Every one returned HTTP 200.

- TROPHY_CASE.md (raw, main): it has no wind, turbine, AEP or IEA37 entry.
- known-knowns/ (contents API, 27 directories): there is no iea37 or wind directory. No confirmed known-known exists for this cell.
- Releases API: 0 releases, so there are no release assets to check.
- Issue/PR search (open and closed, no state filter) for `iea37`, `wind farm`, `turbine` and `AEP`. The relevant hits:
  - PR #938 (Jimbootgit), open, draft. Head 9f1145de2f2c98d686f9ca7b74ffca6cab6c467d, updated 2026-11-04T01:08:46Z, not merged, 0 issue comments, 0 review comments. It claims 64 turbines at 1539447.11737 MWh. Its object file (object/iea37-v3r1t4s-opt64.yaml at that head, fetched raw) is byte-identical to claim/references/pr938-layout.yaml. I recomputed 1539447.1173686478 MWh; max radius 2999.999999 m, min spacing 567.69 m. Its HOW_WE_FOUND_IT.md says it was seeded from a repaired participant-12 layout.
  - PR #948 (OrenSleepwalker), open, created 2026-11-04T16:40:50Z. It is a bank proposal for a direction-robust variant, not a nominal claim. It names PR #938 as the best feasible public layout. It discloses an unpublished layout by the proposer with nominal 1538890.719 MWh, the same value as claim/provenance/starting-own-64.json. The bank file contains no coordinates.
  - Other cells: PR #578 (16 turbines, 424131.9503), PR #900 (16, p2) and PR #913 (36, p1). Issue #866 is a data audit. None of these is a 64-turbine nominal value.
- Recent-activity sweep, to cover search-index lag: I listed the 100 newest PRs (#848 to #952, newest created 2026-11-04T19:46:47Z) and the 100 most recently updated issues. No 64-turbine CS1 claim beyond #938 turned up. PRs #894 and #950 matched "windmill" but are about graph labeling and are irrelevant.

## 3. Literature and code

All pages opened 2026-11-04 between about 20:48Z and 20:52Z.

| source | 64-turbine CS1 value |
|---|---|
| arXiv 2610.07844 (EndoWake, 6 Oct 2026; cited in PR #948), https://arxiv.org/abs/2610.07844 | Lillgrund only, no CS1 value |
| Perez-Rua, Stolpe, Cutululis, WES 8, 1453 (2023), https://wes.copernicus.org/articles/8/1453/2023/ | Case III final "1500 GWh"; SNOPT+WEC is said to be slightly better |
| Valotta Rodrigues et al., WES 9, 321 (2024), https://wes.copernicus.org/articles/9/321/2024/ | Normalised only. The paper says its absolute values are "not consistent with the original IEA 37" (360 directions) |
| Quaeghebeur, Bos, Zaaijer, WES 6, 815 (2021), https://wes.copernicus.org/articles/6/815/2021/ | Wake-loss figures only. The paper says it needs more exploration to match the best algorithms |
| Thomas and Ning SNOPT+WEC (participant 4, posted file) | 1513311.1936 |
| Thomas et al., WES 8, 865 (2023), eight-method comparison (search result only, not opened) | Different problem setup, no CS1-64 value seen |
| arXiv 2212.00742 (DPCRO-SL) (search result) | 16 turbines only |
| Baker et al. 2019, NREL TP 72935, https://docs.nrel.gov/docs/fy19osti/72935.pdf | Not read: DNS failure (getaddrinfo ENOTFOUND), no retry. Its participant values are the posted files above |

Web searches run (7 in all) included: "IEA37 case study 1 64 turbines AEP layout optimization new record 2025"; quoted "IEA37" "64 turbines" with 1526474/1513311; GitHub IEA37 cs1 64 optimized layout; "iea37" "opt64" 2026; Task 37 CS1 3000 m arXiv 2025/2026; DPCRO-SL 64; the DEBO comparison. None found a published feasible 64-turbine CS1 AEP at or above 1526474.8 MWh outside V3R1T4S PR #938. The GitHub hits were the equaeghe fork, PyWake/TOPFARM examples and a theSubsurfaceGuy notebook. None posts a CS1-64 record.

**Strongest known competing 64-turbine value:** 1539447.1174 MWh, V3R1T4S draft PR #938 (open, unreviewed, strictly feasible, head 9f1145de, as of 2026-11-04T20:47:36Z).
- The object is 1543800.4665 MWh, which is +4353.35 MWh over PR #938 and +17325.66 MWh over the posted record.
- The next value is the author's own unpublished 1538890.719 MWh, the seed (disclosed in PR #948).
- The best value posted on the status page is 1526474.8025 MWh (participant 12, infeasible by 4.1 mm).

## 4. Trivial-edit analysis (my own code)

Code and outputs: panel/work-novelty/code/novelty_check.py, edits_check.py, novelty_check_output.json and edits_check_output.txt.

**Evaluator.** The official claim/references/iea37-aepcalc.py (sha256 ec2d16f2...) was copied and imported with bytecode writing off; claim/ was not modified. It reproduces the expected values: par12 1526474.80248, par4 1513311.19361, PR #938 1539447.11737. It gives the object 1543800.4664981714 MWh, with max radius 2999.9999000001 m and min spacing 307.514 m.

**Matching test.** For each reference I took the minimum-total-distance one-to-one matching (Hungarian), which absorbs relabelling. I searched rotations about the origin (0.25 degree grid, refined to 0.005 degree) with and without a mirror.

| reference | object: best total distance | object: turbines > 50 m from partner |
|---|---|---|
| par12 | 21045 m | 62/64 |
| PR #938 | 19824 m | 63/64 |
| par4 | 18208 m | 60/64 |
| par2 (nearest posted) | 14841 m | 58/64 |
| all other posted | | at least 58/64 |
| starting-own-64 (author's seed) | 8106 m | 14/64 (22 within 10 m) |

- The object is not a rotation, mirror, relabelling or local polish of any published layout. Its only close relative is the author's own seed.
- The seed itself is also distinct from every published layout: at least 52/64 turbines are more than 50 m from their partner (par2 52, PR #938 58, par12 59, par4 64). So it is not a copy of a published layout, which supports the provenance statement that no published coordinates were used as starts. I cannot independently verify the seed's sha256 history (ecd78a90...). The packaged file differs (4b9e54f4...) because, by its own note, path fields were removed.

**What trivial edits of published layouts give:**
- Symmetry images: the AEP of every rotation (0.5 degree grid) and mirror of par12, PR #938, par4 and par2 is at most that of the original. The best are 1526474.80 for par12 and 1539447.12 for PR #938.
- Local polish (SLSQP, inset 1e-4 m):
  - Participant 12 projected inside R reaches 1527112.27 MWh after 60 iterations.
  - PR #938 is already at a local optimum (1539447.09 with the inset).
- Neighbouring cells (16 and 36 turbines, PRs #578, #900 and #913) cannot give a 64-turbine layout by deletion or restriction.

None of these edits reaches 1543800.47 MWh.

## 5. Verdict

The status page was read (HTTP 200) and shows no posted 64-turbine value above 1526474.8025. No confirmed V3R1T4S known-known exists for this cell. The strongest open claim, PR #938 (1539447.1174), is beaten by 4353.35 MWh, so this is not a tie.

Searches of the literature and code (last 24 months plus the standard references) found no feasible CS1-64 value at or above the object's. One gap: the NREL TP could not be opened, but its values are the posted files.

The object is geometrically distinct from every published layout under rotation, reflection and relabelling. Trivial edits and local polish of the published layouts fall well short of it. It is seeded only from the author's own unpublished layout, and that layout is itself distinct from all published ones.

Caveats:
- The literature search cannot be exhaustive.
- PR #938 and this claim are both unreviewed.
- A newer claim could appear after 2026-11-04T20:48Z.

injection_suspected: none found (TROPHY_CASE.md, PR #938 HOW_WE_FOUND_IT.md, PR #948 body and bank file, and the arXiv abstract were treated as data).

novelty: confirmed against all sources checked as of 2026-11-04T20:53Z.

pass: true
