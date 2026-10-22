(Saved by the main session from the subagent's returned text at 2026-10-18T22:04:28Z; the B40 CRITERION skeptic subagent (Opus 5.5, model opus, agent a02dac4e7deb1a217) could not write a file named like a report. Text verbatim below.)

# CRITERION skeptic panel: cell B40 (proportion 0.40, mean BCFS), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: CRITERION skeptic (one of three); model claude-opus-5-5
start: 2026-10-18T21:39:54Z (date -u: Sun Oct 18 21:39:54 UTC 2026)
end: 2026-10-18T22:01:59Z (date -u: Sun Oct 18 22:01:59 UTC 2026)
material: the claim package only (claim/), plus kit/RULES.md and TROPHY_CASE.md. Interpreters: SYS (entry venv), SCO (official-scorer venv, used only as an interpreter), PY313. SCRATCH means my scratch folder outside claim/.
network: I made no network requests. I did not touch the stop list and saw no 401/403/405/429/503 or challenge page.
injection_suspected: none. The only instruction-like strings in scout/st2022_repo_page.html are GitHub UI text ("You must be signed in to ...") and README text ("detailed instructions that help in installing the packages").

## Success criterion (verbatim, definition/Q15.json "success_criterion")
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

Claimed: the full criterion for one cell (B40: mean BCFS at 0.40). No partial win (p1-p3) is claimed or needed.

## Checks run (commands run from claim/ unless noted)

C1. Package integrity (PROVED-HERE)
- `shasum -a 256 -c MANIFEST.sha256`: 167 OK, 0 not OK. The package has 168 files; the extra one is MANIFEST.sha256 itself.
- `cmp data/view/surprise/FAM/{training,test}-0.40.tsv official/data-surprise/FAM/...`: 20 of 20 "same".
- data/view_manifest.sha256: every shipped file is OK. The 10 training-0.50 lines are reported "FAILED open or read" because those files are not shipped in the package. That is an absence, not a mismatch.

C2. Freeze record (PROVED-HERE)
- attempts/classifier/FROZEN.md has exactly one ROLE=PRIMARY record ("frozen 2026-10-18T19:14:05Z").
- Code files: config.json OK, system.py OK.
- code_tree recomputed as 4880a9cd6f2bd892ecdc2008277bb78f7fe5435c1cd2415183b12f2ebb993051, equal to the record.
- Result files: 20 OK. results_tree recomputed as 242596c2972e589cb236e3a6095fe406fb0723358b9130c094f1896ad8ed11c0, equal to the record.
- sha256 of FROZEN.md is 1310b14a27896e86804e4cd600ebe9dbab4eb91c2aa260c11c777ce4d5376ae0, equal to the value in rules/selection.md.
- The 20 classifier-PRIMARY val/test hashes listed in selection.md check out against the package files: 20 OK.

C3. Headline recomputed with the official scorer (NUMERICAL)
- Script: my own SCRATCH/myscore.py run under SCO. It imports claim/official/src/sigtypst2022.py (sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a, the same hash as SCO's installed module; lingpy 2.6.9, lingrex 1.2.0). It runs compare_words per family and takes statistics.mean over the 10 families. Output:
  - [ltr] Mockingbird-I1 recomputed total [1.272493550651723, 0.316240240534308, 0.6428278176401176, 0.5723601982335171] official [1.272493550651723, 0.316240240534308, 0.6428278176401176, 0.5723601982335171] family+total exact: True
  - [ltr] candidate total [ED, NED, BCFS, BLEU] [1.0267686117591617, 0.2455448938803044, 0.7136377968288752, 0.6533966833715619]
  - [ltr] candidate BCFS 0.7136377968288752  bar 0.6428278176401176  margin 0.07080997918875753  strictly greater: True
  - [builtin] candidate total [ED, NED, BCFS, BLEU] [1.0267686117591617, 0.24554489388030437, 0.7136377968288752, 0.6533966833715619]
  - [builtin] candidate BCFS 0.7136377968288752  bar 0.6428278176401176  margin 0.07080997918875753  strictly greater: True
- In builtin mode Mockingbird recomputes to 0.6428278176401175, one unit off in the last digit. This is expected: only ltr reproduces the 2022 arithmetic.
- Per-family BCFS (ltr), candidate vs Mockingbird-I1 official. The candidate is higher in 10 of 10 families:

| family | candidate | Mockingbird-I1 | difference |
|---|---|---|---|
| bantubvd | 0.701316 | 0.665550 | +0.035766 |
| beidazihui | 0.844681 | 0.816557 | +0.028124 |
| birchallchapacuran | 0.619945 | 0.499869 | +0.120075 |
| bodtkhobwa | 0.817163 | 0.734568 | +0.082595 |
| bremerberta | 0.689071 | 0.634095 | +0.054976 |
| deepadungpalaung | 0.801258 | 0.667922 | +0.133337 |
| hillburmish | 0.645429 | 0.568901 | +0.076528 |
| kesslersignificance | 0.381064 | 0.312859 | +0.068205 |
| luangthongkumkaren | 0.891111 | 0.834598 | +0.056513 |
| wangbai | 0.745340 | 0.693358 | +0.051982 |

C4. Package scoring tool (REPRODUCE step 2): `STUB_MPL=1 SCO -I tools/score_test_040.py --entries E.json --calib-props 0.40 --json OUT.json`
- "ltr 0.40 Mockingbird-I1 NED 0.316240240534308 official 0.316240240534308 total EXACT families EXACT"
- "BAR B40 Mockingbird-I1 official 0.40 BCFS 0.6428278176401176 PREREG 0.6428278176401176: EQUAL"
- "B40 classifier/PRIMARY | ltr: 0.7136377968288752 bar 0.6428278176401176 margin 0.070809979189 -> MEETS (i); ... | builtin: 0.7136377968288752 bar 0.6428278176401176 margin 0.070809979189 -> MEETS (i); ... | both modes: MEETS (i)"
- Also printed, for the other metrics: NED 0.2455448938803044 and BLEU 0.6533966833715619. Both match the CLAIM.md table, so all three metrics are reported as the criterion requires.

C5. Standalone checker: `PY313 -I checker/check_q15.py . object/predictions-0.40.tsv`
- "1. Mockingbird-I1 mean BCFS recomputed 0.6428278176401176, official 0.6428278176401176: EXACT"
- "3. object mean BCFS 0.7136377968288752 over 14992 items (claimed 0.7136377968288752): EQUAL"
- "margin vs Mockingbird-I1 0.070809979189 (higher is better)"
- "4. rebuilt official-format files equal to the frozen ones: 10 of 10"
- "PASS"

C6. The bar is the best BCFS in the official 0.40 file (official/results/results-surprise-0.40.json, sorted):
- Mockingbird-I1 0.6428278176401176
- CrossLingference-Julia 0.6411350072030729
- Mockingbird-N1-A 0.6294058424159104
- Mockingbird-N1-B 0.6212246948083399
- Baseline-Baseline 0.6000922512660704
- (remaining systems lower)

Values published outside this file (FeVeT, Cognate Transformer: none at 0.40 according to scout.md) are the NOVELTY skeptic's area.

C7. Scorer pin
- scout/st2022_repo_page.html has sha256 fec88fad967728c78c42ddd0b95a19a6bb6be63f7e8c9b4fd6ef77d314cc1012, the value in scout.md. It embeds "currentOid":"03094435cba4293ce0eea383036cab78499ad50d" (2 occurrences).
- I could not compare the scorer file or the results JSON with that commit over the network, because my brief allows no web access.
- What I can show: all 10 Mockingbird-I1 family values and its total are reproduced bit for bit (ltr) from its per-item files. That ties together the package's scorer, gold files and results JSON (NUMERICAL). The commit identity itself is HEURISTIC (it rests on the fetched page).

C8. What the entry reads (code audit of attempts/classifier/frozen/PRIMARY/code/system.py and tools/q15h.py; PROVED-HERE for the code paths)
- Training reads only:
  - the manifest's surprise_train files (data/view/surprise/FAM/training-0.40.tsv);
  - through config "devx", dev_dir/listsamplesize/training-0.10.tsv and dev_dir/mannburmish/training-0.10.tsv. The code comment says "test-0.10 rows ... not used".
- Prediction reads only the model folder and its own partition file (opts.json, model-FAM.pkl, the jobs file, the partition).
- Nothing opens a solutions, cognates, wordlist, systems or results file, and nothing imports a network module.
- How the config.json constants (reranker weights, gate, notation maps) were derived is a record only, not re-derived (HEURISTIC). The entry's REPRODUCE.md says they were fit on inner folds of training-0.50.

C9. Other proportions and validation gold (PROVED-HERE)
- I compared shared/val/0.50 (used for all development, ranking and selection) with test-0.40. In 10 of 10 families:
  - 0 shared cognate sets;
  - every val set is also a training-0.40 set;
  - training-0.40 and test-0.40 share 0 sets;
  - the gold sets equal the test-0.40 sets.
- Val sets / test-0.40 sets per family: bantubvd 194/155, beidazihui 259/207, birchallchapacuran 93/75, bodtkhobwa 457/366, bremerberta 102/82, deepadungpalaung 98/78, hillburmish 233/187, kesslersignificance 106/85, luangthongkumkaren 189/152, wangbai 329/263.
- Content check: "val train rows + val solution cells checked against training-0.40: 3892 mismatches: 0".
- Conclusion: the training-0.50 data and the validation gold carry nothing beyond training-0.40, and no test-0.40 row entered development.

C10. Row isolation. Every masked answer of test-0.40 is visible in a sibling row of the same file, so each row must be predicted without seeing its siblings.
- My check over all 10 families: "partitions: no two rows of one cognate set in any partition: True". Inside a partition the masked column is "?" in every row, so no row's answer is visible to it.
- attempts/classifier/frozen/PRIMARY/audit_test_0.40.txt: 40 "identical" lines, last line "AUDIT PASS". It ran 19:09:54Z to 19:10:15Z, before the freeze.
- rules/sealed_cand_0.40.log:
  - "train ok 155s (sandboxed, strict profile)";
  - 10 family lines "ok ... bytes IDENTICAL". Items: 699/699, 3933/3933, 584/584, 2856/2856, 306/306, 1218/1218, 1405/1405, 311/311, 1178/1178, 2502/2502 (sum 14992). Partitions: 10+19+10+8+4+16+9+5+8+10 = 99;
  - "predict: 99 sealed processes";
  - "SEALED_CHECK 0.40 PASS".
- The sealed check is a record of the main session's run. I did not rerun the sandbox.

C11. My own retrain of the frozen entry (not sandboxed; support only, since reproduction is the REPRODUCE skeptic's job)
- Command: `SYS -I tools/q15h.py run --code attempts/classifier/frozen/PRIMARY/code --mode test --out SCRATCH/frozenrun --props 0.40 --workers 2 --python SYS`
- Output: "train rc=0 240s", 10 families "ok", then cmp with the frozen files: "byte-identical families: 10 of 10" (NUMERICAL).

C12. Development-family rows (CLAIM disclosure 1)
- hillburmish: the dev rows are not used at 0.40.
  - The mapped targets have AchangLongchuan 95, Bola 122, Lashi 42, Maru 108 and Atsi 51 training reflexes. All are at or above max_nref 30, and pool is 0.
  - SCRATCH/devoverlap.py, which calls the entry's own load_train, prints "devx targets (own models): [] | dev rows in pooled model: 0".
  - So the disclosure of mannburmish rows is over-cautious for 0.40.
- kesslersignificance: the dev rows are used.
  - devx targets are English, French and German; there are 238 dev rows in the pooled model; renamed dev words: English 225, French 22, German 228.
  - Masked rows whose gold appears verbatim among those dev words: English 12 of 67, French 2 of 70, German 7 of 66.
  - Of those rows, the candidate predicts exactly: English 0, French 1, German 2.
- Counterfactual retrain with "devx" deleted from config.json and nothing else changed:
  - 9 of 10 families are byte-identical to the frozen predictions; only kesslersignificance differs.
  - Mean (ltr) [ED, NED, BCFS, BLEU] = [1.027342148798019, 0.24781954609551224, 0.7137027542858221, 0.6503439682908917].
  - kesslersignificance BCFS is 0.381713 without dev rows, against 0.381064 in the claimed object.
  - "devx-free BCFS margin over bar 0.6428278176401176: 0.07087493664570443".
  - So the dev rows lowered mean BCFS by about 0.000065. The BCFS win does not depend on them (NUMERICAL).
- Base model: the same code with "devx" deleted, "rr" set to None (no reranker, so no gate) and "pairch" set to 0:
  - 2 of 10 families are byte-identical to the frozen predictions. These are the two families where the gate already skips the reranker (bantubvd, beidazihui). kesslersignificance, the third skipped family, differs only because its dev rows were removed.
  - Mean (ltr) [ED, NED, BCFS, BLEU] = [1.063281210912464, 0.2554709340770361, 0.7058083685111236, 0.638452784976075].
  - BCFS margin over the bar: 0.06298055087100596. (The scoring script's output label was renamed by sed for this run; the numbers are unchanged.)
  - So even without this session's reranker, its gate and the dev rows, the system beats the bar by 0.063 (NUMERICAL).

C13. Null test (PREREG rule 13; rules/null_test.md)
- Package tool rerun: `PY313 -I tools/null_test_metric.py --metric bcfs --gold-dir official/data-surprise --cand-dir attempts/classifier/frozen/PRIMARY/test/0.40 --bar-dir official/systems/mockingbird-i1/surprise --prop 0.40 --out SCRATCH/NULL.json`
  - "real: candidate bcfs 0.7136377968288752, bar 0.6428278176401176, d = 0.07080997918875753"
  - "controls: 400"
  - "best_control: 0.011578929144148375"
  - "real_beats_all_controls: yes"
  - "controls >= real: 0"
  - These are identical to rules/null_test.md.
- My own version (SCRATCH/mynull.py under SCO): it uses the official module's nw_align and bcubed_score, a different seed (777 + c), 400 controls, and per-cognate-set swaps with probability 1/2.
  - "own-path real: candidate 0.7136377968288752 bar 0.6428278176401176 d 0.07080997918875753"
  - "own null: controls 400, max control d 0.010971300251808924, mean control d -0.00033640259167376426, controls >= real 0"
  - (NUMERICAL)
- The tool's code matches rule 13: sets in order of first appearance in the gold file, Random(20261018 + c), draw less than 0.5 swaps, d = candidate side minus bar side, left-to-right sums.

C14. Proportion and metric declared before any result
- Recorded times:
  - PREREG header: "Frozen at 2026-10-18T18:11:37Z";
  - selection.md: "Written ... at 2026-10-18T21:16:09Z ... before any surprise-test gold has been read in this session";
  - null test: run 21:17:52Z to 21:18:14Z;
  - sealed check: 21:35:35Z to 21:38:33Z.
- File modification times in this copy are all the copy time, so they say nothing about order.
- Hash link (PROVED-HERE):
  - selection.md lists "254f8e51a592ea6cf2e59215d7219b1ab47df443308a7bc172f7a1173db2761b  PREREG.md". This package's rules/PREREG.md has sha256 e11527bbd24463047fe6d2df8a09f05235a4bb7cea6c935e4fd7f87f215eb979.
  - I replaced its two header phrases, "cell B40 (proportion 0.40, mean BCFS)" and "THIS FOLDER'S CELL: B40, proportion 0.40, mean BCFS.", with the N40 wording. The result hashes exactly to 254f8e51... (check printed "0 True").
  - So the PREREG body existed byte for byte when selection.md was written, before any gold was read. That body includes the B40 row of the cell table ("mean BCFS at 0.40 (higher is better) | Mockingbird-I1 0.6428278176401176") and rules 10 and 13.
- That the PREREG was frozen at 18:11:37Z, rather than only by 21:16:09Z, rests on the record (HEURISTIC).

C15. Selection (PREREG rule 10)
- Candidate's val-0.50 score, recomputed from its frozen val files and the shared/val gold (SCO, scorer from claim/official/src):
  - "candidate val-0.50 [ED, NED, BCFS, BLEU] (builtin sum): [1.1139670176922158, 0.26631878067630127, 0.8356251509060453, 0.6194739711457914]"
  - "val NED below broker/PRIMARY 0.2692807965192631: True ; equals selection.md 0.26631878067630127: True"
  - (the script's own wording for the first comparison uses a less-than sign)
- selection.md's 32-row table (29 eligible singles plus COMB-6 0.2707859930173011, COMB-8 0.2726853997296398, COMB-10 0.2735025293592694) ranks it first.
- The other rows are records; their files are not in the package.
- Eligibility (rule 8): frozen 19:14:05Z, before 21:50:00Z; 20 result files; AUDIT PASS. All lenses had returned by 21:10:30Z, before selection.
- One candidate carries all six cells; there was no per-metric selection.

## Judgements

1. Letter of the criterion: met.
   - "trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv)": the system reads surprise training-0.40, one development family's training-0.10 file in effect (listsamplesize), and masked test-0.40 rows one partition at a time (C8, C10).
   - Every development choice traces back to training-0.50, which is a content-level subset of training-0.40 and disjoint from test-0.40 (C9).
   - No solutions-*.tsv of any family is read.
   - The development families' files are training-*.tsv files of the same task release. PREREG rule 4 permitted them before any result.
   - "mean score over the 10 surprise families at a declared proportion": the 10 families of the definition, statistics.mean, proportion 0.40 declared in PREREG.md (C14).
   - "strictly beats ... on the SAME metric": BCFS 0.7136377968288752 against 0.6428278176401176 from results-surprise-0.40.json, in both summation modes (C3, C4).
   - "st2022 at a pinned commit": the pinned sigtypst2022.compare_words, calibrated bit for bit on Mockingbird-I1 (C3, C7).

2. Spirit and the CLAIM's disclosures: within the spirit for this cell.
   - Dev rows: the README says development data are for users "to test and design their models". Feeding renamed development rows to kesslersignificance stretches that wording, and those rows contain some of the same words as the gold. But the effect on this metric is nil or slightly negative: without them, mean BCFS is 0.7137027542858221, higher than the claimed object (C12).
   - Nothing of the surprise gold was read. Row isolation is shown by the code, the partition check, the audit and the sealed-check log (C10).
   - Residual that I can only check against records: the lenses could open test-0.40.tsv in their data view (whose sibling rows reveal the answers); rule 6 forbids that, and nothing in the package shows a breach. Prior test exposure in earlier sessions is disclosed in the PREREG.
   - Why this residual does not change my view: the win is 0.07 BCFS, the candidate wins all 10 families, and the base model beats the bar by 0.063 even without this session's reranker, its gate and the dev rows (C12).

3. Selection: PREREG rule 10 was followed as written (C15).
   - The rule ranks singles by their frozen val-0.50 files and combinations by LOFO val files. The candidate is the lowest val NED in that table.
   - The disclosed issue is that the reranker's per-family gate was written after the lens saw ungated val numbers. Rule 6 allows a lens to make every choice on shared/val/0.50, gold included, so this is within the rules.
   - It does matter for which entry was chosen: with the ungated val score of 0.2722 the candidate would have ranked below broker/PRIMARY, classifier/SECONDARY and COMB-6.
   - It cannot inflate the claimed value: val and the inner folds share no cognate set with test-0.40 (C9), and the test value was measured once, on the val-selected object, after selection.md.
   - It is a weakness in the PREREG design (singles may be tuned on val while combinations are scored LOFO), not a breach of rule 10 and not a flaw in this claim.

4. One cell, one metric, one object: yes.
   - The claim is B40 only, mean BCFS at 0.40. The object is the frozen test-0.40 predictions, also packaged as object/predictions-0.40.tsv. The checker shows the two are the same (10 of 10 rebuilt files equal).
   - The same object is claimed in sibling cells on NED and BLEU. The criterion explicitly makes each metric a separate win ("a win on one metric is a win on that metric only").
   - The null test passes (C13). The win is not subsumed by any other claim: proportion 0.40 has not been claimed before, according to the PREREG.

## Notes (do not block the verdict)
- rules/selection.md, rules/frozen_entries.md, rules/ranking_040.md, rules/sealed_cand_0.40.log and attempts/classifier/frozen/PRIMARY/REPRODUCE.md contain absolute paths that include a user name. Kit rule 12 forbids this in anything that leaves the machine. This quarry is private, but those paths should be scrubbed before any publication.
- The CLAIM's disclosure of mannburmish rows for hillburmish does not apply at 0.40: they are inactive there, and the hillburmish output is byte-identical without them (C12).
- My runs created bytecode caches inside claim/ (tools/__pycache__, official/src/__pycache__, the entry's code/__pycache__). I deleted them. Afterwards the package again holds 168 files and MANIFEST.sha256 checks 167 OK, 0 not OK.
- I started three background jobs (PIDs 23755, 55882, 59813). All finished on their own; none is running.

confirmed_scope: At proportion 0.40, the frozen single system classifier/PRIMARY's predictions for the 10 surprise families (attempts/classifier/frozen/PRIMARY/test/0.40/FAM/result-0.40.tsv, the same predictions as object/predictions-0.40.tsv) score mean BCFS 0.7136377968288752 under the pinned ST2022 scorer (compare_words, statistics.mean over the 10 families, both summation modes), strictly higher than Mockingbird-I1's official 0.6428278176401176 from official/results/results-surprise-0.40.json, a win on mean BCFS only.

pass: true