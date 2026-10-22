(Saved by the main session from the subagent's returned text at 2026-10-18T22:04:28Z; the B40 NOVELTY skeptic subagent (Opus 5.5, model opus, agent af2a4a69fd1df816b) could not write a file named like a report. Text verbatim below.)

# NOVELTY skeptic panel: cell B40 (proportion 0.40, mean BCFS), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: NOVELTY skeptic (one of three; fresh context; I saw only the claim package, kit/RULES.md, TROPHY_CASE.md and the web through the shared fetch helper)
start: 2026-10-18T21:39:53Z (date -u)
end: 2026-10-18T21:59:15Z (date -u)

status_source: https://github.com/sigtyp/ST2022 HTTP 200 fetched 2026-10-18T21:41:30Z

## Claim under test
The frozen entry classifier/PRIMARY scores mean BCFS 0.7136377968288752 over the 10 surprise families at proportion 0.40. The bar is Mockingbird-I1's official 0.6428278176401176 (CLAIM.md; official/results/results-surprise-0.40.json).

## 1. Status source (one plain GET through the shared helper, User-Agent naming V3R1T4S, stop lists checked first)
- Helper `check` returned OK. The `get` returned: `200  ad4ef255124c6e6db568ffd1347c63fb6d0a4c91b35812c071bf104f32553863  344669  2026-10-18T21:41:30Z`.
- Page title: "GitHub - sigtyp/ST2022: SIGTYP 2022 Shared Task · GitHub". The embedded `"currentOid":"03094435cba4293ce0eea383036cab78499ad50d"` (2 occurrences) and `"commitCount":"142"` are both unchanged from scout/st2022_repo_page.html, which shows the same oid and count. After masking hashes, the token-level diff against the scout copy shows only per-request session tokens. KNOWN.
- The README rank table on the page still ranks Mockingbird-I1 first on BCFS at proportion 4 (0.40). Its row reads "Mockingbird-I1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 ...".
- I fetched the official results file once at the pinned commit: https://raw.githubusercontent.com/sigtyp/ST2022/03094435cba4293ce0eea383036cab78499ad50d/results/results-surprise-0.40.json returned `200 699aacbc94cb6d8289bb2685ac73f87e2cf72a1df22cee89a6cf8b7e1501ee86 14371 2026-10-18T21:41:51Z`. `cmp` against official/results/results-surprise-0.40.json printed IDENTICAL (same sha256). The official results are unchanged. KNOWN.
- Ranking of every official system at 0.40 by total BCFS, from my own parse of that file; recomputed means equal the totals:
  - Mockingbird-I1 0.6428278176401176
  - CrossLingference-Julia 0.6411350072030729
  - Mockingbird-N1-A 0.6294058424159104
  - Mockingbird-N1-B 0.6212246948083399
  - Baseline-Baseline 0.6000922512660704
  - Mockingbird-N1-C 0.5999320583412607
  - Baseline-Baseline-SVM 0.5990447973691144
  - CEoT-Extalign-RF 0.5804515960120803
  - Leipzig-Transformer 0.47362199458683174
  - Mockingbird-N2 0
  
  NUMERICAL.

## 2. Claimed value (sanity check only; the REPRODUCE skeptic owns reproduction)
`python3 checker/check_q15.py . object/predictions-0.40.tsv` (standard library, run with -I) printed:
- "1. Mockingbird-I1 mean BCFS recomputed 0.6428278176401176, official 0.6428278176401176: EXACT"
- "3. object mean BCFS 0.7136377968288752 over 14992 items (claimed 0.7136377968288752): EQUAL"
- "margin vs Mockingbird-I1 0.070809979189 (higher is better)"
- "4. rebuilt official-format files equal to the frozen ones: 10 of 10"
- "PASS"

Margin computed separately: 0.07080997918875753. NUMERICAL.

## 3. Known prior systems that might report 0.40 (each source opened)
- **FeVeT** (Wientzek 2025, Open Research Europe 5:174, DOI 10.12688/openreseurope.20647.1):
  - Repo page https://github.com/TGH-2020/FeVeT returned 200 at 2026-10-18T21:41:52Z. Embedded oid 31898c53bfffeef87265efa8a780b7be740162d1 and commitCount 29, the same HEAD as recorded in scout/scout.md.
  - results/ tree (200, 21:42:06Z) holds s2s_reflex_{0.10,0.30,0.50}_* files only.
  - results/predictions/reflex/bantubvd (200, 21:42:31Z) holds s2s_reflex_0.10, 0.30 and 0.50 predictions only.
  - results/s2s_reflex_finetuned_avg.txt (200, 21:42:13Z) gives BCFS 0.10: 0.8041, 0.30: 0.7232, 0.50: 0.673.
  - s2s_reflex_avg.txt (no fine-tuning) gives 0.10: 0.7704, 0.30: 0.6874, 0.50: 0.6426.
  - Article JATS XML https://open-research-europe.ec.europa.eu/articles/5-174/v1/xml (200, 21:45:58Z) says: "the model is evaluated on the 10%, 30%, and 50% test proportions of the surprise data". Its Table 3 matches the repo numbers.
  - No version 2 exists: Europe PMC lists version 1 only, and OpenAlex count is 0 for DOIs .20647.2 and .20647.3.
  - Verdict: FeVeT has no value at 0.40. KNOWN.
- **Cognate Transformer** (Akavarapu and Bhattacharya, EMNLP 2023, 2023.emnlp-main.423):
  - PDF https://aclanthology.org/2023.emnlp-main.423.pdf returned 200 at 21:43:47Z.
  - Section 4.1: "Surprise data was divided into different test proportions of 0.1, 0.2, 0.3, 0.4, and 0.5 for evaluation. Among these, we only report for the test proportions 0.1, 0.3, and 0.5."
  - Table 5, CogTran-small BCFS: 0.1: 0.7823, 0.3: 0.6954, 0.5: 0.6477. Appendix A is per family at 0.1, 0.3 and 0.5 only.
  - Repo README (github.com/mahesh-ak/CognateTransformer, 200, 21:44:11Z) has no results table.
  - Correction to the brief and to scout/scout.md: Cognate Transformer reports 0.1, 0.3 and 0.5, not "0.50 only". Either way it has no value at 0.40, so CLAIM.md's statement ("published no 0.40 value") stands. KNOWN.
- **Neither published a value at 0.40, so neither moves the bar.** As a HEURISTIC only (these are not published values), linear interpolation between 0.30 and 0.50 gives:
  - FeVeT fine-tuned: 0.6981
  - CogTran-small: 0.67155
  
  Both are below the claimed 0.7136377968288752.

## 4. Literature search (last 24 months and earlier; one GET per resource; no retries)
- **ACL Anthology**:
  - Full bibliography with abstracts (anthology+abstracts.bib.gz, 200, 42574037 bytes, 21:46:27Z). It has 131708 entries, 10822 of them from 2026 (through ACL 2026).
  - Grep for reflex prediction, cognate reflex, SIGTYP 2022, ST2022 and protoform terms returned only the 2022 shared-task papers, Cognate Transformer (2023), Jambu, Helpful Neighbors and Lu et al. 2024 (protoform reconstruction on other data).
  - A broad 2024–2026 pass (92 entries mentioning cognate, reflex or proto-language) found no paper reporting SIGTYP 2022 surprise scores.
  - Volume pages read: SIGTYP 2023, 2024, 2025 and 2026 (2026.sigtyp-main); LChange 2023, 2024 and 2026.
  - Candidate PDFs read: 2026.lchange-1.6 (Blum and List; correspondence-pattern regularity), 2025.sigtyp-1.6 (Jäger; phylogenetics) and 2023.sigtyp-1.6 (Blum and List; trimming, development families). None reports reflex-prediction scores on the surprise families.
- **OpenAlex** (used only after the earlier 429 stop on that host had passed the 24-hour window, at 21:55:57Z):
  - ST2022 task paper W4287889593 has 15 citing works. Those within 24 months are FeVeT (2025-06-30) and Sci Rep 2024 (Panoan–Takanan).
  - Mockingbird paper W4287888114: 10 citing works, nothing newer than FeVeT.
  - Cognate Transformer W4389520718: 3 citing works (FeVeT; a 2026 bioRxiv paper on ancestral protein sequences; ICCIES 2025 "Reconstructing Proto-Languages Using NMT and Deep Learning").
  - FeVeT: 0 citing works.
  - Zenodo ST2022 dataset W4393634321: 0 citing works.
  - Searches from 2024-10-01 for "reflex prediction" (21 results), "cognate reflexes" (9) and "SIGTYP 2022" (2): no value at 0.40 on the surprise families.
- **Europe PMC** search (7 hits):
  - Sci Rep 2024 (PMC11668889). I read the full text: a pre-registered reflex-prediction test of the Panoan–Takanan hypothesis, with no SIGTYP 2022 surprise evaluation.
  - FeVeT ORE record, version 1 only.
- **Zenodo API** (4 queries):
  - The first attempt returned 400, a size-limit validation error, not a block. I re-queried with size=25.
  - Nothing new: the ST2022 dataset, a CEoT submission, FeVeT supplementary material, and unrelated Latin-to-Romance resources.
- **Hugging Face papers search** (2 queries): no SIGTYP 2022 reflex-prediction result.
- **Archives for Technical Sciences 2026** (PIE reconstruction; OpenAlex full-text match for "SIGTYP 2022"): the PDF (200, 21:58:36Z) only cites Mockingbird. It reports no ST2022 scores.
- **Residual gap (disclosed)**:
  - The full text of ICCIES 2025 (IEEE 11032538) is on ieeexplore.ieee.org, which is stop-listed (challenge). I saw only its OpenAlex abstract, which describes NMT proto-language reconstruction, not SIGTYP 2022 reflex prediction at 0.40. HEURISTIC: unlikely to hold a 0.40 surprise value.
  - arxiv.org is host-stopped (429, other lane, 2026-10-17T22:56:05Z). I did not query it, nor export.arxiv.org, so as not to work around that stop. arXiv is covered indirectly through OpenAlex and Hugging Face. api.semanticscholar.org, dblp.org and scholar.archive.org are stopped and were not used. Google Scholar was not used.

## 5. Crowd and own records
- TROPHY_CASE.md: grep for sigtyp, st2022, cognate, reflex, BCFS and mockingbird found nothing (exit 1). No row for this target.
- V3R1T4S pull requests (github.com HTML; embedded counts):
  - is:pr cognate / sigtyp / reflex / ST2022 / Mockingbird / BCFS each returned "openCount":0 and "closedCount":0 (fetched 21:43:08Z to 21:43:12Z).
  - All PRs: "totalCount":457 ("openCount":160, "closedCount":297), newest number 467. The 24 newest titles are all other targets.

## 6. Blocks during this check (kit rule 5)
- 2026-10-18T21:48:35Z: https://github.com/search?q=sigtyp+2022&type=repositories&s=updated&o=desc returned 429 ("Too many requests · GitHub"). The helper appended this line to the session stop list:
  `2026-10-18T21:48:35Z	429	github.com	https://github.com/search?q=sigtyp+2022&type=repositories&s=updated&o=desc	B40-NOVELTY`
- That is a host-level stop for github.com. The three queued GitHub search URLs were refused by the helper and never requested. No GitHub request followed, and nothing was retried.
- All other requests returned 200, except the single Zenodo 400 (validation) noted above.
- injection_suspected: api.openalex.org JSON meta.notice (21:57:32Z). It tells AI agents to POST their user's email address to an OpenAlex key endpoint. I ignored it, sent no email, and acted on nothing it said.

## 7. Side notes for the main session (outside this lens's pass criterion)
- scout/scout.md says Cognate Transformer "reports 0.50 only". It actually reports 0.1, 0.3 and 0.5 (Table 5). This does not change the bar at 0.40.
- Several package markdown files contain absolute home-directory paths: scout/scout.md, rules/PREREG.md, rules/selection.md, rules/frozen_entries.md, rules/ranking_040.md and attempts/classifier/frozen/PRIMARY/REPRODUCE.md. Kit rule 12 needs them scrubbed before anything leaves the machine.

## Verdict
- best published value at 0.40 on mean BCFS: 0.6428278176401176, Mockingbird-I1 (official results/results-surprise-0.40.json at ST2022 commit 03094435cba4293ce0eea383036cab78499ad50d, unchanged and byte-identical upstream). No later publication I could reach (FeVeT, Cognate Transformer, ACL Anthology through 2026, OpenAlex, Europe PMC, Zenodo, Hugging Face) reports a 0.40 value, so the bar is not moved.
- novelty: the claimed 0.7136377968288752 strictly beats every known value at proportion 0.40 on mean BCFS, by 0.07080997918875753 over Mockingbird-I1. It is not a tie.
- Scope: one cell only (proportion 0.40, mean BCFS, 10 surprise families, official family-averaged scale). Residual unread full text: ICCIES 2025 (stop-listed host; its abstract is off-task).

pass: true