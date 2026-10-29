# How we found it (contributor text, unverified)

- Night 1 (2026-10-22): a small periodic ResNet (14,114 parameters) times a fixed stripe sign, projected on a C4v irrep
  and spin flip, trained by MinSR: exact to 5.9e-5 on 4x4 and 4.95e-4 on 6x6 (J2 = 0.8); its kernels transferred to
  10x10 at J2 = 0.9 and were trained for 648 steps. The training-batch energies sat 0.07 below the published ViT value,
  but training-batch means are not estimates, and on 4x4 the training sampler saw almost none of the true variance.
- Night 2 (2026-10-23): an independent estimator was written and frozen in a pre-registration with instrument checks.
  Two first-design checks failed (an importance sampler over the symmetry images missed half the variance; a float32
  reference was too coarse); a second pre-registration, written before any 10x10 estimate, replaced them with a
  defensive neighbour-mixture estimator (DIS) and a float64 cross-check, and both passed. Exact 4x4 enumeration showed
  where the variance lives (97% on 0.09% of the weight) and that the tail is nearly symmetric.
- Three independent 10x10 measurements (two plain, one DIS; fresh chains and seeds fixed in advance) agree within
  their errors and lie about 0.08 below the bar; a three-skeptic panel checked the claim (panel/).
