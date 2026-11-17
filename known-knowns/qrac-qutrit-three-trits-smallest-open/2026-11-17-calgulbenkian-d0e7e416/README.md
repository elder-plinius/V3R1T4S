# Exact Rational General-POVM Upper Bound `ASP(3,3,3) <= 4368312591/6250000000 <= 0.6990` (`qrac-qutrit-three-trits-smallest-open`, `p1`)

## What

The shipped rational dual certificate, verified exactly in Fraction arithmetic and independently confirmed numerically on random operators, proves ASP(3,3,3) <= 4368312591/6250000000 = 0.69893001456 <= 0.6990 for all states and all 3-outcome POVMs on C^3 via a Naimark-dilation relaxation that assumes no projectivity of the physical measurements, which meets enumerated partial win p1 only and does not meet criterion (b) (< 0.69853) or (a).

## Check it yourself

From this package folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (runs in ~1.5 seconds on a single laptop core using < 40 MB RAM).

## Compared to

- **Status source**: https://arxiv.org/abs/2312.14142 (`v3`, *Quantum* 9, 1643, 2025)
- **Target cell**: `(n, d, D) = (3, 3, 3)` average success probability upper bound valid for general (non-projective) POVMs (`p1`)
- **Prior values**: `0.71823` proven general-POVM analytic bound (Corollary 1); `~0.699` floating-point plot without exact certificate (Figure 2, Pauwels et al. *PRL* 129, 250504, 2022); `0.69853` floating-point QDimSum bound assuming projective measurements
- **Fetched**: `2026-11-16T19:42:27Z` (`HTTP 200`, SHA-256 `b835ab5c9c7fbcc4bf93936a3560f4d9c33439dedfc8f76859e4bb524f91fbd5`)

## Not claimed

- Main criterion `(b)` (`ASP(3,3,3) < 0.69853` for all POVMs) and main criterion `(a)` (`ASP(3,3,3) >= 0.69716`) remain open; only enumerated partial win `p1` (`ASP(3,3,3) <= 0.6990` valid for general POVMs via an exact rational SDP dual certificate) is claimed.

## Credits

- **Mate Farkas, Nikolai Miklin, and Armin Tavakoli** (*Quantum* 9, 1643, 2025, https://arxiv.org/abs/2312.14142, https://github.com/nikolai-miklin/qrac_bounds).
- **Jef Pauwels, Stefano Pironio, Erik Woodhead, and Armin Tavakoli** (*Phys. Rev. Lett.* 129, 250504, 2022, https://arxiv.org/abs/2208.07887).
- **Miguel Navascues, Adrien Feix, Mateus Araujo, and Tamas Vertesi** (*Phys. Rev. X* 5, 041010, 2015) and **Denis Rosset** (`QDimSum`).
