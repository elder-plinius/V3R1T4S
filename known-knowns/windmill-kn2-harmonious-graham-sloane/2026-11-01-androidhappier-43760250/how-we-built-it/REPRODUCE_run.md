# REPRODUCE: K_8^(2) is not harmonious

Requirements: gcc, python3 (standard library only). Runtime: P1 ~41 s, P2 ~12 s (0.75 GB RAM).

```
gcc -O2 -o wsearch checkers/wsearch.c
./wsearch 8          # expect: sum_distinct_sets_containing_0=449472 solutions_ordered_pairs=0 ; VERDICT n=8: NOT HARMONIOUS
python3 checkers/mitm.py 8   # expect: sum_distinct_sets_containing_0=449472 ... solutions_ordered_pairs=0
for n in 3 4 5 6 7; do ./wsearch $n | tail -2; python3 checkers/mitm.py $n | tail -1; done
                     # expect n=4 HARMONIOUS (48 ordered pairs), all others NOT HARMONIOUS
python3 checkers/brute_n4.py   # expect: brute_force_labelings 20736 expected 20736
python3 checkers/check_label.py 4 "0 2 6 11" "3 7 9"   # VALID (a known K_4^(2) labeling)
```

## Definition used
Graham and Sloane (1980): a graph with q edges is harmonious if its vertices can be labelled with distinct residues mod
q so that the q edge sums f(u)+f(v) mod q are distinct. K_n^(2) = two copies of K_n sharing one vertex c
(2n - 1 vertices, q = n(n-1)). For n = 8, q = 56.

## The only reduction: translation (PROVED-HERE)
If f is harmonious, so is g = f - f(c) (mod q): g is injective because f is, and every edge sum changes by the same
constant -2 f(c), which permutes Z_q, so distinct sums stay distinct. Conversely g -> g + t gives back all labelings.
Hence a harmonious labeling exists iff one exists with f(c) = 0. Both programs search only f(c) = 0 and use no other
symmetry (no unit multipliers, no A/B swap). Each clique's 7 non-shared labels are enumerated as an increasing tuple,
which only removes the 7!·7! reorderings of vertices inside each clique (the edge-sum multiset depends only on the
label sets). Check at n = 4: brute force over all injective labelings without any reduction finds 20,736 =
48 (ordered pairs found by P1/P2) x 12 (translations) x 3! x 3! (orderings) labelings.

## Why the search is exhaustive
With f(c) = 0, write A = {0} ∪ A', B = {0} ∪ B'. The edge sums are the C(8,2) = 28 pair sums inside A plus the 28
inside B; all 56 distinct mod 56 means each of A, B has 28 distinct pair sums and the two sum sets are disjoint
(so they partition Z_56). Labels distinct means A' ∩ B' = ∅ and 0 ∉ A' ∪ B'.
- P1 enumerates every increasing A' ⊂ {1..55} with A's pair sums distinct (rejecting only on a repeated sum), then
  every increasing B' ⊂ {1..55} \ A' whose pair sums (with 0 and each other) avoid all sums used so far.
- P2 enumerates every 8-set containing 0 with distinct pair sums (breadth-first), then joins pairs whose sum masks
  are complementary and whose label sets meet only in 0.
Both count 449,472 such 8-sets and 0 labelings.

## Extra checks (optional)
```
gcc -O2 -o wjoin checkers/wjoin.c && ./wjoin 8 14     # P3: 449472 sets; d=14 ... compatible 0; solutions 0
gcc -O2 -o mod14 checkers/mod14.c && for d in 2 4 7 8 14 28; do ./mod14 $d; done
python3 checkers/mod_multiset.py 28   # ~3 min: "compatible ordered pairs (no Sidon condition) = 0"
```
mod14.c is a necessary condition only: every residue class mod 14 must receive exactly 4 of the 56 edge sums; no
set's mod-14 class-count vector has its complement (4 - x per class) among the vectors of the 449,472 sets.

mod_multiset.py is a separate, Sidon-free necessary condition: reduce labels mod 28 (each class of Z_56 mod 28 holds
2 labels, so a clique's label multiset has class multiplicity <= 2, the two cliques together <= 2 per class except
<= 3 at class 0 for the shared vertex), and every class mod 28 must receive exactly 2 of the 56 edge sums. Among
4,349,475 eight-element multisets containing 0, no ordered pair satisfies this.
