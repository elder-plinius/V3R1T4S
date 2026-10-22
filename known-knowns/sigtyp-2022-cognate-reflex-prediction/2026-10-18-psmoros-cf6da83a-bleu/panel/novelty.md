(Saved by the main session at 2026-10-18T12:37:59Z from the novelty skeptic subagent's returned text (cell L50; Opus 5.5, agent a822fe9630e019aef); the subagent could not write a file named like a report. Text verbatim below.)

# NOVELTY skeptic, cell L50 (proportion 0.50, mean BLEU), run 2026-10-18-0839

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
start: 2026-10-18T11:44:33Z (date -u)
end: 2026-10-18T12:00:34Z (date -u)
material used: the claim package only (files named relative to claim/), kit RULES.md, TROPHY_CASE.md. Web access went only through the shared fetch helper: one plain GET per resource, a User-Agent naming V3R1T4S, and the stop lists checked by the helper before each request. Scoring used the scorer interpreter (SCO) and the system python3.13.

## Result (one sentence)
I found no published score on the SIGTYP 2022 surprise test families at proportion 0.50 whose mean BLEU on the official family-averaged scale reaches the candidate's 0.6520222200978466. The highest published BLEU is Mockingbird-I1's official 0.5337187296541888. The best value known on that scale is 0.5768215755932388, from FeVeT's published per-item predictions rescored with the pinned scorer (this is the claim's bar). The candidate beats both strictly. (KNOWN for the statuses, NUMERICAL for the rescoring.)

## 1. Status source
status_source: https://github.com/sigtyp/ST2022 HTTP 200 fetched 2026-10-18T11:45:08Z
- Helper output: `200 e4e957a98f69234c88aada08f68f0bfbaeb348992abf95972e4a3dfa6010455f 344669 2026-10-18T11:45:08Z`
  - title: "GitHub - sigtyp/ST2022: SIGTYP 2022 Shared Task · GitHub"
  - embedded `"currentOid":"03094435cba4293ce0eea383036cab78499ad50d"`
  - "142 Commits"
  - top-level folders: data, data-surprise, results, src, systems
- https://api.github.com/repos/sigtyp/ST2022/commits?per_page=5 gave `200 7b881c75158171750f802d30b85b67bcbe949a72f7d5a4588a5ea6914af2eb0c 11624 2026-10-18T11:45:13Z`. Newest commits:
  - 03094435cba4293ce0eea383036cab78499ad50d 2022-05-27T07:58:23Z 'update for final release'
  - 9d4202ee05ea441b686fcbbadc23057c412d08fb 2022-05-27T07:54:43Z 'update'
  - c223f851e2c1b8616692d57b77debcc5ffc706ce 2022-05-27T07:02:55Z 'update with final results'
  - 4a1331bff978e9772b8ff9959808f6129e5e8f06 2022-05-23T06:06:15Z 'Merge pull request #46 from gcelano/main'
  - 5a0be5ecf77593596bdb5cefecc40900224ce628 2022-05-22T19:05:05Z 'correction decoding'
  - The response is byte-identical to scout/st2022_commits.json (cmp: identical; same sha256).
- https://raw.githubusercontent.com/sigtyp/ST2022/03094435cba4293ce0eea383036cab78499ad50d/results/results-surprise-0.50.json gave `200 3a8e79f9e686a4835f6bd0948529838b4ebb38ef2f02e05d39dfa73389a014f3 14362 2026-10-18T11:45:35Z`.
  - It is byte-identical to official/results/results-surprise-0.50.json (cmp: identical).
  - Official totals [ED, NED, BCFS, BLEU] at 0.50:

