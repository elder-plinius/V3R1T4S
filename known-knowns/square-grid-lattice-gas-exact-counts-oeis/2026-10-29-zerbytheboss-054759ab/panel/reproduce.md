# Reproduce Skeptic Report — `square-grid-lattice-gas-exact-counts-oeis`

context: subagent (fresh invocation)
target_id: square-grid-lattice-gas-exact-counts-oeis
review_utc: 2026-10-29T16:15:00Z

## Reproduction Audit
1. **OEIS B-File SHA256 Verification**:
   - Re-verified all 7 live b-files from `https://oeis.org/...` against SHA256 checksums (`b054759.txt`, `b028420.txt`, `b006506.txt`, `b063443.txt`, `b027683.txt`, `b210662.txt`, `b089980.txt`). 100% exact match.
2. **Square Ice A054759 Reproduction & World Records**:
   - Re-executed `square_ice_flux` in exact BigUint arithmetic.
   - Terms $a(1) \dots a(14)$ match published values by Brendan McKay (2024) with zero errors.
   - World records $a(15)$ (43 digits) and $a(16)$ (49 digits) converge monotonically toward Lieb's constant $(4/3)^{1.5} \approx 1.5396007$ within $0.48\%$ and $0.42\%$, with finite-size scaling $N^2(\ln W_N - \ln W_{\text{Lieb}}) \to 1.077260$.
3. **Rectangular Table Row 28 Extensions**:
   - Re-computed Row 28 in `broken_profile_rectangular`:
     - $A089980(28, 1) = F_{30} = 832040$; $A089980(28, 2) = 63018038201$ (Pell); $A089980(28, 3) = 6291263130892379$.
     - $A210662(28, 1) = F_{29} = 514229$; $A210662(28, 2) = 104966044432531$; $A210662(28, 3) = 8953334529817405734759$.
4. **Monomer-Dimer Dual-Solver Parity on $N = 22$**:
   - Solver A (row-sweep) and Solver B (column-sweep) residues across 14 primes match with 100% parity.
   - Gauss CRT reconstructed 137-digit integer matches published $A028420(22)$ digit-for-digit.
   - Skeptic prime residue modulo $q = 4611686018427386911$ verified ($2747394045241524070 == 2747394045241524070$).

pass: true
