# How We Built It

## Architecture & Innovations
1. **Generating Function Polynomial Convolution**:
   Evaluating Luo's inclusion-exclusion formula $C(r, f)$ (arXiv:2609.25062 eq. A.1) naively requires summing over $3^n$ states. By observing that each label corresponds to a factor $(1 + f_i t)$ or $(1 + 2f_i t + f_i(f_i-1)t^2)$, we reduce the computation to discrete polynomial convolution of degree at most $2n$, evaluating in $O(n^2)$ time ($< 1\mu\text{s}$ per state).

2. **Integer Bellman Equivalence**:
   By defining $W(r, f) = C(r, f) V^+(r, f)$, the dynamic programming recursion becomes:
   $$W(s) = \max_i [ C(s_{\text{succ}, i}) + W(s_{\text{succ}, i}) + W(s_{\text{fail}, i}) ]$$
   This eliminates all floating-point roundoff, division errors, and intermediate rational reductions during the search.

3. **Dual Independent Lenses**:
   - **Lens 1 (Compiled Rust)**: 256-bit limb arithmetic, multiset bit-packing into `[u8; 16]`, layer-by-layer dynamic programming with multithread-ready cache locality.
   - **Lens 2 (Pure Python Standard Library)**: Arbitrary-precision integers, `fractions.Fraction`, in-memory memoization.
   Both implementations agree byte-for-byte across all checked parameters.
