# REPRODUCE skeptic verdict: [[35,7,16;14]]_3 (object/eaqecc_35_7_16_14.json)

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Bottom line

PASS. My own exact checker, written from the criterion before I opened claim/checkers/ or claim/rebuild/,
computes from S alone: s = 42, c = rank(S J S^T)/2 = 28/2 = 14, k = 35 - 42 + 14 = 7, and d = 16 exactly. The
search is complete: it lists every vector of span(S)^perp of symplectic weight <= 16 (up to GF(9) scalars). There
is none of weight <= 15, and there are 7762 projective words of weight 16, none of them in the isotropic part. All
values match the JSON (n 35, k 7, c 14, d 16). Every value printed by the author's steps 1, 2, 3, 5 and 6, and by
the one step-4 part I ran (W = 16, part 0), matches REPRODUCE.md. Repeated runs gave identical output. I found no
mismatch, missing object or non-determinism.

| item | claimed (JSON / REPRODUCE.md) | mine (from S alone) |
|---|---|---|
| s = rank_GF(3)(S) | 42 | 42 (S has 42 rows, so its rows are independent) |
| rank(S J S^T) | 28 (c = 14) | 28, so c = 14 |
| k = n - s + c | 7 | 7 |
| dim span(S)^perp / isotropic part | 28 / 14 | 28 / 14 |
| d = min symplectic weight on span(S)^perp minus the isotropic part | 16 | 16 (exact, complete for weight <= 16) |
| vectors outside the isotropic part of weight <= 15 | none (d >= 16) | none |
| projective weight-16 words outside the isotropic part | 7762 (steps 2 and 4) | 7762 |
| step-4 W = 16 per-part counts | 2593, 2556, 2613 | predicted from my list: 2593, 2556, 2613 |

## The definition (quoted from CLAIM.md, success criterion)

> "with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic
> commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors
> in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC
> definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and
> d <= d_upper. Results for c = 0 are excluded"

The conventions come from the object JSON: S rows are (x|z) over GF(3), J = [[0,I],[-I,0]],
<(x|z),(x'|z')> = x.z' - z.x'. Symplectic weight is #{i : (x_i, z_i) != (0,0)}. GF(9) = GF(3)[w]/(w^2 - w - 1),
a + b w coded a + 3b, phi(a + b w) = (a | b).

## What I computed and how (mine/)

Timing of what I wrote: I wrote and ran mine/eacheck.py, mine/mine_bz9.c, mine/test_small.py and
mine/seeded_negative.py before reading any author code. I wrote the cross-check scripts later:
check_json_fields.py, post_compare.py, check_basis.py and check_constructionX.py. They use the same eacheck.py
routines.


- mine/eacheck.py (GF(3) and GF(9) linear algebra in plain Python), from S only:
  - s = rank_GF(3)(S).
  - M = S J S^T (entries <r_i, r_j>), c = rank(M)/2.
  - N = span(S)^perp = nullspace of (-S_z | S_x).
  - I = span(S) ∩ N = { yS : yM = 0 }. Checked: I ⊆ N, I ⊆ span(S).
  - I checked that N (and I) are closed under the GF(3)-linear map (a,b) -> (b, a+b) at every position. That map
    is multiplication by w. So N = phi(C) for a GF(9)-linear code C with GF(9)-dim 14 (2 x 14 = 28 = dim N), and
    symplectic weight equals Hamming weight on C. The hull I is phi of a GF(9) space of dim 7.
- Exact distance: mine/mine_bz9.c, my own Brouwer-Zimmermann style enumerator with two disjoint information sets.
  - C has disjoint information sets I1 = positions 0..13 and I2 = 14..27, each of rank 14, checked by GF(9)
    elimination.
  - Any codeword of weight <= T has weight <= W1 on I1 or weight <= W2 on I2 whenever W1 + W2 >= T - 1.
    Otherwise its weight would be at least (W1 + 1) + (W2 + 1) > T.
  - With T = 16, W1 = 8 and W2 = 7, the program enumerates every message of weight <= 8 on the systematic matrix
    for I1 and every message of weight <= 7 on the one for I2. The first nonzero coefficient is 1. That is
    7,304,564,710 + 1,006,817,254 codewords, a complete enumeration, not a sample.
  - It prints every codeword of weight <= 16. Python rebuilds each word and checks that phi(word) is orthogonal to
    every row of S, recomputes its symplectic weight, and tests membership in I over GF(3).
  - d = minimum weight of a listed word outside I. Run time: 21.5 s, peak memory 16.6 MB.
- Result (mine/object_T16.txt):
  - s = 42, c = 14, k = 7, rank(SJS^T) = 28, dim N = 28, dim I = 14, N_w_closed = True, I_w_closed = True,
    K9 = 14, hull9 = 7.
  - Listed words by (weight, in I): {16, not in I: 7762}. Nothing of weight <= 15, and nothing in I up to
    weight 16.
  - d = 16, with a witness on positions 9,10,12,13,14,16,...,26 (16 positions).
  - Sha256 of the enumerator output: 8894c2c1b8f0e470fef217b48efd54d49547adcbc6a2692a1c414b19f855e5f7.
