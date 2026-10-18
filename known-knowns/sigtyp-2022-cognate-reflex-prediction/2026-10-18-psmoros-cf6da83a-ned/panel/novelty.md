(Saved by the main session at 2026-10-18T12:37:59Z from the novelty skeptic subagent's returned text (cell N50; Opus 5.5, agent a06e89bb27ae0f237); the subagent could not write a file named like a report. Text verbatim below.)

# Panel: NOVELTY skeptic, cell N50 (proportion 0.50, mean NED), run 2026-10-18-0839

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
started: 2026-10-18T11:44:26Z (date -u: Sun Oct 18 11:44:26 UTC 2026)
ended: 2026-10-18T12:01:33Z
role: NOVELTY only. I did not judge train/predict isolation or the criterion. Those belong to the REPRODUCE and CRITERION skeptics.
material: the claim package (claim/), kit/RULES.md, TROPHY_CASE.md, and the web through the shared fetch helper (one plain GET per resource, User-Agent naming V3R1T4S). To confirm which stop list the helper writes to, I grepped 4 lines of the helper file itself (the session stop list path and the glob). I read nothing else in that run folder.
injection_suspected: none seen.

## 1. Status source (one GET each)
status_source: https://github.com/sigtyp/ST2022 HTTP 200 fetched 2026-10-18T11:45:09Z

- Repository page: HTTP 200, 344670 bytes, sha256 f94d25dd4eb4d37dab794640f323eca1f52680db16e1746761253c397e34ee89, title "GitHub - sigtyp/ST2022: SIGTYP 2022 Shared Task · GitHub". The page shows "142 Commits" and HEAD 03094435cba4293ce0eea383036cab78499ad50d.
- https://api.github.com/repos/sigtyp/ST2022/commits?per_page=5: HTTP 200 at 2026-10-18T11:45:10Z, sha256 7b881c75158171750f802d30b85b67bcbe949a72f7d5a4588a5ea6914af2eb0c. It is byte-identical to claim/scout/st2022_commits.json. Newest commits:
  - 03094435cba4293ce0eea383036cab78499ad50d 2022-05-27T07:58:23Z "update for final release"
  - 9d4202ee05ea441b686fcbbadc23057c412d08fb 2022-05-27T07:54:43Z "update"
  - c223f851e2c1b8616692d57b77debcc5ffc706ce 2022-05-27T07:02:55Z "update with final results"
  - 4a1331bff978e9772b8ff9959808f6129e5e8f06 2022-05-23T06:06:15Z "Merge pull request #46 from gcelano/main"
  - 5a0be5ecf77593596bdb5cefecc40900224ce628 2022-05-22T19:05:05Z "correction decoding"
- Official results at the pinned commit (raw.githubusercontent.com .../03094435.../results/results-surprise-0.50.json): HTTP 200 at 2026-10-18T11:45:21Z, sha256 3a8e79f9e686a4835f6bd0948529838b4ebb38ef2f02e05d39dfa73389a014f3. `cmp` says it is identical to claim/official/results/results-surprise-0.50.json.
- Official mean NED at 0.50, ranked:
  - Mockingbird-I1 0.35176136367373956
  - Mockingbird-N1-B 0.3733789322481769
  - Mockingbird-N1-A 0.37999052172679176
  - Mockingbird-N1-C 0.3950045195670149
  - CrossLingference-Julia 0.4274274213553069
  - Baseline-Baseline 0.4445382690345965
  - CEoT-Extalign-RF 0.45758030716855247
  - Baseline-Baseline-SVM 0.4618527113479192
  - Leipzig-Transformer 0.5256730055461115
  - Mockingbird-N2 is listed as [0, 0, 0, 0] in every family (BCFS 0 and BLEU 0 too). This is the placeholder that compare_systems writes when a results file is missing, not a score.
- Pinned scorer (raw .../03094435.../src/sigtypst2022.py): HTTP 200 at 2026-10-18T11:59:22Z, sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a. `cmp` says it is identical to claim/official/src/sigtypst2022.py.
- ST2022 issues and pull-request pages on github.com (HTTP 200 at 11:59:45Z and 11:59:48Z): "Open 0" issues; pull requests "Open 0 ( 0 ) Closed 22 ( 22 )".
- Status: unchanged since 2022-05-27. No new systems, and the official results stand (KNOWN).

## 2. The bar: FeVeT checked on the official scale
- FeVeT repository commits (https://api.github.com/repos/TGH-2020/FeVeT/commits?per_page=5): HTTP 200 at 11:47:29Z, sha256 4ed6f1469db77527e094ec22d44ddb3278cdc0ee9ad8b5de120693b19c454dc0, byte-identical to claim/scout/fevet_commits.json. HEAD is 31898c53bfffeef87265efa8a780b7be740162d1, 2025-11-28T17:00:16Z, "Update README.md".
- FeVeT tree (git/trees/HEAD?recursive=1): HTTP 200 at 11:47:29Z, tree sha 31898c53bfffeef87265efa8a780b7be740162d1, 1090 entries.
  - I computed git blob sha1 values for claim/fevet/pred_0.50_FAM.tsv and compared them with results/predictions/reflex/FAM/s2s_reflex_0.50_predictions.tsv in that tree: "matches 10 of 10".
  - The sha256 values also equal claim/fevet/FETCH_RECORD.txt.
- Independent rescoring, with my own script (outside the package):
  - Method: the scorer was imported from claim/official/src, run with the SCO interpreter, using left-to-right sum shadowing. FeVeT's long format was converted using the solutions header. The GOLD column was used only to check alignment.
  - Calibration: "MOCKINGBIRD-I1 recomputed total [1.4169823165005235, 0.35176136367373956, 0.6050308536957327, 0.5337187296541888]", equal to the official total; "bit-identical all families: True".
  - FeVeT coverage: rows equal solution cells in every family (bantubvd 816, beidazihui 4921, birchallchapacuran 683, bodtkhobwa 3426, bremerberta 366, deepadungpalaung 1450, hillburmish 1638, kesslersignificance 353, luangthongkumkaren 1444, wangbai 3004). In every family "missing 0 extra 0 gold-mismatch 0 dup 0".
  - FeVeT per-family NED:
    - bantubvd 0.2738211449086926
    - beidazihui 0.14054392738603266
    - birchallchapacuran 0.38983503575546774
    - bodtkhobwa 0.18032880190752512
    - bremerberta 0.33095427258419824
    - deepadungpalaung 0.31953980246418506
    - hillburmish 0.37126877343226733
    - kesslersignificance 0.6725904854643949
    - luangthongkumkaren 0.15645594584295797
    - wangbai 0.2526729450060371
  - "FEVET official-scale total [ED, NED, BCFS, BLEU] [1.286021835157271, 0.30880111347517586, 0.6423935720824072, 0.5768215755932388]": exactly the claim's bar (NUMERICAL, PROVED-HERE as a recomputation).
  - "CANDIDATE official-scale total [ED, NED, BCFS, BLEU] [1.0166617451971307, 0.24912258145405175, 0.7114179305724276, 0.6520222200978466]": equal to the claimed value.
  - With Python's built-in (compensated) sum: FeVeT NED 0.30880111347517586 and candidate NED 0.24912258145405175 are unchanged. Only Mockingbird-I1's BLEU moves in the last digit (0.5337187296541887).
- Standalone checker of the claim (python3 -I checker/check_q15.py . object/predictions-0.50.tsv):
  - "1. Mockingbird-I1 mean NED recomputed 0.35176136367373956, official 0.35176136367373956: EXACT"
  - "2. FeVeT published predictions mean NED 0.30880111347517586"
  - "3. object mean NED 0.24912258145405175 over 18101 items (claimed 0.24912258145405175): EQUAL"
  - "margin vs Mockingbird-I1 0.102638782220"
  - "margin vs FeVeT 0.059678532021"
  - "4. rebuilt official-format files equal to the frozen ones: 10 of 10"
  - "PASS"
- FeVeT's printed numbers are on a different scale. Fetched at commit 31898c53, HTTP 200 at 11:48:12Z to 11:48:13Z:
  - code/result_eval.py avg_results_reflex takes df['NED'].mean() over the rows of the per-language results file ("averaged over languages").
  - results/s2s_reflex_finetuned_avg.txt: "0.50 1.1111 0.2825 0.673".
  - results/s2s_reflex_avg.txt (no fine-tuning): "0.50 1.2405 0.3222 0.6426".
  - The published per-item predictions are from the fine-tuned model. My rescored per-family values sit next to the fine-tuned family table, not the other one. Examples: hillburmish rescored 0.3713, printed fine-tuned 0.3733, printed without fine-tuning 0.4408; beidazihui 0.1405, 0.1436 and 0.2287. So the bar uses FeVeT's better variant.
- Same comparison on FeVeT's language-averaged scale (the official per-language NED averaged over all 99 scored languages, my script): "FeVeT-published-predictions languages 99 language-pooled NED 0.279482", "candidate languages 99 language-pooled NED 0.220632", "Mockingbird-I1 languages 99 language-pooled NED 0.327822". The candidate is also below FeVeT's printed 0.2825 on that scale (NUMERICAL).
- Item-pooled NED, for reference: FeVeT 0.23164705301880062 and candidate 0.18147859497370553 over 18101 items.

## 3. Literature search (last 24 months and known prior work)
- FeVeT paper, Open Research Europe 5:174:
  - The article page https://open-research-europe.ec.europa.eu/articles/5-174 returned HTTP 200 at 11:50:50Z, but it is a JavaScript application shell with no text (not a challenge).
  - The PDF https://open-research-europe.ec.europa.eu/articles/5-174/v1/pdf returned HTTP 200 at 11:51:58Z, sha256 31a08cdf6aa8c84c06281cbf4868a3bccc90cc983a8f56a2246ad1027577fa47. It shows "[version 1; peer review: 1 approved, 1 approved with reservations]", "Latest published: 30 Jun 2025" and "Last updated: 23 SEP 2025".
  - Its Table 3 at proportion 0.5:
    - CognateTransformer 1.2786 / 0.3332 / 0.6477
    - FeVeT (no fine-tuning) 1.2405 / 0.3222 / 0.6426
    - FeVeT 1.1111 / 0.2825 / 0.673
    - IPA-only 2.508 / 0.6642 / 0.4489
  - Europe PMC core record PPR1043857 (HTTP 200 at 11:51:44Z): versionList has version 1 only; citedByCount 0 (KNOWN).
- Cognate Transformer (Akavarapu and Bhattacharya, EMNLP 2023): https://aclanthology.org/2023.emnlp-main.423.pdf returned HTTP 200 at 11:50:27Z, sha256 4ede9ad5014866cdfa89f3a0f8eeaf754c50c8439284bb22e2ef7be7c766f38d. Its Table 5 at 0.5:
  - CogTran-tiny 1.4521 / 0.3873 / 0.6257
  - CogTran-small 1.2786 / 0.3332 / 0.6477
  - Mockingbird - Inpaint 1.4170 / 0.3518 / 0.6050
  - This table is on the official family-averaged scale: its Mockingbird row equals the official 0.35176 (KNOWN).
- ACL Anthology full bibliography (https://aclanthology.org/anthology+abstracts.bib.gz): HTTP 200 at 11:48:53Z, 42574037 bytes, sha256 83b1de6eb8e9af0abd7106886ba7e6decbded519ff6d1259bbb94c8286fa6b5d, 131708 entries. It covers venues through ACL 2026 (July), SIGTYP 2026, LChange 2026 and LREC 2026.
  - A topic regex (reflex prediction, cognate reflex, SIGTYP 2022, ST2022, Mockingbird, Cognate Transformer, FeVeT, protoform and phonological reconstruction, sound correspondence patterns) gave "hits 15" since 2023.
  - A broader 2024+ regex (cognate, reflex, protoform, historical linguistics, sound change, lexibank) gave "n 98" titles, which I read.
  - Abstracts checked: 2026.lchange-1.6 (Blum and List, regularity / leave-one-out irregularity detection, no reflex-prediction score), 2026.acl-long.831 (Middle Chinese sound-law induction and G2P), 2025.sigtyp-1.6 (Jäger, phylogenetics), 2024.emnlp-main.362 (Romance protowords), 2024.findings-emnlp.325 (Ancient Chinese), 2024.cawl-1.7 and 2025.acl-long.876.
  - Newer papers by Wientzek, Akavarapu, Kirov, Blum and List: none reports SIGTYP 2022 surprise reflex-prediction scores.
- arXiv API (export.arxiv.org; 10 queries, 11:52:49Z to 12:00:45Z, all HTTP 200):
  - "reflex prediction": totalResults 6, newest 2403.18769 (2024-03, protoform reconstruction on other data).
  - cognate AND reflex: 6.
  - "SIGTYP 2022": 0.
  - protoform/proto-language/phonological reconstruction AND cognate: 9, of which 2506.10614 is unsupervised protoform reconstruction.
  - cognate AND predict: 36.
  - "sound correspondence": 17.
  - cognate AND wordlists: 2.
  - "historical linguistics": 69.
  - cognates AND neural/transformer/LLM: 33.
  - authors Wientzek/Akavarapu or FeVeT: 8.
  - None after October 2024 reports reflex prediction on the ST2022 surprise families.
- Hugging Face papers search (2 queries, HTTP 200 at 11:53:49Z and 11:53:52Z, 120 results each): nothing relevant; 2604.22730 (Bantu lexical structure) is not reflex prediction.
- Europe PMC:
  - "reflex prediction": hitCount 7. Relevant: FeVeT, and Blum, Barrientos, Ingunza, List 2024 (Sci Rep, Pano-Takanan; it predicts 206 Shipibo-Konibo reflexes from Proto-Takanan, with no ST2022 score).
  - FeVeT title: 1.
  - cognate AND reflex AND predict, 2024-10-01 to 2026-10-18: 155, only those two relevant.
  - SIGTYP/ST2022 AND cognate: 2 (Lexibank 2, Open Problems).
- Zenodo API:
  - The first query returned HTTP 400 (validation error: page size above 25 not allowed). This is not a block; I re-queried with size 25.
  - "reflex prediction": total 13. Relevant: only the FeVeT software record 10.5281/zenodo.16813907 (2025-08-12) and 2020 to 2022 items.
  - "SIGTYP 2022": total 4, all 2022 to 2024 and known.
- OpenReview (api2.openreview.net notes/search "reflex prediction cognate", HTTP 200 at 11:56:42Z): of the top 50, only the known Cognate Transformer and Lu et al. 2024 entries are relevant.
- GitHub repository search ("ST2022", HTTP 200 at 11:54:09Z): total_count 18. Only sigtyp/ST2022 is relevant.
- Result (NUMERICAL, HEURISTIC as to coverage): no published score at 0.50 on the surprise families below the candidate was found, on any scale.

## 4. Crowd: TROPHY_CASE.md and V3R1T4S pull requests
- TROPHY_CASE.md: grep for sigtyp, cognat, reflex, st2022, mockingbird, fevet, proto, lexibank, wordlist, linguist, language, NED and edit distance gave 2 hits, both false matches inside the word "pinned" (lines 32 and 37). Its summary lists six result families and two cipher commitments, none of which is this target.
- PR titles, scout snapshot claim/scout/v3r1t4s_all_prs.json: 381 PRs, newest 2026-10-18T08:02:36Z, "hits 0" for sigtyp, cognat, reflex, st2022, mockingbird, fevet, proto-form, lexibank, wordlist, q15 and private-quarry.
- Fresh PR pages on github.com:
  - Open list https://github.com/elder-plinius/V3R1T4S/pulls: HTTP 200 at 11:57:37Z, 25 PRs, #374 to #398. The 7 PRs opened after the snapshot (#392 to #398, up to 2026-10-18T10:56:07Z) are about other targets; target-word hits 0.
  - Closed list https://github.com/elder-plinius/V3R1T4S/pulls?state=closed: HTTP 200 at 11:57:41Z, newest closed #352 (created 2026-10-17T14:34:14Z); target-word hits 0.
  - I used these pages because their URLs have no ?q= search, which github.com/robots.txt (HTTP 200 at 11:57:11Z) disallows.
- gh was not used: the api.github.com host stop (section 5) covers it.
- Result: no V3R1T4S PR or trophy entry for this target (KNOWN).

## 5. Blocks and limits (kit rule 5)
- api.github.com:
  - At 2026-10-18T11:54:13Z, https://api.github.com/search/repositories?q=%22reflex+prediction%22&sort=updated&per_page=100 returned HTTP 403 with "API rate limit exceeded" for this machine's address. The helper appended that line to the session stop list.
  - Another lens, L50-NOVELTY, got the same 403 at the same second.
  - I ruled a host-level stop and appended "2026-10-18T11:55:06Z 403 api.github.com ALL N50-NOVELTY (...)". The helper then refused api.github.com ("REFUSED host stopped", rc 3).
  - Nothing was retried, and this lens made no further api.github.com request.
  - Effect: 3 queued GitHub repository searches were never run.
- Not used because they appear in stop lists from the last 24 h: api.semanticscholar.org, dblp.org, scholar.archive.org, api.openalex.org, api.crossref.org, and arxiv.org (web host).
  - The arXiv queries went to the separate API host export.arxiv.org, which the helper allowed. I disclose this here.
- Google Scholar was not used (automated queries are against its terms).
- Coverage gap: without Crossref, OpenAlex and Semantic Scholar I could not do citation tracking for FeVeT or Cognate Transformer, and could not fully cover journals outside the ACL Anthology, arXiv, Europe PMC, Zenodo and Open Research Europe (for example Diachronica and Language Dynamics and Change). Europe PMC reports 0 citations of FeVeT.

## Verdict
- Best published value at 0.50 on mean NED: 0.30880111347517586. These are FeVeT's own published per-item predictions (Wientzek 2025, Open Research Europe 5:174; github.com/TGH-2020/FeVeT at 31898c53, results/predictions/reflex/FAM/s2s_reflex_0.50_predictions.tsv), rescored here on the official family-averaged scale.
- Best value printed on the official scale: CogTran-small 0.3332 (Akavarapu and Bhattacharya, EMNLP 2023, Table 5). Official leaderboard: Mockingbird-I1 0.35176136367373956.
- FeVeT's printed 0.2825 (Table 3, fine-tuned) is a language-averaged value. On that scale the candidate scores 0.220632.
- Candidate: 0.24912258145405175 on the official scale. It is strictly lower than FeVeT's rescored 0.30880111347517586 by 0.059678532021, lower than CogTran-small's 0.3332, and lower than Mockingbird-I1 by 0.102638782220. It is not a tie.
- novelty: CONFIRMED for the stated scope only (NUMERICAL): mean NED at proportion 0.50 over the 10 SIGTYP 2022 surprise families, official scorer at commit 03094435. This depends on the reachable sources listed above. Whether the entries used gold-free training data is outside this skeptic's role.

pass: true