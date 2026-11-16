# PREREG.v3 — implementation refinements (timestamped; PREREG.md + PREREG.v2.md unchanged)

Frozen: 2026-11-16 13:5x UTC (`date -u`), after the observed-values computation and BEFORE
the first lens result is scored. The NULLS and THRESHOLDS are unchanged from PREREG/
PREREG.v2; only implementation details were fixed to match the published definitions:

1. H1 (edit-1 ratio) null: the within-line shuffle expectation in its EXACT unbiased
   form — E[# adjacent edit-1 pairs after shuffling a line of n distinct-order items]
   = (1/n) * sum_{a,b} n_a (n_b - [a==b]) * [lev1(a,b)] (random permutation: P(adjacent
   ordered pair (a,b)) = n_a (n_b - [a==b]) / n(n-1), times (n-1) adjacencies =
   n_a(n_b-[a==b])/(n) * ... — the factor is 1/n per the computation above). This is the
   unbiased estimator of the paper's 100-shuffle ratio; observed/expected reproduces the
   published Table-4 values exactly (A 1.197 vs 1.20; B 1.067 vs 1.07; IT2a A 1.238,
   B 1.066). The generator's H1 uses the same exact expectation on its corpus.
2. Latin plaintext: the pinned driver's EXACT `caesar_words()` output (De Bello Gallico
   I-IV, 20,547 words, 123,354 letters — identical to the driver's encryption input),
   split into 10 contiguous chunks L1..L10; Italian = Dante Commedia through Greshko's
   clean_line (28,871 words) split into 10 chunks I1..I10. Seeds, dialect assignment
   (L1-L5/I1-I5 -> A cells; L6-L10/I6-I10 -> B cells) and the 20x10=200-run grid are
   unchanged from PREREG §4/§5.
3. Line template: the per-P-line token counts of the FETCHED ZL3b-n.txt (4,130 lines,
   34,139 tokens) — the criterion's envelope corpus — rather than the driver's 3,950-line
   bundle file (which is a slightly older ZL3b extract). Both are the published control
   convention; the criterion says the envelopes are "computed at verification time from
   ZL3b-n.txt ... as then published", so the template is pinned to the fetched file
   (sha256 of the length list: b9cb5b81c4966ca4).
4. Grapheme inventory for S5-S8: the 58-grapheme inventory of 2604.19762's own code
   (signatures_v27 pools + bridge candidates; frozen in output/paper_graph_inv.json,
   sha256 dd8171a6...), used for BOTH the Voynich calibration and the generated corpora
   (the paper's tokenizer). S7 Voynich ZL3b observed 0.267/0.330 (A/B) vs the paper's
   0.5856/0.4980 on its RF1b-e corpus: cross-corpus consistency check only (per
   PREREG.v2 §3); the scored comparison is always generator-vs-Voynich on the same
   fetched corpus with the same inventory.
