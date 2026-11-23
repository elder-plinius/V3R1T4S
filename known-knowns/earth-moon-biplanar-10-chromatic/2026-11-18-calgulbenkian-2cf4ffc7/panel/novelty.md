context: Claude Code subagent, fresh context [Sonnet 5.5]

# NOVELTY report, earth-moon-biplanar-10-chromatic, partial win p2

## Fetch log (UTC, URL, HTTP, sha256)
- 2026-11-18T17:31:11Z https://teorth.github.io/optimizationproblems/constants/27b.html 200 c62b3145e7db5cfc8e3bf9531a029cac3b4ed7f9b30bbf6885a943005ff275ea
  Value: lower bounds listed 8 [R1959] and 9 (Sulanke, join of K_6 and C_5, [G1980]); upper bound 12. Hash matches the-record-we-beat/status_snapshot.md.
- 2026-11-18T17:31:14Z https://epoch.ai/frontiermath/open-problems/earth-moon 200 69d429f7dbaf287fe29b2b9a3227a39ea3bf65d65e391ec5c101034e1a90e2b4
  Value: "Unsolved"; lower bound 9 (Sulanke 1980), upper 12. Hash differs from the package's (92a7c769...), as expected for a dynamic site page; the status is the same.
- 2026-11-18T17:32:01Z https://api.github.com/repos/Volkopat/earth-moon-biplanar/git/trees/HEAD?recursive=1 200 8ce4e9371e99dc586837d145119460a0b073283952c31ad4acffb23c4c0da866
- 2026-11-18T17:32:01Z https://zenodo.org/api/records/22103613 200 afe5a3025375935fb4ea238e717d49919431197602f61eada3856f253f334059
- 2026-11-18T17:32:02Z https://zenodo.org/api/records/23113159 302 (redirects to record 23173013)
- 2026-11-18T17:32:08Z https://zenodo.org/api/records/23173013 200 5f85b4bdd83f896a57346234579176c2b85197a7d4f54e4bea59fe0e652319ee
- 2026-11-18T17:32:28Z https://academics.hamilton.edu/mathematics/dboutin/ThicknessTwo.pdf 200 34620ae3e069e5ecd11af64a26c581332132f9e502246b72e079e994b5a76d17 (BGS Part One preprint)
- 2026-11-18T17:32:36Z dlib.si PDF and Springer PDF for Part Two: HTTP 200 but both returned HTML paywall pages (sha256 e845eec8..., 43d2b7ae...). Part Two full text NOT read.
- Also two web searches (Part Two; 2026 9-critical biplanar); results only restated abstracts.

## Findings
1. Published 9-critical thickness-two graphs found: Sulanke K_6+C_5 (n=11); BGS Part One, 40 graphs on n=12..16 (preprint: first Hajos sum of two Sulanke graphs has 21 vertices); Gethner-Sulanke Part Two (abstract only): new 9-critical graphs on 17, 25 and 33 vertices. No source found with a 9-critical biplanar graph on 19 vertices.
2. Patil's repository tree (286 entries, 248 of them graph files): by filename the vertex counts are 11:5, 12:13, 13:77, 14:47, 15:10, 16:13, 18:3, 20:13, 21:24, 22:11, 23:13, 24:4, 25:4, 29:1, 31:2. No n=19 file. Filenames only; edge lists were not downloaded or canonicalised. Patil's Zenodo record 22103613 describes 241 graphs: the 40 BGS graphs plus Hajos sums and edge swaps.
3. Spogreev (record 23113159 now redirects to 23173013, v1.1.0, line graphs and joins with fractional chromatic number at most 9): no 19-vertex critical graph.
4. Trivial-edit check. A 9-critical graph is minimal, so it is no proper subgraph of a published 9-critical graph. Hajos sums and Ore compositions have a vertex separator of size 2. I recomputed from object/biplanar_9crit_n19_e92.json with my own stdlib code: n=19, 92 edges, degrees 8..12, no vertex separator of size 4 or fewer (kappa at least 5), clique number 8. So it is not a Hajos or Ore composition of anything. The package's argument "Hajos needs n at least 21" overlooks a K_9 summand (9+11-1=19), but BGS Proposition 3 gives thickness = max of the summands, K_9 has thickness 3, so those sums are not biplanar; kappa at least 5 excludes them anyway. Patil's edge-swap graphs are on n=13..16, so no seed of order 19.
5. Repository check: 1114 pull requests (all states) listed read-only; none mentions earth-moon or biplanar (only unrelated apollo-moonquake claims match "moon"). TROPHY_CASE.md, the repository's known-knowns folder and bank: no hits for earth-moon or biplanar in a recursive grep of the clone.
6. Status unchanged: both pages show best lower bound 9, so no equal-or-better upstream value overtakes the claim. p2 does not require a record, only a graph not in the published lists.

## Bar judgement
p2 bar literally: "not isomorphic to any graph in Boutin-Gethner-Sulanke's published lists". Part One has orders 12..16 only, Part Two orders 17, 25, 33 (abstract). A 19-vertex graph cannot be isomorphic to any of them, so the bar is met by order alone. No later list found that supersedes it.

## Limits
- Gethner-Sulanke Part Two full text was paywalled; I rely on its abstract. "Alalqam 2012" could not be found by search; not confirmed to exist or to contain a 19-vertex graph.
- Patil's corpus checked by filename vertex counts only.
- Gethner's 2018 survey chapter not read.
- Biplanarity, 9-chromaticity and criticality are other roles' checks; here I verified only n, m, degrees, kappa and omega.

confirmed_scope: Among Sulanke (n=11), BGS Part One (n=12..16), Gethner-Sulanke Part Two (abstract: n=17, 25, 33), Patil's corpus (no n=19 file) and Spogreev, no published 9-critical biplanar graph has 19 vertices, and the claimed 5-connected 92-edge graph is not a Hajos or Ore composition, so the p2 non-isomorphism clause holds as stated; its criticality and biplanarity were not assessed in this report.

pass: true
