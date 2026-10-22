(Saved by the main session from the subagent's returned text, 2026-10-18T07:15:51Z: round-2 REPRODUCE skeptic for cell C20 (Opus 5.5, Agent tool), on the round-2 claim package. The same skeptic re-issued its text at the main session's request with angle-bracket tokens written without brackets, for the kit's placeholder check; the main session verified mechanically that it is identical to the skeptic's first text apart from those tokens. Verbatim below.)

# Panel file: REPRODUCE skeptic, cell C20 (proportion 0.20, mean NED), round 2

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
start: Sun Oct 18 06:12:43 UTC 2026 (date -u)
end: Sun Oct 18 06:56:05 UTC 2026 (date -u)

Material I read: the claim copy (claim/) only, plus kit/RULES.md and TROPHY_CASE.md. I read nothing else in the workspace. All scratch work is in my own folder, outside claim/. I made no web requests. The only network attempt was one loopback connection, made inside my sandbox profile to confirm that the sandbox blocks network access (curl returned 000, no HTTP status). I appended nothing to the stop list. File names below are relative to claim/; "mine/…", "retrain/…" and "sbx/…" are files in my scratch folder.

## 0. Definition (quoted)
definition/Q15.json success_criterion: "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED, or a higher mean BCFS, or a higher mean BLEU. Report all three; a win on one metric is a win on that metric only. The repo scorer `st2022` at a pinned commit computes the score."

How the statistic is computed, from official/src/sigtypst2022.py (sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a):
- Per family: `compare_words(solutions, result, report=False)[-1][1:]` gives [ED, NED, BCFS, BLEU].
- System score: `compare_systems` takes `statistics.mean([row[i] for row in totals])` over the 10 families.

## 1. My own scorer, written before reading any of the author's tools (mine/myscore.py, SCO interpreter)
- The script imports official/src/sigtypst2022.py directly. It asserts the module path and prints the module's sha256.
- Mode `ltr`: replaces `sum` in the `sigtypst2022` and `lingrex.util` namespaces with a plain left-to-right loop.
- Mode `builtin`: uses Python 3.13's builtin `sum`.

Calibration on official/systems/mockingbird-i1/surprise/FAM/result-0.20.tsv against the "Mockingbird-I1" entry of official/results/results-surprise-0.20.json:
```
mode ltr:     MEAN ED 1.0413225298738344 NED 0.2648052468982754 BCFS 0.7119659170836019 BLEU 0.632633947442519
REFERENCE total [1.0413225298738344, 0.2648052468982754, 0.7119659170836019, 0.632633947442519]
BIT_IDENTICAL_TO_REFERENCE True mismatching per-family numbers: 0
mode builtin: MEAN ED 1.0413225298738344 NED 0.2648052468982754 BCFS 0.7119659170836019 BLEU 0.632633947442519
BIT_IDENTICAL_TO_REFERENCE False mismatching per-family numbers: 18
```
- In ltr mode all 40 per-family numbers and all 4 totals are bit-identical to the official file.
- In builtin mode the totals are identical but 18 per-family values differ in the last bits.

Bar recomputed from Mockingbird-I1's per-item files: mean NED 0.2648052468982754 in both modes. This equals the cell's bar.

## 2. The claimed object, combiner/test/0.20
```
mode ltr:     MEAN ED 0.7979822478300038 NED 0.20345235544710852 BCFS 0.7780895356732769 BLEU 0.7080911153196365
mode builtin: MEAN ED 0.7979822478300038 NED 0.20345235544710852 BCFS 0.7780895356732768 BLEU 0.7080911153196366
ltr d 0.061352891451166874 True      (bar - candidate > 1e-9)
builtin d 0.061352891451166874 True
```
- These equal CLAIM.md's ED, NED, BCFS and BLEU (ltr values) and its NED in both modes.
- Per-family NED (ltr), candidate vs Mockingbird-I1:

| family | candidate | Mockingbird-I1 |
|---|---|---|
| bantubvd | 0.20290090482487494 | 0.28562860698615367 |
| beidazihui | 0.10519568151147099 | 0.12872807017543858 |
| birchallchapacuran | 0.2693367676777757 | 0.36094267567545335 |
| bodtkhobwa | 0.10467896174863388 | 0.15171903460837888 |
| bremerberta | 0.19284262485481996 | 0.2068815331010453 |
| deepadungpalaung | 0.1485309829059829 | 0.2821314102564103 |
| hillburmish | 0.22187675834594495 | 0.2717668988020789 |
| kesslersignificance | 0.5568035825962655 | 0.6573442181125108 |
| luangthongkumkaren | 0.08456688596491228 | 0.11546052631578949 |
| wangbai | 0.14779040404040403 | 0.18744949494949487 |

