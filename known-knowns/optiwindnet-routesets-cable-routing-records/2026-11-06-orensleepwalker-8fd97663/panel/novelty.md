# Novelty skeptic: Cazzaro-2022G-210.solid.1_OSS, capacity 7, radial

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

Disclosure: the Claude Code harness automatically loaded the workspace instruction files (CLAUDE.md / AGENTS.md) into this context. Among other things, they contain a one-line note on this run's status. I did not ask for this, did not open any other workspace file, and did not use that note. Everything below comes from the claim folder, my own copies of the public data, and public web pages.

Claim under review (CLAIM.md): radial route set, length **360354.0746 m**, 30 feeders, for nodeset `Cazzaro-2022G-210.solid.1_OSS` (T=210, R=1), capacity 7, release r26.10-v4.

## 1. Status source (one honest fetch)

- `https://zenodo.org/api/records/23537067/versions/latest`, fetched 2026-11-06T00:49:47Z with one plain curl request. It returned HTTP 301 with body `{"status": 301, "message": "Redirecting...", "location": "https://zenodo.org/api/records/23537067"}`, so "latest" resolves to this record. I followed that Location once with one plain request at 2026-11-06T00:49:54Z, which returned HTTP 200. This was a redirect follow, not a retry.
- Values read:
  - id 23537067; title "OptiWindNet RouteSets"; publication_date 2026-10-21; created 2026-10-21T15:29:56Z.
  - metadata.dates: "Release 26.05-v4" and "Release 26.10-v4".
  - relations.version: `is_last: True` (parent recid 20053478).
  - One file: `optiwindnet-routesets-r26.10-v4.sqlite.xz`, size 28464808, checksum `md5:85faffb2e13600b017f1b583b259edd7`.
- The local reference file (references/optiwindnet-routesets-r26.10-v4.sqlite.xz) has md5 85faffb2e13600b017f1b583b259edd7, which matches. Its sha256 is c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, which matches CLAIM.md and the bank entry.
- **Result: r26.10-v4 is still the latest version.** The status source was readable.

## 2. Stored route sets for the instance (my own decompressed copy of the reference)

From routeset rows joined to nodeset `Cazzaro-2022G-210.solid.1_OSS` (the only Cazzaro-2022G-210 nodeset in the release):

| cap | id | topology | creator | length (m) | feeders | note |
|---|---|---|---|---|---|---|
| 6 | 25278 | branched | MILP.pyomo.cplex | 399738.0433 | [36] | neighbour cell |
| 6 | 25098 | radial | baselines.hgs | 401553.2842 | [36] | neighbour cell |
| **7** | **25281** | branched | MILP.pyomo.cplex | **363836.6318** | [30] | bound 349122.508 (straight-line objective bound), relgap 2.82%, maxTimeLimit |
| **7** | **25104** | radial | baselines.hgs | **364573.2688** | [30] | stored radial best |
| 8 | 25099 | radial | baselines.hgs | 333965.9754 | [27] | neighbour cell |

The release has only two route sets at capacity 7, and both values match CLAIM.md exactly.

I also checked the earlier published release, 26.05-v4 (Zenodo record 20053479). I fetched its metadata once at 2026-11-06T00:54:41Z: publication_date 2026-05-06, version 26.05-v4, file md5 38d4b0e96797bb103d1af817584fd7da. I downloaded the file once at 2026-11-06T00:54:47Z (HTTP 200, md5 matches). That release holds the same rows for this instance: 25281 = 363836.6318 and 25104 = 364573.2688 at cap 7, and the same cap-6 and cap-8 values. No shorter set exists in the older release.

## 3. V3R1T4S repository (https://github.com/elder-plinius/V3R1T4S)

Each page was requested once and all returned HTTP 200 (UTC times shown):

- `https://api.github.com/repos/elder-plinius/V3R1T4S` (00:51:25Z): default branch main, pushed_at 2026-11-05T18:59:11Z.
- `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` (00:51:50Z): no mention of OptiWindNet, Cazzaro, cable or route sets.
- `https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns` (00:51:25Z): 27 families, none about OptiWindNet or cable routing.
- `https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1` (00:52:05Z; tree sha ed5f3a40..., not truncated, 6796 entries): the only relevant path is the bank entry `known-unknowns/optimization-benchmarks/optiwindnet-routesets-cable-routing-records.md`.
  - I fetched it at 00:52:11Z. It reads "open as of 2026-10-30" and its win criterion is identical to criterion.txt.
  - Its commit history (one request) shows a single commit, f3b19b475065f35d0a7f93e8a6078c9b2f12566e (2026-10-30), which is the pinned commit. The entry has not changed since.
