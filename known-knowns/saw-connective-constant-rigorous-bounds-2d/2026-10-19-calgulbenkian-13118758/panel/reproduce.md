# Reproduce report: saw-482-k34p (4.8^2 connective constant, mu <= 169287/92732, loop length 34 with finite-pocket pruning)

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

Role: reproduce. Group phys, cell saw-482-k34p. Files are named relative to the cell folder.

## Verdict
The theorem is PROVED (details below), all seven review fixes are present in the text and the checker, my own independent program reproduces the state count, the kept and pruned move counts and the exact maximum ratio, and the shipped run_checks.sh ends with ALL CHECKS PASS.

## 0. Integrity
- Verified the contributor's hash list from inside the package folder: every line OK (README.md, INDEX.csv, object/*, RUN_IT_YOURSELF.md, the-record-we-beat/*, verify-it-yourself/*).
- Reassembled vector: 13,312,188 bytes, sha256 13118758b86bc0f0daef592d3e85d353851556e54dcd07ad93b6a1c52fc26e54 (matches SHA256_PARTS.txt). Decompressed: N = 16,873,086, version 1, mantissa high byte 128 to 255 (16-bit normalised), exponents 1 to 25, no zero mantissa. So every entry is a positive integer below 2^41 and all arithmetic fits in 64-bit integers exactly.

## 1. Is THEOREM.md proved? Yes. Re-derivation
I re-derived the argument from the statement and AUTOMATON.md and then compared with THEOREM.md.

Soundness of using the state (an ordered subsequence of the true walk) for the tests. Let W = (w_0..w_n) be a bridge, h = x. Suppose at step m < n the state S is tau of a subsequence w_(j_0), ..., w_(j_(L-1)) with j increasing and j_(L-1) = m, and A = tau(w_(m+1)).
- Test 1 removes V(S), a subset of {w_0..w_m}. The tail w_(m+1)..w_n is a path avoiding V(S) (self-avoidance). Every vertex of W has x at most x(w_n) (bridge), so Lemma R gives a strictly x-increasing ray from w_n whose later vertices have x above all of W, hence miss V(S); w_n itself is not in V(S) as n > m. So A lies in an infinite component. Removing fewer vertices than the whole walk only enlarges components, so using the subset is safe (it keeps more moves, never fewer).
- Test 2 removes S_1..S_(L-1) and A, which are tau of w_(j_1)..w_(j_(L-1)), w_(m+1), all with index above j_0. This is exactly where order is needed: the path w_(j_0), w_(j_0-1), ..., w_0 uses only indices up to j_0, so it avoids the removed set, and the strictly x-decreasing ray from w_0 (x(w_0) < x(w_i) for i >= 1) misses all of W after w_0. With an unordered subset the oldest state vertex could have later walk vertices on its way back to w_0 and the argument fails; ordered inclusion repairs this. Correct as written.
- Lemma R: the neighbour tables give every vertex a neighbour of strictly larger and one of strictly smaller x and y. The text now says the ray avoids F after its first vertex. Correct.

Lemma P at the seeds: for m = 1 the state is the first edge with j = (0,1); a bridge's first directed edge is equivalent under the 8 symmetries and 3Z^2 translations to one of the two seed edges. I confirmed: directed square edges form one class (D4 acts regularly on the 8 directed edges of a cell), directed octagon edges form the other (the two translation classes of horizontal and vertical links are swapped by the diagonal symmetry and reversed by the reflections). Tests at m = 1 are covered by Lemma P as for any m.

Preservation of the invariant. Every candidate is an automorphic image of a subsequence of ex ending at the new head: suffix pruning drops an initial segment, a chord shortcut drops a middle segment, canonicalisation applies an automorphism. The proof only needs that the target is such a subsequence, not which one; any choice (smallest vector entry) works. A candidate target need not be a path in the pruned sense, but chord shortcuts join adjacent vertices, so the key encoding stays valid. The next state is then tau_(m+1) of an increasing subsequence of w_0..w_(m+1) ending at w_(m+1): induction closes.

Injectivity with pruning. A bridge gives a sequence of kept (state, move) pairs. Partition bridges by first directed edge (3 per start vertex), fix tau_1 per class and one witnessing sigma per (state, move). Then tau_(m+1) is a function of the path so far and w_(m+1) = tau_m^(-1)(A_m) is recovered, so distinct bridges give distinct paths in the multigraph of P. Pruned moves contribute nothing because no bridge uses them (Lemma P). So b_n(o) <= 3 lambda^(n-1) max x / min x for every start vertex o, hence limsup b_n^(1/n) <= lambda. This is the full count; it does not need that P bounds c_n (it does not, and the text says so).

