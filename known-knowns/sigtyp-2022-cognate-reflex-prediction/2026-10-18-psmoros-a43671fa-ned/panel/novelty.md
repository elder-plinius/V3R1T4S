(Saved by the main session from the subagent's returned text at 2026-10-18T22:54:04Z; the NA NOVELTY skeptic subagent (Opus 5.5, model opus, agent a94ebb069e409d967) could not write a file named like a report. Text verbatim below.)

# Panel: NOVELTY skeptic, cell NA (aggregate A_NED over P = 0.10, 0.20, 0.30, 0.40, 0.50), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: NOVELTY
started: Sun Oct 18 22:10:25 UTC 2026 (date -u)
ended: Sun Oct 18 22:19:05 UTC 2026 (date -u)
material: the claim package only (claim/CLAIM.md, claim/definition/Q15.json, claim/official/, claim/scout/scout.md, claim/checker/), kit RULES.md, the local copy of TROPHY_CASE.md, and the web through the session's shared fetch helper (lens NA-NOVELTY). I read no other files in the workspace.

## Claim under test
claim/CLAIM.md: classifier/PRIMARY has aggregate A_NED = (S(0.10)+S(0.20)+S(0.30)+S(0.40)+S(0.50))/5 = 0.23164186694791358 (family-mean NED under the pinned official scorer, summed left to right). The bar is Mockingbird-I1's A_NED of 0.2931673956342817, taken from its official results-surprise-P.json totals. Lower is better.

## 1. Stop lists checked before any request
- The session stop list contains one line: `2026-10-18T21:48:35Z 429 github.com https://github.com/search?q=sigtyp+2022&type=repositories&s=updated&o=desc B40-NOVELTY`.
- I also read every stops-*.tsv in both workspaces' logs that changed in the last 24 h. They stop these hosts or URLs: api.github.com (ALL, from 2026-10-18T11:55:06Z), an ieeexplore.ieee.org URL (challenge), arxiv.org (429), spiral.imperial.ac.uk (405), oeis.org (challenge), qmro.qmul.ac.uk (403), dr.ntu.edu.sg (405), api.semanticscholar.org (429), dblp.org (challenge) and scholar.archive.org (challenge).
- I contacted none of these hosts. I did not contact github.com or api.github.com.
- Before the first fetch, `vfetch.py check` printed "OK" for each of the five status URLs.
- None of my 41 requests got 401, 403, 405, 429, 503 or a challenge page, so I added nothing to the stop list. The last line of the stop list was still the 21:48:35Z github.com line when I finished.
- Non-block statuses, none retried:
  - Two Zenodo queries returned 400 with "Page size cannot be greater than 25". I then sent different queries with size=25.
  - aclanthology.org/volumes/2026.sigtyp-1/ returned 404.
  - api.crossref.org/works/10.12688/openreseurope.20647.2 returned 404.
  - Europe PMC fullTextXML for PPR1043857 returned 500.

## 2. Status source (official results files; one plain GET each through the helper)
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.10.json HTTP 200 fetched 2026-10-18T22:10:57Z
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.20.json HTTP 200 fetched 2026-10-18T22:10:57Z
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.30.json HTTP 200 fetched 2026-10-18T22:10:57Z
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.40.json HTTP 200 fetched 2026-10-18T22:10:58Z
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.50.json HTTP 200 fetched 2026-10-18T22:10:58Z

Each fetched file compared with claim/official/results/results-surprise-P.json, the pinned copy at commit 03094435 (`shasum -a 256` plus `cmp`):

| P | sha256 (fetched = pinned) | bytes | cmp |
|---|---|---|---|
| 0.10 | e00f22badafe95729d8a079f0563175528fa63248c62bf7a41de2f43029f4c75 | 14943 | IDENTICAL |
| 0.20 | 80f2b01eb4e6f6c2130749f7eff149dc95fd4c59044ec9b8b22836b74dbbf519 | 14316 | IDENTICAL |
| 0.30 | cca55c5fffa730c29ef578f022741f3a0378ca333e5a20493e23e2d400792563 | 14361 | IDENTICAL |
| 0.40 | 699aacbc94cb6d8289bb2685ac73f87e2cf72a1df22cee89a6cf8b7e1501ee86 | 14371 | IDENTICAL |
| 0.50 | 3a8e79f9e686a4835f6bd0948529838b4ebb38ef2f02e05d39dfa73389a014f3 | 14362 | IDENTICAL |

- These sha256 values also equal the entries in claim/MANIFEST.sha256. `shasum -a 256 -c` printed OK for all five, and for all 470 manifest lines (no non-OK line).
- Result (PROVED-HERE, byte comparison): the official results on the current main branch are byte-identical to the pinned copies. The official table is unchanged and the status is established.
- I also fetched the main-branch README once: https://raw.githubusercontent.com/sigtyp/ST2022/main/README.md, HTTP 200, 2026-10-18T22:17:54Z. Its meta-evaluation table aggregates ranks, not scores. For example, its row "Mockingbird-I1 ... Aggregate 1.06667, Aggregate (STD) 0.258199" is a mean rank (KNOWN).

## 3. Aggregate of every official system (my own script over the fetched files; left-to-right sums)
| system | A_NED (totals, L2R) | per-P NED totals 0.10 / 0.20 / 0.30 / 0.40 / 0.50 |
|---|---|---|
| Mockingbird-N2 | 0.06269171285472723 | 0.31345856427363616 / 0 / 0 / 0 / 0 (placeholder, see below) |
| Mockingbird-I1 | 0.2931673956342817 (builtin sum 0.29316739563428174) | 0.2431316340782435 / 0.2648052468982754 / 0.2898984929868421 / 0.316240240534308 / 0.35176136367373956 |
| Mockingbird-N1-B | 0.314248874788133 | 0.2624870218827144 / 0.290102017112842 / 0.3103285732011085 / 0.33494782949582314 / 0.3733789322481769 |
| Mockingbird-N1-A | 0.3166522361794327 | |
| Mockingbird-N1-C | 0.3326146264819196 | |
| Baseline-Baseline-SVM | 0.34743783782430304 | |
| CEoT-Extalign-RF | 0.3599634843631829 | |
| Baseline-Baseline | 0.3698412067899648 | |
| CrossLingference-Julia | 0.4071544066766225 | |
| Leipzig-Transformer | 0.4451431775904207 | |

- Mockingbird-N2's apparent 0.0627 is not a score. At 0.20 to 0.50 all ten families are [0, 0, 0, 0], with BCFS and BLEU also 0, which a real system could not get.
- The pinned scorer writes exactly this placeholder when a results file is missing. claim/official/src/sigtypst2022.py line 527 has `except FileNotFoundError:` and line 531 has `results[stm][dataset] = [0, 0, 0, 0]`.
- The official meta-evaluation also excludes N2: line 716 has `if x["method"] !="N2"`. N2 submitted 0.10 only and has no five-proportion aggregate.
- The best official aggregate is therefore Mockingbird-I1's 0.2931673956342817, equal to the stated bar (NUMERICAL). The claimed 0.23164186694791358 is lower by 0.0615255286863681 (my script's output).
- Consistency check: I ran the package's standalone checker (`python3 checker/check_q15.py . object`, my own interpreter, rc=0). Key lines:
  - "3. Mockingbird-I1 A_NED from the official totals 0.2931673956342817 (PREREG 0.2931673956342817): EQUAL"
  - "4. object A_NED 0.23164186694791358 (claimed 0.23164186694791358): EQUAL"
  - "margin vs Mockingbird-I1 0.061525528686 (lower is better)"
  - "5. rebuilt official-format files equal to the frozen ones: 50 of 50"
  - Last line: "PASS"
  - At each P it also printed "Mockingbird-I1 mean NED recomputed ... : EXACT".
