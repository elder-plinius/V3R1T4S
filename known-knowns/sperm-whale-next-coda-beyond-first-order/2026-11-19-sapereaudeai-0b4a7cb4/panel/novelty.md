# NOVELTY verdict: sperm-whale-next-coda-beyond-first-order, FULL success criterion

context: subagent (Claude Code Agent tool, novelty type)

Reviewer saw only `claim/` (CLAIM.md, PREREG.md, PREREG.v2.md, REPRODUCE.md, baseline/README.md), the pinned
repo copy (TROPHY_CASE.md, known-knowns/, the bank entry) and the web sources below. Every fetch was one plain
request with a User-Agent naming V3R1T4S and a timeout. Each response is saved in its own numbered subfolder of
`panel_work/novelty/` (entries 01 to 36). The GitHub REST API was not used. injection_suspected: none seen. No page
I read addressed instructions to agents.

## Status source (fetched once)

- URL: https://export.arxiv.org/api/query?search_query=abs:%22sperm%20whale%22&sortBy=submittedDate&sortOrder=descending&max_results=25
- HTTP 200, 40,549 bytes, fetched 2026-11-19T10:22:25Z (`date -u`), sha256
  1d1a18b7520dbb62d3416d2e8a45e0c0d01378ed080bc6d5929f0fc849c4e94f. This is byte-identical to the scout record in
  CLAIM.md (09:37:53Z).
- What it shows: 16 entries. The newest are 2610.33974v2 (published 2026-10-25, updated 2026-11-17, Sinha and Chavan),
  2610.29101v1 (2026-10-21, contrastive coda encoder for unit/type/identity classification), 2609.20350v1 (PAMGuard
  localiser errors), 2609.16612v3 (updated 2026-11-17, Sinha and Chavan), 2609.12593v1 (click-train diarization),
  2606.16084v5 (updated 2026-11-17, Sinha and Chavan), then 2512.02206v1 (WhAM) and older ones. No entry reports a
  held-out next-coda result on sperm-whale-dialogues.csv under the bank's tokens, folds and scored set. The
  2610.29101v1 abstract is about classification ("social unit, coda type, and individual identification ... On
  1,383 codas"), not sequence prediction.

## The decisive finding: an earlier public claim in the same cell (V3R1T4S PR #1159)

- Pull-request search https://github.com/<owner>/V3R1T4S/pulls?q=is%3Apr+whale (HTTP 200, 2026-11-19T10:33:14Z)
  lists "Open 2, Closed 0": #1175 (opened Nov 19, 2026, "[claim] sperm-whale-next-coda-beyond-first-order:
  turn-taking p4, 0.780268 vs 0.850317 bits") and #1159 (opened Nov 18, 2026). The search `is:pr coda` (HTTP 200,
  10:35:01Z) adds only an unrelated tsunami PR (#736).
- PR #1159 (draft, opened 2026-11-18; page HTTP 200, 10:33:49Z; files page HTTP 200, 10:39:15Z) claims this
  target's FULL criterion on the same benchmark: "[claim] sperm-whale-next-coda-beyond-first-order: order-3
  forecaster 2.564371 bits/coda vs R1 2.794781 and one-coda twin 2.850952 (3,418 positions)", with "a fresh paired
  recording-bootstrap 95% interval of 0.241386 to 0.345250 bits for the gain over the twin". Its disclosures say
  "A standard order-2 or order-3 n-gram clears the benchmark's thresholds on this data". They also report an
  independent re-derivation: "an order-3 n-gram 0.266 bits below its own R1 ... and 0.251 below a well-tuned one-coda
  twin". Its protocol text matches the bank cell: "Dialogue grouping is REC, sorted lexically and assigned modulo
  five. Order within REC by numeric TsTo with file order breaking ties ... Duration cutpoints are training-only
  linear quantiles; use right insertion for ties. Alphabet is 50 physically defined tokens. Score from the third
  coda onward." Its model families were interpolated n-gram backoff, repetition-aware backoff (capped run lengths,
  prior distinct token) and timing backoff. The selector "chose the interpolated three-coda context in each fold".
- Consequence: the qualitative FULL result, a frozen held-out model on these dialogues that beats R1 by at least
  0.10 bits and its own one-coda twin by at least 0.05 bits with a REC-bootstrap interval above 0, was already
  publicly claimed one day before this claim (unverified, unmerged draft). This claim is not the first public filing
  of the FULL thresholds.
