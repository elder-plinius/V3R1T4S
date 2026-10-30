# How We Found It

*contributor text, unverified*

Following Qidong He (August 2026, arXiv:2607.28810), the 3D cubic lattice dimer constant $\\lambda_3$ can be upper bounded via diagonal transfer layer projection. On cross-section $(5,5)$, Sector 12 compresses under the 150-element group $G_{5,5}$ into 35,070 symmetry orbits.

We reimplemented the diagonal layer transfer operators in compiled Rust with Rayon multithreading and bitmask acceleration. Iterating Collatz-Wielandt iterations beyond He Table 2 step $p=2$ (which gave 0.452130) to step $p=3$ ($XY^4\\vec{1}$) monotonically contracted the spectral radius ratio to $\\lambda_3 \\le 0.452021$, proving a strict improvement of $1.09 \\times 10^{-4} \\ge 10^{-6}$.
