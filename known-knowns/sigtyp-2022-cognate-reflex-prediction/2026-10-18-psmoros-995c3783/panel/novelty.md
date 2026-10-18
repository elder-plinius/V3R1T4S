(Main session note, 2026-10-18T07:05Z: this NOVELTY file is the round-1 NOVELTY skeptic's text, judged on the round-1 package of this cell. The round-2 package differs only by the added code of the weight-0 stage-2 entries, the sealed-check logs and corrected text; the claimed object, its value and every number this skeptic checked are unchanged. Its status fetch (2026-10-18T04:56-04:57Z) is less than 6 hours before the gate.)
(Saved by the main session from the subagent's returned text, 2026-10-18T06:04Z: round-1 NOVELTY skeptic for cell C20 (Opus 5.5, Agent tool). Verbatim below, harness indentation removed.)

# NOVELTY skeptic, cell C20 (proportion 0.20, mean NED), run 2026-10-18-0202

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
started: Sun Oct 18 04:55:38 UTC 2026 (date -u)
ended: Sun Oct 18 05:11:23 UTC 2026 (date -u)
material: claim/ only (CLAIM.md, definition/Q15.json, scout/, fevet/FETCH_RECORD.txt, official/, combiner/test/0.20). Other files read: the kit rules (repo/kit/RULES.md) and TROPHY_CASE.md. Web access went only through the shared fetch helper (one plain GET per URL, V3R1T4S User-Agent, stop lists checked before each request). GitHub access was read-only `gh pr list` on elder-plinius/V3R1T4S. My scratch files are in my own panel folder, outside claim/.

## Verdict in one sentence
I found no published score on the 10 SIGTYP 2022 surprise families at proportion 0.20 that is lower than the claimed mean NED 0.20345235544710852 on the official family-averaged scale. The best published value at 0.20 is still Mockingbird-I1 at 0.2648052468982754 (official results-surprise-0.20.json), and the claim beats it strictly by 0.061352891. (KNOWN for the published values, NUMERICAL for the rescoring.)

## 1. Status source (one GET each)
status_source: https://github.com/sigtyp/ST2022 HTTP 200 fetched 2026-10-18T04:57:13Z
- helper output: `200  39e59fc46fd4451f3417dd8ac5c9c358eb66bfa43acca613cc4f6ca4dcb484de  344669  2026-10-18T04:57:13Z`. Page title "GitHub - sigtyp/ST2022: SIGTYP 2022 Shared Task · GitHub", "142 Commits", embedded currentOid 03094435cba4293ce0eea383036cab78499ad50d.
- API form: https://api.github.com/repos/sigtyp/ST2022/commits?per_page=5 gave HTTP 200 at 2026-10-18T04:57:14Z, sha256 7b881c75158171750f802d30b85b67bcbe949a72f7d5a4588a5ea6914af2eb0c. This is byte-identical to claim/scout/st2022_commits.json (shasum printed the same hash for both). Newest commits:
  - 03094435cba4293ce0eea383036cab78499ad50d 2022-05-27T07:58:23Z 'update for final release'
  - 9d4202ee05ea441b686fcbbadc23057c412d08fb 2022-05-27T07:54:43Z 'update'
  - c223f851e2c1b8616692d57b77debcc5ffc706ce 2022-05-27T07:02:55Z 'update with final results'
  - 4a1331bff978e9772b8ff9959808f6129e5e8f06 2022-05-23T06:06:15Z 'Merge pull request #46 from gcelano/main'
  - 5a0be5ecf77593596bdb5cefecc40900224ce628 2022-05-22T19:05:05Z 'correction decoding'
- So the repository has not changed since 2022-05-27, and the official results stand.
- Official results at the pinned commit: https://raw.githubusercontent.com/sigtyp/ST2022/03094435.../results/results-surprise-0.20.json gave HTTP 200 at 2026-10-18T04:57:26Z, sha256 80f2b01eb4e6f6c2130749f7eff149dc95fd4c59044ec9b8b22836b74dbbf519. This is identical to claim/official/results/results-surprise-0.20.json.
- Official systems at 0.20 ranked by NED (my parse; the family mean recomputed from the per-family entries matches "total"):
  - Mockingbird-I1 0.2648052468982754
  - Mockingbird-N1-A 0.28249437441268044
  - Mockingbird-N1-B 0.290102017112842
  - Baseline-Baseline-SVM 0.29279651250826044
  - Mockingbird-N1-C 0.3051397866536312
  - CEoT-Extalign-RF 0.31746121037010094
  - Baseline-Baseline 0.33608223596560405
  - CrossLingference-Julia 0.39119892793853606
  - Leipzig-Transformer 0.40461153422061025
- Mockingbird-N2 shows [0, 0, 0, 0] for every family. This is a placeholder, not a score. The contents API (HTTP 200, 05:10:14Z) shows systems/mockingbird-n2/surprise/bantubvd holds only `README.md` and `result-0.10.tsv`, so N2 submitted nothing at 0.20.
- The scorer copy is the pinned one. raw .../03094435.../src/sigtypst2022.py (HTTP 200, 05:07:35Z) has sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a. That equals claim/official/src/sigtypst2022.py and the installed module of the scorer interpreter.

## 2. Bar and claimed value recomputed (official compare_words, left-to-right sum, mean over 10 families)
My own script imports the pinned sigtypst2022 and averages compare_words(...)[-1][1:] over the 10 families:
- claim/official/systems/mockingbird-i1/surprise gives MEAN [ED, NED, BCFS, BLEU] = ['1.0413225298738344', '0.2648052468982754', '0.7119659170836019', '0.632633947442519']. This reproduces the official "total" bit for bit.
- claim/combiner/test/0.20 gives MEAN [ED, NED, BCFS, BLEU] = ['0.7979822478300038', '0.20345235544710852', '0.7780895356732769', '0.7080911153196365']. This equals the CLAIM.md value.
- Margin: 0.2648052468982754 - 0.20345235544710852 = 0.0613528914511669.

## 3. Known later systems
**FeVeT** (Wientzek 2025, Open Research Europe 5:174, DOI 10.12688/openreseurope.20647.1; github.com/TGH-2020/FeVeT):
- Commits API: HTTP 200 at 04:59:41Z, sha256 4ed6f1469db77527e094ec22d44ddb3278cdc0ee9ad8b5de120693b19c454dc0, identical to claim/scout/fevet_commits.json. HEAD is 31898c53bfffeef87265efa8a780b7be740162d1 at 2025-11-28T17:00:16Z ('Update README.md').
- Repo tree at 31898c53: HTTP 200, 1090 entries, not truncated. It has 30 reflex prediction files, `s2s_reflex_0.10/0.30/0.50_predictions.tsv` × 10 families. Searching all paths for 0.20/0.40 found nothing. FeVeT published no predictions and no data at 0.20.
- Paper, as JATS XML (https://open-research-europe.ec.europa.eu/articles/5-174/v1/xml, HTTP 200, 05:00:16Z; the HTML page is a JavaScript shell): "the model is evaluated on the 10%, 30%, and 50% test proportions". The reflex table prints FeVeT NED 0.205 (0.1), 0.2397 (0.3), 0.2825 (0.5). There is no 0.20 value.
- Scale check:
  - I fetched FeVeT's 20 prediction files at 0.10/0.30 and the official solutions at the pinned commit (40 GETs, all HTTP 200, 05:08:55Z to 05:09:24Z). The predictions are byte-identical to the hashes in claim/fevet/FETCH_RECORD.txt (diff empty).
  - Official-scale rescoring, with 0 predictions missing:
    - 0.10: NED 0.2296925777970808
    - 0.30: NED 0.2632988364952282
  - Both match the claim's PREREG bars.
  - A language-pooled average (mean over all 99 family-language rows) gives NED 0.2055 / BCFS 0.8041 at 0.10, against the paper's 0.205 / 0.8041; and NED 0.2342 / BCFS 0.7278 at 0.30, against the paper's 0.2397 / 0.7232. So the paper prints the pooled scale, as the task said.
  - Even FeVeT's 0.10 value is above the claim on both scales: 0.2297 official, 0.205 pooled.
- (HEURISTIC) In every official table NED rises with the proportion, so a FeVeT value at 0.20 would be expected above 0.2297.

**Cognate Transformer** (Akavarapu and Bhattacharya, EMNLP 2023, aclanthology 2023.emnlp-main.423; PDF HTTP 200, 04:59:23Z):
- The paper says "Among these, we only report for the test proportions 0.1, 0.3, and 0.5". Table 5 gives CogTran-small NED 0.2421 / 0.2919 / 0.3332.
- Repo mahesh-ak/CognateTransformer: tree HTTP 200, 534 files, no 0.20 paths. Its last commit is 2023-12-18.
- No value at 0.20.

## 4. Literature search, last 24 months and beyond (all through the helper)
- **ACL Anthology:** the full anthology+abstracts.bib.gz (HTTP 200, 05:58:05Z... recorded by the helper as 2026-10-18T04:58:05Z; 42574037 bytes; sha256 83b1de6e...; 131708 entries, covering ACL 2026, SIGTYP 2026 (2026.sigtyp-main, 7 papers, none on reflexes) and LChange 2026).
  - I grepped titles and abstracts for reflex, cognate, proto-form, SIGTYP, Lexibank, Mockingbird and phonological reconstruction (2022 and later; 2024 and later).
  - Relevant hits were the 2022 shared-task papers, Cognate Transformer (2023), Lu et al. LREC-COLING 2024, Akavarapu EACL 2024, Blum and List SIGTYP 2023, List et al. LChange 2023, and Blum and List LChange 2026.
  - None of these reports an ST2022 surprise score at 0.20. The later ones are on protoform reconstruction (WikiHan/Romance), cognate detection, or regularity.
- **Europe PMC** (indexes ORE and Sci Rep): 10 queries, all HTTP 200.
  - "cognate reflex" (2 hits), "SIGTYP 2022" (0), "reflex prediction" 2023-2026 (4), "phonological reconstruction" 2024-2026 (5), "cognate prediction" (3), "Mockingbird" AND cognate (1, a 2005 poster), "proto-language reconstruction" 2024-2026 (1), "word prediction" AND cognate (3), plus two lookups.
  - Only FeVeT is relevant. Blum, Barrientos, Ingunza and List (Sci Rep 2024) predict Shipibo-Konibo reflexes from Proto-Takanan; that is not ST2022. Lexibank 2 (ORE 2025) is a data paper.
- **Zenodo API:** 5 queries.
  - My first 5 calls used size=100 and each got HTTP 400 ("Page size cannot be greater than 25"). That is not a block status, but the loop sent all 5 before I noticed. The 5 calls redone with size=25 got HTTP 200.
  - Only known items came back: FeVeT software, the ST2022 dataset, the CEoT submission, Lexibank 2, Open Problems, and two Latin forward-reconstruction resources (CLER/CLESp 2026, not ST2022).
- **Hugging Face papers index** (used as the arXiv proxy): 3 queries, HTTP 200, 120 results each. The relevant hits were Lu et al. 2024 (2403.18769), Lu et al. 2024 (2406.05930) and a Bantu neural-recovery paper (2604.22730, not reflex prediction). Nothing at 0.20.
- **GitHub repository search:** 4 queries, HTTP 200 ("reflex prediction" 2, ST2022 18, "sigtyp 2022" 6, "cognate reflex" 5). I inspected the candidates' trees, READMEs and reports:
  - acraevschi/cognate_reflexes_task: a student report; predictions at 0.10 and 0.50 only; surprise 0.10 NED 0.3077.
  - acraevschi/llm_cognate_reflexes: a reconstruction agent with no ST2022 scores.
  - LGirrbach/Cognate-Reflex-Prediction: README says "TODO", no scores.
  - ishana7 and vstephne: January 2023 student projects; 6 families only, no 10-family mean at 0.20.
- **HAL:** 0 hits.
- **V3R1T4S:**
  - `gh pr list --state all --limit 1000` returned 364 PRs (newest 2026-10-18T04:10:03Z). A title/branch regex for sigtyp|cognate|reflex|st2022|mockingbird|proto-form|lexibank|reconstruct|wordlist|NED|fevet|quarry matched nothing.
  - `gh pr list --search` for sigtyp, cognate, reflex, ST2022, Mockingbird, proto-form, FeVeT and lexibank returned [] for each.
  - repo/TROPHY_CASE.md: no match for sigtyp|cognate|reflex|ST2022|mockingbird|proto|Q15|quarry (grep exit 1).

## 5. Coverage gaps and blocked requests (kit rule 5)
- arxiv.org, api.semanticscholar.org, api.openalex.org and api.crossref.org were host-stopped by other lanes' 429s within the last 24 h. The helper refused them and I sent nothing to them. I also did not use export.arxiv.org, to avoid getting around the arxiv.org stop.
- dblp.org was host-stopped at 05:01:18Z, before my first DBLP request, after a challenge page answered skeptic C10-novelty. The helper refused my queued queries and none was sent.
- scholar.archive.org answered my one search (05:02:01Z) with an anti-scrape "Verify - IA Scholar" puzzle page served with HTTP 200. The helper did not flag it. I appended the line by hand to the session stop list logs/stops-2026-10-18-0202.tsv (lens C20-NOVELTY, at 05:02:21Z). The host now refuses, and I made no further request or retry.
- arXiv-only preprints were therefore covered indirectly: through the Hugging Face index, GitHub, Zenodo, and the ACL Anthology, where such work is normally published.
- injection_suspected: none seen.

## 6. Best published value at 0.20
Mockingbird-I1 (Kirov, Sproat and Gutkin 2022, aclanthology 2022.sigtyp-1.9), mean NED 0.2648052468982754, from official results-surprise-0.20.json at commit 03094435 (List, Vylomova, Forkel, Hill and Cotterell, 2022.sigtyp-1.7). FeVeT (Wientzek 2025) and Cognate Transformer (Akavarapu and Bhattacharya 2023) published nothing at 0.20. The claimed 0.20345235544710852 is strictly lower; this is a beat, not a tie.

novelty: no published value at proportion 0.20 below the claimed mean NED was found; status source read (HTTP 200, HEAD unchanged since 2022-05-27).
pass: true
