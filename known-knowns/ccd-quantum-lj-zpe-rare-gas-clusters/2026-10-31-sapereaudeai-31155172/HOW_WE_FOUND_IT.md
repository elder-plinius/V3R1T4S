# How we found it (contributor text, unverified)

The brief: the Calvo-Doye-Wales table ranks a few low-lying classical LJ minima per size by classical energy plus
harmonic zero-point energy. Its candidate lists date from 2000. For neon (q = 0.095) the zero-point term is about
60 epsilon at N = 38 and differs by several epsilon between structures, so minima well above the classical global
minimum can win.

What we did, in one light run (about one hour on a laptop):
1. Built a fast numpy evaluator (energy, gradient, analytic Hessian, L-BFGS, Newton polish), and checked it against a
   finite-difference Hessian and against 47 of the table's posted structures (all four columns to 5e-5).
2. Lens "landscape": basin-hopping on the classical surface, with the Metropolis acceptance using E_Ne of each
   quenched minimum. Ten 10-minute chains ran over several sizes. At N = 38 an 18-second smoke test already passed
   the bar. The T = 0.4 chain reached E_Ne = -108.929936, and a T = 0.8 chain and an Ar-accepting chain also passed
   the bar with shallower basins.
3. Lens "representation": best-first walks along the softest normal modes of the table's own structures. These
   independently reached the same N = 38 minimum.
4. The decimal checker (50-digit energy and gradient) certified the object as written. An independent
   finite-difference self-check agreed. Three fresh-context skeptics passed it.

What did not work: no beat at N = 17, 27, 28 or 30-35, nor at 44, 57 or 98, within the 10-minute chains. No Xe or Ar
beat at N = 38. The same run found objects below the Ne bars at N = 36 and 37 and below the Ar bar at N = 67. Those
were not panelled and are not part of this package.

Caveat from the NOVELTY skeptic: the object's classical energy matches the "state 3" classical minimum reported
(energy only, with no coordinates and no harmonic value) by Predescu, Frantsuzov and Mandelshtam (2005). So the
structure itself may not be new. The claim is about its harmonic Ne value.
