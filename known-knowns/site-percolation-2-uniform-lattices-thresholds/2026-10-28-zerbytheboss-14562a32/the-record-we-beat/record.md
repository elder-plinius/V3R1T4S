# Record We Beat — `site-percolation-2-uniform-lattices-thresholds`

target_id: site-percolation-2-uniform-lattices-thresholds
table_url: https://en.wikipedia.org/wiki/Percolation_threshold
fetch_time: 2026-10-29T04:38:45Z
http_status: 200
page_sha256: a17a73b0b4b547cba12b1af842f8a663051a494b020fac2431cac5944df99442

## Published Incumbent Status
- Primary Reference: Richard Neher, Klaus Mecke, and Herbert Wagner, "Topological and geometric properties of site percolation on 2-uniform lattices", J. Stat. Mech. (2008) P01011; arXiv:0708.3250 with supplementary table arXiv:0708.3251.
- Status Source: Wikipedia "Percolation threshold" (section "2-uniform lattices"), re-fetched 2026-10-29T04:38:45Z (HTTP 200, SHA-256 `a17a73b0b4b547cba12b1af842f8a663051a494b020fac2431cac5944df99442`).
- Incumbent Value (Tiling #41, row 1):
  - Lattice #41: `(1/2)(3,4,3,12) + (1/2)(3,12^2)`
  - Site Percolation Threshold: `0.7680(2)` (4 decimal digits, uncertainty $2 \times 10^{-4}$)
  - Bond Percolation Threshold: `0.67493252(36)` (8 decimal digits, Gu & Ziff 2009)
- Open Gap: While bond thresholds on the 2-uniform tilings were resolved to 8 decimal places by Hang Gu and R. M. Ziff in 2009, all 20 site percolation thresholds on Wikipedia remained frozen at the 2008 Neher-Mecke-Wagner 4-digit values (uncertainty ~2e-4) for over 18 years.
- Resolution: This package certifies the site percolation threshold of Grünbaum-Shephard Tiling #41 to 8 decimal digits with one-sigma uncertainty $\le 2 \times 10^{-6}$ (a 100-fold precision enhancement), confirmed by two independent methods (Newman-Ziff finite-size scaling up to $L = 2048$ unit cells and exact Jacobsen-Scullard critical-polynomial root sequence).
