# Skeptic Panel Report — Role: CRITERION

> **Dated Note (2026-10-29):** This panel report originally reviewed the earlier three-base + audit version under `claim/`, which has since been split into **#517** (this package: base 50, where `claim/lychrel_base50_certificate.json` is now at `object/lychrel_base50_certificate.json` with identical `sha256: dd093b972a4f7eb7d6d9db4c5809a3332e413868719635bb6d2fdc9e59dacdb2`), **#723** (base 98), **#724** (base 146), and **#725** (Kuitché 2023 audit). The other `claim/` files (`CLAIM.md`, `REPRODUCE.md`, `lychrel_base98_certificate.json`, `lychrel_base146_certificate.json`, `seal_base26_baseline_certificate.json`, `kuitche_2023_audit.json`) and copied third-party pages/PDFs (`Lychrel_number.html`, `dseal_live.htm`, `rs_2659802.pdf`) named below are no longer included in this directory.

role: CRITERION
target_id: lychrel-new-base-proof
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
confirmed_scope: Mechanical template-closure proof that Lychrel numbers exist in new base b = 50 = 2*5^2 (object/lychrel_base50_certificate.json, sha256 dd093b972a4f7eb7d6d9db4c5809a3332e413868719635bb6d2fdc9e59dacdb2, Period-4 templates T_1(m)..T_4(m) with |L_0|=|R_0|=36, |M_0|=8, and 82-digit start integer n = T_1(1) plus 1-step pre-template seed n_seed), outside {2^k, 11, 17, 20, 26}, verified by block-by-block symbolic carry computation for all integer parameters m at least 1, symbolic mirrored-block non-palindromicity, brute force over m from 1 to 500, and 100,000-step orbit simulation with compiled regex matching to 50,082 digits in base 50.

## 1. Clause-by-Clause Audit Against Verbatim Success Criterion and Verification Method

