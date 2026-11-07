# Skeptic Panel Report: REPRODUCE

> **Dated Note (2026-11-03):** This panel report derives from the three-skeptic evaluation conducted for [PR #517](https://github.com/elder-plinius/V3R1T4S/pull/517) (`2026-10-19-mizopl-dd093b97`), from which this single-object base-98 package (`object/lychrel_base98_certificate.json`, `sha256: 6ec98e276bfb691187e5ebdb4c8ccf0c149f2754e201e362c15a4a681dbb5256`) was split. All statements below describe this base-98 package only.

role: REPRODUCE
context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)

## 1. Quoted Definitions and Verification Mandate

Before reading `how-we-built-it/author_checker_lychrel_check.py`, an independent checker (`indep_lychrel_check.py`) was written from scratch directly from the mathematical definition of a base-$b$ Lychrel number and the target verification specification:

- **Mathematical Definition (Base-$b$ Reverse-and-Add and Lychrel Number):** For an integer base $b \ge 2$ and a positive integer $x$ with canonical base-$b$ digit expansion $x = \sum_{j=0}^{L-1} d_j b^{L-1-j}$ ($d_0 \neq 0$, $0 \le d_j \le b-1$), the base-$b$ reversal is $\operatorname{Rev}_b(x) = \sum_{j=0}^{L-1} d_j b^j$, and one reverse-and-add step is $F_b(x) = x + \operatorname{Rev}_b(x)$. A positive integer $n$ is a base-$b$ Lychrel number if for every integer $t \ge 1$, the iterate $F_b^t(n)$ is not a base-$b$ palindrome ($\operatorname{digits}_b(F_b^t(n)) \neq \operatorname{Rev}(\operatorname{digits}_b(F_b^t(n)))$).
- **Quoted `success_criterion`:**
  `CONFIRMED only with: (1) a start n and templates T_1..T_k (digit strings with integer-parameter repeated blocks); (2) a proof of closure under reverse-and-add for ALL parameter values that is either formalized (Lean/Coq, no sorry) or reduced to a finite mechanical check. Acceptable reductions are a finite automaton or transducer argument, or an explicit symbolic carry computation in which every parameter-dependent block is shown to produce a constant digit/carry run, together with brute force over all parameters below the threshold; (3) a proof that no template string is a palindrome; (4) a demonstration that n's orbit enters the template set; (5) a base b not in {2^k, 11, 17, 20, 26} and not listed as proven on https://en.wikipedia.org/wiki/Lychrel_number AT VERIFICATION TIME, plus a novelty search (Wikipedia references, OEIS, arXiv, the 2023 construction paper if obtainable). If step (2) only covers parameters up to some P, report 'VERIFIED FOR PARAMETERS leq P, GENERAL CASE UNPROVEN' with no claim. Any step needing 'by inspection' fails unless formalized. A base-10 proof would be a moonshot-level event.`

## 2. File Integrity Verification (`object/lychrel_base98_certificate.json`)

The base-98 certificate in this package was checked for exact byte count and SHA-256 digest prior to running any author code:

| File in This Package | Bytes | SHA-256 Digest | Status |
| :--- | ---: | :--- | :--- |
| `object/lychrel_base98_certificate.json` | `38,310` | `6ec98e276bfb691187e5ebdb4c8ccf0c149f2754e201e362c15a4a681dbb5256` | PASS |

## 3. Independent Checker Architecture and Negative Controls

The independent checker `indep_lychrel_check.py` implemented:
1. **Symbolic Run-Length Block-by-Block Reverse-and-Add (`symbolic_rev_add`):** Reconstructs normalized run-length blocks `(digit, a, c)` (representing `digit` repeated $a m + c$ times for $m \ge 1$) directly from `(prefix, left_repeat_digit, middle, right_repeat_digit, suffix)`, aligns $T_i(m)$ from LSB to MSB against $\operatorname{Rev}_b(T_i(m))$ using the exact linear dominance condition $\Delta a \ge 0 \wedge \Delta a + \Delta c \ge 0$ for all $m \ge 1$, steps through fixed-length blocks ($a = 0$), and enforces that every parameter-dependent block ($a \ge 1$) produces a constant output digit ($d_{\text{out},1} = d_{\text{out},2}$) and a constant outgoing carry equal to its incoming carry ($c_{\text{out}} = c_{\text{in}}$).
2. **Independent Block-Carry Re-derivation:** Independently computes the exact base-$b$ integer sums and carries $(c_R, c_M, c_L)$ on the fixed outer blocks $(L_0, R_0, L_1, R_1)$ and inner cores $(M_0, M_1, M_2, M_3)$ for all four phases:
   - Phases 0 and 2 ($T_1(m) \to T_2(m)$ and $T_3(m) \to T_4(m)$): $R_0 + \operatorname{Rev}(L_0) = R_1$ with $c_R = 0$; $(0^m + (b-1)^m, c_{\text{in}}=0) \to ((b-1)^m, c_{\text{out}}=0)$; $M_{2k} + \operatorname{Rev}(M_{2k}) + 0 = b^{|M_{2k}|} + M_{2k+1}$ with $c_M = 1$; $((b-1)^m + 0^m, c_{\text{in}}=1) \to (0^m, c_{\text{out}}=1)$; $L_0 + \operatorname{Rev}(R_0) + 1 = L_1$ with $c_L = 0$.
   - Phases 1 and 3 ($T_2(m) \to T_3(m)$ and $T_4(m) \to T_1(m+1)$): $R_1 + \operatorname{Rev}(L_1) = b^{\ell} + R_0$ with $c_R = 1$; $((b-1)^m + 0^m, c_{\text{in}}=1) \to (0^m, c_{\text{out}}=1)$; $M_1 + \operatorname{Rev}(M_1) + 1 = M_2[1..|M_1|]$ with $c_M = 0$ (and in Phase 3, $M_3 + \operatorname{Rev}(M_3) + 1 = M_0 \cdot [0]$ with $c_M = 0$, appending one $0$ to $0^m \to 0^{m+1}$); $(0^m + (b-1)^m, c_{\text{in}}=0) \to ((b-1)^m, c_{\text{out}}=0)$; $L_1 + \operatorname{Rev}(R_1) + 0 = L_0 \cdot [b-1]$ with overflow carry $c_L = 1$ (prepending $b-1$ to $M_2[1..|M_1|]$ in Phase 1 and extending $(b-1)^m \to (b-1)^{m+1}$ in Phase 3).
