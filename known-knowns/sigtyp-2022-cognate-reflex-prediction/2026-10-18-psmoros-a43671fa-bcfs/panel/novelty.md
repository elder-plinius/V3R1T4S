(Saved by the main session from the subagent's returned text at 2026-10-18T22:54:04Z; the BA NOVELTY skeptic subagent (Opus 5.5, model opus, agent a77fe41b5e80d8d94) could not write a file named like a report. Text verbatim below.)

# NOVELTY skeptic, cell BA (aggregate of mean BCFS over the five proportions 0.10-0.50), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: NOVELTY (one of three skeptics), lens field in stop lists: BA-NOVELTY
start: 2026-10-18T22:10:21Z (date -u)
end: 2026-10-18T22:21:36Z (date -u)
material: claim/ only (CLAIM.md, definition/Q15.json, official/, scout/, object/, attempts/classifier/frozen/PRIMARY/test/), plus kit RULES.md, the local TROPHY_CASE.md, the shared fetch helper (run as `vfetch.py get URL OUTFILE --lens BA-NOVELTY`) and the interpreters named in my instructions. Scratch files went in the skeptic's own scratch folder, outside claim/.
injection_suspected: none

## 1. Status source (primary table: official results files)

Before each request I ran the helper's `check` and looked at every stops-*.tsv changed in the last 24 h. Stopped at host level: github.com (429, 21:48:35Z), api.github.com (403, ALL), dblp.org, scholar.archive.org, ieeexplore.ieee.org, oeis.org (challenge), arxiv.org (429, the other lane's list) and api.semanticscholar.org (429). I contacted none of these. All five status URLs returned `OK` from `check`. I made one plain GET each through the helper, with no retries:

status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.10.json HTTP 200 fetched 2026-10-18T22:11:30Z
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.20.json HTTP 200 fetched 2026-10-18T22:11:30Z
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.30.json HTTP 200 fetched 2026-10-18T22:11:31Z
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.40.json HTTP 200 fetched 2026-10-18T22:11:31Z
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.50.json HTTP 200 fetched 2026-10-18T22:11:31Z

I compared each fetched file with claim/official/results/results-surprise-P.json, the copy pinned at commit 03094435, using sha256 and `cmp`:
| P | fetched sha256 (bytes) | pinned copy sha256 (bytes) | cmp |
|---|---|---|---|
| 0.10 | e00f22badafe95729d8a079f0563175528fa63248c62bf7a41de2f43029f4c75 (14943) | same (14943) | IDENTICAL |
| 0.20 | 80f2b01eb4e6f6c2130749f7eff149dc95fd4c59044ec9b8b22836b74dbbf519 (14316) | same (14316) | IDENTICAL |
| 0.30 | cca55c5fffa730c29ef578f022741f3a0378ca333e5a20493e23e2d400792563 (14361) | same (14361) | IDENTICAL |
| 0.40 | 699aacbc94cb6d8289bb2685ac73f87e2cf72a1df22cee89a6cf8b7e1501ee86 (14371) | same (14371) | IDENTICAL |
| 0.50 | 3a8e79f9e686a4835f6bd0948529838b4ebb38ef2f02e05d39dfa73389a014f3 (14362) | same (14362) | IDENTICAL |
The same five hashes are listed in claim/MANIFEST.sha256. Result: the official table on the main branch has not changed since the pinned commit, so the status is established (KNOWN).

## 2. Official systems' aggregates (computed from the fetched files)
For every system, A_BCFS is the mean over the five proportions of its "total" BCFS, summed left to right (my own script, python3.13 -I). Output, verbatim:
- Mockingbird-I1 A_BCFS (left to right) = 0.6797616040522236, builtin sum = 0.6797616040522234; per P: 0.767274, 0.711966, 0.67171, 0.642828, 0.605031
- Mockingbird-N1-A 0.6685038317882127
- CrossLingference-Julia 0.664930871621116
- Mockingbird-N1-B 0.6617782236834785
- Baseline-Baseline-SVM 0.6524132392380897
- Mockingbird-N1-C 0.6384489971562578
- Baseline-Baseline 0.6380018455401131
- CEoT-Extalign-RF 0.6320553613131523
- Leipzig-Transformer 0.5268487497003421
- Mockingbird-N2 0.1410805359785975 (zeros at 0.20-0.50: missing files)
- At each P, Mockingbird-I1's total BCFS equals the mean of its 10 family BCFS values (difference 0.0 at all five P).
- Output lines: "claimed A 0.7422025452564412 minus best official 0.062440941204217615 best official Mockingbird-I1" and "strictly beats every official aggregate: True".
The bar is confirmed: Mockingbird-I1's aggregate 0.6797616040522236 is the best official one. The builtin-sum value differs only by 2e-16 (Python 3.13's compensated sum), which does not matter here.

I also checked the README's meta-evaluation table. raw.githubusercontent.com/sigtyp/ST2022/main/README.md returned HTTP 200 at 2026-10-18T22:21:02Z, sha256 51bf43bf61e21f55e07bf056ca2960a6eb49dbcfc830d06ee6855dbca7493d63. Line 115 reads "They contain all ranks for the various cuts of the data". The Mockingbird-I1 row is ranks only (BCFS rank 2 at proportion 5; "Aggregate 1.06667"). So the README aggregates ranks, not scores (KNOWN).

