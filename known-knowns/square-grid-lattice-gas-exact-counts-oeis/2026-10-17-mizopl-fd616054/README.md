# A054759(15): Eulerian orientations of the 15×15 square torus

## What

A054759(15) = 4310182149988584261406143524214457416387448 is confirmed under p1's two-run rule (two agreeing runs with disjoint prime sets and different decompositions: forward+closed-form vs reversed-encoding+explicit-walk, both independently recomputed) and reproduction rule (method reproduces all published terms n=1..14 exactly, and the Eulerian-orientation definition is confirmed by brute force for n=1..3); the main criterion's 1e-3 growth clause is not met at n=15 (gap 0.0074, and the published a(14) also fails it) and is not part of p1.

A054759(n) is the number of Eulerian orientations of the n×n grid on a torus — equivalently the
square-ice / six-vertex model at the ice point: orient every one of the 2n² edges so each vertex has
in-degree 2 and out-degree 2. This package adds the first term past the published range (n=15; the OEIS
b-file/DATA stopped at n=14).

## Check it yourself

One command from this folder (Python 3, standard library; numpy optional for one extra n=15 residue):

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: ~70 s on a laptop. It (A) brute-forces the definition for
n=1,2,3, (B) independently reproduces the published terms n=1..10 with a pure-Python transfer matrix,
(C) independently CRT-reconstructs the n=15 value from the saved residues and checks the CRT bound and
prime-set disjointness, and (D) if numpy is present, recomputes one n=15 residue from scratch.

For the full two-run recomputation of a(15) (~12 min, needs numpy), see RUN_IT_YOURSELF.md.

## Compared to

| sequence | cell | our value | previous table value (a(14)) | source | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A054759 | a(15) | 4310182149988584261406143524214457416387448 | 15844635835975276495290739119895808472 | https://oeis.org/A054759/b054759.txt | 2026-10-17T12:52:52Z |

The b-file (and the sequence DATA) ended at a(14); a(15) was unpublished. See the-record-we-beat/ for the
snapshot (URL, UTC time, HTTP status, sha256).

## Not claimed

- This is a **partial win (p1)**, not the main target (the main target is A028420/A006506/A063443). A054759
  is explicitly a partial in the target definition.
- The main criterion's growth clause "a(N)^(1/N²) within 1e-3 of the entropy constant" is **NOT** met:
  a(15)^(1/225) = 1.546987 vs the Lieb ice constant W=(4/3)^(3/2) = 1.539601 (gap 0.0074). The published
  a(14) also fails this clause (gap 0.0085), so the 1e-3 bound is an asymptotic note no finite reachable
  term satisfies; p1 names only the two-run and reproduction rules, not the growth clause.
- No claim about n ≥ 16, and no claim that this method is novel (it is the standard six-vertex transfer
  matrix; the contribution is computing one further exact term and verifying it).

## Credits

- **Contributor:** [mizopl](https://github.com/mizopl). Found with a V3R1T4S agent run (smaller-first lens), checked by a 3-skeptic panel.
- **Brendan McKay** — computed A054759 through a(14) (OEIS extension, Apr 18 2024). https://oeis.org/A054759
- **The OEIS Foundation** and the A054759 authors/editors — the sequence and its b-file. https://oeis.org/A054759
- **Elliott H. Lieb** — residual entropy of square ice, W=(4/3)^(3/2) (Phys. Rev. Lett. 18, 692, 1967),
  used only as the asymptotic reference constant.
- **Rodney J. Baxter** — exactly-solved-models / six-vertex transfer-matrix framework.
- Method: the sector (conserved up-arrow count) transfer matrix for the six-vertex model at the ice point.
