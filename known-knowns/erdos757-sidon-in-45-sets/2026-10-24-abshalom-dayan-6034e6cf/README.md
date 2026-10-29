# erdos757-sidon-in-45-sets: partial win p2, an abstract hypergraph with alpha/n = 56/101

## What
The explicit 101-vertex, 99-edge 3-uniform hypergraph in H.json is linear, F7-free, has pairwise distinct label-order middles with none at vertex 0 or 100 (so m = n - 2), and has exact independence number 56, so alpha/n = 56/101 < 5/9 < 4/7, meeting partial win p2 as an abstract hypergraph that satisfies the properties arXiv:2602.23282 proves (Lemmas 2.4, 2.5, 5.2) while being provably not the A.P.-hypergraph of any weak Sidon or (4,5)-set and giving no bound on c*.

Note: the sentence above is quoted word for word from `panel/gate.md` (`confirmed_scope`).

Path note: the panel files and the PREREG files refer to the run's claim folder `claim/`. There, `claim/H.json` and
`claim/construction.json` are `object/H.json` and `object/construction.json`, `claim/CLAIM.md` is `README.md`,
`claim/REPRODUCE.md` is `RUN_IT_YOURSELF.md`, `claim/code/` is `how-we-built-it/code/` and `claim/scout_record.md` is
summarized in `the-record-we-beat/RECORD.md`. `claim/paper/` (the fetched arXiv text and HTML, third-party) is not
shipped; its URL, fetch times and sha256 are in `the-record-we-beat/RECORD.md`. The other work files named there
(the skeptics' own scripts and logs, `out/`, `data/`, `target.md`, `GOAL.md` and the run's notes) are not shipped.

Claimed as partial win p2. What it shows: the structural properties Ma and Tang
prove for A.P.-hypergraphs of (4,5)-sets (linear, F7-free, injective middles with none at the ends) do not by
themselves force alpha/n >= 5/9, so a lower-bound proof that uses only them cannot reach 5/9. The margin under 5/9
is 1/909. H is the 9-copy chain of one 13-vertex block glued on 2 vertices per step (object/construction.json); the
chain family has limit 6/11.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS` (exit 0). Needs python3 only (standard library, no network). Under a second on a laptop.
It calibrates on the A.P.-hypergraph of the paper's 14-point set A_base (alpha 8), then checks every property of
object/H.json and computes alpha exactly.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| arXiv:2602.23282 v2 (bank status_source) | Theorem 1.6 upper bound on c*, from A_base (h = 8 of 14) | 4/7 | https://arxiv.org/html/2602.23282 | 2026-10-24T12:31:38Z |
| erdosproblems.com/757 | stated bounds | 9/17 <= c <= 4/7 | https://www.erdosproblems.com/757 | 2026-10-24T12:31:39Z |
| Erdos Problem a Day (community record, outside the named sources) | reader's self-similar family | finite ratios (7+5K)/(11+9K), limit 5/9 | https://erdosproblemaday.com/day/757-reader-five-ninths-refereed | 2026-10-24T12:31:40Z |
| EinsteinArena "Sidon Subsets of (4,5)-Sets" (named in the bank criterion) | leaderboard top | 0.571428571 | https://einsteinarena.com/problems/sidon-45-set | see the-record-we-beat/RECORD.md |

56/101 = 0.55446 is below 4/7 = 0.57143 and below 5/9 = 0.55556 (504 < 505), and below every finite ratio known for a
real (4,5)-set: the reader's family gives (7+5K)/(11+9K), decreasing toward 5/9 and never reaching it (37/65 at
K = 6, 47/83 at K = 8). The literal 4/7 bar of p2 was already met by that family's real 65-point set (37/65); what
is new here is a value below 5/9. Open PR #406 (as of 2026-10-25) is a 4/7 tie with a real set and does not overlap
with this claim. Snapshot details: the-record-we-beat/RECORD.md.

## Not claimed
- H is not the A.P.-hypergraph of any (4,5)-set or weak Sidon set: an 8-vertex piece of every copy, the induced
  subhypergraph on {1,2,3,4,95,97,98,99} with edges (1,2,4), (1,3,98), (3,4,95), (2,95,97), (3,97,99), (2,98,99),
  forces two points to coincide or an extra 3-term progression for every allowed choice of middles. No script for
  this check is shipped in this package.
- No bound on c*: the main success criterion (a finite integer set below the live best) is not met.
- No claim about the infimum of alpha/n over the abstract class (the chain family gives at most 6/11; nothing is
  claimed below that or about tightness).
- Not checked: the full text of Henning and Yeo (2021) was not available to the panel (closed access).

Corrections to the panel text:
- The sentence quoted under "What" (from `panel/gate.md`) says "(so m = n - 2)". Distinct middles that avoid the two
  ends only give m <= n - 2; here m = 99 = n - 2 holds as a separately counted fact, not as a consequence.

## Credits
- J. Ma and Q. Tang, Largest Sidon subsets in weak Sidon sets, arXiv:2602.23282 (v2, 6 Mar 2026), https://arxiv.org/abs/2602.23282 : the A.P.-hypergraph properties (Lemmas 2.4, 2.5, 5.2), A_base and the 9/17 and 4/7 bounds.
- A. Gyarfas and J. Lehel, Linear sets with five distinct differences among any four elements, J. Combin. Theory Ser. B 64 (1995), 108-118, https://doi.org/10.1006/jctb.1995.1028 : the A.P.-hypergraph framework and F7.
- M. A. Henning and A. Yeo, Affine Planes and Transversals in 3-Uniform Linear Hypergraphs, Graphs and Combinatorics 37(3) (2021), 867-890, https://doi.org/10.1007/s00373-021-02285-x : the transversal bound behind 9/17.
- The anonymous reader and Erdos Problem a Day, https://erdosproblemaday.com/day/757-reader-five-ninths-refereed : the 5/9 family and the 2-point chain idea this run generalized.
- hturcotte1/Erdos-757, https://github.com/hturcotte1/Erdos-757 : verification of the reader's family, the seed census, and open question Q5 on the abstract-class constant.
- Erdos Problems (T. Bloom), https://www.erdosproblems.com/757 , and EinsteinArena "Sidon Subsets of (4,5)-Sets", https://einsteinarena.com/problems/sidon-45-set .
- Google OR-Tools CP-SAT, https://github.com/google/or-tools , and PySAT, https://github.com/pysathq/pysat (how-we-built-it/).
- Contributor: Abshalom Dayan (V3R1T4S run).
