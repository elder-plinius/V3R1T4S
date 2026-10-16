context: subagent (same VM)

# REPRODUCE skeptic verdict

Scope: read and ran only files inside this folder; no web, no GitHub tool.

## Definition implemented (quoted from my_checker.py docstring, written before reading check/check_cert.py)
    S = stabilizer (additive self-orthogonal code over GF(4)), |S| = 2^(n-k), A_i = #elements of weight i.
    Normalizer N = S^perp (trace-Hermitian dual), |N| = 2^(n+k), B_j = (1/|S|) sum_i K_j(i) A_i  (MacWilliams),
    K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
    Shadow (Rains): Sh_j = (1/|S|) sum_i (-1)^i K_j(i) A_i >= 0.
    Distance d: no element of N\S of weight < d, i.e. A_j = B_j for 1<=j<d; S subset N so A_j <= B_j all j;
    A_0 = 1; sum A_i = 2^(n-k); A_i >= 0.
    Scaled by M=2^(n-k): E0: A_0=1; E1: sum A_i = M; Q_j (1<=j<d): M A_j - sum_i K_j(i)A_i = 0;
    G_j (d<=j<=n): sum_i K_j(i)A_i - M A_j >= 0; H_j (0<=j<=n): sum_i (-1)^i K_j(i)A_i >= 0.
    Farkas: equalities with free multipliers u, >= rows with multipliers v>=0; if all column coefficients are <= 0
    and sum u*b > 0 then for A>=0: 0 >= y.A = sum u*b + sum v*(g.A) >= sum u*b > 0, contradiction.
Why each row holds for every [[n,k,d]] code: MacWilliams for the additive code S and its dual N; N\S has no word of
weight < d by definition of distance (pure or impure); S subset N gives B_j >= A_j; the shadow is a coset-type weight
enumerator of an additive code (Rains), hence has nonnegative integer coefficients; A_0=1 and |S|=2^(n-k) are basic.
A d=44 certificate also covers any code with distance >= 44 (so it excludes d=44,45,...).

## Own checks (files: my_checker.py, my_checker2.py, my_selftest.py, my_prop.py)
Certificate format inferred from keys (u_E0,u_E1 equality E0,E1; u_Q on j=1..d-1; v_G on j>=d; v_H on 0..n). my_checker2.py
tried all sign/scale conventions of the free multipliers; exactly the convention "u_Q multiplies (K_j.A - M A_j), u_E0 on
column 0 with unit scale" gives 0 positive columns and positive RHS (this is the same convention the author states).

Commands and real output:

    python3 -I my_selftest.py
    Krawtchouk generating-function identity OK        (sum_j K_j(i)x^j = (1-x)^i (1+3x)^(n-i), n=5,9,13, all i)
    B ['1','0','0','30','15','18'] Sh ['1','0','0','30','15','18']     ([[5,1,3]] sanity: B and shadow correct)
    negative controls: halving a v_G multiplier -> NOT PROVEN; dropping a v_H multiplier -> NOT PROVEN
    (a control that only changed the d field 44->45 stayed proven: expected, the 44 certificate uses only rows
     that also exist in the d=45 LP, since G_44 has multiplier 0 and uQ_44 is absent)

    python3 -I my_checker.py result/cert_132_1_44_sh.json result/cert_132_1_45_sh.json
    result/cert_132_1_44_sh.json e0scale 1 cols>0: [] maxcoef<=0: True rhs>0: True rhs bits 3635 -> INFEASIBLE-PROVEN
    result/cert_132_1_45_sh.json e0scale 1 cols>0: [] maxcoef<=0: True rhs>0: True rhs bits 3567 -> INFEASIBLE-PROVEN
    exit 0

Index-range/sign asserts in my checker passed (u_Q in 1..d-1, v_G in d..n, v_H in 0..n, v >= 0).

## Author's checker, run after mine
    python3 -I check/check_cert.py result/cert_132_1_44_sh.json
    VERIFIED [[132,1,44]] shadow=True: value=1095 digits, max column coefficient <= 0, 43+2+41 multipliers   exit 0
    python3 -I check/check_cert.py result/cert_132_1_45_sh.json
    VERIFIED [[132,1,45]] shadow=True: value=1074 digits, max column coefficient <= 0, 44+2+44 multipliers   exit 0
Agrees with check/checker_output.txt and with my checker (value 1095 digits ~ my 3635-bit RHS; same convention).
Reran twice: identical output hashes (deterministic).

## Propagation check (REPRODUCE.md step 3, run in a scratch dir, then removed)
    python3 -I check/parse_table.py data/qubit_table_full_n1-256.html scratch/parsed.json   -> cells 33152 n-range 1 256
    python3 -I check/propagate.py scratch/parsed.json scratch/closure.json
        -> cells k>=1: 32896  live > implied: 1075  of which n>100: 1072  n<=100: 3
    python3 -I -c "...print(T['132']['1'], C['132,1'])"   -> [27, 45] 45     (expected [27, 45] 45: matches)
My own independent parser/closure (python3 -I my_prop.py): 33152 cells parsed, equal to the number of title="n=.., k=.."
occurrences; (132,1)=27-45; neighbours (131,1)=45, (133,1)=45, (131,2)=45 (so R3 gives 46), (132,2)=45; closure(132,1)=45
= live value; min live U(n,1) for n>=132 is 45. Hence 43 (or 44) is not implied by R1/R2/R3 from other live cells.
Note: the live table is non-monotone in 1075 other cells (author reports this honestly); irrelevant for (132,1).

## Data integrity
sha256 of data/QECC_q4_n132_k1_claimtime.html = 61399b24...b2bd11 and of data/qubit_table_full_n1-256.html = 26245491...de4b0b6
both equal the hashes in CLAIM.md. The saved single-cell page reads "Bounds on [[132,1]] lower bound: 27 upper bound: 45".

## Limits / mismatches
No mismatch found. Not verifiable by me (no web allowed): that the table was re-fetched live "immediately before claiming";
I can only confirm the saved claim-time files are internally consistent with the claim. The Rains shadow nonnegativity and
the MacWilliams identity were re-derived/sanity-tested ([[5,1,3]]) but their general proofs rest on the cited papers.
The search is not a sample: the Farkas inequality was checked on all 133 columns for both certificates.

pass: true