- No "Missing entry" lines were printed.
- 7887 items were scored, which equals the total row count of the 10 test-0.20 files.

## 3. Integrity of the saved files
- **MANIFEST.sha256:** `shasum -a 256 -c` gives 322 OK, 0 failures. Every file in claim/ is listed (only MANIFEST.sha256 itself is not). I re-ran this check at the end, after cleaning up (see section 8): 322 OK, no extra files.
- **FROZEN.md lines (mine/checkfrozen.py):** for every entry, every present file matches its line.
  - broker/PRIMARY: ok 21, mismatch 0
  - analogist/SECONDARY: ok 22, mismatch 0
  - broker/SECONDARY: ok 21, mismatch 0
  - phylo/PRIMARY: ok 21, mismatch 0
  - analogist/PRIMARY: ok 22, mismatch 0
  - classifier/PRIMARY: ok 22, mismatch 0
  - The counts cover the code files, all 10 test/0.20 files and all 10 val/0.20 files. The 50 "missing" lines per entry are the 0.10, 0.30 and 0.50 results, which are not shipped in this 0.20 package.
- **Code tree hashes:** recomputed with the freeze's tree formula, all 6 MATCH (e.g. broker/PRIMARY e0e12da3febeabfd…, phylo/PRIMARY 44443f3fa1ff9988…). The code folders hold no unlisted files.
- **selection.md:** the sha256 of each of the 4 FROZEN.md files equals selection.md's freeze records. The 10 combiner/test/0.20 files pass `shasum -c` against selection.md's "out/comb_new/test/0.20" hashes. combiner/combiner_fit.json has sha256 9cc0d8a7…, as recorded.
- **Data view:** data/view/surprise/FAM/{training,test}-0.20.tsv are byte-identical (cmp) to official/data-surprise. data/view holds no solutions file and no other-proportion surprise file. Training and test cognate sets are disjoint in all 10 families (overlap 0).
- **Validation split:** rebuilt from training-0.20 with the official `split_training_test_data(ratio=0.15)`, 30 of 30 shared/val/0.20 files are identical.

## 4. Retraining every stage-2 entry (PREREG rule 12 iv)
Command, once per entry, in an empty folder retrain/LENS/ROLE:
```
env -i PATH=/usr/bin:/bin HOME=MINE OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 \
  SYS -I -B tools/q15h.py run --code attempts/LENS/frozen/ROLE/code --mode test --out NEW --props 0.20 --workers 1|2
```
- The harness manifest lists only data/view/surprise/FAM/training-0.20.tsv for the 10 families, plus data/view/dev.
- `env -i` keeps BRK_DEV and CLS_OPTS unset.
- The harness reported "train rc=0" for every entry and "ok N rows" for all 10 families. Train times: broker/PRIMARY 70 s, classifier 372 s, phylo 10 s, broker/SECONDARY 162 s.

cmp of each re-predicted test-0.20 file against the frozen one (mine/cmpentry.sh):
```
broker/PRIMARY: 10 of 10 test-0.20 result files byte-identical to frozen
classifier/PRIMARY: 10 of 10 test-0.20 result files byte-identical to frozen
analogist/SECONDARY: 10 of 10 test-0.20 result files byte-identical to frozen
analogist/PRIMARY: 10 of 10 test-0.20 result files byte-identical to frozen
broker/SECONDARY: 10 of 10 test-0.20 result files byte-identical to frozen
phylo/PRIMARY: 10 of 10 test-0.20 result files byte-identical to frozen
```
All 6 entries are bit-deterministic and reproduce byte for byte. That is the strict case of rule 12 (iv) for every component, so the 1e-9 fallback was never needed.

## 5. Stage-2 combination
**My own implementation (mine/mystage2.py).** I wrote it from the per-item MBR rule in tools/stage2.py's docstring only:
- For each item: argmin over i of sum_j w_j·NED(c_j→c_i), using the scorer's per-item NED via `sigtypst2022.nw_align`. An empty pseudo-gold row counts as 0.
- Tie rule: +1e-7·(3−w_i) + 1e-9·i.
- It also runs an exact Fraction/lexicographic variant for comparison.
- Weights are [2,3,2,1,0,3] in entries.json order.

