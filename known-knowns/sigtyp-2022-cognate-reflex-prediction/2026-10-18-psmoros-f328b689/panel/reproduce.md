(Saved by the main session from the subagent's returned text, 2026-10-18T07:16:36Z: round-2 REPRODUCE skeptic for cell C10 (Opus 5.5, Agent tool), on the round-2 claim package. The same skeptic re-issued its text at the main session's request with angle-bracket tokens written without brackets, for the kit's placeholder check; the main session verified with a line diff that it is identical to the skeptic's first text apart from those tokens. Verbatim below.)

# Panel: REPRODUCE skeptic, cell C10 (proportion 0.10, mean NED), round 2

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
start (date -u): Sun Oct 18 06:12:45 UTC 2026
end (date -u): Sun Oct 18 07:00:23 UTC 2026

Material: only the claim package (paths below are relative to claim/) and the kit rules (kit/RULES.md). I read
nothing else in the workspace. I made no network requests (no URL was fetched, so nothing went on the stop list).
Interpreters: SYS (Python 3.13.2; lingpy 2.6.13, lingrex 1.4.2, numpy 2.5.4, torch 2.14.1) for the component
systems; SCO (Python 3.13.2; lingpy 2.6.9, lingrex 1.2.0, its installed sigtypst2022.py has the same sha256 as
official/src/sigtypst2022.py: 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a) for scoring;
python3.13 for my own helpers. All my scratch files are in my own folder outside claim/.

## 0. Definition used (quoted)
definition/Q15.json success_criterion: "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never
reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion [...] strictly beats
Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: a lower mean NED [...] The repo
scorer `st2022` at a pinned commit computes the score."
verification_method: "Skeptic reproduces a train->predict run (or audits the code) confirming it consumes ONLY
training-*.tsv + masked test-*.tsv [...] then runs `st2022` at the pinned commit and compares to
results-surprise-*.json."
Statistic: official/src/sigtypst2022.py compare_words(solutions-0.10.tsv, result-0.10.tsv, report=False)[-1][1:]
per family = [ED, NED, BCFS, BLEU]; system score = statistics.mean over the 10 families (as compare_systems does).
Cell bar (from my instructions and rules/PREREG.md): this workspace's own confirmed 0.10 system, 0.19710919181751296
(predictions in bar_holder/). PREREG rule 12 (i): NED lower than the bar by more than 1e-9 in both summation modes;
(iv): the REPRODUCE retrain-and-predict run reproduces the frozen predictions (or, if not bit-deterministic, a NED
that also meets (i)).

## 1. Own scorer, written before reading any author code (myscore.py in my folder)
It loads official/src/sigtypst2022.py by file path and calls compare_words per family, then statistics.mean. Mode
"ltr" sets `sum` in the sigtypst2022 and lingrex.util module namespaces to a plain left-to-right loop; mode "builtin"
leaves Python's builtin sum (compensated in 3.12+).

Check on Mockingbird-I1 (official/systems/mockingbird-i1/surprise/FAM/result-0.10.tsv vs the "Mockingbird-I1" entry
of official/results/results-surprise-0.10.json, every per-family 4-tuple and the total compared with ==):
    ltr:     MEAN 0.9200532775139207 0.2431316340782435 0.7672735092897016 0.6633184488563897
             BITIDENTICAL_TO_JSON Mockingbird-I1 yes []
    builtin: MEAN 0.9200532775139207 0.2431316340782435 0.7672735092897016 0.6633184488563898
             BITIDENTICAL_TO_JSON Mockingbird-I1 no [all 10 families, 'total'] (last-digit differences; NED total equal)
So "ltr" is the bit-exact official statistic.

## 2. The claimed object and the bar, rescored
combiner/test/0.10 (claimed), per family [ED, NED, BCFS, BLEU], ltr:
    bantubvd 0.7402049361928393 0.17980609723953056 0.8580042434416036 0.7206173956038519
    beidazihui 0.3734817813765182 0.10360998650472335 0.881281633630246 0.8443044195638618
    birchallchapacuran 1.2517737358101135 0.24823992425917737 0.7088064886190432 0.636593726042752
    bodtkhobwa 0.22826086956521735 0.09827898550724638 0.8814663881703196 0.8665887368228914
    bremerberta 0.875 0.16151785714285713 0.8235998410564258 0.7377776325510611
    deepadungpalaung 0.334375 0.12604166666666666 0.9386805111826346 0.8211116308267665
    hillburmish 0.8521563149222723 0.2306819829021494 0.7435695509404412 0.6900228689062105
    kesslersignificance 2.055910364145658 0.5580564892623717 0.5770048224862526 0.30385017701016126
    luangthongkumkaren 0.24342105263157893 0.06650219298245613 0.9341393426506079 0.8961145831052693
    wangbai 0.403030303030303 0.11888888888888886 0.8579769910530114 0.8222349458325302
    MEAN ltr     0.73576143576745 0.18916240713560675 0.8204529813230585 0.7339216116265356
    MEAN builtin 0.7357614357674501 0.18916240713560675 0.8204529813230585 0.7339216116265356
