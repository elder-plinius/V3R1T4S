# How We Found the 20 Polytetrahedral Cluster Global Minima & 502-Cluster CCD Audit

*(contributor text, unverified)*

## 1. Exact Calibration and `p2` Forensic Audit of the 502 Posted CCD Point Files

Before launching any structural search, we ingested all 502 coordinate files and energy tables from the four live Cambridge Cluster Database (CCD) polytetrahedral cluster pages:
- **Dzugutov (`N = 3..100`, 98 clusters)**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/Dzugutov.html` (`dzugutov.tar.gz`)
- **Modified-Dzugutov (`N = 3..250`, 248 clusters)**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/mDzugutov.html` (`mdzugutov.tar.gz`)
- **Zetterling-Dzugutov `Z1` and `Z2` (`N = 3..80`, 78 clusters each)**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/Zetterling.html` (`Z1.tar.gz`, `Z2.tar.gz`)

During calibration to the required $10^{-6}$ energy accuracy, we uncovered two critical archival defects (`p2`):
1. **The 10x Repulsive Parameter Typo in Table I of Doye et al. (2003) for `Z2`**:
   In J. P. K. Doye, D. J. Wales, F. H. M. Zetterling & M. Dzugutov, *J. Chem. Phys.* **118**, 2792–2799 (2003), Table I lists the repulsive core prefactor for `Z2` as $b = 4.2 \times 10^7$ alongside $V_0 = 0.13391543$ and $r_{\text{cutoff}} = 2.64488$. However, evaluating the bare potential $V_{\text{bare}}(r) = a r^{-3} e^{\alpha r} \cos(2 k_F r) + b(\sigma/r)^n$ at the third minimum $r_c = 2.644877841213031$ with $b = 4.2 \times 10^7$ gives $-V_{\text{bare}}(r_c) = 0.1335224$ and causes every single `Z2` coordinate file on the CCD to disagree with the published table by tens of energy units. Replacing $b = 4.2 \times 10^7$ with $b = 4.2 \times 10^6$ reproduces the exact printed shift $V_0 = 0.133915425377427$ to all 8 published digits and reproduces all 78 `Z2` cluster energies within `4.828e-7 < 1e-6`.
2. **Five Corrupted Central-Atom Origin Coordinates in `Z1.tar.gz` and `Z2.tar.gz`**:
   In `Z1_13`, `Z1_25`, `Z1_33`, `Z1_37`, and `Z2_25`, the raw CCD energy misses the posted table by $+7.06$ to $+7.74$ reduced units because a single coordinate of the central atom near $(0,0,0)$ had its `0.000000` decimal prefix stripped during archival formatting (leaving `-1466`, `0197`, `-2335`, `6593`, and `-1168`, which place that atom hundreds of bond lengths outside the cluster). Multiplying those five tokens by $10^{-10}$ restores all five energies to within `< 5e-7` of the CCD table.

## 2. Physics of Polytetrahedral Networks & Why Bidisperse/Anisotropic Etch-Cap Cascades Beat Unbiased Basin-Hopping

Unlike Morse or Gupta metal clusters — which pack into compact, convex icosahedra, decahedra, or FCC polyhedra — Dzugutov, modified-Dzugutov, and Zetterling-Dzugutov (`Z1`, `Z2`) potentials possess a prominent Friedel/cage barrier at $r \approx 1.35\text{–}1.65\,\sigma$ that strongly penalizes the $\sqrt{2}\,r_{\text{eq}}$ diagonal of octahedral interstitial sites. Consequently, low-energy clusters form non-convex **polytetrahedral networks**: interpenetrating 13-atom icosahedra, Frank-Kasper Z12/Z14/Z15/Z16 coordination polyhedra, and branched Bernall spirals (tetrahedral chains and rings).

Standard single-size Monte Carlo basin-hopping frequently stalls on these potentials because adding or moving an atom at random almost always creates a high-energy five-fold defect or an octahedral contact across the barrier. We built a dedicated C++17 solver (`how-we-built-it/Dzugutov_Cluster_Hunter.cc`) combining four targeted structural operators:
1. **Cross-Potential Structural Seeding**: Rescaling every posted configuration across `Dzugutov`, `mDzugutov`, `Z1`, and `Z2` to each target potential's equilibrium bond length $r_{\text{eq}}$ (`1.130`, `1.153`, `1.078`, `1.133`) with $\pm 4\%$ radial breathing factors (`0.96, 1.00, 1.04`). This immediately uncovered `Z1_38` (`-100.130184` vs `-99.874893`, `-0.255291`), `Z1_42` (`-111.173977` vs `-111.113917`, `-0.060060`), and `Z1_44` (`-116.872716` vs `-116.579062`, `-0.293654`) from `Z2`'s superior linked-icosahedral topologies.
2. **Downward Peripheral Etching ($N+1 \to N$ and $N+2 \to N$)**: Exhaustively removing 1 atom (or pairs of weakest-bound peripheral atoms) from $(N+1)$ and $(N+2)$ networks and relaxing via a two-stage L-BFGS tournament. This uncovered 11 new global minima, including `mDzugutov_74` (`-0.004790`), `mDzugutov_134` (`-0.003973`, `p1`), `mDzugutov_177` (`-0.003079`, `p1`), `Z1_54`, `Z1_65`, `Z1_67`, `Z1_68`, `Z2_35`, `Z2_43` (`-0.411479`), and `Z2_56` (`-0.293810`).
3. **Two-Sided Upward Regular-Tetrahedral Capping ($N-1 \to N$)**: Enumerating all triangular surface facets $(i, j, k)$ with edges $< 1.36\,r_{\text{eq}}$ and placing a capping atom at regular-tetrahedron altitude $\pm\sqrt{2/3}\,r_{\text{eq}} \approx \pm 0.8165\,r_{\text{eq}}$ along **both** normal directions $\pm\hat{n}$ (essential because polytetrahedral chains and rings are non-convex). This uncovered `mDzugutov_241` (`-641.794163` vs `-641.793084`, `-0.001079`, `p1`), `Z1_74` (`-0.319315`), `Z1_75` (`-0.358156`), `Z1_76` (`-0.243444`), and `Z2_59` (`-0.009157`).
4. **Same-$N$ 1-Atom Peripheral-to-Tetrahedral-Cap Relocation**: Detaching each of the 6 weakest-bound peripheral atoms and relocating it to the lowest-energy regular-tetrahedral cap site on the $(N-1)$-atom core. This uncovered `Z2_69` (`-184.626708` vs `-184.286813`, `-0.339895`) and `Z2_80` (`-214.192847` vs `-213.815040`, `-0.377807`).

## 3. High-Precision Newton-Raphson Polishing & Hessian Certification

Every candidate winner was polished using exact analytical Hessians in float64 followed by 55-digit `decimal.Decimal` Newton-Raphson steps, driving all 20 configurations to:
- `float64` gradient norm $\|\nabla E\|_2 \le 6.76 \times 10^{-13} < 10^{-10}$,
- 55-digit `Decimal` gradient norm $\|\nabla E\|_2 \le 1.45 \times 10^{-33} < 10^{-10}$ (on 36-decimal-place coordinates),
- Exact $3N \times 3N$ analytical Hessian having 6 rigid-body modes with $|\lambda| < 10^{-6}$ and $3N - 6$ strictly positive vibrational eigenvalues ($\lambda_7 \ge 0.2423$).
