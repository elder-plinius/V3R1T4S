id: minimizer-density-record-tables

## Why this target
Charter q3, weight 4. Live lead from the dossier: three runs measured an order
1.6% better than the published table, and the only thing blocking confirmation
was a mis-specified null test. The dossier prescribes the fix: make the density
deterministic by computing the EXACT density instead of estimating it on a random
sequence. This run does that, from the definition, and searches the whole 8!
space.

## Success criterion (verbatim from bank, repo/bank/targets.json)
"An explicit minimizer order for a stated (w, k) pair, given either as a complete rank file
or as deterministic released code that emits one, whose DNA density, computed by the skeptic
with the repositories' own density measurement code, is STRICTLY LOWER (direction: min) than
the smallest value listed for that (w, k) pair across the tables in
github.com/OrensteinLab/10-minimizers and the precomputed minimizers of
github.com/OrensteinLab/GreedyMini (both re-fetched live immediately before claiming) by at
least 0.5% relative, with the comparison made under the same density definition (expected
density for the expected-density tables, particular density on the same sequence otherwise)
and with the order's storage cost stated."

## Partial wins (verbatim from bank)
- p1: Beat the best listed density for a (w, k) cell with a constant-space scheme (no explicit table of k-mer ranks), which the WABI 2026 authors identify as the practically important regime.
- p2: Reproduce a published GreedyMini density for a mid-sized cell (w + k around 20) from scratch with your own search and release the order, confirming the table entry independently.
- p3: An exact computation (not sampling) of the density of a published order for a cell where only estimated values are listed, with the method and its error bound published.

## Target cell
w=12, k=3. Published best = 0.138843 (GreedyMini), from
k_extension_k16_w12.csv, re-fetched live this run, sha256 88c4f8fc...
Threshold: strictly lower by at least 0.5% relative, i.e. < 0.138148785.

## Rank definition
The published table is produced by OrensteinLab/10-minimizers, greedymini_density.ipynb
(sha256 19e5febb...). The order file w12_k3.gm (sha256 c592519b...) holds 8 entries
[8, 2, 8, 8, 0, 4, 1, 3]. The notebook's GreedyMiniScheme.get_minimizer maps a k-mer to
  (order[((kmer>>4)&1)<<2 | ((kmer>>2)&1)<<1 | (kmer&1)] << 2k) + kmer
i.e. the projection A=C=0, G=T=1. The notebook then computes rank = (function(km) << 8k)
+ get_kmer_id_dna(k, km, seed), and the table row is np.mean(densities) * (w+1).
The (w+1) factor belongs to the other table (greedymini_density_all_wtest24.csv); the
cell 0.138843 in k_extension_k16_w12.csv is already the density.

Reproduced this run: the notebook projection gives 0.1388271670 at n=2,000,000 seed 0,
against the published 0.138843. The GreedyMini README's two interleavings give
0.1402996582 and 0.1478376130, both wrong.

## Disclosure
open. No commit-only restrictions.