- All issues and PRs, open and closed: `https://api.github.com/repos/elder-plinius/V3R1T4S/issues?state=all&per_page=100`, pages 1-10 (00:51:29Z-00:51:50Z). That is 959 items, numbers 1-959, of which 920 are PRs. A regex for optiwindnet|cazzaro|routeset|route set|cable rout|inter-array|WFCRP found **no hits**. The separate pulls listing (page 1, 00:51:28Z) also had no hits.
- The GitHub search API (00:51:43-44Z) for `repo:elder-plinius/V3R1T4S` with optiwindnet, cazzaro, routeset and "cable routing" returned total_count 0 for each.
- **Result: no OptiWindNet or cable-routing result, claim or trophy for this instance (or any instance) exists in the repository.**

## 4. Literature and code (last 24 months plus the base paper)

Pages I opened:

- **Zenodo record 23537067** (above). Its description gives aggregate statistics only.
- **WES preprint wes-2026-124**, https://wes.copernicus.org/preprints/wes-2026-124/ (WebFetch, about 00:53Z): received 14 Jul 2026, discussion open until 18 Nov 2026. The landing page has no per-instance lengths and no mention of Cazzaro, .1_OSS or .solid. I did not read the PDF.
- **OptiWindNet dataset docs**, https://optiwindnet.readthedocs.io/stable/dataset.html: lists release 26.05-v4 only, so the docs lag Zenodo. Five hypothetical sites come from Cazzaro & Pisinger (2022), Yi et al. and Taylor et al. `.1_OSS` reduces a layout to a single substation and `.solid` removes obstacles. The page gives no per-instance lengths.
- **OptiWindNet code**: https://github.com/DTUWindEnergy/OptiWindNet (page), GitHub releases API and tags API (00:52:45Z), GitLab releases API `https://gitlab.windenergy.dtu.dk/api/v4/projects/TOPFARM%2FOptiWindNet/releases` (00:52:46Z, 0 releases) and PyPI JSON (00:52:46Z; latest 0.3.2, uploaded 2026-10-12).
  - The GitHub release assets for v0.1.6 to v0.3.2 contain only the wheel and sdist. They hold no route-set data.
  - The release notes mention RouteSets only as the schema and validation code.
