# Skeptic Panel Report — Role: CRITERION

> **Dated Note (2026-11-03):** This panel report derives from the three-skeptic evaluation conducted for [PR #517](https://github.com/elder-plinius/V3R1T4S/pull/517) (`2026-10-19-mizopl-dd093b97`), from which this single-object base-98 package (`object/lychrel_base98_certificate.json`, `sha256: 6ec98e276bfb691187e5ebdb4c8ccf0c149f2754e201e362c15a4a681dbb5256`) was split. All clauses below describe this base-98 package only.

role: CRITERION
target_id: lychrel-new-base-proof
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
confirmed_scope: Mechanical template-closure proof that Lychrel numbers exist in new base b = 98 = 2 * 7^2 (object/lychrel_base98_certificate.json, sha256 6ec98e276bfb691187e5ebdb4c8ccf0c149f2754e201e362c15a4a681dbb5256, Period-4 templates T_1(m)..T_4(m) with |L_0|=|R_0|=37, |M_0|=16, and 92-digit start integer n = T_1(1) plus 1-step pre-template seed n_seed), outside {2^k, 11, 17, 20, 26}, verified by block-by-block symbolic carry computation for all integer parameters m at least 1, symbolic mirrored-block non-palindromicity, brute force over m from 1 to 500, and 2,000-step orbit simulation (t = 0..2,000) with compiled regex matching to 1,092 digits in base 98.

## 1. Clause-by-Clause Audit Against Verbatim Success Criterion and Verification Method

We audited `object/lychrel_base98_certificate.json` using both an independent verification script and `verify-it-yourself/check_lychrel.py`.

### Clause (1): Explicit Start $n$ and Templates $T_1..T_k$
- **Requirement:** A start $n$ and templates $T_1..T_k$ (digit strings with integer-parameter repeated blocks).
- **Evidence Verified:**
  - In base $b = 98$ (`object/lychrel_base98_certificate.json`, `38,310` bytes, `sha256: 6ec98e276bfb691187e5ebdb4c8ccf0c149f2754e201e362c15a4a681dbb5256`), the certificate gives four explicit Period-4 templates $T_1(m), T_2(m), T_3(m), T_4(m)$ parameterized by integer $m \ge 1$:
    - $T_1(m) = L_0 \; 97^m \; M_0 \; 0^m \; R_0$ (length $2m + 90$),
    - $T_2(m) = L_1 \; 0^m \; M_1 \; 97^m \; R_1$ (length $2m + 90$),
    - $T_3(m) = L_0 \; 97^m \; M_2 \; 0^m \; R_0$ (length $2m + 91$),
    - $T_4(m) = L_1 \; 0^m \; M_3 \; 97^m \; R_1$ (length $2m + 91$),
    with $|L_0| = |R_0| = |L_1| = |R_1| = 37$, $|M_0| = |M_1| = 16$, and $|M_2| = |M_3| = 17$.
  - The explicit 92-digit base-98 start integer $n = T_1(1)$ (`start_n_T1_m1_digits`, exact 182-digit base-10 value `31335679324046594453776682353725783129961246758320899429909828808998949313231333927252564930267639166175598329103881796087355725399307991459403160947318793915188975471307402693159161` in `object/lychrel_base98_certificate.json`) enters $T_1(1)$ at step $0$.
  - In addition, the certificate provides an explicit 92-digit pre-template seed $n_{\text{seed}}$ (`pre_template_seed_digits`, exact base-10 value `47242115529155230011031643852291858789712425704573002708512482823484856616054515931689179686881144589191045730774851573939706336640609991356312538325336911851134605592601598598949112`) that lies strictly outside $\{T_1(m), T_2(m), T_3(m), T_4(m)\}$ at step $0$ and maps in $1$ reverse-and-add step to $F_{98}(n_{\text{seed}}) = T_2(1)$.
  - The verifier also reproduces David Seal's 1996 Period-4 baseline in $b = 26$ ($|L_0| = 8$, $|M_0| = 4$, $|T_1(1)| = 22$).
- **Status:** Fully satisfied.

### Clause (2): All-Parameter Proof of Closure Under Reverse-and-Add
- **Requirement:** A proof of closure under reverse-and-add for ALL parameter values reduced to a finite mechanical check: an explicit symbolic carry computation in which every parameter-dependent block is shown to produce a constant digit/carry run, together with brute force over all parameters below the threshold (and up to $\max(\text{threshold}, 200)$ per `verification_method`).
- **Evidence Verified:**
  - **No hidden quantifiers or parity splits:** Because $|L_0| = |R_0| = |L_1| = |R_1| = \ell = 37$, the two symbolic repeated blocks $(b-1)^m = 97^m$ and $0^m$ sit at exact mirror offsets $[\ell, \ell+m)$ from the left and right ends of every template $T_i(m)$. When $T_i(m)$ is aligned with $\operatorname{Rev}_b(T_i(m))$, every position in both length-$m$ blocks pairs digit $b-1 = 97$ with digit $0$, summing to $b-1 = 97$.
  - **Uniform digit/carry run for all $m \ge 1$:** With incoming carry $c_{\text{in}} = 0$, $(b-1) + 0 + 0 = b-1$ emits digit $b-1$ and outgoing carry $c_{\text{out}} = 0 = c_{\text{in}}$ at every position; with incoming carry $c_{\text{in}} = 1$, $(b-1) + 0 + 1 = b$ emits digit $0$ and outgoing carry $c_{\text{out}} = 1 = c_{\text{in}}$ at every position.
  - **Mechanical RLE transducer check (`symbolic_rle_rev_add`):** Across all 4 transitions in base 98 (and the inline base-26 baseline), all 8 parameter-dependent symbolic blocks ($2$ per template $\times 4$ templates) satisfy $c_{\text{out}} = c_{\text{in}}$ and $a \cdot m_0 + c \ge 1$ at $m_0 = 1$, establishing $F_{98}(T_1(m)) = T_2(m)$, $F_{98}(T_2(m)) = T_3(m)$, $F_{98}(T_3(m)) = T_4(m)$, and $F_{98}(T_4(m)) = T_1(m+1)$ for all integers $m \ge 1$ with zero "by inspection" steps.
  - **Brute-force check:** All parameter values $1 \le m \le 500$ (strictly exceeding $\max(1, 200) = 200$) were verified in concrete digit-list arithmetic (and big-integer arithmetic for $1 \le m \le 50$) for bases $26$ and $98$.
- **Status:** Fully satisfied.

### Clause (3): Symbolic Non-Palindromicity Proof
- **Requirement:** A proof that no template string is a palindrome.
- **Evidence Verified:**
  - `check_symbolic_non_palindromicity` mechanically compares the normalized MSB-first and LSB-first symbolic block streams for every $T_i(m)$ ($i \in \{1, 2, 3, 4\}, m \ge 1$).
  - In base $b = 98$: $T_1(m)$ and $T_3(m)$ have first digit $L_0[0] = 1 \neq 95 = R_0[36]$ (and mirrored symbolic blocks $97^m \neq 0^m$ at offset $37$); $T_2(m)$ and $T_4(m)$ have first digit $L_1[0] = 97 \neq 96 = R_1[36]$ (and mirrored symbolic blocks $0^m \neq 97^m$ at offset $37$).
- **Status:** Fully satisfied.

### Clause (4): Orbit Entry and Concrete Simulation with Regex Matching
- **Requirement:** A demonstration that $n$'s orbit enters the template set, plus concrete orbit simulation matching each step to one of $T_1..T_k$ via a regular expression (`verification_method`).
- **Evidence Verified:**
  - $n = T_1(1)$ is in the template set at step $0$, and $n_{\text{seed}}$ enters $T_2(1)$ at step $1$.
  - `simulate_orbit_1e5_with_regex` in `verify-it-yourself/check_lychrel.py` simulates $2,000$ exact base-98 reverse-and-add steps (`t = 0 .. 2,000`) starting from $n = T_1(1)$ (reaching $1,092$ base-98 digits at step $2,000$) and matches every single iterate against compiled regular expressions (`re.Pattern.fullmatch`) for $T_1(m), T_2(m), T_3(m), T_4(m)$, confirming exact run lengths and distinct endpoint digits at every step.
- **Status:** Fully satisfied.

### Clause (5): Base Eligibility, Wikipedia Check, and Complete Novelty Audit
- **Requirement:** Base $b \notin \{2^k, 11, 17, 20, 26\}$ and not listed as proven on `https://en.wikipedia.org/wiki/Lychrel_number` at verification time, plus a novelty search (Wikipedia references, OEIS, arXiv, the 2023 construction paper if obtainable).
- **Evidence Verified:**
  - $98 = 2 \cdot 7^2$ is neither a power of $2$ nor in $\{11, 17, 20, 26\}$.
  - `https://en.wikipedia.org/wiki/Lychrel_number` (`206,959` bytes, `sha256: 2e5338385838c5abe91d01fb0fb68ae77ada436ef0ea765a340629d14bd6ab05`, recorded in `the-record-we-beat/README.md`) states verbatim in Section "Other bases": *"Lychrel numbers have been proven to exist in the following bases: 11, 17, 20, 26, and all powers of 2."*
  - Rostand S. Kuitché's 2023 preprint *"On the Construction of Some Lychrel Numbers"* (DOI `10.21203/rs.3.rs-2659802/v1`) gives an explicit template cycle only in base $b = 4$ (a power of $2$) and proves zero new bases outside $\{2^k, 11, 17, 20, 26\}$ (and never considers base 98).
- **Status:** Fully satisfied.

## 2. Null Model and Perturbation Controls
- **Perturbation control 1 (corrupted middle block):** Incrementing a single middle digit of $M_0$ in $T_1(m)$ (`bad_blocks[len(bad_blocks)//2]["digit"] += 1`) causes `symbolic_rle_rev_add` to fail closure against $T_2(m)$ immediately.
- **Perturbation control 2 (broken carry wire):** Changing the repeated digit from $97$ to $96$ so $d_1 + d_2 = 96 \neq b - 1$ causes `symbolic_rle_rev_add` to raise `ValueError` immediately due to non-uniform carry ($c_{\text{out}} \neq c_{\text{in}}$).
- **Null-model control:** Testing $400$ seeded random 92-digit integers in base $98$ (`random.Random(20261019)`) yields $0 / 400$ entries into the template family.

pass: true
