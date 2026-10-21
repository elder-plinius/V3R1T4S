context: subagent (same VM)

# Criterion skeptic verdict, claim q145-1 ([[145,1,48]])

I read and ran only files inside this folder. I did not use the web, so I could not re-fetch the live table myself.

## Clause-by-clause

1. Range of n. n = 145 is within 101 <= n <= 256. Met.

2. "a proof that no [[n,k,d]] stabilizer code exists for d equal to the live table upper bound".
   - Live record: data/QECC_q4_n145_k1_claimtime.html has sha256 50d08374...ba26392a64bf77, matching CLAIM.md. Its text reads "Bounds on [[145,1]] ... lower bound: 33 upper bound: 49".
   - data/qubit_table_full_n1-256.html also has the sha256 recorded in CLAIM.md. After parsing, the cell reads [33, 49].
   - cert_145_1_49_sh.json is for d = 49, the live upper bound. It is the literal match.
   - cert_145_1_48_sh.json is for d = 48, which is not the live upper bound. It is a stronger result: A_j = B_j for j <= 47 holds for every code with distance >= 48, so it rules out all d >= 48, including d = 49. The d = 48 certificate therefore subsumes the literal d = 49 one. The literal clause is met by the d = 49 certificate, and the headline "<= 47" rests on the d = 48 certificate, which gives a lowering of 2 (at least 1 is required). This is not a stretched definition.
   - Both certificates concern codes with minimum distance >= d, pure or impure, so there is no hidden "pure only" quantifier.

3. "re-fetched live immediately before claiming". The files show a fetch at 19:43:25Z (full table) and 19:43:57Z (cell page), both HTTP 200 per CLAIM.md, with matching hashes. I cannot independently confirm freshness without web access. The record is internally consistent and the cell reads 49 in both the cell page and the full table. I treat this as met, but unverified by me live.

4. "lowering it by at least 1". 49 -> 47 (via d = 48) and, minimally, 49 -> 48 (via d = 49). Met.

5. The LP and its constraints are exactly the stated ones. From check/check_cert.py:
   - A_0 = 1 and sum A_i = 2^(n-k). This is B_0 = 1, i.e. the MacWilliams link.
   - A_j = B_j for 1 <= j <= d-1.
   - A_j <= B_j for j >= d, which is G_j.
   - A >= 0 (Farkas on the nonnegative orthant).
   - Shadow H_j >= 0 for 0 <= j <= n, which the criterion permits ("where used").
   - No extra, unjustified constraint: no integrality, no purity, no divisibility, and no weight-parity constraint.
   - Model check I ran (scratch/null.py, a brute-force null model). For [[5,1,3]], Steane [[7,1,3]], an odd-weight [[3,1,1]] and a [[3,0]] product state, I computed B (normalizer enumerator) and the shadow by brute force. The shadow was defined as {u : <u,s> = wt(s) mod 2 for all s in S}. The MacWilliams formula B_j and the formula Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i both matched exactly. The odd-weight case checks the (-1)^i sign.
   - Tamper tests: removing the shadow multipliers makes the certificate fail (column 49 positive). This is consistent with the shadow being essential. Perturbing a shadow multiplier fails. Reusing the certificate with d = 47 is rejected.

6. "exact rational Farkas certificate ... checked in exact integer arithmetic by an independent script".
   - `python3 -I check/check_cert.py result/cert_145_1_48_sh.json` printed "VERIFIED [[145,1,48]] shadow=True: value=1264 digits, max column coefficient <= 0, 47+2+46 multipliers", exit 0.
   - The same command on result/cert_145_1_49_sh.json printed "VERIFIED [[145,1,49]] ... 48+2+49 multipliers", exit 0.
   - The checker uses Python integers only: math.comb, and explicit multiplier sign checks.
   - I wrote my own re-implementation (scratch/indep.py). It builds Krawtchouk values from the three-term recurrence instead of the binomial sum, and uses a separate row assembly. It verifies both certificates: positive value, all 146 column coefficients <= 0, and max column coefficient exactly 0 for each. (Only the sign of the maximum matters for the Farkas test.)
   - The checker is the claimant's script, so "independent" holds in the sense of being separate from the solver. My re-implementation is an additional independent check.

7. "NOT already implied by propagation of other live cells".
   - I ran `python3 -I check/parse_table.py data/qubit_table_full_n1-256.html scratch/parsed.json`, then check/propagate.py, then the final one-liner. Output: "[33, 49] 49". The closure of the live table at (145,1) is 49.
   - Neighbours: R2 (146,1) = [33,49] gives 49. R3 (144,2) = [30,49] gives 50. R1 is n/a for k = 1.
   - The propagation tool excludes k = 0 cells. Under the listed rules, (145,1) is not affected by k = 0 cells anyway (R3 reaches k = 1 only from k = 2).
   - The page itself says that for n > 100 the upper bounds are "weak (and not necessarily monotone in k)", so a fresh LP result is plausible and not contradicted.
   - The non-monotonicity audit (1072 cells at n > 100 whose live upper bound is above their closure) does not touch (145,1).
   - Not subsumed. Met.

## Residual caveats (do not change the verdict)
- Live freshness at claim time rests on the recorded fetch and hashes. I could not re-fetch.
- Correctness of the LP model rests on the cited theorems (Calderbank-Rains-Shor-Sloane and Rains shadow). I tested the formulas on small codes by brute force. The certificate's soundness is then a pure integer check, which I reproduced.
- The d = 48 headline relies on the d >= 48 reading of "A_j = B_j for j < d", which is valid for all codes of distance >= 48.

confirmed_scope: For qubit stabilizer codes of length 145 and dimension 1, exact integer Farkas certificates of the quantum weight-enumerator LP with MacWilliams link, A_j = B_j below d, A_j <= B_j from d, and shadow nonnegativity, which I re-verified with the claimant's checker and my own re-implementation, show that no [[145,1,d]] code exists for any d >= 48, so the upper bound of the table cell (145,1) (recorded as 49) lowers to at most 47, and the propagation closure of the recorded live table at that cell is 49, so this is not implied by other recorded cells.

pass: true
