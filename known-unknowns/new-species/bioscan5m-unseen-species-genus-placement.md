# BIOSCAN-5M: place DNA barcodes of unseen (placeholder-named) insect species in the right genus, beating BarcodeMAE+ (80.65%)

🦋 **Undescribed life** · standard · tractability ★★☆☆☆ · compute: laptop-hours to laptop-days (only the barcode metadata is needed, a few GB of the 156 GB dataset; alignment and k-mer methods run on CPU, transformer pretraining needs a GPU) · open as of 2026-11-13

## The problem

BIOSCAN-5M (Gharaee, Lowe, Gong, Millan Arias, Pellegrino, Wang, Haurum, Zarubiieva, Kari, Steinke, Taylor, Fieguth, Chang; NeurIPS 2024 Datasets and Benchmarks; CC BY 3.0) holds 5,150,850 insect specimens with images and COI DNA barcodes, the standard animal barcode of about 658 base pairs. Its open-world partition holds unseen species: specimens whose genus is named but whose species has only a placeholder name, which is how undescribed or not-yet-identified species appear in barcode libraries. The task is to put each unseen-species barcode in its correct genus using seen-species data. Query: the test_unseen split (3,401 distinct barcodes of 880 species in the BIOSCAN-5M paper; 3,396 query specimens after the BarcodeMAE+ data preparation); reference: the seen train split (118,051 distinct barcodes of 11,846 species; 117,991 in BarcodeMAE+). Best published genus accuracy, read on 2026-11-13: 80.65% by BarcodeMAE+ with a trained global [CLS] embedding and a genus cross-entropy loss during pretraining, scored by frozen-embedding 1-nearest-neighbour (Safari, Millan Arias, Lowe, Kari, Chang, Taylor; arXiv 2609.35877, 26 September 2026, Table 3). Earlier values: BarcodeMAE 69.0% (arXiv 2502.18405, February 2025), BarcodeBERT pretrained on BIOSCAN-5M 58.31%, and a BLAST baseline of 58.74% in the BIOSCAN-5M paper.

## What counts as a win

A method that assigns a genus to each query barcode, with the query and reference lists built by the data_split script of the BarcodeMAE+ repository (github.com/bioscan-ml/BarcodeMAE) from the test_unseen and seen train splits. Allowed labels: species and genus labels of the seen train split, and the genus labels already present in the unlabelled pretrain partition metadata, as BarcodeMAE+ used them; the seen val split may be used for model selection. Not allowed: BIN, species or other metadata of the pretrain partition, any label or metadata from key_unseen, val_unseen, test_unseen or other_heldout, and any external reference library such as BOLD or GenBank, which hold these specimens. Its genus accuracy over the query list, recomputed by the verifier from saved predictions, must be STRICTLY GREATER than 80.65% by at least 0.5 percentage points (at least 81.15%), as the mean over 3 seeds when training is random. It must also beat any higher value on the same split in a paper from the last 24 months found by the novelty check. Deliverables: code, seeds, saved per-barcode predictions and the reference and query lists.

## Partial wins

- **p1:** A method with no learned parameters (for example global alignment nearest neighbour, or phylogenetic placement on a tree of seen-species barcodes) whose genus accuracy under the same rules is above 69.0% (BarcodeMAE, arXiv 2502.18405).
- **p2:** Frozen-embedding 1-nearest-neighbour genus accuracy above 68.76% (the best BarcodeMAE+ configuration without any genus-supervised auxiliary loss, encoder-decoder with CLS, token embeddings, arXiv 2609.35877 Table 17) from a model pretrained only self-supervised, with no genus or species labels used before the probe.

## How a win is checked

The skeptic downloads the BIOSCAN-5M metadata (Hugging Face or Zenodo), rebuilds the query and reference lists with the BarcodeMAE+ repository's data_split script and checks them against the supplied lists, recomputes accuracy from the saved predictions, inspects the training inputs for unseen-split labels, pretrain-partition species or BIN labels and external libraries, and retrains one seed.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://export.arxiv.org/api/query?search_query=all:BIOSCAN&sortBy=submittedDate&sortOrder=descending&max_results=40>

## Sources

- <https://arxiv.org/abs/2406.12723>
- <https://huggingface.co/datasets/bioscan-ml/BIOSCAN-5M>
- <https://github.com/bioscan-ml/BIOSCAN-5M>
- <https://arxiv.org/abs/2609.35877>
- <https://arxiv.org/abs/2502.18405>
- <https://github.com/bioscan-ml/BarcodeMAE>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Genus membership is a tree question: placing each query on a phylogeny of seen-species barcodes and taking the genus of the smallest enclosing clade can beat nearest-neighbour rules when a genus is not monophyletic at the nearest hit.
- Combine an alignment distance with a learned embedding: alignment is strong for close relatives, embeddings for distant ones.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Papers count this task differently: the BIOSCAN-5M paper reports BarcodeBERT at 23.15% while arXiv 2609.35877 reports 58.31% for BarcodeBERT pretrained on BIOSCAN-5M; only the protocol stated here (BarcodeMAE+ query and reference lists) counts.
- BOLD, GenBank and BIOSCAN-1M contain the same specimens with species names; using any of them as a reference or for supervised training leaks the answer.
- The pretrain partition (about 2.28 million barcodes) may contain conspecific barcodes of unseen species, and about 15.9% of it carries genus labels; BarcodeMAE+ used those genus labels, so they are allowed for parity, but BIN and species fields are not.
- A novelty check that searches arXiv only for the exact string BIOSCAN-5M misses some entries (for example BarcodeMamba+, arXiv 2512.15931); search for BIOSCAN as well.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/new-species/bioscan5m-unseen-species-genus-placement.md
```

Already set up? Say `run V3R1T4S on bioscan5m-unseen-species-genus-placement`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `bioscan5m-unseen-species-genus-placement`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
