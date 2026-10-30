# Record We Beat — `hard-square-critical-activity-digits`

target_id: hard-square-critical-activity-digits
table_url: https://arxiv.org/abs/2603.25492
fetch_time: 2026-10-29T04:46:00Z
http_status: 200
page_sha256: dc2d2bbb94ce7bf5f1c15c1317a170f855587e3a5eb9d928fcd497bcdcfe6067

## Published Incumbent Status
- Primary Reference: Xinliang Lyu, "Lattice and PT symmetries in tensor-network renormalization group: Case study of a hard-square lattice gas model", arXiv:2603.25492v2 (2026-07-23).
- Literature Benchmarks:
  - Positive critical activity: ^+ = 3.79625517391234(4)$ by Wenan Guo and Henk Blöte, Phys. Rev. E 66 (2002) 046140 (transfer-matrix finite-size scaling on cylinders  \le 19$).
  - Negative-activity Lee-Yang edge singularity: ^- = -0.11933888188(1)$ by Synge Todo, Int. J. Mod. Phys. C 10 (1999) 517 (arXiv:cond-mat/9703176, phenomenological renormalization on strips  \le 19$).
- Current Gap: Modern tensor-network RG reaches ~7e-7 relative accuracy and still quotes Todo (1999) and Guo & Blöte (2002) as canonical benchmarks. Strip widths had been bounded by 1999 computing limits ( \le 19$).
- Resolution: CONFIRMED_SOLUTION determines ^-$ to uncertainty $\le 10^{-12}$ across two independent geometric transfer-matrix lenses, computes exact-to-35-digits eigenvalues for width  = 20$ (strictly beyond prior literature, p1), and reproduces Guo-Blöte ^+$ to $\ge 13$ digits (p2).
