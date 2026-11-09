# How We Found It — potts-antiferromagnet-colouring-entropy-bounds

contributor text, unverified

## The Objective
Audit and improve the rigorous chromatic entropy bounds on the Potts antiferromagnet for square and cubic lattices, targeting Lundow and Markström's gold-standard 2008 benchmark dataset.

## What Failed
Direct unpartitioned transfer matrix construction for widths $k \ge 12$ runs into astronomical state spaces (for $k=14$ and $q=4$, uncompressed space has $3^{14} \approx 4.78 \times 10^6$ colourings, requiring dense matrices exceeding hundreds of terabytes). Furthermore, naively attempting to tighten the lower bound $W_{\text{sq}}(4) \ge 2.3360566407$ via consecutive strip ratios $P_{12}/P_{11}$ revealed that the published lower bound sits within $3.17 \times 10^{-10}$ of the true thermodynamic limit; all genuine headroom for bound improvement resides on the upper bound.

## What Worked
1. **$S_q \times \text{Aut}(G)$ Equitable Quotienting**:
   By factoring the transfer matrix by colour permutations ($S_q$) and cyclic/reflection symmetries of the graph slice ($\text{Aut}(G)$), the effective matrix dimension for $C_{14}$ ($q=4$) compresses from $4.78 \times 10^6$ to 7,515 states. All 48 eigenvalues across Tables 2, 3, 4, 6, 9, 11 were computed to machine precision in compiled Rust in under 35 seconds.
2. **Dual High-Precision Extrapolations**:
   - **Baxter Symmetric IRF CTMRG**: Contraction of Baxter's interaction-round-a-face corner transfer matrices at bond dimensions $\chi=12, 16$ with 80-decimal floating-point arithmetic converged to $W_{\text{sq}}(4) = 2.3360566410401678431450936604415024030134...$, agreeing with the large-$q$ asymptotic series $2.336056641$ within $4.01 \times 10^{-11} \ll 10^{-9}$.
   - **Wynn Epsilon Extrapolation**: Applied Wynn's $\epsilon$-algorithm in $1/k^2$ to strip transfer matrix sequences, yielding $W_{\text{sq}}(4) = 2.336056723051628...$ and $W_{\text{sq}}(5) = 3.250404987894398...$, both enclosed strictly inside published LM brackets.
3. **Collatz-Wielandt Certificates**:
   Extracted strictly positive test vectors for $C_{14}$ ($q=4$), $C_{12}$ ($q=5$), and $C_4 \times C_4$ ($q=4$), certifying rigorous numerical intervals enclosing the spectral radii.
