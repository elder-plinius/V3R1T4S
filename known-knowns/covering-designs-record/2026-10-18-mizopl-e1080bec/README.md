# C(94,13,5) <= 125,184: explicit (94,13,5) covering design beating CR (129,203) and LJCR (129,337)

## What

An explicit (94,13,5) covering design in claim/design_94_13_5.txt (sha256 e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908) with 125,184 distinct 13-element blocks over {0..93}, exhaustively verified across all 54,891,018 5-subsets of a 94-set with zero uncovered 5-subsets, strictly improving on the Covering Repository plain (v,k,t) record of 129,203 (by 4,019 blocks) and the La Jolla Covering Repository record of 129,337 (by 4,153 blocks) for C(94,13,5).

To stay under the 1 MB per-file repository limit, the 4,704,754-byte design file is stored as five plain-text parts `object/design_94_13_5_part1.txt` through `object/design_94_13_5_part5.txt` (~940 KB each) whose concatenation is byte-for-byte `claim/design_94_13_5.txt` (`sha256 e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908`).

## Check it yourself

One command from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough laptop time: ~2.5 seconds with `numpy` (~60 seconds with pure standard-library Python). It runs positive and negative self-tests on the Fano plane $C(7,3,2)=7$, reassembles the five part files in `object/`, verifies the SHA-256 and structural validity (`125,184` distinct blocks of 13 strictly increasing points in `0..93`, above the Schonheim lower bound $L(94,13,5)=42,705$), and exhaustively checks that all $\binom{94}{5} = 54,891,018$ 5-subsets are covered (`uncovered=0`).

## Compared to

| repository | cell | our blocks (b) | live table value | improvement | URL | fetched (UTC) |
|---|---|---|---|---|---|---|
| Covering Repository (plain v,k,t archive) | C(94,13,5) | 125,184 | 129,203 | -4,019 (-3.11%) | https://coveringrepository.com/download_archive_vkt.aspx | 2026-10-18T09:40:05Z |
| La Jolla Covering Repository (LJCR v1.2) | C(94,13,5) | 125,184 | 129,337 | -4,153 (-3.21%) | https://dmgordon.org/covering-designs/ | 2026-10-18T09:40:05Z |

## Not claimed

- Only the single cell `C(94,13,5) <= 125,184` is claimed in this package (one cell per package).
- No lower-bound improvement is claimed: the Schonheim lower bound remains $L(94,13,5) = 42,705$.
- No claim is made that `125,184` is optimal; it is an explicit upper-bound construction that is 1-minimal (`0` redundant blocks under single-block deletion).

## Credits

- **Contributor:** [mizopl](https://github.com/mizopl).
- **Daniel M. Gordon** — La Jolla Covering Repository (https://dmgordon.org/covering-designs/, Zenodo https://doi.org/10.5281/zenodo.10779736, GitHub https://github.com/dmgordo/LJCR), whose component coverings for $v=47$ served as the starting ingredients.
- **Giovanni Acerbi** — Covering Repository (https://coveringrepository.com/), primary comparison table for $(v,k,t)$ coverings.
- **Daniel M. Gordon, Greg Kuperberg, and Oren Patashnik** — "New constructions for covering designs", *Journal of Combinatorial Designs* 3(4):269–284, 1995 (combining construction framework).
