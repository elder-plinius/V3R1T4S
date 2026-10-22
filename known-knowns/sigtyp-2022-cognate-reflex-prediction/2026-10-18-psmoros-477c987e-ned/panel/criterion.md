(Saved by the main session from the subagent's returned text at 2026-10-18T22:04:28Z; the N40 CRITERION skeptic subagent (Opus 5.5, model opus, agent a9409e790dcdc139a) could not write a file named like a report. Text verbatim below.)

# CRITERION panel, cell N40 (proportion 0.40, mean NED), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: CRITERION skeptic (one of three skeptics), cell N40, target private-quarry-B (definition/Q15.json)
start: 2026-10-18T21:39:54Z (date -u: "Sun Oct 18 21:39:54 UTC 2026")
end: 2026-10-18T21:55:05Z (date -u: "Sun Oct 18 21:55:05 UTC 2026")
material: claim/ only (CLAIM.md, REPRODUCE.md, definition/, rules/, attempts/, object/, official/, data/, shared/, tools/, checker/); kit RULES.md and TROPHY_CASE.md (TROPHY_CASE has no entry for this target). No other workspace file was opened. No web access and no network request of any kind, so nothing was added to the stop list. Scratch work was done in a skeptic folder outside claim/. Interpreters: SCO (the interpreter with the official scorer installed), SYS (the ML venv the entry runs with) and the system python3.13.
injection_suspected: none seen (the scout HTML pages were not opened).

## Criterion (verbatim, definition/Q15.json "success_criterion")
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

Claimed: the full criterion, on mean NED at the declared proportion 0.40 only. No partial win is claimed. If the full win holds, it covers p2 and p3, so they are not needed.

## Checks run (numbers copied from command output)

### 1. Package and freeze integrity
- `shasum -a 256 -c MANIFEST.sha256` (run in claim/): 167 of 167 lines OK, no other lines; claim/ holds 167 files besides the manifest.
- attempts/classifier/FROZEN.md, record "frozen 2026-10-18T19:14:05Z ROLE=PRIMARY". All 20 listed result files (val/0.50 and test/0.40) check OK against the record; code/config.json OK; code/system.py OK. FROZEN.md holds only one PRIMARY record. It was frozen before the PREREG rule 8 deadline of 21:50:00Z.

### 2. Headline recomputed with the official scorer
- My own script, run under SCO: the official compare_words per family, statistics.mean over the 10 families, both summation modes. The installed module and claim/official/src/sigtypst2022.py have the same sha256, 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a.
- Mockingbird-I1, recomputed from official/systems/mockingbird-i1, left-to-right totals [ED, NED, BCFS, BLEU]: 1.272493550651723, 0.316240240534308, 0.6428278176401176, 0.5723601982335171.
  - These equal the official results-surprise-0.40.json total ("MB total ltr == official: True").
  - All 10 family values also match: "per-family mismatches (ltr): []".
- classifier/PRIMARY (attempts/classifier/frozen/PRIMARY/test/0.40), left-to-right totals [ED, NED, BCFS, BLEU]: 1.0267686117591617, 0.2455448938803044, 0.7136377968288752, 0.6533966833715619.
  - With the builtin sum, NED is 0.24554489388030437.
- NED margin against the bar 0.316240240534308:
  - left-to-right: 0.0706953466540036
  - builtin: 0.07069534665400362
  - Both are far above the PREREG margin of 1e-9.
- Per-family NED, left to right (candidate / Mockingbird-I1). The candidate is lower in 10 of 10 families:

| family | candidate | Mockingbird-I1 |
|---|---|---|
| bantubvd | 0.279163 | 0.300696 |
| beidazihui | 0.107763 | 0.124066 |
| birchallchapacuran | 0.283923 | 0.401267 |
| bodtkhobwa | 0.132007 | 0.195122 |
| bremerberta | 0.246042 | 0.285156 |
| deepadungpalaung | 0.203517 | 0.395699 |
| hillburmish | 0.293042 | 0.366953 |
| kesslersignificance | 0.622523 | 0.729591 |
| luangthongkumkaren | 0.086439 | 0.121226 |
| wangbai | 0.201030 | 0.242626 |

- The official 0.40 JSON gives these NED totals: Mockingbird-I1 0.316240240534308, Mockingbird-N1-B 0.33494782949582314, Mockingbird-N1-A 0.3521333077310183. Mockingbird-N2 is [0, 0, 0, 0], the scorer's placeholder for a missing file. The criterion names Mockingbird-I1, whose value is the bar.
- All three metrics are reported in CLAIM.md, and they equal my recomputation. Only NED is claimed here.

### 3. Standalone checker
`python3 checker/check_q15.py . object/predictions-0.40.tsv` printed:
- "1. Mockingbird-I1 mean NED recomputed 0.316240240534308, official 0.316240240534308: EXACT"
- "3. object mean NED 0.2455448938803044 over 14992 items (claimed 0.2455448938803044): EQUAL"
- "margin vs Mockingbird-I1 0.070695346654 (lower is better)"
- "4. rebuilt official-format files equal to the frozen ones: 10 of 10"
- "PASS" (rc=0)

### 4. Declared proportion and timing
- rules/PREREG.md header: "Frozen at 2026-10-18T18:11:37Z". It fixes cell N40 (mean NED at 0.40, lower is better), the bar (Mockingbird-I1 0.316240240534308), the selection rule (rule 10), the claim rule (rule 12) and the null design (rule 13).
- `shasum -a 256 rules/PREREG.md` gives 254f8e51a592ea6cf2e59215d7219b1ab47df443308a7bc172f7a1173db2761b. This equals the PREREG.md hash recorded in rules/selection.md. The PREREG therefore did not change between its freeze and the selection.
- Order of events, as recorded:
  - PREREG: 18:11:37Z
  - candidate frozen: 19:14:05Z
  - selection.md: 21:16:09Z
  - null test: 21:17:52Z to 21:18:14Z
  - sealed check: 21:35:35Z to 21:38:33Z
- So the proportion, metric and bar were declared before any result of this session.
- Limitation: all of these times are self-reported in the package. The file mtimes are copy times, so they cannot confirm when anything was written.

### 5. Selection (PREREG rule 10 as written)
- rules/selection.md records date -u and sha256 hashes of every freeze record and of the val-0.50 and test-0.40 result files. Rule 10 asks for both.
- Its table puts classifier/PRIMARY first: val NED 0.26631878067630127. Next come broker/PRIMARY 0.2692807965192631, classifier/SECONDARY 0.2702343133887876 and COMB-6 0.2707859930173011. COMB-8 is 0.2726853997296398 and COMB-10 is 0.2735025293592694. There are no ties.
- I rescored the candidate's frozen val-0.50 files against shared/val/0.50 under SCO:
  - builtin mode: mean ED 1.1139670176922158, mean NED 0.26631878067630127
  - left-to-right: the same values
  - Both equal the table. The other entries' val files are not in the package, so their numbers could not be recomputed.
- Conclusion: the rule was followed as written. It picks the lowest val-0.50 mean NED among single entries (their frozen val files) and COMB-6/8/10 (their LOFO val files), and the candidate is that entry.
- The disclosed issue: the per-family reranker gate (rr skip: bantubvd, beidazihui, kesslersignificance) was written after the lens had seen ungated per-family val numbers (ungated val 0.2722).
  - That is a development choice made on shared/val/0.50, which PREREG rule 6 explicitly allows.
  - It can make the candidate's val number optimistic compared with the LOFO-scored combinations, so it can change which entry is selected.
  - It cannot bias the selected entry's test score, because no test information entered the choice.
  - I judge it within both the letter and the spirit of rule 10 and of the criterion.

### 6. What the entry reads, and row isolation
- Harness (tools/q15h.py run): the training manifest lists only data/view/surprise/FAM/training-0.40.tsv and dev_dir data/view/dev. Prediction is split into partitions by masked language, with the assertion "two rows of one cognate set in a partition" never triggered.
- Code audit of code/system.py:
  - At train time it opens only config.json, the manifest, the manifest's training files, the model folder, and dev_dir/mannburmish/training-0.10.tsv and dev_dir/listsamplesize/training-0.10.tsv. A code comment says the dev test-0.10 files are not used.
  - At predict time it opens only the model and the partition files named in the jobs file. Each row is predicted with predict_row(m, row, langs).
  - The code does no network or subprocess calls, and reads no solutions, cognates or wordlist file.
- Data checks with python3.13:
  - For each of the 10 families, the training-0.40 cognate sets and the test-0.40 cognate sets overlap in 0 sets.
  - shared/val/0.50 sets are a subset of the training-0.40 sets: "not-in-train40 0" in every family, and 0 overlap with test sets.
  - "val-0.50 cells/rows checked against training-0.40: 24170 mismatches: 0". All of the development data is therefore inside training-0.40, and nothing from another proportion or from any gold was used.
  - data/view training-0.40 and test-0.40 are byte-identical to official/data-surprise ([True, True] for all 10 families).
- Why isolation is essential: "gold items 14992 answer visible verbatim in a sibling test row: 14992". Every answer of test-0.40 is visible in a sibling row of the same file.
- attempts/classifier/frozen/PRIMARY/audit_test_0.40.txt: 40 lines "identical" (3 single rows and 1 whole partition per family), ending "AUDIT PASS".
- rules/sealed_cand_0.40.log:
  - "train ok 155s (sandboxed, strict profile)"
  - 10 of 10 families "ok ... bytes IDENTICAL"
  - "predict: 99 sealed processes"
  - "SEALED_CHECK 0.40 PASS"
- My own independent sealed rerun (macOS sandbox-exec):
  - Network was denied. File reads were denied under both workspace folders except: the SYS venv; a copy of the frozen code (config.json 225856a4…, system.py 8482ef52…, equal to the freeze record); a view holding only the 10 surprise training-0.40.tsv files and the 10 development families' training-0.10.tsv files; and the model folder.
  - A probe inside this sandbox gave: "DENIED claim/official/data-surprise/bremerberta/solutions-0.40.tsv PermissionError", "DENIED claim/data/view/surprise/bremerberta/test-0.40.tsv PermissionError", "READABLE sbx/view/surprise/bremerberta/training-0.40.tsv".
  - Training: SYS code/system.py train, rc=0, 21:45:05Z to 21:49:26Z.
  - Prediction: each partition was predicted alone in its own process, in a sandbox that could read only the code, the model and that one partition.
  - Result: 10 of 10 families "items identical N/N bytes IDENTICAL" (bantubvd 699/699 … wangbai 2502/2502), "sealed predict processes 99, 168s", "SKEPTIC_SEALED 0.40 PASS".
  - The rebuilt result files have the frozen sha256 values (cbf74c9d…, 096c896e…, d82e290e…, 804f2df8…, 7122207b…, df842a55…, ea8df80b…, b9877195…, 71c83295…, b3c23443…).

### 7. Development-family rows (CLAIM.md disclosure)
- The entry adds listsamplesize English/German/French rows to kesslersignificance, and mannburmish rows (max_nref 30) to hillburmish.
- These are development families' training-*.tsv files from the task release. PREREG rules 4 and 6 allow them, and the criterion forbids only solutions-*.tsv. I judge them within the letter.
- Spirit, a sensitivity check of my own (information only):
  - I retrained under the same sandbox with CLS_OPTS {"devx": null} for hillburmish and kesslersignificance, then predicted their partitions sealed.
  - hillburmish: 1405/1405 bytes IDENTICAL, so the dev rows have no effect at 0.40.
  - kesslersignificance: 92/311 items identical.
  - Official scorer, left-to-right: "kesslersignificance NED 0.645269364983149 … mean NED over 10 families 0.24781954609551224; margin vs bar 0.316240240534308: 0.06842069443879575".
  - Builtin sum: mean 0.2478195460955122, margin 0.06842069443879578.
  - The win does not depend on the development rows; they lower the mean by about 0.0023.
- Overlap of the dev rows with the gold: after the entry's notation maps, gold forms appear verbatim among the dev forms in 12/67 English, 7/66 German and 2/70 French items. Exact predictions with and without the dev rows are 6 vs 5, 7 vs 5 and 3 vs 0. This is not a channel for copying the gold.

### 8. Null test (rules/null_test.md, PREREG rule 13)
- Tool rerun: `STUB_MPL=1 SCO -I tools/null_test.py --prop 0.40 --bar mockingbird --cand-dir attempts/classifier/frozen/PRIMARY/test/0.40 --out NULL.json`, rc=0. It printed:
  - "real: candidate NED 0.2455448938803044, bar NED 0.316240240534308, d = 0.0706953466540036"
  - "fast path bit-identical in every check: yes"
  - "controls: 400", "best_control: 0.011794897907416113", "real: 0.0706953466540036", "real_beats_all_controls: yes"
  - "control mean 0.00017006352720008415 sd 0.0044075171254668415"
  - zero controls at or above real (the tool prints this with a greater-or-equal sign, spelled out here)
  - This is identical to null_test.md.
- My independent implementation: per-item NED through the official nw_align, swaps per cognate set, the scorer's aggregation with left-to-right sums.
  - It gives "real: cand NED 0.2455448938803044 MB NED 0.316240240534308 d 0.0706953466540036".
  - With the PREREG seeds 20261018+c over 400 controls: max d_c 0.011794897907416113, min -0.011577518782049712, zero controls at or above real.
  - With 1600 extra controls (seeds 900000+c): max d_c 0.015275216690531446, zero at or above real.
  - "sd of control d over all 2000 controls 0.004583; real d / sd = 15.4". The null test passes.

### 9. One cell, one metric, one object
- CLAIM.md claims only mean NED at 0.40.
- The object is attempts/classifier/frozen/PRIMARY/test/0.40/FAM/result-0.40.tsv. object/predictions-0.40.tsv holds the same predictions (the checker rebuilds 10 of 10 frozen files from it).
- The same object being claimed in the sibling cells B40 and L40 is consistent with the criterion: "a win on one metric is a win on that metric only". This folder does not reach beyond NED at 0.40, and it is not subsumed. The PREREG and scout record no earlier claim at 0.40; the run 2026-10-17-1806 combiner's single 0.40 score is disclosed as information only and is a different object.

## Judgement
- The result meets the full criterion literally on mean NED at the declared proportion 0.40:
  - training used only training-0.40.tsv plus development training-*.tsv files;
  - the masked test-0.40.tsv was read only partition by partition, which my own sandboxed run confirms byte for byte;
  - no solutions file, no gold and no other proportion was used;
  - the mean over the 10 surprise families, 0.2455448938803044 (builtin 0.24554489388030437), is strictly below Mockingbird-I1's official 0.316240240534308 in both summation modes;
  - the scorer reproduces the official Mockingbird-I1 family values and total bit for bit.
- The selection followed PREREG rule 10 as written. The disclosed gate and dev-row issues are within the letter and spirit, and neither one decides the win.
- Residual limits (not grounds to fail):
  - the time order rests on timestamps inside the package;
  - the claim that the carried classifier code was developed cleanly, under val-0.50-only rules in runs 0104/0202/0839, rests on the PREREG's statements;
  - the scorer's pinned commit (03094435) was not fetched; it is supported by the bit-exact calibration;
  - earlier sessions' exposure to the nested test gold is disclosed and does not enter the mechanical rule.

confirmed_scope: At proportion 0.40, the frozen single system classifier/PRIMARY, whose predictions are attempts/classifier/frozen/PRIMARY/test/0.40/FAM/result-0.40.tsv (the same predictions as object/predictions-0.40.tsv), has mean NED 0.2455448938803044 over the 10 surprise families under the pinned ST2022 scorer (left-to-right summation; 0.24554489388030437 with the builtin sum), strictly lower than Mockingbird-I1's official 0.316240240534308 from results-surprise-0.40.json, a win on mean NED at 0.40 only.

pass: true