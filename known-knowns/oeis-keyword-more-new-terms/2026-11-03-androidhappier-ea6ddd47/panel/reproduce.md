# Panel: REPRODUCE -- runs/2026-11-03-2128-maxembed
context: subagent (reproduce)

Inputs read: claim/ only (CLAIM.md, REPRODUCE.md, object/VALUE.txt = 3360, programs/, table/) and the REPRODUCE line of panel_requests/2026-11-03-2128-maxembed.md.

## 1. Own checker, written from the definition first (panel/reproduce_work/mycheck.py)
Written before I read the claim programs.
- Part 1 (pure definition, brute force): enumerate every ordered tree on n <= 11 vertices as nested tuples, canonicalize as rooted trees (recursively sorted children), group by class, and take the largest class. Pinned by %e: n = 4 gives 5 ordered trees, 4 classes, max 2 (the path rooted at B/C), so a(4) = 2. Results for n = 1..11: 1,1,1,2,3,4,6,12,24,40,60 = DATA.
- Part 2 (exhaustive, n <= 17): generate each rooted tree once as a nonincreasing multiset of earlier-generated subtrees, with c(t) = deg!/prod(mult!) * prod c(child). Self-checks: the tree counts are A000081 (1,...,235381,634847), and sum of c(t) = Catalan(n-1) for every n (True for all n).
- Output: max c for n = 1..16 = 1,1,1,2,3,4,6,12,24,40,60,120,240,420,840,1680 (= DATA a(1..16)); **n = 17: max 3360, attained by exactly 1 tree** (634847 trees). Wall time about 345 s in Python.
- Part 2 was printed to my terminal and not saved as a log. Rerun with `python3 panel/reproduce_work/mycheck.py 17` (about 6 min). panel/reproduce_work/mycheck_12.out keeps the n <= 12 run.

## 2. Claim programs, rebuilt in a fresh dir (gcc -O2)
- pB (programs/pB_c/progB.c, `./pB 17`): column 2 = DATA a(1..16), then 17 -> 3360, sum = 35357670 = Catalan(16), trees = 634847, argmax = 1. Wall 0.15 s. Log: panel/reproduce_work/pB.out
- pA (programs/pA_c/progA.c, run alone, `./pA 17`): this is a brute force over all Dyck words with hash-interned classes. Column 2 = DATA a(1..16), then 17 -> 3360, ordered = 35357670, classes = 634847, argmax = 1. Wall 16.4 s on this box, faster than the claimed ~200 s. MemAvailable stayed at about 9.1 GB before and after, well above the 4.5 GB floor. Log: panel/reproduce_work/pA.out
- table/brute_fixtures.py reruns and matches DATA for n <= 12. Its negative fixture (no multiplicity division) differs at n >= 4 (rows shown for n = 5..12), as stated.

## 3. Comparison with claim logs
pA and pB match claim/programs/*/progA_17.out and progB_17.out on n, max and argmax. The per-n argmax counts (1,1,2,1,1,2,5,3,1,1,6,4,2,3,3,3,1) are identical across my checker, pA and pB.

## Verdict
Three methods agree: my definition-level checker, pA (brute force) and pB (formula). All three reproduce DATA a(1..16) and give A214570(17) = 3360 with a unique maximizer. This matches object/VALUE.txt.

pass: true