| system | ED | NED | BCFS | BLEU |
|---|---|---|---|---|
| CEoT-Extalign-RF | 1.8434144439390892 | 0.45758030716855247 | 0.5193785774155593 | 0.4128463684661985 |
| Baseline-Baseline-SVM | 1.9330343853457885 | 0.4618527113479192 | 0.5371316867267996 | 0.42042502779630175 |
| Baseline-Baseline | 1.8888996360679713 | 0.4445382690345965 | 0.5616582507069442 | 0.4265482031009145 |
| CrossLingference-Julia | 1.6793831176401144 | 0.4274274213553069 | 0.6193241007226449 | 0.4296245318898906 |
| Mockingbird-I1 | 1.4169823165005235 | 0.35176136367373956 | 0.6050308536957327 | 0.5337187296541888 |
| Mockingbird-N1-A | 1.5526682275025492 | 0.37999052172679176 | 0.595911890890592 | 0.4934374243018119 |
| Mockingbird-N1-B | 1.5065986385601715 | 0.3733789322481769 | 0.5863575276995412 | 0.49889009875615786 |
| Mockingbird-N1-C | 1.5817967704709075 | 0.3950045195670149 | 0.5609897492206023 | 0.4748524033538319 |
| Mockingbird-N2 | 0 | 0 | 0 | 0 |
| Leipzig-Transformer | 2.103578503152309 | 0.5256730055461115 | 0.4305519248730835 | 0.343787001129339 |

- Conclusion: there has been no commit since 2022-05-27T07:58:23Z, and the official 0.50 results file at the pinned commit is unchanged. The best official BLEU is Mockingbird-I1's 0.5337187296541888.

## 2. FeVeT (Wientzek 2025, Open Research Europe 5:174, github.com/TGH-2020/FeVeT)
**Repository state and file identity**
- https://api.github.com/repos/TGH-2020/FeVeT/commits?per_page=5 gave `200 4ed6f1469db77527e094ec22d44ddb3278cdc0ee9ad8b5de120693b19c454dc0 21645 2026-10-18T11:45:14Z`.
  - It is byte-identical to scout/fevet_commits.json.
  - HEAD is 31898c53bfffeef87265efa8a780b7be740162d1, 2025-11-28T17:00:16Z, 'Update README.md'. Before it: e4d5597f 2025-08-12 'Update metrics.py'; 77d6320b and 321196c2 2025-06-08; 96d8058d 2025-06-06.
- The recursive git tree at 31898c53 gave `200 67f23d43eba1a5bc24ba2e5c77e2ce55bae2e31ba5b3900ded5f75ab5c5a2a48 280670 2026-10-18T11:46:17Z` (truncated False, 1090 entries).
  - I compared the git blob sha1 of each fevet/pred_0.50_FAM.tsv with the blob of results/predictions/reflex/FAM/s2s_reflex_0.50_predictions.tsv: "matched 10 of 10". Example: bantubvd 9f69914b2115012224296a828b5b9d120e36b287 on both sides.

**What FeVeT prints**
- Raw result files at 31898c53, each 200 between 2026-10-18T11:46:45Z and 11:46:47Z:
  - results/s2s_reflex_avg.txt, row 0.50: ED 1.2405, NED 0.3222, B3_F1 0.6426.
  - results/s2s_reflex_finetuned_avg.txt, row 0.50: ED 1.1111, NED 0.2825, B3_F1 0.673.
  - Every FeVeT result file has only the columns ED, NED and B3_F1. FeVeT publishes no BLEU.
