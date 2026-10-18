(Saved by the main session at 2026-10-18T12:37:59Z from the novelty skeptic subagent's returned text (cell B50; Opus 5.5, agent aed0cfcabcbe42b85); the subagent could not write a file named like a report. Text verbatim below.)

# NOVELTY skeptic, cell B50 (proportion 0.50, mean BCFS), run 2026-10-18-0839

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
start: Sun Oct 18 11:44:30 UTC 2026
end: Sun Oct 18 11:58:15 UTC 2026
lens field used for every web request: B50-NOVELTY (shared fetch helper vfetch.py, one plain GET each, User-Agent naming V3R1T4S, stop lists checked before each request)
material: claim/ only (CLAIM.md, definition/Q15.json, scout/, official/, fevet/, combiner/test/0.50, object/, checker/), plus kit RULES.md, TROPHY_CASE.md, the web through the helper, and read-only gh pr list on elder-plinius/V3R1T4S.

## Verdict in one sentence
I found no published score on the 10 SIGTYP 2022 surprise families at proportion 0.50 that reaches the claimed mean BCFS 0.7114179305724276. The highest number printed anywhere is FeVeT's 0.673, which is on a different scale (a mean over 99 languages, not over families). On that same language-pooled scale the claimed object scores 0.742250. The claim strictly beats every known value. Labels: NUMERICAL (rescoring), KNOWN (literature values).

## 1. Status source
status_source: https://github.com/sigtyp/ST2022 HTTP 200 fetched 2026-10-18T11:44:55Z
- Helper output: `200 0574d02ce9a5c19ceee9f3bbcdb8a562d1207252acc42727ab935aeb49119075 344669 2026-10-18T11:44:55Z`. Page title "GitHub - sigtyp/ST2022: SIGTYP 2022 Shared Task · GitHub", "142 Commits", head commit 03094435cba4293ce0eea383036cab78499ad50d.
- https://api.github.com/repos/sigtyp/ST2022/commits?per_page=5 returned HTTP 200 at 2026-10-18T11:45:06Z, sha256 7b881c75158171750f802d30b85b67bcbe949a72f7d5a4588a5ea6914af2eb0c. This is the same sha256 as the scout's copy. Newest commits:
  - `03094435cba4293ce0eea383036cab78499ad50d 2022-05-27T07:58:23Z 'update for final release'`
  - `9d4202ee... 2022-05-27T07:54:43Z 'update'`
  - `c223f851... 2022-05-27T07:02:55Z 'update with final results'`
  - The repo is unchanged since 2022-05-27.
- https://raw.githubusercontent.com/sigtyp/ST2022/03094435cba4293ce0eea383036cab78499ad50d/results/results-surprise-0.50.json returned HTTP 200 at 2026-10-18T11:48:08Z, sha256 3a8e79f9e686a4835f6bd0948529838b4ebb38ef2f02e05d39dfa73389a014f3. `cmp` against claim/official/results/results-surprise-0.50.json printed IDENTICAL_TO_CLAIM_COPY. The official results are unchanged.
- Official 0.50 totals ranked by BCFS (from that file):
  - CrossLingference-Julia 0.6193241007226449
  - Mockingbird-I1 0.6050308536957327 (NED 0.35176136367373956, BLEU 0.5337187296541888)
  - Mockingbird-N1-A 0.595911890890592
  - Mockingbird-N1-B 0.5863575276995412
  - Baseline-Baseline 0.5616582507069442
  - The rest are lower.
- Observation: the best official BCFS at 0.50 is CrossLingference-Julia, not Mockingbird-I1. The success criterion names Mockingbird-I1, so this changes nothing. Both are far below the claim.
- https://sigtyp.github.io/st2022.html returned HTTP 200 at 2026-10-18T11:54:57Z. It is the 2022 task page and shows no later leaderboard.

## 2. FeVeT bar: published per-item predictions and the paper's scale
- FeVeT commits (https://api.github.com/repos/TGH-2020/FeVeT/commits?per_page=5): HTTP 200 at 2026-10-18T11:46:57Z, sha256 4ed6f1469db77527e094ec22d44ddb3278cdc0ee9ad8b5de120693b19c454dc0, the same as the scout's copy. HEAD is `31898c53bfffeef87265efa8a780b7be740162d1 2025-11-28T17:00:16Z 'Update README.md'`, so FeVeT is unchanged.
- FeVeT tree at 31898c53: HTTP 200 at 11:46:57Z. It has one prediction file per family at 0.50 (results/predictions/reflex/FAM/s2s_reflex_0.50_predictions.tsv). It also has results/s2s_reflex_0.50_{family,language}_results{,_finetuned}.txt.
- I fetched all 10 prediction files fresh from raw.githubusercontent.com at 31898c53 (HTTP 200, 11:47:19Z to 11:47:22Z). Each sha256 equals claim/fevet/expected.sha256. Examples:
  - bantubvd a9fafb3f...30b4
  - wangbai 3231b6d3...cfd5
  - `shasum -c` on claim/fevet: 10 of 10 OK.
- My own rescoring script loads claim/official/src/sigtypst2022.py and runs compare_words. Official scale means the per-family TOTAL row, then statistics.mean over the 10 families. Coverage check: every gold cell has a FeVeT row with 0 gold mismatches, except deepadungpalaung, where 1448 of 1450 cells carry a non-empty prediction. Output:
  - `FeVeT-published-0.50 OFFICIAL-SCALE MEAN: ED 1.286021835157271 NED 0.30880111347517586 BCFS 0.6423935720824072 BLEU 0.5768215755932388` (equals the claim's bar exactly)
  - `CLAIMED-OBJECT combiner/test/0.50 OFFICIAL-SCALE MEAN: ED 1.0166617451971307 NED 0.24912258145405175 BCFS 0.7114179305724276 BLEU 0.6520222200978465`
- FeVeT paper: Wientzek 2025, Open Research Europe 5:174, doi 10.12688/openreseurope.20647.1. I read it as JATS XML from https://open-research-europe.ec.europa.eu/articles/5-174/v1/xml (HTTP 200, 2026-10-18T11:52:34Z). Table 3 at proportion 0.5:
  - CognateTransformer ED 1.2786, NED 0.3332, BC 0.6477
  - FeVeT (no fine-tuning) ED 1.2405, NED 0.3222, BC 0.6426
  - FeVeT ED 1.1111, NED 0.2825, BC 0.673
- Is a newer version of the paper out? The v2 XML request returned 500, an ORE "Internal server error" page. Europe PMC lists only version .1. So v1 is the only version I could find.
- The FeVeT paper's scale, from FeVeT's own result files:
  - Mean over all 99 languages of language_results_finetuned.txt: ED 1.111068, NED 0.282542, B3_F1 0.673023. This reproduces the paper's FeVeT row.
  - Mean over 99 languages of language_results.txt: B3_F1 0.642635. This reproduces the "no fine-tuning" row.
  - So the paper prints language-pooled averages: a mean over 99 languages, not the official mean over families. Confirmed.
  - On a family-averaged scale, FeVeT's own files give 0.641800 (finetuned family file mean, or 0.641802 rebuilt from its language file) and 0.620460 (no-ft family file).
- Which model are the published predictions from? Their official per-language BCFS differs from FeVeT's finetuned language file by mean 0.022391 (max 0.076616) and from the no-ft file by mean 0.049238. Their official language-pooled mean is BCFS 0.675458, close to the paper's fine-tuned 0.673. So the published predictions are most likely the fine-tuned model. Rescored on the official scale they give 0.6423935720824072.
- On the language-pooled scale, the claimed object scores ED 0.868433, NED 0.220632, BCFS 0.742250, BLEU 0.688228. That beats FeVeT's 0.673 by 0.06925.
- The claim's standalone checker, `python3 -I checker/check_q15.py . object/predictions-0.50.tsv`, printed:
  - "Mockingbird-I1 mean BCFS recomputed 0.6050308536957327, official 0.6050308536957327: EXACT"
  - "FeVeT published predictions mean BCFS 0.6423935720824072"
  - "object mean BCFS 0.7114179305724276 over 18101 items (claimed 0.7114179305724276): EQUAL"
  - "rebuilt official-format files equal to the frozen ones: 10 of 10"
  - "PASS"

## 3. Cognate Transformer (Akavarapu and Bhattacharya, EMNLP 2023)
- https://aclanthology.org/2023.emnlp-main.423.pdf: HTTP 200 at 2026-10-18T1151:15Z, sha256 4ede9ad5014866cdfa89f3a0f8eeaf754c50c8439284bb22e2ef7be7c766f38d. Text extracted with PDFKit.
- Table 5, test proportion 0.5:
  - CogTran-tiny 1.4521 / 0.3873 / 0.6257
  - CogTran-small 1.2786 / 0.3332 / 0.6477
  - Mockingbird-Inpaint 1.4170 / 0.3518 / 0.6050
- Appendix A, CogTran-small B-Cubed F by family at 0.5: 0.7027, 0.7143, 0.5335, 0.7161, 0.6197, 0.6863, 0.5261, 0.3637, 0.7504, 0.6444. The mean over the 10 families is 0.62572 (computed), which does not match Table 5's 0.6477. Either way, both values are below the claim.
- Observation: if Table 5 is on the official family scale (its Mockingbird value equals the official 0.6050), then CogTran-small's 0.6477 is above the claim's PREREG bar of 0.6424. The bar was not the highest published number. The claim still beats 0.6477 by 0.0637179306.
- The repository README (raw.githubusercontent.com mahesh-ak/CognateTransformer HEAD README.md, HTTP 200, 11:55:45Z) shows no published predictions and no newer scores.

## 4. Literature search, last 24 months (2024-10-18 to 2026-10-18)
- **ACL Anthology.** https://aclanthology.org/anthology+abstracts.bib.gz: HTTP 200 at 2026-10-18T11:49:27Z, 42574037 bytes, sha256 83b1de6e...6b5d. That is 131708 entries, through ACL 2026 (2026.acl-long 2223 entries), 2026.sigtyp-main, 2026.lchange-1, LREC 2026 and TACL/CL 2026. EMNLP 2026 is not yet in the Anthology.
  - I searched titles and abstracts (2023 onward) for reflex, ST2022, SIGTYP 2022, Mockingbird, cognate, proto-form, phonological reconstruction, sound correspondence and comparative method, and read every relevant abstract.
  - Only Cognate Transformer (2023.emnlp-main.423) reports reflex prediction on ST2022.
  - Newer related work reports no ST2022 surprise scores:
    - Lu, Wang and Mortensen, LREC-COLING 2024 (2024.lrec-main.762): Chinese and Romance protoforms.
    - Lu, Xie and Mortensen, ACL 2024 (2024.acl-long.788)
    - Dinu et al., EMNLP 2024 (2024.emnlp-main.362): Romance protowords.
    - Akavarapu and Bhattacharya, EACL 2024 (2024.eacl-long.58): cognate detection.
    - Blum and List, LChange 2026 (2026.lchange-1.6): irregularity detection.
    - Liu et al., ACL 2026 (2026.acl-long.831): Chinese dialects.
    - SIGTYP 2024, 2025 and 2026 papers: none on reflex prediction.
- **Europe PMC.** Two searches, HTTP 200 at 11:52:13Z and 11:54:56Z. Hits: FeVeT (doi 10.12688/openreseurope.20647.1) and Blum, Barrientos, Ingunza and List 2024, Sci. Rep., doi 10.1038/s41598-024-82515-3 (Panoan-Takanan, not the ST2022 surprise families). Also Lexibank 2 and List's "Open Problems". No ST2022 0.50 score.
- **Zenodo.** https://zenodo.org/api/records?q=...&size=25: HTTP 200 at 11:55:17Z, 13 hits. My first URL with size=50 returned HTTP 400, a validation error (not a stop code), and I corrected the size parameter. Hits include the FeVeT supplement (10.5281/zenodo.16813907, 2025-08-12), the 2022 ST2022 archive and the CEoT submission, and two 2026 forward-reconstruction resources for Spanish and Romanian (not ST2022). No new score.
- **GitHub repository search.** Five queries, all HTTP 200, 11:53:43Z to 11:53:46Z: reflex prediction, cognate reflex, sigtyp 2022, ST2022, sigtyp shared task cognate.
  - acraevschi/cognate_reflexes_task (pushed 2024-11-14): a University of Zurich course-project report. Fetched final_ML4NLP2_project_report.pdf, HTTP 200 at 11:54:22Z. Its Table 3 gives surprise data at 50%: Multilingual Transformer NED 0.3956, B-Cubed FS 0.5659, BLEU 0.4701, below Mockingbird-I1 (0.6050).
  - acraevschi/llm_cognate_reflexes (pushed 2026-07-12): a reconstruction workbench. Its README has no ST2022 scores.
  - LGirrbach/Cognate-Reflex-Prediction (2023): its README says TODO, no scores.
  - No other new ST2022 work.
- **Hugging Face papers index**, which covers part of arXiv. Two searches, HTTP 200 at 11:54:51Z and 11:54:53Z. Relevant hits are only 2403.18769 (Lu et al. 2024) and 2406.05930 (Lu et al. 2024). The index is incomplete: Cognate Transformer's arXiv version is not among its results.
- **OpenReview API**, which includes DBLP-imported records. Two searches, HTTP 200 at 11:57:28Z and 11:57:46Z. Only the 2023/2024 papers above appear; nothing new on cognate reflex prediction.
- **Not reached, by rule.** These hosts are in stop lists changed in the last 24 h, and I did not request them:
  - arxiv.org (429, 2026-10-17T22:56:05Z, other lane, host-level stop). I also made no request to any other arXiv host.
  - api.openalex.org and api.crossref.org (429)
  - api.semanticscholar.org (429)
  - dblp.org and scholar.archive.org (challenge)
- **api.github.com during this session.** Two other skeptics' requests got 403 at 2026-10-18T11:54:13Z, and lens N50 ruled a host-level stop at 11:55:06Z. My last api.github.com request was at 11:54:00Z, and my gh calls were at 11:46:27Z to 11:46:41Z. I made no api.github.com or gh request after the stop.
- My own requests got no 401, 403, 405, 429, 503 or challenge page. I added no line to the stop list; grep for B50 in it returns 0. Other responses I got were the Europe PMC full-text 500, the ORE v2 500 and the Zenodo 400. None is a stop code, and none was retried.
- **Residual risk.** I could not search arXiv directly, and the Anthology search covers titles and abstracts only. A preprint that exists only on arXiv, or a paper that mentions ST2022 only in its body, could have been missed. Given the margins below, I judge this risk low but not zero.
- injection_suspected: none seen.

## 5. Trophy case and V3R1T4S pull requests
- repo/TROPHY_CASE.md (sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9, 100 lines): no line matches sigtyp, st2022, cognate, reflex, mockingbird, fevet, proto, lexib, linguist, wordlist or BCFS (grep exit 1).
- `gh pr list -R elder-plinius/V3R1T4S --state all --limit 1000`, run 2026-10-18T11:46:27Z to 11:46:30Z:
  - It returned 388 PRs (155 CLOSED, 142 MERGED, 91 OPEN), the newest #398 at 2026-10-18T10:56:07Z.
  - I searched title, body and branch names for sigtyp, st2022, cognate, reflex, mockingbird, fevet, proto-form, lexibank, BCFS, B-Cubed, wordlist and "surprise famil": 0 matches.
  - `gh pr list --search` for sigtyp, cognate, reflex, ST2022, Mockingbird and FeVeT: 0 hits each.
  - The 12 newest PRs (#387 to #398) are on covering designs, bank facts, percolation and Condorcet domains.

## Best published value at 0.50 on mean BCFS
On the official family-averaged scale, the best published value is CogTran-small 0.6477 (Akavarapu and Bhattacharya, EMNLP 2023, Table 5, repeated in FeVeT Table 3). This assumes Table 5 is on that scale; its own appendix averages to 0.62572 over families. FeVeT's published per-item predictions rescored with the pinned official scorer give 0.6423935720824072. The best official ST2022 entry is CrossLingference-Julia at 0.6193241007226449, and Mockingbird-I1 is at 0.6050308536957327. The highest number printed on any scale is FeVeT (Wientzek 2025, ORE 5:174, Table 3) at 0.673, a mean over 99 languages.

Margins of the claimed 0.7114179305724276, all computed:
| compared with | margin | strictly beaten |
|---|---|---|
| FeVeT 0.673 (language-pooled) | 0.0384179306 | True (and 0.06925 on the same language-pooled scale: 0.742250 vs 0.673) |
| CogTran 0.6477 | 0.0637179306 | True |
| FeVeT rescored 0.6423935720824072 | 0.0690243585 | True |
| FeVeT finetuned family file 0.6418 | 0.0696179306 | True |
| CogTran appendix family mean 0.62572 | 0.0856979306 | True |
| CrossLingference-Julia 0.6193241007226449 | 0.0920938298 | True |
| Mockingbird-I1 0.6050308536957327 | 0.1063870769 | True |
| course-project report 0.5659 | 0.1455179306 | True |

No value equals the claim, so there is no tie.

novelty: the claimed mean BCFS 0.7114179305724276 at proportion 0.50 on the 10 SIGTYP 2022 surprise families is above every published value I could reach honestly, on the official scale and on FeVeT's language-pooled scale. arXiv could not be searched directly because of a host-level stop, and that gap remains.

pass: true