# Akkadian: restore masked/damaged signs in Oracc/eBL transliterations, beating the Lazar et al. 2021 held-out benchmark with frozen predictions

🏺 **Ancient texts and fragments** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-08

## The problem

Lazar, Saret, Yehudai, Horowitz, Wasserman and Stanovsky (EMNLP 2021, arXiv 2109.04513) framed filling gaps in Akkadian transliterations as masked language modelling on about 1M words / 2.3M signs scraped from Oracc. Their best model (MBERT+Akk, greedy decoding) reports hit@5 = 0.89 and MRR = 0.83 on a 20% held-out split with 15% random masking. These are token-level (BERT word-piece) scores: the paper says 'Table 2 compares token level evaluation', and the repository's evaluate_bert.py masks and scores each word piece separately (positions with label_ids != -100); multi-sign and word prediction is evaluated separately (its Figure 3). They released code and the scraped data (github.com/SLAB-NLP/Akk, MIT, data/akk_from_jsons.jsonl 21 MB, last commit 2022-11-10). The paper's split is a random 80/20 split by text (about 8K train / 2K test texts, its Table 1). The code fixes the seed (preprocessing/main_preprocess.py: SEED = 2, train_test_split(test_size=0.2, random_state=SEED)), but it splits a fresh Oracc scrape written to data/raw/akk_jsons.jsonl, which is not in the repository; the shipped data/akk_from_jsons.jsonl is not referenced by the code and holds 23,211 records, more than Table 1 reports, so the paper's exact test set is not known to be reproducible. The shipped data file (data/akk_from_jsons.jsonl, 21.2 MB, repository commit dfd2a66d of 2022-11-10) is the frozen corpus. Vetter re-check 2026-10-08: two literature searches found no later work reporting hit@k/MRR on this task (later Akkadian work is NMT: Gutherz et al. 2023, TabletCraft 2026). The real-world task is restoring the editorial gaps ('x', [...]) that remain unrestored in Oracc and eBL editions; eBL alone has 625,844 transliterated lines, a large fraction containing bracketed editorial restorations that can serve as a natural held-out test.

## What counts as a win

On the SLAB-NLP/Akk released data (data/akk_from_jsons.jsonl at commit dfd2a66d or a later recorded commit), with an 80/20 split by text and the 15% random masking of the repository's evaluate_bert.py reproduced with a documented fixed seed, the frozen list of masked positions published (hash) before any model is trained, and masked units being whole whitespace-delimited transliteration tokens (words) scored by exact string match as in the repository's single-token evaluation: (1) the claimant retrains the paper's MBERT+Akk baseline with the repository code and default hyperparameters on the same frozen split and freezes its top-5 predictions (hash) - its hit@5 must land within 0.02 of 0.89 on the frozen masked positions, otherwise the split is not comparable and no full win is possible; (2) a prediction file (top-5 per masked token) for the new system, frozen (hash) before scoring and trained/tuned ONLY on the training split, scores BOTH hit@5 and MRR strictly above the paper's values (re-read from the arXiv/ACL paper immediately before claiming) AND strictly above the reproduced baseline on the identical masked positions. Any use of test documents, of eBL/Oracc texts that duplicate test documents (same P/Q number or same composition), or of a corpus fetched after the split was frozen voids the claim.

## Partial wins

- **p1:** Same protocol as the full criterion (including the reproduced baseline), beating only hit@5 or only MRR by at least 1 absolute point over both the paper's value and the reproduced baseline; or beating both metrics on a genre subset for which the paper reports a per-genre number (re-read from the paper's per-genre table/figure; genre defined by Oracc project as in the paper).
- **p2:** Natural-lacuna holdout: a permanent held-out set of at least 2,000 editorially restored signs (text inside [ ] in eBL fragments with joins == [] and no corpus-chapter manuscript link, sampled by a published deterministic rule from fragments fetched on a recorded date, hashed before training) is masked and predicted with frozen top-5 predictions. All training material must exclude any line sharing 6 or more consecutive signs with the 20-sign context window around any holdout gap (parallel/duplicate exclusion, re-checked by the verifier). hit@1 at least 0.50 and hit@5 at least 0.75, with BOTH a unigram-frequency baseline and a k-NN retrieval baseline over the filtered training set reported alongside and beaten by at least 20 absolute points on hit@1.

