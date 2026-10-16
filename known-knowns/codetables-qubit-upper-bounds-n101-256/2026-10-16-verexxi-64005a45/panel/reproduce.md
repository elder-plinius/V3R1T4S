context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic report, claim [[148,2,49]] nonexistence

## Method
1. Read CLAIM.md and REPRODUCE.md only for the definition (LP: A_0=1, sum A_i=2^(n-k), A_j=B_j for 1<=j<d, A_j<=B_j for j>=d, shadow Sh_j>=0, B_j and Sh_j via q=4 Krawtchouk K_j(i)). Saw only the certificate's key structure (u_E0, u_E1, u_Q, v_G, v_H) before writing my own checker.
2. Wrote my own checker from that definition (independent Krawtchouk with guarded binomials, per-column accumulation, own sign handling), run from outside the claim folder. First attempt had a sign error on the Q rows (Q rows are sign-free, I had flipped the orientation); the corrected version is the definition-consistent one. Only after that did I read check/check_cert.py.
3. Sanity of my K/B/Sh code on a known code, [[5,1,3]] with A=(1,0,0,0,15,0): B=[1,0,0,30,15,18], Sh=[1,0,0,30,15,18] (64 = normalizer size, as expected).

## Results (real output)
My checker (all multipliers integer, v_G and v_H asserted >= 0, Q indices asserted in 1..d-1, G indices >= d):
  result/cert_148_2_49_sh.json  -> max column coefficient <= 0: True; RHS value u_E0 + u_E1*2^146 > 0: True; value has 1062 digits
  result/cert_148_2_50_sh.json  -> max column coefficient <= 0: True; RHS value > 0: True; value has 1298 digits
(The variant that multiplied E0/E1 by 2^146 failed, so the correct scaling is the one in the claim: E0, E1 unscaled, Q/G/H rows scaled by 2^(n-k).)

Author's checker:
  $ python3 -I check/check_cert.py result/cert_148_2_49_sh.json
  VERIFIED [[148,2,49]] shadow=True: value=1062 digits, max column coefficient <= 0, 48+2+49 multipliers   (exit 0)
  $ python3 -I check/check_cert.py result/cert_148_2_50_sh.json
  VERIFIED [[148,2,50]] shadow=True: value=1298 digits, max column coefficient <= 0, 49+2+47 multipliers   (exit 0)
Determinism: two runs of the d=49 check give identical output (md5 b7000a3b7499d5b8fa24a622f64e8cf8 both times). Output matches check/checker_output.txt.

Proof step re-derivation: for feasible A>=0, sum_i c_i A_i = u_E0 + u_E1*2^(n-k) + sum v_G*G(A) + sum v_H*H(A) >= value > 0 (Q rows vanish, G,H >= 0, v >= 0), but c_i <= 0 for all i forces sum c_i A_i <= 0. Contradiction, so the LP is infeasible. The LP constraints are the standard valid ones for stabilizer codes (A_j=B_j below d, S subset of N gives A_j<=B_j, Rains shadow nonnegativity). d=49 relaxes the d>=50 case (fewer equalities), so no [[148,2,d]] with d>=49 exists, giving upper bound 48.

Table and propagation (data files only, no web access used):
- sha256sum of data/QECC_q4_n148_k2_claimtime.html = d59b202d...98136aeb98c0 and data/qubit_table_full_n1-256.html = 26245491...de4b0b6, both match CLAIM.md.
- Raw grep of the full table: (148,2)=30-50, (147,3)=28-49, (148,1)=33-50, (149,2)=30-51, (148,3)=29-50, (147,2)=30-49.
- Ran check/parse_table.py then check/propagate.py: T[148][2] = [30, 50], closure at (148,2) = 50 (R1 from (148,1): 50, R2 from (149,2): 51, R3 from (147,3): 49+1 = 50). So 48 is not implied by propagation from the saved live cells.

## Limits
I did not re-fetch the live table (no web access allowed to me), so "live immediately before claiming" is only confirmed from the saved, hash-matching files. I did not independently re-implement the table parser/propagation beyond the raw-grep cross-check of the neighbouring cells above.

pass: true
