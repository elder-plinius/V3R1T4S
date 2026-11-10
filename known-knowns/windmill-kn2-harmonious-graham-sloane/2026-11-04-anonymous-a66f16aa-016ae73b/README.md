# Finite nonexistence decision for K10^(2)

## What

There is no injective labeling of the 19 vertices of two copies of K10 sharing exactly one vertex by residues modulo 90 for which the 90 within-clique edge sums are all distinct modulo 90.

This is a computational claim for the single enumerated partial win p1 of `windmill-kn2-harmonious-graham-sloane`. Its proof consists of complete finite enumeration with two distinct research programs, reviewed and reproduced with a third independently written checker.

## Check it yourself

Requirements: Python 3.8+ and PowerShell 7.3+ with its bundled .NET UInt128 support. Validation here used Python 3.14.2 and PowerShell 7.6.9/.NET 10.0.14 on Windows. Other platforms have not been tested.

From this folder:

```sh
sh verify-it-yourself/run_checks.sh
```

The final line must be `PASS`. On Windows, `python verify-it-yourself/check.py` runs the same checker without a shell. It recompiles the independent C# source in memory and enumerates the entire n=10 domain. The original independent run took about 20 seconds and used about 582 MB peak working memory; performance varies. A time or memory cap fails the check. No network access or package installation is required. The checker does not delete files or create output files in this package.

## Compared to

The [official DS6 source](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6), fetched 2026-11-04T18:12:23.972111Z with HTTP 200, returned the 2025-10-30 edition. Its windmill table leaves the two-clique conjecture stated generally. The directly checked historical obstructions do not exclude n=10. [PR 894](https://github.com/elder-plinius/V3R1T4S/pull/894) gives the adjacent n=8 decision and explicitly leaves p1; no earlier completed n=10 certificate was identified in the inspected publications, code, or release assets. Details and bibliographic limits are in `panel/novelty.md` and `the-record-we-beat/status.json`.

## Not claimed

No decision of the general conjecture, no new algorithm, no timing record, and no universal proof of absence of earlier publications. The original full texts of Levine 1983 and Liu 1994 were not obtained; the directly checked primary corroborations and remaining uncertainty are disclosed in the novelty review. Maintainers and outside researchers have not endorsed this contribution.

## Credits

- R. L. Graham and N. J. A. Sloane, [On Additive Bases and Harmonious Graphs](https://neilsloane.com/doc/RLG/073.pdf), including the note crediting E. Levine.
- J. A. Gallian, [A Dynamic Survey of Graph Labeling](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6).
- B. Liu and Z. Zhang, [On harmonious labelings of graphs](https://combinatorialpress.com/article/ars/Volume%20036/volume-36-paper-34.pdf), Ars Combinatoria 36 (1993).
- CharanRayudu, [PR 894](https://github.com/elder-plinius/V3R1T4S/pull/894), for the adjacent computation and pre-existing generic approaches. Both complement masks and direct backtracking are prior methods.
- Contributor: anonymous-a66f16aa. Programs and reviews were produced with Codex assistance. Independent review means separate model contexts and independently authored programs; all executions used the same local software environment.
