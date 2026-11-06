# REPRODUCE skeptic — tsasm-a005164-order-51-exact

context: subagent (parent Task)
Worked only on a scratch copy of claim/ ([scratch]/repro/claim). Did not read REPORT.md, NOTES, attempts/, LOG or other panel files.
Files read: claim.md, REPRODUCE.md, code/*, data/*, result/* (all relative to claim/).

## Definition used (quoted)
OEIS A005164 %N (data/A005164.txt, and re-fetched): "Number of alternating sign 2n+1 X 2n+1 matrices invariant under all symmetries of the square."
ASM: entries in {-1,0,1}; every row and column has partial sums in {0,1} and total 1. D4 = the 8 symmetries of the square.

## 1. My own checkers, written BEFORE reading the author's code
(a) brute.c / brutesym.c — brute force straight from the definition: row-by-row DFS over every matrix with entries in
{-1,0,1}, row partial sums in {0,1}, column partial sums in {0,1}, totals 1; at the leaf the full ASM check is done and
all D4 images are compared. brute.c is unpruned (all ASMs); brutesym.c additionally rejects early any entry that
breaks A[i][j]=A[j][i], A[i][j]=A[i][N-1-j] or A[i][j]=A[N-1-i][j] (necessary for D4-invariance; exhaustive over
D4-invariant matrices, final full D4 check retained).
  - brute.c: N=1,3,5,7 -> ASM totals 1,7,429,218348 (correct ASM numbers), TSASM 1,1,1,2.
  - brutesym.c: N=1..21 (n=0..10) -> 1,1,1,2,4,13,46,248,1516,13654,142873 = published a(0..10).
(b) hdp.py — exact big-integer DP using a DIFFERENT reduction from the author's (height functions, not their Q-matrix):
  H(i,j)=i+j-2*c(i,j) (c = corner sums) gives the standard bijection ASM(N) <-> H on [0..N]^2 with |adjacent diff|=1
  and boundary H(0,j)=j, H(i,0)=i, H(N,j)=N-j, H(i,N)=N-i. Derived: transpose <=> H(i,j)=H(j,i); horizontal-axis flip
  <=> H(i,j)=N-H(N-i,j). With N=2n+1, rows n,n+1 are swapped, forcing |2H(n,j)-N|=1, and parity H≡i+j forces
  H(n,j)=n+(j mod 2). So a(n) = # of functions on the triangle 0<=i<=j<=n with ±1 steps along edges, H(0,j)=j,
  H(i,n)=n+(i mod 2). Cell-by-cell column sweep, Python ints (no modular arithmetic), pruning only by the valid
  Lipschitz bound |H(i,j)-H(i,n)|<=n-j; final column asserted equal to the boundary.
  - Output n=0..26 is byte-IDENTICAL to result/a005164_0_26.txt; n=0..24 equals OEIS DATA; n=0..10 equals brute force.
  - a(25) = 30533896243799704017627552102998416 (exact). Re-run of n=25 gave identical output (DETERMINISTIC). Runtime 3.5 min.

## 2. Author's recipe (REPRODUCE.md) run verbatim on the copy (binaries/outputs in /tmp)
- Program A (row-major, P_A, 4 primes <2^62) and Program B (column-major, P_B, 4 primes <2^61; plus mod-2^128 mode): all
  per-n CRT checks with the 4th prime = OK (27/27 each, 0 FAIL). compare.py: "ALL_AGREE over n=0..26", n=25 wrap128=same,
  n=0..24 OEIS=yes.
- n=25 lines: A value=30533896243799704017627552102998416 check=OK; B same check=OK; B mod 2^128 same.
- primes.py prints exactly the P_A / P_B sets used.
- tsasm_check.py 6 (author's brute force): fixtures behave as stated; a(0..6) = 1,1,1,2,4,13,46.
- result/residues.txt: every one of its 216 lines for n=0..26 equals the regenerated residues; it also contains 4 extra
  Program-A residues for n=27 not produced by the REPRODUCE recipe — I regenerated them (tsA p 27 27) and they match.
  All residues are consistent with my exact values (0 inconsistencies).
- a(26) also agrees across A, B and my exact DP (not part of the claim).

## 3. Success criterion checklist
- Exact enumeration, not the Hagendorf–Liénardy formula: yes (transfer-matrix code read; confirmed independently by my exact DP).
- Same program reproduces a(0..13): yes (both A and B), and a(14..24): yes, no disagreements.
- Two independent runs agree on a(25) with different prime sets and different sweep order/encoding: yes (A row-major
  in-place pairing, P_A; B column-major pull/new-old arrays, P_B + mod 2^128). Note A and B share the same Q-matrix
  reduction; my height-function DP is a third run with a different reduction and exact big integers.
- Not already in OEIS: saved files' sha256 match claim.md. My re-fetch (one GET each, UA "V3R1T4S-research-agent",
  2026-11-01T03:08:49Z = Oct 31 23:08 EDT): search?q=id:A005164&fmt=text 200, sha256 identical to data/A005164.txt;
  b005164.txt 200, sha256 identical (ends n=24); draft/A005164 200, "No pending changes for A005164" (differs only in
  site footer/Cloudflare token). 30533896243799704017627552102998416 appears in none of them.

## Verdict
Claimed value, all properties and the status condition reproduced exactly and deterministically, including by an
independent exact checker built from the definition with a different reduction. No mismatch found.

pass: true
