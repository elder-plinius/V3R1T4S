# PREREG: CCD cobalt Gupta clusters Co_N, N = 2..200 (bank target ccd-gupta-cobalt-clusters-n200)

Written before any request of this task. Upstream main 04fdfba48c6e277fe083b6811f1a5deb3c52b74e. Classification:
part A is an audit (bank partial win p1); part B is an exploratory search; part C is the confirmatory check of any
candidate from B, with code written separately from the search code.

## Questions and novelty
- A (audit, p1): under ONE Gupta parameter set calibrated on the posted files, (a) does each of the 199 table point
  files reproduce its posted energy within 1e-5 eV, (b) does each of the ten Co.zip files reproduce the energy the
  page states for it, and (c) does any posted structure polish lower by more than 1e-4 eV? Novelty: the bank lists
  this audit as partial win p1; no published audit of this table is known to us.
- B (search): is there, for some N in 2..200, a Co_N structure whose energy under the calibrated potential is lower
  by >= 1e-4 eV than min(table, Co.zip, any published value for the same potential)? Expected value: the bank's
  statement says the 2..200 range rests on one 2005 search plus a 10-size patch; prior is modest (N > 100 likeliest).

## Primary sources (pinned by sha256 on download)
CCD cobalt page https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/cobalt.html, points.tgz, Co.zip (same directory);
Zhan, Chen, Liu, Lai, J. Chem. Phys. 122, 244707 (2005), doi 10.1063/1.1940028 (metadata only; full text if open).

## Method
- Potential: E = sum_i [ sum_{j!=i} A exp(-p (r_ij/r0 - 1)) - sqrt( sum_{j!=i} xi^2 exp(-2 q (r_ij/r0 - 1)) ) ], no
  cutoff unless the page states one. Parameters: those stated on the CCD page if any; otherwise Cleri-Rosato (1993)
  cobalt values as the starting point. CALIBRATION RULE (fixed now): a parameter set is accepted only if it reproduces
  the posted energies of 10 table files chosen by random.Random(20261019).sample(range(2, 201), 10) to 1e-6 eV AND all
  ten Co.zip files to the precision printed on the page. If no set passes, part B is not run and A reports the best
  set and the residuals (negative result).
- A: energy of every file in float64 with math.fsum; polish = L-BFGS (scipy) to gradient norm < 1e-8, then Newton
  steps with the analytic Hessian to < 1e-10 if reachable in float64 (report the reached norm); Hessian eigenvalues.
- B (exploratory): seeded basin hopping (add/remove one surface atom from the best N-1 / N+1, random rotations of
  surface atoms) and lattice seeds (Ino/Marks decahedra, Mackay icosahedra, fcc/hcp spheres), first for
  N = 80..125 and 190..200, then the rest if budget remains. Seeds: numpy default_rng(100000 * N + run).
- C (confirmatory): a second implementation (pure Python + math.fsum, and mpmath at 30 digits if installable) evaluates
  energy and gradient; Hessian check (exactly 6 |lambda| < 1e-6, no negative eigenvalue); polish every posted structure
  for that N and require a gap >= 1e-4 eV (distinct basin); re-fetch the live page before any claim; literature
  search (arXiv, Crossref) for 'cobalt clusters Gupta global minimum'.
## Success / refutation
B succeeds for N only under the bank's full success criterion (margin >= 1e-4 eV vs table, Co.zip and literature;
certified minimum; distinct basin). Otherwise B is a negative result for the sizes searched, reported with budget used.
## Budget and stop
Downloads: www-wales.ch.cam.ac.uk only, <= 5 requests, <= 20 MB, no retries; stop on 4xx/5xx. Compute for B: <= 2 h
wall in total, <= 2 worker processes, <= 1.5 GB RSS; stop early if system free memory < 15%.
## Negative controls (C)
(1) a posted structure with one atom displaced by 0.05 A must fail the gradient test; (2) a structure with N-1 atoms
must be rejected; (3) a wrong parameter set (p +1%) must fail calibration; (4) re-polishing a posted structure must
not pass the distinct-basin test.
## Alternative explanations to rule out
under-converged posted coordinates; parameter-set mismatch; unit or scaling (eV vs reduced); comparison against the
table where Co.zip already holds a better value; values already published after 2005.
FROZEN 2026-10-19T03:56:13Z

## Format line required by kit/RUN.md step 3b (added 2026-10-19T04:45:18Z, before any claim/ file existed; every line above is
## byte-identical to the frozen file, sha256 5c2849aab40ea75f...)
null_test: not needed because the claim is an explicit object checked by a deterministic checker against table values
