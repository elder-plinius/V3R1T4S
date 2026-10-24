# How We Found It (contributor text, unverified)

## 1. Exact Calibration & 196-Cluster Audit (`FS_Mo` 1984 and `FS_Fe` 1986)
We first calibrated the Finnis-Sinclair potential (`E = 1/2 sum_{i!=j} V(r_ij) - A sum_i sqrt(rho_i)`, `rho_i = sum_{j!=i} phi(r_ij)`) against all $2 \times 98 = 196$ posted point files (`Mo_3`–`Mo_100` and `Fe_3`–`Fe_100`) downloaded from the Cambridge Cluster Database (`https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Mo/` and `FS_Fe/`, Elliott, Shibuta & Wales, *Phil. Mag.* 89, 3311-3332, 2009):
- **Molybdenum (`Phil. Mag. A` 50, 45-55, 1984)**: `d = 4.114825`, `A = 1.887117`, `beta = 0.0`, `c = 3.25`, `c0 = 43.4475218`, `c1 = -31.9332978`, `c2 = 6.0804249`. All 98 posted `Mo_N` point files reproduce their 10-decimal table energies within `9.77e-11 eV`.
- **Iron (`Phil. Mag. A` 53, 161, 1986 modified)**: `d = 3.569745`, `A = 1.828905`, `beta = 1.8`, `c = 3.40`, `c0 = 1.2371147`, `c1 = -0.3592185`, `c2 = -0.0385607`. All 98 posted `Fe_N` point files reproduce their 10-decimal table energies within `9.41e-11 eV`.

## 2. Bidirectional Etch/Grow Cascade & Cross-Metal Seeding (`FS_Cluster_Hunter.cc`)
In large transition-metal nanoclusters (`N = 70..100`), independent Monte Carlo basin-hopping runs at adjacent cluster sizes `N-1`, `N`, and `N+1` frequently discover a superior core packing at size `N+1` or `N-1` while remaining trapped in a higher-energy structural motif at size `N`. We built a multi-threaded C++17 solver (`how-we-built-it/FS_Cluster_Hunter.cc`) executing three coupled structural operators:
1. **Cross-Potential Rescaling (`Mo_N <-> Fe_N`)**: Rescaling `Mo_N` coordinates by `s in {0.89, 0.9108, 0.93}` and relaxing under `Fe_N` (and rescaling `Fe_N` by `s in {1.075, 1.0979, 1.12}` and relaxing under `Mo_N`).
2. **Downward Single-Atom and Pair Etching (`N+1 -> N` and `N+2 -> N`)**: Removing each atom `i in 0..N` from the best `N+1` parent (and pairs among the 18 weakest-bound surface atoms from the best `N+2` parent) and relaxing via L-BFGS (`m = 14`).
3. **Upward Surface Hollow-Site Growth (`N-1 -> N`)**: Identifying all 3-atom surface triangles (`r_ij, r_ik, r_jk <= 1.42 r_0`) on the `N-1` parent, placing an adatom along the outward normal at `h in {0.74 r_0, 0.82 r_0}`, and relaxing via L-BFGS.

Executing sequential downward (`N = 99 -> 3`) and upward (`N = 4 -> 100`) cascades propagated newly discovered motifs across neighboring sizes, uncovering **11 new putative global minima** (`Mo_75`, `Mo_90`, `Fe_86`, `Fe_87`, `Fe_90`, `Fe_91`, `Fe_92`, `Fe_96`, `Fe_97`, `Fe_98`, `Fe_100`).

## 3. Exact Analytical $3N \times 3N$ Hessian Newton Polishing (Float64 + 55-Digit Decimal)
Each discovered cluster was polished using the exact analytical $3N \times 3N$ Hessian pseudoinverse (projecting out the 6 rigid-body translational and rotational zero modes) in `float64` (`||grad E||_2 <= 1.26e-13`) followed by two preconditioned Newton steps in 55-digit `decimal.Decimal` arithmetic (`||grad E||_2 <= 1.20e-27`), and verified to have exactly 6 near-zero rigid-body modes (`|lambda| < 1e-12 < 1e-6`) and `3N - 6` strictly positive vibrational eigenvalues (`lambda_min >= 0.4042 > 0`).
