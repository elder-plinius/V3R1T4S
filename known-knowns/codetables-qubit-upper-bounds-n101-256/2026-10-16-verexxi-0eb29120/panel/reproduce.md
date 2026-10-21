# VERDICT (REPRODUCE skeptic)

context: subagent (same VM)

Scope: I read and ran only files inside this folder (CLAIM.md, REPRODUCE.md, result/, data/ pages for the table, check/ after my verdict). No web, no GitHub. My own scripts are in mine/.

## Definition (quoted from my checker mine/my_checker.py, written BEFORE opening check/*.py)
```
DEFINITION (qubit stabilizer-code LP). An [[n,k,d]] stabilizer code has a stabilizer S, an
additive self-orthogonal (trace-Hermitian) subgroup of F_4^n of size 2^(n-k), normalizer N=S^perp
of size 2^(n+k), S subset N, d = min wt(N \ S). Let A_i = #{s in S: wt s=i}, B_i = #{u in N: wt u=i}.
(1) A_0=1, sum_i A_i = 2^(n-k).
(2) MacWilliams (CRSS Thm 5): B_j = 2^-(n-k) sum_i K_j(i) A_i,
    K_j(i)=sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s)   [coefficient of y^j in (x+3y)^(n-i)(x-y)^i].
(3) S subset N so A_j <= B_j for all j; no word of N\S has weight <d so A_j=B_j for 1<=j<d.
(4) Rains shadow: Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i >= 0 for all j.
    Proof: s -> wt(s)+<u,s> mod 2 is additive on S (wt(s+t)=wt s+wt t+<s,t> mod 2, <s,t>=0 on S),
    so sum_{s in S}(-1)^{wt s+<u,s>} = |S| if u in shadow else 0; summing over u of weight j and using
    sum_{wt u=j}(-1)^{<u,s>}=K_j(wt s) gives Sh_j = #(shadow words of weight j) >= 0.
FARKAS: rows multiplied by M=2^(n-k), variables A>=0:
  E0: A_0 = 1 ; E1: sum A_i = M ; Q_j (1<=j<d): sum_i K_j(i)A_i - M A_j = 0 (sign free);
  G_j (j>=d): sum_i K_j(i) A_i - M A_j >= 0 ; H_j: sum_i (-1)^i K_j(i) A_i >= 0.
If u (free), v>=0 give column sums c_i <= 0 for all i = 0..n and rhs u0*1+u1*M > 0, then
0 >= sum c_i A_i = rhs + sum v*(row.A) >= rhs > 0: contradiction, so no such code exists.
```
Re-derivation of each step: (1) trivial (identity word; |S|=2^(n-k)). (2) A(x+3y,x-y)/|S| with the coefficient extraction stated above; N=S^perp has size 2^(n+k) so the MacWilliams transform of A divided by |S| counts N. (3) S subset N gives A_j<=B_j; the definition of d as min weight of N\S gives A_j=B_j for 0<j<d. (4) shadow argument above. Farkas step: valid since every G,H row is in ">= 0" form with multiplier >= 0, the Q,E rows are equalities (any sign), and c_i<=0, A_i>=0 give sum c_i A_i <= 0.

## Sanity of my definitions by brute force (mine/sanity.py)
Enumerated S, N and the shadow {u : <u,s> = wt(s) mod 2 for all s in S} explicitly and compared with the formulas (exact Fractions), for the 5-qubit code, Steane, [[4,2,2]], [[1,0]] (Z), [[3,1]] (ZII,IZI), [[3,0]] (XXX,ZZI,IZZ), [[6,0]] graph-like state:
```
5-qubit A [1, 0, 0, 0, 15, 0] B [1, 0, 0, 30, 15, 18] Sh [1, 0, 0, 30, 15, 18] d 3 identities+constraints ok: True
Steane A [1, 0, 0, 0, 21, 0, 42, 0] B [1, 0, 0, 21, 21, 126, 42, 45] Sh [1, 0, 0, 21, 21, 126, 42, 45] d 3 identities+constraints ok: True
[[4,2,2]] A [1, 0, 0, 0, 3] B [1, 0, 18, 24, 21] Sh [1, 0, 18, 24, 21] d 2 identities+constraints ok: True
[[6,0,?]] GHZ-ish A [1, 0, 15, 0, 15, 0, 33] B [1, 0, 15, 0, 15, 0, 33] Sh [1, 0, 15, 0, 15, 0, 33] d 7 identities+constraints ok: True
[[1,0]] Z A [1, 1] B [1, 1] Sh [0, 2] d 2 identities+constraints ok: True
[[3,1]] ZII,IZI A [1, 2, 1, 0] B [1, 5, 7, 3] Sh [0, 0, 4, 12] d 1 identities+constraints ok: True
[[3,0]] GHZ-like XXX,ZZI,IZZ A [1, 0, 3, 4] B [1, 0, 3, 4] Sh [0, 3, 0, 5] d 4 identities+constraints ok: True
```

