context: hermes delegation (delegate_task)

# Reproduce skeptic verdict: FAIL

## Definition quoted (from claim/CLAIM.md success criterion)

"An explicit minimizer order for a stated (w, k) pair, given either as a complete rank
file or as deterministic released code that emits one, whose DNA density, computed by
the skeptic with the repositories' own density measurement code, is STRICTLY LOWER
(direction: min) than the smallest value listed for that (w, k) pair across the tables
in github.com/OrensteinLab/10-minimizers and the precomputed minimizers of
github.com/OrensteinLab/GreedyMini (both re-fetched live immediately before claiming)
by at least 0.5% relative, with the comparison made under the same density definition
(expected density for the expected-density tables, particular density on the same
sequence otherwise) and with the order's storage cost stated."

## Measurement definition (from claim/greedymini_density.ipynb)

The notebook's `random_density_function_dna_includes_tiebreaking` computes:

  rank = (function(km, w, k, seed) << 8k) + get_kmer_id_dna(k, km, seed)

where `function(km, w, k, seed)` for a minimizer order returns:

  (order[projection] << 2k) + kmer

so the full rank is:

  ((order[projection] << 2k) + kmer) << 8k + get_kmer_id_dna(k, km, seed)

The sequence is generated as:

  rng = np.random.default_rng(seed)
  nucleotides = rng.integers(0, 4, size=n_samples + w + k - 1, dtype=np.uint32)

with n_samples=10,000,000, w=12, k=3, seeds 0..4.

## Independent checker

Wrote my_checker.py from the notebook's definition (not from the author's code).
It implements two rank functions:
1. "notebook": the faithful notebook rank ((order[projection] << 2k) + kmer) << 8k + tiebreak
2. "checker_style": the author's rank (order[projection] << 2k) << 8k + tiebreak (omits + kmer)

Command: python3 my_checker.py

## Findings

### (a) Order file is a valid 8-entry permutation: PASS

order.txt contains [3, 4, 1, 0, 5, 6, 2, 7]. Sorted: [0,1,2,3,4,5,6,7].
This is a valid permutation of {0..7}.

### (b) Density measurement reproduces published GreedyMini value 0.138843: FAIL

Under the notebook's own rank function (with + kmer):

  GreedyMini seeds 0..4 mean density = 0.984363938763
  claimed order seeds 0..4 mean density = 0.984363938763

This does NOT reproduce the published cell 0.138843. The notebook measurement
gives density ~0.984 for BOTH orders (identical to 12 decimal places).

Under the checker-style rank function (without + kmer):

  GreedyMini seeds 0..4 mean density = 0.138865853361
  claimed order seeds 0..4 mean density = 0.136478296226

This DOES match the published cell (0.138865853361 vs 0.138843, within 0.017%
sampling noise). But this is NOT the notebook's measurement.

The discrepancy: the notebook's rank function includes "+ kmer" inside the
shifted term, i.e. ((order[projection] << 2k) + kmer) << 8k + tiebreak.
The checker omits the "+ kmer", computing (order[projection] << 2k) << 8k + tiebreak.
The "+ kmer" term (kmer << 24) dominates the tiebreak (0..4095), making the
notebook's rank ordering primarily determined by kmer within each projection
group. This yields density 0.984 (nearly every window has a unique minimum).
The checker's rank ordering is determined by the SHA-256 tiebreak hash, yielding
density 0.139.

### (c) Claimed order's density strictly below published cell by 0.5% relative: FAIL (under notebook measurement)

Under the notebook's measurement:
  claimed order density = 0.984363938763
  published cell = 0.138843
  The claimed order's density is 608.98% ABOVE the published cell, not below.

Furthermore, under the notebook's measurement, the claimed order's density is
IDENTICAL to GreedyMini's density (0.984363938763 = 0.984363938763).
The claimed order is NOT strictly lower than GreedyMini.

Under the checker-style measurement (not the notebook's):
  claimed order density = 0.136478296226
  published cell = 0.138843
  relative difference = -1.7031% (below by more than 0.5%)
  This passes, but only under the incorrect rank function.

### (d) Result is deterministic: PASS

Running the checker twice gives identical results (same sampled counts, same
densities). The computation is fully deterministic.

## Why the notebook and checker differ

For k=3, the notebook's rank for a k-mer with projection p and kmer value m is:

  rank = ((order[p] << 6) + m) << 24 + tiebreak

The tiebreak get_kmer_id_dna(3, m, seed) ranges from 0 to 4095.
The term m << 24 ranges from 0 to 1,056,964,608.
Since m << 24 >> tiebreak, the rank ordering within each projection group
is determined by m (the kmer value), not by the tiebreak hash.

The checker's rank is:

  rank = (order[p] << 6) << 24 + tiebreak = order[p] << 30 + tiebreak

Here the tiebreak (0..4095) is the sole ordering key within each projection
group, making the ordering pseudo-random and yielding a much lower density.

The CLAIM.md quotes the notebook's rank function as:

  rank = (order[((kmer>>4)&1)<<2 | ((kmer>>2)&1)<<1 | (kmer&1)] << 2k) + kmer

which includes "+ kmer". But the author's checker.py omits this term.
The claim's measured values (0.138865853361 and 0.136478296226) are reproduced
only by the buggy checker-style rank function, not by the notebook's.

## Verdict

FAIL. The claim states the measurement is the notebook's own, but the actual
computation uses a rank function that omits the "+ kmer" term. Under the
notebook's own measurement code:
- The density is 0.984, not 0.139.
- Both orders give identical density; the claimed order is NOT strictly lower.
- The claimed order's density is not below the published cell by 0.5%.

pass: false