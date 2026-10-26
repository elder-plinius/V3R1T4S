# Self-break checks so far (before the N = 20 result; the VERDICT comes after it)

1. Normalization of the finite criterion (raised by an outside audit: "should it be K_N < p?"). Our continuation
   starts at y = v_{N+1}, which is NOT on the path: A = {v_0..v_N open, F closed} (N+1 sites: p^(N+1) (1-p)^|F|),
   B = {y open and joined to infinity inside Z^3 minus (path u F)}. B is contained in {|C(y)| = infinity}, so
   P(B) <= theta exactly; no factor 1/p arises. Code: kcheck.py uses p**(N+1); par/main.go counts y with
   !onPath[y] && adj[y] == 1 && !inF[y]. On the b-ary tree the same argument gives (bp)^(N+1) < 1, i.e. p < 1/b,
   exactly p_c. The audit's K_N < p version is also valid but weaker (N = 18: 0.240626 vs 0.261794).
2. Ground truth (groundtruth.py A, partA_300.txt): 300 random configurations in a 15^3 box (p in 0.3-0.6), true
   BFS tree with the parent rule; every tree path up to length 10 is a NAW, all its F sites are closed, no detour
   pair candidate has both sites open, every child of the endpoint is a valid extension.
   Mutation tests: reversing the corner comparison, or loosening the pair shortcut gap from 5 to 3, both fail at
   once with explicit counterexamples (so the test can detect rule errors).
3. Independent enumeration (groundtruth.py B 9, b9.txt): complete-path Python implementation reproduces the Go
   table exactly at N = 9 (go9.txt), total 649086 = a_9. Chain: Python = plain Go (N = 9); plain Go = parallel Go
   (N = 12, 14); parallel totals = NAW counts (N <= 18) and the Alm program's a_18.
