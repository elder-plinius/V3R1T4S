# Skeptic Panel Report: REPRODUCE

> **Dated Note (2026-10-29):** This panel report originally reviewed the earlier three-base + audit version under `claim/`, which has since been split into **#517** (this package: base 50, where `claim/lychrel_base50_certificate.json` is now at `object/lychrel_base50_certificate.json` with identical `sha256: dd093b972a4f7eb7d6d9db4c5809a3332e413868719635bb6d2fdc9e59dacdb2`), **#723** (base 98), **#724** (base 146), and **#725** (Kuitché 2023 audit). The other `claim/` files (`CLAIM.md`, `REPRODUCE.md`, `lychrel_base98_certificate.json`, `lychrel_base146_certificate.json`, `seal_base26_baseline_certificate.json`, `kuitche_2023_audit.json`) and copied third-party pages/PDFs (`Lychrel_number.html`, `dseal_live.htm`, `rs_2659802.pdf`) named below are no longer included in this directory.

role: REPRODUCE
context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)

## 1. Quoted Definitions and Verification Mandate

Before reading `how-we-built-it/author_checker_lychrel_check.py`, an independent checker (`indep_lychrel_check.py`) was written from scratch directly from the mathematical definition of a base-$b$ Lychrel number and the target verification specification:

- **Mathematical Definition (Base-$b$ Reverse-and-Add and Lychrel Number):** For an integer base $b \ge 2$ and a positive integer $x$ with canonical base-$b$ digit expansion $x = \sum_{j=0}^{L-1} d_j b^{L-1-j}$ ($d_0 \neq 0$, $0 \le d_j \le b-1$), the base-$b$ reversal is $\operatorname{Rev}_b(x) = \sum_{j=0}^{L-1} d_j b^j$, and one reverse-and-add step is $F_b(x) = x + \operatorname{Rev}_b(x)$. A positive integer $n$ is a base-$b$ Lychrel number if for every integer $t \ge 1$, the iterate $F_b^t(n)$ is not a base-$b$ palindrome ($\operatorname{digits}_b(F_b^t(n)) \neq \operatorname{Rev}(\operatorname{digits}_b(F_b^t(n)))$).
- **Quoted `success_criterion`:**
  `CONFIRMED only with: (1) a start n and templates T_1..T_k (digit strings with integer-parameter repeated blocks); (2) a proof of closure under reverse-and-add for ALL parameter values that is either formalized (Lean/Coq, no sorry) or reduced to a finite mechanical check. Acceptable reductions are a finite automaton or transducer argument, or an explicit symbolic carry computation in which every parameter-dependent block is shown to produce a constant digit/carry run, together with brute force over all parameters below the threshold; (3) a proof that no template string is a palindrome; (4) a demonstration that n's orbit enters the template set; (5) a base b not in {2^k, 11, 17, 20, 26} and not listed as proven on https://en.wikipedia.org/wiki/Lychrel_number AT VERIFICATION TIME, plus a novelty search (Wikipedia references, OEIS, arXiv, the 2023 construction paper if obtainable). If step (2) only covers parameters up to some P, report 'VERIFIED FOR PARAMETERS leq P, GENERAL CASE UNPROVEN' with no claim. Any step needing 'by inspection' fails unless formalized. A base-10 proof would be a moonshot-level event.`

## 2. File Integrity Verification (`object/lychrel_base50_certificate.json`)

