# How We Found It — `2026-10-29-mizopl-1b264270` (`asteroid-precovery-arc-extension`: `2014 OV236`)

*(contributor text, unverified)*

## 1. Technical Keys in Archival Pan-STARRS 1 (`F51`) Multi-Night Precovery (`2014 OV236`)

1. **STScI Pan-STARRS DR2 Filter Coverage (`g, r, i, z, y`) & `TIMESYS = TAI` Exposure Midpoints:**
   - The public STScI Pan-STARRS DR2 cutout server (`ps1filenames.py` / `fitscut.cgi`) serves the $3\pi$ survey `g, r, i, z, y` warps (`2010–2014`, `MJD 55348–57050`).
   - Raw Pan-STARRS 1 warp FITS headers store the photometric zero-point for a 1-second exposure in `HIERARCH FPA.ZP` (`ZP_eff = FPA.ZP + 2.5 * log10(EXPTIME)`) and record `MJD-OBS` at the **exposure midpoint in International Atomic Time (`TIMESYS = TAI`)**, not UTC exposure start. Subtracting the exact IERS leap-second offset (`TAI - UTC = 34.0 s` prior to `MJD 56109` in August 2010) eliminated a systematic `~0.85"` along-track timing bias and dropped our 4-frame post-fit residual RMS on `2014 OV236` to **`0.0442 arcsec`** (`max = 0.0853 arcsec`).

2. **Multi-Night Multi-Band (`r, i, g`) Precovery & $\sigma_a$ Reduction (`precovery-neocp-style-short-arc`):**
   - Back-propagating `2014 OV236` (`first_obs = 2014-05-24`, `n_obs_used = 36 < 50`) by `1,375.0 days` (`3.76 years`) using our 6D relativistic (`DE421` Sun + 8 planets + Moon + Schwarzschild 1PN) `DOP853` integrator (`verify-it-yourself/nbody_precovery.py`) yielded 4 high-SNR (`SNR = 36.39, 32.59, 46.85, 15.60`) detections across 2 consecutive nights (`2010-08-18` and `2010-08-19`) in `r`, `i`, and `g` filters, each `1.13–1.69 sigma` inside the $3\sigma$ error ellipse ($0.69'' \times 0.25''$).
   - Full 6D Gauss-Newton differential orbit refitting (`verify-it-yourself/fits_astrometry.py`) across all 40 observations (`36` MPC + `4` new PS1) yielded post-fit new residuals `0.0582", 0.0517", 0.0477", 0.0853"` (`RMS = 0.0442"`), extended the observed arc from `3,870.0 d` to `5,244.96 d`, and reduced $\sigma_a$ by **`62.92%` (`LS`) / `55.37%` (`SBDB`)**.