- Other properties of the JSON (mine/check_json_fields.txt):
  - S == [phi(r), phi(w r) for each row r of D9], in that order.
  - rank_GF(9)(G9) = 14 and rank_GF(9)(D9) = 21.
  - G9 is Hermitian-orthogonal to D9 (sum g_i d_i^3 = 0 for all 14 x 21 pairs).
  - rowspace(G9) equals my C recovered from S.
  - dim(C ∩ C^perpH) = 7 equals my I; [[35, 14-7, ?; 35-14-7]] = [[35,7,?;14]].
  - JSON n, k, c, d = 35, 7, 14, 16.
- The Construction X proof steps, re-derived numerically from my C (mine/check_constructionX.txt):
  - Head code (columns 0..27) has rank 14 and d = 12 exactly (complete list of weight <= 12: 7380 projective
    words).
  - Zero-tail subcode has dim 10 and d = 16 exactly (complete list of weight <= 16: 7440 words).
  - Tail code (columns 28..34) has dim 4, and all 35 of its 4 x 4 minors are nonzero, so it is a [7,4,4] MDS code.
  - So d(C) >= min(16, 12 + 4) = 16. This matches the author's L3, L5, L6 and L7 numbers. The Goppa arithmetic
    also checks: deg(2Q + 8P_inf) = 16 and deg(Q + 8P_inf) = 12 with deg Q = 4; genus 3 gives dims 14 and 10, and
    the bounds 28 - 16 = 12 and 28 - 12 = 16.
  - I did not independently re-derive the author's identification of these codes as AG codes on a specific place
    (L4). The exhaustive result does not depend on it.

## Tests of my checker

- Small brute-force cases (mine/test_small.py, seed 20261025; output: mine/test_small.txt). GF(9)-linear cases
  with n in {6,7}, run through the full pipeline including the C enumerator with a random tight threshold T:
  - 160 cases. 88 have a nontrivial isotropic part. In 34 of them, d_EA differs from the classical minimum
    distance, so excluding the isotropic part matters. 5 random draws were skipped because they had no two
    disjoint information sets.
  - Brute force tested every vector of GF(3)^{2n} for membership in N and enumerated span(S) directly.
  - In all 160 cases, s, c, k, dim N, dim I, the exact set of projective words of weight <= T and d agreed with
    brute force.
  - 150 generic random GF(3) cases (n in {4,5}, 1 to 7 rows): s, c, k, dim N and dim I agreed with brute force,
    and the w-closure detector agreed with brute force (all 150 not w-closed, all correctly flagged).
  - Failures: 0.
- Seeded negatives at full size (mine/seeded_negative.txt):
  - neg1 replaces one GF(9) generator of C by a planted weight-10 vector and rebuilds S' (42 rows) as the GF(3)
    symplectic dual. My checker reports d = 10 on exactly the planted support {2,3,9,11,17,18,20,25,26,31},
    plus c = 16, k = 9, so it is detected.
  - neg2 changes one entry of S. My checker reports c = 15, k = 8, dim I = 12 and N not w-closed, so it is
    detected.
- Determinism: a second run of my checker on the object gave a byte-identical report and an identical enumerator
  output (same sha256).

## The author's steps (run in authorrun/, a copy of claim/, so that claim/ stays unmodified)

Object sha256 (claim/object/eaqecc_35_7_16_14.json): e3d6a8cad3db3a6ea28262ced2969b03a429b1ede488ae9cd59b69f5055b73b4 (as stated).

| step | expected (REPRODUCE.md) | printed | match |
|---|---|---|---|
| 1 rebuild | X code [35,14] hull=7 -> [[35,7,?;14]]  S 42x70  D9 21x35; sha256 e3d6a8ca...b73b4 | same line; rebuilt.json sha256 e3d6a8cad3db3a6ea28262ced2969b03a429b1ede488ae9cd59b69f5055b73b4, byte-identical (cmp); a second rebuild gave the same hash | yes |
| 2 prep | n=35 s=42 c=14 k=7 dim_N=28 dim_I=14 N_closed_under_w=True, kappa=14 | n=35 s=42 c=14 k=7 dim_N=28 dim_I=14 N_closed_under_w=True; kappa=14 (2*kappa == dim_N: True) | yes |
| 2 m=20 | deficient=0 in every part; subsets 2004173586, 875699289, 368070285 (sum 3247943160 = C(35,20)) | deficient=0 x3; subsets 2004173586, 875699289, 368070285; sum 3247943160 = C(35,20) (computed) | yes |
| 2 m=19 | deficient 4090, 2343, 1329 (7762) | 4090, 2343, 1329; sum 7762; subsets sum 4059928950 = C(35,19) | yes |
| 3 gf9info witness | weight=16 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False | same | yes |
| 3 witness.py | symplectic_weight=16 orthogonal_to_all_rows_of_S=True in_span_S=False | same | yes |
| 4 prep | n=35 s=42 c=14 k=7 dim_isotropic=14 dim_dual=28 | same | yes |
| 4 W=16 part 0 | examined=1353309650, with_vector_outside_isotropic=2593 | W=16 part=0/3 total_subsets=4059928950 examined=1353309650 with_vector_outside_isotropic=2593 first=0,1,2,3,4,5,6,7,8,9,10,12,13,14,16,17 (1446.18 s real, 1436.29 s user, exit 0); my own GF(3) check of that first subset: dim N_T = 2, dim I_T = 0 | yes |
| 5 bz64 | K=14 n=35 d=16 sets=14,14,4,3 maxw=7 words=4027269016 + weight-16 witness | K=14 n=35 d=16 sets=14,14,4,3 maxw=7 words=4027269016 witness=0 1 0 0 0 0 0 0 0 0 6 5 0 2 8 3 8 1 6 3 4 3 0 5 5 4 1 0 0 0 0 0 0 0 0 (12.16 s); a second run gave identical output | yes |
| 6 goppa_x4 | last line RESULT: d_EA = 16 exactly (theorem-based; no distance search): True; bound min(28-12, 28-16+4) = 16 | last line identical; "L7: d(C) >= min(16, 12 + 4) = 16"; a second run gave identical output | yes |

