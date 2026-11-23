# Correction to the carried literature record, from this run's NOVELTY panel skeptic

`related_work-carried.md` (run 2026-11-20-0215's survey) lists the highest published Spearman for FLIP GB1
three-vs-rest as **0.8995 +- 0.0058** for ProtEGNN(t6). This run's NOVELTY skeptic (`../panel/novelty.md`) could
**not verify that number to four decimals** and found two gaps in the carried survey. Recorded here because it
bears directly on the full success criterion, which requires being "strictly higher than any published value for
the same split found by the novelty check":

1. What the ProtEGNN preprint's own prose says, quoted by NOVELTY from the source it opened: "Both ProtEGNN(t6)
   and ProtEGNN(ESMc-L) reach an SPR of 0.90, matching the best-performing 5.7B parameter Ankh3 model." So
   **two** models are reported at "0.90", not one, and the carried survey lists neither an ESMc-L value nor a
   four-decimal figure that NOVELTY could confirm. A value anywhere in [0.895, 0.905) rounds to 0.90, so a
   published number **above this run's 0.902852 cannot be ruled out**. The bioRxiv PDF is a compressed byte
   stream, the HTML renders those table cells as placeholders, and both OpenReview URLs served a
   browser-verification challenge, which NOVELTY correctly did not bypass and did not retry.
2. PLMFit's own Table 3 prints "0.9" at one decimal for ESM2-15B with LoRA and adapters, with no metric named.
   That is **not** a separate higher number: 0.8791 itself rounds to 0.9.

Ruled out as non-comparable by NOVELTY, with reasons: Ankh3's 0.9044 is the `sampled` split (6,291/670/1,772, not
this 2,691/299/5,743 one); arXiv 2501.18223's 0.905 is a train-set rho, its test value being 0.840; the FLIPv2
near-0.90 values are NDCG, not Spearman, and FLIPv2 adds no GB1 rows.

**Consequence, stated plainly: the full success criterion's "strictly higher than any published value" clause
cannot be established from the sources that could actually be read, so this run does not claim it.** The
published floor for a *language-model-free* model on this split is far below: FLIP's own one-hot ridge baseline
is 0.76, one-hot + Gaussian process 0.850 (Greenman et al. 2023), and Kermut's baseline GP 0.73-0.77.
