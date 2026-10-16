context: subagent (same VM)

# Criterion-skeptic verdict, claim q139-1 ([[139,1,46]] / [[139,1,47]])

Only files inside this folder were read or run. Nothing was fetched from the web, so the "re-fetched live" clause is judged on the recorded fetch only.

## Clause-by-clause

1. Range of n: n = 139 lies in 101..256 and k = 1. Met.

2. "d equal to the live table upper bound".
   - data/QECC_q4_n139_k1_claimtime.html says "Bounds on [[139,1]] lower bound: 29 upper bound: 47".
   - The complete-table file gives the same cell, [29, 47]. I recomputed the sha256 of both html files; they match the sha256 values in CLAIM.md.
   - The literal criterion is d = 47. result/cert_139_1_47_sh.json targets d = 47, so the literal reading is met.
   - The headline claim uses d = 46, which is not the live bound. No [[139,1,46]] code implies no [[139,1,47]] code and no code with d >= 46, so "upper bound <= 45" follows. The d = 46 certificate is stronger than the literal criterion and does not weaken it.
   - The page itself says that for n > 100 the upper bounds "are weak (and not necessarily monotone in k)". A fresh LP result at this cell is therefore plausible and not suspicious.

3. "Re-fetched live immediately before claiming". The recorded fetches are 2026-10-16T19:43:25Z and T19:43:49Z, HTTP 200, with matching hashes. I cannot re-fetch from here, so I rely on the record. This is an unverified-by-me clause, not a violated one.

4. "Lowering it by at least 1". 47 to 45 (or 47 to 46 via the d = 47 certificate) is a drop of at least 1. Met.

5. The LP and its constraints. The criterion lists A_0 = 1 and sum A = 2^(n-k) (normalization), the MacWilliams link, A_i <= B_i, A_i = B_i for 0 < i < d, nonnegativity, and shadow nonnegativity "where used".
   - The checker's rows match these exactly, with no extra constraint: E0, E1, Q_j for 1 <= j <= d-1 (equalities), G_j for d <= j <= n (inequalities), H_j for 0 <= j <= n (shadow).
   - The checker rejects out-of-range multiplier indices and negative inequality multipliers.
   - Shadow formula: Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i. I re-derived it from Rains, Sh(x,y) = A(x+3y, y-x)/|S|, and it agrees.
   - Soundness test with real codes (work/sanity.py): the [[5,1,3]] and [[7,1,3]] stabilizer weight enumerators, built from generators, satisfy every LP row. My independent Krawtchouk implementation (generating-function expansion) equals the checker's binomial-sum version for n = 5 and n = 9.
   - Null model for over-constraint (work/lpfeas.py, an exact Fraction simplex that I wrote): for all 65 cells with n <= 18, k = 1..4 and d = the live table lower bound, so a code exists, the LP with shadow is feasible. There were 0 wrongly infeasible cases. The LP is not over-constrained.

6. "Exact rational Farkas certificate, checked in exact integer arithmetic by an independent script".
   - `python3 -I check/check_cert.py result/cert_139_1_46_sh.json` printed `VERIFIED [[139,1,46]] shadow=True: value=1270 digits, max column coefficient <= 0, 45+2+44 multipliers`, exit 0.
   - The same command on cert_139_1_47_sh.json printed `VERIFIED [[139,1,47]] ... 46+2+46 multipliers`, exit 0.
   - I re-verified both certificates with my own script (work/indep.py) that uses a different Krawtchouk method. Both pass: every column coefficient <= 0, value > 0, all inequality multipliers >= 0.
   - Mutation null model: dropping the shadow multipliers (dropH) or the G multipliers (dropG) makes both certificates fail. The checker is therefore not vacuous.
   - The certificate uses integer multipliers only (decimal strings). "Rational" is satisfied by integers after clearing the 2^(n-k) denominators, which the docstring states.
   - "Independent": check_cert.py is standard library only and separate from the solver that found the certificate. I did not see the solver, so independence rests on the checker not importing anything from it. I additionally cross-checked with my own implementation.

7. "NOT already implied by propagation from other live cells".
   - I ran `python3 -I check/parse_table.py data/qubit_table_full_n1-256.html work/parsed.json`, then `python3 -I check/propagate.py work/parsed.json work/closure.json`, then printed T['139']['1'] and the closure value. The output was `[29, 47] 47`.
   - The closure of the live upper bounds under R1 (k >= 2), R2 and R3 at (139,1) is 47. Neighbours are (140,1) = 47, (138,2) = 47, and (139,1) has no R1 case because k = 1. So 45 or 46 is not implied by the stated rules.
   - The table itself is non-monotone in 1072 cells with n > 100. For those cells the live bound is above the propagation closure. This is not a problem for this cell, where live equals closure.
   - The k = 0 column (for example (140,0) = 41) is not part of the listed rules. The propagate.py header says k = 0 "uses a different distance notion" and excludes it. The criterion does not list a k = 0 rule, and no standard rule here links [[139,1,d]] to a k = 0 cell. Not subsumed under the criterion's stated rules.

## Hidden quantifiers and stretched definitions
- The criterion says "for some qubit cell". The claim is one cell, (139,1). No quantifier is stretched.
- "Minimum distance upper bound lowered" is read as "no code with this d exists". That is legitimate for stabilizer codes, since d >= 46 implies d = 46 as an "at least" distance.
- The certificate proves nonexistence of stabilizer (additive) codes only. The table is for additive qubit codes, so this matches the table's own scope. It does not address non-additive codes, and the claim does not assert that.
- The claim does not say the table or the literature never excluded d = 46 or 47 before. It rests only on the table's current record. I cannot rule out an LP bound published elsewhere. The criterion only asks about the live table and propagation, so this is not a failure.

## Result
Every clause is either checked and met, or (live re-fetch) accepted on the recorded evidence. No clause is unmet or stretched.

confirmed_scope: The exact-integer Farkas certificates for the quantum weight-enumerator LP (with Rains shadow nonnegativity, and with only the criterion's listed constraints) verify for [[139,1,46]] and for [[139,1,47]], so there is no additive qubit [[139,1,d]] code for d >= 46 and the codetables.de upper bound for [[139,1]], which was 47 at the recorded fetch of 2026-10-16T19:43Z, can be lowered to at most 45, and the closure of the other live cells under the stated propagation rules at (139,1) is 47, so this is not implied by them.

pass: true
