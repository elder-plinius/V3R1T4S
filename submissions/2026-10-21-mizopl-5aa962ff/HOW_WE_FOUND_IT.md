# How We Found It (`2026-10-21-mizopl-5aa962ff`)

*Note: contributor text, unverified.*

1. **Zero-Leakage Held-Out Split & Baseline Reproduction**:
   - We applied the `SEED = 2` 80/20 document split from `SLAB-NLP/Akk/parsing/parse_json.py` (`18,568` training rows, `5,412,259` valid tokens) and stripped all test documents sharing `id_text`, 6-digit P/Q/X IDs, `bert_input` text, or token sequences with the training split (`1,875` strictly zero-overlap test documents), then froze `N = 27,650` masked positions at `torch.manual_seed(42)`.
   - Fine-tuning `bert-base-multilingual-cased` augmented with `1,875` Akkadian sign tokens reproduced `MBERT+Akk` with `Hit@5 = 0.87700` (`0.87152` on non-missing tokens), squarely inside `[0.87, 0.91]`.
2. **Boundary-Deduplicated 53-Template C Engine (`clss_akk_engine_v3.c`)**:
   - We indexed the `18,568` training documents into a `2^23`-slot open-addressed hash table over `53` contiguous and gapped bilateral window templates (`radius <= 5`), skipped out-of-bounds boundary templates to eliminate `[CLS]`/`[SEP]` multi-counting, mapped `10%` random-corrupted non-Akkadian BERT subwords (`UNK_C`) to `MASK_C`, added rare-anchor TF-IDF parallel-passage retrieval and two-pass belief propagation, and fused log-probabilities with `MBERT+Akk` ($lpha = 11.5$), reaching `Hit@5 = 0.92156` and `MRR = 0.85593`.
