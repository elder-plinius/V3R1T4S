# Hostile referee report on PROOF.md (sha256 425cb1e7...1879)

Reviewer: a fresh subagent that read only PROOF.md. It did not see the code, outputs, notes or earlier reviews.
Date: 2026-10-19. The harness blocks subagents from writing report files, so the main session saved this text verbatim
from the reviewer's hand-back. Scratch script: audit/hostile/scratch/attack.py (one core, under a minute).

The main session confirmed the main finding independently. The literal definition admits exactly 6
non-self-avoiding walks at N = 2 and none at N = 1, 3, 4 or 5. The enumerator (onPath check) and the package's
check_fast.py both require self-avoidance, and the certificate tables start at N = 3. No number changes.

## Summary (reviewer)
The proof survives. The verdict is GAPS (fixable). The argument holds for N = 20, which is what the Theorem uses,
and there is no counterexample at N = 20. One definition is wrong at N = 2, and several standard steps are stated
without proof.

Most serious finding. The NAW definition on line 9 ("v_i ~ v_j only for |i-j| = 1") does not imply self-avoidance
at N = 2. The walk (0, e, 0) passes it, because v_0 = v_2 and a site is not adjacent to itself.
- So "in particular it is self-avoiding" is false at N = 2.
- Lemma 4 is then literally false at N = 2. (0,+x,0) and (0,-x,0) lie in the same orbit, and the "turn" compares
  two directions on the same axis, where the index depends on the sign. The first walk gets |F| = 0; the second
  gets F = {+x}, |F| = 1.
- The same false remark is used in three other places: the "not opposite" step of Lemma 0; Lemma 3's "N+1+|F|
  distinct sites" at N = 2; and Lemma 2's "hence a NAW: y not in gamma" at N = 1.

None of this changes a number:
- For N >= 3 the definition forces self-avoidance: a repeat v_i = v_{i+2} would leave v_{i-1} or v_{i+3} adjacent
  to it at index distance 3.
- The 6 bad walks have E empty, so they add nothing to K_2 or to c_f.
- Tree paths are self-avoiding anyway, because d(v_k) = k (Lemma 1(a)).

Fix: add "self-avoiding" to the NAW definition, and use d(y) = N+1 for "y not in gamma" in Lemma 2.

## (a) Coverage (Lemma 2): HOLDS (fix needed only at N = 1)
- T is a tree: each x in C(0)\{0} has exactly one parent, and d drops by 1 along each parent edge, so following
  parents reaches 0. T is therefore connected and acyclic.
- Koenig applies: every vertex has at most 6 neighbours, so T is locally finite, and on the event its vertex set
  C(0) is infinite. The rooted form gives a ray with parent(v_{m+1}) = v_m.
- y = v_{N+1} is in E(gamma). It is adjacent to no v_i with i < N, by Lemma 1(b) for the tree path of length N+1.
  It is open, so it is not in F, which is closed.
- "y not in gamma" at N = 1: the proof takes this from the false self-avoidance remark. Use d(y) = N+1 > N instead.
- The tail avoids gamma and F: tail sites have d > N, so they are not in gamma; they are open, so they are not in F.
  They are distinct because their d values differ.
- Experiment: 1,280 tree paths in 18 random configurations at p = 0.30, 0.45 and 0.60. No failures: every next
  vertex was in E, and every tree descendant avoided gamma u F.

## (b) Forced-closed set (Lemma 1(c)): HOLDS
- Shortcut sites: if w is open, then d(w) <= i+1, so d(v_j) <= i+2 < j, a contradiction. The gap is applied to the
  right indices.
- A gap of 2 would be wrong. The only common neighbour of v_i and v_{i+2} other than v_{i+1} is the turn corner,
  which is why C exists.
- Turn corners: if u is open, then d(u) <= k and k+1 <= d(u)+1, so d(u) = k and u is in P(v_{k+1}). The corner rule
  compares directions seen from v_{k+1}, exactly as the parent rule does (dirindex(w - x) with x = v_{k+1}).
- Boundaries:
  - k = 1 works: u_1 ~ 0 and d(u_1) = 1.
  - k = N-1 uses parent(v_N) = v_{N-1}, which the tree-path definition gives.
  - There is no corner at k = 0 or k = N. That is fine, because F only needs to be a subset of the forced-closed
    sites.
  - The origin is never in F.
  - A shortcut site next to the origin works: i = 0 gives d(v_j) <= 2 < 3.
- Experiment: 0 failures with the rules as written.
- Mutation tests: a gap of 2, or a reversed corner inequality, produced open "forced" sites in 174 of 340 paths, so
  the test can detect such errors.

## (c) Disjointness and independence: HOLDS; one standard step not argued (GAP, trivial fix)
- Lemma 0: the conclusion is true, but one step of its proof needs self-avoidance (see g1).
- Measurability of B: the proof never shows that B depends only on sites outside gamma u F. Fix: write
  B = {y open} intersected over n with {y is joined to the boundary of Lambda_n by an open path in Z^3 \ (gamma u F)},
  using Koenig for locally finite graphs. Each term is a finite cylinder on sites outside gamma u F, so product
  measure gives independence from A.
- The tree never enters A or B; it is used only to prove the inclusion of events.
- P(B) <= theta: B is contained in {|C(y)| = infinity}, since restricting to a subgraph only shrinks the event.
  Translation invariance then gives theta.
