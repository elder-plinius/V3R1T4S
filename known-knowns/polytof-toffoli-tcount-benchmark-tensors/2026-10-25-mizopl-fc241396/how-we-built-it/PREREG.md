# Pre-Registration (`PREREG.md`) — `polytof-toffoli-tcount-benchmark-tensors`

- **Run ID:** `2026-10-25-1935`
- **Target ID:** `polytof-toffoli-tcount-benchmark-tensors`
- **Pre-Registered Prediction ID:** `P0082` (`p = 0.75`)
- **Timestamp (UTC):** `2026-10-25T18:35:00Z`
- null_test: required

## 1. Frozen Success Criteria

### Full Win (`CONFIRMED_SOLUTION`)
For one or more tensor IDs listed in the live `ZIB-IOL/polytof` table (`https://github.com/ZIB-IOL/polytof/blob/main/docs/tensors.md`, commit `0dcac107d15adc34dc646242d222f21ae7d32699`), construct an explicit decomposition over $\mathbb{F}_2$ with **strictly fewer terms** (margin $\ge 1$ term) than the listed `CP` value (Toffoli count) or the listed `Waring` value (T-count) for that exact tensor ID (`07xx`, `05xx`, `08xx`, or `01xx`), such that:
1. **Exact Tensor Reproduction:**
   - For a `CP` claim on a symmetric cubic phase tensor (`07xx`, `08xx`, `01xx`), the $r$ binary vector triples $(u_t, v_t, w_t) \in (\mathbb{F}_2^n)^3$ satisfy
     $$\text{upper\_triples}\!\left(\sum_{t=1}^r \text{Sym}(u_t \otimes v_t \otimes w_t) \bmod 2\right) = \text{upper\_triples}(T_{\text{ref}})$$
     on all strict cubic monomials $i < j < k$, verified both by an independent zero-dependency script (`verify.py`) and by `polytof`'s `scripts/verify_paper_schemes.py` convention (both in the BCO basis and mapped back to the original tensor `data/tensors/{id:04d}.npy` via the invertible $\mathrm{GL}(n, \mathbb{F}_2)$ basis change $A$).
   - For a `CP` claim on a bilinear tensor (`05xx`), $\sum_{t=1}^r u_t \otimes v_t \otimes w_t \equiv T_{\text{ref}} \pmod 2$ entrywise across all $k \times k \times k$ entries.
   - For a `Waring` claim (`07xx`, `08xx`, `01xx`), the $r$ parity vectors $a_t \in \mathbb{F}_2^n$ satisfy
     $$\text{upper\_triples}\!\left(\sum_{t=1}^r a_t \otimes a_t \otimes a_t \bmod 2\right) = \text{upper\_triples}(T_{\text{ref}})$$
     both in the BCO basis and in the original basis of `data/tensors/{id:04d}.npy`.
2. **Exact Circuit-Level Equivalence Check (Requirement (c)):**
   - For at least one claimed circuit ($n \le 30$ qubits), synthesize the explicit CNOT + Toffoli/CCZ (for CP) or CNOT + `{T, S, Z}` phase-polynomial circuit (for Waring, fixing quadratic and linear diagonal phase corrections so the full phase polynomial matches the original circuit's phase polynomial modulo $8$) and verify exact unitary / statevector / path-sum equivalence on all $2^n$ computational basis states (or exact symbolic phase-polynomial identity over $\mathbb{Z}_8[x_1, \dots, x_n]/(x_i^2 - x_i)$).
3. **Literature Non-Supersession (Requirement (d)):**
   - Confirm against `arXiv:2602.15285`, `arXiv:2610.01024`, AlphaTensor-Quantum (`arXiv:2402.14396`), and Vandaele (`arXiv:2405.00083` / `2502.xxxxx`) that the new count is strictly lower than any published count for that tensor variant.

### Partial Wins (`p1`, `p2`, `p3`)
- **`p1`:** Strictly lower Toffoli (`CP`) count than the live table for at least one $\mathrm{GF}(2^k)$ multiplication tensor (`07xx`/`05xx`, $k = 2..10$) or AES S-box circuit tensor, checked against both `docs/tensors.md` and the classical bilinear complexity literature if on `05xx`.
- **`p2`:** Certified optimality proof (exact SAT/UNSAT with DRAT proof or exhaustive algebraic certificate re-checkable in $< 1$ hour) that no decomposition with $(\text{table value} - 1)$ terms exists for a table row whose optimality is not already published.
- **`p3`:** Complete independent re-verification audit of all 88 decompositions in `data/paper/` reporting every table value in `docs/tensors.md` not reproduced by its posted decomposition.

## 2. Attack Lenses (CLSS + Law `M7`)

- **Lens 1 (`L-PTTF-001`, Law `M7` Fiber Diversity + Higher-Beam FastTODD & Flip-Graph Search):**
  - First, complete the exact 88-tensor audit (`p3`).
  - Second, apply **Law `M7`** (*Interface Gauge Freedom & Solution-Fiber Diversity*) to $\mathrm{GF}(2^k)$ multiplication (`0725..0733` / `0525..0533`) and circuit benchmarks (`0800..0824`, `0101..0168`):
    - Generate a diverse fiber of minimal-rank CP decompositions via $\mathrm{Aut}(\mathbb{F}_{2^k})$, tower basis changes, evaluation-point permutations, and FGS plateau flips (`--fgs --plus`).
    - Run `waring` (FastTODD) across the entire CP fiber and with elevated beam width (`-b 8..64`) + random column permutations to strictly beat the live `Waring` (T-count) and `CP` (Toffoli-count) records in `docs/tensors.md`.
- **Lens 2 (`L-PTTF-002`, Symmetric Phase-Tensor CP Reduction & Cenk–Özbudak / Chudnovsky Sub-30 `GF(2^9)` / `GF(2^7)` Construction + `p2` Optimality Certificates):**
  - Attack `CP` rank directly on `07xx` (`topp` symmetric cubic tensors, where cross-register terms and symmetric cancellations are permitted) and `05xx` (`GF(2^9)` rank $< 30$ via Cenk–Özbudak 2010 / Bshouty / FGS on `0532`/`0732` and `0726..0733`), plus certify exact optimality (`p2`) on small table rows.
