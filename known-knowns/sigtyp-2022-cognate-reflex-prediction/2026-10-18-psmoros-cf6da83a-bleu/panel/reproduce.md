(Saved by the main session at 2026-10-18T12:37:59Z from the reproduce skeptic subagent's returned text (cell L50; Opus 5.5, agent a2c1d69bf5ebf21c7); the subagent could not write a file named like a report. Text verbatim below.)

# REPRODUCE skeptic, cell L50 (proportion 0.50, mean BLEU), run 2026-10-18-0839

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
start: Sun Oct 18 11:44:30 UTC 2026
end: Sun Oct 18 12:18:28 UTC 2026
material: only the claim package claim/ (CLAIM.md, definition/Q15.json and the files it names), the kit rules and the named interpreters. I made no web requests, so nothing was added to the stop list. No injection_suspected.

## Definition used (quoted)
definition/Q15.json "success_criterion": "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

The statistic is the pinned scorer official/src/sigtypst2022.py, as compare_systems uses it: for each family, compare_words(solutions-0.50.tsv, result-0.50.tsv, report=False)[-1][1:] gives [ED, NED, BCFS, BLEU], and the system value is statistics.mean over the 10 surprise families. The cell bar is FeVeT's published per-item predictions rescored on this scale (rules/PREREG.md rule 2; rule 12 (i) requires a margin of more than 1e-9 in both summation modes).

## Check 1: my own scorer (written before I read any author code)
scratch script scripts/myscore.py (my work folder, outside claim/). It loads official/src/sigtypst2022.py by file path under SCO. It runs two modes:
- lr: builtin sum replaced by a plain left-to-right loop in the sigtypst2022 and lingrex.util namespaces.
- bi: Python 3.13 builtin sum.

It captures "Missing entry" prints and takes the statistics.mean over the 10 families. SCO: Python 3.13.2, lingpy 2.6.9, lingrex 1.2.0.

Calibration on official/systems/mockingbird-i1/surprise/FAM/result-0.50.tsv against the "Mockingbird-I1" entry of official/results/results-surprise-0.50.json:
```
lr mockingbird ED NED BCFS BLEU = [1.4169823165005235, 0.35176136367373956, 0.6050308536957327, 0.5337187296541888] missing 0
lr families bit-identical: 10 /10; total identical: True [True, True, True, True]
bi mockingbird ED NED BCFS BLEU = [1.4169823165005235, 0.35176136367373956, 0.6050308536957327, 0.5337187296541887] missing 0
bi families bit-identical: 1 /10; total identical: False [True, True, True, False]
```
Left-to-right summation reproduces the official JSON bit for bit: all 4 metrics of all 10 families and the total. With builtin sum the last bits differ, as the claim says.

## Check 2: the bar, recomputed from fevet/
fevet/expected.sha256: all 10 pred_0.50_FAM.tsv files OK. All 10 also match the sha256 lines in fevet/FETCH_RECORD.txt. (expected.sha256 also lists 0.10 and 0.30 files that are not in the package. shasum reports them as unreadable. That is not relevant at 0.50.)

My converter (scripts/fevet_conv.py) writes official-layout result files with the solutions header and rows:
```
TOTAL items 18101 covered 18101 gold-mismatch 0 extra 0
```
Every solutions cell is covered. FeVeT's GOLD column equals the solutions cell for every item.
```
lr fevet ED NED BCFS BLEU = [1.286021835157271, 0.30880111347517586, 0.6423935720824072, 0.5768215755932388] missing 0
bi fevet ED NED BCFS BLEU = [1.286021835157271, 0.30880111347517586, 0.6423935720824072, 0.5768215755932388] missing 0
bar 0.5768215755932388 equal: True
```

## Check 3: the claimed object, scored with my scorer
```
lr candidate ED NED BCFS BLEU = [1.0166617451971307, 0.24912258145405175, 0.7114179305724276, 0.6520222200978466] missing 0
bi candidate ED NED BCFS BLEU = [1.0166617451971307, 0.24912258145405175, 0.7114179305724276, 0.6520222200978465] missing 0
claimed 0.6520222200978466 equal lr: True  claimed compensated 0.6520222200978465 equal bi: True
margin over FeVeT lr 0.07520064450460784 bi 0.07520064450460773
margin over Mockingbird official 0.11830349044365784
```
Per-family BLEU (lr), candidate / FeVeT / Mockingbird-I1:

| family | candidate | FeVeT | Mockingbird-I1 |
|---|---|---|---|
| bantubvd | 0.6149144814770632 | 0.592530385802995 | 0.4986880940054677 |
| beidazihui | 0.845286843153689 | 0.7925699791020799 | 0.8001936139106623 |
| birchallchapacuran | 0.5450834358387138 | 0.42729160678332 | 0.3544929894676464 |
| bodtkhobwa | 0.8165114562863156 | 0.7606573057195887 | 0.7101300613249889 |
| bremerberta | 0.6216615225364938 | 0.5154666818090824 | 0.5597163129710025 |
| deepadungpalaung | 0.7044831616267102 | 0.567108229282128 | 0.42755111818027175 |
| hillburmish | 0.5878449397558231 | 0.520134714432988 | 0.44774522451899657 |
| kesslersignificance | 0.2532084192888352 | 0.18794017672637114 | 0.15351700479784142 |
| luangthongkumkaren | 0.8426359713006655 | 0.7631365402270252 | 0.7803301833566277 |
| wangbai | 0.6885919697141568 | 0.6413801360468095 | 0.6048226940083821 |

The candidate beats FeVeT on all 10 families.

The package's standalone checker (python3 -I checker/check_q15.py . object/predictions-0.50.tsv) printed:
```
1. Mockingbird-I1 mean BLEU recomputed 0.5337187296541888, official 0.5337187296541888: EXACT
2. FeVeT published predictions mean BLEU 0.5768215755932388
3. object mean BLEU 0.6520222200978466 over 18101 items (claimed 0.6520222200978466): EQUAL
   margin vs Mockingbird-I1 0.118303490444 (higher is better)
   margin vs FeVeT 0.075200644505 (higher is better)
4. rebuilt official-format files equal to the frozen ones: 10 of 10
PASS
```
My own comparison of object/predictions-0.50.tsv with combiner/test/0.50:
```
object rows 18101 result cells 18101 identical mapping True
```

## Check 4: integrity of saved files
- shasum -a 256 -c MANIFEST.sha256, before any run: rc=0, 379 of 379 OK. No file in the package is missing from the manifest, and no listed file is missing.
- The same check after all retrains: 379 of 379 OK. After I removed my run's side effects (see Notes), there are 0 files not in the manifest.
- My script scripts/check_frozen.py checks every sha256 line in attempts/LENS/FROZEN.md for the 8 entries of combiner/entries.json. Code lines are relative to code/; 0.50 result lines are relative to frozen/ROLE/. For carried entries it also checks the test/0.50 lines in CARRIED.md, and that every code file and every 0.50 result file present is covered by some hash line:
```
broker/PRIMARY               frozen 2026-10-18T10:09:21Z code files ok 1, 0.50 result lines ok 20 (other-proportion lines skipped 0), carried test lines 0, problems 0, code_tree a8f295186339fbdb
classifier/SECONDARY         frozen 2026-10-18T10:39:38Z code files ok 2, 0.50 result lines ok 20 (other-proportion lines skipped 0), carried test lines 0, problems 0, code_tree 6cc33b903ae1097c
broker/SECONDARY             frozen 2026-10-18T10:43:41Z code files ok 1, 0.50 result lines ok 20 (other-proportion lines skipped 0), carried test lines 0, problems 0, code_tree fc4aee016f3e2159
r0202-broker/PRIMARY         frozen 2026-10-18T03:14:07Z code files ok 1, 0.50 result lines ok 10 (other-proportion lines skipped 60), carried test lines 10, problems 0, code_tree e0e12da3febeabfd
classifier/PRIMARY           frozen 2026-10-18T10:18:47Z code files ok 2, 0.50 result lines ok 20 (other-proportion lines skipped 0), carried test lines 0, problems 0, code_tree 014f4baa8694bafe
analogist/PRIMARY            frozen 2026-10-18T09:58:18Z code files ok 2, 0.50 result lines ok 20 (other-proportion lines skipped 0), carried test lines 0, problems 0, code_tree 94556b993ae1b190
phylo/PRIMARY                frozen 2026-10-18T10:07:31Z code files ok 1, 0.50 result lines ok 20 (other-proportion lines skipped 0), carried test lines 0, problems 0, code_tree 94b531e1fe882c36
r0202-analogist/SECONDARY    frozen 2026-10-18T03:23:18Z code files ok 2, 0.50 result lines ok 10 (other-proportion lines skipped 60), carried test lines 10, problems 0, code_tree 476c111d7f481d91
FROZEN CHECK PASS
```
- I recomputed the tree hashes with the freeze formula (sha256 of the sorted "sha256  relpath" lines plus a final newline):
```
code_tree recomputed==record: True for all 8 entries; results_tree(record lines)==record: True for all 8; results_tree(files)==record: True for the 6 entries of this run (n/a for the 2 carried ones: the 0202 record also covers proportions not in the package)
```
- Carried entries: the code_tree in CARRIED.md equals the 0202 record. rules/carry_entries.json code_tree_sha256 and results_tree_sha256_0202 equal CARRIED.md for both broker/PRIMARY and analogist/SECONDARY. The freeze times are 03:14:07Z and 03:23:18Z.
- data/view/surprise: all 20 files (training-0.50 and test-0.50) are byte-identical to official/data-surprise ("20 same"). data/view holds only 0.50 files of the surprise families, plus training-0.10 and test-0.10 of the 10 development families. There are no solutions files in data/view.
- The val split is clean, for all 10 families: "train/test set overlap 0, val sets not in training 0, val sets in test 0, val gold cells not found in training 0". shared/val/0.50 is cut from training-0.50 only.
- rules/: every entry's audit_test_0.50.txt has 40 "identical" lines, 0 FAIL lines, and ends "AUDIT PASS". The sealed logs cover all 8 entries:
  - rules/sealed_new_0.50.log: 100 "bytes IDENTICAL" lines, ends "SEALED_CHECK 0.50 PASS".
  - rules/sealed_carry_0.50.log: 110 lines, ends "SEALED_CHECK 0.50 PASS". It includes carry__broker-PRIMARY and carry__analogist-SECONDARY.

## Check 5: PREREG rule 12 (iv), retrain of every entry from its frozen code
For each of the 8 entries of combiner/entries.json (weight 0 included) I ran this from claim/, in a fresh scratch folder outside claim/ (retrain/LENS-ROLE/):

OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 HOME=(fresh folder) SYS -I tools/q15h.py run --python SYS --code attempts/LENS/frozen/ROLE/code --mode test --out (fresh)/out --props 0.50 --workers 2

The run was capped at 2400 s with perl alarm. Then I ran cmp on every test/0.50/FAM/result-0.50.tsv against the frozen file. At most 3 retrains ran at a time.

SYS: Python 3.13.2, numpy 2.5.4, scipy 1.18.1, sklearn 1.9.1, lingpy 2.6.13, lingrex 1.4.2.

The harness wrote a manifest.json with surprise_train = data/view/surprise/FAM/training-0.50.tsv for the 10 families, and dev_dir = data/view/dev. The train command took only that manifest and the model dir. Predict took only the model dir and the per-family jobs file of partitions.

| entry | weight | retrain window (UTC) | train | rc | test-0.50 files bit-identical | recomputed BLEU (lr) | recomputed BLEU (builtin) | determinism case |
|---|---|---|---|---|---|---|---|---|
| broker/PRIMARY | 1 | 11:48:33-12:06:22 | 423 s | 0 | 10/10 | 0.640778849958583 | 0.6407788499585829 | bit-identical (the 1e-9 fallback was not needed) |
| classifier/SECONDARY | 2 | 11:45:20-11:48:33 | 157 s | 0 | 10/10 | 0.6206724448162763 | 0.6206724448162761 | bit-identical |
| broker/SECONDARY | 3 | 11:45:20-12:10:46 | 432 s | 0 | 10/10 | 0.6440316967070725 | 0.6440316967070724 | bit-identical |
| r0202-broker/PRIMARY | 2 | 11:48:48-11:54:19 | 50 s | 0 | 10/10 | 0.6399423156375929 | 0.6399423156375927 | bit-identical |
| classifier/PRIMARY | 2 | 12:04:43-12:11:01 | 289 s | 0 | 10/10 | 0.6032930588922872 | 0.6032930588922872 | bit-identical |
| analogist/PRIMARY | 1 | 11:45:20-11:48:48 | 109 s | 0 | 10/10 | 0.6312480358613681 | 0.631248035861368 | bit-identical |
| phylo/PRIMARY | 0 | 11:01-12:12:55 (12:11:01 start) | 6 s | 0 | 10/10 | 0.6252463996778401 | 0.6252463996778401 | bit-identical |
| r0202-analogist/SECONDARY | 2 | 11:54:19-11:56:36 | 60 s | 0 | 10/10 | 0.6205899732987447 | 0.6205899732987447 | bit-identical |
| combination (my MBR over the 8 retrained outputs) | stored weights | - | - | - | 10/10 vs combiner/test/0.50 | 0.6520222200978466 | 0.6520222200978465 | bit-identical |

(phylo/PRIMARY retrain window: 12:11:01-12:12:55.)

Over all cmp outputs: "80 same", 0 DIFF.

Each single entry also beats the bar 0.5768215755932388 (lr margins from 0.02647148329904847 for classifier/PRIMARY to 0.06721012111383373 for broker/SECONDARY). The cell result therefore does not depend on the combiner alone.

## Check 6: stage-2 combination, own implementation
scripts/my_mbr.py implements the rule as tools/stage2.py's docstring states it, without the authors' code:
- Items: every "?" cell of data/view/surprise/FAM/test-0.50.tsv.
- Candidates: the 8 entries' strings, in entries.json order.
- Choice: argmin over i of sum_j w_j * NED(c_j to c_i) + 1e-7 * (3 - w_i) + 1e-9 * i.
- NED is the scorer's item value: lingpy nw_align from the pinned module, an empty prediction becomes 2*len 'Ø', and an empty pseudo-gold row adds 0.
- Weights: combiner/combiner_fit.json "0.50" "weights_all10" = [1, 2, 3, 2, 2, 1, 0, 2].

Output on the frozen entry predictions:
```
{"items": 18101, "exact_vs_float_disagree": 0, "min_gap": 1.000000082740371e-09, "chosen_by_entry": [8, 1747, 15700, 294, 63, 41, 20, 228], "n_only_weight0": 20}
only_weight0 first 12: ['bantubvd 1396-1-1', 'bantubvd 3664-1-1', 'bantubvd 3756-1-1', 'bantubvd 4688-3-2', 'beidazihui 1011-10-Nanchang', 'beidazihui 60-15-Wenzhou', 'beidazihui 707-19-ZhongyuanYinyun', 'birchallchapacuran 133-2-jaru', 'birchallchapacuran 97-9-wanyam', 'deepadungpalaung 17-14-PangKham', 'hillburmish 119-2-Atsi', 'hillburmish 125-4-Lashi']
same bantubvd ... same wangbai   (cmp: 10 of 10 families byte-identical to combiner/test/0.50)
```
Notes on this output:
- The 20 items chosen only from a weight-0 entry (phylo/PRIMARY) match the count and the first 12 items listed in CLAIM.md.
- An exact-fraction version of the risk with lexicographic ties agrees with the float rule on every item.
- Run on the 8 retrained outputs, the combination is again 10/10 byte-identical. The stats line is the same.

Weight refit, two ways:
(a) tools/stage2.py rerun from claim/: STUB_MPL=1 SCO -I tools/stage2.py --entries E.json (a copy of combiner/entries.json) --val-test-root shared/val --gold-map G.json ({"0.50": "shared/val"}) --test-root data/view --props 0.50 --out (scratch)
```
0.50 weights(all 10) [1, 2, 3, 2, 2, 1, 0, 2] in-sample 0.259198 LOFO 0.262507
0.50 LOFO val mean (combine.py value) 0.26250736260023105; official compare_words on the written val files: NED 0.26250736260023105 (ED 1.085555251937082 BCFS 0.8428560115539521 BLEU 0.6241764938734388)
```
All 20 output files (test/0.50 and the LOFO val/0.50) are byte-identical to combiner/ ("20 same").

(b) My own exhaustive search (scripts/my_fit.py, numpy) over all 65535 non-zero tuples in {0..3}^8, using the entries' frozen val/0.50 files and shared/val/0.50 gold. It uses the compare_words family NED and the tuple tie rule from the docstring:
```
best weights [1, 2, 3, 2, 2, 1, 0, 2] in-sample mean val NED 0.2591983017536702
next [0, 1, 3, 2, 2, 1, 0, 2] 0.25939738927941336
stored tuple rank 1 of 65535 F 0.2591983017536702
```
The stored value is 0.25919830175367015; the difference is in the last bit, from summation order.

## Check 7: what the code reads, and row isolation
- Code audit (grep of every open/glob/listdir/walk/Path/environ/subprocess/import, and reading of each train and predict function in all 8 code/system.py):
  - train reads only man["surprise_train"][FAM] (training-0.50).
  - broker/PRIMARY and broker/SECONDARY also read man["dev_dir"]/FAM/training-0.10.tsv of the development families.
  - classifier/PRIMARY and classifier/SECONDARY also read dev_dir/mannburmish and dev_dir/listsamplesize training-0.10.tsv. This is disclosed in CLAIM.md and permitted by PREREG rule 4 (data/view/dev).
  - Other reads: code/config.json, and the model dir.
  - predict reads only the model dir and the partition files of --jobs, and loops partition by partition and row by row.
  - No code reads any solutions, cognates or wordlist file, or any surprise file of another proportion; data/view holds none.
  - No network or subprocess use. The env overrides BRK_DEV and CLS_OPTS exist but were not set.
- The harness (tools/q15h.py make_partitions) splits each test file by masked language and asserts that no partition holds two rows of one cognate set.
- My own isolation audit (scripts/my_audit.py, seed 4242, different rows from the harness audit seed 20261017). For each entry and family, with the retrained model, each in a fresh process: 4 random rows predicted alone, plus one random partition predicted with its rows in reversed order. Every prediction was compared with the frozen merged result:
```
analogist/PRIMARY MY_AUDIT PASS checks 50 failed 0
classifier/SECONDARY MY_AUDIT PASS checks 50 failed 0 22s
r0202-broker/PRIMARY MY_AUDIT PASS checks 50 failed 0 61s
r0202-analogist/SECONDARY MY_AUDIT PASS checks 50 failed 0 13s
broker/PRIMARY MY_AUDIT PASS checks 50 failed 0 65s
broker/SECONDARY MY_AUDIT PASS checks 50 failed 0 117s
classifier/PRIMARY MY_AUDIT PASS checks 50 failed 0 25s
phylo/PRIMARY MY_AUDIT PASS checks 50 failed 0 144s
```

## Check 8: null test, own implementation (supporting, not my lens's gate)
scripts/my_null.py follows rules/null_test.md and REPRODUCE.md section 5:
- 400 controls; control c uses random.Random(20261018 + c), with one draw per cognate set.
- Families are in fixed order; sets are in order of first appearance in the solutions file.
- A draw below 0.5 swaps all rows of that set between the candidate and FeVeT.
- BLEU uses compare_words aggregation with left-to-right sums.
```
real cand 0.6520222200978466 bar 0.5768215755932388 d 0.07520064450460784
controls 400 best control d 0.0125124368567755 real beats all: True
```
This agrees with rules/null_test.md (real 0.07520064450460762, best control 0.01251243685677561) to about 1e-15. The record's tool is a separate standard-library implementation.

## Notes (none of them changes the result)
- Side effects inside claim/ from my runs, all removed afterwards:
  - __pycache__ under tools/ and official/src/, from importing mplstub and the scorer.
  - attempts/phylo/frozen/PRIMARY/home (lingpy 2.6.13 sound-class caches). phylo/PRIMARY's code sets HOME to a "home" folder beside its own code folder, so any retrain writes there. It holds generic lingpy caches, no word data.
  - MANIFEST.sha256 was 379 of 379 OK after the runs, and the package has no extra files after cleanup.
- To meet the deadline I stopped my own queue loop subshell (a PID I started, killed by number) and started classifier/PRIMARY and phylo/PRIMARY earlier. Never more than 3 retrains ran at once. My short single-process scoring and combination jobs (each under 30 s) overlapped with them.
- For CRITERION and NOVELTY, not my lens: classifier/PRIMARY and classifier/SECONDARY (weight 2 each) add development-family rows (mannburmish for hillburmish; listsamplesize english/german/french for kesslersignificance). These may hold the same concepts as the surprise gold in another dataset's transcription. This is disclosed in CLAIM.md, and they are training-*.tsv files of the task release. The cell does not hinge on it: every single entry, including the 6 that read no such rows, beats the bar on its own (smallest such margin 0.04376839770550589, r0202-analogist/SECONDARY).
- Kit rule 12 hygiene for any publication: 17 package files contain absolute home-directory paths. Examples: combiner/combiner_fit.json entry_dirs, tools/q15h.py DEFAULT_PY and SCORER_PY, each entry's REPRODUCE.md, rules/selection.md, rules/null_test.md, the sealed logs, scout/scout.md. They should be scrubbed before anything is shared. The target is private, so nothing leaves this machine.
- I could not check the pinned commit hash of official/src/sigtypst2022.py online (no web for this lens). Its sha256 is 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a. It reproduces the official results-surprise-0.50.json for Mockingbird-I1 bit for bit, which is the binding calibration.

## Verdict
- Every entry was retrained from its frozen code: 80 of 80 files byte-identical, and all eight entries are bit-deterministic.
- The combination was rebuilt by my own implementation: 10 of 10 files byte-identical.
- The weight refit gave the same weights, both with tools/stage2.py and with my own search.
- My scorer is calibrated bit for bit on Mockingbird-I1. It gives the claimed mean BLEU, 0.6520222200978466 (lr) and 0.6520222200978465 (builtin). This beats the bar 0.5768215755932388 by 0.07520064450460784 (lr) and 0.07520064450460773 (builtin), more than 1e-9 in both modes. It also beats Mockingbird-I1's official 0.5337187296541888.
- No mismatch, missing object, forbidden read or non-determinism was found.

pass: true