- Comparison with the known in-cell object. Same 3,418 scored positions. The two packages describe the same streams,
  folds, 50-token alphabet and training-only linear-quantile bins, so the model cross-entropies are on the same
  token sequences.
  - This claim's model: 2.1238 bits per coda, against #1159's 2.564371. That is 0.4406 bits lower, so strictly
    better.
  - Gain over R1: 0.6563 here against 0.2304 there.
  - Gain over the own one-coda twin: 0.5311 [0.4571, 0.6325] here against 0.2866 [0.2414, 0.3453] there. This
    claim's twin (2.6549) is a stronger comparator than #1159's twin (2.851, which is worse than R1).
  - Not derivable from #1159's order-3 n-gram by deletion, restriction, relabelling or a local numerical polish. This
    claim is a log-linear tilt with skip-bigram, coda t-2 identity, run length, stream caches, tempo-trend and
    whale-switch features, and it lowers cross-entropy by 0.44 bits, far more than smoothing changes to an n-gram
    can give. Nothing in `claim/` shows it was seeded from #1159.
  - Under kit POLICY rules 4 and 5, a strictly better value is not blocked by an earlier open PR in the same cell
    (rule 5 blocks only a later PR that "matches or is beaten by" the earlier one), and the bank marks condition (1)
    "direction: min".
- R1 discrepancy, flagged for REPRODUCE and CRITERION. On the same positions #1159 reports R1 = 2.794781 (alphas
  0.3, 0.1, 0.1, 0.3, 0.3; "pooled inner cross-validation, respecting REC groups and refitting boundaries"). This
  claim reports R1 = 2.7802 (alpha 0.3 in every fold; leave-one-training-fold-out, bins from the 4 training folds).
  The bank's "inner cross-validation on the training folds" leaves this convention open. The 0.0146-bit difference
  does not affect the model-to-model comparison above or either threshold here.

## Other sources checked, and what each says about this exact result

1. Sinha and Chavan, arXiv 2606.16084v5 (HTML, HTTP 200, 10:23:02Z): a different corpus and different tokens.
   "We begin with recordings and click annotations from the publicly shared sperm-whale audio collection linked by
   Gubnitsky and Diamant ... 63 recordings provide 1,952 coda crops". The units are encoder-defined whole-coda forms.
   "The second preceding form adds 0.1812 bits/coda (segment-bootstrap 95% CI [0.1250,0.2405]..." on 1,478 targets
   in 114 segments. But against the strict segment-local reference it gives "lift −0.00609 bits, p=0.5908", and a
   run-preserving control leaves "0.0016 with whole-source holdout". The file sperm-whale-dialogues.csv is not used,
   and the paper holds no equivalent number on the DTag dialogues.
2. Sinha and Chavan, arXiv 2609.16612v3 (HTML, HTTP 200, 10:23:28Z): the same Gubnitsky and Diamant collection
   ("1,952 annotated coda crops from 63 recordings"). Primary order-2 minus order-1 "+0.0279 bits/event for Whale
   ... [−0.0069,+0.0805], includes zero". Not these data, and no equivalent number.
