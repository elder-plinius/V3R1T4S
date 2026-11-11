# PREREG — total domatic cells of the queens graph (time stamp from `date -u` on the last line)

Criterion: verbatim in target.md (bank entry queens-graph-domatic-numbers). Cells: tdom(Q_11) in {16, 17},
tdom(Q_10) in {15, 16}, tdom(Q_12) in {18, 19, 20} (Table 1 of Lauri's Corrigendum, read in this run from the fetched
file: total domination numbers 6, 7, 7 for n = 10, 11, 12).

Definition. A set D totally dominates Q_n when every square, members of D included, shares a row, a column or a
diagonal with a member of D other than itself. A total domatic k-partition: all n^2 squares split into k classes, each
totally dominating.

Lower-bound claim (partial win p1): only for a grid file with k classes, k above the table's lower bound for its cell,
for which BOTH runs/2026-11-05-0019-queens/attempts/checker/code/check.py and check_bits.py, called with kind tdom,
print PASS (they were validated on 2026-11-05 on Lauri's published partitions and on a mutated grid; re-tested in this
run on a positive and a negative tdom case before use), and after a three-skeptic panel. One object, one cell per claim.

Search design. A superset of a total dominating set is total dominating, so each class can be shrunk to a minimal
total dominating set and the freed squares moved to another class. With g the total domination number, N = n^2 and K
classes, the slack is s = N - gK. A K-partition then consists of K - c pairwise disjoint total dominating g-sets and c
other classes, 0 <= c <= s, whose union is the set of remaining squares. The search enumerates all total dominating
g-sets (minimum sets, hence minimal), then looks for K - c disjoint ones whose remainder splits into c total dominating
sets (for c = 0 the remainder is empty or loose squares that join any class).
An exhaustive negative for every c would exclude K as mathematics, NOT as a bank win; it will be reported as
"negative"/"progress" with its exact limits (completeness of the list rests on calibration and two branching rules).
Calibration required before any list is used: the enumerator must find no total dominating set below the published
total domination number (5 for n = 9, 6 for n = 10, 7 for n = 11 and 12) and at least one at that size.

null_test: not needed because the claims are explicit objects or exhaustive searches checked deterministically
written_utc: 2026-11-11T18:21:29Z
