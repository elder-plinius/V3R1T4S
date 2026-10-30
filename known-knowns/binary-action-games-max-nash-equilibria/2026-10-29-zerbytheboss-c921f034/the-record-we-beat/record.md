# Record We Beat — `binary-action-games-max-nash-equilibria`

target_id: binary-action-games-max-nash-equilibria
table_url: https://arxiv.org/abs/2412.17890
fetch_time: 2026-10-29T04:41:42Z
http_status: 200
page_sha256: c2cd243dedf14c4a0f1d2b13977ce80f010a1be84f2bc48d2f2d2baa46a215fa

## Published Incumbent Status
- Primary Reference: Christoph Hertling, Jelena Vujic, "Maximal two-action games", arXiv:2412.17890v2 [math.PR] (25 Sep 2026).
- Status Source: arXiv:2412.17890v2 page retrieved 2026-10-29T04:41:42Z (HTTP 200).
- Published Record:
  - Vidunas (2017) established the theoretical upper bound mu(4) <= 65.
  - Hertling and Vujic (arXiv:2412.17890v2, Theorem 4.2) established the lower bound mu(4) >= 37 by proving the existence of generic deformations of product two-action games.
  - Conjecture 4.5 optimistically conjectures mu(4) = 37.
- Open Gap: The published proof in Hertling & Vujic is an abstract deformation/existence proof; no explicit certified rational payoff table listing all 37 equilibrium coordinates and machine-checked Jacobians existed in standard repositories.
- Resolution: This package establishes an explicit generic rational 4-player binary-action game with exactly 37 regular Nash equilibria (Partial Win p1), certified across all 81 support branches with non-singular Jacobians and strict best-response slacks.