- **OptiWindNet docs index** v0.3.2 (https://optiwindnet.readthedocs.io/v0.3.2/) and the notebook **"Cazzaro and Pisinger 2022 G-140 and G-210"**, https://optiwindnet.readthedocs.io/v0.3.2/notebooks/p06_cazzaro_2022_g140_g210.html. This is the closest published object for this site at κ = 7, but it is a **different variant**:
  - It loads `Cazzaro-2022G-210.yaml`, the original site, which the docs' location list gives as 3 substations and 210 turbines, with obstacles.
  - It solves a **balanced** radial MILP (Gurobi, 95 s): objective 294123.1, bound 280249.41, relgap 4.72%. It also reports relative improvements over a "G210_ref" reference.
  - With three substations instead of one, these numbers do not apply to `.solid.1_OSS`, and I do not compare them.
- **Souza de Alencar, Göçmen, Cutululis**, "Flexible cable routing framework for wind farm collection system optimization", EJOR 329(3) 1037-1051 (2026), doi 10.1016/j.ejor.2025.07.069, RePEc page https://ideas.repec.org/a/eee/ejores/v329y2026i3p1037-1051.html. The abstract gives aggregate gains only (1.6-17%), with no .1_OSS lengths.
- **Zenodo 20140812** (PhD-thesis code artifacts, https://zenodo.org/records/20140812): notebooks only. The RouteSets database is not shipped, and the record shows no Cazzaro-G210 lengths.
- **Base paper**, D. Cazzaro and D. Pisinger, Networks 80 (2022) 386-406, doi 10.1002/net.22100:
  - The DTU Orbit landing page (https://orbit.dtu.dk/en/publications/balanced-cable-routing-for-offshore-wind-farms-with-obstacles/) opened, giving the abstract only.
  - The full-text PDF (https://orbit.dtu.dk/files/302263821/Networks_2022_Cazzaro_Balanced_cable_routing_for_offshore_wind_farms_with_obstacles.pdf) returned **HTTP 403**.
  - Wiley full text (https://onlinelibrary.wiley.com/doi/full/10.1002/net.22100) returned **HTTP 403**.
  - I made no retries on either.
- **Companion abstract**, Cazzaro, Koza, Pisinger, TRISTAN XI (2022), https://tristan2022.org/Papers/TRISTAN_2022_paper_6972.pdf (read). Table 1 reports instance **G** as unbalanced 75.41 M€ and balanced 78.15 M€. These are **monetary costs** with two cable types (6 and 8 turbines, 240/336 €/m), with obstacles and the original substations. That is a different objective and a different variant, so the figures are not comparable to a single-substation, obstacle-free length at capacity 7.
- Web searches for `"Cazzaro-2022G-210.solid.1_OSS"`, `"Cazzaro-2022G" OptiWindNet`, and recent Cazzaro-instance cable-routing work returned nothing that reports a route set or length for the `.solid.1_OSS` variant at capacity 7. Search-result snippets I did not open (for example the Springer 2026 integrated-design paper and the ScienceDirect uncertainty paper) are not cited as evidence. Snippets indicate they use other instances or objectives.

**Variant note:** every published number I found for "Cazzaro G-210" outside RouteSets refers to the original 3-substation site with obstacles, as balanced MILP objective or € cost. The `.solid.1_OSS` single-substation variant appears to be a RouteSets construction, and RouteSets r26.10-v4 (identical in 26.05-v4) is the only published source with values for it.

## 5. Trivial-edit check (object vs stored route sets)

I wrote my own decoder for the routeset `edges` parent array, mapping index i to node i for i < T and to node i+B otherwise, with clones mapped to their prime via clone2prime. Using the release's VertexC blob:

- **Coordinates and length:**
  - The object's routeset-packed.json decodes, with the release's own coordinates, to exactly the segment set in object/segments.json (228 segments).
  - The multiset sum is 360354.0740 m, against the claimed 360354.0746 m. The difference comes from rounding coordinates to 1 mm in my multiset key; the plain sum over segments.json is 360354.07455 m.
  - The stored rows decode to their stored lengths (25104: 364573.2690; 25281: 363836.6319).
- **vs 25104 (radial best):**
  - 187 of 228 object segments are shared (270485.6 m). 41 segments, **89868.5 m (24.9% of the object's length)**, are not in 25104, and 46 stored segments (94087.7 m) were removed.
  - At turbine level, 32 of 210 links differ and 53 turbines have changed neighbours.
  - Both sets have 30 strings. Only 19 strings have identical turbine sets; the other 11 were re-partitioned. All 30 object strings are full (7 turbines each).
- **vs 25281 (branched best):** 48 object-only segments (96954.4 m, 26.9%), 40 of 210 turbine links differ, and 18 of 30 strings are identical.
- **Neighbouring cells:**
  - The cap-6 sets are valid at cap 7 by restriction, but they are longer (best 399738.04 m).
  - Cap-8 sets are infeasible at cap 7.
  - Converting the branched cap-7 set to radial cannot make it shorter than itself (363836.63 m).
  - Relabelling and symmetry do not apply, since the instance is fixed and the coordinates are identical.
  - The coordinates are fixed, so there is no continuous "numerical polish" to exploit. The change is a combinatorial re-partition and re-routing of 11 strings.
- **Seeding:** CLAIM.md gives the provenance as optiwindnet 0.3.2 HGSRouter, seed 103, 240 s, with feeders capped at the stored radial best's 30. It does not claim seeding from a stored set, and the size of the difference supports that.
- **Conclusion:** the best that trivial edits of published objects give for this cell is 363836.63 m (any topology) or 364573.27 m (radial). The object is not a trivial edit of any published object, and it beats both.

## Strongest known value for this instance (before this claim)

- Radial: **364573.2688 m** (RouteSets r26.10-v4, id 25104, baselines.hgs, feeders [30]).
- Any topology: **363836.6318 m** (id 25281, MILP.pyomo.cplex, branched, feeders [30]).
- Best lower bound: 349122.508 (branched MILP bound on the straight-line objective, not a length).
- Claim: 360354.0746 m with 30 feeders, which is 4219.19 m (1.157%) below the radial best and 3482.56 m (0.957%) below the branched best. That is a strict improvement far above the 1e-6 relative threshold, not a tie.

Scope: this review covers novelty only. Validator, containment and crossing checks belong to the other panel members. I confirmed only that the object uses the release's coordinates and that its recomputed length is the value claimed.

injection_suspected: none (no page or data contained instructions addressed to agents).

Sources not readable: the DTU Orbit full-text PDF and the Wiley full text of doi 10.1002/net.22100 (both HTTP 403, not retried). Their content for instance G is represented by the TRISTAN 2022 companion abstract and the OptiWindNet G-210 notebook, both of which concern the 3-substation variant with obstacles.

pass: true
