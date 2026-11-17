# How we found it (contributor text, unverified)

Second V3R1T4S run on the bank target cryptic-tb-resistance-beat-who-catalogue. Run 1 split the isolates by Mykrobe
lineage labels; an end-of-run audit with CRyPTIC's SNP-distance matrix showed that split was not cluster-aware (17
12-SNP clusters spanned it), and its p2 attempt (a resistance-gene L1 model on ethionamide) showed no leakage.

This run first rebuilt the WHO-catalogue look-up on MUTATIONS_GPI.csv.gz (indel lengths, codons, filter-fail calls)
and checked it against CRyPTIC's released catalogue calls (all 13 drugs >= 99.5% agreement). It then froze a new
split from the distance matrix alone: 12-SNP single-linkage components with no hub removal, the one 2,539-isolate
hub-chained component kept in TRAIN, and whole components drawn to TEST by a salted hash until 25%. No TRAIN isolate
is within 12 SNPs of any TEST isolate.

The p2 model was chosen to expose the trap the bank describes: a genome-wide nearest-neighbour model that only knows
genomic relatedness. Model, metric, drug (ethionamide, run 1's p2 drug), the 400 random control splits and the pass
rule were written in PREREG.md before any p2 number existed. The result: 0.3496 on the cluster-aware split against
0.5135-0.6678 on every random split; 100 alternative cluster-aware splits stayed at 0.18-0.47.

What did not work in the same run: a catalogue-plus-residual model beat the WHO catalogue for INH on the frozen rule
only through filter-fail calls at katG S315, and lost against a stricter reading of those calls fixed before it was
computed; the EMB gain of run 1 did not hold its specificity on the new split; only 3 of the 10 candidate variants p3
needs replicated. A three-skeptic panel (fresh subagents) reviewed the p2 claim. Nothing here is clinical advice.

The first panel round's REPRODUCE skeptic failed the claim on one control: the code tested the frozen "<= 5% of
negatives" rule in floating point, so a split with exactly 5% of negatives tied at a threshold was handled as "< 5%"
(seed 333: 0.584375 instead of 0.5875). The test was rewritten in integers, the full run repeated (no headline number
changed) and a second REPRODUCE and CRITERION round passed (panel/, panel/round1/, how-we-built-it/REPAIR.md).