## How a win is checked

The verifier re-creates the split and masks from the published seed/rule on the recorded data commit, checks the hashes of both frozen prediction files (baseline and new system) against the hashes committed before training (timestamps from the pre-registered holdout protocol), rescores hit@k/MRR for both with independent code on the identical masked positions, and checks that no test document or duplicate (same Oracc P/Q number, composition, or eBL museum number) appears in the training material. Rescoring is minutes; the verifier never retrains.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/SLAB-NLP/Akk>

## Sources

- <https://github.com/SLAB-NLP/Akk>
- <https://arxiv.org/abs/2109.04513>
- <https://ar5iv.labs.arxiv.org/html/2109.04513>
- <https://www.ebl.lmu.de/api/statistics>
- <https://oracc.museum.upenn.edu/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Character/sign-level n-gram or small transformer LMs trained from scratch on signs (not words) with genre tags; the 2021 model was a word-level MBERT fine-tune and never used sign-level context.
- Retrieval-augmented restoration: Akkadian royal inscriptions and omens are highly formulaic, so k-NN over duplicate passages in the training split can restore many gaps exactly.
- Ensemble a forward and backward sign LM with a lexicon constraint (only attested sign sequences for the word), which directly targets MRR.
- Build the natural-lacuna holdout (p2) from eBL bracketed restorations, stratified by genre and gap length, and seal it before any training.
- Report per-gap-length curves; long gaps dominate the real editorial need and are where the 2021 model fails.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The 2021 split is produced by code (SEED = 2) on a fresh Oracc scrape, not shipped as files; a different scrape yields a different test set. Only the reproduced-baseline control makes a beat meaningful.
- Massive duplication in Oracc (parallel manuscripts of the same composition, RINAP duplicates) leaks test text into training; deduplicate by composition/Q number or report leakage.
- data/akk_from_jsons.jsonl repeats records: 5,666 id_text values occur 2 to 5 times (8,781 extra records; 8,691 lines are exact repeats), although the repository's scraper skips an id_text it has already written. Splitting this file as the repository's --do_preprocessing path does (preprocess_akk_file keeps all 23,211 records in order, then train_test_split(test_size=0.2, random_state=2)) gives 18,568 train / 4,643 test records and puts a byte-identical copy of 2,606 of the 4,643 test documents (56.1%) in training. The repository's evaluation (main_bert.py --do_eval) then scores only test documents whose id_text is neither in training nor earlier in the test file: it drops 2,761 (2,616 with the id_text in training, 145 repeats within the test set) and scores 1,882. Remove repeated records (same id_text) before splitting, or apply the same id filter, and report how many were removed.
- Exact-match filters do not remove composition-level duplicates. Under the SEED = 2 split, dropping the test records whose id_text, 6-digit P/Q/X id, text or word-piece sequence also occurs in train leaves 1,875 documents (the test set of claim PR #611). Of the 1,755 with at least 8 words, 131 share half or more of their word 8-grams with the training records, and 25 share 90% or more. For 18 of those 25, a single training record holds at least 90% of the 8-grams. Some test texts are largely covered by a composite text (Q number) in train: P229143 (19 words) shares 10 of its 12 distinct 8-grams with Q002268. Measured 2026-10-22 over bert_input words; a verifier can compute the same share for every test document before accepting a claim.
- Editorial restorations are themselves often made from parallels: hit rates on bracketed text overstate performance on truly unknown gaps.
- LLM-judged 'plausibility' of restorations is not a criterion; only frozen top-k predictions scored against held-out text count.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/ancient-texts/akkadian-lacuna-restoration-heldout.md
```

Already set up? Say `run V3R1T4S on akkadian-lacuna-restoration-heldout`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `akkadian-lacuna-restoration-heldout`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