- I only checked the arithmetic and the bar. Training cleanliness belongs to the REPRODUCE and CRITERION skeptics.

## 4. Literature search, last 24 months (2024-10 to 2026-10); one GET per resource, 36 requests, all through the helper
OpenAlex:
- Task paper: W4287889593, cited_by_count 15. Its 15 citing works list (fetched 22:11:58Z) has only three items from 2024-10 on:
  - Sci. Rep. 2024-12-24 (Panoan and Takanan reflex prediction as a hypothesis test; field elicitation, not the ST2022 data);
  - FeVeT, Open Research Europe, 2025-06-30;
  - none other.
- Works citing Cognate Transformer (W4389520718): 3 results.
  - ICCIES 2025, proto-language NMT. It sits on ieeexplore, which is stop-listed. Its OpenAlex abstract describes proto-form reconstruction with no ST2022 or proportion results.
  - FeVeT.
  - A bioRxiv 2026 paper on protein ancestral sequence reconstruction.
- Works citing FeVeT: 0.
- Works citing Mockingbird (W4287888114), the other three ST2022 system papers, and the trimming and uncertainty papers, from 2024-10-01 on: only the Lexibank 2 versions and FeVeT.
- Keyword searches from 2024-10-01: "reflex prediction" (21 hits), "SIGTYP 2022 cognate" (15), "cognate reflex" (617, filtered by computational keywords), "phonological reconstruction" (179).
- Full-text search for "SIGTYP 2022" (2 hits: Sci. Rep. and an unrelated PIE paper).
- I read the abstracts of all 12 plausible candidates. They include LChange'26 "Using Correspondence Patterns to Identify Irregular Words..." (a regularity measure, not reflex-prediction scores), borrowing detection, phylogenetic representation learning, and a neural Bantu morphology paper. None reports ST2022 surprise reflex-prediction scores.

