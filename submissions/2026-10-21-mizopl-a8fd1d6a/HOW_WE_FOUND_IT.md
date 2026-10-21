# How We Found It — `2026-10-21-mizopl-a8fd1d6a` (`asteroid-precovery-arc-extension`)

*(contributor text, unverified)*

## 1. Two Technical Bottlenecks in Archival Pan-STARRS 1 (`F51`) Precovery

1. **STScI Pan-STARRS DR2 Filter Coverage (`g, r, i, z, y` vs `w`-band) & `TIMESYS = TAI` Exposure Midpoints:**
   - The public STScI Pan-STARRS DR2 cutout server (`ps1filenames.py` / `fitscut.cgi`) serves the $3\pi$ survey `g, r, i, z, y` warps (`2010–2014`, `MJD 55348–57050`), whereas post-2015 `F51` NEO survey observations in the wide `w` filter are not in DR2.
   - Furthermore, raw Pan-STARRS 1 warp FITS headers store the photometric zero-point for a 1-second exposure in `HIERARCH FPA.ZP` (`ZP_eff = FPA.ZP + 2.5 * log10(EXPTIME)`) and record `MJD-OBS` at the **exposure midpoint in International Atomic Time (`TIMESYS = TAI`)**, not UTC exposure start. Subtracting the exact IERS leap-second offset (`TAI - UTC = 34.0 s` prior to `MJD 56109` in 2010 and `35.0 s` prior to `MJD 57204` in 2014) eliminated a systematic `~0.85"` along-track timing bias and dropped our 4-frame post-fit residual RMS on `2014 OV236` to **`0.0442 arcsec`** (`max = 0.0853 arcsec`).

2. **1D Line-of-Variations (LOV) Tracklet Linkage for Short-Arc (`data_arc < 365 d`) Asteroids:**
   - Single-apparition (`data_arc < 365 d`) asteroids back-propagated `4–5 years` have $3\sigma$ sky uncertainty ellipses stretched into a narrow ribbon (`Line of Variations`, LOV) along the orbital track ($116.92'' \times 0.57''$ for `2019 QT15` on `2014-11-11`).
   - Using our 6D relativistic (`DE421` Sun + 8 planets + Moon + Schwarzschild 1PN) `DOP853` integrator (`verify-it-yourself/nbody_precovery.py`), we projected the $6 \times 6$ JPL SBDB covariance matrix onto the sky plane and scanned along the principal eigenvector (`lov_z in [-3, +3]`) across multi-epoch Pan-STARRS 1 warps (`how-we-built-it/lov_ps1_short_arc_hunter.py`).
   - On `2014-11-11` (`1,754.08 days` before discovery), `2019 QT15` (`data_arc = 88.0 d`, `n_obs_used = 41`) appeared at `lov_z = -0.750` (`2.16–2.85 sigma` inside the $3\sigma$ ellipse) across 3 consecutive $i$-band warps spanning `39.15 min >= 20 min`, moving by `21.66"` (`86.6` PS1 pixels) at the exact predicted rate and position angle. Full 6D Gauss-Newton differential orbit refitting (`verify-it-yourself/fits_astrometry.py`) collapsed the new-epoch residuals to `0.0216", 0.2275", 0.1756"` (`RMS = 0.1176"`), multiplied the observed arc by **`20.93x`** (`88.0 d -> 1,841.82 d`), and reduced $\sigma_a$ by **`87.38%` (`SBDB`) / `83.25%` (`LS`)**.
