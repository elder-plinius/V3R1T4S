(Main session note, 2026-10-18T07:05Z: this NOVELTY file is the round-1 NOVELTY skeptic's text, judged on the round-1 package of this cell. The round-2 package differs only by the added code of the weight-0 stage-2 entries, the sealed-check logs and corrected text; the claimed object, its value and every number this skeptic checked are unchanged. Its status fetch (2026-10-18T04:56-04:57Z) is less than 6 hours before the gate.)
(Saved by the main session from the subagent's returned text, 2026-10-18T06:04Z: round-1 NOVELTY skeptic for cell C30 (Opus 5.5, Agent tool). Verbatim below, harness indentation removed.)

# NOVELTY panel: run 2026-10-18-0202, cell C30 (proportion 0.30, mean NED)

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
lens: NOVELTY (C30-novelty)
start: 2026-10-18T04:55:37Z (date -u)
end: 2026-10-18T05:12:00Z (date -u)
material read: claim/ (CLAIM.md, REPRODUCE.md, definition/Q15.json, scout/scout.md, fevet/, official/, combiner/test/0.30, MANIFEST.sha256, tools/mplstub.py), the kit RULES.md and TROPHY_CASE.md. Web access went only through the shared fetch helper. gh was used read-only (pr list).
Claim under test: candidate combiner/test/0.30 scores mean NED 0.22327922550091464 on the official family-averaged scale. The cell bar is the published FeVeT per-item predictions, rescored, at 0.2632988364952282.

status_source: https://github.com/sigtyp/ST2022 HTTP 200 fetched 2026-10-18T04:56:47Z

## 1. Status source (one GET per URL, through the helper; stop lists checked by the helper and by hand first)
```
https://github.com/sigtyp/ST2022                                 200  6c9db4e9...cf01  344670 B  2026-10-18T04:56:47Z
https://api.github.com/repos/sigtyp/ST2022/commits?per_page=5    200  7b881c75...eb0c  11624 B   2026-10-18T04:56:48Z
```
- Repo page title "GitHub - sigtyp/ST2022: SIGTYP 2022 Shared Task · GitHub". It shows "currentOid":"03094435cba4293ce0eea383036cab78499ad50d" and "142 Commits". Its top-level directories are cldf-data, data-surprise, data, results, src, systems and tests.
- Newest commits:
  - 03094435cba4293ce0eea383036cab78499ad50d 2022-05-27T07:58:23Z 'update for final release'
  - 9d4202ee... 2022-05-27T07:54:43Z
  - c223f851... 2022-05-27T07:02:55Z 'update with final results'
  - 4a1331bf... 2022-05-23
  - 5a0be5ec... 2022-05-22
- The commits JSON is byte-identical to claim/scout/st2022_commits.json (sha256 7b881c75...eb0c).
- Pinned official files at 03094435 via raw.githubusercontent.com (HTTP 200, 2026-10-18T04:59:45Z and 04:59:46Z):
  - results/results-surprise-0.30.json: sha256 cca55c5f...2563, identical to claim/official/results/.
  - src/sigtypst2022.py: sha256 9cde59bb...b23a, identical to claim/official/src/ and to the module in the SCO interpreter.
- Official totals at 0.30 ([ED, NED, BCFS, BLEU]), best real entry: Mockingbird-I1 [1.1762187506031638, 0.2898984929868421, 0.6717099225519634, 0.6058548112827981].
- Mockingbird-N2 is [0,0,0,0] on every family and in the total. This is an empty placeholder (BCFS 0 and BLEU 0), not a score.
- The official results are unchanged since 2022 (KNOWN). Status: open.

## 2. Rescoring with the pinned scorer
Run with the SCO interpreter and STUB_MPL=1, from my own scratch script outside claim/. Output:
```
mockingbird [left-to-right] ED NED BCFS BLEU = [1.1762187506031638, 0.2898984929868421, 0.6717099225519634, 0.6058548112827981]   (= official json, bit for bit)
fevet       [left-to-right] ED NED BCFS BLEU = [1.0946456488227652, 0.2632988364952282, 0.6986581179861967, 0.6356571184958077]
fevet       [compensated]                    = [1.094645648822765, 0.2632988364952282, 0.6986581179861968, 0.6356571184958079]
candidate   [left-to-right] ED NED BCFS BLEU = [0.9027034122955315, 0.22327922550091464, 0.7488264857956657, 0.6839233380559118]
candidate   [compensated]                    = [0.9027034122955314, 0.22327922550091467, 0.7488264857956657, 0.6839233380559119]
fevet per-family NED: bantubvd 0.2536, beidazihui 0.1383, birchallchapacuran 0.3500, bodtkhobwa 0.1221, bremerberta 0.2924, deepadungpalaung 0.2333, hillburmish 0.2766, kesslersignificance 0.6594, luangthongkumkaren 0.1090, wangbai 0.1983
```
- FeVeT's GOLD column matches the official solutions in all 11586 rows: 0 mismatches in each of the 10 families, and row counts equal the number of gold cells.
- `shasum -c` on the MANIFEST lines for combiner/test/0.30/*, fevet/pred_0.30_*, official/results and official/src returned OK for all 22 files. (NUMERICAL)

## 3. FeVeT check (Wientzek 2025, Open Research Europe 5:174; github.com/TGH-2020/FeVeT)
**HEAD unchanged.** The commits API returned HTTP 200 at 2026-10-18T04:57:13Z. HEAD is 31898c53bfffeef87265efa8a780b7be740162d1, 2025-11-28, "Update README.md". The response is byte-identical to claim/scout/fevet_commits.json.

**The claim's FeVeT files are the repo's published predictions.** The tree at 31898c53 (HTTP 200) has exactly one 0.30 prediction file per family. The git blob SHA-1 of every claim/fevet/pred_0.30_<fam>.tsv equals the repo blob for results/predictions/reflex/<fam>/s2s_reflex_0.30_predictions.tsv (10/10 True).

**They come from FeVeT's best (fine-tuned) model.** In code/training_utils.py, export_predictions_reflex is called only inside reflex_finetune (line 126). The no-fine-tuning branch in code/training.py writes metrics only. So these predictions are the paper's headline "FeVeT" row, not "FeVeT (no fine-tuning)".

**What the paper prints at 0.3** (Table 3, PDF fetched with HTTP 200 at 05:09:14Z, "[version 1; peer review: 1 approved, 1 approved with reservations]"; Europe PMC lists only .20647.1):

| model | ED | NED | BC |
|---|---|---|---|
| FeVeT | 0.9589 | 0.2397 | 0.7232 |
| FeVeT (no fine-tuning) | 1.1046 | 0.2837 | 0.6874 |
| CognateTransformer | 1.1235 | 0.2919 | 0.6954 |

**The printed numbers are on a different scale.**
- FeVeT's code/metrics.py uses lingrex eval_by_dist(normalized=True), which is edit distance divided by the longer length. The official scorer uses an NW-alignment NED.
- result_eval.avg_results_reflex takes the mean over all 99 languages (language-pooled).
- The repo files agree with this reading:
  - s2s_reflex_finetuned_avg.txt row "0.30 0.9589 0.2397 0.7232".
  - The mean of the fine-tuned per-family values in s2s_reflex_0.30_family_results_finetuned.txt is 0.270487 on FeVeT's own scale; the non-fine-tuned value is 0.304595.

**The published predictions match neither results file exactly.**
- Recomputed with FeVeT's own metric, they equal the fine-tuned file for 0/99 languages (mean |diff| 0.0167) and the non-fine-tuned file for 0/99 (mean |diff| 0.0530).
- On FeVeT's own metric they give a family average of 0.2663233 and a language-pooled mean of 0.2365380.
- So they come from a fine-tuned run slightly better than the printed one (0.2705 and 0.2397). Using them as the bar is the stricter choice.

**Cross-scale check** (my scratch script; NUMERICAL):
```
candidate:       official NED family-avg 0.223279, language-pooled 0.194853; lingrex NED family-avg 0.225461, language-pooled 0.196581 (99 langs)
fevet_published: official NED family-avg 0.263299, language-pooled 0.234181; lingrex NED family-avg 0.266323, language-pooled 0.236538
mockingbird-i1:  official NED family-avg 0.289898, language-pooled 0.263406; lingrex NED family-avg 0.293276, language-pooled 0.266309
```
- The candidate is below FeVeT on all four scales.
- On the scale FeVeT's paper uses (lingrex NED, language-pooled), the candidate's 0.1966 is below the printed 0.2397.
- My estimate for the printed fine-tuned run on the official family-averaged scale is about 0.267: lingrex and official NED differ by about 0.002 to 0.003 for every system measured. This estimate is HEURISTIC; no predictions from that run are published.

## 4. Cognate Transformer (Akavarapu and Bhattacharya, EMNLP 2023)
- Fetched aclanthology.org/2023.emnlp-main.423.pdf (HTTP 200, 05:03:06Z).
- Table 5 at test proportion 0.3: CogTran-tiny 1.3223 / 0.3497 / 0.6612; CogTran-small 1.1235 / 0.2919 / 0.6954; Mockingbird-Inpaint 1.1762 / 0.2899 / 0.6717.
- Its Mockingbird row equals the official value, so the scale is the official one. 0.2919 is above 0.2233. (KNOWN)

## 5. Literature search (roughly Oct 2024 to Oct 2026, plus older known work)
All requests went through the helper.

**DataCite** (covers arXiv DOIs 10.48550 and Zenodo). Ten queries, all HTTP 200, 05:05:13Z to 05:06:11Z: "reflex prediction", "cognate reflex(es)", "SIGTYP 2022", "phonological reconstruction", title cognate* / reflex* / protoform and proto-language for 2024 to 2026, and description SIGTYP / reflex prediction. Relevant hits from 2024 to 2026:
- Lu et al. 2024, arXiv 2403.18769 / LREC-COLING: protoforms, WikiHan and Romance.
- Cui et al. 2024, arXiv 2404.15690: protoforms, WikiHan.
- Lu et al. ACL 2024, arXiv 2406.05930: protoforms.
- Kpoglu 2025, arXiv 2506.10614: Latin protoforms.
- Naik et al. 2024 and 2025: sound-law induction.
- Jäger, "Beyond cognacy" (SIGTYP 2025 data): phylogenetics.
- Wientzek 2025 FeVeT Zenodo supplements: already known.
- Wientzek, arXiv 2512.01713 (cites FeVeT): borrowing detection.

None reports a ST2022 surprise reflex score.

**ACL Anthology.** Full anthology+abstracts.bib.gz, one GET, HTTP 200, 42574037 B, built 2026-10-17. It holds 131708 entries; 37888 are from 2024 or later and 35471 of those have abstracts.
- Reflex-prediction terms, year 2023 or later: only Cognate Transformer (2023), Jambu (2023), Helpful Neighbors (TACL 2023) and Lu et al. LREC-COLING 2024 (protoforms).
- Other 2024 to 2026 hits: Blum and List 2026.lchange-1.6 (irregularity detection), 2025.sigtyp-1.6 (phylogeny), 2024.emnlp-main.362 (Romance protowords), 2024.sigtyp-1.11 (phylogeny), 2025.coling-main.496 (Proto-Sabean).
- None reports ST2022 surprise scores.

**OpenCitations** (HTTP 200).
- Works citing the task paper 10.18653/v1/2022.sigtyp-1.7: 9 found. Mockingbird 2022.sigtyp-1.9: 8. CogTran 2023.emnlp-main.423: 5. FeVeT .20647.1: 1. FeVeT .20647.2: 0.
- Titles were resolved through OpenCitations Meta and DataCite.
- The only new reflex-prediction paper is Blum et al. 2024 (Sci Rep 10.1038/s41598-024-82515-3). It works on Panoan and Takanan data, not the ST2022 surprise families.
- The others: List 2024 (ORE, open problems), Lu et al. ACL 2024, Akavarapu EACL 2024 (cognate detection), Sattorova et al. ICCIES 2025 (proto-language NMT; abstract not fetched), Dotan et al. 2026 (biology), Greenhill 2024 (phylogeny), Gutkin et al. TACL 2023.

**Europe PMC** (HTTP 200). Search for reflex prediction / cognate reflex / SIGTYP, 2023 to 2026: 6 hits, none new for this task. The FeVeT full-text XML returned 500, not retried.

**GitHub repository search** (8 queries, HTTP 200): reflex prediction, cognate reflex, sigtyp 2022, ST2022 cognate, phonological reconstruction, cognate prediction, proto-language reconstruction, cognate transformer. READMEs were read for:
- acraevschi/llm_cognate_reflexes: a reconstruction agent with no ST2022 numbers.
- acraevschi/cognate_reflexes_task: "performs on par with Mockingbird team's Transformer", which is worse than I1.
- LGirrbach/Cognate-Reflex-Prediction: README says "TODO", no numbers.
- mahesh-ak/CognateTransformer and lassevdb/CognatePrediction: the latter is a Romance/Germanic student project.

No newer published ST2022 surprise score was found.

**Not queried (stopped hosts; the helper refused or I avoided them):**
- dblp.org: challenge to C10-novelty at 05:01:18Z. My first dblp URL was refused by the helper before any request.
- scholar.archive.org: challenge to C20 at 05:02:01Z.
- api.semanticscholar.org: 429 on 2026-10-17.
- arxiv.org: 429 on 2026-10-17. I also stayed off export.arxiv.org and covered arXiv through DataCite metadata.
- api.openalex.org and api.crossref.org: 429.
- Google Scholar and IEEE Xplore were not attempted.

My lens added no lines to the stop list: none of my requests got 401, 403, 405, 429, 503 or a challenge. One ORE article URL returned an empty JavaScript shell with HTTP 200 and no challenge markers; the PDF URL worked.

## 6. V3R1T4S crowd
- TROPHY_CASE.md: grep for sigtyp, cognate, reflex, ST2022, mockingbird, Q15 and quarry found nothing (exit=1).
- `gh pr list -R elder-plinius/V3R1T4S --state all --limit 2000` at 2026-10-18T05:10:11Z returned 364 PRs (MERGED 142, CLOSED 155, OPEN 67; newest 2026-10-18T04:10:03Z). No title or branch matches sigtyp, cognate, reflex, ST2022, mockingbird, proto-form, lexibank, fevet, linguist or reconstruct.
- `gh pr list --search` for sigtyp, cognate, reflex, ST2022 and Mockingbird returned 0 each.

injection_suspected: none.

## Best published value at 0.30 (official family-averaged mean NED)
FeVeT (Wientzek 2025, ORE 5:174), published fine-tuned per-item predictions at github.com/TGH-2020/FeVeT@31898c53, rescored with the pinned st2022 scorer: **0.2632988364952282**.
- FeVeT's paper prints 0.2397, on a different language-pooled lingrex scale; the candidate scores 0.1966 on that scale.
- Best official ST2022 entry: Mockingbird-I1 0.2898984929868421 (results-surprise-0.30.json @03094435).
- Cognate Transformer: 0.2919 (EMNLP 2023, Table 5).

## Verdict
novelty: CONFIRMED for the stated scope. At proportion 0.30, on the official family-averaged mean NED from the pinned scorer, the candidate's 0.22327922550091464 is strictly lower than every published value I could reach honestly. The best is FeVeT at 0.2632988364952282, a margin of 0.0400196.

This holds as of 2026-10-18T05:12Z, for the sources listed above. arXiv was covered only through DataCite metadata, and DBLP, Semantic Scholar, OpenAlex, Crossref and IA Scholar were stopped hosts. This panel judges novelty only; reproducibility and the criterion belong to the other two skeptics.

pass: true