Lemma B. I fetched Grimmett and Li, Locality of connective constants (statslab.cam.ac.uk/~grg1000/papers/loc-6.pdf, HTTP 200, 2026-10-19 UTC, sha256 2ec73172d21c51a7a520760009d8e28cf44bc3fbaaea5c8c28a2f1ed70cc46fb) and read Definition 3.1, (3.1), (4.1), Proposition 4.2, Theorem 4.3. Their bridge definition (4.1), h(pi_0) < h(pi_i) <= h(pi_n) for 1 <= i <= n, is ours with h = x. Theorem 4.3 needs an infinite, connected, quasi-transitive, locally finite, simple graph with a unimodular graph height function; Definition 3.1 needs h integer valued with the root at 0 (a shift), H a subgroup of Aut acting quasi-transitively with h difference-invariant, and a neighbour of strictly lower and higher h at each vertex. H = translations by 3Z^2 acts with four orbits, preserves x-differences, and acts freely, so every stabiliser is trivial and (3.1) holds (unimodular). The quasi-transitivity of H is the number of orbits being finite; four orbits qualifies. Proposition 4.2 gives b_n(v)^(1/n) -> beta for each v, and Theorem 4.3 gives beta = mu. The application is correct. I also checked the lattice: the neighbour tables give degree 3 and the faces are squares (diamond around (0,0)) and octagons, joined by the horizontal and vertical links; this is 4.8^2.

Pocket-search exactness. A vertex outside the box enlarged by 2 escapes by a monotone ray, so "infinite" from the box rule is exact; "finite" is only reported when the component is exhausted. The cap (total discovered vertices, 4096) could only turn a finite component of over 4096 vertices into "infinite", which keeps a move (safe direction). It is also unreachable: a state has at most 34 vertices (L-1+dist >= L for L > 2), so extended window plus tested vertex span at most 35 positions per coordinate, box 39, discovery at most 41 per side, under 1700 vertices. In my own run the largest search discovered 68 vertices.

Residual remarks (none affect the verdict):
- THEOREM.md section 4 says all directed edges reduce to the two seeds "using the vertex-transitivity ... on a window and periodicity". I did the two-class check by hand above; the window check is fine because the lattice is 3Z^2-periodic.
- P is a bound for bridges only, and the text says so.

## 2. The seven review fixes
Read against THEOREM.md, AUTOMATON.md, README.md and the checker.
1. Second-pass limit: AUTOMATON.md now states "NO limit" and the checker minimises over all present second-pass candidates; the text and the code agree. (Also numerically inert: 0 present in the state set. I confirmed this independently, see below.)
2. Lemma B: cites Theorem 4.3 and Proposition 4.2 with each hypothesis checked (I rechecked against the paper).
3. Lemma R wording: now "the ray avoids F after its initial vertex", and test 1 uses the actual removed set V(S). Present.
4. Injectivity by first directed edge with fixed tau_1 and a fixed witnessing sigma per pair: present in section 4.
5. Cap: documented as total discovered vertices, a zero-cap check is a hard failure in the checker (check at line 304 of the checker), and the unreachability count is in section 5. Present.
6. Ordered indices: the checker's inv_ok requires in-range indices, strictly increasing, last index equal to the new head, and finds sigma by search over the 8 symmetries and translation, not by the canonicaliser; ids are carried through suffix trimming and chord shortcuts. Present (ids are carried, not re-derived from scratch, and the text now says so).
7. Diagnostic renamed: the output line reads "second-pass candidates present in the state set (all enter the minimum): 0; of these, strictly lowering the running minimum: 0". Present.

## 3. My own independent program
Written from AUTOMATON.md before I read the shipped checker (in C, plus Python drivers for preparation, the exact ratio and a bridge simulation; none of these are shipped in this package). Single thread, under nice. What it does:
- Regenerates the states by BFS from the two seeds, using its own lattice tables, its own distance table (BFS on the lattice by vertex type), its own canonicaliser (all 8 symmetries, lexicographic from the head), and a hash set of keys.
- Pocket tests exactly as defined: test 1 removed set V(S) with tested vertex A; test 2 removed set ex[1..] with tested vertex ex[0]. Method: a monotone-ray proof of infinity in four directions where it succeeds, else the full breadth-first search with the enlarged box and no cap. On every 97th move both tests are also run by the full search alone and compared (no mismatch).
- Candidates: plain pruned suffix first, then chord shortcuts in recursion pre-order (depth below 3, minimum a carried), distinct list capped at 64, second-pass suffixes added only if present in the final state set (counted).
- Rebuilds every kept transition in a second pass and, for every candidate (90,733,935 checked, including second-pass ones), verifies strictly increasing in-range indices ending at the new head and finds sigma by direct search over 8 symmetries and translations in 3Z^2 (failures: 0).
- Every pruned move: the failing test is re-run by the full search alone and found finite (3,725,505 moves, no exception).
- Exact ratio: for every state, sum over kept moves of the smallest candidate vector entry, in 64-bit integers; maximum ratio found by 128-bit integer cross-multiplication over all 16,873,086 states (no floating point).