## 3. Incidental re-scoring with the pinned scorer (NUMERICAL)
The installed scorer module (the interpreter with the official scorer installed) has sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a, identical to claim/official/src/sigtypst2022.py. I wrote a small driver that calls compare_words(solutions, result) per family and takes statistics.mean over the 10 families.
- Pipeline check: Mockingbird-I1 at 0.10 (claim/official/systems/mockingbird-i1) gives "TOTAL 0.10 ... BCFS 0.7672735092897016". This matches the official total exactly.
- The candidate's frozen files claim/attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv give BCFS 0.8091752827860231 (0.10), 0.7629197798251665 (0.20), 0.7347693490340722 (0.30), 0.7136377968288752 (0.40), 0.690510517808069 (0.50).
- That makes A_BCFS = 0.7422025452564412 summed left to right, and the same with the builtin sum. "A - bar: 0.062440941204217615 strictly greater: True". All five values equal the CLAIM.md table.
- claim/object/predictions-P.tsv equals the non-empty cells of the frozen result files ("identical: True" at all five P; 4029, 7887, 11586, 14992 and 18101 rows).

## 4. Literature search, last 24 months and beyond (one GET per resource, all through the helper, no blocks)
Requests (HTTP status, UTC time):
- OpenAlex: task paper doi:10.18653/v1/2022.sigtyp-1.7, W4287889593, 200 22:12:11Z. Works citing it: 200 22:12:16Z, 15 works. Mockingbird paper doi:10.18653/v1/2022.sigtyp-1.9: 200 22:12:26Z. Works citing Mockingbird: 200 22:12:44Z, 10. Works citing Cognate Transformer: 200 22:12:26Z, 3. Works citing FeVeT: 200 22:12:27Z, 0. Searches from 2024-10-01: "reflex prediction" (search) 200 22:12:27Z; title/abstract "cognate reflex" 200 22:12:44Z (6); title/abstract "reflex prediction" 200 22:12:45Z (276); fulltext "SIGTYP 2022" 200 22:12:47Z (117); title/abstract "protoform reconstruction" 200 22:15:05Z (5); title/abstract "phonological reconstruction" 200 22:15:06Z (216); fulltext "cognate reflexes" 200 22:15:08Z (461); fulltext "cognate reflex prediction" 200 22:18:41Z (122).
- ACL Anthology volumes: 2024.sigtyp-1 200, 2025.sigtyp-1 200, 2026.sigtyp-main 200, 2024.lchange-1 200, 2025.lchange-1 404, 2026.lchange-1 200 (22:13:21Z to 22:13:24Z). Paper page 2025.sigtyp-1.6 200 22:19:38Z. Paper 2023.emnlp-main.423.pdf 200 22:14:50Z, sha256 4ede9ad5014866cdfa89f3a0f8eeaf754c50c8439284bb22e2ef7be7c766f38d.
- Open Research Europe: article page 5-174 200 22:13:20Z (JavaScript shell, no text). /v1/xml 200 22:14:20Z, sha256 320a1e5af399ff68bf4863518946f97e54bcdf3494b0678a0753b00c16b7e93f. /v2/xml 500 22:14:22Z (server-error page, no v2 found; not a block status, not retried).
- Europe PMC: "reflex prediction" 200 22:13:58Z (7 hits), SIGTYP 200 22:13:59Z (4), "cognate reflex" 200 22:14:00Z (2). PPR1043857 fullTextXML 500 22:14:13Z (not retried).
- Zenodo: three searches with size=100 returned 400 at 22:15:26-29Z (validation error "Page size cannot be greater than 25"; not a block). New searches with size=25 all returned 200: "reflex prediction" (13), "SIGTYP 2022" (4), "cognate reflex" (3), "ST2022 surprise" (2226, noise). Records 15619250 (200) and 16813907. Archive TGH-2020/FeVeT-v1.1.zip: 200 22:16:14Z, 84314976 bytes, md5 237538887be0e533b2a59156a6a2620a, which equals Zenodo's listed checksum. I only listed and read it as data; I ran none of its code.
- raw.githubusercontent.com: mahesh-ak/CognateTransformer/main/README.md 200 22:18:39Z (usage text only, no results). TGH-2020/FeVeT/main/README.md 200 22:18:40Z (differs from the v1.1 archive README only in the citation year, line 14).
- Crossref: query "cognate reflex prediction" from 2024-10-18, 200 22:18:40Z.