From the frozen component predictions:
```
items 7887 float-vs-exact differing choices 0
items whose chosen string is produced only by weight-0 entries: 1 [('kesslersignificance', '1222-2', [4])]
identical bantubvd … identical wangbai   (10 of 10 byte-identical to combiner/test/0.20)
```
From MY RETRAINED component predictions:
```
combiner from RETRAINED components (my MBR): 10 of 10 files byte-identical to combiner/test/0.20
mycomb_retrained MEAN ED 0.7979822478300038 NED 0.20345235544710852 BCFS 0.7780895356732769 BLEU 0.7080911153196365
```
This also confirms CLAIM.md's statement that exactly one item (kesslersignificance 1222-2) is chosen from a string only the weight-0 entry analogist/PRIMARY produced.

**Weight refit.** I re-ran tools/stage2.py over the 6 entries (my own copy of entries.json with absolute paths), with gold map shared/val, `--props 0.20`:
```
0.20 weights(all 10) [2, 3, 2, 1, 0, 3] in-sample 0.228854 LOFO 0.234296
0.20 LOFO val mean (combine.py value) 0.23429616596915276; official compare_words on the written val files: NED 0.2342961659691527 …
test+val identical bantubvd … test+val identical wangbai   (all 10 test and all 10 LOFO-val files byte-identical to combiner/test and combiner/val)
```
My own scorer on combiner/val/0.20 against shared/val/0.20 gold gives NED 0.2342961659691527, ED 1.002959544666826, BCFS 0.7869639560388485, BLEU 0.6735923893677556. These equal combiner_fit.json's lofo_val_scorer_total.

## 6. Data access and row isolation
**Code audit.** I grepped all 6 system.py files for every open() and every other file-reading call. Each component reads only:
- the manifest's `surprise_train[fam]` (training-0.20);
- its own config.json;
- the model dir;
- the jobs file and the partition files it names.

None reads dev_dir, and no code path reads solutions, cognates, wordlist or other-proportion files. Prediction builds fresh per-row state ("fresh per row" scorers or Sim objects). The only module-level caches are pure functions of segment symbols (`_bc`, `_sc`, sound-class tables).

