(Saved by the main session from the subagent's returned text at 2026-10-18T22:04:28Z; the N40 NOVELTY skeptic subagent (Opus 5.5, model opus, agent a1623ee6158c5700f) could not write a file named like a report. Text verbatim below.)

# NOVELTY skeptic, cell N40 (proportion 0.40, mean NED, lower is better), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: NOVELTY (one of three skeptics). Material read: the claim package (claim/), kit RULES.md, TROPHY_CASE.md, and the shared fetch helper. Web access only through the helper (lens N40-NOVELTY).
start: Sun Oct 18 21:39:54 UTC 2026
end: Sun Oct 18 21:56:07 UTC 2026
injection_suspected: none (no fetched page contained instructions)

status_source: https://github.com/sigtyp/ST2022 HTTP 200 fetched 2026-10-18T21:40:43Z

## 1. Status source (one plain GET through the helper, stop lists checked first)
Helper output (tab-separated): `200  c16c6c5a4e8d88992c7df666de2bf93581249bdf2030dfbbaeb8473c5b93433b  344669  2026-10-18T21:40:43Z`
What the page shows (parsed from its embedded JSON):
- title "GitHub - sigtyp/ST2022: SIGTYP 2022 Shared Task · GitHub"
- refInfo.name = main, refInfo.currentOid = 03094435cba4293ce0eea383036cab78499ad50d (the newest commit oid embedded in the page; the same oid as the pinned commit named in scout/scout.md), overview.commitCount = 142, refInfo.listCacheKey = v0:1653644709.4644532 (1653644709 = Fri May 27 09:45:09 UTC 2022 by `date -u -r`), releases 7, not archived.
- The page sha256 differs from the scout copy (fec88fad...) only through per-request tokens: same size 344669 bytes, same oid. KNOWN.
Official results unchanged (PROVED-HERE): one GET of https://raw.githubusercontent.com/sigtyp/ST2022/03094435cba4293ce0eea383036cab78499ad50d/results/results-surprise-0.40.json returned `200  699aacbc94cb6d8289bb2685ac73f87e2cf72a1df22cee89a6cf8b7e1501ee86  14371  2026-10-18T21:42:19Z`; `cmp` with claim/official/results/results-surprise-0.40.json: IDENTICAL (both sha256 699aacbc...ee86).
Ranking of that file by total NED (my script, real output):
```
Mockingbird-N2                   ED 0.000000 NED 0 BCFS 0.000000 BLEU 0.000000
Mockingbird-I1                   ED 1.272494 NED 0.316240240534308 BCFS 0.642828 BLEU 0.572360
Mockingbird-N1-B                 ED 1.361814 NED 0.33494782949582314 BCFS 0.621225 BLEU 0.546609
Mockingbird-N1-A                 ED 1.454240 NED 0.3521333077310183 BCFS 0.629406 BLEU 0.529291
Mockingbird-N1-C                 ED 1.435284 NED 0.35467328872000803 BCFS 0.599932 BLEU 0.522759
Baseline-Baseline-SVM            ED 1.615853 NED 0.3890729260804659 BCFS 0.599045 BLEU 0.490334
CEoT-Extalign-RF                 ED 1.569450 NED 0.39599855357096486 BCFS 0.580452 BLEU 0.477265
Baseline-Baseline                ED 1.682128 NED 0.40106538946052545 BCFS 0.600092 BLEU 0.471656
CrossLingference-Julia           ED 1.605919 NED 0.4111909730747342 BCFS 0.641135 BLEU 0.447274
Leipzig-Transformer              ED 1.922090 NED 0.47999149421316156 BCFS 0.473622 BLEU 0.389291
```
The Mockingbird-N2 row is a placeholder for a missing submission, not a score (KNOWN, three independent checks): every family and the total are [0, 0, 0, 0] (a real NED of 0 would force BCFS 1 and BLEU 1); https://raw.githubusercontent.com/sigtyp/ST2022/03094435cba4293ce0eea383036cab78499ad50d/systems/mockingbird-n2/surprise/bantubvd/result-0.40.tsv returned `404` ("404: Not Found") while the same path at 0.10 returned `200` (6284 bytes, real predictions); the Mockingbird paper (aclanthology 2022.sigtyp-1.9, p. 75) says "the N2 configuration was only trained in the 10% ("dense") sparsity condition", and the task paper (2022.sigtyp-1.7) says N2 "was only applied to the 0.1 proportion" and lists no N2 row in its 0.4 table.
Mockingbird-I1 total = mean of its 10 family NEDs: my script printed `n fams 10 mean of family NED (sorted order) 0.316240240534308 official total 0.316240240534308`.

## 2. The claimed value (only to fix what is compared; reproduction is the REPRODUCE skeptic's job)
`python3 checker/check_q15.py . object/predictions-0.40.tsv` (standard library only, run by me from outside claim/), real output:
```
1. Mockingbird-I1 mean NED recomputed 0.316240240534308, official 0.316240240534308: EXACT
3. object mean NED 0.2455448938803044 over 14992 items (claimed 0.2455448938803044): EQUAL
   margin vs Mockingbird-I1 0.070695346654 (lower is better)
4. rebuilt official-format files equal to the frozen ones: 10 of 10
PASS
```

## 3. Literature and code search (one GET per resource, all through the helper; 49 GETs, none blocked for this lens)
### 3a. FeVeT (Wientzek 2025, Open Research Europe 5:174)
- https://github.com/TGH-2020/FeVeT (200, 21:42:19Z): oid 31898c53bfffeef87265efa8a780b7be740162d1 (unchanged from scout/scout.md), 29 commits. results/ tree (200, 21:43:33Z) holds reflex files only for 0.10, 0.30, 0.50 (s2s_reflex_0.10/0.30/0.50_family_results[_finetuned].txt, s2s_reflex_avg.txt, s2s_reflex_finetuned_avg.txt). KNOWN.
- raw results at that oid (200, 21:43:40Z): s2s_reflex_finetuned_avg.txt = `0.10 0.7836 0.205 0.8041 / 0.30 0.9589 0.2397 0.7232 / 0.50 1.1111 0.2825 0.673` (Proportion, ED, NED, B3_F1); s2s_reflex_avg.txt = 0.10 NED 0.2525, 0.30 NED 0.2837, 0.50 NED 0.3222. No 0.40 row.
- Article full text via the ORE JATS API https://open-research-europe.ec.europa.eu/extapi/article/xml?doi=10.12688/openreseurope.20647.1 (200, 21:49:42Z; the plain article page is a script-only shell): "the model is evaluated on the 10%, 30%, and 50% test proportions of the surprise data"; Table 3 rows at 0.1, 0.3, 0.5 only (FeVeT NED 0.205, 0.2397, 0.2825). Only version 1 exists: doi.org handle API gave 200 for 10.12688/openreseurope.20647.1 and 404 (responseCode 100, not found) for .2. KNOWN.
- Scale note (PROVED-HERE, my arithmetic on FeVeT's own per-family files): the official scale averages the 10 family means; FeVeT's per-family finetuned files average to `0.30: 0.270490` and `0.50: 0.311060`, versus 0.2397 and 0.2825 in its avg file, so FeVeT's headline numbers are on a different (not family-averaged) scale. On either scale every FeVeT number, even at the easier 0.30, is above 0.2455448938803044, and no 0.40 value exists.
### 3b. Cognate Transformer (Akavarapu and Bhattacharya, EMNLP 2023, aclanthology 2023.emnlp-main.423)
- PDF (200, 21:45:41Z), section 4.1: "Surprise data was divided into different test proportions of 0.1, 0.2, 0.3, 0.4, and 0.5 for evaluation. Among these, we only report for the test proportions 0.1, 0.3, and 0.5." Table 5 (CogTran-small NED): 0.1 0.2421, 0.3 0.2919, 0.5 0.3332; Appendix A also 0.1/0.3/0.5 only.
- Code repo https://github.com/mahesh-ak/CognateTransformer (200, oid 4da845d4f49c055b82ee4a1c98bfc1f5333c07c3); results/reflex_small.tsv and reflex_tiny.tsv at that oid list test_prop 0.10, 0.30, 0.50 only.
- Correction (kit rule 14): rules/PREREG.md (lines 69-70: "a table at 0.50 only") and scout/scout.md (lines 14-15: "reports 0.50 only") misstate this; the paper reports 0.10, 0.30 and 0.50. The conclusion they draw (no 0.40 value) is correct, so the bar does not move. KNOWN.
### 3c. Primary 2022 sources (could they move the bar?)
- Task paper 2022.sigtyp-1.7 (200, 21:53:46Z), Table 3, "Proportion in Test: 0.4": best NED Mockingbird-I1 0.3162 (ED 1.2725, B-Cubes 0.6428, BLEU 0.5724), equal to the JSON; no N2 row.
- Mockingbird paper 2022.sigtyp-1.9 (200, 21:53:34Z): "we only discuss the 10% ("dense") and 50% ("sparse") conditions"; Tables 2 and 3 are 0.10 and 0.50. No extra 0.40 value.
### 3d. Index searches
- ACL Anthology: full anthology+abstracts.bib.gz (200, 21:43:55Z, 42574037 bytes, gzip build Sat Oct 17 12:23:28 2026, 131708 entries; 2024: 12135, 2025: 14931, 2026: 10822 entries). Regex over titles and abstracts (reflex prediction, cognate reflex, SIGTYP 2022, ST2022, Mockingbird, protoform, cognate, sound correspondence, ...) plus author filter (Akavarapu, Wientzek, Kirov, List, Mortensen, Jäger, Forkel, Vylomova) for 2024-2026, and full listings of SIGTYP 2024, 2025, 2026 and LChange 2026: no paper after 2023.emnlp-main.423 reports reflex prediction on the ST2022 surprise data. Nearest items checked by abstract: 2024.lrec-main.762 (protoform reranking, Chinese/Romance), 2024.acl-long.788, 2024.emnlp-main.362, 2026.lchange-1.6 (irregular cognates), 2025.sigtyp-1.6, 2026.acl-long.831: none on this task.
- OpenCitations (api.opencitations.net, 200): 9 works cite the task paper DOI 10.18653/v1/2022.sigtyp-1.7 and 8 cite the Mockingbird paper; the only ones on reflex prediction are FeVeT (2025-06-30) and Cognate Transformer (2023, plus arXiv 2310.07487); also Blum et al. 2024 (Sci. Rep., 10.1038/s41598-024-82515-3, Panoan-Takanan data; Europe PMC full text PMC11668889: 0 hits for "0.4", "proportion", "Mockingbird", "NED"), Greenhill 2024 (osf.io/628cv, phylogenetics), Jambu 2023, TACL 2023, List 2023/2024 ORE review "Open Problems in Computational Historical Linguistics" (Europe PMC full text PMC10864822: 0 hits for "0.4", "proportion", "NED"), and IIHC 2022 "Language Model Based Related Word Prediction From An Indian Epic-Mahabharata" (OpenCitations metadata; unrelated).
- arXiv via export.arxiv.org API (3 queries, 200; arxiv.org itself is host-stopped and was not contacted): newest reflex-prediction hit is 2403.18769 (2024-03-27); a date-sorted query on cognate/protoform terms (227 results) shows no ST2022 reflex-prediction paper since 2024-10.
- Europe PMC (3 searches + 1 full text, 200), Zenodo API (200 with size=25; size=100 gave 400, a validation error, not a block): 13 Zenodo hits, newest relevant is the FeVeT supplement 10.5281/zenodo.16813907 (2025-08-12, same results as the repo); Hugging Face papers search (200), OpenReview API (200, 362 hits; only CT and LREC 2024 relevant), sigtyp.github.io/st2022.html (200, no results table).
- GitHub repository search (3 searches, 200, before the stop below): sigtyp 2022 (6 repos), "reflex prediction" (2), cognate reflex (5). Checked: acraevschi/cognate_reflexes_task (predictions at 0.10 and 0.50 only, README "on par with Mockingbird team's Transformer model"), acraevschi/llm_cognate_reflexes (reconstruction workbench, no ST2022 scores in README or cognate_reflexes/), CiCiXi/ling_sigtyp_2022 (README only); the rest were last updated before 2023-02 (shared-task systems, student projects, or the unrelated MRL 2022 morphology task).
- Unavailable (stopped hosts, not requested): api.semanticscholar.org, api.openalex.org, api.crossref.org, dblp.org, scholar.archive.org, arxiv.org, ieeexplore.ieee.org, api.github.com, and github.com after 21:48:35Z. HEURISTIC: the search is broad but not exhaustive; a paper in a venue indexed only by those services could be missed.

## 4. V3R1T4S trophy case and pull requests
- TROPHY_CASE.md (local copy): grep for sigtyp|st2022|cognate|reflex|mockingbird|fevet|lexibank: 0 lines. Live copy https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md (200, 21:51:20Z, 31235 bytes, sha256 b946f68e...171a1): 0 lines; live README.md (200, 21:51:26Z): 0 lines.
- Pull requests: github.com became host-stopped during this panel (this session's stop list: `2026-10-18T21:48:35Z 429 github.com https://github.com/search?q=sigtyp+2022&type=repositories&s=updated&o=desc B40-NOVELTY`), before my planned PR queries, so I made no live PR request (rule 5). My own 12 github.com GETs (21:40:43Z to 21:48:35Z, all 200) may have added to that shared rate limit. Instead I parsed the package's snapshots, whose sha256 match scout/scout.md: scout/v3r1t4s_pulls_all.html (72e98718...0ad1): totalCount 420, openCount 123, closedCount 297, PR numbers 406-430 on the page, 0 titles matching sigtyp|cognate|reflex|st2022|mockingbird|fevet|proto-form|lexibank|linguist|Q15|quarry; scout/v3r1t4s_pulls_search.html (7d506467...45f31, query "is:pr sigtyp OR cognate OR reflex OR ST2022 OR Mockingbird OR FeVeT OR proto-form"): openCount 0, closedCount 0. This covers open and closed PRs as of 2026-10-18T18:07:43Z, not the last 3.8 h. KNOWN (as of that time).

## 5. Verdict
best published value at proportion 0.40, mean NED (official family-averaged scale): Mockingbird-I1 0.316240240534308 (sigtyp/ST2022 results/results-surprise-0.40.json at commit 03094435cba4293ce0eea383036cab78499ad50d; task paper 2022.sigtyp-1.7 Table 3 prints 0.3162). FeVeT and Cognate Transformer publish no 0.40 value; nothing newer reporting 0.40 was found.
novelty: the claimed 0.2455448938803044 is lower than every published value I could find at 0.40 (margin 0.070695346654 to Mockingbird-I1; not a tie). Scope: NED at 0.40 only; this panel does not judge reproduction, data-use rules or the development-family rows disclosed in CLAIM.md (REPRODUCE and CRITERION lenses).
caveats: the live V3R1T4S PR re-check was impossible after the github.com stop (snapshot of 18:07:43Z used); several literature indexes were stopped; PREREG.md and scout.md misstate Cognate Transformer's proportions (no effect on the bar).
pass: true