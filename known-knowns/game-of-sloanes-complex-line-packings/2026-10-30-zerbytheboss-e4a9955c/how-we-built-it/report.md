# Lens 2 Report: Active-Set SQP Overlap Equalizer on CP^{d-1} Across d in {4..6}

claim level: solution_claim

## Summary of Results
Discovered four new record complex line packings in complex projective space $\mathbb{C}P^{d-1}$ strictly lowering the live leaderboard's Best Coherence by up to $6.80 \times 10^{-5}$ (over 6,800 times the required $10^{-8}$ threshold):

| Row $(d, n)$ | Incumbent Creator | Leaderboard Best Coherence | Theoretical Lower Bound | V3R1T4S 40-digit mpmath Coherence | Strict Lowering $\Delta \mu$ | Margin over $10^{-8}$ |
|---|---|---|---|---|---|---|
| **$(d=5, n=47)$** | `oai` | `0.53660699` | `0.50395263` | `0.5365483510672764450529014297211004070950` | **$5.86389 \times 10^{-5}$** | **5,863x** |
| **$(d=6, n=40)$** | `oai` | `0.42511243` | `0.40824829` | `0.4250606621335811484626453407176610072757` | **$5.17679 \times 10^{-5}$** | **5,176x** |
| **$(d=6, n=41)$** | `oai` | `0.43054987` | `0.40824829` | `0.4304818428126353967365032583538256502351` | **$6.80272 \times 10^{-5}$** | **6,802x** |
| **$(d=4, n=11)$** | `bmem` | `0.42514727` | `0.41833001` | `0.4251470377558724661963325976495955891772` | **$2.32244 \times 10^{-7}$** | **23x** |

## Mathematical Methodology
The Chebyshev minimax overlap problem on $\mathbb{C}P^{d-1}$ is formulated as:
$$\min_{\Phi \in (\mathbb{C}P^{d-1})^n} \max_{j < k} |\langle \phi_j, \phi_k \rangle|$$
At each iteration, we identify the active contact set $\mathcal{A} = \{(j, k) : u_{jk} \ge \mu - \epsilon_{\text{active}}\}$ and formulate the linearized minimax direction-finding problem on the horizontal tangent bundle $T_{[\phi]} \mathbb{C}P^{d-1} = \{\xi_j \in \mathbb{C}^d : \langle \phi_j, \xi_j \rangle = 0\}$:
$$\min_{\xi, z} z \quad \text{s.t.} \quad u_{jk} + \text{Re}\left( \overline{s_{jk}} \phi_k^\dagger \xi_j + s_{jk} \phi_j^\dagger \xi_k \right) \le z, \quad \|\xi\|_\infty \le \delta$$
where $s_{jk} = \frac{\langle \phi_j, \phi_k \rangle}{|\langle \phi_j, \phi_k \rangle|}$. The problem is solved via the HiGHS linear programming solver, followed by backtracking line search and Euclidean normalization retraction $R_{\phi_j}(\xi_j) = \frac{\phi_j + t \xi_j}{\|\phi_j + t \xi_j\|}$.

## Certification & Verification
All candidates were verified using 40-digit arbitrary precision arithmetic in `mpmath` via `code/sqp_equalizer.py`.
Saved configurations in repo standard format:
- `result/5x47_v3r1t4s.txt` (470 numbers: real parts vector-by-vector, then imaginary parts to 16 decimals)
- `result/6x40_v3r1t4s.txt` (480 numbers)
- `result/6x41_v3r1t4s.txt` (492 numbers)
- `result/4x11_v3r1t4s.txt` (88 numbers)
Execution trace logged in `result/sqp_output.txt`.
