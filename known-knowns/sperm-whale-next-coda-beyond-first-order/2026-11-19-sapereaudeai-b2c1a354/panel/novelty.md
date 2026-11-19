# NOVELTY review: partial win p4 (turn-taking), sperm-whale-next-coda-beyond-first-order

context: subagent (Claude Code Agent tool, novelty type)

Reviewer scope: I read only the claim package (CLAIM.md, PREREG.md, PREREG.v2.md, REPRODUCE.md, baseline/README.md,
result/p4_summary.json, result/run_output.txt, result/p4_per_position.csv), the pinned V3R1T4S repo copy
(TROPHY_CASE.md, known-knowns/, the bank entry and its known-unknowns page) and public sources. Each source was fetched
once with plain curl, a User-Agent naming V3R1T4S and a timeout. I did not retry any refusal and did not log in. I took
no outward action. Fetched pages are saved under panel_work/novelty/, one numbered subdirectory per fetch. Times are UTC.

Claim under review: pooled held-out log-loss 0.7631118 bits per coda for same-or-switch of the whale label at the 3,418
scored positions, against 0.8503174 for the smoothed first-order same/switch reference. Gain +0.0872055, REC bootstrap
[0.0649, 0.1166]. The model was frozen at 2026-11-19T09:55:11Z (PREREG.md).

## Status source (fetched once)

- URL: https://export.arxiv.org/api/query?search_query=abs:%22sperm%20whale%22&sortBy=submittedDate&sortOrder=descending&max_results=25
- HTTP 200 at 2026-11-19T10:16:39Z (`date -u`). Saved as panel_work/novelty/01_status_arxiv_api/page.xml, sha256
  1d1a18b7520dbb62d3416d2e8a45e0c0d01378ed080bc6d5929f0fc849c4e94f. This is byte-identical to the scout's 09:37:53Z
  fetch quoted in CLAIM.md.
- What it shows: totalResults 16, and 16 entries. The newest are 2610.33974v2 (updated 2026-11-17), 2610.29101v1,
  2609.20350v1, 2609.16612v3 (updated 2026-11-17), 2609.12593v1 and 2606.16084v5 (updated 2026-11-17). After those come
  2512.05808v1, 2512.02206v1 (WhAM) and older items, down to 1602.02369v1 (myoglobin, off-topic).
- No returned abstract reports a held-out same-or-switch or next-speaker prediction. Only one abstract touches turns at
  all: 2609.12593v1, "Audiovisual diarization of overlapping click trains in sperm whale ... vocal sparring". It is about
  attributing clicks to emitters ("reconstructed and assigned 11 distinct, intertwined click trains"), not about
  predicting turns.

## The decisive comparison: a prior public claim on this exact cell exists, and this claim strictly beats it

- V3R1T4S pull request #1175 is an open draft by another contributor, created 2026-11-19T09:59:53Z: "[claim]
  sperm-whale-next-coda-beyond-first-order: turn-taking p4, 0.780268 vs 0.850317 bits". I found it through the github.com
  HTML search pages (panel_work/novelty/14, 15, 23, 24). Its README says: "predicts adjacent speaker-label equality at
  3,418 eligible positions with 0.780267728 bits per position versus 0.850317354 for the smoothed first-order
  same-or-switch reference, improving by 0.070049626 bits with a positive REC-bootstrap interval". Its
  object/turns-result.json gives CI95 [0.05347, 0.09153], fold gains 0.0607 / 0.0634 / 0.1213 / 0.0482 / 0.0763, and
  per-fold reference alpha 1.0 / 0.01 / 1.0 / 0.01 / 1.0.
- That PR became public 4 min 42 s after this claim's freeze. So this claim's model cannot have been seeded from it, and
  the "must name it" rule for seeded objects does not apply. The two models also come from different families. #1175
  uses an interpolated categorical backoff over the binary switch sequence with run-length context (campaign.py; 116
  distinct probability values over 3,418 positions). This claim uses a logistic regression on 21 continuous
  history features, including gaps and overlaps (3,418 distinct values). Their correlation is 0.908 and the mean
  absolute difference is 0.084.
- Paired check on identical positions. I fetched #1175's five per-fold files from its head commit 8949ab62, and their
  sha256 values match the PR's SHA256SUMS. I read them with zipfile and numpy.lib.format.read_array(allow_pickle=False),
  so no pickle was loaded. I aligned them with this claim's result/p4_per_position.csv. Scripts and output are in
  panel_work/novelty/30_paired_comparison_output/.
  - All 3,418 targets, folds and REC labels agree. The two reference vectors are identical (max |diff| = 0.0; pooled
    0.8503173540 in both).
  - Pooled bits: this claim 0.7631118, #1175 0.7802677. This claim is better by 0.0171559 bits per coda.
  - It is better on every fold: +0.0120, +0.0058, +0.0298, +0.0253 and +0.0307 bits on folds 0 to 4.
  - I ran a paired REC bootstrap of the difference (188 RECs, 10,000 resamples, fresh seed 424242). The interval is
    [0.00336, 0.03340], and P(draw <= 0) = 0.008. This is not a tie.
  - Trivial edits of the published object do not reach this claim's number, even with oracle help. I recalibrated #1175's
    selected predictor with a logit-affine map fitted on the held-out labels themselves. That gives 0.780243. A
    held-out-fitted logistic stack of all four of its published variants (order2, order3, repetition, timing) gives
    0.776723. Both are above 0.763112.