Cross-checks between the author's outputs and mine:

- All three author witnesses are in my complete list of weight-16 words, are orthogonal to S, and are not in my I:
  the step-3 gf9info word, the step-3 witness.py vector, and the step-5/6 bz64 word.
- The author's basis.txt (step 4 input) checks against my spaces: its first 14 rows have rank 14 and lie in my I,
  and all 28 rows have rank 28 and lie in my N.
- The author's G9.txt (steps 2 and 5 input) spans my C.
- The 7762 deficient 19-subsets of step 2 are the zero sets of my 7762 weight-16 words, whose 7762 supports are
  distinct.
- I assigned each of my 7762 supports its lexicographic index mod 3. That is the part rule of subset_ea64.c, which
  I read after my numbers existed. The prediction is 2593, 2556 and 2613 per part, the same as REPRODUCE.md's
  three W = 16 values.

Not run:

- Step 4 W = 15 parts 0, 1, 2 and W = 16 parts 1, 2: not run, within the budget and slot limits given to me.
  These are not mismatches. My own complete enumeration covers the same statement (no weight <= 15 vector outside
  the isotropic part), and my prediction of the W = 16 per-part counts matches all three stated values.
- Step 7 (network, live table): not run. It belongs to the other skeptics.

## The author's proof steps, re-derived

- Step 2's logic is sound. A nonzero codeword with >= 20 zeros vanishes on some 20-subset, and a rank-14 20-subset
  forces the message to 0. So "every 20-subset has rank 14" is equivalent to d(C) >= 16, and d_EA >= d(C) because
  N minus I lies inside N minus {0}.
- Step 4's logic is sound. dim N_T = dim N - rank(N|OUT), and a vector of N minus I is supported in T exactly when
  dim N_T > dim I_T.
- Step 6's Construction X bound is re-derived numerically above.
- The upper bound d <= 16 comes from an explicit weight-16 vector outside I, found by me and by the author.

## Process notes

- Memory-cap breach (disclosed). The second run of test_small.py brute-forced all 3^14 = 4,782,969 vectors at
  once in int64 for n = 7. It ran 133.67 s and peaked at 2,600,585,592 bytes, which /usr/bin/time -l reports as
  "peak memory footprint" (2.6 GB, above the 1 GB cap). The first run had stopped after 0.53 s on an uncaught case
  and peaked at 162,726,488 bytes. I then chunked the brute force to at most 3^10 vectors at a time. The rerun
  peaked at 601,932,712 bytes. Every other run stayed far below 1 GB: the full-size checker
  peaked at 16.6 MB and the seeded negatives at 21.0 MB.
- Heavy-job count: checked before each long run (2 or fewer each time). All compiled programs had names ending in
  bz9, infoset, bz64 or subset_ea64, were run with nice and had an alarm cap.
- The one background job (the step-4 part; PIDs 22014, 22016 and 22018 recorded in mine/author_step4_pids.txt)
  exited 0 at 04:56:06 UTC. A ps check afterwards showed none of those PIDs left. No job of mine is still running.
- Times (date -u): start 2026-10-25 04:18:10 UTC. My checker printed its numbers at 04:27:07 UTC, and its
  determinism rerun and the seeded negatives finished at 04:28:17 UTC. I first opened the author's code (a grep of
  its import lines, before running step 1) after that, and step 1 started at 04:28:51 UTC. step 4 part ended 04:56:06 UTC. test_small.py was rerun (04:56:32 to 04:57:14 UTC) with the output saved to mine/test_small.txt: same stats, 0 failures, peak 593,757,048 bytes. Step 5 was rerun with identical output (04:57:29 UTC).
- Scope: I did not check the table bounds (d_lower = 15, d_upper = 26 for (35,7,14)) or novelty. Those belong to
  the other skeptics. If the table is as the claim states, 15 < 16 <= 26 holds for my d = 16.

pass: true
