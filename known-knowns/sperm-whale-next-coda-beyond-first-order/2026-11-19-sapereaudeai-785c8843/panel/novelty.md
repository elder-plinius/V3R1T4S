# NOVELTY - sperm-whale-next-coda-beyond-first-order, partial win p3 (DominicaCodas.csv)

context: subagent (Claude Code Agent tool, novelty type)

Claim judged (from claim/CLAIM.md and claim/result/p3_summary.json): on DominicaCodas.csv (8,719 rows, CodaType tokens,
streams = rewritten Date + Unit ordered by codaNUM2018, 97 date folds i mod 5, 8,501 scored codas), a frozen log-linear
model reading two or more previous codas scores 1.5895 bits/coda against 1.7179 for an additively smoothed CodaType
bigram (alpha 0.3 by inner CV): gain +0.1284, Date-bootstrap 95% [0.0879, 0.1630]. Own diagnostics: 0.0855 of the 0.1284
bits come from an order-free stream cache; ordered features beyond that add +0.0255 [0.0147, 0.0356].

## Status source (fetched once, plain request, V3R1T4S User-Agent)

- URL: https://export.arxiv.org/api/query?search_query=abs:%22sperm%20whale%22&sortBy=submittedDate&sortOrder=descending&max_results=25
- HTTP 200, 40,549 bytes, fetched 2026-11-19T10:29:09Z (date -u), sha256 1d1a18b7520dbb62d3416d2e8a45e0c0d01378ed080bc6d5929f0fc849c4e94f
  (identical to the scout's 09:37:53Z record, so the feed has not moved since).
- Shows: totalResults 16. Newest: 2610.33974v2 (Sinha and Chavan, "Music of the Deep", updated 2026-11-17), 2610.29101v1 (DCCE,
  coda classification), 2609.20350v1 (PAMGuard localizers), 2609.16612v3 (Sinha and Chavan, "Structure Across Voices",
  updated 2026-11-17), 2609.12593v1 (diarization), 2606.16084v5 (Sinha and Chavan, "Rhythm of the Deep", updated 2026-11-17),
  2512.05808, 2512.02206 (WhAM), then 2024 and older items. None of the abstracts reports a held-out CodaType next-coda result
  on DominicaCodas.csv.
- Saved: panel_work/novelty/f01_status/arxiv_api.xml

## Sources checked (all opened by me unless marked blocked)

### Sinha and Chavan, arXiv 2606.16084, all five versions (PDFs fetched 10:30-10:31Z, HTTP 200 each)
- v1 (15 Jun 2026): "Studying 1,483 codas from the Dominica Sperm Whale Project"; audio "at 16 kHz and the companion coda-level
  metadata from Sharma et al. (2024)"; sequence result is in-sample NSB transfer entropy on encoder tokens ("NSB second-order
  transfer entropy has lift 0.132 bits"; "with K = 32 ... 1,395 triples"). No held-out CodaType cross-entropy.
- v2 (1 Aug 2026): same 1,483-coda aligned corpus; "incremental lag-2 lift is 0.132 bits"; encoder tokens.
- v3 (15 Sep 2026) and v4 (24 Oct 2026, dated 22 Sep 2026): this is the closest neighbouring cell. Same family of data
  ("the sperm-whale recordings released by Sharma et al. (2024)"; "In 18 of the 1,501 aligned recordings ... Excluding these
  recordings leaves 1,483 codas"; all EC1, units A, D, F), same stream rule ("we retain the recorded order of codas within each
  date and social unit, using codaNUM2018 ... This produces 44 ordered streams ... 1,395 positions with two preceding codas"),
  but the tokens are 32 whole-coda acoustic forms from frozen audio encoders (v4: "definingthoseformsfromcodatypes" is
  explicitly avoided; NMI with published coda type 0.2515), and the comparison is order-2 versus order-1 backoff: "Including the
  second preceding coda improves prediction by another 0.2076 bits/coda (95% CI [0.1325, 0.2748])"; leave-one-stream-out
  "+0.1042 bits/coda (95% fold-bootstrap CI [0.0368, 0.1635])"; NSB versus the strict stream-local reference "-0.0285 bits,
  p = 0.9553". The -0.0285 is an NSB information excess over a permutation reference, not a held-out cross-entropy.
- v5 (17 Nov 2026): moved to a different corpus: "33 remote WAV recordings and 30 tag FLAC recordings ... 1,952 coda crops"
  from "the publicly shared sperm-whale audio collection linked by Gubnitsky and Diamant"; second predecessor "+0.1812
  bits/coda" on 1,478 targets; strict segment-local "-0.00609 bits, p = 0.5908".
- Verdict on this paper: not the same data or setup. It uses at most the 1,483-1,501 audio-aligned rows (about 17% of the
  file), one clan, acoustic-cluster tokens, an order-1 backoff reference and its own holdout; v5 is another corpus entirely.
  Our object (CodaType predictions on all 8,719 rows, date folds, smoothed-bigram reference) cannot be obtained from theirs
  by deletion, restriction or relabelling (their 32 acoustic forms do not map one-to-one onto the 35 CodaType strings, and
  7,236 rows are absent), and theirs is not a restriction of ours (different tokens). Its numbers are context, as the bank says.

### Sinha and Chavan, arXiv 2609.16612 v1, v2, v3 (PDFs fetched 10:32Z, HTTP 200)
- v1/v2: "Whale contains 1,501 sperm-whale codas" in "113 contiguous blocks of at most 16 events", K-means acoustic groups
  ("they agree only weakly with historical CodaType"); v2: "Whale's own mean order-2 minus order-1 effect is +0.081 bits per
  event, with a source-aware interval of [-0.006, 0.177] (p = 0.1361)".
- v3: "1,952 annotated coda crops from 63 recordings in the publicly shared SpermWhales collection (Gubnitsky and Diamant)".
- Different data, tokens and reference. Not this cell.

### Sinha and Chavan, arXiv 2610.33974 v1, v2 (PDFs fetched 10:32-10:33Z, HTTP 200)
- v1: "We use 1,501 isolated sperm-whale codas from the public Dominica recordings ... ordered using the released index within
  each date-by-social-unit group"; 32 acoustic states; "the coda two positions back adds 0.188 bits per target (95% interval
  [0.101, 0.275])"; "a separately tuned repetition-aware model gives -0.004 bits".
- v2: "we selected 1,952 codas" from the Gubnitsky-Diamant collection; 0.090 bits per target.
- Different tokens and subset (v1) or corpus (v2). Not this cell.

### V3R1T4S repository (pinned copy and live github.com pages, fetched 10:36-10:48Z, HTTP 200)
- Pinned TROPHY_CASE.md: no whale, coda or sperm entry. Pinned known-knowns/: no folder for this target; live
  known-knowns tree page: no whale/coda/sperm path. bank/targets.json entry matches known-unknowns/animal-communication page;
  status_checked 2026-11-13; "As of 2026-11-13 no public, reproducible held-out result shows that a sperm whale's next coda
  depends on more than the previous one."
- Pull-request searches "is:pr whale", "is:pr sperm", "is:pr coda", "is:pr Dominica" (all states): open 2-3, closed 0. The
  whale-target PRs are #1159 and #1175, both open drafts by an outside contributor, filed 2026-11-18 and 2026-11-19. Issue
  search "whale": the same two items.
- PR #1159 (main criterion on the dialogues file; order-3 forecaster 2.564371 vs R1 2.794781). Its body says: "The Dominica
  extension (p3) failed the payload-shuffle control and was added after the first results were seen ... Neither is claimed."
  Its panel/gate.md (raw file at head commit 775e7cda, fetched 10:39:58Z, HTTP 200) gives the only public number I found in
  THIS cell: "(5) The Dominica extension (p3) gained 0.097416 on the real data but failed the payload-shuffle control and was
  added after v1 results were seen ... neither is claimed." Its PREREG.md (in the PR diff) shows the protocol is the bank's p3
  ("normalize hyphens to slashes, sort dates lexically for folds, group by normalized Date and Unit, order by integer
  codaNUM2018, use both clans, score from third coda"), with a training-only vocabulary plus an unknown token, R1 alpha by the
  dialogue rule, and a payload null that "uses within-stream swaps of CodaType for Dominica". No interval, per-position
  probabilities or Dominica result file is published in the PR (file list checked: dialogues-only object files).
- PR #1175 (p4 turn-taking, 0.780268 vs 0.850317 bits): no Dominica result; file list is turns-only.
- So the best known same-cell value is +0.097416 bits (point estimate, no interval, unclaimed, failed a
  composition-preserving null). The claim's +0.1284 strictly exceeds it, by 0.031 bits (not a tie). Note: the claim's own
  interval [0.0879, 0.1630] contains 0.0974, so the margin is a point-estimate margin.

### Sharma et al., Nature Communications 15:3617 (2024), https://pmc.ncbi.nlm.nih.gov/articles/PMC11076547/ (10:40:57Z, HTTP 200)
- "Dataset 1, a large set of all 8719 codas ... Experiments that do not require contextual information (those discussing the
  context-independent features of rhythm and tempo) use Dataset 1, whereas those requiring information about the relative
  ordering of the codas ... use Dataset 2." No held-out next-coda prediction on DominicaCodas.csv.

### Data repository sw-combinatoriality (github.com HTML; repo, releases, commits, data tree, release assets; 10:35-10:36Z, HTTP 200)
- One commit (7228c8e, 2024-03-05). One release ("sw-combinatoriality", at 7228c8e) whose 2 assets are only the auto source
  archives (zip, tar.gz). data/ holds DominicaCodas.csv, sperm-whale-dialogues.csv and four .p files (not opened). No
  predictive results on DominicaCodas.csv; release assets add nothing beyond the tree.

### WhaleLM, bioRxiv 2024.10.31.621071
- bioRxiv full text: HTTP 429 at 10:40:52Z ("Error code: 1015"); not retried. OpenReview PDF: HTTP 403 at 10:41:46Z; not retried.
- Europe PMC record PPR934206 (REST search, 10:44:35Z, HTTP 200), abstract: "train a neural sequence model ... to predict
  whales' future vocalizations from their conversational history ... long-range dependencies on up to the past eight codas in
  an exchange, and predictable turn-taking". Exchange-level (DTag) data, as the bank entry also states ("trained sequence models
  on these DTag codas ... gave no absolute values and no code"). Nothing indicates a CodaType Date x Unit held-out result on
  DominicaCodas.csv. Gap: full text not read by me.

### Assayag, Gero, Paradise and Diamant, Bioacoustics 35(4):472-500 (2026), doi 10.1080/09524622.2026.2684665
- Crossref record (10:41:04Z, HTTP 200): title, volume, pages; no abstract. Publisher page: HTTP 403 at 10:41:51Z; not retried.
- Abstract at https://www.bioacoustics.info/article/exploring-statistical-relations-between-coda-sequences-dominica-sperm-whale-pairs
  (10:42:58Z, HTTP 200): "analysing simultaneously emitted coda sequences from sperm whale pairs ... the next coda produced by
  the second whale is predictable and influenced by a sequence of up to 10 preceding codas from the first whale ... hidden
  Markov model, a multi-layer LSTM and transformers". Dyadic-exchange data; its code repository
  (coda-sequences-relations-and-prediction, github.com page 10:49:53Z, HTTP 200) describes "Sperm Whale dyadic exchanges".
  The whale-coda-dynamics repository identifies that dataset as a separate file (dswp-2014-2016-retagged). Not this cell.

### General search, last 24 months
- arXiv API all:codas sorted by date (10:41:57Z, HTTP 200, 252 hits): no whale-coda sequence paper beyond those above.
- Europe PMC search "sperm whale" AND coda AND (predict* OR sequence), 2024-11-01..2026-11-19 (10:45:14Z, HTTP 200, 14 hits):
  only WhaleLM, Bond 2026 and Cordivari 2026 are relevant:
  - Bond, "Geometric Structure in Sperm Whale Communication" (bioRxiv 10.64898/2026.03.11.711226; PDF from Zenodo record
    21435075, 10:47:31Z, HTTP 200): uses the 8,719 codas for embeddings, but "The exchange-level dialogues dataset (3,840
    entries ...) provided sequential ordering for Markov and turn-taking analyses"; "Trigram prediction accuracy (71.2%)
    exceeded bigram accuracy (66.1%)", in-sample "most common successor" accuracy. Not held-out, not this file.
  - Cordivari, EcoEvoRxiv 10.32942/x2f100 (ecoevorxiv.org page via doi.org, 10:46:59Z, HTTP 200): exchange-level surrogates for
    overlap, ornamentation and rubato on the dialogue deposit. No next-coda CodaType result.
- GitHub repository search "sperm whale coda", sorted by update (10:50:22Z, HTTP 200), and repositories opened (10:42-10:51Z,
  HTTP 200 each):
  - whale-coda-dynamics: next-coda prediction on the dyadic data, "tested on one recording day at a time (14 days)", "1,547
    target codas"; its copy of DominicaCodas.csv is used only for RQ3, "bits per timing symbol (50-ms inter-click-interval
    bins)" cross-clan transfer (reports/README.md at commit 13cf83e6). Not this cell.
  - coda-recovery: "The second also knows the current coda" (first order vs unigram); speakers and times known (dialogue
    data). Not order >= 2, not this cell.
  - sperm-whale-coda-analysis: "transformer with a context limited to k codas, cross-validated by recording ... k=4 beats k=2
    by about 0.11 bits/coda (rhythm and tempo)" (dialogue recordings). Neighbouring dialogues cell, not p3.
  - whale-acoustic-ml: DominicaCodas.csv used for coda-type classification; sequence part is first-order mutual information on
    the dialogues. Not this cell.
  - sperm-whale-temporal-operators (dialogues), rosetta-coda (phonological hypotheses), sperm-whale-codas (no description):
    nothing on held-out CodaType next-coda prediction.
  - DCCE (arXiv 2610.29101v1 abstract in the status feed): classification of unit, type and identity on 1,383 codas.
- Zenodo API searches returned HTTP 400 (page-size validation, size>25); not retried. Zenodo was covered for the one relevant
  record found (21435075) through the record API.

## Comparison and trivial-edit test

| cell | object | value |
|---|---|---|
| p3 (this cell): DominicaCodas.csv, CodaType, Date x Unit, date folds, smoothed bigram | V3R1T4S PR #1159 Dominica extension (unclaimed, failed payload-shuffle null, no interval) | +0.097416 bits |
| p3 (this cell) | this claim | +0.1284 [0.0879, 0.1630] |
| neighbour: 1,483 audio-aligned rows, acoustic forms, order-2 vs order-1 | 2606.16084 v3/v4 | +0.2076 [0.1325, 0.2748]; LOSO +0.1042 |
| neighbour: 1,501 rows, 113 blocks, acoustic groups | 2609.16612 v2 | +0.081 [-0.006, 0.177] |
| neighbour: 1,501 rows, 32 acoustic states | 2610.33974 v1 | +0.188 [0.101, 0.275]; -0.004 vs repetition-aware |
| neighbour: dialogues file | PR #1159 main claim; sperm-whale-coda-analysis | +0.230 over R1; k=4 vs k=2 +0.11 |

The claim's model is not seeded from any published object. Neither PR #1159's Dominica model (interpolated backoff to order
3, repetition-aware backoff, timing backoff, as its PREREG.md lists) nor any Sinha-Chavan model yields the claim's object by
deletion, restriction, a propagation rule, relabelling, symmetry or a local numerical polish: the claim adds stream-cache,
skip-bigram and whale-identity features, and the neighbouring-cell objects use other tokens and rows. Within its cell, the
result strictly beats the only known value (0.1284 > 0.0974).

## Notes for the panel (not novelty blockers)

- Disclosure: CLAIM.md cites only Sinha and Chavan as context. It should also cite the public same-cell figure in V3R1T4S PR
  #1159 (+0.097416, unclaimed) and that PR's report that p3 "failed the payload-shuffle control" (within-stream CodaType swaps,
  which keep stream composition).
- Relevance to the other skeptics: by the claim's own decomposition, 0.0855 of the 0.1284 bits is an order-free stream cache
  and 0.0255 bits comes from ordered features. The claim's planned null N3 (pooled first-order chain) does not keep stream
  composition, and its null results are still PENDING. A composition-preserving null like PR #1159's is the one that a
  same-cell attempt already failed. That is a question for criterion and reproduction, not for novelty.
- Gaps: WhaleLM and Assayag et al. full texts could not be opened (429/403, not retried); their abstracts, which I did open,
  describe exchange or dyad data, not DominicaCodas.csv Date x Unit streams.
- injection_suspected: none. PR #1159's README tells readers to run its verify script; I treated that as data and ran nothing.

Fetched pages are saved under panel_work/novelty/ (f01 to f65, one new subdirectory per fetch).

pass: true