- The other public best numbers for this cell, all inside #1175, are order3 0.7845, order2 0.7987 and timing 0.8435.
  All are beaten.

## Neighbouring cells and the literature (last 24 months plus the classic base)

- **WhaleLM, bioRxiv 2024.10.31.621071.** I read the v1 full text (HTTP 200, 10:18:49Z) and its v1 supplementary PDF
  (HTTP 200, 10:20:21Z). I also read the v2 full text (HTTP 200, 10:26:40Z; posted Nov 11, 2024, a title change only:
  "The title change was not reflected the first time the manuscript was submitted"). The abstract claims "predictable
  turn-taking". The supplement folds turn-taking into joint tokens: "There are three types of turn-taking: 1)
  Self-response ... 2) Response by another whale ... 3) Overlapping call ... Each unique combination of rhythm, tempo,
  rubato, ornament, and turn-taking behaviour is assigned a unique token". Evaluation is perplexity on held-out days. The
  paper reports no turn-specific held-out number and no first-order switch baseline. It says "The code will be made
  available upon publication". So it is qualitative prior art for turn predictability, but it gives no equivalent number
  on this binary task. I did not read the NeurIPS 2025 workshop PDF: openreview.net returned HTTP 403 at 10:26:45Z
  (recorded, not retried). A probe for a bioRxiv v3 returned HTTP 429 at 10:29:18Z (error 1015; not retried). The v2 page
  shows no newer-version link.
