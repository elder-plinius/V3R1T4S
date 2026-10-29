# CRITERION skeptic: erdos757-sidon-in-45-sets, claimed partial win p2

context: subagent (fresh context, given only claim/)

Inputs read: claim/CLAIM.md, claim/H.json, claim/construction.json, claim/REPRODUCE.md, claim/scout_record.md,
claim/code/check_p2.py, claim/code/chain_build.py, claim/paper/arxiv_2602.23282_v2.txt (all of it) and
claim/paper/arxiv_2602.23282_v2.html (cross-checked: sha256 6b668ce6...4608 matches the scout record; the same 28
numbered statements appear in html and text; the F7 edge list in the html is {012,034,056,135,246}). No text addressed
to reviewers was found in any claim/ file or in the paper.

## Bottom line

The claim meets partial win p2 literally, and that is the only win claimed. The full success criterion is not met and
is not claimed: there is no set A of integers, so items (1) to (4) and (6) are not in play. Every property p2 asks for
holds on H.json under my own independent checks. alpha(H) = 56 is exact (six methods agree). 56/101 is strictly below
4/7 (the live best on the criterion's named sources) and also below 5/9 (the community record in the scout record). The
paper neither exhibits nor excludes such an H. The main caveat, which the claim discloses itself: H is provably not
the A.P.-hypergraph of any weak Sidon set or (4,5)-set, so it is a "frozen abstract target" only in the sense the p2
wording allows (it satisfies the paper's proven necessary conditions). It cannot be realized and gives no bound on c*.

## Texts judged against (verbatim from claim/CLAIM.md)

- p2: "A frozen abstract target: an explicit 3-uniform hypergraph H on n vertices that satisfies every structural
  property arXiv:2602.23282 proves for 3-AP hypergraphs of (4,5)-sets (linear, F7-free, at most n-2 edges, and any
  further listed condition, each checked by script against the paper), with exact independence number alpha(H) and
  alpha(H)/n strictly below the live best ratio. The skeptic must confirm that the paper does not already exhibit or
  exclude such an H."
- "Live best ratio": criterion item (3) defines it as the best upper bound on c* shown at erdosproblems.com/757, on
  the EinsteinArena leaderboard and in any newer arXiv paper (4/7 on 2026-10-03). Per claim/scout_record.md
  (2026-10-24) the first two still show 4/7. The community self-similar family (blog plus GitHub, outside the named
  sources) gives c* <= 5/9 as a limit.
- The claim (CLAIM.md): n = 101, m = 99; linear; F7-free; distinct middles in label order, none at 0 or 100, so
  m <= n-2; alpha = 56; 56/101 < 5/9 < 4/7. "Not claimed": not realizable, no bound on c*.

## Every structural property the paper proves for A.P.-hypergraphs of (4,5)-sets

I read the whole paper for hypergraph-level statements that hold for H(A) when A is a (4,5)-set. Prop 2.2 makes every
(4,5)-set weak Sidon, so the weak-Sidon lemmas apply. The list in Section 1.3 ("linear, ... distinct middle points
(with respect to the natural order on R), and ... F7-free") is complete: nothing else in the paper is a property of
H alone. Lemma 2.3 (h(A) = alpha(H)) links A to H. Lemmas 3.x are about sets. Section 4.1 is about the weak Sidon
family A_{2n+1}.

| Property | Source in paper | H.json | My check |
|---|---|---|---|
| 3-uniform, edges are triples a_i<a_j<a_k | Definition 1.7 | yes: 99 distinct 3-sets in 0..100 | direct |
| midpoint map injective | Lemma 2.4 (weak Sidon; via Prop 2.2) | yes: 99 distinct middles (middle label of each sorted triple) | direct |
| midpoint never a_1 or a_n | Lemma 2.4 proof | yes: middles are exactly 1..99 | direct |
| m <= n-2 | Lemma 2.4 | 99 = 101-2 (tight: every interior vertex is a middle) | direct |
| linear | Lemma 2.5 | yes: every vertex pair lies in at most one edge | pair count |
| no subhypergraph isomorphic to F7 (not necessarily induced) | Lemma 5.2 (from [5]); F7 as in Section 1.3 | yes | two new methods (below) |
| 4 tau <= n + m (any 3-uniform) | Theorem 4.6 | 180 <= 200 | consequence, holds |
| 17 tau <= 5n + 3m | Theorem 5.3 (Henning-Yeo) | 765 <= 802 | consequence, holds |
| alpha >= 9n/17 | Theorem 1.6 proof | 56 >= 53.47 | consequence, holds |

How I checked F7-freeness, independently of claim/code/:
(a) "link" method: F7 is two disjoint edges e, f plus a vertex c outside both whose link (a matching, by
linearity) maps e onto f. It found 0 copies.
(b) networkx subgraph monomorphism of the typed vertex-edge incidence graph of F7 into that of H. It found none.
Positive controls: both methods find F7 in F7 itself and in a relabelled F7 inside a 20-vertex hypergraph. They agree
on 300 random linear hypergraphs (108 positives). Both report the A.P.-hypergraph of the paper's A_base as F7-free.

How I certified alpha(H) = 56 exactly (panel_work/criterion/crit_check.py):
- RC2 MaxSAT gives 56, with a witness I checked is independent.
- SCIP MIP gives 56, status OPTIMAL, bound 56.
- Exact bucket elimination over a min-degree order (induced width 6) gives 56.
- Cross-check: on 300 random hypergraphs with n <= 14, all three methods match brute force.
- The author's claim/code/check_p2.py, rerun by me, says P2_CHECK: PASS: CP-SAT OPTIMAL 56/56, pysat UNSAT at 57,
  and the author's DP gives 56.
- On A_base, my methods return h = 8 (the calibration value of Lemma 5.1).
- I rebuilt H from claim/construction.json under my own reading of its description: 101 vertices, 99 edges,
  isomorphic to H.json.

Ratio comparisons in fractions.Fraction:
- 56/101 < 4/7 (392 < 404).
- 56/101 < 5/9 (504 < 505). The margin is 1/909: tiny, but strict and exact.
- 56/101 >= 9/17, so there is no contradiction with Theorem 1.6.

## Hidden quantifiers and stretched definitions

- "for all n" / "in the limit": the claim concerns one finite H (the K = 8 chain). The chain family tends to 6/11
  (alpha = 8+6K, n = 13+11K; first member below 5/9 at K = 8), but no limit is claimed. Nothing hidden.
- "Realizable": p2 says "abstract" and asks only for the properties the paper proves. The paper proves no
  realizability criterion beyond them, so realizability is not required by the wording. The claim says plainly that
  H is not realizable, and I confirmed it with exact rational linear algebra (panel_work/criterion/rebuild_realize.py):
  - The induced subhypergraph on {1,2,3,4,95,97,98,99} has exactly the six edges listed in CLAIM.md.
  - The paper's Lemma 2.4 requires distinct middles. For every one of the 95 choices of middles that respects it, the
    solution space of x_a + x_c = 2 x_b has dimension 2 (the points are fixed up to an affine map). In every case it
    forces two points to coincide or forces an extra 3-AP.
  - The bare 13-vertex block behaves the same way: all 563 such choices are degenerate.
  - So H is not H(A) for any weak Sidon set A, and in particular for no (4,5)-set.
  This does not break p2's wording, but it narrows what H is: a certificate that the paper's listed properties do not
  force alpha/n >= 5/9, not a candidate (4,5)-set.
- "Middles" in an abstract hypergraph: Lemma 2.4 speaks of AP midpoints in the real order. The claim stands in the
  vertex labels for that order, and the middle of each sorted label triple for the midpoint. That is the faithful
  abstraction, and with it every interior label is the middle of exactly one edge.
- "F7-free" is the non-induced notion ("contains no subhypergraph isomorphic to F7"). Both of my methods test the
  non-induced notion.
- "Live best ratio": strict below under both readings, 4/7 (the named sources) and 5/9 (the community record).
  Residual gap: claim/scout_record.md does not document a search for newer arXiv papers other than 2602.23282
  (only that v2 is its latest version). A newer arXiv bound at or below 0.5545 would change the comparison. I had
  no web access and did not check this.

## Null models

- Random ordered hypergraphs with the same constraints (each interior vertex the middle of at most one edge,
  linear, F7-free; panel_work/criterion/nullmodel.py):
  - n = 16, 20, 30 (300 samples each): minimum alpha/n of 0.625, 0.65 and 0.667.
  - n = 101 (1000 samples, all with m = 99): minimum alpha 69 (0.683), mean 71.2.
  - A naive local search minimizing alpha (3 runs x 3000 moves) reached only 5/8, 13/20 and 19/30 at n = 16, 20, 30.
    At n = 101 (3 runs x 1000 moves) it reached 68/101 (0.673), against 56 for H.
  - None came near 4/7, so a trivial or random construction does not meet the wording.
- The paper's own low-ratio family A_{2n+1} (Section 4.1; ratio (n+1)/(2n+1), below 4/7 from N = 9) fails p2: its
  A.P.-hypergraph is never linear (Lemma 4.4 edges {X_i,X_{i+1},Y_i} and {X_i,Y_i,Y_{i+1}} share two vertices), and
  it is not a (4,5)-set (checked N = 5..15).
- Known construction from claim/scout_record.md (O, phi, S_K): I rebuilt it in exact rationals.
  - |S_K| = 11+9K and alpha = 7+5K for K = 0..9. Each S_K is linear.
  - S_6 is a (4,5)-set (all C(65,4) quadruples checked), with alpha/n = 37/65 < 4/7.
  - So at the literal 4/7 bar, the p2 wording was already met by a known and even realizable object.
  - But every S_K ratio is above 5/9: 9(7+5K) > 5(11+9K). The claimed H is the only object here below 5/9.

## Subsumption

- The paper does not exhibit such an H. A_base gives exactly 4/7, which is not strictly below. The A_{2n+1} family
  is not linear. F7 is excluded by definition.
- The paper does not exclude such an H. Its only lower bound is 9/17 (Theorem 1.6, via Theorem 5.3), and
  56/101 > 9/17. The non-realizability argument above is not in the paper.
- claim/scout_record.md: every finite ratio recorded there is above 5/9 (the S_K family; C004 33/58; C005 38/67), and
  no abstract hypergraph is recorded. So 56/101 is not subsumed by anything in my inputs.
- Outside my remit: whether the Henning-Yeo paper [6] or other literature already gives linear, F7-free, distinct-
  middle hypergraphs with m <= n-2 and alpha/n < 5/9 (for example tight examples for 17 tau <= 5n + 3m). The paper does
  not say. That is for the novelty review.

## Concerns (not disqualifying under p2's wording)

1. H is provably unrealizable. Its value is as a barrier: any proof using only the paper's listed properties cannot
   give c* >= r for r > 56/101. It is not a set to be realized, and it says nothing about c*.
2. The margin under 5/9 is 1/909, and only the K = 8 member of the chain is claimed.
3. No search for newer arXiv bounds is documented in the scout record.

confirmed_scope: The explicit 101-vertex, 99-edge 3-uniform hypergraph in H.json is linear, F7-free, has pairwise distinct label-order middles with none at vertex 0 or 100 (so m = n - 2), and has exact independence number 56, so alpha/n = 56/101 < 5/9 < 4/7, meeting partial win p2 as an abstract hypergraph that satisfies the properties arXiv:2602.23282 proves (Lemmas 2.4, 2.5, 5.2) while being provably not the A.P.-hypergraph of any weak Sidon or (4,5)-set and giving no bound on c*.

pass: true