3. Sinha and Chavan, arXiv 2610.33974v2 (HTML, HTTP 200, 10:23:43Z): the same collection ("63 sperm-whale
   recordings from the publicly shared SpermWhales collection"). "At 32 states, the gain is 0.090 bits per target
   ... [0.020,0.143]. The exact test across four conservative source pools gives p=0.0625". Against an
   adjacent-pair-preserving reference: "0.0156 bits ... p=0.080 after correction". Not these data, and no
   equivalent number.
4. WhaleLM, bioRxiv 2024.10.31.621071v1 (full text, HTTP 200, 10:24:04Z) and v2 (HTTP 200, 10:31:14Z; posted
   November 11, 2024; footnote "The title change was not reflected the first time the manuscript was submitted").
   It uses the DTag DSWP data ("comprising 3948 codas"), its own tokenizer ("rhythm, tempo, rubato, and
   ornamentation ... as well as the time elapsed since the preceding coda in the exchange, and the identity of the
   vocalizing whale"), and 10-fold day-held-out CV. It states "Removing order information from inputs increases
   perplexity ... by up to 22.7%" and "Short contexts (containing 6 or fewer preceding codas) substantially reduce
   the predictability ... (by up to 20.6%)". On availability: "The code will be made available upon publication".
   - Figure 2 (image F2.large.jpg, HTTP 200, 10:24:45Z) does plot perplexity on absolute axes. Read off the plot,
     Fig. 2B(ii) falls from about 53 at T = 2 to about 43.5 at T = 8, and Fig. 2D gives about 52 for the n-gram and
     about 44 for the LSTM. The context axis starts at T = 2, so no single-previous-coda condition is plotted.
   - So WhaleLM qualitatively reports held-out dependence beyond the last codas on (a version of) these DTag
     recordings. But it uses a different, larger vocabulary that also predicts timing and speaker, different folds,
     no tabulated values and no code. It is not the bank's cell, gives no comparable bits-per-coda number, and
     cannot be turned into this claim by trivial edits.
   - Correction needed: CLAIM baseline/README.md says WhaleLM "reports only relative perplexity changes". In fact it
     plots absolute perplexities, under its own tokenization only.
5. WhaleLM, NeurIPS 2025 workshop. The OpenReview PDF https://openreview.net/pdf/c994ef85af328c42d526b99077d5eccc581dfa2c.pdf
   was REFUSED with HTTP 403 at 10:27:58Z; not retried, and unread. The NeurIPS virtual page
   https://neurips.cc/virtual/2025/131495 returned 302 at 10:28:16Z; I followed the redirect once and got HTTP 200
   at 10:28:30Z. It shows only the abstract ("vocalizations exhibit order dependence and long-range dependencies on
   up to eight previous codas") and an OpenReview link, with no code link. The authors' homepage
   (first author's GitHub Pages site, https://<owner>.github.io/, HTTP 200, 10:28:54Z) lists WhaleLM as "bioRxiv, 2024" with a paper link
   only and no code link. Weighing: the workshop abstract describes the same study as the preprint, with WhaleLM's
   own tokens. Even if the unread PDF tabulated perplexities, they would not be in the bank's cell.
6. Sharma et al., Nature Communications 15:3617 (PMC11076547, HTTP 200, 10:25:30Z). There is no next-coda
   predictive model and no held-out cross-entropy. It has the sequence-level statistic "rubato is sustained across
   sequences of multiple codas" (tempo-drift correlation r = 0.57) and describes "Dataset 2, a smaller set of 3948
   codas ... recorded from animal-borne DTags". There is no equivalent number.
7. The data repository github.com/<owner>/sw-combinatoriality:
   - The main page, commits, code tree and releases all returned HTTP 200 (10:25:53Z to 10:27:27Z).
   - The main-branch head is commit 7228c8e (2024-03-05), the commit the claim used.
   - The code folder holds only the paper's seven notebooks (1-exchange-plot through 7-supplementary-extra). There
     is no sequence or language model.
   - There is one release, tag "sw-combinatoriality" (14 Mar 2024, commit 7228c8e). Its "Assets 2" are only the
     auto-generated source zip and tar.gz (expanded_assets, HTTP 200, 10:26:50Z).
   - So the repository's releases do not add anything that its tree lacks.
8. whale-coda-dynamics, a 2026 MSc group project on GitHub (repo page HTTP 200, 10:29:45Z; reports/README.md HTTP
   200, 10:30:15Z; docs/data_dictionary.md HTTP 200, 10:30:40Z). This is the closest neighbouring cell.
   - Data and tokens: held-out (14 leave-one-day-out folds) bits per coda on 1,547 targets from the Assayag et al.
     (2026) DSWP release, not on sperm-whale-dialogues.csv. The data dictionary says the dialogues file "shares
     recording/onset combinations with 2,788 rows of the Assayag file ... The temporary reference file was not
     merged". The tokens are named coda types, and the inputs are the whale's own and its partner's histories.
   - "Run length, recent distinct types and repertoire, all together | +0.052 [0.023, 0.099], 13/14 days, p = 0.008"
     beyond a three-own-coda logistic model.
   - "Order of earlier types beyond the repertoire | +0.013 [0.002, 0.027], ... p = 0.053".
   - "Nine instead of three own codas ... +0.009 [−0.014, 0.037]". The authors conclude "This is not clear evidence
     of switching structure beyond ornaments."
   - So it is a different data release, labels, streams and folds: not this exact result, and its numbers are not
     comparable. It is prior art for stream-level (repertoire and run-length) gains, and the claim should credit it
     next to its `rep` and `local` decomposition.
9. Bond, "Geometric Structure in Sperm Whale Communication", bioRxiv 10.64898/2026.03.11.711226v1 (HTTP 200,
   10:36:13Z; posted March 13, 2026; also on Zenodo, 2026-07-19). It uses the dialogues file ("3,840 entries with
   rhythm type labels"). "Trigram prediction accuracy (71.2%) exceeded bigram accuracy (66.1%), demonstrating
   higher-order sequential structure". The accuracy is "computed as the proportion of transitions correctly
   predicted by the most common successor", with no held-out split for this test. So it is in-sample accuracy on
   rhythm types, not a held-out probabilistic result, and not this cell.
10. Assayag et al. (2026, Bioacoustics). Code repository page (HTTP 200, 10:35:57Z): one notebook with GMM-HMM, LSTM
    and Transformer models for dyadic prediction of the next coda's continuous features from the partner's
    sequence, on their own DSWP release. A different task and different data.
11. whale-gpt (GitHub, HTTP 200, 10:32:20Z): an experimental transformer that generates dialogues from a re-encoded
    file. It reports no held-out comparison with a first-order model.
12. NESS-code (GitHub page HTTP 200, 10:32:35Z; notebook HTTP 200, 10:38:17Z): in-sample plug-in entropies on the
    dialogues file ("whalesNES: 0.2140", a first-order normalised entropy slope). No held-out model, and no
    published paper found.
13. CET-002, an issue in another GitHub project (HTTP 200, 10:35:43Z): a plan only. "No cetacean dataset has been
    downloaded or scored".
14. phys.org, 2026-10-23, "How to speak whale: AI uses eight to ten click sequences to predict sperm whales'
    feeding dives". REFUSED with HTTP 403 at 10:31:49Z; not retried, and unread. A search-engine summary (not the
    page) describes Project CETI dive-behaviour prediction. I could not check whether it reports a next-coda
    cross-entropy, but nothing points to a bank-cell number.
15. General search:
    - arXiv API `abs:coda AND abs:whale` (HTTP 200, 10:36:45Z): 7 results, all already listed above.
    - arXiv API `all:"sperm whales" OR all:codas` (HTTP 200, 10:36:59Z): nothing new and relevant.
    - Zenodo `"sperm whale" AND coda`: my first request was malformed (HTTP 400, page size above 25); the corrected
      request returned HTTP 200 at 10:37:33Z with 11 records. The relevant 2026 records, read from their metadata
      only:
      - "Sperm Whale Coda Communication ..." (first-order "mutual information = 0.195").
      - "Immediate A-B-A rhythm and tempo continuity ..." ("post-hoc ... not evidence of syntax, memory", a zip
        not opened).
      - An "ordering-provenance audit" of a 1,483-coda corpus.
      - "From Coda Categories to Temporal Operators" (speaker-switch prediction).
      None reports a held-out next-coda cross-entropy under the bank's tokens.
    - Web searches turned up the repositories above and nothing else in the cell.
16. This repo:
    - TROPHY_CASE.md (pinned copy) has no whale or coda entry. The live copy (raw file, HTTP 200, 10:40:15Z) is
      byte-identical.
    - known-knowns/ in the pinned copy has no folder for this target. #1159 would add
      known-knowns/sperm-whale-next-coda-beyond-first-order/ but it is not merged.
    - The bank entry (status_checked 2026-11-13) says "no public, reproducible held-out result shows that a sperm
      whale's next coda depends on more than the previous one". That is no longer true of public claims since
      #1159 (2026-11-18).

## Judgement

- Is this exact result already public? Not as stated. No public source has a model at or below 2.1238 bits per coda
  in this cell, or a twin gain near 0.53 bits.
- But the FULL thresholds were already publicly claimed in this cell by PR #1159 (2026-11-18, 2.564371 bits,
  unverified draft). Neighbouring cells (WhaleLM on its own DTag tokens; whale-coda-dynamics on the Assayag
  release; Sinha and Chavan on audio-derived forms; Bond in-sample) already report, with mixed strength, that the
  next coda carries information beyond the previous one.
- This claim strictly beats every known value in its cell (2.1238 < 2.564371, a 0.4406-bit improvement). It is not
  a tie. It is not obtainable from a published object by trivial edits, and it is not seeded from one. Under the
  kit's rule ("Pass only if the result strictly beats everything known") it is new as a record improvement, not as
  first evidence.
- This pass covers novelty only. It assumes the claimed values are reproduced by REPRODUCE.

Required before any filing (disclosure, not optional):
- Name PR #1159 (filed 2026-11-18, order-3 n-gram at 2.564371 bits; R1 2.794781; twin 2.850952) as the first public
  claim of the FULL thresholds. Say that this claim's novelty is the strictly lower cross-entropy and the larger
  twin gain.
- Explain the R1 difference (2.7802 here vs 2.794781 there) as an inner-CV convention difference, or fix whichever
  one departs from the bank text.
- Correct baseline/README.md. A public in-cell value now exists (#1159), and WhaleLM's figures do plot absolute
  perplexities under its own tokens.
- Credit whale-coda-dynamics (stream-level run-length and repertoire gains on overlapping DSWP recordings) and Bond
  2026 (in-sample higher-order accuracy on the dialogues file) as neighbouring prior work.
- Record the two unread secondary sources (OpenReview PDF 403, phys.org 403).

pass: true
