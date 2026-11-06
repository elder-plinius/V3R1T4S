# LABS, L = 401: energy 10776 (merit factor 7.4611), below every published value

## What

The sequence in sequence_L401.txt is an explicit +-1 sequence of length 401 whose exactly computed integer energy E = 10776 is strictly below the minimum L = 401 energy over the criterion's named sources as archived in this package (11888, from the borkob/git_labs skew tables at commit 1aa1234, with the arXiv:2607.09688v1 and arXiv:2504.00987v2 tables and the 2026-10-24 arXiv search listing no L = 401 value), below every other published L = 401 value in the package (ERK'2025 Figure 2: 11000; arXiv:2206.12070: 11456; arXiv:2011.00068v1: 11472), and below every truncate-then-extend (up to 10 symbols) derivation of a verified package witness (lowest 11200).

This package contains one object only: `object/sequence_L401.txt` ('1' = +1, '0' = -1), sha256 e979ad4ab8b2de33a68d6700b89b83c9e227cc2a616c041f1ce4fb6969e1f8da. Its exact integer
energy is E = 10776, so F = 401^2/(2E) = 7.4611.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library only, under a second. It checks the object's sha256, length and
alphabet, recomputes C_k and E with integers, compares E with every value below, and confirms a corrupted copy is rejected.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Pšeničnik, Bošković, Brest, "Integer Partitions and the Merit Factor Problem", ERK'2025, Figure 2 | L = 401 | E = 11000 (F = 7.3091) | https://erk.fe.uni-lj.si/2025/papers/psenicnik(integer_partitions).pdf | 2026-10-24T20:21:40Z |
| Dimitrov, arXiv:2206.12070 | L = 401 | E = 11456 | https://arxiv.org/abs/2206.12070 | 2026-10-24T15:16:31Z |
| Brest & Bošković, arXiv:2011.00068v1 | L = 401 | E = 11472 | https://arxiv.org/abs/2011.00068v1 | 2026-10-24T15:18:39Z |
| Bošković et al. records archive (named in the bank criterion) | L = 401 | E = 11888 | https://github.com/borkob/git_labs/blob/1aa123407636e48630174e0bf122037e369c1d68/results-2018/2018-labs-skew.txt | 2026-10-24T15:12:34Z |
| arXiv:2607.09688 (bank status source) and arXiv:2504.00987 (named) | L = 401 | no value | https://arxiv.org/abs/2607.09688 | 2026-10-24T15:18:38Z |

The lowest trivial end-derivation of any public sequence is 11200. Details in `the-record-we-beat/`.

## Not claimed

- No optimality; only this one length.
- The ERK'2025 value at L = 401 is read from a figure, because the paper prints sequences only for L = 405, 422, 433, 441
  and 450. Our margin over it is 224 in energy (0.152 in F), far larger than the reading's uncertainty (about ±1 in energy).
- The sequence was found by search from random starts. It is not an end-extension or trimming of any published sequence:
  its minimum Hamming distance to Dimitrov's L = 401 sequence, over the 8 energy-preserving symmetries, is 160 of 401.

## Credits

- Credit for this result: Sherpa (https://github.com/shitcoinsherpa), found and checked with a V3R1T4S run.
- Blaž Pšeničnik, Borko Bošković, Janez Brest: ERK'2025 integer partitions (the value we beat), arXiv:2409.07222 with René
  Mlinarič (dual-step optimization), arXiv:2607.09688 with Jan Popič (partition-guided GPU walks).
- Miroslav Dimitrov: arXiv:2206.12070 (restriction classes and self-avoiding walks in the skew-symmetric space).
- Janez Brest and Borko Bošković: arXiv:2011.00068. Borko Bošković, Jana Herzog, Janez Brest: arXiv:2210.15962 (sokol_skew).
- Borko Bošković, Franc Brglez, Janez Brest: the LABS records archive and solvers (https://github.com/borkob/git_labs).
- Tom Packebusch and Stephan Mertens: exhaustive optima (arXiv:1512.02475). Zhiwei Zhang, Jiayu Shen, Niraj Kumar, Marco
  Pistoia: arXiv:2504.00987. José E. Gallardo, Carlos Cotta, Antonio J. Fernández: memetic tabu search (2009).
