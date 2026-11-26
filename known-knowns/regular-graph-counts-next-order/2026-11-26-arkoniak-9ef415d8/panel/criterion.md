# Criterion skeptic verdict

Claimed branch: "a connected quartic count at order 51 or more (beyond Cheng-Xu's published table)". The object is one cell, C_4(51). It is a named enumerated branch of the bank criterion, not a stretched partial win.

## (a) Order 51, beyond Cheng-Xu
- N = 51 is the first order past the Cheng-Xu Tables 4/5 (29..50) as given in data/cx_table_*.txt. The claim folder records that the paper's table ends at 50 (abs page v1 only). I did not check novelty further because that is outside this clause.
- The object is connected 4-regular graphs on 51 vertices, which is exactly what the branch names. No hidden quantifier: it is a single order and a single sequence.

## (b) Two independent methods that agree exactly
- Method A is a C histogram recurrence (methodA/cubic.c), run modulo 62-bit primes with CRT done in driver.py. Method D is a Python per-cycle-type coefficient extraction (short part) plus a count-vector DP over long cycles (Dd.py, Ddsym.py, D.py), done modulo 2^521-1.
- runDd.py does import methodA/engine.py. With --noA (used for every N=51 row: all 239943 rows have status Donly) the only calls are E.set_degree, which only clears engine's own caches. Dd, Ddsym, Ddsym2 and D do not import engine and do not use the histogram recurrence. The per-type F_D values do not depend on method A.
- Both methods share only the Burnside outer frame (sum over partitions of F/z_lambda). The criterion's own example accepts that shape ("Burnside/cycle-index count and Howroyd-style labeled counting fixed by permutations implemented separately"). The per-type algorithms, languages, moduli and final summation code are separate. I judge them independent.
- I reran dsumcheck at N=51 from the lane files: types=239943 = p(51), every type has a valid row, and U_D = U_A = 152556963477307480948188554287675435592122034073857046 (AGREE).
- From U to C: C_4(51) is the inverse Euler transform of U(0..51). U_D = U_A for every N = 5..51; I recomputed this from the raw lane files for N = 5..50 (46/46 AGREE, and each matches its line in Dsum_check_d4.txt). N = 0..4 are trivial (1,0,0,0,0). cxcheck applies the inverse Euler transform separately to U_A and U_D, and both give C_4(51) = 152556958807091391617335751728584931970607218791861386. Since the inputs agree exactly at every order, agreement on the totals is enough for the connected count.
- Exactness mod 2^521-1: F(lambda) <= F(1^N), the number of all labeled 4-regular graphs, because fixed graphs are a subset. The largest F_D in the N=51 files is 120 digits (397 bits), below 2^520, and the code asserts residue < P/2. Denominators are products of small factorials and are invertible mod the prime. The argument is adequate. However, REPRODUCE.md's figure "at N=50 about 64 digits" is wrong (F(1^N) is about 10^119 to 10^120). The conclusion still holds by a margin of about 120 bits. This is a documentation error, not a correctness issue. Method A's CRT range does not matter here, because its value matches D exactly.

## (c) Same code reproduces every published term (sequence + disconnected version)
- allterms.py on the method-D totals gives b033301.txt (A033301, n=0..28): checked=29 MISMATCH 0. The inverse Euler transform vs b006820.txt (A006820, n=1..28) gives checked=28 MISMATCH 0. The OEIS b-files are the synthesized-from-entry versions that OEIS serves (live fetch is byte-identical, http 200).
- cxcheck: U_D vs CX Table 4 and inverse-Euler C vs CX Table 5, N=29..50, 22/22 each, MISMATCH 0. The same holds for U_A.
- So the same method-D code reproduces every published term of the connected sequence (OEIS plus Cheng-Xu to 50) and of the disconnected version.
- Minor: the A006820 n=0 entry is not compared. It is a convention term, so this does not matter.

## Null-model / subsumption
- The result is not subsumed: the published data stops at 50, and 51 is a new order. It is not a trivially derivable value, since it needs the full Burnside sum over p(51) types.
- One cell, one order, one sequence.

confirmed_scope: Two separately implemented Burnside-over-cycle-type computations (method D per-type extraction mod 2^521-1, and method A C histogram recurrence mod 62-bit primes with CRT) agree exactly on U_4(N) for every N up to 51, and their inverse Euler transform gives C_4(51) = 152556958807091391617335751728584931970607218791861386 connected 4-regular graphs on 51 vertices; the method-D code reproduces every term of the A033301 and A006820 b-files (n<=28) and Cheng-Xu Tables 4-5 (orders 29-50).
context: subagent
pass: true
