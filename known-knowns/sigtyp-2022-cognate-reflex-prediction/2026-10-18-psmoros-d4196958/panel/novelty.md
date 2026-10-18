(Saved by the main session at 2026-10-18T13:18:27Z from the novelty skeptic subagent's returned text (cell L30; Opus 5.5, agent a9ae1b918ce5ff58f); the subagent could not write a file named like a report. Text verbatim below.)

# NOVELTY skeptic, cell L30 (proportion 0.30, mean BLEU), private-quarry-B (charter Q15, SIGTYP 2022 surprise families)

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: NOVELTY (one of three skeptics; I saw only the claim package, the kit rules and TROPHY_CASE.md)
start: Sun Oct 18 12:53:16 UTC 2026 (date -u)
end: Sun Oct 18 13:11:18 UTC 2026 (date -u)

status_source: https://github.com/sigtyp/ST2022 HTTP 200 fetched 2026-10-18T12:55:22Z

## Verdict in one sentence
At proportion 0.30, the claimed object combiner/test/0.30 has mean BLEU 0.6874377388475998 on the official family-averaged scale (pinned ST2022 scorer). That is strictly higher than every value I know or found: our own earlier bar bar_comb_new/test/0.30 0.6839233380559118, FeVeT's published per-item predictions rescored 0.6356571184958077, and Mockingbird-I1 official 0.6058548112827981. A search of the literature from the last 24 months found no published score at 0.30 on mean BLEU for the 10 surprise families. novelty: no prior or concurrent value found that ties or beats the claim (NUMERICAL for the scores, KNOWN for the literature status as of the fetch times below).

## Fetch discipline (kit rule 5)
- Every web request went through the session's shared fetch helper (vfetch.py get ... --lens L30-NOVELTY). That is one plain GET with a V3R1T4S User-Agent. Before each GET, a `vfetch.py check` read the stop lists.
- Stop lists read at start: the session list plus every stops-*.tsv changed in the last 24 h in both workspaces. Hosts the helper refused, so I sent no request to them: api.github.com (host-level stop, ALL), arxiv.org (429 in another lane), api.openalex.org, api.crossref.org, api.semanticscholar.org, dblp.org, scholar.archive.org and ieeexplore.ieee.org. As instructed, I used no gh and no GitHub API calls. For pull requests I used the plain github.com pages instead.
- Decision about export.arxiv.org: this is arXiv's API host. It is a different host from arxiv.org, it has no stop line, and the helper allowed it. The arxiv.org stop is a 429 on a cs.GT listing page in another lane at 2026-10-17T22:56:05Z. I sent 5 export.arxiv.org API GETs, 4 s or more apart, and none was blocked. A stricter reading could count this as reaching arXiv after an arxiv.org stop, so I record it here.
- Blocks: none. No request got 401, 403, 405, 429, 503 or a challenge page. The session stop list has 4 lines, and none is from L30 (grep -c L30 gives 0).
- One non-block error: Zenodo returned HTTP 400 "Page size cannot be greater than 25" on size=100. I then sent one GET each to the corrected URLs (size=25). This is not a retry of a blocked request.
- injection_suspected: none seen.

## 1. Status source (one GET)
- `vfetch.py get https://github.com/sigtyp/ST2022` gave: `200 e3fc969175ebcb7d362a6e2d8a9aa24d0054f5b7111a3c1a39da95e5b042c41f 344670 2026-10-18T12:55:22Z`
- Page title: "GitHub - sigtyp/ST2022: SIGTYP 2022 Shared Task · GitHub". "currentOid":"03094435cba4293ce0eea383036cab78499ad50d". "commitCount":"142". defaultBranch "main". The top-level tree is unchanged: cldf-data, data-surprise, data, results, src, systems, tests, and the root files. The word "captcha" appears twice, both times inside GitHub feature-flag names (octocaptcha_origin_optimization, swp_forms_disable_octocaptcha). It is not a challenge page.
- Compared with scout/st2022_repo_page.html (also 344670 bytes, sha256 027feb55...): the only differences are per-request nonces, request ids and tooltip ids.
- Newest commit date, from one GET of https://github.com/sigtyp/ST2022/commits/main/: `200 4ed4c379b61bef184d5a0cf44a1ba6ac921cf5e9ad57071c3459c7efcbfe011d 451491 2026-10-18T12:55:57Z`. Newest commits: 03094435cba4293ce0eea383036cab78499ad50d at 2022-05-27T09:58:23.000+02:00 ("update for final release"), 9d4202ee05ea441b686fcbbadc23057c412d08fb at 2022-05-27T09:54:43+02:00, c223f851e2c1b8616692d57b77debcc5ffc706ce at 2022-05-27T09:02:55+02:00. The head is the pinned commit named in scout/scout.md, so the repository is unchanged since 2022.
- Official results are unchanged. One GET of https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.30.json gave `200 cca55c5fffa730c29ef578f022741f3a0378ca333e5a20493e23e2d400792563 14361 2026-10-18T12:56:07Z`. cmp against official/results/results-surprise-0.30.json: IDENTICAL.
- Ranking by total BLEU in that file: Mockingbird-I1 0.6058548112827981; Mockingbird-N1-B 0.5791625685444537; Mockingbird-N1-A 0.5779469689176259; Mockingbird-N1-C 0.5636298574483483; Baseline-Baseline-SVM 0.5554196432327262; CEoT-Extalign-RF 0.5286024411099635; Baseline-Baseline 0.5195251805013861; CrossLingference-Julia 0.4503387270234224; Leipzig-Transformer 0.420650747918691; Mockingbird-N2 0 (no 0.30 submission).

## 2. Re-scoring of the compared values (my own script, official scorer)
Integrity: `shasum -a 256 -c MANIFEST.sha256` gave 364 OK. The claim has 364 files besides MANIFEST.sha256.

The scorer module in the calibrator interpreter is byte-identical to official/src/sigtypst2022.py (both sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a).

I wrote my own script (score_all.py, skeptic scratch outside the claim). It calls compare_words(official/data-surprise/FAM/solutions-0.30.tsv, RESULT, report=False)[-1][1:] and takes statistics.mean over the 10 families, with builtin sum replaced by a left-to-right loop in the sigtypst2022 and lingrex.util namespaces. For FeVeT, it builds an official-format result file from fevet/pred_0.30_FAM.tsv. Output (left-to-right):
```
mockingbird-i1  ED 1.1762187506031638 NED 0.2898984929868421 BCFS 0.6717099225519634 BLEU 0.6058548112827981
candidate       ED 0.8901395410281422 NED 0.22149461586532132 BCFS 0.7502543049557795 BLEU 0.6874377388475998
bar_comb_new    ED 0.9027034122955315 NED 0.22327922550091464 BCFS 0.7488264857956657 BLEU 0.6839233380559118
fevet           ED 1.0946456488227652 NED 0.2632988364952282 BCFS 0.6986581179861967 BLEU 0.6356571184958077
official Mockingbird-I1 total [1.1762187506031638, 0.2898984929868421, 0.6717099225519634, 0.6058548112827981]
calibration per-family equality: True
candidate - bar_comb_new BLEU: 0.003514400791688077
candidate - fevet BLEU: 0.051780620351792095
candidate - mockingbird BLEU: 0.08158292756480179
```
Per-family BLEU (candidate, bar_comb_new, fevet, mockingbird):
```
  bantubvd             0.675209 0.674102 0.626373 0.582785
  beidazihui           0.834813 0.833598 0.795830 0.817141
  birchallchapacuran   0.564429 0.558037 0.488664 0.429211
  bodtkhobwa           0.856624 0.855352 0.831754 0.769006
  bremerberta          0.656938 0.655421 0.568380 0.638334
  deepadungpalaung     0.769183 0.769578 0.673530 0.568918
  hillburmish          0.647174 0.642279 0.630980 0.577302
  kesslersignificance  0.251134 0.236396 0.194554 0.150429
  luangthongkumkaren   0.872633 0.872417 0.832815 0.828464
  wangbai              0.746241 0.742054 0.713692 0.696957
```
The candidate is lower than the bar on 1 of the 10 families (deepadungpalaung). The mean is what counts.

Compensated summation (same script with builtin sum kept, Python 3.13.2):
```
candidate       ... BLEU 0.6874377388475998
bar_comb_new    ... BLEU 0.6839233380559119
fevet           ... BLEU 0.6356571184958079
mockingbird-i1  ... BLEU 0.6058548112827982
candidate - bar_comb_new BLEU: 0.003514400791687966
```
Both modes match CLAIM.md exactly: 0.6874377388475998, with margins 0.003514400791688077 (left-to-right) and 0.003514400791687966 (compensated).

FeVeT rescoring check, which the prompt asked for: for every family, the FeVeT rows cover every gold item at 0.30, and the GOLD column equals the official solutions-0.30 cell in every row (gold_mismatch 0). Rows: bantubvd 582, beidazihui 2945, birchallchapacuran 470, bodtkhobwa 2200, bremerberta 243, deepadungpalaung 941, hillburmish 1109, kesslersignificance 252, luangthongkumkaren 912, wangbai 1932, for 11586 in total. The claim's FeVeT value 0.6356571184958077 is confirmed.

Standalone checker: `python3.13 -I checker/check_q15.py . object/predictions-0.30.tsv` ended with `exit 0`:
```
1. Mockingbird-I1 mean BLEU recomputed 0.6058548112827981, official 0.6058548112827981: EXACT
2. FeVeT published predictions mean BLEU 0.6356571184958077
2. earlier object bar_comb_new/predictions-0.30.tsv mean BLEU 0.6839233380559118 (stated 0.6839233380559118): EQUAL
3. object mean BLEU 0.6874377388475998 over 11586 items (claimed 0.6874377388475998): EQUAL
   margin vs Mockingbird-I1 0.081582927565 (higher is better)
   margin vs FeVeT 0.051780620352 (higher is better)
   margin vs bar_comb_new/predictions-0.30.tsv 0.003514400792 (higher is better)
4. rebuilt official-format files equal to the frozen ones: 10 of 10
PASS
```
I also scored the six packaged entries at 0.30 (my score_entries.py, left-to-right) to confirm that none beats the object:
```
broker/PRIMARY         ... BLEU 0.6773572720481368
analogist/SECONDARY    ... BLEU 0.674666799591828
broker/SECONDARY       ... BLEU 0.6698786005734902
phylo/PRIMARY          ... BLEU 0.6596514642479974
analogist/PRIMARY      ... BLEU 0.6583352796054924
classifier/PRIMARY     ... BLEU 0.6591573147847148
```
The package says COMB-ALL10 exists at 0.10 only (rules/selection.md: C10). I could not score the other frozen entries of the run, which are not in this package. The bar of rules/PREREG.v2.md (COMB-NEW at 0.30) is the main session's declared highest known value at 0.30.

## 3. Literature and crowd search (last 24 months: 2024-10-18 to 2026-10-18)
Each line gives the resource, its status line from the helper (status, sha256 prefix, bytes, UTC time) and what it shows.

- ACL Anthology full bibliography with abstracts, https://aclanthology.org/anthology+abstracts.bib.gz: `200 83b1de6e... 42574037 2026-10-18T12:57:51Z`. 131708 entries, max year 2026. It includes 2026.acl-long (2223), 2026.eacl-long (395), 2026.findings-acl (2164), 2025.emnlp-main (1810), 2025.naacl-long (638), 2025.coling-main (758), 2026.lrec-1 (945), 2026.lchange-1 (14), 2025.sigtyp-1 (16), 2026.sigtyp-main (7), 2025/2026 TACL and CL. I grepped years 2023 and later for: reflex prediction, cognate reflex, predict reflex, SIGTYP 2022, ST2022, Mockingbird, cognate prediction, surprise families. The only entry that reports results on the ST2022 reflex task is Akavarapu and Bhattacharya 2023, "Cognate Transformer for Automated Phonological Reconstruction and Cognate Reflex Prediction" (2023.emnlp-main.423), which is known and older than 24 months. These other hits are not ST2022 surprise-test reflex scores: Lu, Wang and Mortensen 2024 (LREC-COLING, protoform reranking on Chinese and Romance), Akavarapu and Bhattacharya 2024 (EACL, cognate detection), Blum and List 2026 (LChange, irregular words, leave-one-out), "Beyond cognacy" (SIGTYP 2025, phylogenetics), Liu et al. 2026 (ACL, Middle Chinese sound-law induction and dialect G2P). No 2026.sigtyp-main paper concerns reflex prediction.
- Cognate Transformer PDF, https://aclanthology.org/2023.emnlp-main.423.pdf: `200 4ede9ad5... 309405 2026-10-18T12:59:23Z`. Its Table 5 reports ED, NED and BC only, at 0.1, 0.3 and 0.5. At 0.3 it gives CogTran-small ED 1.1235, NED 0.2919, BC 0.6954 and Mockingbird ED 1.1762, NED 0.2899, BC 0.6717. "BLEU" occurs 0 times in the text.
- Cognate Transformer repository, https://github.com/mahesh-ak/CognateTransformer: `200 397d8b50... 259475 2026-10-18T12:59:38Z`. HEAD 4da845d4f49c055b82ee4a1c98bfc1f5333c07c3, 5 commits. The results folder (`200 dd6d4f87... 2026-10-18T13:09:30Z`) has reflex_small.tsv (`200 2397abf1... 100 2026-10-18T13:09:45Z`) and reflex_small_detailed.tsv (`200 a2edf20e... 11368 2026-10-18T13:09:49Z`). The columns are test_prop, ED, NED and B3_F1 (0.30 row: 1.1235, 0.2919, 0.6954). BLEU occurs 0 times, and there are no per-item 0.30 reflex predictions to rescore.
- FeVeT repository, https://github.com/TGH-2020/FeVeT: `200 9dd85414... 266141 2026-10-18T12:59:33Z`. HEAD 31898c53bfffeef87265efa8a780b7be740162d1 (the same as scout/scout.md, so unchanged), 29 commits. results/s2s_reflex_finetuned_avg.txt (raw at 31898c53, `200 9fbf75de... 100 2026-10-18T13:07:38Z`) has columns Proportion, ED, NED and B3_F1, with the 0.30 row "0.9589 0.2397 0.7232". results/s2s_reflex_0.30_family_results_finetuned.txt (`200 0ba34113... 365 2026-10-18T13:07:42Z`) has the same columns per family. FeVeT publishes no BLEU.
- FeVeT paper, https://open-research-europe.ec.europa.eu/articles/5-174/v1/pdf: `200 31a08cdf... 2129841 2026-10-18T13:06:36Z`. It is a 10-page PDF headed "Open Research Europe 2025, 5:174 Last updated: 23 SEP 2025 ... [version 1; peer review: 1 approved, 1 approved with reservations] ... Latest published: 30 Jun 2025". Table 3 shows ED, NED and BC. At 0.3, FeVeT has 0.9589, 0.2397 and 0.7232. "BLEU" occurs 0 times. The main session's statement that the paper prints no BLEU is confirmed. The article HTML page (https://open-research-europe.ec.europa.eu/articles/5-174, `200 fc915a3f... 55677 2026-10-18T12:59:28Z`) is a script-only shell with no article text. A Europe PMC search for the title (`200 f65ecafe... 2026-10-18T13:02:59Z`) found 1 hit, PPR1043857, DOI 10.12688/openreseurope.20647.1, versionNumber 1. No version 2 exists.
- arXiv API on export.arxiv.org:
  - abs:reflex AND abs:cognate, newest first (`200 ce4d9e9e... 12409 2026-10-18T12:59:43Z`): 6 results, the newest 2403.18769 (2024-03-27, protoform reranking). The others are 2310.07487 (Cognate Transformer), 2306.02514 (Jambu), 2210.10200, 2205.09570 (CEoT 2022) and 1907.08495.
  - abs:"reflex prediction" (`200 2d577083... 11836 2026-10-18T12:59:52Z`): the same 5 linguistics papers. None is newer than 2024-03-27.
  - all:"SIGTYP 2022" (`200 d0b84176... 715 2026-10-18T12:59:47Z`): 0 results.
  - abs:cognate, newest 100 of 164 (`200 d2d086d5... 214322 2026-10-18T13:03:13Z`): the post-2024-10 papers are about language distance, cognate data in phylogenetics, unsupervised protoform reconstruction (2506.10614), Bantu morphology, Arabic-Hebrew cognates for LLMs, irregular words (2602.02221) and others. None reports ST2022 surprise reflex scores.
  - id_list 2604.22730 (`200 457267b7... 2026-10-18T13:03:08Z`): Bantu lexical structure from modern data. Not reflex prediction.
- Europe PMC:
  - "reflex prediction" OR "cognate reflex" OR "SIGTYP 2022" (`200 31d245a6... 2026-10-18T13:00:06Z`): hitCount 7. The relevant hits are FeVeT (PPR1043857), Blum, Barrientos, Ingunza and List 2024 (Sci Rep 14:30636, PMC11668889, Panoan-Takanan) and List 2023 "Open Problems".
  - Blum et al. full text (`200 5162d324... 123260 2026-10-18T13:02:53Z`): BLEU occurs 0 times. SIGTYP appears only in a reference. It has no ST2022 surprise-test scores.
  - "SIGTYP" AND (cognate OR reflex) (`200 4d2ee00d... 2026-10-18T13:03:04Z`): 2 hits, Lexibank 2 and Open Problems.
  - cognate AND (reflex OR phonological reconstruction OR word prediction), first published from 2024-10-01 (`200 ae3a97df... 87330 2026-10-18T13:06:51Z`): hitCount 197. The relevant ones are FeVeT, Blum et al. 2024, an East Polynesian calendars study and the IE cognate relationships dataset. None has ST2022 scores.
- Zenodo:
  - "reflex prediction", size 25 (`200 a66dc478... 2026-10-18T13:03:17Z`): total 13. The newest relevant record is the FeVeT supplement, 10.5281/zenodo.16813907 (2025-08-12). The others are the 2022 task record, the CEoT 2022 submission, Open Problems, Lexibank 2, and Spanish and Romanian CFR resources from 2026.
  - "SIGTYP 2022" OR ST2022 OR "cognate reflex" (`200 31d2b844... 2026-10-18T13:03:23Z`): total 6. Nothing new.
- Hugging Face papers search (`200 b101b0d4... 2026-10-18T13:00:11Z`; `200 f0340b5d... 2026-10-18T13:06:56Z`): the only reflex or cognate items are 2403.18769 and the SIGTYP 2024 shared-task papers (word embeddings, a different task).
- OpenReview search "cognate reflex prediction" (`200 1705d8f7... 2026-10-18T13:00:16Z`): the relevant notes are the Cognate Transformer EMNLP 2023 submission and DBLP records of known papers. Nothing new.
- GitHub repository search pages, server-rendered results:
  - "cognate reflex prediction" (`200 46d963cb... 2026-10-18T13:00:21Z`): 3 results.
  - "ST2022 sigtyp" (`200 420eb3ac... 2026-10-18T13:00:25Z`): 2 results.
  - "reflex prediction" (`200 13226784... 2026-10-18T13:03:29Z`): 2 results.
  - "sigtyp 2022" (`200 73626149... 2026-10-18T13:03:34Z`): 6 results.
  - "cognate prediction" (`200 bc532fa4... 2026-10-18T13:03:39Z`): 9 results.
  - "phonological reconstruction" (`200 f13a56ef... 2026-10-18T13:06:46Z`): 12 results, all Chinese and Egyptian historical phonology tools, unrelated.
  - The only reflex repository updated within 24 months is acraevschi/cognate_reflexes_task (updated 2024-11-14; page `200 b97e2bd3... 2026-10-18T13:02:48Z`, HEAD e09f68a0, 13 commits). It holds predictions at 0.10 and 0.50 only. Its report PDF (raw, `200 6f7f5758... 106470 2026-10-18T13:06:42Z`) gives surprise BLEU 0.5801 at 10% for its multilingual Transformer and covers only 10% and 50%, so it has no 0.30 value. The other repositories date from 2022-2024-09.
- SIGTYP task page, https://sigtyp.github.io/st2022.html (`200 6ddfaac3... 10843 2026-10-18T13:10:13Z`): static 2022 text with no leaderboard update.
- V3R1T4S pull requests (github.com pages; gh and the API are off limits):
  - Keyword searches on is:pr, open and closed, title and body: sigtyp (`200 2b46f133...`), cognate (`200 96555c27...`), reflex (`200 3fb3f802...`), ST2022 (`200 a5963d66...`), mockingbird (`200 6d990667...`), lexibank (`200 b05ca0b6...`) and phonetic (`200 8736f232...`), between 2026-10-18T13:03:43Z and 13:05:12Z. Each returned openCount 0 and closedCount 0.
  - Positive control is:pr covering (`200 e34ee230... 2026-10-18T13:04:58Z`): totalCount 12 (open 9, closed 3). The search works logged out.
  - Full list newest first (`200 54eb2809... 2026-10-18T13:04:12Z` and page 2 `200 e82e25fa... 2026-10-18T13:05:03Z`): totalCount 389 (open 92, closed 297). The newest is #399 (2026-10-18T12:04:25Z). None of the titles from #348 to #399 concerns SIGTYP or cognate reflexes. The scout's 361-PR snapshot ended at #370 (2026-10-18T01:19:15Z).
- TROPHY_CASE.md (30936 bytes): grep -i for sigtyp, cognate, reflex, ST2022, mockingbird, proto, BLEU, lexib, linguist, Q15, quarry, humanit, wordlist, phonetic and lingu found nothing (exit 1). This target has no entry.

Coverage limits, stated honestly: several hosts were stopped (Semantic Scholar API, OpenAlex, Crossref, dblp, IA Scholar, IEEE Xplore, arxiv.org web), so I could not run a citation search of the 2022 task paper or a journal-wide search. Venues outside the ACL Anthology and Europe PMC, such as Diachronica, Language Dynamics and Change or Journal of Language Evolution, are only partly covered. Proceedings later than the Anthology dump of 2026-10-18 are not covered.

## Best published value at 0.30 on mean BLEU (official family-averaged scale)
- Best value printed in a publication: Mockingbird-I1 0.6058548112827981 (results/results-surprise-0.30.json at ST2022 HEAD 03094435). KNOWN.
- Best value derivable from published per-item predictions: FeVeT (Wientzek 2025, Open Research Europe 5:174; github.com/TGH-2020/FeVeT, predictions at 31898c53) rescored at 0.6356571184958077. FeVeT itself prints no BLEU. NUMERICAL, confirmed here.
- Cognate Transformer (Akavarapu and Bhattacharya, EMNLP 2023) prints no BLEU and publishes no per-item 0.30 predictions.
- Highest value known at 0.30, and this cell's bar: our own NED-targeted object bar_comb_new/test/0.30 0.6839233380559118 (unpublished; confirmed here).
- Claimed object: 0.6874377388475998. This is strictly above all of the above, by 0.003514400791688077 (left-to-right) and 0.003514400791687966 (compensated). It is not a tie.

## Notes for the panel (outside NOVELTY's remit, not a reason to fail)
- The margin over our own bar is small: 0.0035 BLEU. The packaged null test (rules/null_test.md) passes narrowly, with real 0.003514400791687966 against a best control of 0.0035017194380646544. Whether that is robust is for the CRITERION and REPRODUCE skeptics. The novelty comparison itself is strict in both summation modes.
- The candidate beats the bar on 9 of 10 families. It is lower on deepadungpalaung (0.769183 against 0.769578).

novelty: no published or known value at 0.30 on mean BLEU ties or beats 0.6874377388475998. The status source was readable (HTTP 200) and is unchanged since 2022-05-27.

pass: true