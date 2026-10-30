# PREREG: ecc-inversion-addition-chains & gf2-polymult-8term-25-products

- **Frozen timestamp (UTC)**: 2026-10-29T15:10:00Z
- **Target ID**: ecc-inversion-addition-chains

## Criterion Verbatim
Success means an explicit addition chain 1 = a_0, a_1, ..., a_L = E, where E is one of the eight exponents N - d listed in addchain's doc/results.md for Curve25519, P-256, P-384 and secp256k1 field and scalar inversion (d=3 for the P-256, P-384 and secp256k1 field entries; d=2 for the Curve25519 field entry and all four scalar entries), in which every a_i (i >= 1) equals a_j + a_k for some j, k < i (j = k is a doubling), checked with exact integer arithmetic, and whose length L is STRICTLY LESS (direction: min) than the best of: Brian Smith's live page, addchain's live doc/results.md, and any shorter chain for the same exponent published elsewhere (papers or library source such as BoringSSL, Go crypto, fiat-crypto, RustCrypto, curve25519-dalek, libsecp256k1 before its switch to safegcd), which the claimant must search for and cite. Bars on 2026-10-25: Curve25519 field 265, P-256 field 266, P-384 field 396, secp256k1 field 269, secp256k1 scalar 290, P-256 scalar 292, P-384 scalar 433, Curve25519 scalar 283. Include the best valid composition of published objects for the same parameters and metric in the bar, even if it is absent from a printed table. State whether the candidate is a composition. Identify its components and composition rule. Values in unmerged pull requests are not bars.

Partial wins verbatim:
- p1: For one of the twelve field-inversion exponents that addchain lists without a published best (M-221, E-222, Curve1174, E-382, M-383/Curve383187, Curve41417, M-511, P-192, P-224, Goldilocks, secp192k1, secp224k1), a verified chain strictly shorter than addchain's listed length and than any chain the claimant finds in papers or public source code for that exponent.
- p2: For one of the eight main exponents, a verified chain of the same total length as the live bar but with strictly fewer additions (multiplications), i.e. a cheaper inversion whenever a squaring costs less than a multiplication.

For `gf2-polymult-8term-25-products`:
- Success means an explicit bilinear algorithm over GF(2) for the product of two 8-term polynomials using at most 25 products, given as 0/1 matrices U (r x 8), V (r x 8) and W (15 x r), where r <= 25 (zero padding to 25 rows is allowed) such that, over GF(2), sum_t U[t][i] V[t][j] W[k][t] equals 1 if i + j = k and 0 otherwise, for all 0 <= i, j <= 7 and 0 <= k <= 14 (direction: min; best known 26).
- p1: A circuit of 2-input AND, XOR and XNOR gates (no other gates, no constants) for multiplication in GF(2^8) modulo the AES polynomial x^8 + x^4 + x^3 + x + 1, standard polynomial basis in and out, verified on all 65536 input pairs, with at most 116 gates.
- p2: The same kind of circuit for GF(2^7) modulo x^7 + x^4 + 1 with at most 83 gates, or modulo x^7 + x^3 + 1 with at most 84, or for GF(2^6) modulo x^6 + x^3 + 1 with at most 56, verified on all input pairs.

## Exact Statistic and Checker
1. **ECC Addition Chains**:
   - The statistic is the total chain length $L = D + A$, where $D$ is the count of doublings ($j = k$) and $A$ is the count of additions ($j \neq k$).
   - Validity check: $a_0 = 1$; for every $i \in [1, L]$, $a_i = a_{j_i} + a_{k_i}$ with $0 \le j_i \le k_i < i$; $a_L = E = N - d$.
   - Independent verification: Python exact big-integer arithmetic re-evaluating each step from indices, matching against target hex, and 100 Fermat test modular exponentiations $x^E \cdot x^d \equiv 1 \pmod N$ for nonzero random $x$.

2. **GF(2) Field Multipliers & Bilinear Tensors**:
   - The statistic is the total gate count $G = N_{\text{AND}} + N_{\text{XOR}} + N_{\text{XNOR}}$ in the standard polynomial basis.
   - Circuit validity check: only 2-input AND, XOR, XNOR gates allowed; no constants, no NOT gates; acyclic topological order.
   - Truth-table verification: exhaustive evaluation over all $2^{2k}$ input pairs ($2^{12} = 4,096$ for GF(2^6), $2^{14} = 16,384$ for GF(2^7), $2^{16} = 65,536$ for GF(2^8)) against reference polynomial product modulo $P(x)$.
   - Tensor Brent equations: $\bigoplus_{t=0}^{r-1} U_{t, i} V_{t, j} W_{k, t} = \delta_{i+j, k}$ across all 960 triplets $(i, j, k) \in [0..7] \times [0..7] \times [0..14]$.

## Thresholds
- **ECC Addition Chains**:
  - Secondary curve length $L < L_{\text{addchain}}$: satisfies **p1**.
  - Main curve addition count $A < A_{\text{live}}$ at $L = L_{\text{live}}$: satisfies **p2**.
  - Main curve length $L < L_{\text{live}}$: satisfies **CONFIRMED_SOLUTION**.
- **GF(2) Field Multipliers**:
  - GF(2^6) mod (x^6+x^3+1): $G \le 56$ gates: satisfies **p2**.
  - GF(2^7) mod (x^7+x^4+1): $G \le 83$ gates: satisfies **p2**.
  - GF(2^7) mod (x^7+x^3+1): $G \le 84$ gates: satisfies **p2**.
  - GF(2^8) AES field mod (x^8+x^4+x^3+x+1): $G \le 116$ gates: satisfies **p1**.
  - 8-term polynomial multiplication tensor: $r \le 25$ products: satisfies **CONFIRMED_SOLUTION**.

## Null Design
null_test: not needed because addition chain step validity (a_i = a_j + a_k), modular exponentiation, and GF(2) polynomial circuit truth tables are algebraic identities verified deterministically by exact integer and field arithmetic without statistical estimation.
