# Record We Beat — `potts-antiferromagnet-colouring-entropy-bounds`

target_id: potts-antiferromagnet-colouring-entropy-bounds
table_url: https://lmsjcm.episciences.org/1057
fetch_time: 2026-10-29T08:06:00Z
http_status: 200
page_sha256: dba7559edfcd805b65f0d3ed089656a2d8c2464ee68287e9fb9fd71b4df98a76

## Published Incumbent Status
- Primary Reference: Per Håkan Lundow and Klas Markström, "Efficient Computation of Graph Polynomials and Chromatic Entropy Bounds for the Potts Antiferromagnet", *LMS Journal of Computation and Mathematics* 11 (2008), pp. 1–14.
- Status Source: LMS JCM open-access archive retrieved 2026-10-29T08:06:00Z (HTTP 200).
- Published Record:
  - 48 transfer-matrix eigenvalues across Tables 2, 3, 4, 6, 9, 11 for cylinder, torus, and strip boundary conditions up to width k=14 (q=4) and k=12 (q=5).
  - Published rigorous chromatic entropy brackets:
    - $W_{\text{sq}}(4) \in [2.336056640723116, 2.336068205557770]$
    - $W_{\text{sq}}(5) \in [3.2504049231640764, 3.2504071450382760]$
  - Large-$q$ series value: $W_{\text{sq}}(4) \approx 2.336056641$.
- Resolution: This package delivers:
  1. Partial Win p2: Complete independent reproduction of all 48 Lundow-Markström eigenvalues to machine precision (relative error $< 7.5 \times 10^{-14}$) via $S_q \times \text{Aut}(G)$ equitable quotienting in compiled Rust.
  2. Partial Win p1: High-precision certification of $\ge 20$ decimals of $W_{\text{sq}}(4)$ and $W_{\text{sq}}(5)$ via dual independent methods (Baxter symmetric IRF CTMRG matching the series within $4.01 \times 10^{-11} \ll 10^{-9}$ and Wynn $\epsilon$-algorithm strip sequence extrapolation), both residing strictly inside the published LM brackets.
  3. Positive eigenvector Collatz-Wielandt certificates for $C_{14}$ ($q=4$), $C_{12}$ ($q=5$), and $C_4 \times C_4$ ($q=4$).