The base-50 certificate in this package (and the companion files from the initial multi-base run now split into #723, #724, and #725) was checked for exact byte count and SHA-256 digest prior to running any author code:

| File in This Package | Bytes | SHA-256 Digest | Status |
| :--- | ---: | :--- | :--- |
| `object/lychrel_base50_certificate.json` | `34,276` | `dd093b972a4f7eb7d6d9db4c5809a3332e413868719635bb6d2fdc9e59dacdb2` | PASS |

## 3. Independent Checker Architecture and Negative Controls

The independent checker `indep_lychrel_check.py` implemented:
1. **Symbolic Run-Length Block-by-Block Reverse-and-Add (`symbolic_rev_add`):** Reconstructs normalized run-length blocks `(digit, a, c)` (representing `digit` repeated $a m + c$ times for $m \ge 1$) directly from `(prefix, left_repeat_digit, middle, right_repeat_digit, suffix)`, aligns $T_i(m)$ from LSB to MSB against $\operatorname{Rev}_b(T_i(m))$ using the exact linear dominance condition $\Delta a \ge 0 \wedge \Delta a + \Delta c \ge 0$ for all $m \ge 1$, steps through fixed-length blocks ($a = 0$), and enforces that every parameter-dependent block ($a \ge 1$) produces a constant output digit ($d_{\text{out},1} = d_{\text{out},2}$) and a constant outgoing carry equal to its incoming carry ($c_{\text{out}} = c_{\text{in}}$).
2. **Independent Block-Carry Re-derivation:** Independently computes the exact base-$b$ integer sums and carries $(c_R, c_M, c_L)$ on the fixed outer blocks $(L_0, R_0, L_1, R_1)$ and inner cores $(M_0, M_1, M_2, M_3)$ for all four phases:
   - Phases 0 and 2 ($T_1(m) \to T_2(m)$ and $T_3(m) \to T_4(m)$): $R_0 + \operatorname{Rev}(L_0) = R_1$ with $c_R = 0$; $(0^m + (b-1)^m, c_{\text{in}}=0) \to ((b-1)^m, c_{\text{out}}=0)$; $M_{2k} + \operatorname{Rev}(M_{2k}) + 0 = b^{|M_{2k}|} + M_{2k+1}$ with $c_M = 1$; $((b-1)^m + 0^m, c_{\text{in}}=1) \to (0^m, c_{\text{out}}=1)$; $L_0 + \operatorname{Rev}(R_0) + 1 = L_1$ with $c_L = 0$.
   - Phases 1 and 3 ($T_2(m) \to T_3(m)$ and $T_4(m) \to T_1(m+1)$): $R_1 + \operatorname{Rev}(L_1) = b^{\ell} + R_0$ with $c_R = 1$; $((b-1)^m + 0^m, c_{\text{in}}=1) \to (0^m, c_{\text{out}}=1)$; $M_1 + \operatorname{Rev}(M_1) + 1 = M_2[1..|M_1|]$ with $c_M = 0$ (and in Phase 3, $M_3 + \operatorname{Rev}(M_3) + 1 = M_0 \cdot [0]$ with $c_M = 0$, appending one $0$ to $0^m \to 0^{m+1}$); $(0^m + (b-1)^m, c_{\text{in}}=0) \to ((b-1)^m, c_{\text{out}}=0)$; $L_1 + \operatorname{Rev}(R_1) + 0 = L_0 \cdot [b-1]$ with overflow carry $c_L = 1$ (prepending $b-1$ to $M_2[1..|M_1|]$ in Phase 1 and extending $(b-1)^m \to (b-1)^{m+1}$ in Phase 3).
3. **Symbolic Non-Palindromicity (`symbolic_is_non_palindrome`):** Symbolically aligns $T_i(m)$ against $\operatorname{Rev}_b(T_i(m))$ for all $m \ge 1$ and checks both endpoint digits ($L_0[0] \neq R_0[\ell-1]$, $L_1[0] \neq R_1[\ell-1]$) and mirrored symbolic wires ($(b-1)^m$ vs $0^m$ at offset $\ell$).
4. **Negative Controls Verified Before Positive Runs:**
   - *Negative Control 1 (Corrupted Middle Digit):* Incrementing `T_1(m)` block 38 mod 50 caused `symbolic_rev_add` to mismatch `T_2(m)` (`PASS`).
   - *Negative Control 2 (Non-Uniform Symbolic Carry Wire):* Changing the symbolic repeat digit from $49$ to $48$ in `T_1(m)` raised `ValueError` for non-uniform carry/digit across symbolic block of length $1m+0$ with $d_a=48, d_b=0, c_{\text{in}}=1$ yielding $(d_1=49, c_1=0)$ vs $(d_2=48, c_2=0)$ (`PASS`).
   - *Negative Control 3 (Palindromic Symbolic Template):* Passing a symmetric RLE template `[5, 49^m, 12, 12, 49^m, 5]` returned `False` from `symbolic_is_non_palindrome` (`PASS`).

## 4. Independent Verification of Base 26 (Baseline) and Base 50 (Two Deterministic Runs)

`indep_lychrel_check.py` was executed twice to verify determinism (`Run 1`: `21.22s` total, `20.62s` orbit simulation; `Run 2`: `21.27s` total, `20.70s` orbit simulation), producing identical results across both runs:

| Target | Base $b$ | Eligible New Base? | Outer $\ell$ | $|M_0|, |M_2|$ | $|T_1(1)|$ | All-$m$ Symbolic Closure | Symbolic Non-Palindrome | Seed Entry ($n_{\text{seed}} \to T_2(1)$) | Brute-Force $1 \le m \le 500$ |
| :--- | ---: | :--- | ---: | :--- | ---: | :--- | :--- | :--- | :--- |
| David Seal (1996) Baseline | $26$ | Baseline (Seal 1996) | $8$ | $4, 5$ | $22$ | PASS (4 phases, 8 sym blocks) | PASS ($1 \neq 23$, $25 \neq 24$) | PASS (step 1) | PASS ($2,000$ instances) |
| `object/lychrel_base50_certificate.json` | $50$ | Yes ($2 \cdot 5^2$) | $36$ | $8, 9$ | $82$ | PASS (4 phases, 8 sym blocks) | PASS ($1 \neq 47$, $49 \neq 48$) | PASS (step 1) | PASS ($2,000$ instances) |

- **100,000-Step Base-50 Orbit Simulation & Regex Fullmatch:** Starting from $n = T_1(1)$ (82 base-50 digits), `indep_lychrel_check.py` simulated $100,000$ reverse-and-add steps ($t = 0 \dots 100,000$), reaching length $50,082$ base-50 digits at $t = 100,000$ ($m = 25,001$). Every one of the $100,001$ iterates was verified non-palindromic and matched via `re.Pattern.fullmatch` against the compiled regex for $T_{(t \bmod 4) + 1}(\lfloor t / 4 \rfloor + 1)$ with exact symbolic wire lengths $m = \lfloor t / 4 \rfloor + 1$.
- **Cross-Check of `README.md` vs `object/lychrel_base50_certificate.json`:** All 8 base-50 block arrays ($L_0, R_0, L_1, R_1, M_0, M_1, M_2, M_3$) in `README.md` and `object/lychrel_base50_certificate.json` match digit-for-digit, and `start_n_T1_m1_base10` (`803319634591911080790138327923...75462193309396720297`) and `pre_template_seed_base10` (`121690994086842491822584267395...75462193309396720296`) in `object/lychrel_base50_certificate.json` are the exact base-10 values of $T_1(1)$ and $n_{\text{seed}}$.

## 5. Comparison with Package Verifier (`verify-it-yourself/check_lychrel.py`)

The standalone base-50 package verifier `verify-it-yourself/check_lychrel.py` produces:

```text
=== V3R1T4S Mechanical Lychrel Template-Closure Verifier (Base 50) ===
[1/5] File integrity verified for object/lychrel_base50_certificate.json.
[2/5] Baseline reproduction PASSED: David Seal Base 26 (Period 4, 8 symbolic blocks, brute-forced m=1..500).
[3/5] New Base b= 50 PASSED: symbolic all-m closure (8 uniform symbolic blocks), symbolic non-palindromicity, seed entry, and brute-force m=1..500 (|L0|=36, |M0|=8, |T_1(1)|=82).
[4/5] Base 50 orbit simulation + regex matching PASSED: 100,000 steps (t=0..100,000, final length = 50,082 base-50 digits) in 15.77s.
[5/5] Perturbation & null-model controls PASSED (corrupted M0 rejected, non-uniform carry rejected, 0/400 random 82-digit starts).
ALL CHECKS PASSED in 15.86s.
```

The independent checker and package verifier are in 100% agreement across `object/lychrel_base50_certificate.json`, symbolic carry checks, brute-force parameter sweeps, 100,000-step regex orbit verification, and negative controls. Temporary working files were cleaned up prior to completion.

pass: true