## My checker on the certificates (exact integers, all 155 columns, Krawtchouk computed from the binomial sum)
Command: `python3 -I mine/my_checker.py result/cert_154_1_51_sh.json result/cert_154_1_52_sh.json`
```
result/cert_154_1_51_sh.json n,k,d= 154 1 51 shadow flag True
 #Q 50 #G 2 #H 51 Q-indices complete 1..d-1: True
 max column coefficient <= 0 : True  (#positive columns 0 )
 rhs > 0 : True  rhs sign 1 digits 1439
 RESULT VERIFIED
result/cert_154_1_52_sh.json n,k,d= 154 1 52 shadow flag True
 #Q 51 #G 2 #H 49 Q-indices complete 1..d-1: True
 max column coefficient <= 0 : True  (#positive columns 0 )
 rhs > 0 : True  rhs sign 1 digits 1540
 RESULT VERIFIED
```
Index ranges checked (Q in 1..d-1 and complete, G in d..n, H in 0..n), all G,H multipliers >= 0. Two runs give byte-identical output (cmp: deterministic).
Negative controls (mine/negctl.py), all correctly FAILED: perturb u_E1 by 10^60 (1 positive column); drop one shadow row (51 positive columns); drop Q_7 (63 positive columns); u_E0 large negative (rhs < 0).
Result: [[154,1,51]] infeasible (so no [[154,1,d]] with d>=51 exists; upper bound <= 50), and [[154,1,52]] infeasible.

## Propagation (own implementation mine/my_prop.py on data/qubit_table_full_n1-256.html; sha256 of both saved pages match CLAIM.md)
sha256: qubit_table_full 26245491ba11...de4b0b6, QECC_q4_n154_k1_claimtime beef68a113ab...d7d4a5 (verified with sha256sum, identical to CLAIM.md).
The saved single-cell page says "Bounds on [[154,1]] lower bound: 33 upper bound: 52".
```
cells 33152 n range 1 256
iterations 16
table (154,1) (33, 52) closure 52
(154, 2) (30, 52) 52 ; (155, 1) (33, 53) 53 ; (153, 2) (30, 51) 51 ; (154, 0) (18, 46) 46 ; (153, 1) (33, 51) 51
```
Closure under R1 (k>=2), R2, R3 at (154,1) is 52 (via R3: (153,2) 51 + 1; R2: (155,1) 53). So 50 (or 51) is not implied by the listed propagation rules. The author's propagation scripts were re-run as in REPRODUCE.md step 3 and print `[33, 52] 52`, same as mine.

## Author's checker (compared only after the verdict above)
`python3 -I check/check_cert.py result/cert_154_1_51_sh.json` -> `VERIFIED [[154,1,51]] shadow=True: value=1439 digits, max column coefficient <= 0, 50+2+51 multipliers` (exit 0)
`python3 -I check/check_cert.py result/cert_154_1_52_sh.json` -> `VERIFIED [[154,1,52]] shadow=True: value=1540 digits, max column coefficient <= 0, 51+2+49 multipliers` (exit 0)
Same output as check/checker_output.txt. Its LP (E0,E1,Q,G,H rows, signs, Farkas rule) is identical to mine; its column sums agree with mine in verdict.

## Mismatches / caveats
- No mismatch in the mathematics or the certificates.
- check/propagation_check.txt contains only the one-line (154,1) summary (live [33,52], closure 52, neighbours R2 [33,53], R3 [30,51]); the stdout of check/propagate.py is a longer list. Not a content conflict: both agree on closure 52 at (154,1), and my own implementation agrees. Cosmetic: the checker prints "value=1439 digits" (it is the digit count of the value).
- Cannot be verified here (no web allowed): that codetables.de still says 52 at the moment of reading. Only the saved page (2026-10-16T19:44:15Z) was confirmed.
- The data/TROPHY_CASE_pinned_9b1d444.md file is unrelated to this check; I did not rely on it.

pass: true