Other sources:
- OpenCitations COCI, citations of 10.18653/v1/2022.sigtyp-1.7: 9 citing items. In-window: Sci. Rep. 2024-12-24 and FeVeT 2025-06-30 only.
- Crossref query "cognate reflex prediction" from 2024-10-01: the only relevant hits are Sci. Rep., FeVeT and FeVeT's two review reports.
- Europe PMC ("reflex prediction" OR "SIGTYP" OR "cognate reflexes"): 10 hits. The relevant ones are Sci. Rep., FeVeT (PPR1043857), Open Problems (2023) and Lexibank 2.
- Zenodo ("reflex prediction"; "SIGTYP cognate"; "cognate reflex"): nothing new except FeVeT's supplementary record 16813907 and two Latin-to-Romance forward-reconstruction resources (not ST2022).
- ACL Anthology:
  - SIGTYP 2024 and 2025 volume pages: no reflex-prediction paper. 2025.sigtyp-1.6 "Beyond cognacy" is about phylogenetics; I read its abstract.
  - 2026.sigtyp-1: 404.
  - LChange 2024 and LChange'26 volumes: no reflex-prediction result.
- raw.githubusercontent.com: the FeVeT README and the Cognate Transformer README. Neither gives five-proportion surprise results.

Known prior results, verified from the sources themselves:
- FeVeT (Wientzek 2025, Open Research Europe 5:174):
  - The ORE v1 XML (HTTP 200, 22:14:17Z) says "the model is evaluated on the 10%, 30%, and 50% test proportions of the surprise data".
  - Table 3 FeVeT NED: 0.1 = 0.205, 0.3 = 0.2397, 0.5 = 0.2825.
  - Crossref has no version 2 (10.12688/openreseurope.20647.2 returned 404).
  - The Zenodo archive FeVeT-v1.1.zip (HTTP 200, 22:14:57Z, sha256 e82909eb3a30c2498637d8b46e824d957d66902464a4967bf4a48d1ef01946ae) has reflex predictions only for _0.10_, _0.30_ and _0.50_ (10 files each).
  - Its finetuned family-result files give family-mean NED 0.22892 / 0.27049 / 0.31106.
  - Either way, classifier/PRIMARY is lower at each of these three proportions: 0.20017478183757248 / 0.23201071558421696 / 0.26834206801685595.
  - FeVeT has no 0.20 or 0.40 value and no five-proportion aggregate (KNOWN, verified).
- Cognate Transformer (Akavarapu and Bhattacharya, EMNLP 2023; PDF HTTP 200, 22:15:04Z): "Surprise data was divided into different test proportions of 0.1, 0.2, 0.3, 0.4, and 0.5 for evaluation. Among these, we only report for the test proportions 0.1, 0.3, and 0.5." Table 5 CogTran-small NED: 0.2421 / 0.2919 / 0.3332. No aggregate (KNOWN, verified).

Best published aggregate:
- No publication I could reach reports surprise-family scores at all five proportions with a mean over proportions, other than the official results files.
- The best published five-proportion aggregate is therefore Mockingbird-I1's 0.2931673956342817, computed from the official results-surprise-P.json totals (source: the ST2022 results files above).
- No published value moves the bar.

## 5. Crowd checks
- TROPHY_CASE.md (local copy, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9, 100 lines): grep for sigtyp, cognate, reflex, ST2022, mockingbird, FeVeT, quarry, lingu, phonolog and language found nothing. There is no entry for this target.
- The V3R1T4S pull-request list lives on github.com, which is host-stopped for this session (429 at 2026-10-18T21:48:35Z). I did not contact it and could not re-check it myself. The only record is the main session's scout (claim/scout/scout.md, fetched 2026-10-18T18:07:43Z), which reports a keyword search with 0 open and 0 closed matches. That check is not mine.

## 6. Limits of this search (HEURISTIC: absence cannot be proved)
- Not consulted, because their hosts are stop-listed: arXiv, Semantic Scholar, dblp, IA Scholar, GitHub search. Google Scholar was not used.
- arXiv items were covered indirectly through OpenAlex, which returned arXiv records in these searches.
- Non-English and paywalled venues may be under-covered.
- injection_suspected: none (I grepped the fetched content for instruction-like text and found none).

## Verdict
- Status: established. The five official results files on main are byte-identical to the pinned copies.
- Bar: Mockingbird-I1's A_NED 0.2931673956342817 is the best official five-proportion aggregate. N2's lower number is a missing-file placeholder.
- Literature: I found no published five-proportion aggregate on the official family-averaged scale, and no published value that would move the bar. The three-proportion results of FeVeT and Cognate Transformer are all higher (worse) than the claim's values at the same proportions.
- The claimed A_NED 0.23164186694791358 is strictly lower than everything known, by 0.061525528686. It is not a tie.
- Scope, one sentence: on the ten SIGTYP 2022 surprise families, mean NED over the five proportions 0.10 to 0.50, classifier/PRIMARY's 0.23164186694791358 is lower than every published value I could find (best: Mockingbird-I1, 0.2931673956342817). This judges novelty only, not training cleanliness.
novelty: no prior published result found that beats or ties the claim
pass: true