No "Missing entry" line was printed (every gold item has a prediction).
Claimed: NED 0.18916240713560675 (both modes), ED 0.73576143576745, BCFS 0.8204529813230585, BLEU
0.7339216116265356: all reproduced exactly.

Bar, bar_holder/r1806-combiner/test/0.10:
    MEAN ltr     0.7681031861535738 0.19710919181751296 0.8160580391288506 0.7211197226355787
    MEAN builtin 0.7681031861535739 0.19710919181751294 0.8160580391288506 0.7211197226355787
Bar NED 0.19710919181751296 (claimed) reproduced in ltr mode.
Margins (python3.13): bar - candidate = 0.00794678468190621 (ltr), 0.007946784681906183 (builtin); both > 1e-9 (True).
Mockingbird-I1 - candidate = 0.053969226942636755; FeVeT - candidate = 0.040530170661474046.
FeVeT (fevet/pred_0.10_FAM.tsv, long format, converted by my own script to the official wide format with the
test-0.10 header): MEAN ltr 0.9045536873465417 0.2296925777970808 0.7814883090261855 0.6833751184272755, 0 missing
entries; equals the claim table.

## 3. Integrity of the saved objects
- MANIFEST.sha256: 385 lines; `shasum -a 256 -c`: 0 lines not OK; files on disk not in the manifest: only
  MANIFEST.sha256 itself; files in the manifest missing on disk: none. (My first scorer run wrote a
  official/src/__pycache__/*.pyc into claim/; I deleted it at once and used -B afterwards; a re-run of the check at the
  end again gives 0 not OK and no extra file.)
- FROZEN.md (own parser, frozencheck.py; section matching each entry's ROLE): for all 7 entries every code file listed
  equals the shipped code/ folder (no extra, no missing, all sha256 match), every shipped result file (test/0.10, val/0.10)
  matches its FROZEN.md line, all 10 test/0.10 files present; the only unlisted shipped files are the audit logs
  (test/0.x/audit/audit.log). Output: "FROZEN_CHECK PASS". Freeze stamps: r1806-smuggler/PRIMARY 2026-10-17T21:10:10Z,
  r1806-correspondence/PRIMARY 2026-10-17T21:14:15Z, analogist/SECONDARY 2026-10-18T03:23:18Z, classifier/PRIMARY
  2026-10-18T04:03:30Z, broker/PRIMARY 2026-10-18T03:14:07Z, correspondence/PRIMARY 2026-10-18T03:40:38Z,
  phylo/PRIMARY 2026-10-18T03:19:07Z.
- data/view: holds exactly 20 training-0.10.tsv and 20 test-0.10.tsv (10 surprise + 10 dev families), no other file;
  the 20 surprise files are byte-identical to official/data-surprise/FAM/{training,test}-0.10.tsv (20/20 same).
- shared/val/0.10 rebuilt by my own script with the official split_training_test_data(ratio=0.15) and
  write_cognate_file from training-0.10: "30/30 files byte-identical; cognate-set IDs shared between training-0.10
  and test-0.10: 0" (validation data is disjoint from the test sets by construction).

## 4. Retrain and re-predict every stage-2 entry (PREREG rule 12 iv)
Setup: a fresh folder of mine containing ONLY a copy of tools/q15h.py, a copy of data/view (the 40 files above) and a
copy of each entry's frozen code/ (diff -r against the frozen code: identical for 6 entries; for
r1806-correspondence/PRIMARY the only change is code/system.py line 16, HOME pointed to a folder of mine, as
REPRODUCE.md section 3 instructs; I pre-warmed that folder's lingpy 2.6.13 cache with one import, as REPRODUCE.md
recommends). Because q15h.py derives its root from its own location, every training manifest pointed into that folder
only: each manifest lists 10 files ROOT/data/view/surprise/FAM/training-0.10.tsv plus dev_dir ROOT/data/view/dev;
no solutions, cognates, wordlist, val or other-proportion file existed under that root.
Command per entry: OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 SYS -I -B tools/q15h.py run --code COPY --mode test
--out FRESH/ENTRY --props 0.10 --workers 1 or 2, under perl alarm and nice 5. The machine was heavily loaded by
other processes (load average up to 172 on 12 cores).
Harness train lines (run 1): r1806-correspondence 19s, r1806-smuggler 56s, phylo 12s, analogist 109s, classifier 471s,
broker 178s, correspondence 327s; every family "ok", every train rc=0.
Then cmp of each re-predicted test/0.10/FAM/result-0.10.tsv with attempts/LENS/frozen/ROLE/test/0.10/FAM/result-0.10.tsv:
    CMP r1806-smuggler_PRIMARY vs frozen: 10/10 byte-identical
    CMP r1806-correspondence_PRIMARY vs frozen: 10/10 byte-identical
    CMP analogist_SECONDARY vs frozen: 10/10 byte-identical
    CMP classifier_PRIMARY vs frozen: 10/10 byte-identical
    CMP broker_PRIMARY vs frozen: 10/10 byte-identical
    CMP correspondence_PRIMARY vs frozen: 10/10 byte-identical
    CMP phylo_PRIMARY vs frozen: 10/10 byte-identical
Second, independent retrain of all 7 (run 2, in another fresh folder, --workers 1, system.py run under a Python audit
hook that logs every file open): all 7 x 10 result files byte-identical to run 1 (so also to the frozen files).
Training is bit-deterministic for every entry on this machine; PREREG rule 12 (iv) holds in its first case
(predictions reproduced byte for byte) for all 7 entries, including weight-0 correspondence/PRIMARY.

## 5. Stage-2 combination recomputed
Own implementation (mystage2.py, written from the rule as stated in CLAIM.md and tools/stage2.py's docstring, not
from its code): per item, output c_i with i = argmin_i sum_j w_j * NED(c_j -> c_i) + 1e-7*(3 - w_i) + 1e-9*i, NED with
c_j in the gold slot (nw_align from the pinned scorer's namespace; empty prediction -> 2*len 'Ø'; empty pseudo-gold
contributes 0), weights 3,3,1,2,1,0,1 from combiner/combiner_fit.json "0.10" "weights_all10" in combiner/entries.json order.
- on the FROZEN component predictions: 10/10 files byte-identical to combiner/test/0.10;
  "items 4029 argmin-index counts [3451, 494, 21, 45, 11, 4, 3]";
  "items whose chosen string is produced only by weight-0 entries: [('hillburmish', '93-3', [5]), ('hillburmish',
  '477-9', [5]), ('kesslersignificance', '560-1', [5]), ('kesslersignificance', '1222-4', [5])]" (index 5 =
  correspondence/PRIMARY): exactly the 4 items CLAIM.md lists.
- on MY RETRAINED component predictions (run 1): "own stage-2 on RETRAINED component predictions vs
  combiner/test/0.10: 10/10 byte-identical"; rescored: ltr MEAN 0.73576143576745 0.18916240713560675
  0.8204529813230585 0.7339216116265356; builtin NED 0.18916240713560675.
- weight refit with the author's tools/stage2.py (SCO, STUB_MPL=1, --props 0.10 --procs 1 --verify-reference, entries
  = combiner/entries.json, gold-map = shared/val, out = my folder): "verify-reference (combine.py per-tuple loop): F
  bit-identical True; tuple-family pairs with different item choices 0"; "weights(all 10) [3, 3, 1, 2, 1, 0, 1]
  in-sample 0.207294 LOFO 0.211310"; its test/0.10 output 10/10 and val/0.10 output 10/10 byte-identical to
  combiner/test/0.10 and combiner/val/0.10; weights_all10, insample_mean_all10, lofo_val_mean, lofo_weights,
  single_entry_val_mean, entries, lofo_val_scorer_total all equal (==) to combiner/combiner_fit.json.

## 6. Data access and row isolation
- Static read of the 7 entries' code (grep for solution/cognates/wordlist/data-surprise/official/glob/listdir/os.walk/
  scandir/urlopen/socket/subprocess/absolute paths/other proportions, and every open()/json.load/pickle.load call
  site): train reads only man["surprise_train"][fam] (and, for correspondence/PRIMARY only, man["dev_dir"]/DEV
  FAM/training-0.10.tsv and test-0.10.tsv); predict reads only --model-dir and the --jobs partition files. The only
  absolute path in any code is r1806-correspondence's HOME line.
- Dynamic trace (run 2; audit hook on "open"; my summariser flags any path matching solution|cognates|wordlist|
  data-surprise|official|-0.[2-5]0.tsv|/val/|/claim/): flagged paths = 0 for all 7 entries. Files opened besides
  code/config/model files and the harness manifest: surprise training-0.10.tsv (10 per entry; 20 opens for
  correspondence), part-NN.tsv (99 per entry) and, for correspondence/PRIMARY only, dev/FAM/training-0.10.tsv (10)
  and dev/FAM/test-0.10.tsv (10, masked dev files listed in the manifest). Limit: processes spawned by
  multiprocessing pools (r1806-correspondence and classifier training) are not traced; for them the static read and
  the folder isolation (nothing else readable under the harness root) apply.
- Harness audit, tools/q15h.py audit --mode test --props 0.10 on my run-1 output, every entry: 40 identical, 0
  FAIL/MISMATCH, "AUDIT PASS" (r1806-smuggler, r1806-correspondence, analogist, phylo, classifier, broker,
  correspondence).
- Own isolation check (partcheck.sh): every test-0.10 partition (99 per entry, one masked language each, at most one
  row per cognate set) predicted alone in its own fresh process from my retrained model and compared byte for byte
  with the merged run's partition output:
    PARTCHECK r1806-smuggler_PRIMARY: 99/99 partitions byte-identical when predicted alone
    PARTCHECK analogist_SECONDARY: 99/99
    PARTCHECK broker_PRIMARY: 99/99
    PARTCHECK classifier_PRIMARY: 99/99
    PARTCHECK r1806-correspondence_PRIMARY: 99/99
    PARTCHECK correspondence_PRIMARY: 99/99
    PARTCHECK phylo_PRIMARY: 99/99 (922s)
- Own null test (mynull.py, from REPRODUCE.md section 5's description, 400 controls, Random(20261018 + c)):
  "real: cand NED 0.18916240713560675 bar NED 0.19710919181751296 d 0.00794678468190621"; "controls 400 max control d
  0.005948936672339172 controls with d >= real: 0 real_beats_all_controls yes" (equals rules/null_test.md / CLAIM.md).

## 7. Reproduction table (test-0.10; NED = mean NED of my retrained predictions, official scorer, ltr summation)
| entry | weight | retrained vs frozen test-0.10 | determinism | recomputed NED | harness audit | own 99-partition check |
|---|---|---|---|---|---|---|
| r1806-smuggler/PRIMARY | 3 | 10/10 bit-identical | 2 retrains identical | 0.2065798750856504 | PASS 40/40 | 99/99 |
| r1806-correspondence/PRIMARY | 3 | 10/10 bit-identical | 2 retrains identical | 0.20065194617897522 | PASS 40/40 | 99/99 |
| analogist/SECONDARY | 1 | 10/10 bit-identical | 2 retrains identical | 0.20460403212077688 | PASS 40/40 | 99/99 |
| classifier/PRIMARY | 2 | 10/10 bit-identical | 2 retrains identical | 0.2061706513594121 | PASS 40/40 | 99/99 |
| broker/PRIMARY | 1 | 10/10 bit-identical | 2 retrains identical | 0.19836914089048766 | PASS 40/40 | 99/99 |
| correspondence/PRIMARY | 0 | 10/10 bit-identical | 2 retrains identical | 0.20546744883430543 | PASS 40/40 | 99/99 |
| phylo/PRIMARY | 1 | 10/10 bit-identical | 2 retrains identical | 0.20809801282747903 | PASS 40/40 | 99/99 |
| combiner (stage-2 MBR, own code) | - | 10/10 bit-identical to combiner/test/0.10 (from frozen and from retrained inputs) | deterministic | 0.18916240713560675 (ltr and builtin) | row-local by construction | - |

## 8. Observations (do not change the verdict)
- Publication hygiene (kit rule 12): combiner/combiner_fit.json ("entry_dirs"), tools/q15h.py (DEFAULT_PY,
  SCORER_PY), attempts/r1806-correspondence/frozen/PRIMARY/code/system.py line 16 and several component REPRODUCE.md
  files contain absolute local paths that include the local user name. Strip them before anything is published.
- classifier/PRIMARY prints scikit-learn lbfgs ConvergenceWarnings during training; the output is still
  bit-deterministic (two retrains plus the frozen files identical).
- The bar comparison is against this workspace's own earlier system (cell C10's bar); Mockingbird-I1 (0.2431316340782435)
  and FeVeT (0.2296925777970808) are also beaten, by 0.0540 and 0.0405 NED.

## Verdict
Every check passed: the claimed value 0.18916240713560675 (both summation modes) and the bar 0.19710919181751296 are
reproduced by my own scorer, which is bit-exact on Mockingbird-I1; all 7 stage-2 entries (weight 0 included) retrain
from their frozen code on training-0.10 + dev view only and re-predict test-0.10 byte for byte, deterministically;
my own MBR implementation reproduces combiner/test/0.10 byte for byte from both the frozen and the retrained component
predictions; the weights refit to [3, 3, 1, 2, 1, 0, 1]; no component read solutions, cognates, wordlist, val or
other-proportion files; rows are predicted in isolation (harness audit and my own per-partition check).
Label: NUMERICAL, reproduced here by rerun (PROVED-HERE for the byte identities). Scope confirmed: at proportion 0.10, combiner/test/0.10 has mean NED 0.18916240713560675 on the 10 surprise families
under the pinned official scorer, lower than the C10 bar 0.19710919181751296 by 0.00794678468190621 (ltr) /
0.007946784681906183 (builtin).
pass: true
