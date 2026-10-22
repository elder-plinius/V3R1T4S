(Saved by the main session at 2026-10-18T12:37:59Z from the criterion skeptic subagent's returned text (cell N50; Opus 5.5, agent a0eaa0fa6ffcb3582); the subagent could not write a file named like a report. Text verbatim below.)

# CRITERION skeptic, cell N50 (proportion 0.50, mean NED), run 2026-10-18-0839

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: CRITERION (one of three skeptics)
start: 2026-10-18T11:44:25Z (date -u)
end: 2026-10-18T12:21:13Z (date -u)
material: only claim/ (every path below is relative to claim/), plus the kit rules and the trophy case (the trophy case has no Q15 entry). I made no network requests, so there was nothing to check against or add to the stop list. All my scratch files were outside claim/.
interpreters: SYS = the entries' ML venv (Python 3.13, lingpy 2.6.13); SCO = the pinned-scorer venv, used only as an interpreter; PY3 = stock Python 3.13.

## The criterion (definition/Q15.json "success_criterion", verbatim)
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

## Verdict
The full criterion is met on mean NED at the declared proportion 0.50. This is not a partial win. The cell's stricter bar (FeVeT rescored) is also beaten. Details below.

## Checks run (real output)

C1. Package integrity (PROVED-HERE)
- `shasum -a 256 -c MANIFEST.sha256`: 379 of 379 OK. There are 379 files besides the manifest.
- `data/view_manifest.sha256`: 40 of 42 OK. The two failures are data/view/datasets.json and data/view/datasets-surprise.json. Both are listed but not shipped. They are metadata, not files any system reads.
- fevet/expected.sha256: the 10 shipped pred_0.50 files are OK. The 20 listed 0.10 and 0.30 files are not shipped.

C2. The claimed object is the selected candidate (PROVED-HERE)
- The sha256 of each of the 10 files combiner/test/0.50/FAM/result-0.50.tsv equals the COMB-8 test hash recorded in rules/selection.md: 10 MATCH (for example, bantubvd 0463946121fe8515d80370660c7f353ee1d810cd8cab24b00ff931ce5408b2a1).

C3. Headline recomputed with the package's scoring tool (PROVED-HERE)
Command: `STUB_MPL=1 SCO -I tools/score_test_050.py --entries E.json --json OUT.json --calib-props 0.50 --fevet-props 0.50 --candidate candidate`, with E.json = [{"name": "candidate", "dir": "combiner"}].
Output:
- ltr 0.50 Mockingbird-I1 NED 0.35176136367373956 official 0.35176136367373956 total EXACT families EXACT
- ltr 0.50 FeVeT NED 0.30880111347517586 BCFS 0.6423935720824072 BLEU 0.5768215755932388 (checks: missing 0, gold mismatches 0)
- ltr 0.50 candidate ED 1.016662 NED 0.24912258145405175 BCFS 0.7114179305724276 BLEU 0.6520222200978466
- builtin 0.50 candidate ED 1.016662 NED 0.24912258145405175 BCFS 0.7114179305724276 BLEU 0.6520222200978465
- N50, ltr: NED 0.24912258145405175, bar 0.30880111347517586, margin 0.059678532021, MEETS (i); margin vs Mockingbird-I1 0.102638782220.
- N50, builtin: the same values and margins. Both modes: MEETS (i).
- The recomputed FeVeT bar equals the PREREG table value (the tool printed EQUAL).
- In builtin (compensated) mode, the tool prints "total DIFF families DIFF" for Mockingbird-I1 against the official vector. Left-to-right summation is the mode that is bit-exact with the 2022 results.

C4. Independent scoring with my own script (PROVED-HERE)
I ran it under the SCO interpreter. It loads official/src/sigtypst2022.py by file path, not the installed module, and uses left-to-right summation in both that module and lingrex.util.
- sha256 of the installed module: 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a. sha256 of the package source file: the same value.
- Mockingbird-I1 recomputed total [1.4169823165005235, 0.35176136367373956, 0.6050308536957327, 0.5337187296541888]. This equals the official total (EXACT), and all 10 family values are exact (True).
- Object total [ED, NED, BCFS, BLEU]: [1.0166617451971307, 0.24912258145405175, 0.7114179305724276, 0.6520222200978466].
- FeVeT: 18101 rows, 0 missing, 0 gold mismatches, mean NED 0.30880111347517586.
- Margins of the object's NED: 0.05967853202112411 below FeVeT; 0.10263878221968781 below Mockingbird-I1 official.
- Mean NED per family (object / FeVeT / Mockingbird-I1). The object is lower than both in all 10 families.

| family | object | FeVeT | Mockingbird-I1 |
|---|---|---|---|
| bantubvd | 0.259321 | 0.273821 | 0.360396 |
| beidazihui | 0.103719 | 0.140544 | 0.133499 |
| birchallchapacuran | 0.294073 | 0.389835 | 0.467463 |
| bodtkhobwa | 0.137543 | 0.180329 | 0.219477 |
| bremerberta | 0.253110 | 0.330954 | 0.297502 |
| deepadungpalaung | 0.214348 | 0.319540 | 0.444929 |
| hillburmish | 0.318954 | 0.371269 | 0.441929 |
| kesslersignificance | 0.595464 | 0.672590 | 0.726768 |
| luangthongkumkaren | 0.099618 | 0.156456 | 0.146555 |
| wangbai | 0.215076 | 0.252673 | 0.279095 |

- Other entries in official/results/results-surprise-0.50.json: Mockingbird-N2 is all zeros (no submission). The lowest real NED there is Mockingbird-I1's 0.351761.

C5. Standalone checker (PROVED-HERE)
Command: `PY3 -I checker/check_q15.py . object/predictions-0.50.tsv`. Output:
- 1. Mockingbird-I1 mean NED recomputed 0.35176136367373956, official 0.35176136367373956: EXACT
- 2. FeVeT published predictions mean NED 0.30880111347517586
- 3. object mean NED 0.24912258145405175 over 18101 items (claimed 0.24912258145405175): EQUAL; margin vs Mockingbird-I1 0.102638782220; margin vs FeVeT 0.059678532021
- 4. rebuilt official-format files equal to the frozen ones: 10 of 10
- PASS

C6. Pinned scorer and status source (KNOWN, from the recorded status files)
- scout/st2022_commits.json: newest commit 03094435cba4293ce0eea383036cab78499ad50d, 2022-05-27T07:58:23Z, "update for final release". This is the PREREG pin.
- scout/fevet_commits.json: newest commit 31898c53bfffeef87265efa8a780b7be740162d1, 2025-11-28T17:00:16Z.
- I could not re-fetch these (no web in this role). The pin rests on the recorded status source, backed by the bit-exact reproduction of Mockingbird-I1's official values in C3 and C4.

C7. The data the systems were given (PROVED-HERE)
- data/view contains:
  - training-0.50 and test-0.50 of the 10 surprise families (20 files, all byte-identical to official/data-surprise);
  - training-0.10 and test-0.10 of the 10 development families.
- It contains no solutions, cognates or wordlist file, and no other proportion of any surprise family.

C8. Row isolation: why it matters, and the package's own evidence
- My script: for all 18101 of the 18101 masked items in test-0.50, the gold reflex is visible verbatim in a sibling row of the same cognate set. So row isolation decides whether a result is honest (PROVED-HERE).
- Test-mode audits (attempts/LENS/frozen/ROLE/audit_test_0.50.txt): all 8 entries show "40 identical, 0 FAIL; AUDIT PASS".
- rules/sealed_new_0.50.log: 100 lines of "bytes IDENTICAL" (10 components x 10 families), then "SEALED_CHECK 0.50 PASS", done 2026-10-18T11:42:47Z.
- rules/sealed_carry_0.50.log: 11 components x 10 families IDENTICAL, then PASS, done 09:20:18Z.
- Together the two logs cover all 8 COMB-8 entries.
- The sandbox profile in tools/sealed_check.py works as follows:
  - Training can read only its own copy of training-0.50 and of the development view, plus the interpreter's venv.
  - Each partition is predicted in its own sandboxed process. That process can read only the code, the model and its own partition.

C9. My own retrain with sibling rows removed (PROVED-HERE for these rows)
- I made a scratch copy of tools/, data/ and the 8 entries' code/ folders.
- I replaced each family's test-0.50.tsv with one random row per cognate set (random.Random(4242)), keeping 2064 rows. After this, no masked answer appears anywhere in any test file, and the copy holds no solutions file.
- Each of the 8 entries was retrained from its frozen code (`SYS -I tools/q15h.py run --code ... --mode test --props 0.50 --workers 1`, HOME inside my scratch). All 10 families reported "ok" for every entry.
- Row-by-row comparison with the frozen test predictions: 2064 rows identical, 0 different, for every one of the 8 entries:
  - broker/SECONDARY
  - classifier/SECONDARY
  - classifier/PRIMARY
  - r0202-broker/PRIMARY
  - r0202-analogist/SECONDARY
  - broker/PRIMARY
  - analogist/PRIMARY
  - phylo/PRIMARY
- Training wall times, on a heavily loaded machine (load average 68 to 110):

| entry | train time |
|---|---|
| broker/SECONDARY | 973 s |
| classifier/SECONDARY | 493 s |
| classifier/PRIMARY | 293 s |
| broker/PRIMARY | 228 s |
| analogist/PRIMARY | 215 s |
| r0202-broker/PRIMARY | 52 s |
| r0202-analogist/SECONDARY | 33 s |
| phylo/PRIMARY | 3 s |

- Conclusion: for these rows, the frozen predictions depend neither on sibling rows nor on the rest of the test file. Training reproduces bit for bit from training-0.50 plus the development view. The combiner's choice for an item depends only on that item's candidate strings and the weights, so the object inherits this isolation.

C10. Code audit (PROVED-HERE)
- I grepped all 12 code files under attempts/*/frozen/*/code/:
  - No absolute paths.
  - No reference to solutions, official/ or data-surprise, apart from three docstrings in broker that mention the "official" NED.
  - Files are read only from the manifest, its dev_dir, the model folder and the partition files.
- I scanned the string literals for hard-coded word lists: 0 non-ASCII literals with three or more space-separated segments, in every file.
- Use of the development data:
  - broker/PRIMARY and broker/SECONDARY learn generic substitution priors (learn_univ) from every development family's training-0.10.
  - classifier/PRIMARY and classifier/SECONDARY (identical system.py) use the devx option (see C15).
  - No other entry reads dev_dir.

C11. Validation split and stage 2 (PROVED-HERE)
- Validation split:
  - I rebuilt shared/val/0.50 from data/view/surprise/FAM/training-0.50.tsv with the harness's own split rule (ratio 0.15).
  - train, test and solutions came out byte-identical for all 10 families.
  - In every family, training-0.50 and test-0.50 share 0 COGIDs. Result: VAL_REBUILD PASS.
- Stage-2 refit:
  - Command: tools/stage2.py under SCO, gold map {"0.50": "shared/val"}, entries in the order of combiner/entries.json.
  - Output: "0.50 weights(all 10) [1, 2, 3, 2, 2, 1, 0, 2] in-sample 0.259198 LOFO 0.262507"; LOFO val NED 0.26250736260023105.
  - The written test files are cmp-identical to combiner/test/0.50 (10 of 10); the val files are identical (10 of 10); the LOFO weights are identical.
  - stage2 reads only the validation gold.
- My item-level check:
  - Every object string is one of the entries' strings (strings produced by no entry: 0).
  - 20 items were chosen only through weight-0 entries, as CLAIM.md says.
  - Exact matches: 10612 of 18101 (0.5863).

C12. Freeze records (PROVED-HERE)
- My script checked the last record per ROLE in each attempts/LENS/FROZEN.md, plus CARRIED.md for the carried entries. For all 8 entries, every code-file sha256 and every val-0.50 and test-0.50 result-file sha256 matches. There are no unlisted code files, and all 10 test files of each entry match selection.md.
- Freeze times:

| entry | frozen |
|---|---|
| analogist/PRIMARY | 09:58:18Z |
| phylo/PRIMARY | 10:07:31Z |
| broker/PRIMARY | 10:09:21Z |
| classifier/PRIMARY | 10:18:47Z |
| classifier/SECONDARY | 10:39:38Z |
| broker/SECONDARY | 10:43:41Z |
| r0202-broker/PRIMARY (carried) | 03:14:07Z |
| r0202-analogist/SECONDARY (carried) | 03:23:18Z |

- All new entries froze before the 12:40:00Z deadline.
- rules/carry_setup.out shows code_tree MATCH for the carried entries and ends "CARRY_SETUP PASS".

C13. Order of events (KNOWN, from each record's own date -u line)
- PREREG frozen at 08:49:14Z.
- Freezes from 09:58 to 10:43Z.
- Last lens returned at 11:20:47Z.
- selection.md written at 11:25:56Z.
- Null test run at 11:27Z.
- Sealed check of the new entries done at 11:42:47Z.
- rules/PREREG.md declares:
  - proportion 0.50 only;
  - cell N50 = mean NED;
  - bar FeVeT 0.30880111347517586, with Mockingbird-I1 at 0.35176136367373956;
  - one candidate rule shared by all three cells (rule 10);
  - no aggregate and no partial wins claimed.
- The bar values come from run 0202's scoring of published systems, not from this run's outputs.

C14. Null test rerun (PROVED-HERE)
Command: `STUB_MPL=1 SCO -I tools/null_test.py --prop 0.50 --bar fevet --cand-dir combiner/test/0.50`. Output:
- controls: 400
- best_control: 0.011032244018352122
- real: 0.05967853202112411
- real_beats_all_controls: yes
- control mean 6.578504829674106e-05, sd 0.0037513751152675164
- controls at or above real: 0
- fast path bit-identical in every check: yes

This is identical to rules/null_test.md. Extra check, not pre-registered: the same tool with --bar mockingbird (the criterion's own bar) gives real 0.10263878221968781, best_control 0.012431796567331954, controls at or above real 0.

C15. The disclosed use of development-family rows (NUMERICAL)
- Overlap, measured with classifier/PRIMARY's own load_train:
  - hillburmish: 472 mannburmish rows are added for the targets Atsi and Lashi. None of the gold strings occurs among the renamed, tone-stripped rows (Atsi 0 of 216, Lashi 0 of 209).
  - kesslersignificance: 238 listsamplesize rows are added for English, French and German. Gold strings found verbatim among them: English 16 of 74, French 2 of 83, German 10 of 72.
  - Of those 28 strings, the object predicts exactly 3. The 6-entry combination without the classifier entries predicts 2.
- Sensitivity check (after the fact, not the claimed object):
  - I refit stage 2 on val over the 6 entries without classifier/PRIMARY and classifier/SECONDARY: weights [3, 2, 0, 1, 3, 2], LOFO val 0.271082.
  - Its test-0.50 mean NED is 0.2505548582783105, still 0.058246255197 below FeVeT and 0.101206505395 below Mockingbird-I1.
  - The classifier entries improve hillburmish by 0.005664 and kesslersignificance by 0.000959. That is about the same as in families that get no dev rows (beidazihui 0.005615, luangthongkumkaren 0.004916).
- Bound: if hillburmish and kesslersignificance are given the worse of FeVeT's and Mockingbird-I1's family NED, the object's mean is 0.27455046088782603. That is still below both bars.

## Judgement on each part of the criterion

1. "trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv)"
- What each entry reads:
  - training-0.50 of the 10 surprise families (the harness manifest);
  - the development view: training-0.10 of the development families (broker priors, classifier devx);
  - the masked test-0.50 rows, one partition at a time.
- The stage-2 weights were fit on shared/val/0.50. This split was cut from training-0.50 alone: I rebuilt it byte for byte (C11). Its file is named solutions.tsv, not solutions-*.tsv, and it holds only training-0.50 content.
- Nothing came from another surprise proportion (C7), and no gold of any family was read by any system.
- Every masked answer sits in a sibling row (C8). But the sealed logs, the audits and my retrain with sibling rows removed (C9: 8 of 8 entries, 2064 of 2064 rows identical) show that the predictions use no sibling row.
- Run 0202's freeze records list result files at 0.10 to 0.30 for the carried entries. Those were that run's outputs, and its lenses could not score them; nothing at those proportions enters this object.
- Verdict: met.

2. Development-family rows used for languages shared with surprise families
- The letter: the development families' training-0.10.tsv files are training-*.tsv files of the same task release. The criterion's file pattern does not limit them to the scored family, and no solutions-*.tsv file of any family was read (data/view contains none). So this use is within the letter.
- The spirit: the parenthetical and the definition's verification method show the concern is access to the scored gold (copying solutions, or here sibling rows). The development rows are different datasets' independent transcriptions. The organisers released them for building systems, and they contain no test-0.50 item as such. Their use was pre-registered (PREREG rule 4) and openly disclosed.
- The measured overlap is small and not exploited (C15: hillburmish 0 overlap; kesslersignificance 28 overlapping strings, 3 predicted). The NED win does not depend on it (C15: 0.2505548582783105 without the classifier entries; 0.27455046088782603 under the worst-case bound).
- I conclude the use is within both the letter and the spirit.
- A stricter reading would allow each scored family's own files only. That reading would also rule out generic priors learned from development data (broker), and the task's own design, which releases development data for building systems, contradicts it. Under that reading this object would fail, but the existence of a NED win at 0.50 would not (the alternative object is not claimed and has not been panelled).

3. "mean score over the 10 surprise families at a declared proportion (stated in PREREG.md)"
- The mean is statistics.mean over the 10 families of the official compare_words values (C3, C4).
- PREREG.md (08:49:14Z) declares 0.50 only. That is earlier than selection.md (11:25:56Z), the null test (11:27Z) and the test scoring.
- Verdict: met. The times are recorded, not independently provable from the package.

4. "strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric"
- Mean NED 0.24912258145405175 against Mockingbird-I1's official 0.35176136367373956 (official/results/results-surprise-0.50.json), lower by 0.10263878221968781, in both summation modes.
- The cell's stricter bar, FeVeT's published per-item predictions rescored to 0.30880111347517586, is beaten by 0.05967853202112411.
- Both pass the paired null (C14).
- Verdict: met.

5. "The repo scorer st2022 at a pinned commit computes the score"
- The score comes from compare_words in official/src/sigtypst2022.py, which is byte-identical to the installed module.
- That scorer reproduces Mockingbird-I1's official total and all 10 family values bit for bit.
- The pin is 03094435 (C6).
- Verdict: met.

6. "Report all three; a win on one metric is a win on that metric only"
- CLAIM.md reports ED, NED, BCFS and BLEU, and claims NED only.
- I recomputed BCFS 0.7114179305724276 and BLEU 0.6520222200978466. They are reported here, not claimed in this cell.

7. One cell, one metric, one object
- Cell N50, metric mean NED, object combiner/test/0.50. object/predictions-0.50.tsv holds the same predictions (checker step 4: 10 of 10 rebuilt).
- The sibling cells B50 and L50 claim the same object on other metrics. Each claim is one metric, and this cell borrows nothing from them.

8. Partial wins and overlap with other claims
- The full criterion is met for mean NED.
- Partial win p3 ("exactly one" metric) would not apply in any case, because the object also beats Mockingbird-I1 on BCFS and BLEU.
- Under a conjunctive reading of the criterion (all three metrics), the same object would still meet it.
- The win is not covered by a weaker or earlier claim: the earlier own cells are at 0.10 to 0.30, and the aggregate is not claimed.

## Caveats (none blocks the pass)
- The PREREG, selection and null-test times are each record's own date -u line. The package cannot prove their order independently.
- The pinned commit, the official results JSON and the FeVeT files rest on the recorded status source and the fetch hashes. I had no web access.
- Packaging:
  - data/view_manifest.sha256 lists 2 files that are not shipped, and fevet/expected.sha256 lists 20.
  - Several package files (in tools/, rules/, attempts/.../REPRODUCE.md and scout/scout.md) contain absolute workspace paths that include a local user name.
  - scout/scout.md names outbox folders that contain a personal handle.
  - This is fine while the private quarry stays on this machine, but it must be scrubbed before anything is published (kit rule 12).
- broker/SECONDARY took 973 s to train in my run on a heavily loaded machine. PREREG rule 7 sets 10 min; the sealed check trained it in 263 s. This is a REPRODUCE matter, not a criterion matter.
- I did not rerun the sandboxed sealed check. My retrain with sibling rows removed was not sandboxed, but its copy held no solutions file and no sibling row, and the entries' code reads no path outside the manifest.

confirmed_scope: At proportion 0.50, the frozen stage-2 combination combiner/test/0.50 (the same predictions as object/predictions-0.50.tsv; 8 frozen entries trained only on the surprise families' training-0.50.tsv and the development families' training-0.10.tsv, with weights fit on shared/val/0.50 cut from training-0.50, each masked test-0.50.tsv row predicted without its sibling rows) has mean NED 0.24912258145405175 over the 10 surprise families under the ST2022 scorer pinned at 03094435, strictly lower than Mockingbird-I1's official 0.35176136367373956 in official/results/results-surprise-0.50.json and than this cell's bar, FeVeT's published predictions rescored at 0.30880111347517586, on mean NED only.
pass: true