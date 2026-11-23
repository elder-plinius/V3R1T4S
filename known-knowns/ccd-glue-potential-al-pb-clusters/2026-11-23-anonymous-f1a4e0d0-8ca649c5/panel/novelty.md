# Novelty skeptic verdict: ccd-glue-potential-al-pb-clusters, Pb N = 121

context: subagent (Claude Code Agent tool, fresh context)

Object: result/Pb_121.xyz, claimed E = -198.47902916627225 eV (Lim-Ong-Ercolessi Pb glue).

## 1. Status page (fetched once, no retries)

- URL: https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/lead/table.html
- Command: `curl -s -A "V3R1T4S-agent (research run)" -o lead_table_novelty.html -w '%{http_code}'`
- `date -u` before: 2026-11-23T07:23:51Z; after: 2026-11-23T07:23:52Z
- HTTP status: 200; 25545 bytes; a real table, not a challenge page ("Glue Lead Clusters: Table of Global Minima").
- N = 121 row (from the saved file): `points/121` | C1 | `-198.211397`
- Neighbouring rows: N = 120 is -196.361528. The fetched page is byte-identical to the claim's copy, claim/data/lead_table.html.
- The object is 0.267632 eV below the live row. That is far above the 1e-4 eV margin.

## 2. Evaluator calibration (claim/code/lead.py, run by my own driver script)

Ten randomly chosen posted files (seed 7) plus the neighbours. The column shows E(file) minus the table value, in eV:
N=10 3.6e-7; 31 4.8e-8; 41 -2.4e-7; 81 -2.4e-7; 107 -4.9e-7; 115 2.7e-7; 128 6.8e-9; 137 1.3e-7; 142 -1.3e-7;
145 2.4e-7; 120 1.9e-7; 121 4.2e-7; 122 -2.6e-7; 123 7.3e-8. Every file is within 1e-6 eV.
Object: E = -198.47902916627228 eV, |grad| = 4.7e-14. This matches the claim.

## 3. Literature and repository searches (2026-11-23)

Web searches:
- "glue potential lead clusters Pb global minima"
- "Pb cluster Lim Ong Ercolessi glue potential structures 2025 arXiv"
- '"glue potential" lead nanoclusters basin hopping lower energy Cambridge Cluster Database 2024 2025 2026' (extended)

Every search returned only the following. None of them gives a Pb-glue N = 121 value below the table:
- Doye & Hendy, cond-mat/0207432 / EPJD 22, 99 (2003): the table's source.
- Hendy & Doye, cond-mat/0207566: N >= 900.
- Doye, cond-mat/0405234: Gupta potential, which is a different potential.
- A 2024 JPCA deep-RL cluster paper that does not cover the Pb glue potential.
- The CCD pages.

No 2024-2026 Pb-glue work was found.

V3R1T4S repository (gh, read-only):
- TROPHY_CASE.md: 0 matches for "glue". No glue, lead or Pb entry.
- known-knowns/: 47 directories, none glue or Pb. lennard-jones-ccd-doye-table is the only CCD directory.
- Code search for "ccd-glue": only known-unknowns/packings-physics/ccd-glue-potential-al-pb-clusters.md and the README. The target is still open.
- PRs, all states:
  - The "glue" search returns 9 PRs, all on other targets.
  - A title filter over 1000 PRs for glue, ercolessi, lead, Pb_ or aluminum matched only "leaderboard" titles.
  - Other CCD claims (#374, #375, #365, #484, #466, #799, #202) concern other potentials.
- Issues: none match.
- Releases: none listed (`gh release list` is empty).

## 4. My own trivial-edit tests

Setup:
- Code is in my working folder (edits.py). It uses claim/code/lead.py energy and gradient with L-BFGS-B, gtol 1e-7.
- Inputs are the posted files claim/data/lead_points/120 to 125.
- New atoms go at random outward surface sites 3.3-3.6 A from an outer atom, at least 3.0 A from all atoms.
- A "hit" is E < E_obj + 1e-4.

Results, copied from the output:

| edit family | trials | best E (eV) | gap to object (eV) | hits |
|---|---|---|---|---|
| posted 122 minus each atom (all) | 122 | -198.187380578451 | 0.29165 | 0 |
| posted 123 minus every pair (all) | 7503 | -198.17060647207882 | 0.30842 | 0 |
| posted 120 plus one atom | 6000 | -198.18999436309335 | 0.28903 | 0 |
| posted 121, one atom relocated (each atom x 50 sites) | 6050 | -198.22958787573432 | 0.24944 | 0 |
| posted 121, 2 random atoms relocated | 20000 | -198.23975912018224 | 0.23927 | 0 |
| posted 121, 3 random atoms relocated | 20000 | -198.2332424238149 | 0.24579 | 0 |
| posted 121, 4 random atoms relocated | 10000 | -198.21139657587702 | 0.26763 | 0 |
| posted 122 minus 2 atoms plus 1 added | 10000 | -198.21139657587725 | 0.26763 | 0 |
| posted 124 minus 3 random atoms | 8000 | -198.17255605412453 | 0.30647 | 0 |
| posted 125 minus 4 random atoms | 8000 | -197.9524537023913 | 0.52658 | 0 |
| posted 120 minus 1 plus 2 added | 8000 | -198.22068934061588 | 0.25834 | 0 |
| posted 121 random shake (sigma 0.1-0.5 A) + relax | 6000 | -198.2113965758774 | 0.26763 | 0 |

- Total: 129,675 relaxations, with no hit.
- The best any edit reached is -198.23976 eV, from a 2-relocation of posted 121. The object is 0.2393 eV below that.
- Relabelling, rotation and reflection leave the energy unchanged, so they cannot produce the object.
- The shake/polish rows show that local polishing of posted 121 stays in its basin at -198.2113966 eV.

My numbers agree with the claim's disclosed bars:
- 122 minus 1: identical, -198.1873806.
- 123 minus 2: identical, -198.1706065.
- 120 plus 1: identical, -198.1899944.
- The claim's 2-relocation best was -198.2409842 and mine was -198.2397591. Both are far above the object.

The claim's own alignment file (bars/align_object_vs_posted121.txt) shows 3 atoms displaced 4.6-7.4 A and 4 more displaced about 0.9 A. Its oracle k = 3 bar (-198.40278, chosen with knowledge of the object) also failed to reach the object.

## 5. Judgement

- Seeding is disclosed: basin hopping from posted 121 and from posted 122 minus atoms. The object names those seeds.
- The object beats everything the trivial edits gave, both mine and the claim's, by at least 0.239 eV.
- It strictly beats the live table row by 0.267632 eV.
- No other published Pb-glue value for N = 121 was found, and the repo has no prior entry for this cell.
- This is not a tie or a relabelling, and no trivial edit I tried reproduces it.

Limitation: the 2-relocation and 3-relocation families were sampled randomly, not exhaustively. 40,000 trials found nothing within 0.239 eV.

novelty: CONFIRMED (strictly below everything known; not reachable by tested trivial edits)

pass: true