**Sandboxed retrain (mine/deny.sb, macOS sandbox-exec).** The sandbox made the following unreadable:
- every path under the workspace containing solutions, cognates or wordlist;
- data/view/surprise/*/test-*;
- every *-0.10/0.30/0.40/0.50 .tsv in the workspace (including the dev files, so this is stricter than PREREG);
- official/, shared/, combiner/, fevet/, scout/, rules/;
- all frozen test/ and val/ outputs, and runs/;
- the network.

Training under it, then comparison with the harness-trained models:
- broker/PRIMARY: 10 of 10 model files byte-identical.
- broker/SECONDARY: 10 of 10 byte-identical.
- classifier/PRIMARY: 11 of 11 byte-identical.
- phylo/PRIMARY: 1 of 1 byte-identical.
- analogist/PRIMARY and analogist/SECONDARY: the pickles differ in bytes (set/dict order, because the hash seed differs between processes), but "pickles equal as objects (dict/set order ignored, floats by repr): 10 of 10" for each.

One earlier sandboxed classifier attempt failed only because my working directory sat inside a denied folder (`os.getcwd()` raised PermissionError in multiprocessing spawn). It was rerun from an allowed directory and passed as above.

**Each partition alone, in its own fresh process, under the sandbox** (mine/isolate.py, 99 processes per entry, using the sandbox-trained models):
```
ISOLATION (sandboxed) alone analogist/PRIMARY:   rows identical 7887, differing 0, processes 99, failed 0 -> PASS
ISOLATION (sandboxed) alone analogist/SECONDARY: rows identical 7887, differing 0, processes 99, failed 0 -> PASS
ISOLATION (sandboxed) alone classifier/PRIMARY:  rows identical 7887, differing 0, processes 99, failed 0 -> PASS
ISOLATION (sandboxed) alone broker/PRIMARY:      rows identical 7887, differing 0, processes 99, failed 0 -> PASS
ISOLATION (sandboxed) alone broker/SECONDARY:    rows identical 7887, differing 0, processes 99, failed 0 -> PASS
ISOLATION (sandboxed) alone phylo/PRIMARY:       rows identical 7887, differing 0, processes 99, failed 0 -> PASS
```
Before that, unsandboxed runs of the same test also gave PASS (7887/7887) for broker/PRIMARY and classifier/PRIMARY.

**Order test.** One sandboxed process per family, with partitions in reverse order and rows reversed inside each partition: all 6 entries PASS, "rows identical 7887, differing 0, processes 10" each. Each line was compared byte for byte with the frozen merged line for its COGID.

The saved audit files (audit_test*.txt) show 40 identical and 0 FAIL at 0.20 for every entry, ending "AUDIT PASS".

## 7. Null test, my own implementation (mine/mynull.py, from rules/null_test.md text)
```
unswapped: candidate NED 0.20345235544710852  bar NED 0.2648052468982754  real d 0.061352891451166874
controls 400 max d 0.01732600288224881 mean 0.00030137828913791466 sd 0.005775232913398775; controls >= real: 0; real_beats_all_controls: yes
```
- max d and the mean equal rules/null_test.md bit for bit.
- The sd differs only because I used the sample sd and the file uses the population sd: 0.005775232913 × sqrt(399/400) = 0.0057680.

## 8. Notes (none of these is a reproduction failure)
- **Files my runs created in the claim copy, all removed:**
  - My first scorer import wrote official/src/__pycache__/sigtypst2022.cpython-313.pyc. I removed it and used -B from then on.
  - phylo/PRIMARY's code sets HOME to its frozen/PRIMARY/home folder, and lingpy wrote a cache there (Library/Caches/lingpy/2.6.13/*.pkl) during my runs. This is a write outside the harness output dir, but it is harmless (lingpy symbol tables only). I removed it.
  - After cleanup, MANIFEST.sha256 checks 322/322 and claim/ holds no files beyond the manifest.
- **The "rc=…" lines in my chain logs mean nothing.** Bash expanded `$(date)` before `$?`. I judged every step by its output files and by the harness's own "train rc" and "ok N rows" lines.
- **Publication hygiene (kit rule 12), for the main session:** several package files contain absolute home-directory paths that include the account name. These are combiner/combiner_fit.json ("entry_dirs", 18 lines), attempts/*/frozen/*/REPRODUCE.md, attempts/*/frozen/*/test/*/audit/audit.log, rules/null_test.md, rules/sealed*_check_0.20.log, scout/scout.md and tools/null_test.py. Scrub them before anything is published. This does not affect reproduction.
- **Scorer pin:** I cannot confirm the pinned commit without the web, which this panel forbids. What I can say is that the shipped scorer reproduces the official 2022 results file bit for bit.

## Table of what was reproduced (test-0.20; NED is mean NED with ltr summation, recomputed by my scorer from my retrained files)

| object | weight | retrained via harness: test-0.20 files byte-identical | sandboxed retrain: model | sandboxed each-partition-alone / reversed order | recomputed NED | beats bar 0.2648052468982754 by >1e-9 |
|---|---|---|---|---|---|---|
| broker/PRIMARY | 2 | 10/10, bit-deterministic | 10/10 bytes | 7887/7887 / 7887/7887 | 0.21549423637349877 | yes |
| analogist/SECONDARY | 3 | 10/10, bit-deterministic | 10/10 object-equal | 7887/7887 / 7887/7887 | 0.21229071804613978 | yes |
| broker/SECONDARY | 2 | 10/10, bit-deterministic | 10/10 bytes | 7887/7887 / 7887/7887 | 0.2214642934147208 | yes |
| phylo/PRIMARY | 1 | 10/10, bit-deterministic | 1/1 bytes | 7887/7887 / 7887/7887 | 0.2219895459418176 | yes |
| analogist/PRIMARY | 0 | 10/10, bit-deterministic | 10/10 object-equal | 7887/7887 / 7887/7887 | 0.22562186548790167 | yes |
| classifier/PRIMARY | 3 | 10/10, bit-deterministic | 11/11 bytes | 7887/7887 / 7887/7887 | 0.21945044930968327 | yes |
| combiner (my MBR over frozen, and over retrained, predictions; plus tools/stage2.py refit) | [2,3,2,1,0,3] reproduced | 10/10 byte-identical to combiner/test/0.20 (all three routes) | n/a | row isolation holds by construction (per-item rule) | 0.20345235544710852 (builtin sum: 0.20345235544710852) | yes, d = 0.061352891451166874 |

Verdict: everything I checked reproduces. The claimed value, the bar, every component's re-prediction (bit for bit), the stage-2 combination (bit for bit, by my own implementation and by refitting), the data-access restrictions (code audit plus sandboxed retrain) and row isolation all hold. I found no mismatch, no missing object and no non-determinism.

pass: true
