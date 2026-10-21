context: subagent (same VM)

# Criterion skeptic verdict: claim q152-1 (qubit cell [[152,1]])

Scope of reading: only files inside this folder; no web, no GitHub tool, nothing outside the folder read.
data/TROPHY_CASE_pinned_9b1d444.md was grepped for qubit/codetables/stabilizer/QECC/152 (no hits, unrelated).

## Clause-by-clause

1. "some qubit cell (n,k) with 101 <= n <= 256": cell (152,1); n = 152 is in range. Met.

2. "a proof that no [[n,k,d]] stabilizer code exists for d equal to the live table upper bound":
   data/QECC_q4_n152_k1_claimtime.html says "lower bound: 33 upper bound: 51" (grep of the saved page);
   the parsed full table (check/parse_table.py) also gives [33, 51] for (152,1). The literal reading
   (d = 51 = live upper bound) is covered by result/cert_152_1_51_sh.json (d = 51); the stronger
   result/cert_152_1_50_sh.json (d = 50) is also supplied. No hidden quantifier: the d=51 certificate is
   exactly the literal criterion; d=50 is a strictly stronger extra. Met.

3. "re-fetched live immediately before claiming": the folder records fetches at 2026-10-16T19:43:25Z (full table)
   and 19:44:06Z (cell page), HTTP 200, with sha256 values. I re-computed the sha256 of both saved files and they
   match CLAIM.md (d03ffa95..., 26245491...). I cannot re-fetch (no web allowed), so the "live at fetch time"
   fact rests on the recorded files, not on my own fetch. Accepted as recorded; flagged as not independently re-fetched.

4. "thereby lowering it by at least 1": d=51 certificate lowers 51 -> <= 50; d=50 certificate lowers 51 -> <= 49
   (a [[n,k,d]] stabilizer code is also an [[n,k,d-1]] code, so excluding d=50 excludes 51 as well). Met.

5. "exact rational infeasibility certificate (Farkas dual) of the quantum weight-enumerator LP (stabilizer and
   normalizer enumerators linked by the quaternary MacWilliams identity, A_i <= B_i, A_i = B_i for 0 < i < d,
   nonnegativity, plus shadow-enumerator nonnegativity where used)": the LP in check/check_cert.py is
   A_0 = 1, sum A_i = 2^(n-k) (equivalent to B_0 = 1 under MacWilliams; normalisation of a stabilizer of order 2^(n-k),
   not an extra restriction), Q_j: B_j = A_j for 1<=j<=d-1, G_j: A_j <= B_j for d<=j<=n, A >= 0 (implicit in the
   Farkas argument), H_j: Sh_j >= 0 (Rains shadow, (-1)^i sign). No other constraints (no integrality, no
   evenness, no pure/Hamming-type extras, no ad-hoc inequalities). The rows are sound: I wrote my own
   enumerator-row test (three-term-recurrence Krawtchouk, validated against the binomial formula for n=5,7,12)
   and confirmed that the true weight enumerators of [[5,1,3]] (1+15x^4) and Steane [[7,1,3]] (1+21x^4+42x^6)
   satisfy every row with d=3 (and Steane correctly fails d=4). Certificate multipliers are integers (decimal
   strings), equality multipliers u_Q of free sign on indices 1..d-1, inequality multipliers v_G, v_H >= 0
   (checked: zero negative v_G/v_H; v_G supported on {52,53} for d=50, {53,54} for d=51; v_H on 49/50 indices).
   Rational scaling by 2^(n-k) gives integer rows. Met.

6. "checked in exact integer arithmetic by an independent script":
   - Ran: python3 -I check/check_cert.py result/cert_152_1_50_sh.json
     -> VERIFIED [[152,1,50]] shadow=True: value=1480 digits, max column coefficient <= 0, 49+2+49 multipliers (exit 0)
   - Ran: python3 -I check/check_cert.py result/cert_152_1_51_sh.json
     -> VERIFIED [[152,1,51]] shadow=True: value=1476 digits, ... 50+2+50 multipliers (exit 0)
   - Wrote scratch/indep.py (independent of check_cert.py: recurrence Krawtchouk, pure Python ints). Both
     certificates VERIFIED there as well (all 153 column coefficients <= 0, value 1480 / 1476 digits positive;
     for d=50: 152 negative columns and exactly 1 zero column).
   - Soundness of the checker itself: mutated certificates are rejected (scratch/mut1.json u_E0 inflated -> FAILED
     column 0 positive; scratch/mut2.json d=60 with d=50 support -> FAILED index outside d..n; scratch/mut3.json
     k=3 -> FAILED positive column). So the checker is not vacuous.
   - Farkas logic re-derived by hand: for a feasible A >= 0, sum_i c_i A_i = u_E0 + u_E1 2^(n-k) + (nonneg terms)
     >= value > 0, but c_i <= 0 forces sum c_i A_i <= 0. Contradiction. Met.
   "Independent": checker is standard-library only and separate from the solver that produced the certificate
   (the producing solver is not in the folder); I additionally re-implemented it. Met.

7. "NOT already implied by applying the standard propagation rules ... to other live cells":
   Ran: python3 -I check/parse_table.py data/qubit_table_full_n1-256.html scratch/parsed.json   -> cells 33152, n 1..256
        python3 -I check/propagate.py scratch/parsed.json scratch/closure.json   -> 32896 cells k>=1, 1075 live cells above closure (1072 with n>100)
        python3 -c "...print(T['152']['1'], C['152,1'])"   -> [33, 51] 51
   Closure uses R1 (k>=2), R2 d(n,k)<=d(n+1,k), R3 d(n,k)<=d(n-1,k+1)+1 over every live cell, to a fixed point,
   and gives 51 at (152,1); neighbours: R2 (153,1) = [33,51], R3 (151,2) gives 51. k=1 has no R1. The 49 / 50
   bound is therefore not implied by propagation from other live cells. (Note: the table's own warning says n>100
   bounds are weak and non-monotone; that makes (152,1) more, not less, likely to be improvable, and the closure
   check is done on the supplied table as is.) Met.

## Hidden quantifiers / stretched definitions / null models
- No quantifier mismatch found: the criterion asks for one cell and one-step lowering; the literal d=51 certificate
  exists and verifies, and the claimed d=50 is a stronger, also verified, statement.
- Null model 1 (known feasible codes): rows hold for [[5,1,3]] and [[7,1,3]]; no row contradicts reality.
- Null model 2 (corrupted/other-parameter certificates): rejected by the checker (above).
- The claim is for stabilizer codes (what the criterion asks), not claimed for general nonadditive codes.
- Residual caveats (not criterion failures): (a) I did not re-fetch the live table; I rely on the recorded
  fetch files whose hashes match CLAIM.md. (b) The enumerator-row formulas are standard (Calderbank-Rains-Shor-Sloane
  MacWilliams, Rains shadow) and I validated them only on small known codes plus the algebra, not against a
  published n=152 LP value. (c) No LP solver was available here (no scipy), so I did not re-derive infeasibility
  by solving; the exact certificate check is the proof.

confirmed_scope: For the qubit cell (152,1), the supplied integer Farkas certificates (d=50 and d=51) of the stated weight-enumerator LP with Rains shadow constraints verify in exact integer arithmetic (supplied checker and my own re-implementation), so no [[152,1,50]] (hence no [[152,1,51]]) stabilizer code exists, lowering the recorded live upper bound 51 to at most 49, which the propagation closure of the recorded full-table snapshot (51) does not imply; the live status was taken from the recorded fetch files and not re-fetched by me.
pass: true
