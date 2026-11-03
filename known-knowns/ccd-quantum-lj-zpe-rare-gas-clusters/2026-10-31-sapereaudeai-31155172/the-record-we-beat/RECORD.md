# The record we compared against

- Table: "Lennard-Jones clusters LJ_n which change global minimum in the range n<100" (energies with harmonic
  zero-point energy for Xe, Ar, Ne), Cambridge Cluster Database, page signed "Florent Calvo 12/12/2000";
  the data of F. Calvo, J. P. K. Doye and D. J. Wales, J. Chem. Phys. 114, 7312 (2001).
- URL: https://www-wales.ch.cam.ac.uk/~florent/LJZPE/table.html
- Fetched once by the run: 2026-10-31T19:16:16Z (curl start, `date -u`), HTTP 200, 27710 bytes,
  sha256 of the page 5e8632e8ab257910961ae596019c6a7fa9335c68e4d7c08e8552f0fb1751177b.
- Selected response headers: `Date: Sat, 31 Oct 2026 19:16:21 GMT`, `Last-Modified: Mon, 26 Feb 2018 16:57:01 GMT`,
  `Content-Length: 27710`, `Content-Type: text/html`.
- Re-fetched by the NOVELTY skeptic at 2026-10-31T19:37:09Z and the CRITERION skeptic at 19:40:18 GMT. Both copies
  were byte-identical (same sha256), per `panel/novelty.md` and `panel/criterion.md`.
- Extracted cell (N = 38 rows; columns E_LJ, E_Xe, E_Ar, E_Ne, point group):
  - 38A: -173.92843, -166.82835, -152.62818, -106.47765, Oh
  - 38B: -168.51999, -162.08887, -149.22662, -107.42431, C1
- Compared value: lowest Ne value for N = 38 = **-107.42431** (row 38B). This package's object: E_Ne = -108.929936.
- The page itself is not included.