3. **Symbolic Non-Palindromicity (`symbolic_is_non_palindrome`):** Symbolically aligns $T_i(m)$ against $\operatorname{Rev}_b(T_i(m))$ for all $m \ge 1$ and checks both endpoint digits ($L_0[0] \neq R_0[\ell-1]$, $L_1[0] \neq R_1[\ell-1]$) and mirrored symbolic wires ($(b-1)^m$ vs $0^m$ at offset $\ell$).
4. **Negative Controls Verified Before Positive Runs:**
   - *Negative Control 1 (Corrupted Middle Digit):* Incrementing a middle digit of $M_0$ in $T_1(m)$ caused `symbolic_rev_add` to mismatch $T_2(m)$ (`PASS`).
   - *Negative Control 2 (Non-Uniform Symbolic Carry Wire):* Changing the symbolic repeat digit from $b-1 = 97$ to $b-2 = 96$ in $T_1(m)$ raised `ValueError` for non-uniform carry/digit across the symbolic block (`PASS`).
   - *Negative Control 3 (Palindromic Symbolic Template):* Passing a symmetric RLE template returned `False` from `symbolic_is_non_palindrome` (`PASS`).

## 4. Independent Verification of Base 26 (Baseline) and Base 98 (Two Deterministic Runs)

`indep_lychrel_check.py` was executed twice to verify determinism, producing identical results across both runs:

| Target | Base $b$ | Eligible New Base? | Outer $\ell$ | $|M_0|, |M_2|$ | $|T_1(1)|$ | All-$m$ Symbolic Closure | Symbolic Non-Palindrome | Seed Entry ($n_{\text{seed}} \to T_2(1)$) | Brute-Force $1 \le m \le 500$ |
| :--- | ---: | :--- | ---: | ---: | ---: | :--- | :--- | :--- | :--- |
| David Seal (1996) Baseline | $26$ | Baseline (Seal 1996) | $8$ | $4, 5$ | $22$ | PASS (4 phases, 8 sym blocks) | PASS ($1 \neq 23$, $25 \neq 24$) | PASS (step 1) | PASS ($2,000$ instances) |
| `object/lychrel_base98_certificate.json` | $98$ | Yes ($2 \cdot 7^2$) | $37$ | $16, 17$ | $92$ | PASS (4 phases, 8 sym blocks) | PASS ($1 \neq 95$, $97 \neq 96$) | PASS (step 1) | PASS ($2,000$ instances) |

- **2,000-Step Base-98 Orbit Simulation & Regex Fullmatch:** Starting from $n = T_1(1)$ (92 base-98 digits), `verify-it-yourself/check_lychrel.py` simulated $2,000$ reverse-and-add steps (`t = 0 .. 2,000`), reaching length $1,092$ base-98 digits at $t = 2,000$ ($m = 501$). Every one of the $2,001$ iterates was verified non-palindromic and matched via `re.Pattern.fullmatch` against the compiled regex for $T_{(t \bmod 4) + 1}(\lfloor t / 4 \rfloor + 1)$ with exact symbolic wire lengths $m = \lfloor t / 4 \rfloor + 1$.
- **Cross-Check of `README.md` vs `object/lychrel_base98_certificate.json`:** All 8 base-98 block arrays ($L_0, R_0, L_1, R_1, M_0, M_1, M_2, M_3$), sizes, and base-10 values (`start_n_T1_m1_base10` and `pre_template_seed_base10`) in `object/lychrel_base98_certificate.json` match the base-98 digit arrays $T_1(1)$ and $n_{\text{seed}}$ exactly.

## 5. Comparison with Package Verifier (`verify-it-yourself/check_lychrel.py`)

The standalone base-98 package verifier `verify-it-yourself/check_lychrel.py` produces:

```text
=== V3R1T4S Mechanical Lychrel Template-Closure Verifier (Base 98) ===
[1/5] File integrity verified for object/lychrel_base98_certificate.json.
[2/5] Baseline reproduction PASSED: David Seal Base 26 (Period 4, 8 symbolic blocks, brute-forced m=1..500).
[3/5] New Base b= 98 PASSED: symbolic all-m closure (8 uniform symbolic blocks), symbolic non-palindromicity, seed entry, and brute-force m=1..500 (|L0|=37, |M0|=16, |T_1(1)|=92).
[4/5] Base 98 orbit simulation + regex matching PASSED: 2,000 steps (t=0..2,000, final length = 1,092 base-98 digits) in 0.02s.
[5/5] Perturbation & null-model controls PASSED (corrupted M0 rejected, non-uniform carry rejected, 0/400 random 92-digit starts).
ALL CHECKS PASSED in 0.28s.
```

The independent checker and package verifier are in 100% agreement across `object/lychrel_base98_certificate.json`, symbolic carry checks, brute-force parameter sweeps, 2,000-step regex orbit verification (`t = 0..2,000`), and negative controls. Temporary working files were cleaned up prior to completion.

pass: true