- The paper, through the ORE XML export https://open-research-europe.ec.europa.eu/extapi/article/xml?doi=10.12688/openreseurope.20647.1 (`200 320a1e5af399ff68bf4863518946f97e54bcdf3494b0678a0753b00c16b7e93f 214948 2026-10-18T11:56:48Z`):
  - Table 3 at 0.5:
    - CognateTransformer: 1.2786 / 0.3332 / 0.6477
    - FeVeT (no fine-tuning): 1.2405 / 0.3222 / 0.6426
    - FeVeT: 1.1111 / 0.2825 / 0.673
    - IPA-only: 2.508 / 0.6642 / 0.4489
  - "BLEU" occurs 0 times in the article.
  - Europe PMC lists only version 1 (DOI 10.12688/openreseurope.20647.1, 2025-06-30): hitCount 1.
  - The ORE HTML page (https://open-research-europe.ec.europa.eu/articles/5-174, 200 at 2026-10-18T11:51:04Z, 55677 bytes) is a JavaScript shell with no text. It is not a challenge page.

**Scale check (the paper prints language-pooled averages)**
- I averaged FeVeT's own per-language result files over all 99 languages:
  - "non-ft pooled mean over languages: ED 1.2405 NED 0.3222 BC 0.6426"
  - "ft pooled mean over languages: ED 1.1111 NED 0.2825 BC 0.6730"
  - These are exactly the printed averages, so the printed numbers are pooled means over 99 languages, not the official mean over 10 families.
- The same fine-tuned per-language results averaged within each family, then over the 10 families: "ED 1.272524 NED 0.311049 BC 0.641802 families 10". These come from FeVeT's own metric code, not the official scorer.

**Rescoring on the official scale (my own script)**
- Method:
  - Scorer: the official compare_words from the pinned sigtypst2022.py in the SCO interpreter (sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a, identical to official/src/sigtypst2022.py), with matplotlib stubbed.
  - Family value: the TOTAL row. System value: statistics.mean over the 10 families.
  - Two summation modes: left-to-right (sum shadowed in sigtypst2022 and lingrex.util) and builtin.
- Converting FeVeT's predictions to the official wide format:
  - 18101 items in total (bantubvd 816, beidazihui 4921, birchallchapacuran 683, bodtkhobwa 3426, bremerberta 366, deepadungpalaung 1450, hillburmish 1638, kesslersignificance 353, luangthongkumkaren 1444, wangbai 3004).
  - gold_mismatch 0 (FeVeT's GOLD column equals official/data-surprise/FAM/solutions-0.50.tsv), missing 0, extra 0.
- Output [ED, NED, BCFS, BLEU]:
  - ltr Mockingbird-I1: [1.4169823165005235, 0.35176136367373956, 0.6050308536957327, 0.5337187296541888]
    - "ltr Mockingbird-I1 total equal to official: True"
    - "ltr Mockingbird-I1 every family equal: True"
  - ltr candidate: [1.0166617451971307, 0.24912258145405175, 0.7114179305724276, 0.6520222200978466]
  - ltr FeVeT-published: [1.286021835157271, 0.30880111347517586, 0.6423935720824072, 0.5768215755932388]
  - builtin BLEU: Mockingbird-I1 0.5337187296541887, candidate 0.6520222200978465, FeVeT-published 0.5768215755932388
  - "BLEU candidate-FeVeT ltr 0.07520064450460784 builtin 0.07520064450460773"
  - "BLEU candidate-Mockingbird ltr 0.11830349044365784"
- Per-family BLEU, ltr:

| family | candidate | FeVeT | Mockingbird-I1 |
|---|---|---|---|
| bantubvd | 0.6149144814770632 | 0.592530385802995 | 0.4986880940054677 |
| beidazihui | 0.845286843153689 | 0.7925699791020799 | 0.8001936139106623 |
| birchallchapacuran | 0.5450834358387138 | 0.42729160678332 | 0.3544929894676464 |
| bodtkhobwa | 0.8165114562863156 | 0.7606573057195887 | 0.7101300613249889 |
| bremerberta | 0.6216615225364938 | 0.5154666818090824 | 0.5597163129710025 |
| deepadungpalaung | 0.7044831616267102 | 0.567108229282128 | 0.42755111818027175 |
| hillburmish | 0.5878449397558231 | 0.520134714432988 | 0.44774522451899657 |
| kesslersignificance | 0.2532084192888352 | 0.18794017672637114 | 0.15351700479784142 |
| luangthongkumkaren | 0.8426359713006655 | 0.7631365402270252 | 0.7803301833566277 |
| wangbai | 0.6885919697141568 | 0.6413801360468095 | 0.6048226940083821 |

- The claim's bar, 0.5768215755932388, is confirmed in both summation modes.

**Which FeVeT run produced the published predictions**
- The published per-item predictions reproduce neither of FeVeT's printed per-language tables exactly.
  - bantubvd language 1: the mean Levenshtein distance of the published predictions is 1.3987 (n 153).
  - FeVeT prints 1.3595 for that language without fine-tuning and 1.2876 with fine-tuning.
- So the published files come from a run other than the one behind the printed tables.
- For this cell it changes nothing, because no FeVeT variant has a published BLEU. The only FeVeT BLEU on the official scale is the rescored published predictions.
- On FeVeT's own numbers, the fine-tuned model sits at family-averaged NED 0.311 and BC 0.642. That is close to the rescored published predictions (NED 0.3088, BCFS 0.6424) and far from the candidate (NED 0.2491, BCFS 0.7114). A fine-tuned FeVeT BLEU above 0.652 is therefore implausible (HEURISTIC), and in any case it is not published.

**The claim's own checker**
`python3 -I checker/check_q15.py . object/predictions-0.50.tsv` printed:
```
1. Mockingbird-I1 mean BLEU recomputed 0.5337187296541888, official 0.5337187296541888: EXACT
2. FeVeT published predictions mean BLEU 0.5768215755932388
3. object mean BLEU 0.6520222200978466 over 18101 items (claimed 0.6520222200978466): EQUAL
   margin vs Mockingbird-I1 0.118303490444 (higher is better)
   margin vs FeVeT 0.075200644505 (higher is better)
4. rebuilt official-format files equal to the frozen ones: 10 of 10
PASS
```

## 3. Cognate Transformer (Akavarapu and Bhattacharya, EMNLP 2023)
- https://aclanthology.org/2023.emnlp-main.423.pdf gave `200 4ede9ad5014866cdfa89f3a0f8eeaf754c50c8439284bb22e2ef7be7c766f38d 309405 2026-10-18T11:50:12Z`.
  - Table 5 at 0.5 [ED, NED, BC]:
    - CogTran-tiny: 1.4521 / 0.3873 / 0.6257
    - CogTran-small: 1.2786 / 0.3332 / 0.6477
    - Mockingbird-Inpaint: 1.4170 / 0.3518 / 0.6050 (the official scale)
  - "BLEU" occurs 0 times in the paper.
- github.com/mahesh-ak/CognateTransformer:
  - commits: 200 at 2026-10-18T11:50:32Z; newest 4da845d4f49c055b82ee4a1c98bfc1f5333c07c3, 2023-12-18T09:16:53Z, 'Added citation'.
  - tree: 200 at 11:50:40Z; results/ holds aggregates only, no per-item reflex predictions.
  - results/reflex_small.tsv (200 at 11:50:55Z), row 0.50: ED 1.2786, NED 0.3332, B3_F1 0.6477.
  - reflex_small_detailed.tsv: 0 BLEU mentions.
- So Cognate Transformer has no published BLEU at 0.50, and its predictions are not available for rescoring.

## 4. Literature search, last 24 months (2024-10-18 to 2026-10-18)
**ACL Anthology**
- https://aclanthology.org/anthology+abstracts.bib.gz gave `200 83b1de6eb8e9af0abd7106886ba7e6decbded519ff6d1259bbb94c8286fa6b5d 42574037 2026-10-18T11:48:34Z`.
  - "entries 131708"; "max year 2026"; counts 2024: 12135, 2025: 14931, 2026: 10822.
- Narrow pass over titles and abstracts (reflex prediction | cognate reflex | SIGTYP 2022 | ST2022 | Mockingbird | prediction of cognate | cognate prediction | FeVeT | Cognate Transformer): 19 entries, none inside the window.
  - The newest are 2024.eacl-long.58 (cognate detection, March 2024) and 2024.lrec-main.762 (protoform reconstruction reranked by reflex prediction, May 2024).
- Broad pass over 2024-2026 (reflex | cognate | protoform | proto-language | phonological reconstruction | sound correspondence | comparative method | historical linguistic | sound change): 97 entries. I read the abstracts of the related ones; none scores the ST2022 surprise test:
  - 2026.lchange-1.6 (Blum and List, irregular cognate sets)
  - 2026.acl-long.831 (Middle Chinese sound law induction)
  - 2026.findings-acl.432 and 2025.acl-long.1432 (sound law induction as programming by example)
  - 2025.acl-long.876 (language affiliation)
  - 2025.sigtyp-1.6 (Beyond cognacy)
  - 2024.emnlp-main.362 (Romance protowords)
  - 2024.acl-long.788 (semisupervised reconstruction)
  - 2024.cawl-1.7 and 2024.sigtyp-1.11
- I also listed every title of SIGTYP 2025 (16 entries), SIGTYP 2026 (7) and LChange 2026 (14): none is on reflex prediction.

**arXiv** (through export.arxiv.org; the host arxiv.org is on a stop list and was not requested)
- Query "reflex prediction" OR "cognate reflex" OR "cognate reflexes" OR "SIGTYP 2022" OR "predicting reflexes" (200 at 2026-10-18T11:53:12Z): 7 results. The newest is 2403.18769 (2024-03-27, protoform reranking), outside the window.
- Query cognate AND (prediction OR reconstruction OR reflex OR reflexes OR protoform) (200 at 11:53:21Z): 48 results, 12 since 2024-09. I read the three possibly related abstracts (2604.22730 Bantu lexical structure, 2604.00023 Sulawesi substrate, 2506.10614 unsupervised Latin protoforms): none is on ST2022 reflex prediction.
- An id_list lookup (200 at 11:53:02Z) showed that 2512.01713 is "Self-Supervised Borrowing Detection on Multilingual Wordlists" (2025-12-01, cites FeVeT); 2406.05930 and 2310.07487 are known reconstruction papers.

**Europe PMC**
- Search (200 at 2026-10-18T11:51:44Z): hitCount 7.
- In the window: Blum et al., Sci Rep, 2024-12-24, "Cognate reflex prediction as hypothesis test for a genealogical relation between the Panoan and Takanan language families". In its full text (PMC11668889, `200 5162d324fa63a8e28e88a3d5ba62bfbbf783c33c3b541ee4efe8aa71e1063488 123260 2026-10-18T11:53:39Z`), SIGTYP 2022 appears only in the reference list. "BLEU", "Mockingbird" and "B-Cubed" do not occur, and there is no ST2022 test score.

**OpenCitations (index v2)**
- Citing works of the task paper 10.18653/v1/2022.sigtyp-1.7 (200 at 2026-10-18T11:52:27Z): 9.
- Citing works of the Mockingbird paper 10.18653/v1/2022.sigtyp-1.9 (200 at 11:52:45Z): 8.
- Citing works of FeVeT 10.12688/openreseurope.20647.1 (200 at 11:52:47Z): 1.
- Citing works of Cognate Transformer 10.18653/v1/2023.emnlp-main.423 (200 at 11:52:48Z): 5.
- Citing works inside the window:
  - FeVeT itself
  - the Sci Rep paper above
  - arXiv 2512.01713 (borrowing detection)
  - 10.1109/iccies63851.2025.11032538, "Reconstructing Proto-Languages Using Neural Machine Translation And Deep Learning" (2025-04-24; title from OpenCitations Meta, 200 at 11:54:00Z). Its full text could not be read: IEEE served a challenge (section 6).
  - 10.64898/2026.01.18.700141, "Ancestral Sequence Reconstruction Using Generative Models" (2026-01-21, biology)
- osf.io/628cv (OSF API, 200 at 11:53:47Z) is a Trans-New Guinea phylogenetics preprint (2024-05-24), outside the window and off topic.

**GitHub repository search**
- Four queries were answered (200 at 2026-10-18T11:54:11Z to 11:54:13Z): reflex+prediction (total 19), sigtyp+2022 (6), cognate+reflex (5), ST2022+cognate (0). The fifth got 403 (section 6).
- ST2022-related repositories pushed inside the window:
  - cognate_reflexes_task (pushed 2024-11-14). Its README (200 at 11:54:56Z) says it "performs on par with Mockingbird team's Transformer model" and gives no number. That level is Mockingbird's N1 models, official BLEU 0.4748524033538319 to 0.49889009875615786 at 0.50.
  - llm_cognate_reflexes (pushed 2026-07-12). Its README (200 at 11:54:56Z) describes a proto-form reconstruction agent toolkit and reports no ST2022 score.

**Zenodo API**
- Page size 25 (200 at 2026-10-18T11:58:36Z): total 13 records.
- Inside the window: FeVeT supplementary material (2025-08-12), Lexibank 2 (2025), and the Spanish and Romanian forward-reconstruction resources (2026). None gives ST2022 scores.

**Older known sources**
- The Mockingbird paper (https://aclanthology.org/2022.sigtyp-1.9.pdf, 200 at 2026-10-18T11:58:08Z), Table 3 (0.50), line "surprise total": BLEU 0.43, 0.53, 0.49, 0.50 and 0.47 (best 0.53, the I1 model).
- Helpful Neighbors, TACL 2023 (https://aclanthology.org/2023.tacl-1.6.pdf, 200 at 11:59:29Z), gives only shared-task ranks.

## 5. TROPHY_CASE.md and V3R1T4S pull requests
- **TROPHY_CASE.md** (100 lines, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9): grep for sigtyp | cognate | reflex | st2022 | mockingbird | fevet | proto | Q15 | lexibank | quarry gives 0 lines. Its families are degree-diameter graphs, Lehmer, matrix multiplication, VNN-COMP, RobustBench, constant-weight codes and cipher commitments.
- **gh was not used.** api.github.com became a stopped host for the NOVELTY lenses (403 rate limit at 2026-10-18T11:54:13Z, in the stop list), so I read the github.com pages through the helper instead.
- Newest pull requests page (https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+sort%3Acreated-desc, 200 at 2026-10-18T11:55:24Z):
  - totalCount 388 (openCount 91, closedCount 297); newest #398, created 2026-10-18T10:56:07Z.
  - Seven pull requests were created after the scout's snapshot (#392 to #398, 2026-10-18T08:51:20Z to 10:56:07Z). Their topics are covering designs and bank pages (C_3a and sunflower, alphaevolve constants, BB(6), live values, DNA codes). None is on this target.
- Searches is:pr sigtyp, is:pr cognate and is:pr reflex (200 at 11:55:48Z, 11:55:52Z and 11:55:56Z): openCount 0 and closedCount 0 each.
- Positive control is:pr condorcet (200 at 11:56:23Z): totalCount 12. So the search works without a login.
- The scout's list (scout/v3r1t4s_all_prs.json, 381 pull requests, newest 2026-10-18T08:02:36Z) has 0 title hits for the same keywords.

## 6. Refused, blocked or failed requests (kit rule 5)
- **403, api.github.com, 2026-10-18T11:54:13Z.** URL: https://api.github.com/search/repositories?q=reflex+prediction+in:readme&sort=updated&order=desc&per_page=100 ("API rate limit exceeded"). The helper wrote it to the session stop list with lens L50-NOVELTY. It was not retried, and this lens made no further api.github.com request.
- **Challenge, ieeexplore.ieee.org, 2026-10-18T12:00:03Z.** URL: https://ieeexplore.ieee.org/document/11032538 (HTTP 202 with an empty body). The stop-list line is at 12:00:04Z with lens L50-NOVELTY. Not retried.
- **Refused by the helper before any request:** api.openalex.org (host stopped by another lane's 429 at 2026-10-17T21:44:03Z).
- **Not attempted because they are on stop lists:** api.semanticscholar.org, api.crossref.org, dblp.org, scholar.archive.org, arxiv.org.
- **500 from Europe PMC** fullTextXML for PPR1043857, 2026-10-18T11:56:39Z. This is a server error, not a block status. Not retried; I read the article through the ORE XML export instead.
- **400 from Zenodo** at 11:58:18Z ("Page size cannot be greater than 25"). This was my parameter error, not a block. One corrected request with size 25 followed.

injection_suspected: none observed.

## 7. Best published value at 0.50 on mean BLEU
- **Highest printed BLEU:** Mockingbird-I1, 0.5337187296541888 (official results-surprise-0.50.json, sigtyp/ST2022 at 03094435; system by Kirov, Sproat and Gutkin 2022; task by List, Vylomova, Forkel, Hill and Cotterell 2022). FeVeT and Cognate Transformer print no BLEU.
- **Best known value on the official scale:** FeVeT's published per-item predictions (Wientzek 2025, github.com/TGH-2020/FeVeT at 31898c53) rescored with the pinned scorer, 0.5768215755932388. This is the claim's bar.
- **Nothing newer** was found in the ACL Anthology, arXiv, Europe PMC, OpenCitations, GitHub, Zenodo, Open Research Europe, TROPHY_CASE.md or the V3R1T4S pull requests.
- **Candidate:**
  - 0.6520222200978466 (left-to-right) and 0.6520222200978465 (builtin).
  - Above FeVeT rescored by 0.07520064450460784 (ltr) and 0.07520064450460773 (builtin).
  - Above Mockingbird-I1 by 0.11830349044365784.
  - The win is strict, not a tie.

## Needs you (residual risk, does not change the verdict)
- I could not read the full text of the IEEE ICCIES 2025 paper 10.1109/iccies63851.2025.11032538 (challenge). Its title says proto-language reconstruction; a human can check it by hand.
- OpenAlex, Semantic Scholar, Crossref, dblp and Google Scholar were not used because their hosts are stopped. Citation coverage rests on the ACL Anthology bibliography, the arXiv API, Europe PMC, OpenCitations, GitHub, Zenodo and Open Research Europe.
- Observation, not a flaw of this claim: FeVeT's published 0.50 per-item predictions do not exactly match its printed per-language tables (section 2).

pass: true