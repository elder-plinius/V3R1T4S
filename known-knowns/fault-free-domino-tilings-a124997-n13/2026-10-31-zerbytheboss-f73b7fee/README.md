# Fault-Free Domino Tilings of the Square: A124997(13), A124997(14), A124997(15), and 24x26

## What

Exact fault-free domino tiling counts A124997(13) = 6247544447707621227323332397746698905631862234864529357713987234906581365476497906 (full win, 26x26 square), A124997(14) = 199616955472645465045650566203466781313162448998311240985347793453943630517044514139601504958394 (partial win p1, 28x28 square), fault_free(24, 26) = 1917746391484128020631543300994138189551214236354867955795097459933023415049 (partial win p2, 24x26 rectangle), and A124997(15) = 63475064278343163277051387360507712735129306155819697817518828203759678852889059288805572285667838906821823010 (30x30 square), verified by independent algebraic and combinatorial solvers reproducing A124997(1..12).

## Check It Yourself

Run the standalone verification script from the package root:

```bash
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/check_fault_free.py` (Python 3 standard library only, ~2.0 seconds runtime), which computes the exact rectangle domino tiling table $D(w, h)$ up to $30 \times 30$ via two independent methods (Chebyshev-resultant companion determinant and bipartite Kasteleyn transfer / broken-profile DP), computes `A124997(1..15)` and `fault_free(24, 26)` via both Integer-Partition Horizontal Fault Compression with 1D Renewal Inversion (`Method 1`) and Parity-Split Even-Composition Decomposition (`Method 2`), cross-checks $6 \times 6$, $8 \times 8$, and $10 \times 10$ against Direct Unbroken-Line Bitmask Profile Transfer (`Method 3`), and verifies every field in `object/a124997_fault_free_dominoes.json`.

## Compared To

- **Published Record (OEIS A124997)**: Entered by Don Knuth in 2008, extended to $a(7)$ by Alois P. Heinz in 2015, and extended to $a(8)..a(12)$ ($24 \times 24$) by Xu Mingkuan in December 2016 (`b124997.txt` ends at $n = 12$ with `a(12) = 1934659183999048207708201264307215891852758175871534722685882120022644`).
- **This Submission**: Extends `A124997` by three new consecutive terms (`a(13)` on the $26 \times 26$ board, `a(14)` on the $28 \times 28$ board, and `a(15)` on the $30 \times 30$ board) plus the $24 \times 26$ rectangular count (`p2`).

## Not Claimed

- No closed-form product formula analogous to Kasteleyn's unconstrained formula (A004003) is claimed for fault-free domino tilings.

## Credits

- Contributor: `@HindsightWise`
- Prior work:
  - Ronald L. Graham, "Fault-free tilings of rectangles," in *The Mathematical Gardner*, ed. D. A. Klarner (1981), 120-126.
  - Pieter W. Kasteleyn, "The statistics of dimers on a lattice: I. The number of dimer arrangements on a quadratic lattice," *Physica* 27 (1961), 1209-1225 (`https://oeis.org/A004003`).
  - Donald E. Knuth, Alois P. Heinz, and Xu Mingkuan (`https://oeis.org/A124997` and `https://oeis.org/A124997/b124997.txt`, 2008-2016).
  - Pablo Blanco, Robert Dougherty-Bliss, Natalya Ter-Saakov, and Doron Zeilberger, "The Amazing World of Framing," `https://arxiv.org/abs/2606.05439` (2026).
