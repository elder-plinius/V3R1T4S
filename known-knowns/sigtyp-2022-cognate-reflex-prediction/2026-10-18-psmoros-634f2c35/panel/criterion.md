(Saved by the main session from the subagent's returned text, 2026-10-18T07:03Z: round-2 CRITERION skeptic for cell C30 (Opus 5.5, Agent tool), on the round-2 claim package. Verbatim below, harness indentation removed.)

# Panel: CRITERION skeptic, cell C30 (proportion 0.30, mean NED), round 2

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
start: Sun Oct 18 06:12:43 UTC 2026 (date -u)
end: Sun Oct 18 06:40:51 UTC 2026 (date -u)
material read: claim/ (the copied package), the kit's RULES.md and TROPHY_CASE.md (TROPHY_CASE has no sigtyp/ST2022/cognate entry). Nothing else in the workspace was read.
network requests: none. No stop-list line was written. No URL was requested.
interpreters: SCO (pinned-scorer venv, used only as an interpreter: lingpy 2.6.9, lingrex 1.2.0), SYS (the q15ml system venv, used by the sealed check), and python3.13 for my own scripts. My scripts and outputs are in this skeptic's scratch folder, outside claim/.

## Criterion (verbatim, claim/definition/Q15.json "success_criterion")
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

What is claimed (CLAIM.md): one cell (P 0.30), one metric (mean NED), one object (combiner/test/0.30). No partial win (p1-p3) is claimed. The full criterion is judged on NED only.

## Checks run, with real output

### 1. Package integrity (shasum -a 256 -c MANIFEST.sha256)
332 lines OK, 0 not OK. The set of files equals the manifest list exactly ("file set identical to manifest").

### 2. Scorer identity
- sha256 of official/src/sigtypst2022.py is 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a. The module installed in SCO has the same hash.
- scout/st2022_commits.json: newest commit 03094435cba4293ce0eea383036cab78499ad50d, 2022-05-27T07:58:23Z, "update for final release". This matches the pinned commit in PREREG.
- I read compare_systems in official/src/sigtypst2022.py: the total is statistics.mean of compare_words(...)[-1][1:] over the datasets. My scorer uses exactly that code path. The CLI `st2022` was not invoked; it calls the same functions.

### 3. My own recomputation with the official compare_words (my script myscore.py, from claim/ files only; ltr = left-to-right sum shadowed in sigtypst2022 and lingrex.util)
```
ltr Mockingbird-I1 total [1.1762187506031638, 0.2898984929868421, 0.6717099225519634, 0.6058548112827981] official [same] total_bit_identical True families_bit_identical True
ltr candidate combiner/test/0.30 total [ED,NED,BCFS,BLEU] [0.9027034122955315, 0.22327922550091464, 0.7488264857956657, 0.6839233380559118]
ltr FeVeT rescored total [1.0946456488227652, 0.2632988364952282, 0.6986581179861967, 0.6356571184958077]   (all 10 families: missing 0, gold_mismatch 0)
ltr margin vs Mockingbird-I1 official NED: 0.066619267486
ltr margin vs FeVeT rescored NED: 0.040019610994
builtin candidate total [0.9027034122955314, 0.22327922550091467, 0.7488264857956657, 0.6839233380559119]
builtin FeVeT rescored total [1.094645648822765, 0.2632988364952282, 0.6986581179861968, 0.6356571184958079]
builtin margin vs Mockingbird-I1 official NED: 0.066619267486
builtin margin vs FeVeT rescored NED: 0.040019610994
```
Per-family NED, candidate / Mockingbird-I1 / FeVeT:
- bantubvd: 0.218380 / 0.296221 / 0.253610
- beidazihui: 0.111579 / 0.123724 / 0.138280
- birchallchapacuran: 0.289302 / 0.393862 / 0.349971
- bodtkhobwa: 0.106780 / 0.170167 / 0.122121
- bremerberta: 0.229241 / 0.241785 / 0.292404
- deepadungpalaung: 0.161543 / 0.319762 / 0.233319
- hillburmish: 0.261946 / 0.310702 / 0.276574
- kesslersignificance: 0.599932 / 0.723283 / 0.659450
- luangthongkumkaren: 0.080172 / 0.113312 / 0.108955
- wangbai: 0.173917 / 0.206167 / 0.198306

All headline values in CLAIM.md (the ED/NED/BCFS/BLEU table and both margins) are reproduced digit for digit. The candidate file is complete: 11586 solution rows, 11586 candidate rows, 0 extra rows, 0 missing, empty or "?" cells.

### 4. Data provenance and the sibling-row trap (my script datacheck.py)
For every family:
- data/view == official: True for both training-0.30 and test-0.30.
- test keys == solution keys: True.
- training ∩ test cognate sets: 0.
- shared/val/0.30 rebuilt from training-0.30 with the organisers' split rule (q15h.split_training_test_data, ratio 0.15): byte-identical for train, test and solutions.
- val ∩ test-0.30 sets: 0. val ⊂ training-0.30: True.

```
TOTAL test-0.30 rows 11586, gold visible verbatim in a sibling row of the same set: 11586
```
So every masked answer can be read from a sibling row of the same file, and row isolation is decisive (see checks 8 and 9).

### 5. Is training-0.50 (used for development) disjoint from test-0.30? (my script nested.py; gold-free)
The official split_data splits the same cognates.tsv at every proportion with the same stable coverage sort, so test-P is a prefix of that order. For all 10 families, test-0.30 is consistent with being the top-30% prefix: the set count equals int(N*0.30+0.5), and min test coverage >= max training coverage. Example: bantubvd has 388 sets, 116 test sets, expected 116, coverage 3/3. All 10 families print "prefix-consistent".

So test-0.30 ⊂ test-0.50, and training-0.50 ⊂ training-0.30. Label: HEURISTIC. This is inferred from the official code plus the prefix check; the training-0.50 files are not in the package.

### 6. The claimed object is a gold-free function of the components (I re-ran stage 2)
Command: SCO -I claim/tools/stage2.py, with entries = combiner/entries.json order, --val-test-root shared/val, gold-map {0.30: shared/val}, --test-root data/view, --props 0.30.
```
0.30 matrices: 0.9s ...; empty candidates val 0 test 0
0.30 weights(all 10) [2, 2, 0, 3, 0, 3] in-sample 0.229557 LOFO 0.234363
0.30 LOFO val mean (combine.py value) 0.23436296736916745; official compare_words on the written val files: NED 0.23436296736916745
```
- All 10 test files and all 10 LOFO val files are byte-identical to combiner/test/0.30 and combiner/val/0.30 (cmp).
- combiner_fit.json at 0.30: weights_all10, insample_mean_all10, lofo_val_mean, lofo_weights, single_entry_val_mean and lofo_val_scorer_total all equal the shipped values.
- Stage 2 reads only component predictions, val gold cut from training-0.30, and the masked test file (for the item list).
- Selection (rules/selection.md): COMB-NEW's val-0.30 value 0.23436296736916745 is below the best single new entry, broker/PRIMARY at 0.2396718067901131.

Weight-0 influence (my own count): 6 items take a string produced only by a weight-0 entry. These are bantubvd 1418-1 and 2893-8, kesslersignificance 560-1, 1155-4 and 421-5, and wangbai 3536-5, all from analogist/PRIMARY. This matches CLAIM.md. Every chosen string is produced by at least one entry.

### 7. Freeze and selection hashes
- The sha256 of each of the 10 combiner/test/0.30 files equals the hash listed for out/comb_new/test/0.30 in rules/selection.md (10 of 10 match).
- The sha256 of each FROZEN.md equals the hash in selection.md:
  - analogist c8b4cf2c…
  - broker d41dd287…
  - classifier df50a06e…
  - phylo 32b2829e…
- My script frozencheck.py, using the last record per role, checked each entry's code and its 0.30 result files against that record:

| entry | frozen at | code files (mismatches) | 0.30 result files (matching) |
|---|---|---|---|
| broker/PRIMARY | 2026-10-18T03:14:07Z | 1 (0) | 20 (20) |
| analogist/SECONDARY | 03:23:18Z | 2 (0) | 20 (20) |
| broker/SECONDARY | 04:00:49Z | 1 (0) | 20 (20) |
| phylo/PRIMARY | 03:19:07Z | 1 (0) | 20 (20) |
| analogist/PRIMARY | 02:43:13Z | 2 (0) | 20 (20) |
| classifier/PRIMARY | 04:03:30Z | 2 (0) | 20 (20) |

No code file is present without being listed.

### 8. Code audit: what each component reads
- Training: the only manifest keys used are man["families"] and man["surprise_train"] (grep over all six system.py files). There are 0 references to dev_dir, dev_families or "dev". No urllib, requests, socket or subprocess imports.
- Prediction: each component reads only the model dir (plus config.json in its own code folder) and the partition files listed in --jobs. It predicts row by row; analogist and broker build fresh per-row state.
- Embedded data: only generic sound-symbol tables (vowel, tone and consonant-class character sets). No word lists.
- Harness audits: every entry's test-mode audit file ends "AUDIT PASS", with 40 of 40 audit lines at 0.30 "identical" and 0 FAIL/MISMATCH.

### 9. Sealed retrain-and-predict, run by me (all six entries)
Command: python3.13 -I claim/tools/sealed_check.py --prop 0.30, all six frozen ROLE folders, --jobs 3, strict profiles, work root in my scratch folder, --view claim/data/view.
```
2026-10-18T06:17:06Z SEALED 0.30 start: 6 components, 11586 test rows in memory (parent), jobs 3, strict profiles
phylo__PRIMARY train ok 5s; 10 families ok, items identical, bytes IDENTICAL; predict: 99 sealed processes, 416s
broker__PRIMARY train ok 95s; 10/10 bytes IDENTICAL; 99 sealed processes, 131s
analogist__SECONDARY train ok 55s; 10/10 bytes IDENTICAL; 99 sealed processes, 25s
classifier__PRIMARY train ok 292s; 10/10 bytes IDENTICAL; 99 sealed processes, 39s
analogist__PRIMARY train ok 38s; 10/10 bytes IDENTICAL; 99 sealed processes, 18s
broker__SECONDARY train ok 81s; 10/10 bytes IDENTICAL; 99 sealed processes, 135s
2026-10-18T06:39:17Z SEALED 0.30 done in 1330s
SEALED_CHECK 0.30 PASS
```
Every family line reads, for example, "items identical 2945/2945 bytes IDENTICAL". Independent cmp: 60 of 60 sealed result files are byte-identical to the frozen ones.

Sandbox efficacy test: I ran python under the generated profiles and tried to open files.
- predict.sb: claim/official/.../solutions-0.30.tsv, claim/data/view/.../test-0.30.tsv, claim/data/view/.../training-0.30.tsv, the sandbox's own input training copy, and another partition (part-02) all fail with "PermissionError: [Errno 1] Operation not permitted". Its own partition part-01 gives READ OK.
- train.sb: the gold, the view test file and the view training file are all denied. Its own input/training-0.30 copy gives READ OK. (The partition folder is readable under train.sb, but partitions are written only after training ends.)

So each component is trained from training-0.30 alone. Each test partition, which by assertion holds no two rows of one cognate set, is predicted alone in a fresh sealed process, and the frozen predictions are reproduced exactly. The sibling-row answers cannot have reached any prediction. Together with check 6, this is a full train->predict reproduction of the claimed object from training-0.30 + masked test-0.30. Label: PROVED-HERE.

### 10. Null test (rules/null_test.md; my own implementation, mynull.py, official nw_align item NED, compare_words aggregation, ltr sums)
```
bar fevet       PREREG seeds 20261018+c    cand 0.22327922550091464 bar 0.2632988364952282 real d 0.04001961099431353 | max control 0.01038051165515197 | controls >= real 0 | mean 9.711894693928851e-05 sd 0.0035018285383694057
bar fevet       independent seeds 99173+c  ... real d 0.04001961099431353 | max control 0.011117108917412938 | controls >= real 0
bar mockingbird PREREG seeds 20261018+c    ... bar 0.2898984929868421 real d 0.06661926748592747 | max control 0.01695492782041369 | controls >= real 0
bar mockingbird independent seeds 99173+c  ... real d 0.06661926748592747 | max control 0.012985890213222162 | controls >= real 0
```
This reproduces null_test.md exactly: real 0.04001961099431353, best control 0.01038051165515197, control mean 9.711894693928851e-05, sd 0.0035018285383694057. real_beats_all_controls = yes, against both the cell bar and the criterion's named bar.

### 11. Declared proportion: was it fixed before results? (all times self-reported in the package)
- rules/PREREG.md says it was frozen at 2026-10-18T02:09:41Z. It declares C30 = proportion 0.30, mean NED, bar FeVeT 0.2632988364952282.
- First freeze: 02:43:13Z. Last eligible freeze: 04:36:18Z.
- rules/selection.md was written at 04:46:29Z, "before any surprise-test gold was read".
- Sealed check start: 04:46:45Z. Null test: 04:49Z.
- null_test.md cites selection.md sha256 2d0d43d4901280c8c26b1ae2d3b02e0c8c770873de4e9ee67cbf3dffedd1063c, which equals my shasum of rules/selection.md.

The ordering is internally consistent. There is no external timestamp or commitment for PREREG.md, so the time itself cannot be independently verified (label: KNOWN-from-package only).

## Verdict on the literal criterion
- **"trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv)": met.**
  - Components: training-0.30 only, sealed (check 9).
  - Stage-2 weights: val split cut from training-0.30, rebuilt byte-identical, disjoint from test-0.30 (checks 4 and 6).
  - Development used training-0.50 / val-0.50. These are training-*.tsv files and, by the official nested split, a subset of training-0.30 (check 5, HEURISTIC).
  - No solutions file, no other proportion's test file and no system's predictions are read by the frozen system.
  - Generic phonetic-symbol knowledge in the code (and lingpy sound classes in phylo) is not training data; the organisers' own LingRex baseline uses the same library.
- **"mean score over the 10 surprise families at a declared proportion ... stated in PREREG.md": met** (0.30, declared before any result per the package timeline).
- **"strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric": met.** Mean NED is 0.22327922550091464 against 0.2898984929868421, a margin of 0.066619267486 in both summation modes. The cell's stricter bar, FeVeT rescored at 0.2632988364952282, is also beaten, by 0.040019610994 in both modes.
- **"The repo scorer st2022 at a pinned commit computes the score": met** as far as can be checked offline. The pinned module is byte-identical to the scorer venv's module, Mockingbird-I1's official 0.30 totals and all 10 family values are reproduced bit for bit, and compare_systems' code path is used.
- **"Report all three": met** (ED, NED, BCFS and BLEU are all in CLAIM.md). Only NED is claimed.
- **One cell, one metric, one object: yes.**
- **Null: passes.**
- **Not subsumed:** no earlier confirmed claim covers P 0.30. The earlier confirmed claim is P 0.10 only, and TROPHY_CASE has no entry for this target. Whether a lower published 0.30 value exists is the NOVELTY skeptic's question.

## Caveats (none changes the verdict)
1. Privacy (kit rule 12): absolute paths containing a user name appear in package files. Examples: combiner/combiner_fit.json "entry_dirs", scout/scout.md, path constants in tools/*.py, attempts/*/frozen/*/REPRODUCE.md, and the "python ..." field of rules/sealed*_check_0.30.log. Scrub them before anything leaves the machine.
2. The PREREG and selection times are self-reported. Only their internal consistency was checked.
3. The scorer bytes were not compared with the remote at 03094435 (no web, by instruction). Bit-identical calibration is the evidence.
4. The training-0.50 files are not in the package. Disjointness from test-0.30 is inferred (check 5).
5. What lenses read during development (their briefs, any meta-knowledge from run 2026-10-17-1806) cannot be audited from the package. The frozen systems' inputs are verified directly. Given the margins (0.040 below FeVeT, max null control 0.0104), method-level knowledge cannot explain the result.

confirmed_scope: At proportion 0.30, the frozen stage-2 combiner predictions combiner/test/0.30, reproducible from the surprise families' training-0.30 files and masked test-0.30 rows alone, score mean NED 0.22327922550091464 over the 10 SIGTYP-2022 surprise families under the pinned official ST2022 scorer (left-to-right summation; 0.22327922550091467 with compensated summation), strictly below FeVeT's published predictions rescored on the official scale (0.2632988364952282) and Mockingbird-I1's official results-surprise-0.30.json value (0.2898984929868421).

pass: true
