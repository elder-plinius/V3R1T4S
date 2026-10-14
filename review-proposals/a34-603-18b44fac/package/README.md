# A(34,8,7) >= 603 | staging package, NOT YET ACCEPTED

## What

The explicit file `object/A34_8_7_603.txt` with SHA-256 `18b44fac5d5ff1d4895fd9de1240669eb71543b3e15599f7f864e090aa1491ad` contains 603 distinct binary words of length 34 and weight 7 with minimum pairwise Hamming distance 8, establishing A(34,8,7) ≥ 603.

This is a constructive lower bound, **not** a proof of optimality. The package is STAGING because three fresh-context role reviews pass, the current table response is captured, and historical preregistration compliance remains disclosed and unresolved. `panel/gate.md` correctly says `PROMISING` and does not authorize publication as a confirmed claim.

## Check it yourself

Run from the package directory in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final line: `PASS`. Python 3.10+ and `numpy` (for the upstream checker) are needed. The pure Python validator only needs the standard library. The pairwise check visits all 181,503 pairs, the support-subset check visits 21,105 subsets and the delta reconstruction is byte-for-byte. Should take seconds on a modern laptop.

## Compared to

| Cell | Source | Lower bound | This code | Difference |
|---|---|---:|---:|---:|
| A(34,8,7) | [V3R1T4S INDEX.csv](https://github.com/elder-plinius/V3R1T4S/blob/7aca3835635e5323b48cdf3b5b59fcde502cab28/known-knowns/bigger-codes/INDEX.csv) at `7aca3835635e5323b48cdf3b5b59fcde502cab28` | 602 | 603 | +1 |
| A(34,8,7) | [William Echols public code](https://github.com/williamechols/cwc-seeded-tabu-search/blob/4f0bf18b094fb15c3634001ea8aed847e8353d1c/codes/34_8_7_600.txt) | 600 | 603 | +3 |
| A(34,8,7) | [Brouwer live table](https://aeb.win.tue.nl/codes/Andw.html), viewed 2026-10-14T02:29:20Z | 601 [Bo] | 603 | +2 |

The independent reviewers checked the equivalent cell A(34,8,27), the named 2026 papers, newer literature and open repository PRs; their bounded public-source search found no subsuming construction. The `the-record-we-beat/` dossier preserves both results and evidence limitations.

## Not claimed

No optimality theorem, literature-wide priority, unpublished-work exclusion, novel general algorithm, three-skeptic panel approval, `CONFIRMED_*` status, maintainer endorsement or repository publication is claimed. The builder used the source project's already documented blocker-guided / plateau strategy, not an allegedly original algorithm.

## Credits

William Echols separately published a 600-word construction (checked as a published comparison, not as a direct construction parent). Jordan Boisclair constructed the credited 601-word seed `a34.8.7.601H`. A. E. Brouwer maintains the constant-weight-code table. The `elder-plinius/V3R1T4S` contributors produced the published 602-word construction and documented its large-neighborhood / plateau method. This 603-word extension was AI-assisted under the GitHub handle `rfreel`. Source commit `7aca3835635e5323b48cdf3b5b59fcde502cab28`. Please preserve these credits in any resulting submission.

## Current preparation status

Current raw table provenance is recorded in `the-record-we-beat/current_table.md`. See `how-we-built-it/PROVENANCE_CLARIFICATION.md` for the corrected, narrower historical procedure gap. A separate tested checker patch is included with the review deliverables. No upstream checker change or repository acceptance is claimed.
