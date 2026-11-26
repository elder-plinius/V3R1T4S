# REPRODUCE skeptic verdict

Scope: only claim/. My own scripts are in a scratch folder (not inside claim/). I wrote them from the definition in claim/REPRODUCE.md before reading any author code:
"U_4(N) = (1/N!) sum_{g in S_N} Fix(g) ... U(N) = sum_lambda F(lambda)/z_lambda, z_lambda = prod_k k^{c_k} c_k!.
Connected counts follow by the inverse Euler transform: 1 + sum_n U(n) x^n = prod_n (1 - x^n)^(-C(n))."

## 1. N=51 Burnside sum (own checker, exact Fractions)
- results/Dd4_N51_lane0.txt + lane1.txt: 239943 rows, all status Donly, no ERR rows, no duplicates, 0 missing and 0 extra partitions compared with my own enumeration of the partitions of 51 (p(51) = 239943, computed independently).
- sum F/z_lambda has denominator 1, and U_D = 152556963477307480948188554287675435592122034073857046.
- This equals U_A(51) in methodA/A_terms_d4.txt exactly (EQUAL).

## 2. All N=5..51 plus the inverse Euler transform (own code)
- I re-summed every lane file for N=5..51 myself. Each order has p(N) valid types, no conflicting rows, and an integer sum. Every sum equals U_D and U_A in results/Dsum_check_d4.txt (all marked AGREE) and U in methodA/A_terms_d4.txt (0 issues). For N=0..4 I used 1,0,0,0,0.
- Own inverse Euler (via b_n = sum_{d|n} d C(d)): C_4(51) = 152556958807091391617335751728584931970607218791861386, which matches the claim and the C column of methodA/A_terms_d4.txt at N=51. A forward Euler product of the C values gives back U(0..51) exactly.
- data/b033301.txt (n=0..28, 29 terms): 0 mismatches. data/b006820.txt (n=0..28, 29 terms): 0 mismatches. data/cx_table_U4.txt and data/cx_table_C4.txt (N=29..50, 22 terms each): 0 mismatches.
- data/b006820.txt is byte-identical to data/b006820_live.txt. Note: its header reads "b-file synthesized from sequence entry", so it is the OEIS entry data, not a separately uploaded b-file. This does not affect correctness.

## 3. Independent brute force of the per-type definition (small N)
- My own Fix(g) counter: enumerate the edge orbits of g, then backtrack over unions of orbits that give a 4-regular graph. It reproduces every per-type F row of results/Dd4_N7, N8 and N9 lane files: 15, 22 and 30 types, 0 mismatches.

## 4. Re-runs of the author code (copied to a scratch folder, python3 -I)
- Method A (cubic.c compiled fresh, driver.py --deg 4 --nmax 36 --nprimes 8 --pivot max --dumpU): N=5..36, both U and C agree with methodA/A_terms_d4.txt at all 32 orders, 0 mismatches.
- Method D at N=51, three types recomputed via Ddsym2.F_D with the freshly built svdp. All three are equal to their rows in results/Dd4_N51_lane*.txt:
  - 2^17 1^17 -> 62582271756253883780609259087813550438051752699397777509813878148
  - 3^5 2^8 1^20 -> 30163331372091001456934841673457311498153293153923232
  - 7 5 4 3 3 2 2 1^25 -> 56400641942428794585903095598094924534438932438
- Independence: the method D modules (D, Dd, Ddsym, Ddsym2, Svdp, Svdpc) do not import methodA. Only runDd.py imports engine, for the optional F_A column, and the runs used --noA.

## Judgement
The value is a full Burnside sum over all 239943 types, not a search. I could not recompute every type at N=51. However:
- my own exact sum over the complete saved table equals the independent method A total;
- method A reproduces correctly when re-run (to N=36);
- the N=51 spot checks of method D match;
- the per-type definition is confirmed by brute force at small N;
- both methods reproduce all published terms to N=50.

A wrong per-type value at N=51 would have to be cancelled exactly by an independent C histogram recurrence, which is not plausible. No mismatch, missing object or non-determinism was found.

context: subagent
pass: true
