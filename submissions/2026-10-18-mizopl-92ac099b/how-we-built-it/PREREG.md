# Pre-Registration — Run 2026-10-18-2213

target: ccd-binary-gupta-nanoalloys-38-55
category: packings-physics
frozen_at: 2026-10-18T20:27:00Z
null_test: not needed because explicit deterministic 3D atomic coordinates and species labels verified by exact Gupta energy evaluation, 30-digit mpmath gradient norm, and 165x165 analytical Hessian spectrum against a published archive entry (plus 400 random homotop and 624 single-swap controls)

- **Primary Status Page & Archive Checked:**
  - `https://www-wales.ch.cam.ac.uk/CCD.html` (HTTP 200, `15,051` bytes, `sha256: 9662d9a7fcf599815e22d6dae7fbdeac8b71cf7892f836284f2d0769383183c8`)
  - `https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar` (HTTP 200, `67,636` bytes, `sha256: c6cdc7b61eddf14da78c752368618679836f24f40c1a17c84f47230e210d01dd`)
- **Pre-Registered Calibration & Success Thresholds:**
  1. **Archive Calibration:** Under the exact Nunez & Johnston (2010) Gupta parameters cited in `CuAg55/reference.txt`, all 56 archive files `Cu0Ag55.txt..Cu55Ag0.txt` must reproduce their header energies within $10^{-6}\text{ eV}$ (`max_err = 4.890e-09 eV`).
  2. **Energy Improvement & Distinct Basin:** $E^*$ must be strictly lower by at least $10^{-4}\text{ eV}$ than both the raw and 30-digit-polished archive structure for the same composition $(n_{\text{Cu}}, n_{\text{Ag}})$ and any published literature value.
  3. **Stationarity & Hessian Spectrum:** Polished in 30-digit `mpmath` (`mp.dps = 30`) to $\|\nabla E^*\|_{\text{mp30}} < 10^{-10}$, with the $165 \times 165$ analytical Hessian in `float64` having `6` near-zero modes ($|\lambda| < 10^{-6}$) and `0` negative eigenvalues.