We audited `object/lychrel_base50_certificate.json` (originally at `claim/lychrel_base50_certificate.json` in the combined three-base run alongside the companion files now split into #723, #724, and #725) using both an independent verification script and `verify-it-yourself/check_lychrel.py` (`how-we-built-it/author_checker_lychrel_check.py`).

### Clause (1): Explicit Start $n$ and Templates $T_1..T_k$
- **Requirement:** A start $n$ and templates $T_1..T_k$ (digit strings with integer-parameter repeated blocks).
- **Evidence Verified:**
  - In base $b = 50$ (`object/lychrel_base50_certificate.json`, `34,276` bytes, `sha256: dd093b972a4f7eb7d6d9db4c5809a3332e413868719635bb6d2fdc9e59dacdb2`), the certificate gives four explicit Period-4 templates $T_1(m), T_2(m), T_3(m), T_4(m)$ parameterized by integer $m \ge 1$:
    - $T_1(m) = L_0 \; 49^m \; M_0 \; 0^m \; R_0$ (length $2m + 80$),
    - $T_2(m) = L_1 \; 0^m \; M_1 \; 49^m \; R_1$ (length $2m + 80$),
    - $T_3(m) = L_0 \; 49^m \; M_2 \; 0^m \; R_0$ (length $2m + 81$),
    - $T_4(m) = L_1 \; 0^m \; M_3 \; 49^m \; R_1$ (length $2m + 81$),
    with $|L_0| = |R_0| = |L_1| = |R_1| = 36$, $|M_0| = |M_1| = 8$, and $|M_2| = |M_3| = 9$.
  - The explicit 82-digit base-50 start integer $n = T_1(1)$ (`start_n_T1_m1_digits`, exact 140-digit base-10 value `803319634591911080790138327923868078346985580436311600817766986472726093862002163822300704837735070450470992436928311975462193309396720297` in `object/lychrel_base50_certificate.json`) enters $T_1(1)$ at step $0$.
  - In addition, the certificate provides an explicit 82-digit pre-template seed $n_{\text{seed}}$ (`pre_template_seed_digits`, exact base-10 value `1216909940868424918225842673958849505129891635886751053942766986472726093862002163822300704837735070450470992436928311975462193309396720296`) that lies strictly outside $\{T_1(m), T_2(m), T_3(m), T_4(m)\}$ at step $0$ and maps in $1$ reverse-and-add step to $F_{50}(n_{\text{seed}}) = T_2(1)$.
  - The verifier also reproduces David Seal's 1996 Period-4 baseline in $b = 26$ ($|L_0| = 8$, $|M_0| = 4$, $|T_1(1)| = 22$). (Companion Period-4 certificates for $b = 98$ and $b = 146$ from the initial run are in #723 and #724.)
- **Status:** Fully satisfied.

### Clause (2): All-Parameter Proof of Closure Under Reverse-and-Add
- **Requirement:** A proof of closure under reverse-and-add for ALL parameter values reduced to a finite mechanical check: an explicit symbolic carry computation in which every parameter-dependent block is shown to produce a constant digit/carry run, together with brute force over all parameters below the threshold (and up to $\max(\text{threshold}, 200)$ per `verification_method`).
- **Evidence Verified:**
  - **No hidden quantifiers or parity splits:** Because $|L_0| = |R_0| = |L_1| = |R_1| = \ell$, the two symbolic repeated blocks $(b-1)^m$ and $0^m$ sit at exact mirror offsets $[\ell, \ell+m)$ from the left and right ends of every template $T_i(m)$. When $T_i(m)$ is aligned with $\operatorname{Rev}_b(T_i(m))$, every position in both length-$m$ blocks pairs digit $b-1$ with digit $0$, summing to $b-1$.
  - **Uniform digit/carry run for all $m \ge 1$:** With incoming carry $c_{\text{in}} = 0$, $(b-1) + 0 + 0 = b-1$ emits digit $b-1$ and outgoing carry $c_{\text{out}} = 0 = c_{\text{in}}$ at every position; with incoming carry $c_{\text{in}} = 1$, $(b-1) + 0 + 1 = b$ emits digit $0$ and outgoing carry $c_{\text{out}} = 1 = c_{\text{in}}$ at every position.
  - **Mechanical RLE transducer check (`symbolic_rle_rev_add`):** Across all 4 transitions in base 50 (and the inline base-26 baseline), all 8 parameter-dependent symbolic blocks ($2$ per template $\times 4$ templates) satisfy $c_{\text{out}} = c_{\text{in}}$ and $a \cdot m_0 + c \ge 1$ at $m_0 = 1$, establishing $F_b(T_1(m)) = T_2(m)$, $F_b(T_2(m)) = T_3(m)$, $F_b(T_3(m)) = T_4(m)$, and $F_b(T_4(m)) = T_1(m+1)$ for all integers $m \ge 1$ with zero "by inspection" steps.
  - **Brute-force check:** All parameter values $1 \le m \le 500$ (strictly exceeding $\max(1, 200) = 200$) were verified in concrete digit-list arithmetic (and big-integer arithmetic for $1 \le m \le 50$) for bases $26$ and $50$.
- **Status:** Fully satisfied.

### Clause (3): Symbolic Non-Palindromicity Proof
- **Requirement:** A proof that no template string is a palindrome.
- **Evidence Verified:**
  - `check_symbolic_non_palindromicity` mechanically compares the normalized MSB-first and LSB-first symbolic block streams for every $T_i(m)$ ($i \in \{1, 2, 3, 4\}, m \ge 1$).
  - In base $b = 50$: $T_1(m)$ and $T_3(m)$ have first digit $L_0[0] = 1 \neq 47 = R_0[35]$ (and mirrored symbolic blocks $49^m \neq 0^m$ at offset $36$); $T_2(m)$ and $T_4(m)$ have first digit $L_1[0] = 49 \neq 48 = R_1[35]$ (and mirrored symbolic blocks $0^m \neq 49^m$ at offset $36$).
- **Status:** Fully satisfied.

### Clause (4): Orbit Entry and 100,000-Step Simulation with Regex Matching
- **Requirement:** A demonstration that $n$'s orbit enters the template set, plus simulation of the orbit of $n$ for $10^5$ steps matching each step to one of $T_1..T_k$ via a regular expression (`verification_method`).
- **Evidence Verified:**
  - $n = T_1(1)$ is in the template set at step $0$, and $n_{\text{seed}}$ enters $T_2(1)$ at step $1$.
  - `simulate_orbit_1e5_with_regex` simulates $100,000$ exact base-50 reverse-and-add steps (`t = 0 .. 100,000`) starting from $n = T_1(1)$ (reaching $50,082$ base-50 digits at step $100,000$ in `15.77s`) and matches every single iterate against compiled regular expressions (`re.Pattern.fullmatch`) for $T_1(m), T_2(m), T_3(m), T_4(m)$, confirming exact run lengths $r_1 = r_2 = 1 + \lfloor t/4 \rfloor + \mathbf{1}_{t \bmod 4 \in \{0, 2\}}$ and distinct endpoint digits at every step.
- **Status:** Fully satisfied.

### Clause (5): Base Eligibility, Wikipedia Check, and Complete Novelty Audit (Including Kuitché 2023)
- **Requirement:** Base $b \notin \{2^k, 11, 17, 20, 26\}$ and not listed as proven on `https://en.wikipedia.org/wiki/Lychrel_number` at verification time, plus a novelty search (Wikipedia references, OEIS, arXiv, the 2023 construction paper if obtainable).
- **Evidence Verified:**
  - $50 = 2 \cdot 5^2$ is neither a power of $2$ nor in $\{11, 17, 20, 26\}$.
  - `https://en.wikipedia.org/wiki/Lychrel_number` (`206,959` bytes, `sha256: 2e5338385838c5abe91d01fb0fb68ae77ada436ef0ea765a340629d14bd6ab05`, recorded in `the-record-we-beat/README.md`) states verbatim in Section "Other bases": *"Lychrel numbers have been proven to exist in the following bases: 11, 17, 20, 26, and all powers of 2."*
  - Rostand S. Kuitché's 2023 preprint *"On the Construction of Some Lychrel Numbers"* (DOI `10.21203/rs.3.rs-2659802/v1`, `648,343` bytes, `sha256: c5130873a5d82c3577ac52d7a9a1ec94a7dce1017d9ce2dededa13a87f64dac7`) was obtained and mechanically audited across all bases $3 \le b \le 10$ (packaged separately in #725; copied PDF and HTML files are omitted from this directory). Kuitché (2023) gives an explicit template cycle only in base $b = 4$ (a power of $2$) and proves zero new bases outside $\{2^k, 11, 17, 20, 26\}$.
- **Status:** Fully satisfied.

## 2. Null Model and Perturbation Controls
- **Perturbation control 1 (corrupted middle block):** Incrementing a single middle digit of $M_0$ in $T_1(m)$ (`bad_blocks[len(bad_blocks)//2]["digit"] += 1`) causes `symbolic_rle_rev_add` to fail closure against $T_2(m)$ immediately.
- **Perturbation control 2 (broken carry wire):** Changing the repeated digit from $49$ to $48$ so $d_1 + d_2 = 48 \neq b - 1$ causes `symbolic_rle_rev_add` to raise `ValueError` immediately due to non-uniform carry ($c_{\text{out}} \neq c_{\text{in}}$).
- **Null-model control:** Testing $400$ seeded random 82-digit integers in base $50$ (`random.Random(20261019)`) yields $0 / 400$ entries into the template family.

pass: true
