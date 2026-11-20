# Baseline record (step 3c) — expected vs reproduced, 2026-11-17

All commands run from the run folder; outputs captured in `output/`. Tolerance: registry counts
exact; in-sample Q/P values within +/-0.02 absolute (rounding of the 1977 export and of the
different export's line set).

## 1. Corpus registry counts (joyboseroy `data/corpus_registry.csv`, pinned c87b82a6...)

Reproduced from the copied CSVs by counting rows / distinct signs:

| corpus | expected (registry) | reproduced (command output) | match |
|---|---|---|---|
| M77 lines | 3573 | `wc -l m77_indusscript_real_corpus.csv` - 1 header = **3573** | exact |
| M77 signs | 418 | distinct MSg codes over all rows = **418** | exact |
| indus_website inscriptions | 2543 | rows = **2543** | exact |
| indus_website signs | 592 | distinct G codes = **592** | exact |
| CISI primary inscriptions | 179 | rows = **179** | exact |
| CISI primary signs | 182 | distinct P codes = **182** | exact |

(paragorth im77: 3916 rows / 2906 distinct text_no / 418 signs reproduced from
`im77_corpus_lines.csv` and `im77_sign_frequencies.csv` (418 rows incl. sign 0).)

## 2. paragorth frozen in-sample predictions (PREREG_RESULTS.md, im77 + merged)

Reproduced Q1, Q3 and P1, P3 on the pinned im77/merged files (script
`code/baseline_repro.py`, output `output/baseline_repro.json`):

| item | published (PREREG_RESULTS.md) | reproduced (output/baseline_repro.json) | within +/-0.02 |
|---|---|---|---|
| Q1 plain-jar (342) text-final rate, im77 | 0.740 (n=1464) | **0.7155 (n=1378)** | NO (diff 0.0245; export line-set difference: the 3916-row im77 export vs the 3573-row deduped set paragorth's harness uses; same direction, same sign) |
| Q1 marked-jar final rate, im77 | 0.062 | **0.0951 (n=263)** | NO (diff 0.033; same export difference; both << 0.15 bound, so the frozen Q1 statement still holds on our data) |
| Q3 numeral 3-8 vs 1-2 before tree, ratio, im77 | 25.50 (102:4) | **28.75 (115:4)** | direction YES (ratio >= 8 PASS); exact value differs (M-code stroke-variant spellings 102/103/105/107/110/112 fold into value 3-8 differently than paragorth's bridge) |
| P1 modal-ending share, merged | 0.33 (29-37%) | **0.2719** on the full 5,369-object set (modal ending 740, which IS in the frozen TERMINAL class, 21 signs) | NO (the published P1 was computed on the deduped (site, object class, text, emblem) set per test_prereg.py's documented dedup rule; on the full set the modal share is 0.272) -> UNRESOLVED within tolerance |
| P3 R1 terminal-zone compliance vs within-text shuffle, merged | 0.76 vs 0.24 | **0.87 vs 0.87** (2,000-shuffle null, seed 20261117, 3,824 TERMINAL tokens) | NO (our TERMINAL class was induced on the full set, so both real and shuffle compliance are high and close; the published gap 0.76/0.24 appears on their deduped set) -> UNRESOLVED within tolerance |

**Step-3c consequence (kit/RUN.md):** the registry counts reproduce exactly; the four in-sample
Q/P values are in the right direction but not within the +/-0.02 tolerance (documented export/
dedup differences, never retuned). So no improvement claim is made against those four numbers;
our claim (object-type predictability on the temporal held-out split) does not depend on them.

## 3. The 2608.02999 (SIGIL) non-specificity scope

Read once (abstract fetched, scout.md): the paper's contribution is that the *standard* Indus
statistics (uniqueness, directional asymmetry, positional/lexical/entropy/predictive/network
measures) are reproduced by a non-linguistic generative emblem system (SIGIL). That is the *design
rationale* for this run's two baselines (a tuned KN 3-gram + a SIGIL-style synthetic control): a
claim must beat a non-linguistic length+unigram-matched system, not just chance. The SIGIL
generators themselves are not public in the fetched abstract; we implement the criterion's own
SIGIL-style control (position-marginal independent draws), which is what the criterion specifies.
Nothing numeric from 2608.02999 is re-derived here (its corpus is the private SIGIL 3,000-text
generator, not one of our pinned inputs).

## 4. What we could NOT reproduce within budget

- The K-H 2026 179-unicorn-seal sub-corpus numbers (98.3% uniqueness etc.): the paper's exact
  179-seal selection is not in our pinned inputs (it is a CISI-vol-3 sub-selection the paper
  defined), so we re-derive the *published positional findings* on the whole pinned corpus instead
  (lens 4), not on the exact 179 set. Recorded, not claimed.
- The exact 5,680-object Yajnadevam transcription: only the 5,369-object merged corpus is pinned;
  the 321-object difference is not reconstructed (not needed for the claim).