Findings:
- FeVeT (Wientzek 2025, Open Research Europe 5:174, v1; KNOWN, read here):
  - The text says "the model is evaluated on the 10%, 30%, and 50% test proportions of the surprise data". Table 3 gives FeVeT BC 0.8041 / 0.7232 / 0.673 at 0.1 / 0.3 / 0.5.
  - These are averages over the 99 languages pooled across families, computed with FeVeT's own scorer (code/result_eval.py, avg_results_reflex: "averaged over languages"). They are not on the official family-mean scale.
  - The v1.1 archive holds reflex results and predictions for 0.10, 0.30 and 0.50 only. There are no 0.20 or 0.40 files and no aggregate.
  - FeVeT's data-surprise files (90 training/test/solutions files) are byte-identical to claim/official/data-surprise ("compared 90 files, differing 0").
  - I scored FeVeT's published per-item predictions with the pinned official scorer: BCFS 0.7814883090261855 (0.10), 0.6986581179861968 (0.30), 0.6423935720824072 (0.50), with no "Missing entry" warnings. The candidate is higher at each of these by 0.027687, 0.036111 and 0.048117.
  - The predictions belong to the fine-tuned FeVeT run: language-averaged ED recomputed from them is 0.7786 / 0.9398 / 1.1126, against 0.7836 / 0.9589 / 1.1111 fine-tuned and 0.9451 / 1.1046 / 1.2405 not fine-tuned (NUMERICAL).
- Cognate Transformer (Akavarapu and Bhattacharya, EMNLP 2023, 2023.emnlp-main.423; KNOWN, read here):
  - The text says "Surprise data was divided into different test proportions of 0.1, 0.2, 0.3, 0.4, and 0.5 for evaluation. Among these, we only report for the test proportions 0.1, 0.3, and 0.5."
  - Table 5 gives CogTran-small BC 0.7823 / 0.6954 / 0.6477, all below the candidate's 0.8092 / 0.7348 / 0.6905. I did not verify the scale these numbers are on.
  - Correction to the package: claim/scout/scout.md says Cognate Transformer "reports 0.50 only". The paper reports 0.1, 0.3 and 0.5. This does not affect the verdict, since neither system gives 0.20, 0.40 or an aggregate.
- Other works found from the last 24 months: none reports SIGTYP 2022 surprise-family reflex prediction scores.
  - Sci. Rep. 2024 (Panoan-Takanan hypothesis test, elicitation data).
  - LChange 2026.lchange-1.6 (irregular-word detection).
  - SIGTYP 2025 "Beyond cognacy" (phylogenetics).
  - arXiv 2609.05262 (phylogenetics) and arXiv 2512.01713 (borrowing detection), seen only as OpenAlex records; arxiv.org was not contacted.
  - Diachronica 2024 (Gyalrongic).
  - IEEE ICCIES 2025 "Reconstructing Proto-Languages Using NMT and Deep Learning": OpenAlex abstract only, because ieeexplore is stopped. It is about proto-language reconstruction, not ST2022 reflex prediction. This is a small residual risk.
  - Lexibank 2 and "Open Problems in Computational Historical Linguistics" (ORE).
  - No SIGTYP 2024, 2025 or 2026 volume title is about reflex prediction.
- Heuristic bounds (HEURISTIC, not published values), using only systems with three proportions:
  - FeVeT on the official scale: linear interpolation at 0.20 and 0.40 gives 0.7066278115270566. The optimistic bound S(0.20)=S(0.10), S(0.40)=S(0.30) gives 0.7205372852214345.
  - Cognate Transformer table values: 0.70716 interpolated, 0.72062 optimistic.
  - All four are below the claimed 0.7422025452564412.
  - Only FeVeT's own language-averaged numbers with the optimistic rule (0.74552) would exceed it. That is a different metric scale, and the same predictions score lower on the official scorer at every proportion, so it does not move the bar.
- TROPHY_CASE.md (local copy): 0 matches for sigtyp, cognate, reflex, ST2022, mockingbird, Q15, quarry, proto-form or BCFS. No entry for this target.
- V3R1T4S pull-request list: it lives on github.com, which is host-stopped for this session (429 at 2026-10-18T21:48:35Z), so I could not check it. The package's local copies (claim/scout/v3r1t4s_pulls_all.html, captured at 18:07:43Z) show totalCount 420 (123 open, 297 closed). The keyword search page shows openCount 0 and closedCount 0. I could not re-verify these after 18:07Z.
- Not searched (stopped hosts or not honestly reachable): Semantic Scholar, arXiv, dblp, IA Scholar, GitHub search, Google Scholar. OpenAlex indexes arXiv and ACL items, which partly covers these.

## 5. Best published aggregate
No published result on the SIGTYP 2022 surprise families gives scores at all five proportions with a mean over proportions, other than the official results files (KNOWN, by the search above). The best published five-proportion aggregate is Mockingbird-I1's 0.6797616040522236: the mean of its official results-surprise-P.json BCFS totals, left to right, from raw.githubusercontent.com (byte-identical to commit 03094435). No official system and no later paper beats it on this aggregate. Later systems (FeVeT 2025, Cognate Transformer 2023) publish only 0.10, 0.30 and 0.50. At each of those proportions they are below the candidate: FeVeT on the official scorer, Cognate Transformer by its table.

novelty: the claimed A_BCFS 0.7422025452564412 exceeds the bar 0.6797616040522236 by 0.062440941204217615 (left to right; strict, not a tie). It also exceeds every official system's aggregate and every heuristic aggregate of later published systems on the official scale. Scope: novelty only. Training cleanliness and reproduction belong to the other skeptics.

pass: true