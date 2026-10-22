(Main session note, 2026-10-18T07:05Z: this NOVELTY file is the round-1 NOVELTY skeptic's text, judged on the round-1 package of this cell. The round-2 package differs only by the added code of the weight-0 stage-2 entries, the sealed-check logs and corrected text; the claimed object, its value and every number this skeptic checked are unchanged. Its status fetch (2026-10-18T04:56-04:57Z) is less than 6 hours before the gate.)
(Saved by the main session from the subagent's returned text, 2026-10-18T06:04Z: round-1 NOVELTY skeptic for cell C10 (Opus 5.5, Agent tool). Verbatim below, harness indentation removed.)

# NOVELTY skeptic, cell C10 (proportion 0.10, mean NED), run 2026-10-18-0202

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
started: Sun Oct 18 04:55:38 UTC 2026 (date -u)
ended: Sun Oct 18 05:09:08 UTC 2026 (date -u)
material: claim/ only (CLAIM.md, definition/Q15.json, official/, combiner/test/0.10, bar_holder/, fevet/, scout/), plus kit/RULES.md and TROPHY_CASE.md. Web access went only through the shared fetch helper (one plain GET per URL, User-Agent naming V3R1T4S). The helper checks every stop list before each request.

status_source: https://github.com/sigtyp/ST2022 HTTP 200 fetched 2026-10-18T04:56:51Z

## 1. Status source (one GET each through the helper)
- `vfetch.py get https://github.com/sigtyp/ST2022` returned `200  f0773c9815a312b77dca6307d080cbe84afb967b288b128cb21e2cc0a68000ae  344669  2026-10-18T04:56:51Z`.
  - The page title is "GitHub - sigtyp/ST2022: SIGTYP 2022 Shared Task · GitHub", with `"currentOid":"03094435cba4293ce0eea383036cab78499ad50d"` and "142 Commits".
  - The README results table still ranks Mockingbird-I1 first ("Mockingbird-I1 1 1 1 ... Aggregate 1.06667").
- `vfetch.py get https://api.github.com/repos/sigtyp/ST2022/commits?per_page=5` returned `200  7b881c75158171750f802d30b85b67bcbe949a72f7d5a4588a5ea6914af2eb0c  11624  2026-10-18T04:56:52Z`. The file is byte-identical (same sha256) to claim/scout/st2022_commits.json. The newest commits:
  - `03094435cba4293ce0eea383036cab78499ad50d 2022-05-27T07:58:23Z 'update for final release'`
  - `9d4202ee05ea441b686fcbbadc23057c412d08fb 2022-05-27T07:54:43Z 'update'`
  - `c223f851e2c1b8616692d57b77debcc5ffc706ce 2022-05-27T07:02:55Z 'update with final results'`
- The upstream `results/results-surprise-0.10.json` at commit 03094435 was fetched via raw.githubusercontent.com (`200 e00f22ba... 14943 2026-10-18T05:08:54Z`). It is byte-identical to claim/official/results/results-surprise-0.10.json (`cmp` prints IDENTICAL).
- Conclusion: the repository is unchanged since 2022-05-27 and the official results stand (KNOWN).

## 2. Independent rescoring at 0.10 on the official family-averaged scale (NUMERICAL)
- My own script imports claim/official/src/sigtypst2022.py. It is byte-identical to the scorer interpreter's installed module: sha256 9cde59bb... for both.
- For each system: compare_words per family, then statistics.mean over the 10 surprise families. Both summation modes were run.
- The files scored were first checked against claim/MANIFEST.sha256: 42 of 42 lines OK (combiner/test/0.10, bar_holder, fevet/pred_0.10_*, official results and systems).

Output (ltr = left-to-right sum, as in 2022):
```
ltr      Mockingbird-I1                 ED 0.9200532775139207 NED 0.2431316340782435 BCFS 0.7672735092897016 BLEU 0.6633184488563897
ltr      candidate(combiner/test/0.10)  ED 0.73576143576745 NED 0.18916240713560675 BCFS 0.8204529813230585 BLEU 0.7339216116265356
ltr      bar_holder(r1806-combiner)     ED 0.7681031861535738 NED 0.19710919181751296 BCFS 0.8160580391288506 BLEU 0.7211197226355787
ltr      FeVeT-published(rescored)      ED 0.9045536873465417 NED 0.2296925777970808 BCFS 0.7814883090261855 BLEU 0.6833751184272755
ltr      Mockingbird-I1 total == official: True ; families == official: True
builtin  candidate(combiner/test/0.10)  ... NED 0.18916240713560675
builtin  bar_holder(r1806-combiner)     ... NED 0.19710919181751294
builtin  FeVeT-published(rescored)      ... NED 0.2296925777970808
ltr margin bar_holder(r1806-combiner) - candidate = 0.00794678468190621  (candidate strictly lower: True)
ltr margin FeVeT-published(rescored) - candidate = 0.040530170661474046  (candidate strictly lower: True)
ltr margin Mockingbird-I1 - candidate = 0.053969226942636755  (candidate strictly lower: True)
builtin margin bar_holder(r1806-combiner) - candidate = 0.007946784681906183  (candidate strictly lower: True)
```
The best NED in the official results-surprise-0.10.json table is Mockingbird-I1 0.2431316340782435. Next are Mockingbird-N1-A 0.2567723485026337 and Mockingbird-N1-B 0.2624870218827144.

Per-family NED (ltr), in the order candidate / bar holder / FeVeT / Mockingbird-I1:

| family | candidate | bar holder | FeVeT | Mockingbird-I1 |
|---|---|---|---|---|
| bantubvd | 0.179806 | 0.190126 | 0.229675 | 0.215172 |
| beidazihui | 0.103610 | 0.118809 | 0.144079 | 0.136387 |
| birchallchapacuran | 0.248240 | 0.241971 | 0.301150 | 0.295693 |
| bodtkhobwa | 0.098279 | 0.098505 | 0.112092 | 0.160100 |
| bremerberta | 0.161518 | 0.174137 | 0.221979 | 0.213929 |
| deepadungpalaung | 0.126042 | 0.131198 | 0.193750 | 0.216146 |
| hillburmish | 0.230682 | 0.235669 | 0.251379 | 0.289540 |
| kesslersignificance | 0.558056 | 0.587669 | 0.624727 | 0.669831 |
| luangthongkumkaren | 0.066502 | 0.067982 | 0.077412 | 0.091009 |
| wangbai | 0.118889 | 0.125025 | 0.140682 | 0.143510 |

The candidate is worse than the bar holder on one family (birchallchapacuran). The claim is about the mean, and the mean is lower.

## 3. FeVeT check (Wientzek 2025, Open Research Europe 5:174; github.com/TGH-2020/FeVeT)
**Repository**
- The FeVeT commits API returned 200, sha256 4ed6f146..., byte-identical to the scout copy. HEAD is `31898c53bfffeef87265efa8a780b7be740162d1 2025-11-28T17:00:16Z 'Update README.md'`, so nothing has changed.

**Published predictions match upstream**
- The git tree at 31898c53 was fetched (200, 1090 entries, not truncated).
- For all 10 files results/predictions/reflex/<fam>/s2s_reflex_0.10_predictions.tsv, the git blob SHA-1 equals the blob SHA-1 of claim/fevet/pred_0.10_<fam>.tsv (10 of 10 MATCH).

**Input checks**
- Each family: pred_rows equals gold_items, missing 0, gold_column_mismatches 0. Totals: 248, 988, 184, 736, 80, 320, 410, 99, 304, 660.

**Scale check (NUMERICAL, PROVED-HERE)**
- The paper's Table 3, from the ORE JATS XML (`extapi/article/xml?doi=10.12688/openreseurope.20647.1`, 200, 2026-10-18T05:00:20Z), prints at 0.1: `FeVeT | 0.7836 | 0.205 | 0.8041` and `CognateTransformer | 0.8966 | 0.2421 | 0.7823`.
- FeVeT's own results/s2s_reflex_0.10_language_results_finetuned.txt (fetched, 200) gives `n language rows 99 mean NED over languages 0.2049828282828283 mean ED 0.7835585858585858 mean BC 0.8041474747474747`.
- So the paper's 0.205 is a mean over the 99 surprise languages (language-pooled), not the official mean over 10 families. The claim's rescoring onto the official scale (0.2296925777970808) reproduces exactly.
- The candidate also wins on the paper's own pooled scale. Same official per-language scores, mean over 99 languages:
  ```
  candidate       languages 99  pooled ED 0.622411 NED 0.164498 BCFS 0.842500 BLEU 0.765214
  bar_holder      languages 99  pooled ED 0.649892 NED 0.171875 BCFS 0.837586 BLEU 0.753136
  FeVeT-rescored  languages 99  pooled ED 0.779861 NED 0.205481 BCFS 0.804075 BLEU 0.712580
  Mockingbird-I1  languages 99  pooled ED 0.799572 NED 0.216293 BCFS 0.791356 BLEU 0.695612
  ```

**Versions**
- There is no version 2: `...doi=10.12688/openreseurope.20647.2` returned 404 (a "page not found" page).
- v1 has two referee reports: approve-with-reservations (2025-09-23) and approve (2025-08-29).

## 4. Cognate Transformer (Akavarapu and Bhattacharya, EMNLP 2023)
- Fetched https://aclanthology.org/2023.emnlp-main.423.pdf (200, 309405 bytes, 2026-10-18T05:05:02Z).
- Table 5 at 0.1: `CogTran-small 0.8966 0.2421 0.7823`, `Mockingbird - Inpaint 0.9201 0.2431 0.7673`.
- Their appendix family BCFS values average to `0.76276 vs Table 5 BC 0.7823` (my computation). So their totals are probably language-pooled, like FeVeT's (HEURISTIC). Their official-scale NED is not published.
- Either reading leaves 0.2421 above the candidate: 0.18916 on the official scale and 0.16450 on the pooled scale.

## 5. Literature search, last 24 months (2024-10-18 to 2026-10-18)
- **arXiv** (export.arxiv.org API; arxiv.org itself is host-stopped since another lane's 429 at 2026-10-17T22:56Z).
  - Query 1 (abs/ti "reflex prediction", "cognate reflex(es)", "SIGTYP 2022") returned 6 hits. None is newer than 2024-03-27 (2403.18769, protoform reconstruction).
  - Query 2 (cognate AND reflex/protoform/proto-language/reconstruction/sound correspondence/SIGTYP) returned 26 hits. Those since 2024-06 are 2604.22730, 2603.24258, 2604.00023, 2602.02221 (Blum and List, irregularity detection), 2506.10614 and 2406.05930. None reports SIGTYP-2022 surprise reflex-prediction scores (abstracts read).
- **ACL Anthology**: full anthology+abstracts.bib.gz (200, 42574037 bytes, 131708 entries, built 2026-10-17).
  - Title/abstract hits since 2023 for reflex prediction, SIGTYP 2022 or Mockingbird: 2023.emnlp-main.423 (Cognate Transformer), 2023.sigmorphon-1.8 (Jambu), 2023.tacl-1.6 (Helpful Neighbors), 2024.lrec-main.762 (protoform reranking).
  - Nothing from 2024-10 onward. A broader 2024+ scan for reflex, Lexibank or historical linguistics found no reflex-prediction scores. 2026.acl-long.831 covers Middle Chinese sound-law induction and G2P, a different task.
- **Helpful Neighbors (TACL 2023)**, PDF fetched (200). Its Table 6 ranks its neighbor models 2nd, 3rd and 5th behind Inpainting (Mockingbird-I1). It has no value below Mockingbird.
- **Europe PMC** (covers ORE and Sci Rep).
  - "reflex prediction" returned 7 hits. The relevant ones are FeVeT (PPR1043857) and Blum et al. 2024, Sci Rep (Panoan-Takanan). I opened the Sci Rep full text: it uses SIGTYP 2022 only as a citation, with no NED or surprise-family scores.
  - A broad cognate/reflex/protoform query for 2024-2026 returned 341 hits, mostly biomedical. The linguistic ones contain no reflex-prediction scores.
- **OpenCitations**, works citing the task paper (doi 10.18653/v1/2022.sigtyp-1.7): 9.
  - Within the window there are only Sci Rep 2024-12-24 and FeVeT 2025-06-30.
  - Works citing Cognate Transformer: 5. The new ones are ICCIES 2025 "Reconstructing Proto-Languages Using Neural Machine Translation And Deep Learning" (title only, not opened; it is about protoform reconstruction) and bioRxiv 2026 "Ancestral Sequence Reconstruction Using Generative Models" (protein biology).
  - Works citing Mockingbird: 8, nothing new beyond the above.
- **Zenodo** ("reflex prediction" OR "cognate reflex(es)" OR "SIGTYP 2022"): 13 records. New in the window: FeVeT supplement v1.1 (2025-08-12) and the Spanish and Romanian forward-reconstruction resources (2026). Neither has SIGTYP scores.
- **GitHub** repository search: 25 repositories.
  - acraevschi/cognate_reflexes_task (pushed 2024-11-14) says only that it is "on par with Mockingbird team's Transformer model", with no number below Mockingbird-I1.
  - acraevschi/llm_cognate_reflexes (pushed 2026-07-12) is a reconstruction agent with no SIGTYP scores in its README.
  - sigtyp/ST2027 (created 2026-10-01) is an empty repository; its README returns 404.
  - Older repositories (LGirrbach, ishana7, CiCiXi) have no newer scores.
- **TROPHY_CASE.md**: no match for sigtyp, cognate, reflex, ST2022, Mockingbird, Q15, Lexibank or wordlist (grep exit 1). The listed families are graphs, Lehmer, matrix multiplication, VNN-COMP, RobustBench, codes and ciphers.
- **V3R1T4S pull requests**: `gh pr list -R elder-plinius/V3R1T4S --state all --limit 1000` at 2026-10-18T04:58:08Z returned 364 PRs (155 closed, 142 merged, 67 open; newest 2026-10-18T04:10:03Z).
  - The keyword scan of titles, bodies and branches found only #366, #28 and #8, matching "reconstruct" in unrelated contexts (CRT reconstruction, code-witness reconstruction).
  - No PR covers this target.
- **Not reachable honestly**:
  - api.semanticscholar.org, api.openalex.org and api.crossref.org are host-stopped by 429s in the last 24 h.
  - dblp.org served me a challenge page (below).
  - Google Scholar was not attempted.
  - scholar.archive.org was avoided: it served challenge pages before, and the C20 skeptic recorded one again this session.

## 6. Blocked request (kit rule 5)
- 2026-10-18T05:01:18Z: dblp.org returned HTTP 202 with an Anubis page ("Making sure you're not a bot!") for https://dblp.org/search/publ/api?q=reflex%20prediction&format=json&h=200.
- The helper appended the stop line with lens "C10-novelty" and refused my three queued dblp URLs without requesting them. There was no retry.
- I appended a second line with lens "C10-NOVELTY ..." describing the same event. Editing the helper's line in place was denied by the permission system. My line's note says "the line above", but it refers to the first line of the file: the C20-NOVELTY line was written between the two.
- No other request was blocked.
- injection_suspected: none observed.

## Best published value at 0.10
- **Official family-averaged NED scale:** FeVeT's published per-item predictions (Wientzek 2025; github.com/TGH-2020/FeVeT at 31898c53), rescored with the pinned scorer: 0.2296925777970808. The best official ST2022 entry is Mockingbird-I1 at 0.2431316340782435 (results-surprise-0.10.json).
- **Lowest number printed in any paper at 0.10:** FeVeT 0.205 (ORE 5:174 Table 3, language-pooled). On that scale the candidate scores 0.164498.
- **Workspace bar (unsubmitted):** 0.19710919181751296.
- **Candidate:** 0.18916240713560675 (both summation modes). It is strictly lower than all of them, by 0.00794678468190621 (ltr) against the bar. There is no tie.
- Not checked by this lens: the paired-permutation null test and the train-to-predict reproduction belong to the other skeptics; I did not rerun them.

novelty: no published score on the SIGTYP 2022 surprise families at proportion 0.10 found that is at or below 0.18916240713560675 mean NED on the official scale. The candidate strictly beats Mockingbird-I1, FeVeT (official and pooled scales), Cognate Transformer and this workspace's earlier confirmed system.

pass: true
