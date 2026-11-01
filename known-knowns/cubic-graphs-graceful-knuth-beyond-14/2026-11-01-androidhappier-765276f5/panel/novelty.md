# Novelty skeptic: cubic-graphs-graceful-knuth-beyond-14

context: subagent (Grok Bot Task executor)

Inputs read: CLAIM.md, REPRODUCE.md, checkers/glab.c, checkers/run_all.sh (grep only), result/cert_{16,18,20,22}.txt (line counts only).
The claim is criterion (a): every connected cubic graph on 16, 18, 20 and 22 vertices is graceful, with one certificate per order.
Line counts I measured: cert_16.txt 4,060; cert_18.txt 41,301; cert_20.txt 510,489; cert_22.txt 7,319,447 (these match A002851; correctness is for the other panels to check).

## Status fetch (one GET each, User-Agent "V3R1T4S-research-agent", no cookies, no retries)

| URL | time (UTC) | HTTP | sha256 | value read |
|---|---|---|---|---|
| https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6 | 2026-11-01T16:56:19Z | 200 | 4acc9fa4dcea3c7c804e2765f7091641ae7be7ffff7b1ffbcf0d7137e763cdb5 | "#DS6: Oct 30, 2025" (current edition); DC.Date.modified 2026-01-27 (metadata only) |
| https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS6/pdf/ | 2026-11-01T16:56:20Z | 200 | b1b5d8ba828b3fcd7eb4d73402b63252bd06b59bdcfb4f32f558f8af5898842e (same as the scout's hash) | "Twenty-eighth edition, October 30, 2025". Section 2: "Knuth [1863] proved by way a computer search that all cubic graphs on 4, 6, 8, 10, 12, or 14 vertices, except 2K4 and 3K4 ... are graceful." **DS6 bound: 14.** |
| https://www-cs-faculty.stanford.edu/~knuth/fasc7a.ps.gz | 2026-11-01T16:56:23Z | 200 | 24ab2d899b0ab91c25c1d760b3ba5afef09e89dbc7c80c94047fed26cfcb255d (same as the scout's hash; PS dated Dec 5, 2024) | Answer to ex. 96: "With considerably more computation, the results of exercise 95 can be extended to the 204,154,267,353 graceful labelings of cubic graphs on 16 vertices. There are 4207 such graphs, of which 4060 are connected. The evidence is overwhelming: ..." **Knuth bound: 16.** |
| https://cs.stanford.edu/~knuth/papers/coups.pdf ("Coups de gr\^aceful graphs", rev. 02 Jan 2026) | 2026-11-01T16:58:40Z | 200 | (not pinned) | Only KP/KC clique-path graphs. Nothing on cubic graphs past 16. |

The HTML page hash differs from the scout's (dynamic OJS page). The PDF hash and the edition are unchanged.

## Literature and code search (last 24 months and older)

- Kennedy, "An Algorithmic Exploration of Gracefully Labeling Cubic Graphs", Macalester honors project 2021: "true for cases of graphs with 16 vertices or fewer". Bound: 16.
- OEIS A337965 (total graceful labelings of cubic graphs on 2n vertices): ends at a(8) = 204,154,267,353, i.e. 16 vertices.
- No paper, preprint or survey I found (web search for 18/20/22-vertex graceful cubic verification, arXiv, SAT/CP 2025) reports a verification past 16 vertices. Nearby results are about other properties and do not overlap: cubic leaves at 16/18/22 (Australas. J. Combin. 61), the 3-decomposition conjecture up to 28 vertices (CP 2025), and Knuth's KP-graph paper.
- GitHub code and repo search ("graceful 41301", "graceful 510489", "graceful cubic geng", repo search "graceful cubic"): no certificate or claim for cubic graphs on 18 or more vertices. The hits I checked (BrettKnox/open-problems-lab, Joe975/math-lab) cover graceful trees only (up to 18 and up to 14).
- This repo: TROPHY_CASE.md has no graceful or cubic entry. known-knowns/ has no graceful-cubic folder. PRs on elder-plinius/V3R1T4S (searched "graceful" and "cubic", open and closed): the only graceful PR is #880 (odd-graceful trees, a different target). The "cubic" PRs are dimer, percolation, Potts and Erdős 699, all unrelated. No prior PR claims this target.
- Release assets: no repository with releases on this topic turned up. The one certificate release I saw (CharanRayudu odd-graceful-certificates) is about trees.

## Comparison with published objects (this cell and its neighbours)

- Order 16 (neighbouring cell, published by Knuth fasc. 7A and Kennedy 2021): **not new**. cert_16.txt ties a known result and earns no credit.
- Orders 18, 20 and 22: no published labeling or verification exists for any of them. Trivial edits of a published object cannot produce these certificates. Deletion, restriction, relabelling, symmetry and local polish of the 16-vertex data do not yield graceful labelings of 18-, 20- or 22-vertex cubic graphs. Each order is its own exhaustive class and needs a separate labeling for every graph. glab.c says it is an edge-driven randomized backtracking search run on fresh geng output, and grep found no seed, import or reference to Knuth or Kennedy data. So the certificates are not seeded from a published object.
- Result versus the best known: the best published verification bound is 16 vertices (Knuth, Kennedy; DS6 still says 14). The claim covers every connected cubic graph on 18, 20 and 22 vertices. That strictly beats every known bound (largest order verified goes from 16 to 22), so it is not a tie.

## Caveats

- This is a novelty verdict only. The validity of the labelings and the canonical-form coverage were not checked here.
- An unindexed private verification (for example in Knuth's unpublished notes) cannot be ruled out. Knuth's own answer stops at 16 and calls it "considerably more computation".
- Credit applies to orders 18, 20 and 22 only, not to 16.

novelty: NEW for orders 18, 20, 22 (known bound 16: Knuth fasc. 7A ex. 96, Kennedy 2021; DS6 28th ed. says 14); order 16 is not new.

pass: true
