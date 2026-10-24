# Panel verdict — NOVELTY skeptic

context: subagent
target: `dreval-ldo-beat-naive-mean-effects`
written: 2026-10-24 (all times below UTC, from `date -u` immediately around each command)
scope read: `claim/` only, plus `repo/TROPHY_CASE.md`, `repo/bank/targets.json`, and the web. I did not open
anything else under the run directory; `attempts/literature/`, `scout.md`, `BRIEF.md`, `target.md`,
`REPORT.md` and `panel/` were left unread, and every search below is my own.

---

## 1. The status page, fetched once

One fetch, no retries, User-Agent naming the agent and its purpose.

| field | value |
|---|---|
| URL | `https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LDO_normalized.html` |
| time (`date -u` before the call) | `Sat Oct 24 00:01:01 UTC 2026` |
| server `date` header | `Sat, 24 Oct 2026 00:01:02 GMT` |
| HTTP | `200` |
| bytes | `4665771` (`content-length: 4665771`) |
| sha256 | `b7dd9273b4a9efbf36d5d8718a4163c73d1132f7fe8580c9dfd246e55d2c4364` |
| `last-modified` | `Fri, 17 Oct 2025 14:20:40 GMT` |
| `etag` | `"68f250b8-4731ab"` |

Not blocked, no challenge page. The sha256 is **byte-identical** to the one recorded in
`the-record-we-beat/README.md`.

**One cosmetic discrepancy, resolved.** That README records `last-modified` as `14:20:41 GMT` and etag
`"68f250b9-4731ab"`; I got `14:20:40` and `"68f250b8-..."`. GitHub Pages encodes the mtime in the etag's
first field: `0x68f250b8` = 1760710840 = `Fri, 17 Oct 2025 14:20:40 GMT`, `0x68f250b9` = 1760710841 =
`14:20:41 GMT`, and the second field `0x4731ab` = 4665771 = the byte count, identical in both. Two edge
nodes report mtimes one second apart for the same object. Content hash identical, so this is not a change
to the page. Not held against the claim.

### The live maximum, decoded by me

I decoded the page's own Plotly arrays — base64 `bdata`, `"dtype":"f8"`, little-endian float64 — with my own
script, not by transcription. The R² panel carries `"shape":"11, 1"` and decodes to 11 flat values against
the single x label `R^2: normalized`:

| model (page's own y order) | normalized R², decoded |
|---|---:|
| RandomForest | −0.1186137829 |
| NaivePredictor | −0.0891998450 |
| NaiveTissueMeanPredictor | −0.0605339757 |
| MultiOmicsRandomForest | −0.0415598882 |
| ProteomicsRandomForest | −0.0400845409 |
| ElasticNet | −0.0304731681 |
| DIPK | −0.0181021098 |
| NaiveMeanEffectsPredictor | −0.0169112013 |
| SimpleNeuralNetwork | −0.0105003767 |
| GradientBoosting | +0.0108256886 |
| **MultiOmicsNeuralNetwork** | **+0.0234662787** |

**Confirmed:** the maximum over all 11 models is **+0.0235 (+0.0234662787)** and it belongs to
**MultiOmicsNeuralNetwork**. Every one of the eleven values in `the-record-we-beat/README.md` matches my
decode at the precision quoted there. The page's second array (`"shape":"11, 3"`) gives the normalized rank
metrics, where DIPK leads at Pearson +0.3537854333 and Spearman +0.3559470047 — also as recorded.

### The page does not name its dataset — I verified the identification separately

Worth stating because the claim asserts a CTRPv2 cell: the fetched page contains **zero** case-sensitive
occurrences of `LDO` and **zero** of `CTRP`. Its `<title>` is `plotly-logomark` and its only layout title is
`"Heatmap of the evaluation metrics"`. Nothing on the page says which dataset or which setting it is; the
filename is the sole in-page indication. So I checked two further documents (different URLs — not retries of
a blocked fetch):

- `https://dilis-lab.github.io/drevalpy-report/` — `Sat Oct 24 00:03:40 UTC 2026`, HTTP 200, 3448 bytes.
  Heading "Results for all_runs", nf-core/drugresponseeval logo, links to `LCO.html`, `LDO.html`,
  `LPO.html`, `LTO.html`. No dataset named anywhere.
- `https://dilis-lab.github.io/drevalpy-report/LDO.html` — `Sat Oct 24 00:04:07 UTC 2026`, HTTP 200,
  23368 bytes. Confirms the metric definition verbatim: *"Before calculating the evaluation metrics, all
  values were normalized by the predictions of the NaiveMeanEffectsPredictor."* Its **cross-study** tables
  are `table_cross_study_CCLE_LDO.html`, `..._CTRPv1_LDO.html`, `..._GDSC1_LDO.html`, `..._GDSC2_LDO.html`
  — the four other drevalpy datasets, with CTRPv2 absent, i.e. CTRPv2 is the training dataset.
- The paper settles it. `https://www.nature.com/articles/s41467-026-72903-w` — `Sat Oct 24 00:08:56 UTC
  2026`, HTTP 200, 491473 bytes: *"We evaluate all models across application settings (LPO, LCO, LTO, LDO),
  **training on the largest dataset, CTRPv2**, and testing generalization to other public datasets"*, and
  *"All results are compiled into an interactive HTML report (example:
  https://dilis-lab.github.io/drevalpy-report/)"*. It also gives CTRPv2 as *"886 unique cell lines and 545
  compounds"* (the 545 the claim uses), and explains the model count: *"SRMF and SuperFELTR are omitted from
  LDO as they can not predict unseen drugs."*

**Verdict on the cell's identity: correct, but the claim states it where the source does not.** The page is
the CTRPv2 LDO normalized heatmap, and I am satisfied of that — but only after reading two other documents
and the paper. `the-record-we-beat/README.md` presents "CTRPv2" as a field of the snapshot without saying
that the page itself never says so. That should be made explicit.

## 2. Is anything newer? — the Zenodo leaderboard assertion checked independently

A copy of `leaderboard_Oct26.zip` (Zenodo record 23159774) was already on disk; I used it rather than
re-downloading. `md5sum` = `2c39020eaec28ad89e603c054ec61603`, matching the value recorded in
`the-record-we-beat/README.md`. Listed and parsed with Python `zipfile`/`csv`:

- 692 entries. Paths containing `ldo` (case-insensitive): **0**. Paths containing `LCO`: 678. Containing
  `LPO`: 0. The only setting directory is `leaderboard_Oct26/LCO/`.
- `leaderboard_Oct26/evaluation_results.csv`: **270 data rows**, `test_mode` takes exactly one value,
  `{'LCO': 270}`; 10 CV splits; cells anywhere in the file containing the string `LDO`: **0**.

**The claim's assertion is true**: the authors' newest leaderboard has no leave-drug-out results at all. Two
corrections to how it is described:

- `the-record-we-beat/README.md` says "26 models". The file has **27** distinct `algorithm` labels
  (AdaBoostDecisionTree, DIPK, DrugGNN, ElasticNet, EnsembleMF, GradientBoosting, KNNRegressor, Lasso,
  LightGBM, four MultiView variants, NaiveDrugMeanPredictor, NaiveMeanEffectsPredictor, NaivePredictor,
  NaiveTissueDrugMeanPredictor, NaiveTissueMeanPredictor, PaccMann, PharmaFormer, Precily, RandomForest,
  SRMF, SVR, SimpleNeuralNetwork, SparseGO, XGBoost). Immaterial to the claim; still an inaccuracy.
- Those 27 include many models newer than the 11 on the LDO page. None has ever been run in LDO by anyone.
  So the 0.0235 bar is the best of an **older and smaller** model set, and it is the best of that set because
  the cell was abandoned, not because it was contested. See §6.

The report itself is frozen: the `DILiS-lab/drevalpy-report` repository's newest commit is
`2025-10-17T14:09:52` (GitHub API, `Sat Oct 24 00:08:06 UTC 2026`), consistent with the `last-modified` above.

## 3. Literature search, done from scratch

What I searched, and what came back. (Counts and times are from real command output.)

- **OpenAlex** (`api.openalex.org`, `Sat Oct 24 00:05:10`–`00:08:57 UTC 2026`, all HTTP 200): the DrEval
  benchmark search returns 58 works; plus four more topic searches (NCI-60 panel-mean QSAR; NCI-60 combined
  with CTRP/GDSC for unseen drugs; drug-blind external-screen augmentation; growth-inhibition prediction
  from structure).
- **Europe PMC** (5 queries, `Sat Oct 24 00:05:10 UTC 2026`, all HTTP 200): `drevalpy` → hitCount **2**
  (the DrEval preprint and the paper, nothing else); `drugresponseeval` → **2**; `"drug response" AND
  "normalized R2"` → **1** (DrEval only); `"leave-drug-out"` → 34, all drug-synergy or library papers;
  `DrEval` → 490, dominated by false matches on an unrelated acronym.
- **arXiv API** (`Sat Oct 24 00:09:28`–`00:09:48 UTC 2026`, HTTP 200): full-text search
  `all:"DrEval" OR all:"drevalpy" OR all:"drugresponseeval"` → totalResults **4**, all four plasma-physics
  papers matching the surname "Dreval". `abs:"drug-blind" OR abs:"leave-drug-out" OR abs:"unseen drugs"` →
  totalResults **31**, newest first; I read the three relevant ones.
- **bioRxiv API**: the DrEval preprint record (`10.1101/2025.05.26.655288`, 2025-05-29, Bernett, Iversen,
  Picciani, Wilhelm, Baum, List).
- **GitHub** (`daisybio/drevalpy`, pushed `2026-10-23T21:41:47Z`, 31 open issues): searched its issues and
  PRs for `LDO`, `normalized`, `CTRPv2`. 16 LDO hits, none reporting a number. The claim's reference to the
  combination-treatment caveat checks out: issue **#300, "LDO should exclude Combination treatments"**, open,
  created 2025-10-24. Rate limit stopped three further queries; nothing in what I did see reports an LDO
  normalized R².
- **Two web searches** (DrEval LDO normalized R² leaderboard; NCI-60 pretraining for drug-blind CTRP/GDSC).

**Result: I found no published DrEval/drevalpy LDO result above 0.0235, on any dataset, from any group.**
Nor any below it — nobody has published one at all beyond the eleven on that page.

**Corroboration from the benchmark's own authors.** Iversen et al., *Leveraging uncertainty estimates for
drug response prediction in cancer cell lines*, Bioinformatics Advances 2026 (`10.1093/bioadv/vbag246`,
open-access full text read via Europe PMC `PMC13600678`, `Sat Oct 24 00:10:05 UTC 2026`, HTTP 200) contains
**zero** occurrences of `LDO` and says plainly: *"Drug response models currently still extrapolate poorly to
unseen drugs (leave-drug-out setting) (Bernett et al. 2026). We therefore restrict our uncertainty benchmark
to cell-line generalization."* The follow-up work from this group deliberately skipped the cell.

**One source was inaccessible, and that is evidence neither way.** The publisher copy of that same paper
(`https://doi.org/10.1093/bioadv/vbag246` → `academic.oup.com/...`) returned **HTTP 403**, 5740 bytes, at
`Sat Oct 24 00:09:28 UTC 2026`. I did not retry; the open-access PMC copy covered it.

### Comparability of the near-neighbours — my view

The nearest numbers in the literature are **not like-for-like**, and in each case the direction of the
mismatch matters:

- **Lavelle et al., arXiv:2608.11444** reports drug-blind **global** R² on the **IMPROVE** benchmark.
  Global R² over all held-out (drug, cell line) pairs is dominated by between-drug potency spread; it is the
  very quantity DrEval's normalization removes. 0.22 there and +0.2249 here are different measurements that
  happen to land on the same number.
- **Heo, arXiv:2605.20885** (*Training distribution determines the ceiling of drug-blind cancer sensitivity
  prediction*, 2026-05-20, OpenAlex record read `Sat Oct 24 00:05:37 UTC 2026`) makes exactly this argument
  in print: *"the standard benchmark, global Pearson r, is dominated by between-drug potency differences that
  a trivial drug-mean predictor captures without any cell-specific learning"*. It reports per-drug Pearson r,
  not normalized R², and its method is mechanism-stratified training, not external-screen augmentation.
- **Liu et al., arXiv:2609.32467** (*Bison*, 2026-09-26) is cross-dataset unseen-compound prediction but of
  **transcriptional** responses on gene panels, scored by overall-response and drug-contrast Pearson. Not
  viability, not this metric.
- Older cross-study work (e.g. the Briefings in Bioinformatics cross-study analysis spanning NCI-60, CTRP,
  GDSC, CCLE and gCSI) reports global R²/Pearson across screens. Same mismatch.

So: nothing in the literature is a comparable measurement of this cell, and nothing is higher even on its own
terms. That is a clean field for the number — and it is clean partly because so few people are measuring here.

## 4. The method's novelty, separately from the number

### The attribution to Lavelle et al. is accurate

I read the paper. `https://arxiv.org/abs/2608.11444` (`Sat Oct 24 00:05:57 UTC 2026`, HTTP 200, 44101 bytes)
and its v2 full text `https://arxiv.org/html/2608.11444v2` (`Sat Oct 24 00:06:24 UTC 2026`, HTTP 200,
150469 bytes):

- **Title/authors as cited**: *Large-scale AI-Ready Data for Anti-Cancer Drug Response Modeling*; Vincent
  Lavelle, Yitan Zhu, Kaitlyn Marlor, Thomas Brettin, Rick Stevens; submitted 11 Aug 2026, v2 17 Aug 2026.
- **The numbers the claim quotes are in its Table 3**, "Mean R² across 10 cross-validation folds": Original
  UNO drug-blind **0.03**, Expanded UNO drug-blind **0.22**. `HOW_WE_FOUND_IT.md`'s "raised drug-blind global
  R² from 0.03 to 0.22" is exact.
- **"by adding NCI-60 compounds" is a fair reading**, not a distortion. The abstract leads with PharmacoDB,
  but the paper's Table 1 gives `NCI60_2021` as 53,323 drugs / 4,267,356 experiments out of totals of 53,949
  drugs / 5,455,444 experiments, and the text says the expanded set *"is heavily dominated by experiments
  from the NCI60 study"* and that *"the NCI60 dataset constitutes the majority of the expanded dataset"*.

**So the credit is correctly given, and the idea is indeed not this claim's.** It was in print roughly ten
weeks before this run.

### The stated delta over Lavelle is real, and narrow

Lavelle et al. excluded held-out **identities** only: *"all experiments involving the held-out drugs or cell
lines were removed from the remaining data for that fold, regardless of their source."* No analogue
exclusion. This claim adds salt-stripped InChIKey-skeleton matching **or** Morgan Tanimoto ≥ 0.60
(`how-we-built-it/H10-PRECOMMIT.md`, Amendment 2), and reports the monotone sensitivity curve across four
thresholds. That is a genuine methodological addition Lavelle did not make, and it is the right one: it is
the test that separates chemistry transfer from analogue lookup. I credit it.

### Two attribution gaps I do hold against the package

1. **The credit lives only in the file marked unverified.** `grep` over all of `claim/` finds "Lavelle"
   exactly once, at `HOW_WE_FOUND_IT.md` line 55 — a file whose own first line reads *"Contributor text,
   unverified."* Neither `the-record-we-beat/README.md`, nor `how-we-built-it/README.md`, nor
   `how-we-built-it/H10-PRECOMMIT.md`, nor any of `PREREG.md`/`.v2`–`.v5` cites the prior work at all. The
   load-bearing documents describe the external potency prior as "the decisive component" with no indication
   that its central idea is published. Chronologically this is explicable — H10-PRECOMMIT is timestamped
   `2026-10-23T22:32:51Z` and `HOW_WE_FOUND_IT.md` says the literature search came afterwards — but the fix
   is to carry the citation into the load-bearing files, not to leave it in narrative.
2. **Panel-mean NCI-60 potency QSAR is decades-old prior art, and is cited nowhere.** The claim's prior is
   an MLP on Morgan-2048 fingerprints predicting panel-mean log10 GI50. Predicting NCI-60 growth inhibition
   from structure is a well-worked task: Cortés-Ciriano, van Westen, Bouvier, Nilges, Overington, Bender,
   Malliavin, *Improved large-scale prediction of growth inhibition patterns using the NCI60 cancer cell line
   panel*, Bioinformatics (`10.1093/bioinformatics/btv529`; 17,142 compounds × 59 NCI60 lines, 941,831 data
   points, and explicitly tests extrapolation *"to dissimilar compounds"*); Martorana et al.,
   *Antiproliferative Activity Predictor: A New Reliable In Silico Tool for Drug Response Prediction against
   NCI60 Panel*, IJMS 2022 (`10.3390/ijms232214374`), a ligand-based GI50 predictor for the NCI60 panel.
   Both abstracts read via Europe PMC, `Sat Oct 24 00:11:45 UTC 2026`, HTTP 200.
   The claim never asserts this component is novel — but a package whose stated contribution is rigour should
   point at the field it is standing on.

**Net judgement on originality:** the claim does **not** overstate its own originality in the one place it
addresses the question — `HOW_WE_FOUND_IT.md` says "The idea is not ours" and names the source correctly.
Its sin is placement and omission, not misrepresentation. That is a documentation defect, not dishonesty, and
it does not change what the number is.

## 5. TROPHY_CASE.md — no drug-response or cancer-pharmacology result

Per-pattern counts over `repo/TROPHY_CASE.md` (100 lines): `drug` 0, `cancer` 0, `pharma` 0, `IC50` 0,
`GDSC` 0, `CTRP` 0, `cell.line` 0, `biolog` 0, `molecul` 0, `protein` 0, `DrEval` 0, `dreval` 0, `response`
0. The only hit, `chem` ×6, is "schemes" in the matrix-multiplication rows. The seven family rows are
degree-diameter graphs, Lehmer's totient problem, matrix multiplication, VNN-COMP 2026 counterexamples, a
RobustBench CIFAR-100 attack, constant-weight codes, and the cipher-challenge commitments.

**Nothing in the trophy case touches drug response or cancer pharmacology.** This would be the first.
(`repo/bank/targets.json`: 287 targets, of which 38 match a drug/cancer/pharmacology regex — the bank has
biology targets; the trophy case has no biology results.)

## 6. Pull requests — none covers this target

Enumerated honestly against `github.com/elder-plinius/V3R1T4S` (the repo's `origin`):

- **Open PRs at `per_page=100`**, `Sat Oct 24 00:07:02`–`00:07:46 UTC 2026`, all HTTP 200: pages 1–3 returned
  100 each, page 4 returned 6, page 5 returned 0 → **306 open PRs enumerated in full**. I read every title.
  None concerns drug response, DrEval, LDO, CTRPv2 or any pharmacology target. The nearest biology items are
  `#467`/`#463` (ProteinGym cancer DMS zero-shot), `#569` (TCR-epitope), `#568` (Polaris MoleculeACE
  activity cliffs) — all different targets.
- **Search endpoint** (covers closed and merged), `Sat Oct 24 00:07:20 UTC 2026`, all HTTP 200, `type:pr`:
  `dreval` **0**, `drug+response` **0**, `LDO` **0**, `leave-drug-out` **0**, `CTRPv2` **0**,
  `dreval-ldo-beat-naive-mean-effects` **0**, `NCI-60` **0**, `drevalpy` **0**. Issues (not restricted to
  PRs) for `dreval`: **0**.
- **I verified the search index actually works on this repo** rather than trusting eight zeros:
  `covering-designs` → total_count 17, `proteingym` → 2, `degree-diameter` → 6, with matching PR numbers. The
  zeros are real.

**No open, closed or merged pull request covers this target.**

## 7. Decision, and what I think the number means

**The record stands, strictly.** Live maximum on the primary status page, decoded by me from the page's own
binary arrays at `Sat Oct 24 00:01:02 UTC 2026`: **+0.0234662787**, MultiOmicsNeuralNetwork. The claim's
**+0.2249** (and the more conservative row-aligned **+0.2244** in `verify-it-yourself/RECEIPTS.md`) exceed it
by roughly an order of magnitude. Not a tie. Nothing newer exists — the authors' October 2026 leaderboard has
no LDO rows at all, verified in the archive. Nothing in 2019–2026 literature reports a DrEval LDO result
above 0.0235, from any group on any dataset, and the nearest neighbours are different metrics on different
benchmarks and are not higher anyway. The attribution to Lavelle et al. is real, correctly numbered, and
candid about not owning the idea. On my instruction's test — strictly beats everything known for this
benchmark cell, and honest attribution — this passes.

**Four framing objections that belong in the record even though the number stands.**

1. **This is not a like-for-like model comparison, and the mismatch runs in the claim's favour.** The paper
   states the eleven leaderboard models were trained *"on the largest dataset, CTRPv2"* — 545 compounds. This
   method adds an external screen of ~53,500 compounds, about a hundredfold more chemical space. No model on
   that page uses an external response screen, and the page is not an open leaderboard: it is DrEval's own
   controlled comparison of eleven models under uniformly processed data. Beating its maximum by changing the
   data regime is a legitimate and interesting result, but "ten times the published best" invites the reading
   that the *modeling* is better, when what the result actually demonstrates is that the training
   distribution was the binding constraint — the conclusion Lavelle et al. and Heo et al. already published.
   The claim's own closing paragraph is more careful than its headline; the headline should match it.
2. **The bar being cleared is not a statistically meaningful record.** The paper's LDO critical-difference
   analysis gives a **Friedman p-value of 0.742** over the eleven models (t = 11, 10 folds) — no significant
   differences among any of them, naive baselines included. `LDO.html`'s post-hoc Conover table shows the
   same. So +0.0235 is a noise-level maximum, and a ratio taken against it carries no effect-size meaning.
   The defensible statement is the absolute margin and its across-split spread, which the package does report.
3. **The cell is uncontested rather than hard-won.** The page has been unchanged for a year
   (`last-modified Fri, 17 Oct 2025 14:20:40 GMT`; report repo's last commit `2025-10-17T14:09:52`). The same
   group's October 2026 leaderboard dropped LDO entirely, and their 2026 follow-up says in so many words that
   they restrict to cell-line generalization because models extrapolate poorly to unseen drugs. Twenty-seven
   newer algorithms exist in that leaderboard and not one has been run in LDO. "Beats everything known" is
   true; "beats everything that tried" would overstate it, because almost nothing tried.
4. **What the metric measures is narrower than the setting's name.** Because the LDO reference baseline has
   no information about an unseen drug, the normalized residual is dominated by that drug's average potency
   across cell lines, and this model predicts exactly one number per drug — it is silent on the
   cell-line-specific response that "personalised" would mean. The package says this itself, including the
   finding that a substantial share of the potency variance tracks the experimenters' chosen top
   concentration. That self-criticism should travel with the headline wherever the headline goes, and any
   write-up should state that beating this cell is not evidence of progress on cell-line-specific prediction.

**Required before publication, in my view:** carry the Lavelle et al. citation into
`the-record-we-beat/README.md` and `how-we-built-it/README.md` rather than leaving it in the file marked
unverified; cite the NCI-60 panel-potency QSAR prior art; state in `the-record-we-beat/README.md` that the
page itself names neither the dataset nor the setting and say how CTRPv2 was established; and correct
"26 models" to 27. None of these changes the number.

pass: true
