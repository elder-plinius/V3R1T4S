(Saved by the main session from the subagent's returned text at 2026-10-18T22:04:28Z; the L40 NOVELTY skeptic subagent (Opus 5.5, model opus, agent a9054c1e9a3156fdb) could not write a file named like a report. Text verbatim below.)

# NOVELTY skeptic, cell L40 (proportion 0.40, mean BLEU, higher is better), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: NOVELTY (one of three skeptics; I saw only the claim package, the kit rules, TROPHY_CASE.md and the web through the shared fetch helper vfetch.py)
start: Sun Oct 18 21:39:52 UTC 2026 (date -u)
end: Sun Oct 18 21:59:51 UTC 2026 (date -u)

status_source: https://github.com/sigtyp/ST2022 HTTP 200 fetched 2026-10-18T21:40:36Z

best published value at 0.40 on mean BLEU: Mockingbird-I1 0.5723601982335171 (official results/results-surprise-0.40.json of sigtyp/ST2022 at commit 03094435cba4293ce0eea383036cab78499ad50d; byte-identical to official/results/results-surprise-0.40.json in this package). No other published 0.40 mean-BLEU value was found. KNOWN
claimed value: classifier/PRIMARY mean BLEU 0.6533966833715619 at 0.40, margin +0.081036485138 over Mockingbird-I1 (strict, not a tie). NUMERICAL (checker re-run below)

## Verdict
As of 2026-10-18T21:58Z, no published score on the 10 SIGTYP 2022 surprise families at proportion 0.40 that I could reach beats or equals the claimed mean BLEU 0.6533966833715619 on the official family-averaged scale. Nothing moves the bar either: Mockingbird-I1's official 0.5723601982335171 is still the best published value at 0.40, so the claim strictly beats everything known.

## 1. Status source (one plain GET through the shared helper, User-Agent naming V3R1T4S, stop lists checked first)
Command: vfetch.py check https://github.com/sigtyp/ST2022 returned OK; then vfetch.py get https://github.com/sigtyp/ST2022 st2022.html --lens L40-NOVELTY
Output: 200	472f3ad3aff0f2f8c910a377528715b1c50af1b4340c66496d65c343052e5959	344670	2026-10-18T21:40:36Z
What the page shows (parsed from the saved page):
- title: GitHub - sigtyp/ST2022: SIGTYP 2022 Shared Task · GitHub
- embedded "currentOid":"03094435cba4293ce0eea383036cab78499ad50d" (2 occurrences, branch main), the only commit oid in the page (the other 40-hex strings are hmac/token values). listCacheKey v0:1653644709.4644532 = 2022-05-27T09:45:09Z, "commitCount":"142". This is the same HEAD as the package's pin (scout/scout.md), so nothing changed.
- README meta-evaluation (ranks), row "Mockingbird-I1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 1 1.2 1 1.06667 0.258199": rank 1 on NED/BCFS/BLEU at proportion 4 (0.40).
- Official results unchanged: raw.githubusercontent.com/sigtyp/ST2022/03094435cba4293ce0eea383036cab78499ad50d/results/results-surprise-0.40.json returned 200, sha256 699aacbc94cb6d8289bb2685ac73f87e2cf72a1df22cee89a6cf8b7e1501ee86, 14371 bytes, 2026-10-18T21:41:36Z. The package copy official/results/results-surprise-0.40.json has the same sha256, and cmp reports IDENTICAL.
- Metric order checked in official/src/sigtypst2022.py (lines 491-493: headers "Language", "ED", "ED (Normalized)", "B-Cubed FS", "BLEU"), so total[3] is BLEU.
Official totals at 0.40 sorted by BLEU (total = [ED, NED, BCFS, BLEU], from the pinned JSON):
  Mockingbird-I1 [1.272493550651723, 0.316240240534308, 0.6428278176401176, 0.5723601982335171]
  Mockingbird-N1-B [1.3618136397516487, 0.33494782949582314, 0.6212246948083399, 0.5466088108887145]
  Mockingbird-N1-A [1.4542399832668305, 0.3521333077310183, 0.6294058424159104, 0.5292909685449981]
  Mockingbird-N1-C [1.435283929525084, 0.35467328872000803, 0.5999320583412607, 0.522759311540485]
  Baseline-Baseline-SVM [1.6158526162556408, 0.3890729260804659, 0.5990447973691144, 0.4903341422214015]
  CEoT-Extalign-RF [1.5694502736482905, 0.39599855357096486, 0.5804515960120803, 0.47726464541828323]
  Baseline-Baseline [1.6821275072093866, 0.40106538946052545, 0.6000922512660704, 0.4716560151572001]
  CrossLingference-Julia [1.6059186324923054, 0.4111909730747342, 0.6411350072030729, 0.4472737391375306]
  Leipzig-Transformer [1.9220898125844423, 0.47999149421316156, 0.47362199458683174, 0.3892908289228411]
  Mockingbird-N2 [0, 0, 0, 0]
KNOWN

## 2. Sanity re-run of the package's standalone checker (standard library; python3 checker/check_q15.py . object/predictions-0.40.tsv)
  1. Mockingbird-I1 mean BLEU recomputed 0.5723601982335171, official 0.5723601982335171: EXACT
  3. object mean BLEU 0.6533966833715619 over 14992 items (claimed 0.6533966833715619): EQUAL
     margin vs Mockingbird-I1 0.081036485138 (higher is better)
  4. rebuilt official-format files equal to the frozen ones: 10 of 10
  PASS
(Whether the training was clean is the REPRODUCE and CRITERION skeptics' job. I only checked that the claimed number is the one I compare against the literature.) NUMERICAL

## 3. Known prior work: both claims in the brief checked
FeVeT (Wientzek 2025, Open Research Europe 5:174):
- github.com/TGH-2020/FeVeT returned 200, 2026-10-18T21:41:36Z; embedded oid 31898c53bfffeef87265efa8a780b7be740162d1 (the oid scout/scout.md records, so unchanged). The results/ tree lists s2s_reflex_0.10_*, s2s_reflex_0.30_*, s2s_reflex_0.50_* (family/language, plain and finetuned), s2s_reflex_avg.txt and s2s_reflex_finetuned_avg.txt. There is no 0.40 file.
- raw .../31898c53.../results/s2s_reflex_avg.txt (200): "Proportion ED NED B3_F1 / 0.10 0.9451 0.2525 0.7704 / 0.30 1.1046 0.2837 0.6874 / 0.50 1.2405 0.3222 0.6426".
- raw .../s2s_reflex_finetuned_avg.txt (200): "0.10 0.7836 0.205 0.8041 / 0.30 0.9589 0.2397 0.7232 / 0.50 1.1111 0.2825 0.673".
- Article XML open-research-europe.ec.europa.eu/articles/5-174/v1/xml (200, 2026-10-18T21:42:31Z): DOI 10.12688/openreseurope.20647.1, volume 5, elocation 174, epub 2025-06-30. Text: "Following Akavarapu & Bhattacharya (2023), the model is evaluated on the 10%, 30%, and 50% test proportions of the surprise data given out in the shared task." Table 3 has ED/NED/BC only, at 0.1/0.3/0.5. The string "BLEU" occurs 0 times.
- A version 2 could not be confirmed: .../5-174/v2/xml returned 500 (not a block status; not retried). Europe PMC and OpenAlex list only the version-1 DOI plus two peer-review reports of version 1 (2025-08-29, 2025-09-23). Zenodo lists FeVeT software v1.1 (2025-08-12, "Minor changes after workflow issue").
- Result: FeVeT has no 0.40 value and no BLEU at any proportion. The brief's claim holds. KNOWN
Cognate Transformer (Akavarapu and Bhattacharya, EMNLP 2023, aclanthology 2023.emnlp-main.423):
- PDF aclanthology.org/2023.emnlp-main.423.pdf returned 200, sha256 4ede9ad5014866cdfa89f3a0f8eeaf754c50c8439284bb22e2ef7be7c766f38d, 2026-10-18T21:43:48Z. Section 4.1: "Surprise data was divided into different test proportions of 0.1, 0.2, 0.3, 0.4, and 0.5 for evaluation. Among these, we only report for the test proportions 0.1, 0.3, and 0.5." Metrics: ED, NED, B-Cubed F1 (no BLEU). Table 5 CogTran-small: 0.1 ED 0.8966 NED 0.2421 BC 0.7823; 0.3 ED 1.1235 NED 0.2919 BC 0.6954; 0.5 ED 1.2786 NED 0.3332 BC 0.6477.
- github.com/mahesh-ak/CognateTransformer returned 200, oid 4da845d4f49c055b82ee4a1c98bfc1f5333c07c3. results/reflex_sota holds res_0.10.tsv, res_0.30.tsv, res_0.50.tsv and reflex_prev_sota.tsv only. results/reflex_small.tsv (200): "test_prop ED NED B3_F1 / 0.10 0.8966 0.2421 0.7823 / 0.30 1.1235 0.2919 0.6954 / 0.50 1.2786 0.3332 0.6477". results/reflex_tiny.tsv has the same three proportions.
- Correction to the brief and to scout/scout.md: Cognate Transformer reports 0.10, 0.30 and 0.50, not "0.50 only". The conclusion that matters still holds: it has no 0.40 value and no BLEU. CLAIM.md's sentence "FeVeT and Cognate Transformer published no 0.40 value" is correct. KNOWN

## 4. Literature search, last 24 months (2024-10-18 to 2026-10-18) and older where cheap
ACL Anthology: aclanthology.org/anthology+abstracts.bib.gz returned 200, 42574037 bytes, sha256 83b1de6eb8e9af0abd7106886ba7e6decbded519ff6d1259bbb94c8286fa6b5d (gzip header: last modified Sat Oct 17 12:23:28 2026); 131708 entries (year counts 2024 12135, 2025 14931, 2026 10822).
- I searched titles and abstracts (year 2022 or later) for reflex prediction, cognate reflex, SIGTYP 2022, ST2022, Mockingbird, Cognate Transformer, FeVeT, protoform, phonological or proto-language reconstruction, and sound correspondence: 20 hits. From 2024 onward: 2024.acl-long.788, 2024.eacl-long.58, 2024.lrec-main.762, 2024.sigtyp-1.11, 2026.lchange-1.6.
- A broader search (2024-2026; reflex, cognate, proto-form, proto-language, sound change, comparative method, lexibank, historical linguistic, sigtyp) gave 105 hits. I read the abstracts of every plausible one: 2025.sigtyp-1.6, 2026.lchange-1.6, 2026.acl-long.831, 2026.findings-acl.432, 2025.acl-long.1432, 2024.emnlp-main.362, 2024.lrec-main.762, 2024.eacl-long.58, 2026.scil-main.14, 2026.lchange-1.3, 2026.dialres-1.12, 2023.sigtyp-1.6, 2023.lchange-1.3.
- None of them reports reflex prediction on the SIGTYP 2022 surprise families at 0.40, and none reports mean BLEU on them.
Europe PMC (also indexes Open Research Europe):
- AUTH:"Wientzek": 34 hits, including the FeVeT preprint record PPR1043857 (DOI 10.12688/openreseurope.20647.1). Its fullTextXML returned 500 (not retried).
- "reflex prediction" OR "cognate reflex(es)" OR "SIGTYP 2022": 7 hits. The only one in the window is Blum, Barrientos, Ingunza, List 2024 (Sci Rep, 10.1038/s41598-024-82515-3), which predicts Panoan reflexes from Proto-Takanan and does not use the SIGTYP data.
- Reconstruction and cognate terms with PUB_YEAR 2024-2026: 24 hits, none relevant.
Hugging Face papers index (arXiv-based; huggingface.co/api/papers/search):
- "cognate reflex prediction": 120 results. "SIGTYP 2022 shared task cognate reflexes": 120 results.
- Filtered for reflex/cognate/SIGTYP/proto-form/Lexibank: only 2403.18769 (LREC-COLING 2024, Chinese/Romance protoforms), 2406.05930 (protoforms), 2604.22730 (Bantu morphology) and unrelated items. None is relevant.
OpenAlex (api.openalex.org; see the stop-list note in section 6):
- Seeds: W4287889593 (ST2022 task paper, cited_by 15), W4287888114 (Mockingbird, 10), W4389520718 (Cognate Transformer, 3), W4411787216 (FeVeT, 0).
- Works citing any seed: count 20. Within the window there are 4:
  - FeVeT (above).
  - Sci Rep Panoan-Takanan (above).
  - bioRxiv 10.64898/2026.01.18.700141, protein ancestral sequence reconstruction: not linguistic data.
  - ICCIES 2025 10.1109/iccies63851.2025.11032538, "Reconstructing Proto-Languages Using Neural Machine Translation and Deep Learning". Its abstract (OpenAlex) is about proto-language reconstruction and mentions no SIGTYP data, proportions or BLEU. Its full text is on ieeexplore.ieee.org, which is stop-listed (challenge), so I did not open it.
- Keyword search ("reflex prediction" OR "cognate reflexes" OR "cognate reflex" OR "SIGTYP 2022", from 2024-10-01): count 26. I checked the abstracts of 10.1075/dia.23025.lai, arXiv 2512.01713, arXiv 2609.05262 and 10.70102/afts.2026.1835.049. None reports SIGTYP 2022 reflex prediction.
Zenodo (zenodo.org/api/records, size 25): total 13. In the window there are only FeVeT software v1.1, Lexibank 2 (ORE) and two Latin-to-Romance forward-reconstruction resources (CLESp/SpanLLex, CLER/RoLLex). A first request with size=50 returned 400 ("Page size cannot be greater than 25"), which is not a block status. I re-sent it once with size=25, which is a different URL.
GitHub HTML repository search (unauthenticated, sorted by updated):
- "reflex prediction": 2 results (cmu-llab/reranked-reconstruction 2024-04, LGirrbach/Cognate-Reflex-Prediction 2023-01).
- "SIGTYP 2022": 5. "cognate reflex": 5. "ST2022 sigtyp": 2. "cognate prediction": 5. "phonological reconstruction": 7. "reflexes sigtyp": 2.
- "SIGTYP 2022" in:readme: 12. "reflex prediction" in:readme: 21 (pages 1 and 2).
- Repositories updated inside the window that I opened:
  - acraevschi/cognate_reflexes_task (2024-11-14, oid e09f68a00fdfde0806a7a6bdc2a28a78492216f1): predictions and models at 0.10 and 0.50 only; README says "on par with Mockingbird team's Transformer model". No 0.40 value.
  - acraevschi/llm_cognate_reflexes (2026-07-12, oid ab2b2f109f054f804b9a4278698ba5ffedbd2f1e): a reconstruction workbench; README has no SIGTYP, surprise, 0.4, BLEU or NED value.
  - LabGuy94/IPABrew (2026-06): protoform app trained on SIGTYP 2022 + WikiHan; no reflex-prediction scores, no 0.4, no BLEU.
  - musahinist/etimoloji (2026-09): Turkic etymology engine that exports its own data in SIGTYP 2022 format; no surprise-family scores.
  - Sunbro26/Indo-Aryan-FeVeT (2026-06): Indo-Aryan; no SIGTYP scores.
Result of the search: no published score at 0.40 on the SIGTYP 2022 surprise families exists outside the official results file, and no published mean BLEU on them at any proportion exists outside the official results files. Bar unchanged. KNOWN (within the reach stated in section 6)

## 5. Crowd: V3R1T4S pull requests and the trophy case
- TROPHY_CASE.md: grep -c -i -E 'sigtyp|cognate|reflex|ST2022|mockingbird|fevet|Q15|quarry|BLEU' gives 0. The six families and two commitments listed there do not include this target.
- github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr returned 200, 2026-10-18T21:46:36Z. Embedded counts: totalCount 457, openCount 160, closedCount 297 (newest #467). No title on page 1 matches sigtyp, cognate, reflex, ST2022, mockingbird, BLEU or Q15.
- Keyword searches (is:pr plus each term, open and closed together), each returning embedded {"openCount":0,"closedCount":0}: cognate (21:46:20Z), sigtyp, reflex, ST2022, Mockingbird (21:46:37-39Z), FeVeT, BLEU, and "cognate reflex" OR "reflex prediction" OR lingpy OR lexibank (21:46:52-54Z).
- Control search is:pr Delsarte returned totalCount 12 (openCount 9, closedCount 3), so the zero counts are real.
- Result: no open or closed V3R1T4S pull request claims this target. KNOWN

## 6. Stop lists, blocks and reach (kit rule 5)
- Before the first request I read the session stop list and every stops-*.tsv changed in the last 24 h. The helper re-reads them before every request.
- Host-level stops in force, so not queried:
  - arxiv.org (429, 2026-10-17T22:56:05Z, other lane), so arXiv was not queried directly. Coverage comes from OpenAlex's arXiv records and the Hugging Face papers index. export.arxiv.org was not used either.
  - api.semanticscholar.org (429), dblp.org (challenge), scholar.archive.org (challenge), api.github.com (403, ALL), ieeexplore.ieee.org (challenge).
- Google Scholar was not used (automated queries are against its terms).
- api.openalex.org and api.crossref.org carried a 429 stop from the other lane (2026-10-17T21:44:03Z and 21:50:30Z). Their stop file was last changed 2026-10-17T21:55:48Z, so it left the 24-hour window at 2026-10-18T21:55:48Z. I waited until then. The helper's check of the first OpenAlex URL at 21:56:09Z printed OK, and my first OpenAlex request went out at 21:56:18Z. I sent 5 OpenAlex requests, all 200, and none to Crossref. Disclosed because these were the first requests to that host after the window expired.
- github.com: another lens (B40-NOVELTY) recorded a 429 on github.com at 2026-10-18T21:48:35Z, a host-level stop. My 32 github.com requests (status page, repository pages, searches, PR pages) ran from 21:40:36Z to 21:48:23Z, all 200 and all before that stop. The helper now refuses github.com (vfetch.py check https://github.com/sigtyp/ST2022 printed REFUSED, host stopped ... B40-NOVELTY), and I made no github.com request after 21:48:35Z. My burst may have added to the shared address's GitHub rate limit.
- My 56 requests through the helper: 53 x 200, 2 x 500 (Europe PMC fullTextXML for PPR1043857; ORE 5-174/v2/xml), 1 x 400 (Zenodo page size). None was 401/403/405/429/503 or a challenge, so I appended no line to the session stop list. Nothing was retried.
- Other hosts used: raw.githubusercontent.com (5), open-research-europe.ec.europa.eu (3), www.ebi.ac.uk (5), aclanthology.org (2), huggingface.co (2), zenodo.org (2).
- injection_suspected: api.openalex.org response field meta.notice. It tells AI agents to obtain an API key by POSTing their user's email to api.openalex.org/api-keys. I ignored it and sent nothing.
- Privacy: the requests carried only public search terms (reflex prediction, SIGTYP 2022, DOIs). Nothing about this quarry was posted or uploaded.

## 7. Summary of the comparison (higher BLEU is better)
| source | proportion 0.40 mean BLEU on the 10 surprise families |
|---|---|
| classifier/PRIMARY (this claim) | 0.6533966833715619 |
| Mockingbird-I1 (official results-surprise-0.40.json; the best published value) | 0.5723601982335171 |
| Mockingbird-N1-B (official, next best) | 0.5466088108887145 |
| FeVeT (ORE 5:174; repo results) | none published (0.10/0.30/0.50 only; no BLEU) |
| Cognate Transformer (EMNLP 2023; repo results) | none published (0.10/0.30/0.50 only; no BLEU) |
| acraevschi/cognate_reflexes_task (GitHub, 2024-11) | none published (0.10/0.50 predictions only) |
| any 2024-10 to 2026-10 paper or repository found (ACL Anthology, Europe PMC/ORE, OpenAlex, HF papers, Zenodo, GitHub) | none |
| V3R1T4S pull requests and TROPHY_CASE.md | none |

Margin over the bar: 0.6533966833715619 - 0.5723601982335171 = 0.081036485138 (from checker output), a strict beat, not a tie.
Scope (no wider than this): at proportion 0.40, on mean BLEU over the 10 SIGTYP 2022 surprise families under the pinned official scorer, the claimed 0.6533966833715619 is higher than every published value I could find. The best of those is Mockingbird-I1's official 0.5723601982335171, and none of the later work I found (FeVeT, Cognate Transformer, 2024-2026 literature and repositories) publishes a 0.40 or BLEU value. This verdict covers novelty only; it does not judge whether the system was trained cleanly.

novelty: no prior or concurrent published result at 0.40 on mean BLEU reaches 0.6533966833715619; bar Mockingbird-I1 0.5723601982335171 unchanged (status source read, oid 03094435cba4293ce0eea383036cab78499ad50d)
pass: true