Results (my run, about 2.7 minutes):
- states 16,873,086 (equal to the claim).
- moves 30,056,689 = kept 26,331,184 + pruned by test 1 2,507,806 + pruned by test 2 1,217,699 (all three equal the counts the claim reports).
- ordered-invariant failures 0.
- Second-pass suffix candidates examined 40,504,441, present in the state set 0.
- Pocket searches: 101,566,766 ray proofs, 17,963,561 full searches, largest discovery count 68, none near 4096.
- Maximum ratio at state index 6930368: 710041141248 / 388946198528, which Python Fractions reduces to 169287/92732 = 1.825551050338610188..., so the decimal rounded up to 12 places is 1.825551050339. It is below 1.82926 by 0.0037089 (the exact comparison against 1.82926 minus 2e-6 is True). The state ordering of my BFS matches the shipped vector, which the exact agreement with a vector I did not touch shows.
- 252,708 states have ratio within 1e-6 of the maximum, so the vector is nearly tight, as expected from a Collatz-Wielandt vector.
- The maximum state has two kept moves with single candidates (indices 8961053 and 8961054); I recomputed the sum from the vector in Python.

Extra empirical test of Lemma P (my bridge-simulation driver): 210 random bridges, 16,537 steps, where the state is an actual ordered subsequence chosen at random among the pruned suffix and chord candidates; both pocket tests passed at every step, as Lemma P says (the test is a sanity check on the proof, not a substitute for it).

## 4. Shipped run_checks.sh
Run from a private copy of the package with 3 workers, under nice. All steps passed, including the two negative controls (vector entry set to 1 rejected, set to 0 rejected). The checker printed states found 16873086, moves kept 26331184, pruned by test 1 2507806, by test 2 1217699, zero cap hits, zero non-canonical states, zero ordered-invariant failures, exact max 169287/92732 at state 6930368, elapsed 2550 s, peak 7.6 GB. Last line of run_checks.sh: `ALL CHECKS PASS` (the checker's own last line: `PASS`).

## 5. Open questions in the claim record (not shipped)
1. Is the pruning theorem correct and complete? Yes. Lemma P and the induction in section 4 have no gap (section 1 above). The ordered form is needed for test 2 and is supplied.
2. Is the Grimmett-Li application right, in particular a free action by translations with four orbits? Yes. Quasi-transitive means finitely many orbits; a free action is unimodular by (3.1). All hypotheses of Definition 3.1, Proposition 4.2 and Theorem 4.3 are met, checked against the paper text.
3. Is the pocket test exactly the mathematical test? Yes. The box rule and the "finite only when exhausted" rule are exact. A cap overflow could only answer "infinite" for a finite component, which keeps a move and keeps lambda an upper bound. The cap is unreachable anyway (largest search in my run: 68 vertices; checker reports 0 cap hits).
4. Is the second-pass definition clear enough to rebuild without the generator? Yes. I rebuilt the same 16,873,086 states and the same ratio from the text alone. The only points I had to choose are that the plain candidate is first in the list and chords are emitted in recursion pre-order; both are the natural reading and agree with the shipped vector. No second-pass candidate is present in the state set, so that part is inert.
5. Is a rounded vector plus a rebuild-from-definition checker acceptable as the certificate? It meets the criterion's wording (the automaton definition plus a nonnegative test vector whose ratio is verified exactly). I rebuilt the transitions with independent code and obtained the identical exact fraction, which is the evidence that matters. The one soft spot is that the state order is defined only by the procedure; an error there would show up as a worse ratio, not a hidden one, and two independent codes agree.
6. Is agreement with the generator's fraction enough for the state order? Together with my independent rebuild (same order, same numerator and denominator), yes.
7. Are window checks (+-9 and +-12) with periodicity under 3Z^2 enough for the lattice facts? Yes. Every fact is a statement about neighbour offsets by vertex type and so is 3Z^2-periodic; the window covers all four types and every offset pattern with margin. I also rely on the explicit neighbour tables, which I checked by hand as 4.8^2.
8. The 1.82926 baseline: not part of my role (novelty). The quoted baseline only matters for the margin, and the margin 0.0037 is large against any rounding of the baseline.
9. Cross-family review: its seven findings are all present in the files (section 2).

## 6. Doubts and limits
- I did not run the generator, and did not need to.
- The ratio holds for the rounded 16-bit vector shipped (169287/92732), not for the author's 13-digit vector; the claim is stated for the rounded one.
- Novelty and the criterion are other roles and not judged here.

pass: true
