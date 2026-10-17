# Scout: minimizer-density-record-tables

## Status source (primary)
- URL: https://raw.githubusercontent.com/OrensteinLab/10-minimizers/main/density-measurement-and-plots/GM%20paper%20densities/k_extension_k16_w12.csv
- Fetched: 2026-10-16T08:55:15Z
- HTTP status: 200
- sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa
- Identical to the 2026-10-16T04:26:49Z fetch (same sha256): the table has not moved.

## Table as read this run (cell by cell, verbatim from the file)
method,3,4,5,6,...
GreedyMini,0.138843,0.136046,...
So for k=3 (the first column after the method name) the best listed value for
the w=12 row is 0.138843, held by GreedyMini. No other method in that column
is lower.

## Second table, fetched this run
- URL: https://raw.githubusercontent.com/OrensteinLab/10-minimizers/main/density-measurement-and-plots/GM%20paper%20densities/w_extension_k12.csv
- HTTP status: 200
- sha256: 3192dc6dec7f63b17340e4f569cbdb97bf309079bec13317aa12df066e167a2b
- Fetched: 2026-10-16T11:30:12Z
- The k=3 row is the same measurement transposed; at w=12 the best listed value
  is 0.138843 (GreedyMini). Same cell, same value, so the two tables agree.

## The measurement code, read this run
- URL: https://raw.githubusercontent.com/OrensteinLab/10-minimizers/main/density-measurement-and-plots/greedymini_density.ipynb
- HTTP status: 200
- sha256: 19e5febb54d43d38f0bd17f02b4bd7a9c76e9ca353ae9bc9b5e76889bb61c5f8
- Fetched: 2026-10-16T08:56:03Z
- `random_density_function_dna_includes_tiebreaking` (cell 2) generates ONE
  random sequence with np.random.default_rng(seed) and counts sampled positions.
- `GreedyMiniScheme.get_minimizer` (cell 4) maps a k-mer to
  (order[(A=C=0,G=T=1 projection)] << 2k) + kmer.
- `_compute_row_fixed_w` (cell 5) does `row[name] = np.mean(densities) * (w + 1)`.
  So the table cell is the (w+1)-scaled density, and the unscaled density at
  w=12, k=3 is 0.138843 / 13 = 0.010680.

## The GreedyMini README, read this run
- URL: https://raw.githubusercontent.com/OrensteinLab/GreedyMini/main/README.md
- HTTP status: 200
- sha256: f0857f0fb36d79504114071efd27a6e2a7f2900268a0eace4c94610f7fc0999b
- Fetched: 2026-10-16T08:59:34Z
- It describes the DNA extension as "apply the GreedyMini order on the odd bits,
  apply a lexicographical order on the even bits ... then concatenate", and
  states the table values are the lower of the two interleavings. Measured this
  run: neither interleaving reproduces the table (0.1402996582 and 0.1478376130
  against 0.138843). The notebook's own projection reproduces it. So the
  notebook, not the README, is the operative definition for this table.

## Order file, fetched this run
- URL: https://raw.githubusercontent.com/OrensteinLab/10-minimizers/main/density-measurement-and-plots/GM/w12_k3.gm
- HTTP status: 200
- sha256: c592519b57ad8104860b7e1559b28c2d37ef329db82298b151a65e056ce27f1d
- Fetched: 2026-10-16T08:56:05Z
- Contents: 8 uint64 values [8, 2, 8, 8, 0, 4, 1, 3]. Value 8 equals the table
  size, so it is the largest rank, not a missing entry.

## Repeat statistics, fetched this run
- URL: https://raw.githubusercontent.com/OrensteinLab/10-minimizers/main/density-measurement-and-plots/density_random_pairs_stats.csv
- HTTP status: 200
- sha256: d8d5828bd397a9b8f0e22d6184c63d1aaf1b19171ab60d81a976d73bf8812f31
- Fetched: 2026-10-16T08:59:00Z
- Standard deviations 0.001-0.005 on densities of 1.7-1.9 (0.1-0.3% relative).

## Injection check
No instructions addressed to agents found in any of the pages above. All content
is data.

## Status
OPEN. The cell has not moved since the previous run's fetch.