- P(A) = p^{N+1} (1-p)^{|F|} needs gamma to be self-avoiding, which Lemma 0 does not supply. It fails only for the
  bad N = 2 walks, which have E empty.

## (d) Counting: HOLDS
- The finite union bound gives sum over gamma of |E(gamma)| p^{N+1} (1-p)^{|F|} theta = K_N theta.
- Overcounting in E is harmless, and E always contains the true next vertex.
- The condition "y not in F" in E is redundant: every site of F has a path neighbour with index below N (v_i with
  i <= N-3 for S, v_{k-1} for a corner).

## (e) Lemma 4: GAP at N = 2 (literal counterexample above); HOLDS for N >= 3, including N = 20
- At a turn the two directions are perpendicular, so the comparison is between two different axes. Indices 2a and
  2a+1 are both below every index of a higher axis, and flips preserve axes.
- The corner map commutes with g by linearity (used but not stated).
- Flipping a used axis moves some vertex, so the stabilizer is the set of flips of unused axes, and the orbit has
  2^{|A|} elements.
- Exactly one member has a positive first step along every used axis.
- Experiment, N = 1..7, over all literal NAWs (6, 36, 126, 534, 2214, 9246 and 38142 walks):
  - flip violations only at N = 2 (24), all from the bad walks;
  - every orbit has size 2^{|A|} and exactly one canonical member;
  - the orbit formula for c_f equals direct summation for every N.

## (f) Corollary: HOLDS
- theta is a probability, so it is finite; theta <= K theta with K < 1 forces theta = 0.
- Then p lies in {p : theta(p) = 0}, so p_c = sup >= p.
- Monotonicity is needed only for the extra clause about all p' <= p.

## (g) Hidden assumptions
- g1 (GAP): the NAW definition fails at N = 2, as above.
- g2 (HOLDS): tree paths are NAWs. Lemma 1(b) gives the neighbour condition. Self-avoidance comes from Lemma 1(a),
  which the proof does not say.
- g3 (HOLDS): the parent is unique.
- g4: it is implicit that 0 is open, which parent(v_1) needs.
- g5: standard facts stated without proof: measurability, independence, translation invariance, Koenig.
- g6: the certificate depends on main.go, which is outside the proof. The logical claims section 3 makes about it
  are correct:
  - the incremental F equals F(gamma), because a flagged site has path neighbours at indices a < b with b - a >= 2,
    so it could only become v_m with m - a >= 3, which violates the NAW condition;
  - the canonical-sign rule enumerates exactly the canonical walks;
  - the leaf count equals |E|.

## Extra findings
- X1: the "largest passing grid value" remark is justified only on [0, 21/44]. The proof says it is not needed for
  validity, and that is right.
- X2: at p = 1 the formula needs the convention 0^0 = 1.
- X3: nothing in the logic is specific to N = 20. Once g1 is fixed, theta <= K_N theta holds for every N >= 1.

## Wording and notation issues
1. L9-10: "in particular it is self-avoiding" is false at N = 2.
2. L6: p_c lacks the "site" superscript used in the Corollary and the Theorem.
3. L6: monotonicity of theta is used only in a clause that is not needed.
4. L7: say that d is defined only on C(0).
5. L16: "at most 6 children" is true, but non-root vertices have at most 5.
6. L17: it is implicit that each v_{k+1} is in C(0)\{0} and that 0 is open.
7. L17/19: "tree path of length N" and "N-step NAW" are used for the same thing.
8. L21: for the bad N = 2 walk the "turn" is a reversal.
9. L23: "y not in F" is redundant.
10. L29: "|m-(k-1)| <= 1" should be "= 1".
11. L26-27: "not opposite" needs self-avoidance.
12. L34: Lemma 1(b) should say that self-avoidance comes from (a).
13. L42: A_gamma is introduced "for y in E(gamma)" but does not depend on y.
14. L48: "Konig" should be "Koenig" (with umlaut).
15. L50-51: "hence a NAW: y not in gamma" needs self-avoidance at N = 1.
16. L51-52: "are open" appears twice.
17. L58-59: "distinct sites (Lemma 0)": Lemma 0 gives disjointness, not self-avoidance.
18. L60: the measurability argument for B is missing.
19. L56: p = 1 needs the convention 0^0 = 1.
20. L63: "theta(p') = 0 for all p' <= p" is not needed.
21. L72: "step k-1" and "step k" are undefined numbering; they are correct only for 0-based steps.
22. L72: "two different axes" fails at N = 2; after the fix, say "perpendicular".
23. L71: "which gives everything except the corner rule" silently uses that the corner map commutes with g.
24. L75: "the stabilizer is the set of flips of unused axes" would be clearer as "the subgroup of flips supported on
    unused axes".
25. L85-86: "(two path neighbours, or a path neighbour at index distance >= 2)" does not say what the distance is
    measured from.
26. L89: a_20 is not defined.
27. L80/89/90: the certificate depends on external files and is not self-contained.
28. L90: K_20(5/19) is irrelevant to the Theorem.
29. L92: "largest passing value on the 10^-6 grid" is justified only on [0, 21/44].

## Experiments
- Exp1 (NAW definition): exactly 6 non-self-avoiding literal NAWs at N = 2, all with |E| = 0; none at N = 1 or
  N = 3..5.
- Exp2 (Lemma 4): as in (e).
- Exp3 (Lemmas 0-2): all checks passed on 1,280 tree paths built with the parent tree exactly as defined.
- Exp3b (mutation controls): both mutated rules failed, as expected.

verdict: GAPS (fixable)
