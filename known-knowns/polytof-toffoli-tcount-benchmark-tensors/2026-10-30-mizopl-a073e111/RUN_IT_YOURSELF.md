# Run It Yourself

From the package root (`known-knowns/polytof-toffoli-tcount-benchmark-tensors/2026-10-30-mizopl-a073e111/`):

```bash
bash verify-it-yourself/run_checks.sh
```

## What `run_checks.sh` Does (`~0.21s` on a single CPU core)
1. Verifies `SHA256SUMS` across all package files.
2. Runs `python3 verify-it-yourself/verify.py --cert object/p2_0725_optimality_certificate.json`, which recomputes from scratch:
   - All $\left[\begin{matrix} 6 \\ 3 \end{matrix}\right]_2 = 1,395$ RREF 3D subspaces of $\mathbb{F}_2^6$ and their 20-bit exterior 3-wedge masks in $\Lambda^3(\mathbb{F}_2^6)$, checking all $1,395$ singletons ($R=1 \implies 0$), all $\binom{1395}{2} = 972,315$ pairs ($R=2 \implies 0$), and all $120$ optimal unordered triples at $R=3$.
   - All $9$ rank-1 bilinear forms on $\mathbb{F}_2^2 \times \mathbb{F}_2^2$ for `0525`, checking all $9$ singletons ($R=1 \implies 0$), all $36$ pairs ($R=2 \implies 0$), and all $3$ optimal triples at $R=3$.
   - The $41 \times 63$ parity-check matrix $H$ of $\mathrm{RM}(3,6)^* / \mathrm{RM}(2,6)^*$, its 22-dimensional nullspace $\ker(H)$, and the exact Hamming weight of all $2^{22} = 4,194,304$ valid Waring decompositions in the coset $e_0 + \ker(H)$ ($0$ at $r \le 16$, $1,008$ optimal schemes at $r = 17$), and asserts exact equality with `object/p2_0725_optimality_certificate.json`.
