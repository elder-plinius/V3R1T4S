# Ne38 with harmonic zero-point energy: a classical LJ38 minimum below the Calvo-Doye-Wales table's lowest Ne value

Target: `ccd-quantum-lj-zpe-rare-gas-clusters` (V3R1T4S bank). Cell: N = 38, neon (q = 0.095). Credit: SapereAudeAI.

## What

The 38-atom configuration in object/N38_Ne.xyz (sha256 31155172...0fe1), as written with 18 significant digits, is a certified local minimum of the classical Lennard-Jones energy (E_LJ = -168.984987247422, gradient norm 1.641e-13, exactly 6 |lambda| < 1e-6, lowest eigenvalue -9.65e-14), and its harmonic Ne energy E_LJ + (0.095/2) sum sqrt(lambda) over its 108 nonzero eigenvalues is -108.929936, which is 1.505626 below -107.42431, the lowest Ne value (row 38B) for N = 38 on the LJZPE table at www-wales.ch.cam.ac.uk/~florent/LJZPE/table.html (unchanged as of 2026-10-31T19:40Z), with the table convention reproduced on rows 17A, 31B, 38A and 38B to within 1.1e-5; comparison against other published harmonic-ZPE values was not checked by this skeptic.

(That is the panel's confirmed_scope sentence, verbatim. The object file is `object/N38_Ne.xyz`, sha256
31155172b650ba08dc63be96d76a7f189e754612e2d6e7183a744ac6c1270fe1.)

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Needs Python 3 with numpy (`python3` or `python` on PATH). Expected last line: `PASS`. It takes a few seconds on a
laptop. The checker computes E_LJ and the gradient in 50-digit decimal arithmetic, takes the analytic Hessian's
eigenvalues in double precision, applies the criterion's minimum tests, computes E_Ne = E_LJ + (0.095/2) sum
sqrt(lambda) over the 3N-6 nonzero eigenvalues, and requires bar - E_Ne >= 5e-4. Real output: `verify-it-yourself/RECEIPTS.md`.
`RUN_IT_YOURSELF.md` adds the criterion's calibration on the table's rows 17A, 31B, 38A and 38B.

## Compared to

- Table: https://www-wales.ch.cam.ac.uk/~florent/LJZPE/table.html (Cambridge Cluster Database; F. Calvo, J. P. K.
  Doye, D. J. Wales, J. Chem. Phys. 114, 7312 (2001); page signed "Florent Calvo 12/12/2000").
- Cell: N = 38, Ne column. Rows 38A -106.47765 and 38B -107.42431, so the bar is **-107.42431**.
- This object: E_Ne = -108.929936, lower by 1.505626 (the criterion needs 5e-4).
- Table fetched 2026-10-31T19:16:16Z (HTTP 200, sha256 5e8632e8ab257910961ae596019c6a7fa9335c68e4d7c08e8552f0fb1751177b),
  and re-fetched by two skeptics at 19:37Z and 19:40Z with identical bytes. Details: `the-record-we-beat/RECORD.md`.
- Published harmonic values found by the NOVELTY skeptic for Ne38: none below -107.42431. Predescu, Frantsuzov and
  Mandelshtam 2005, Table I, repeat 38B (-100.639 K/atom = -107.4237 eps) and Oh.

## Not claimed

- Not a quantum ground state. The harmonic approximation is known to be poor for Ne38: path-integral and DMC
  ground-state energies (about -113 eps) are far lower and use other conventions.
- Not that the structure is new. Its classical energy matches the "state 3" classical minimum that Predescu et al.
  (2005) reported with neither coordinates nor a harmonic value. The claim is about the harmonic Ne value of this
  minimum against the table.
- Not the lowest harmonic Ne value for N = 38. The search was stochastic and capped, so no search space is covered.
- Nothing about Xe or Ar at N = 38 (this object does not beat those columns), or about any other N.

## Credits

- F. Calvo, J. P. K. Doye and D. J. Wales: the table, its point files and the harmonic-ZPE convention
  (J. Chem. Phys. 114, 7312 (2001), https://www-wales.ch.cam.ac.uk/pdf/JCP.114.7312.2001.pdf), hosted on the
  Cambridge Cluster Database (https://www-wales.ch.cam.ac.uk/CCD.html).
- C. Predescu, P. A. Frantsuzov and V. A. Mandelshtam, J. Chem. Phys. 122, 154305 (2005), arXiv:physics/0508057
  (https://arxiv.org/abs/physics/0508057): the published harmonic Ne38 values, and a possible earlier
  classical-energy-only report of this minimum ("state 3").
- J. D. Mallory and V. A. Mandelshtam, J. Chem. Phys. 149, 104305 (2018)
  (https://pubs.aip.org/aip/jcp/article/149/10/104305/196157/), and C. Deckman, P. A. Frantsuzov and
  V. A. Mandelshtam, Phys. Rev. E 77, 052102 (2008) (https://www.chem.uci.edu/~mandelsh/publ/LJ_Quantum.pdf):
  quantum (DMC, VGW) studies of LJ38 checked for comparable values.
- The search method is basin-hopping (Wales and Doye) with an E_Ne acceptance rule. Panel files are in `panel/`.
