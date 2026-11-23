# A Non-Isometric 19-Dimensional Periodic Sphere Packing Matching the Live Record Center Density as a Zero-Dimensional Kissing-Stratum Vertex

## What

A 6-translate periodic packing in R^19 over a det-300 Leech cross-section lattice has exact minimal squared center distance 52/15 and exact center density equal to the table's 3^(-9) 5^(-21/2) 13^(19/2), and it is non-isometric to the Chen-Hu-Li-Wang-Wu antipode packing in that cell (per-sphere kissing multiset (4022,4022,4072,4072,4072,4072) versus six 4110s, and norm-4 counts 6858 versus 6942 with trivial translate stabilizer), all certified by exact rational Fincke-Pohst enumeration with no floating point.

## Check it yourself

From this package folder in a POSIX shell with an ISO C99 compiler (`cc`) and Python `3` (`python3` standard library only, KNOWN):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS` (typical laptop runtime: `20`–`45` seconds, NUMERICAL).

## Compared to

- **Table**: Henry Cohn, *Sphere packing* (`https://cohn.mit.edu/sphere-packing/`, KNOWN)
- **Cell**: Dimension `n = 19`, unrestricted sphere packings, Table `1` (KNOWN)
- **Live Table Value**: Center density `3^(-9) * 5^(-21/2) * 13^(19/2)` (`# = 6` translates, decimal density `0.0041473691458627...`, upper bound `0.0092288097047995`, ratio `2.226`; sole lower-bound reference `[8]`: Ruitao Chen, Jiachen Hu, Binghui Li, Liwei Wang, and Tianyi Wu, `arXiv:2505.02394`, `2025`) (KNOWN)
- **Our Certified Value**: Exact center density `3^(-9) * 5^(-21/2) * 13^(19/2)` (`1461920290375446110677 / 184736485004425048828125 == (3^(-9) * 5^(-21/2) * 13^(19/2))^2`, matching live record; partial win `p1` certified by `tau_sorted = (4022, 4022, 4072, 4072, 4072, 4072)` versus `(4110, 4110, 4110, 4110, 4110, 4110)`, `leech_sat = 1`, `sym_trans_stab_size = 1`, `norm4(L_new) = 6858` versus `norm4(L_ref) = 6942`, `bilateral_contact_rank_trans = 95/95`, and `bilateral_contact_rank_full = 285/285`) (PROVED-HERE)
- **Live Fetch UTC**: `2026-11-19T06:31:25Z` (`HTTP 200`, `88271` bytes, SHA-256 `82146ed92040267f45ec2862c58534d28fe2aad5e531a7525e3e80955a4bb26d`, recorded in `the-record-we-beat/cohn_sphere_packing_snapshot.md`, KNOWN)

## Not claimed

- We do **not** claim a denser sphere packing than Cohn's live table (`Full Win`); `P19_II_vtx` matches, and does not exceed, the best known `19`-dimensional center density `3^(-9) * 5^(-21/2) * 13^(19/2)` (KNOWN / PROVED-HERE).
- We do **not** claim a pure `1`-translate lattice packing (`# = 1`, partial win `p2`, where the live `19`-dimensional lattice record is `2^(-7/2)`, KNOWN) matching the non-lattice record, nor do we claim optimality in `R^19` or a new `19`-dimensional kissing-number record.
- We do **not** claim **unilateral Farkas hard-sphere collective jamming** (positive-stress caging `omega^T J_trans = 0` with `omega` strictly positive in the sense of Salvatore Torquato and Frank H. Stillinger, *The Journal of Physical Chemistry B* `105`, no. `47` (`2001`), `11849`–`11853`, `https://doi.org/10.1021/jp011960q`, and Aleksandar Donev, Salvatore Torquato, Frank H. Stillinger, and Robert Connelly, *Journal of Computational Physics* `197`, no. `1` (`2004`), `139`–`166`, `https://doi.org/10.1016/j.jcp.2003.11.022`, and *Journal of Applied Physics* `95`, no. `3` (`2004`), `989`–`999`, `https://doi.org/10.1063/1.1633647`, KNOWN): our Jacobian ranks (`bilateral_contact_rank_trans = 95/95`, `bilateral_contact_rank_full = 285/285`, PROVED-HERE) certify **bilateral** bar-framework contact-stratum rigidity (`0`-dimensional vertex isolation inside the fixed kissing-graph stratum), whereas all `100` cross-cluster contacts on `(0, 2)` and `(3, 4)` lie in a single open half-space so translating `{t_1, t_2, t_3}` back along `-u_int / 1860` detaches those cross-cluster contacts into `Orbit II`'s open `19`-dimensional rattle cavity while remaining strictly over `L_II` (`norm4 = 6858 != 6942`, `tau ≤ 4072` strictly below `4110`, NUMERICAL).

