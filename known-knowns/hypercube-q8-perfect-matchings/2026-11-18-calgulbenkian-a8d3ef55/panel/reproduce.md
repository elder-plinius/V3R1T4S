context: Claude Code subagent, fresh context [Sonnet 5.5]

# REPRODUCE report, a8d3ef55 (hypercube-q8-perfect-matchings, claimed partial win p2)

No network fetches were made. My own checkers were written and run before I opened any of the package's code (I read only the claim record and the file listing first).

## 1. Burnside step, re-derived
P = <s>, s = coordinate cycle (0 1 2 3 4), has order 5 and acts on the set M of perfect matchings of Q_8 (s is a graph automorphism). Orbits have size dividing 5, so size 1 or 5. Hence |M| = |Fix(P)| + 5k, so A005271(8) is congruent to |Fix(P)| mod 5. Fixed points are exactly the s-invariant matchings.

## 2. My independent structural reduction
Write a vertex as (u,w), u in {0,1}^5, w in {0,1}^(n-5). s rotates u.
- Fixed vertices: u in {00000,11111}, 2*2^(n-5) of them. Non-fixed vertices form orbits of size 5 (n=8: 48 orbits, 24 even and 24 odd, since s preserves parity).
- An s-fixed edge has both ends fixed (if s a = b then s b = a, impossible for order 5). Fixed vertices are adjacent only via w-flips (00000 and 11111 differ in 5 bits), so they form two copies of Q_(n-5).
- In an invariant matching a fixed vertex cannot be matched to a non-fixed vertex (the partner's whole orbit would be matched to it). So fixed vertices carry a perfect matching of two copies of Q_(n-5): A005271(n-5)^2 choices (n=8: 81; n=7: 4; n=6: 1; n=5: 0, two isolated vertices).
- Non-fixed edge orbits have size 5. An edge inside one vertex orbit would give a 5-cycle, and does not occur in Q_n. An edge orbit between vertex orbits A and B is a perfect matching A-B. So an invariant matching on non-fixed vertices is a perfect matching of the quotient bipartite multigraph (24 x 24 for n=8), weighted by the number of edge orbits between A and B (= neighbours of a representative of A lying in B). Edges to fixed vertices are excluded.
- Hence |Fix| = A005271(n-5)^2 * perm(W_quotient).

## 3. Computations (my files in work-reproduce/mine)
Quotient permanent computed two ways: bitmask DP over the odd side in C (not shipped in this package), and Ryser/Gray-code with __int128 fed by a separately written Python orbit and weight builder (not shipped in this package, a working file (not shipped)). Both agree:
- n=5: perm 24, fixed 0
- n=6: perm 836, fixed 836
- n=7: perm 1435396, fixed 4*1435396 = 5741584
- n=8: perm 9174591260928, fixed 81*9174591260928 = 743141892135168

Brute-force validation with no quotient reasoning (not shipped in this package):
- Q_5: all 589185 perfect matchings enumerated; exactly 0 are s-invariant.
- Q_6 and Q_7: direct search for s-invariant perfect matchings (adding whole edge orbits to a vertex mask) gives 836 and 5741584, equal to the quotient values.
- Full-cube Ryser on the biadjacency matrix reproduces A005271(3,4,5) = 9, 272, 589185. I did not recompute the full Q_6 and Q_7 counts (32x32 and 64x64 exact permanents are beyond a quick run); I compared residues with the published values.

Residues mod 5: A005271(5)=589185 is 0, fixed 0. A005271(6)=16332454526976 is 1, fixed 836 is 1. A005271(7)=391689748492473664721077609089 is 4, fixed 5741584 is 4. All consistent.

Q_8: |Fix(P_5)| = 743141892135168 exactly, matching the claimed value. 743141892135168 mod 5 = 3, so A005271(8) is congruent to 3 mod 5.

## 4. Package check
In a copy of this package inside work-reproduce, verify-it-yourself/run_checks.sh printed PASS in about 2.7 s. Both engines agree on the Q_5..Q_8 fixed counts (0, 836, 5741584, 743141892135168), reproduce A005271(1..5), and match A005271(5,6,7) mod 5. Output agrees exactly with mine. SHA256SUMS lists panel/*.md files that are withheld (expected); no other file failed.

## 5. Limits
- The package checker reproduces A005271(1..5) in full and 6, 7 only through residues against published values; the p2 wording (reproduce A005271(7) mod p) is satisfied.
- Novelty and the literature check are not covered by this role.
- Only the residue is established, not the full A005271(8).

Result: the claimed fixed count and residue are confirmed by an independent derivation and two independent computations, validated against brute force on Q_5, Q_6, Q_7.

pass: true
