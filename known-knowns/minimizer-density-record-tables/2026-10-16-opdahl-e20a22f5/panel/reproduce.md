context: hermes delegation (delegate_task)

# REPRODUCE verdict

## Composed rank expression read from the notebook (quoted)

Cell 2 (`random_density_function_dna_includes_tiebreaking`):
    shift_8k = 8 * k
    ranks = [
        (function(km, w, k, seed) << shift_8k) + get_kmer_id_dna(k, km, seed)
        for km in kmers
    ]

Cell 4 (`GreedyMiniScheme.get_minimizer` → `_fn`):
    return (rank_train << (2 * k)) + kmer

Composed rank the notebook specifies:
    rank = (((order[bin_kmer] << (2*k)) + kmer) << (8*k)) + get_kmer_id_dna(k, km, seed)

where bin_kmer uses the HIGH-bit projection (bit = (nuc >> 1) & 1, i.e. bits 5,3,1 for k=3).

## Measured densities (n=2,000,000, seeds 0,1,2)

Composition (i) — notebook's composition (WITH +kmer, high-bit projection):
    GreedyMini  mean density = 0.138882000041
    Claimed     mean density = 0.136644513466

Composition (ii) — same but with `+kmer` dropped from _fn:
    GreedyMini  mean density = 0.138791000587
    Claimed     mean density = 0.136585347155

Author's checker approach (low-bit projection, no +kmer) — for reference:
    GreedyMini  mean density = 0.138843000275
    Claimed     mean density = 0.136447347983

## Which composition the notebook specifies

The notebook specifies composition (i): WITH `+kmer` and HIGH-bit projection.
The author's checker.py uses a DIFFERENT composition (low-bit projection, no `+kmer`).

The previous attempt's finding of 0.984 for both orders does NOT reproduce under any
composition tested here. All compositions give ~0.1388 for GreedyMini, matching the
published table value 0.138843. The previous attempt's error was ignoring the
`order[p] << 30` term which dominates across projection groups; the `m << 24` term
only matters within the same projection group and cannot produce density 0.984.

## Order file validation

order.txt = [3, 4, 1, 0, 5, 6, 2, 7]
  Valid 8-entry permutation of [0..7]: YES

w12_k3.gm (GreedyMini incumbent) = [8, 2, 8, 8, 0, 4, 1, 3]
  Valid 8-entry permutation of [0..7]: NO (8 appears 3 times; 3,5,6,7 missing)

## Determinism

Deterministic: YES (two runs with seed 0 at n=100,000 gave identical density 0.138593368796)

## Claim judgment

Smallest table value for (w=12, k=3) in k_extension_k16_w12.csv:
  angle-based: 0.138389448 (smallest)
  GreedyMini:  0.138843

Under the notebook's composition (i):
  Claimed order density = 0.136644513466
  Threshold (0.5% below smallest) = 0.138389448 * 0.995 = 0.137697500760
  Claimed < threshold: YES
  Relative improvement vs smallest: -1.2609% (exceeds 0.5% margin)

## Command run

  cd panel && python3 my_checker.py

pass: true
