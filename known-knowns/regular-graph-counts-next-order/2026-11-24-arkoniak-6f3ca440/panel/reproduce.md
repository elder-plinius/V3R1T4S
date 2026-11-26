# REPRODUCE skeptic report

context: subagent (fresh context, saw only claim/)

Definition used (REPRODUCE.md): U_5(N) = (1/N!) sum_g Fix(g) = sum_lambda F(lambda)/z_lambda, z = prod k^{c_k} c_k!; connected counts by inverse Euler transform 1 + sum U(2n) x^n = prod (1-x^n)^(-C(2n)). Worked in a scratch copy of claim/; my own code written before reading the author's code (Python, `python3 -I`).

## 1. Burnside sum from saved per-type F (own code)
Own partition generator and z_lambda; read results/Dd5_N{N}_lane*.txt, skipped ERR rows, took F_D column, flagged conflicting duplicates (none), compared with the full partition set of N.
Output (N: #partitions, #valid rows, #missing, #extra, sum is integer):
- N=6: 11,11,0,0 True; N=10: 42,42,0,0; N=20: 627,627,0,0; N=28: 3718,3718,0,0
- N=30: 5604, 5604, 0, 0, True. Status counts in N=30 files: ok 1131, ERR 1804, Donly 4473 (every type has a valid non-ERR row).
- U(30) = 1690586697369281612308192667831589 (exact integer, no remainder), equals claimed U_5(30).
- Same for all even N 6..30 and N 0..5 (U = 1,0,0,0,0,0): all rows complete, sums integral.

## 2. Inverse Euler transform (own code, exact integer division asserted)
U(2n), n=0..15 -> C(2n). Compared with data/b165626.txt and data/b006821.txt (n=0..14):
- both files have n=0..14 exactly; U mismatches: none; connected mismatches: only n=0 (my convention c_0=0 versus the file's 1; not part of the claim).
- c15 = 1690586697346784893842479211750187 == claimed; u15 == claimed U (True, True).
Note: the two b-files are headed "b-file synthesized from sequence entry" (built from the 15 terms in data/A*.txt, which I checked equal the b-file contents). So the "published terms" are the OEIS data lines, n=0..14, which is all that is published. The fetch_utc file shows A006821.fetch_utc has a refetch note; not independently checkable offline.

## 3. Brute force from the definition (own code)
Enumerated all labeled 5-regular graphs on N vertices, computed Fix for one permutation per cycle type, weighted by class size.
- N=6: 1 labeled graph, U=1, remainder 0, all F per type equal saved F: True
- N=8: 3507 labeled graphs, U=3, remainder 0, all 22 saved F per type equal: True
(N=10 not feasible: tens of millions of labeled graphs.)

## 4. Recompute F by package method D (methodD/ copied to scratch, svdp.c compiled)
Ddsym2.F_D (with C short part) for 18 types: 12 hand-chosen of N=30 / 26 / 20 / 12 (6,6,3^6; 3^10; 4^6,3,3; 5^6; 7^4,2; 1^12; 2^10; 10^3; 15^2; 30; 4^5 2 2 1 1; 9 9 6 3 3) plus 6 random mid types (N=16..20, seed 1). All 18 equal the saved value: True. Package check 1 (dsumcheck N=30): `N=30 types=5604 U_D=...589 U_A=...589 AGREE`.

## 5. Method A full rerun (second method)
`gcc -O2 -o cubic methodA/cubic.c; python3 -I methodA/driver.py --bin cubic --deg 5 --nmax 30 --nprimes 8 --pivot max --dumpU` (about 4 min). Output last data line:
`30 1690586697369281612308192667831589 1690586697346784893842479211750187`
All 13 lines N=6..30 (U and connected C) identical to methodA/A_terms_d5.txt (that file additionally holds N=32..42 and trailing mismatch noise from an earlier run without a b-file; harmless). U_A(30) = U_D(30) from my independent sum of item 1.

## Observations (not failures)
- methodA/A_terms_d5.txt contains stderr junk lines ("MISMATCH connected idx=... FAIL") from an earlier run with a mismatched b-file indexing; unrelated to the claim values.
- Method A shares only engine/driver code with the optional F_A column, and the F_D rows with `ok` status carry F_A == F_D; the Donly rows were verified by my spot recomputations and by the sum agreeing with the separately run method A.
- Not checked: that the two methods are truly independent in design beyond the code being separate; no deterministic re-run differences seen (method A rerun identical).

## Mismatches: none.

pass: true