- **Sharma et al., Nature Communications 15:3617 (2024), PMC11076547.** HTTP 200 at 10:18:54Z. The paper analyses these
  dialogues descriptively. It defines turn-taking ("next-in-sequence codas whose onset occurred within two seconds, but
  after the termination, of the initial coda (as in ref. 33)"). It reports duration matching of overlapping codas
  (0.099 s) and an in-sample Fisher test that ornamented codas are "disproportionately succeeded by a change in
  chorusing behaviour" (odds ratio 1.56, p = 0.009). It has no held-out same-or-switch prediction.
- **Data repository sw-combinatoriality** (github.com/<owner>/sw-combinatoriality, the data repository the bank names).
  The repo page (HTTP 200, 10:18:57Z) shows one commit. The code/ folder holds notebooks 1-exchange-plot, 2-tempo,
  3-rhythm, 4-rubato, 5-ornament, 6-information-capacity and 7-supplementary-extra; none is a turn-prediction model. The
  releases page and its expanded assets (HTTP 200, 10:19:00Z and 10:21:37Z) show one release, "sw-combinatoriality",
  dated 2024-03-14 at 7228c8e. Its only assets are "Source code (zip)" and "Source code (tar.gz)", so the release adds
  nothing beyond the tree. The repo has one PR (#2, "Adding csv with Tempo, Ornamentation, Rhythm ...") and one issue
  (#1, "Availability of acoustic recordings"), neither about turns.
- **Sinha and Chavan, newest versions dated 2026-11-17.** I read the abstract pages and full HTML of 2606.16084v5,
  2609.16612v3 and 2610.33974v2 (all HTTP 200, 10:17:27Z to 10:17:38Z). They analyse 1,952 CETI codas from 63
  recordings, a different corpus from these dialogues, using encoder-defined acoustic forms. 2606.16084v5 says its
  sequence groups "do not establish whether consecutive codas belong to a behavioral exchange" and "We cannot infer ... a
  continuous exchange". 2609.16612v3 says its four pools "are not four verified whales or social units". None of the three
  predicts the speaker or same-or-switch.
- **Assayag, Gero, Paradise and Diamant, Bioacoustics 35(4):472-500 (2026), doi 10.1080/09524622.2026.2684665.** I found
  it in the reference list of 2606.16084v5 ("preceding timing features help predict later vocalizations in selected
  exchanges between whales"). The DOI fetch hit a publisher Cloudflare challenge (HTTP 403 at 10:19:03Z, "Cf-Mitigated:
  challenge"; not retried, not bypassed). I read the authors' public code instead: the repository
  github.com/<owner>/coda-sequences-relations-and-prediction (HTTP 200, 10:28:03Z) and its notebook codaspred.ipynb
  (18.7 MB of notebook JSON, HTTP 200, 10:28:23Z, scanned as text, not executed). The models (GMM-HMM, LSTM, Transformer)
  predict ICI, duration and coda type of the next coda in dyadic exchanges. They use random 70/15/15 splits and report MSE
  or accuracy. No cell takes next speaker or same-or-switch as its target. It is a different task and protocol.
- **whale-coda-dynamics** (github.com/<owner>/whale-coda-dynamics, a 2026 UvA MSc group project). I read the repo page,
  reports/README.md and docs/data_dictionary.md (HTTP 200, 10:26:49Z to 10:27:38Z). It predicts coda type on the
  Assayag 2014-2016 file (1,547 targets, 14 leave-one-day-out folds). It uses the turn state as an input: "S, the state of
  the exchange when the coda starts (whose turn it is, and how long the gap or overlap was)". It never uses the turn as
  the target. It found "Timing, LL(A,B,S) - LL(A,B) | -0.020". It includes sperm-whale-dialogues.csv only as provenance
  material. It reports no same-or-switch prediction.
- **Bond, "Geometric Structure in Sperm Whale Communication", bioRxiv 10.64898/2026.03.11.711226v1** (posted March 13,
  2026; HTTP 200 at 10:29:21Z). It uses this dialogues file ("3,840 sequentially ordered entries across 11 identified
  whales"). Its turn-taking result is descriptive and uses the latency of the coda being classified: "cross-whale response
  latency was approximately half that of same-whale continuation latency ... (Kolmogorov-Smirnov D = 0.560)". It is not a
  held-out, leakage-free forecast and has no first-order switch baseline.
- **Schulz, Whitehead, Gero and Rendell, Animal Behaviour 76:1977-1988 (2008), doi 10.1016/j.anbehav.2008.07.032.** This
  is the classic overlap and matching work. The DOI fetch (HTTP 200, 10:30:21Z) returned only the Elsevier linking-hub
  JavaScript redirect page, which confirms the title "Overlapping and matching of codas in vocal interactions between
  sperm whales: insights into communication function". I did not follow it into ScienceDirect. Sharma 2024 summarises
  its finding ("overlapping codas were more likely to be of the same coda type than expected by chance"). It predates the
  2014-2018 DTag recordings, so it cannot hold a held-out number on these dialogues.
- **Other items opened.**
  - CodaBridge issue #6 (HTTP 200, 10:29:26Z) is a plan for a descriptive "Context Lab" on the dialogues file. It says
    explicitly: "No p-value, independence claim, fitted prediction score, bits/coda ... in this slice".
  - symthaea issue #7667 (HTTP 200, 10:31:56Z) is an open proposal from 2026-10-16 for a dyadic coda-feature benchmark,
    with no result.
  - Northeastern news, 2026-10-22 (HTTP 200, 10:32:34Z), covers CETI dive prediction ("around eight to ten codas can
    predict whether they are about to head off on deep foraging dives") with no turn number.
  - The phys.org repost returned HTTP 403 at 10:31:54Z (not retried).
- **Searches.** I ran web searches for sperm-whale turn-taking, speaker-switch prediction, chorusing and overlap work in
  2025-2026, and for any use of sperm-whale-dialogues.csv or sw-combinatoriality for turn prediction. I opened every hit
  listed above. No other held-out turn-taking prediction number on these data surfaced.

## V3R1T4S repository

- Pinned copy (head 5d2d31e): TROPHY_CASE.md has no sperm, whale or coda entry, and known-knowns/ has no folder for this
  target.
- Live: TROPHY_CASE.md on main (HTTP 200, 10:31:17Z) is byte-identical to the pinned copy, and
  known-knowns/sperm-whale-next-coda-beyond-first-order on main returns HTTP 404 (10:31:14Z).
- PR and issue searches (github.com HTML, HTTP 200, 10:19:57Z to 10:23:29Z): "is:pr sperm", "is:pr whale", "is:pr coda",
  "is:pr turn-taking" and issues "whale" return only two items, both open drafts. No closed PR matched.
  - #1159 is the main-criterion claim, a different cell. Its body says "the turn-taking result (p4) has no separate
    review. Neither is claimed", and its only p4 number is the cross-reference title of #1175.
  - #1175 is the prior p4 claim analysed above.
- No GitHub REST API call was made.

## Handling notes

- Instructions found inside fetched pages were treated as data and not followed. Examples are "Run sh
  verify-it-yourself/run_checks.sh" in #1175 and branch-creation steps in CodaBridge #6. None of them targeted this
  review, so no injection is suspected.
- Refusals recorded and not retried: tandfonline 403, openreview 403, bioRxiv v3 probe 429, phys.org 403. The status
  source itself was not blocked.

## Verdict

Novel as a strict improvement, not as the first clearance of p4. Two facts support this:

1. No paper, preprint, code release or data-repository asset publishes a held-out, leakage-free same-or-switch number on
   these dialogues.
2. The only public number on this exact cell is the open draft #1175 (0.7802677). This claim strictly beats it:
   - by 0.0172 bits per coda, on all 5 folds;
   - with a paired REC-bootstrap interval of [0.0034, 0.0334] that excludes 0;
   - beyond what even held-out-fitted recalibration or stacking of #1175's published predictors gives.

Conditions for any filing:

- The claim text must name PR #1175 and state the comparison above.
- It must say that #1175 first publicly cleared p4, about 5 minutes after this claim's freeze. Maintainers may credit p4
  only once.
- It must disclose that its own switch-pattern-only diagnostic (+0.0595) is below #1175's gain (+0.0700), so its margin
  over #1175 comes from the timing, overlap and speaker-share features.
- It must keep the WhaleLM precedence ("predictable turn-taking") explicit, as #1175 does.

pass: true
