(Saved by the main session from the subagent's returned text, 2026-10-18T07:02Z: round-2 CRITERION skeptic for cell C20 (Opus 5.5, Agent tool), on the round-2 claim package. Verbatim below, harness indentation removed.)

# CRITERION skeptic, cell C20 (proportion 0.20, mean NED), round 2

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
start: 2026-10-18T06:12:41Z (date -u)
end: 2026-10-18T06:54:26Z (date -u)
material: claim/ only (CLAIM.md, definition/Q15.json and the rest of the package), plus kit RULES.md. Interpreters: SYS (the component systems' venv), SCO (used only as an interpreter with the pinned scorer installed), and my own python3.13. I wrote my scratch scripts (myscore.py, valcheck.py, isolate.py, plus copies of tools/stage2.py and tools/null_test.py with the clone path pointed at claim/official) outside claim/.
web: none. I made no network requests and added nothing to any stop list. injection_suspected: none.

## Criterion (verbatim, definition/Q15.json "success_criterion")
"A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

The claim (CLAIM.md) covers one cell (0.20), one metric (mean NED) and one object (combiner/test/0.20). It claims no partial win.

## Checks run (real output)

1. Package integrity
   - MANIFEST.sha256: 322 lines, 0 failures, no unlisted files.
   - My imports had written two __pycache__ .pyc files into claim/. I removed them, and the re-check gives 323 files and 0 failures.
   - The four FROZEN.md sha256 values match rules/selection.md:
     - analogist c8b4cf2c...
     - broker d41dd287...
     - classifier df50a06e...
     - phylo 32b2829e...
   - All 10 claimed files (combiner/test/0.20/*/result-0.20.tsv) match the frozen candidate hashes for out/comb_new/test/0.20 in selection.md: 10 of 10 MATCH.
   - combiner/combiner_fit.json is 9cc0d8a7...f53ec, the same value as in selection.md.
   - rules/selection.md is 2d0d43d4...d1063c, the hash rules/null_test.md cites.

2. Component freeze records. For each of the 6 stage-2 entries, the code files and all 20 result files at 0.20 (val and test) match that entry's last FROZEN.md record, with 0 bad.
   - Freeze times: analogist/PRIMARY 02:43:13Z, broker/PRIMARY 03:14:07Z, phylo/PRIMARY 03:19:07Z, analogist/SECONDARY 03:23:18Z, broker/SECONDARY 04:00:49Z, classifier/PRIMARY 04:03:30Z.
   - All are before the 05:45:00Z deadline in PREREG rule 8.

3. Data view. data/view/surprise/*/training-0.20.tsv and test-0.20.tsv are byte-identical to official/data-surprise for all 10 families.

4. Scorer
   - official/src/sigtypst2022.py has sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a. The SCO-installed module has the same hash.
   - Mockingbird-I1 rescored with left-to-right summation: [1.0413225298738344, 0.2648052468982754, 0.7119659170836019, 0.632633947442519]. Total bit-identical to official results-surprise-0.20.json: True. All 10 family values bit-identical: True.
   - With builtin (compensated) summation, the total is also bit-identical; the family values are not.

5. Headline, recomputed by me: compare_words per family, then statistics.mean over the 10 families, as compare_systems does.
   - Left-to-right, candidate [ED, NED, BCFS, BLEU] = [0.7979822478300038, 0.20345235544710852, 0.7780895356732769, 0.7080911153196365].
   - Builtin: NED 0.20345235544710852 (BCFS 0.7780895356732768, BLEU 0.7080911153196366).
   - Margin (bar minus candidate) = 0.061352891451166874 in both modes, which is more than 1e-9 and strictly lower.
   - The candidate also has higher BCFS and higher BLEU than Mockingbird-I1. These are reported only, not claimed.
   - Candidate NED is lower than Mockingbird-I1's on 10 of 10 families:

     | family | candidate NED | Mockingbird-I1 NED |
     |---|---|---|
     | bantubvd | 0.202901 | 0.285629 |
     | beidazihui | 0.105196 | 0.128728 |
     | birchallchapacuran | 0.269337 | 0.360943 |
     | bodtkhobwa | 0.104679 | 0.151719 |
     | bremerberta | 0.192843 | 0.206882 |
     | deepadungpalaung | 0.148531 | 0.282131 |
     | hillburmish | 0.221877 | 0.271767 |
     | kesslersignificance | 0.556804 | 0.657344 |
     | luangthongkumkaren | 0.084567 | 0.115461 |
     | wangbai | 0.147790 | 0.187449 |

   - These values match CLAIM.md exactly.

6. Official 0.20 table. Mockingbird-I1 at 0.2648052468982754 is the lowest real NED. Next come Mockingbird-N1-A 0.2824943744126804 and Baseline-SVM 0.2927965125082604. "Mockingbird-N2" shows all zeros; this is compare_systems' [0, 0, 0, 0] for a missing result file, not a score. In any case the criterion names Mockingbird-I1 as the bar.

7. Stage-2 refit. I re-ran tools/stage2.py (copy) at 0.20 from the frozen component val and test predictions, with gold only from shared/val/0.20:
   - weights(all 10) [2, 3, 2, 1, 0, 3]; LOFO val mean 0.23429616596915276.
   - All 10 combiner/test/0.20 files and all 10 combiner/val/0.20 files are byte-identical to my output.

8. Validation split
   - Rebuilt from official training-0.20 with the official split_training_test_data(ratio=0.15). train, test and solutions are identical to shared/val/0.20 for all 10 families.
   - Every val set is inside the training-0.20 sets. Overlap of val sets with test-0.20 sets is 0, and overlap of training-0.20 with test-0.20 is 0, in every family.
   - The official 0.20 files follow the nested construction. Test sets = int(N*0.2+0.5), for example 78 of 388 in bantubvd. In every family the smallest test set is at least as large as the largest training set, and the training file is in non-increasing order.
   - So by the pinned split code (one cognates.tsv, a stable sort), training-0.50 and val-0.50 lie inside training-0.20 and are disjoint from test-0.20. I proved this from the code and the 0.20 files; training-0.50 is not in the package.

9. Code audit: what each component reads (all 6 system.py files).
   - Train reads only man["surprise_train"][fam], which the harness sets to data/view/surprise/<fam>/training-0.20.tsv, plus its own config.json.
   - Predict reads only the model dir and the partition files named in --jobs.
   - No system uses dev_dir. None builds test, solutions or other paths. None uses network, base64, zlib, exec or eval, or embeds data (longest line 506 characters: a config dict).
   - Predict loops row by row, with fresh per-row state in broker and analogist.
   - stage2.py reads only val gold (--gold-map) and masked test files.

10. Retrain and re-predict. I ran tools/q15h.py run in test mode at P 0.20 with --workers 1 for every entry, using copies of the frozen code.
    - All 6 match the frozen test/0.20 files byte for byte, 10 of 10 families each: analogist/SECONDARY, broker/PRIMARY, classifier/PRIMARY, analogist/PRIMARY, broker/SECONDARY, phylo/PRIMARY.

11. Row isolation, my own test. I used each retrained model and predicted every test-0.20 partition (one masked language) alone, in its own fresh process and folder that held only that partition. No partition holds two rows of one cognate set.
    - The merged results are byte-identical to frozen in all 10 families for all 6 entries: "ISOLATION PASS" 6 of 6, 99 partitions per entry.
    - My test was not sandboxed. The code audit (check 9) shows no other file access. The package's sandboxed logs (rules/sealed_check_0.20.log, rules/sealed2_check_0.20.log) end "SEALED_CHECK 0.20 PASS".
    - The lens audits at 0.20 show 40 checks identical, 0 FAIL, "AUDIT PASS" for all 6.

12. Sibling-answer trap and leak check
    - All 7887 of the 7887 test-0.20 answers appear verbatim in a sibling row of the same set, so copying from siblings would be possible.
    - Exact-match rates:
      - Candidate on test: 5076 of 7887 (0.6436).
      - Clean leave-one-family-out (LOFO) combiner on val-0.20: 2823 of 4425 (0.6380).
      - Mockingbird-I1 on test: 4316 of 7887 (0.5472).
    - The test rate matches the val rate, which is the opposite of what copying (a rate near 1.0) would give.

13. Null test (rules/null_test.md). I re-ran tools/null_test.py (copy, clone path set to claim/official) with --prop 0.20 --bar mockingbird:
    - Real d = 0.061352891451166874.
    - The fast path was bit-identical in all 6 checks.
    - 400 controls; best_control 0.01732600288224881; real_beats_all_controls yes; control mean 0.00030137828913791466, sd 0.00576800935470761; controls at or above real: 0.
    - This is identical to rules/null_test.md.

14. Weight-0 entry. Every one of the 7887 chosen strings comes from at least one entry. Exactly one item's string comes only from analogist/PRIMARY (weight 0): kesslersignificance 1222-2, as CLAIM.md says. analogist/PRIMARY passes checks 10 and 11 and sealed2.

15. Timeline (times as stated in the package; file mtimes are copy times):
    - PREREG frozen 2026-10-18T02:09:41Z, after the session start at 02:02:48Z.
    - First freeze 02:43:13Z.
    - selection.md written 04:46:29Z, before any test gold was read, and it holds the object's hashes; the object is unchanged (check 1).
    - Sealed check 04:46:45Z to 05:03:02Z; null test 04:49Z; sealed2 06:03Z.
    - PREREG fixes metric NED at proportion 0.20 for cell C20 before any system output.

## Clause-by-clause verdict
- "trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv)": MET.
  - Components train on training-0.20 only (code, my retrain, sealed logs).
  - Each masked row is predicted from its own partition only (my isolation test).
  - Stage-2 weights come from val-0.20, which is cut out of training-0.20 (rebuilt identically).
  - Development and member selection used val-0.50 and training-0.50 per PREREG, which are subsets of training-0.20 and disjoint from test-0.20.
  - No other proportion's test file and no solutions-*.tsv or gold is read by any part of the system.
  - Note: the literal criterion would even allow reading the masked test file whole (sibling copying); this claim meets a stricter row-isolation standard, so it is not the degenerate loophole.
- "mean score over the 10 surprise families at a declared proportion ... stated in PREREG.md": MET. 0.20 and NED were declared at 02:09:41Z, before results. PREREG declares three cells in three folders; this folder claims only 0.20, and the margin (about 10.6 null SDs, 10 of 10 families) leaves no room for a selection effect.
- "strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric": MET. 0.20345235544710852 < 0.2648052468982754 on mean NED, in both summation modes.
- "Report all three": MET. ED, NED, BCFS and BLEU are reported, and only NED is claimed.
- "The repo scorer st2022 at a pinned commit": MET. This is the pinned module's compare_words with compare_systems' aggregation (commit 03094435 per scout/), shown by reproducing the official Mockingbird-I1 JSON bit for bit. I did not invoke the CLI binary itself; it calls the same functions.
- FeVeT published no value at 0.20. This does not matter for the criterion: FeVeT is not in the official results-surprise-0.20.json, and the criterion's bar is Mockingbird-I1 only. Comparison with FeVeT is a novelty question, not a criterion question.
- Not subsumed: this is a distinct cell from the earlier confirmed 0.10 claim, it is a full-criterion win rather than a partial one, and it is one cell, one metric, one object.

## Notes for the main session (not criterion defects)
- Rule 12 hygiene: several package files contain absolute machine paths that include a user name. These are the tools' path constants, the command line in rules/null_test.md, the sealed logs, combiner_fit.json entry_dirs and scout/. Strip them before publication.
- My check confirms what the frozen systems read and the selection hashes. The lenses' own conduct (development limited to val-0.50, training-0.50 and dev) rests on the package's records. Earlier runs' test-0.20 exposure in the main session's history is a process caveat, not a data-access breach of the criterion.

confirmed_scope: At proportion 0.20, the frozen stage-2 combiner predictions combiner/test/0.20 (six component systems trained only on the 10 surprise families' training-0.20.tsv files, each masked test-0.20.tsv row predicted in isolation, combiner weights fit on a validation split cut from training-0.20) reach mean NED 0.20345235544710852 over the 10 surprise families under the pinned ST2022 scorer (left-to-right and compensated summation), strictly below Mockingbird-I1's official results-surprise-0.20.json mean NED 0.2648052468982754 (FeVeT published no value at 0.20), a win on mean NED at 0.20 only.

pass: true
