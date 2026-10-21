# VERDICT (REPRODUCE skeptic) -- claim: no [[164,1,54]] qubit stabilizer code (and none with d=55)

context: subagent (same VM)

Scope: only files inside this folder were read or run. No web, no GitHub tool.

## Definition used (quoted from my own checker, mine/my_checker.py, written BEFORE reading check/check_cert.py)

> An [[n,k,d]] stabilizer code is given by a self-orthogonal (trace-symplectic) additive code S <= GF(4)^n, |S| = 2^(n-k) =: 2^m,
> with normalizer N = S^perp, |N| = 2^(n+k), and d = min wt(N \ S). Let A_i = #{s in S: wt s = i}, B_i = #{v in N: wt v = i}.
> (1) A_0 = 1 ; sum_i A_i = 2^m.
> (2) Quaternary MacWilliams: B_j = 2^-m * sum_i K_j(i) A_i, K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
> (3) S <= N so A_j <= B_j for every j; N\S has min weight d so A_j = B_j for 1 <= j < d.
> (4) Rains shadow: Sh_j = 2^-m * sum_i (-1)^i K_j(i) A_i >= 0 for all j.
> Farkas: equalities a_r.A = b_r (multiplier u_r free), valid inequalities g_s.A >= 0 (multiplier v_s >= 0). If
> c := sum u_r a_r + sum v_s g_s has c_i <= 0 for all i and R := sum u_r b_r > 0, then for feasible A >= 0:
> c.A = R + sum v_s g_s.A >= R > 0 but c.A <= 0, contradiction; the LP is infeasible.

Rows used (integers, multiplied by 2^m, m = n-k = 163): E0: A_0 = 1; E1: sum A_i = 2^m; Q_j (1<=j<d): sum_i K_j(i)A_i - 2^m A_j = 0;
G_j (j>=d): g_j.A = sum_i K_j(i)A_i - 2^m A_j (= 2^m(B_j-A_j)) >= 0; H_j: h_j.A = sum_i (-1)^i K_j(i) A_i (= 2^m Sh_j) >= 0.
A code of distance >= d (not only exactly d) satisfies all these rows, so infeasibility excludes every [[164,1,>=d]] stabilizer code.

## Re-derivation of each constraint on small codes (mine/lp_sanity.py)
Brute force over 360 random stabilizer codes with n = 2..7 (symplectic representation, S, N = S^perp, shadow
= {v : <v,s> = wt(s) mod 2 for all s in S}), all with Fractions: B_j from MacWilliams equals the true normalizer count;
Sh_j equals the true shadow count (hence >= 0 and integral); A_j <= B_j; A_j = B_j for 1 <= j < d.

    $ python3 -I mine/lp_sanity.py
    codes checked 360 all: MacWilliams B, shadow==count, A<=B, A=B below d  OK

## Certificate check with my own checker (exact Python integers, no floats)
Reading of the JSON keys (u_E0,u_E1 = free multipliers on E0,E1; u_Q on Q_j; v_G on G_j; v_H on H_j) was inferred from
the key names and the LP; the inequality orientation was derived from validity (g_j >= 0 and h_j >= 0 are the valid
directions; first attempt with the wrong orientation FAILED, correcting it per the Farkas derivation above gave the result below).
Sign exploration (mine/explore.py) showed the only consistent pattern with R > 0 is the natural one (u as stored, +v on valid >= rows).

    $ python3 -I mine/my_checker.py result/cert_164_1_54_sh.json result/cert_164_1_55_sh.json
    MY_VERIFIED flipQ=False result/cert_164_1_54_sh.json {'n': 164, 'k': 1, 'd': 54, 'max_col': 0, 'all_cols_le0': True, 'rhs_positive': True, 'nnz_cols': 164, 'rhs_digits': 1685, ...}
    MY_VERIFIED flipQ=False result/cert_164_1_55_sh.json {'n': 164, 'k': 1, 'd': 55, 'max_col': 0, 'all_cols_le0': True, 'rhs_positive': True, 'nnz_cols': 164, 'rhs_digits': 1830, ...}
    (the extra flipQ=True lines are a deliberately wrong sign control and FAIL, as they should)

Index ranges checked: u_Q = 1..d-1 (53 resp. 54 entries), v_G = {56,57} resp. {57,58} (all >= d), v_H subset of 0..n, all v >= 0.
Negative controls (mine/ only): dropping one or all shadow multipliers -> a column becomes positive (FAIL);
making u_E0 hugely negative -> R <= 0 (FAIL). So the check is not vacuous.

## Author's checker (compared only AFTER my verdict was formed)
    $ python3 -I check/check_cert.py result/cert_164_1_54_sh.json   (run twice, identical output, exit=0)
    VERIFIED [[164,1,54]] shadow=True: value=1685 digits, max column coefficient <= 0, 53+2+53 multipliers
    $ python3 -I check/check_cert.py result/cert_164_1_55_sh.json
    VERIFIED [[164,1,55]] shadow=True: value=1830 digits, max column coefficient <= 0, 54+2+55 multipliers
Its docstring states exactly the same LP and Farkas rule as mine; its code combines the same rows. Deterministic, matches check/checker_output.txt.

## Propagation / table checks (REPRODUCE.md step 3, plus my own parser mine/my_prop.py)
    $ sha256sum data/*  -> QECC html 05af667a...b1d8, full table 26245491...4b6, as stated in CLAIM.md
    $ python3 -I check/parse_table.py data/qubit_table_full_n1-256.html mine/parsed.json   -> cells 33152 n-range 1 256
    $ python3 -I check/propagate.py mine/parsed.json mine/closure.json   -> cells k>=1: 32896 live > implied: 1075 ...
    $ python3 -c "...print(T['164']['1'], C['164,1'])"   -> [33, 55] 55
    $ python3 -I mine/my_prop.py -> (164,1)=55 (165,1)=55 (163,2)=55 closure(164,1)=55, implied bound <=53? False
Saved single-cell page says "Bounds on [[164,1]]" (saved table shows 33-55). R1/R2/R3 are valid rules ([[n,k,d]]->[[n,k-1,d]], [[n+1,k,d]], [[n-1,k+1,d-1]]); the closure of the saved live table at (164,1) is 55, so 53 (or 54) is not implied by other cells.

## Mismatches / caveats
- No mismatch found in certificates, propagation, or hashes of the saved files.
- Not verifiable from this folder: that the data files really are the live codetables.de pages (only their stated hashes and internal consistency can be checked; no web allowed).
- The saved table is itself non-monotone in 1075 cells (live > closure), so it is a snapshot with slack; irrelevant to the (164,1) closure, which is computed from the saved snapshot as the criterion states.
- The surprising size of the improvement (55 -> 53) is not something I can judge; the mathematical certificate itself is sound as checked.
- My key-orientation reading was guessed first and corrected via the Farkas derivation (disclosed above); no ambiguity remains since the check is justified by validity of each row, which I tested on brute-forced codes.

pass: true