## Credits

- **Henry Cohn**: *Sphere packing* live density table (`https://cohn.mit.edu/sphere-packing/`, KNOWN).
- **Ruitao Chen, Jiachen Hu, Binghui Li, Liwei Wang, and Tianyi Wu**: *New Sphere Packings from the Antipode Construction*, preprint (`2025`), `arXiv:2505.02394` (`https://arxiv.org/abs/2505.02394`, KNOWN), who discovered the rank-`5` determinant-`300` Gram matrix `K_19` and constructed the original (`Orbit I`) `19`-dimensional record packing compared against here.
- **John H. Conway and Neil J. A. Sloane**: *The antipode construction for sphere packings*, *Inventiones Mathematicae* `123`, no. `2` (`1996`), `309`–`313` (`https://doi.org/10.1007/s002220050028`, KNOWN), and *Sphere Packings, Lattices and Groups*, `3`rd ed., Grundlehren der mathematischen Wissenschaften `290`, Springer-Verlag, New York (`1999`, `https://doi.org/10.1007/978-1-4757-6568-7`, KNOWN), for the antipode construction and `4 x 6` Miracle Octad Generator coordinates of `Lambda_24`.
- **Ivan Dorofeev, Xiaoming Sun, and Chengu Wang**: *Optimal Extensions of Cross-Sections: Sphere Packings in Dimensions 38 to 43*, preprint (`2026`), `arXiv:2607.20359` (`https://arxiv.org/abs/2607.20359`, KNOWN), for the fiber-kissing analysis of antipode packings and embedding-dependence remarks in `P_48` (`dimensions 38`–`47`, KNOWN).
- **Salvatore Torquato, Frank H. Stillinger, Aleksandar Donev, and Robert Connelly**: *Multiplicity of Generation, Selection, and Classification Procedures for Jammed Hard-Particle Packings*, *The Journal of Physical Chemistry B* `105`, no. `47` (`2001`), `11849`–`11853` (`https://doi.org/10.1021/jp011960q`, KNOWN); *A linear programming algorithm to test for jamming in hard-sphere packings*, *Journal of Computational Physics* `197`, no. `1` (`2004`), `139`–`166` (`https://doi.org/10.1016/j.jcp.2003.11.022`, KNOWN); and *Jamming in hard sphere and disk packings*, *Journal of Applied Physics* `95`, no. `3` (`2004`), `989`–`999` (`https://doi.org/10.1063/1.1633647`, KNOWN), for the distinction between bilateral bar-framework contact-Jacobian rank and unilateral Farkas hard-sphere collective jamming.
- **Henry Cohn, Abhinav Kumar, Stephen D. Miller, Danylo Radchenko, and Maryna Viazovska**: *The sphere packing problem in dimension 24*, *Annals of Mathematics* (`2`) `185`, no. `3` (`2017`), `1017`–`1033` (`https://doi.org/10.4007/annals.2017.185.3.8`, `https://arxiv.org/abs/1603.06518`, KNOWN).
- **Alexey Kravatskiy**: *Sphere-packing density bounds and constructions* (`https://github.com/alexlegeartis/SpherePackings`, `2026`; repository `CITATION.cff` title: *Sphere-packing density: new upper bounds in dimensions 4 through 48, with verification packages*, KNOWN), cited on Cohn's `n = 19` upper-bound column (`[25]`, KNOWN).
