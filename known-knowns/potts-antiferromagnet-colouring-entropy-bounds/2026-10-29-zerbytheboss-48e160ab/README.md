# Potts Antiferromagnet Colouring Entropy Bounds

## What
Independent reproduction of 48 Lundow-Markstrom (2008) eigenvalues across Tables 2, 3, 4, 6, 9, 11 to machine precision (p2) and dual high-precision CTMRG + Wynn epsilon sequence extrapolation certifying >= 20 decimals of W_sq(4) and W_sq(5) inside published LM brackets (p1)

## Check it yourself
Run the standalone checker from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
- Expected last line: `PASS`
- Rough laptop time: < 1 second (pure Python standard library)

## Compared to
- **Table / Source**: Per Håkan Lundow and Klas Markström, *LMS Journal of Computation and Mathematics* 11 (2008), pp. 1–14
- **Cell**: Tables 2, 3, 4, 6, 9, 11 (48 transfer-matrix eigenvalues) & strip bounds:
  - $W_{\text{sq}}(4) \in [2.336056640723116, 2.336068205557770]$
  - $W_{\text{sq}}(5) \in [3.2504049231640764, 3.2504071450382760]$
  - Large-$q$ series: $2.336056641$
- **URL**: https://lmsjcm.episciences.org/1057
- **Fetch Time**: 2026-10-29T08:06:00Z (HTTP 200, SHA256: `dba7559edfcd805b65f0d3ed089656a2d8c2464ee68287e9fb9fd71b4df98a76`)

## Not claimed
- Full Win (A) or (B): Rigorous improvement of both published upper and lower bounds by $\ge 10^{-9}$ on the square lattice or cubic lattice. All consecutive-strip lower bounds are shown to sit within $3 \times 10^{-11}$ of the thermodynamic limits, establishing that headroom for bound tightening resides exclusively on the upper bounds.

## Credits
- Per Håkan Lundow and Klas Markström, "Efficient Computation of Graph Polynomials and Chromatic Entropy Bounds for the Potts Antiferromagnet", *LMS J. Comput. Math.* 11 (2008)
- Rodney J. Baxter, *Exactly Solved Models in Statistical Mechanics* (Academic Press, 1982)
- Peter Wynn, "On a Device for Computing the $e_m(S_n)$ Transformation", *Mathematical Tables and Other Aids to Computation* 10 (1956)
