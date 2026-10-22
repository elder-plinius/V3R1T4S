# PROVENANCE_WINDOWS: A(25,6,11) M = 8,734 (TXT f9f28061..., NPY d9a093d6...)

Written 2026-10-19 (about 11:58-12:16Z) by the Windows packaging specialist, from existing files only. Paths are
relative to the workspace `constant-weight-codes/` (W) or to the delivery worktree (`worktrees/selection`, branch
`windows/selection-20261017`, D). Personal paths are redacted as `<user Python312>` / `<tess-pilot venv>`.
No checker, engine or test was run for this note; the only Python executions are the version prints of section 1c.

Scope note: this folder also holds files of a fuller package started before the coordinator's scope change of 11:55Z
(README, object/, verify-it-yourself/, how-we-built-it/, the-record-we-beat/, LICENSING.md, LICENSE*). That package
is INCOMPLETE and UNVERIFIED: its run_checks.sh was never executed, it has no RECEIPTS.md and no PACKAGE_SHA256.
Nothing was added to it after 11:55Z except this file. It is not a deliverable; ignore or delete it.

## 1. Effective interpreter and package versions

### 1a. Which interpreter ran what (from logs and code)
| process | interpreter, as recorded | source |
|---|---|---|
| Stage K engine `lb_lns_gen.py` (all six jobs), wrapper `j7_run.py`, its snapshot checkers and `post_check.py` | the pte-eval supervisor's `{PY}` = the venv's BASE interpreter `<user Python312>\python.exe` (logged as `python=` in the supervisor start line), started with `PYTHONPATH=<tess-pilot venv>\Lib\site-packages` and `VIRTUAL_ENV=<tess-pilot venv>`; the wrapper starts the engine and both checkers with its own `sys.executable` and the inherited environment, so all of them ran under that same base interpreter + venv site-packages | W `runs/2026-10-19-0955-k-a25-6-11-seeds/supervisor.log` line 1; `.../attempts/seeds/code/launch_K.sh` (`--venv .../tess-pilot/.venv-tess312`); pte-eval `tools/supervise.py` `base_python()` and `launch()` (PYTHONPATH=site); `j7_run.py` (`sys.executable`, `CHK_ENV = dict(os.environ, ...)`) |
| Stages F, G, H engine + wrappers + checkers | same supervisor, same `python=` line, same `--venv` | `runs/2026-10-19-0037-f-a25-6-11/supervisor.log`, `runs/2026-10-19-0223-g-.../supervisor.log`, `runs/2026-10-19-0307-h-.../supervisor.log` |
| Stage K owner recheck (10:45:22-10:45:32Z) | NOT recorded (no driver script saved; only `recheck.log`) | `runs/2026-10-19-0955-k-.../attempts/owner_recheck/report.md` |
| Package r2 `run_checks.sh` (the 8,732 checkers, 08:55Z) | the venv launcher `<tess-pilot venv>\Scripts\python.exe` | `runs/2026-10-19-0755-i-a25-6-11-evidence/lenses/package-r2/LOG.md` (08:55:31Z row), `.../pkg-cwc-8732-r2/run_checks.log` line 4 |

### 1b. Versions recorded at the time
| what | recorded | source |
|---|---|---|
| Stage K engine interpreter: Python / numpy / numba / llvmlite / psutil | **NOT captured** by any K log, freeze record, post-check JSON or job log (no version print exists in K) | searched `runs/2026-10-19-0955-k-...` (all logs, JSONs, supervisor.log) |
| numba of the base interpreter + venv path, Stage F (00:43:47Z) | numba **0.68.0**, threading layer omp, 4 threads; a probe in "the same interpreter", not the engine worker itself | `runs/2026-10-19-0037-f-a25-6-11/attempts/gates/output/numba_layer_probe.json`, `.../gates/RECEIPTS.md` |
| numba cache written for the Stage K engine copy | the nine numba cache indexes (`*.nbi`) in `runs/2026-10-19-0955-k-.../attempts/seeds/code/engine/__pycache__/` carry the version string **0.68.0**; their file times are 09:53:19Z (the code copy, before the first K job at 09:53:44Z), the folder time 10:34:36Z; consistent with, not proof of, numba 0.68.0 in K | file headers read as bytes; `ls` times |
| checker interpreter, package r2 (08:55Z) | Python **3.12.6**, numpy **2.5.4** (printed by run_checks.sh) | `.../pkg-cwc-8732-r2/run_checks.log` line 4 |
| psutil, llvmlite in any stage | NOT captured | - |

### 1c. Installed now (UTC), NOT proof of what ran in K
From package metadata folder names (`*.dist-info`), read-only, at about 12:00Z:
- `<tess-pilot venv>\Lib\site-packages`: numpy-2.5.4, numba-0.68.0, llvmlite-0.50.0, psutil-7.2.2 (folder times
  2026-10-17T23:19:58Z-23:20:41Z, i.e. installed before Stage F); `pyvenv.cfg`: version 3.12.6, home = `<user Python312>`.
- `<user Python312>\Lib\site-packages` (the base interpreter's own packages): numpy-2.3.5, numba-0.63.1,
  llvmlite-0.46.0, no psutil. `include/patchlevel.h`: PY_VERSION "3.12.6".
- Consequence: with the supervisor's `PYTHONPATH` the venv packages come first on `sys.path`; the base's own numpy
  2.3.5 / numba 0.63.1 would only be used if `PYTHONPATH` were missing. No K log shows which was imported.

Version prints, run once per configuration at 2026-10-19T12:15:02-12:15:05Z, after `tasklist` showed 0 python
processes (L queue ended), with `-B` (no bytecode), command
`import sys,numpy,numba,llvmlite,psutil; print(versions, 'venv-tess312' in numpy.__file__)`:
- (A) the K configuration: `<user Python312>\python.exe` with `PYTHONPATH=<tess-pilot venv>\Lib\site-packages`:
  Python 3.12.6, numpy 2.5.4, numba 0.68.0, llvmlite 0.50.0, psutil 7.2.2; numpy imported from the venv: True.
- (B) the venv launcher `<tess-pilot venv>\Scripts\python.exe`: identical output.
Installed now, NOT proof of what ran in K (the venv's dist-info folders date from 2026-10-17T23:20Z, before Stage F,
and nothing in the logs records a later install, but K itself printed no versions).

## 2. Origin and licence of the construction and checking files

| file | sha256 (K copy) | origin | first appearance in the delivery branch (D, `git log --diff-filter=A`) | licence (V3R1T4S LICENSING.md) |
|---|---|---|---|---|
| `lb_lns_gen.py` | abf23696f619face... | **V3R1T4S, unchanged**: byte-identical to `repo/known-knowns/bigger-codes/how-we-built-it/lb_lns_gen.py` (pinned repo commit 9b1d444eb864a1475e092047d49612a7410a7c5a, 2026-10-13); written by the V3R1T4S agents | 10cf171 2026-10-19T01:03:29+02:00 (relay B, `cwc-b-2026-10-18-2136/run/.../code/lb_lns_gen.py`) | AGPL-3.0 |
| `gslib.py` | 56603baad2b6d993... | V3R1T4S, unchanged (byte-identical to the repo file of the same name) | 10cf171 | AGPL-3.0 |
| `lns6.py` | 66f9a7465748ed17... | V3R1T4S, unchanged (byte-identical to the repo file of the same name) | 10cf171 | AGPL-3.0 |
| `cwcheck_int.py` | 3b4840b7c213daa7... | workspace-local (W `tools/`), written by the Windows agents for this campaign; file time 2026-10-16T19:47:29Z; no author header. NOT derived from the repo checker: the repo has `verify-it-yourself/cwcheck.py` (different name, sha256 fffa9d46...), no file of these names | 10cf171 (`cwc-b-2026-10-18-2136/tools/cwcheck_int.py`) | AGPL-3.0 (checker) |
| `cwcheck_set.py` | 7160f9b4fc252b34... | workspace-local, as above (same file time) | 10cf171 | AGPL-3.0 |
| `cwio.py` | 4fb218c9ad0eea78... | workspace-local parser shared by both checkers (parsing only), as above | 10cf171 | AGPL-3.0 |
| `post_check.py` | fa563fea64ae5031... | workspace-local, written by the Windows agents in Stage F (docstring "Post-job check (Stage F)"); identical bytes in F, G, H, K | 1efa284 2026-10-19T03:01:35+02:00 (`cwc-f-2026-10-19-0037/.../code/post_check.py`) | AGPL-3.0 |
| `j7_run.py` | 0c012a4941108e1e... | workspace-local wrapper, written by the Windows agents; lineage below | 0193906 2026-10-19T12:53:48+02:00 (`cwc-w-2026-10-19-0947/attempts/fix/code/j7_run.py`); K copy in 942aad5 | AGPL-3.0 |

Wrapper lineage (our own modifications; none of these files exists in the pinned repo):
- F: `start_gate.py` (c81cb852..., last-start gate only) ran the engine; a `j5_run.py` (aba2cb21...) was written in F but not launched.
- j5 (2138cd60..., 109 lines; "adapted from Stage F j5_run.py: + gain-time curve CSV and final kept fractions"): used in G and H; first in D at d407772 (2026-10-19T03:32:54+02:00).
- j5 -> j6 (3d1b3a2d..., CRLF): +158 / -19 lines (`runs/2026-10-19-0755-i-a25-6-11-evidence/lenses/wrapper/code/j5_to_j6.diff`, also j5_to_j6_v1/v2 and j6v2_to_j6v3 diffs): suspend the engine while the checkers run, resume, pause receipts, test snapshot option; first in D at bb58b13.
- j6 -> j7 (0c012a49..., LF), in the W stage (`runs/2026-10-19-0950-w-wrapper-fix/attempts/fix/code/`): `j6_to_j7.diff` +60 / -11 lines, fail-closed paths P1 (watchdog kills the checker, never resumes, exit 5), P2 (hash mismatch -> no check, exit 6), P3 (invalid snapshot or post-check -> exit 7); then `j7v1_to_j7.diff` +5 / -0 lines, P4 `--stop-at-M` (used only by the seed-105 controls). The K copy is byte-identical to the W stage's final j7_run.py.
- None of the wrappers changes engine arguments: every stage calls `lb_lns_gen.py START 25 6 11 PREFIX --seconds S --rounds 1000000 --seed X`.

Data: the code files (TXT/NPY) and all records/logs are CC BY 4.0 under the same convention; the seed is
third-party (credit below) and not ours to relicense.

Caution for the bundle: commit 942aad5 also contains numba cache files
(`cwc-k-2026-10-19-0953/attempts/seeds/code/engine/__pycache__/*.nbi, *.nbc`); they are caches, not sources, and
should not be published.

## 3. The chain 8,698 -> 8,721 -> 8,728 -> 8,732 -> 8,733 -> 8,734

Seed: `a25.6.11.8698H`, https://aeb.win.tue.nl/codes/cwc/d6/a25.6.11.8698H, fetched 2026-10-18T21:39:25Z by curl,
HTTP 200, 69,593 bytes, sha256 f35a2cfecf75e79c85153a82d937233db0236b78ff0db2c643fc1856327cf038 (W
`logs/FETCHES_b.log` line 2; stored at W `sources/archive/a25.6.11.8698H`, re-hashed now: equal; the same digest is in
the pinned repo's `bigger-codes/how-we-built-it/SEEDS.sha256`). Author credit, from the legend of the table page
`runs/2026-10-19-0755-i-a25-6-11-evidence/data/Andw_live.html` (read 2026-10-18T21:39:24Z, sha256 15b15c8d...):
"Bo: Jordan Boisclair, email 2026-08-22 with 18 new codes, email 2026-08-30 with 90 new codes." That page now shows
the cell as `8718 Pl -24630`; the attribution of 8698H to Bo comes from the 2026-10-08/10 table versions parsed in
the pinned repo (`the-record-we-beat/parsed_cells_*.tsv`: `8698Bo-24630`). Converted with `tools/cwio.py`
(`runs/2026-10-19-0037-f-a25-6-11/attempts/gates/code/g1_convert_check.py`) to seed_8698.txt 9513ec3f... and
seed_8698.npy c42b36b1e43882d1768fb3ad41ed7baa7faf3537252d9f85a4d098df4ca42fdf (8,698 words, both checkers rc 0).

Engine fixed parameters in every step: rmax 8, KB 3 (log line 1), clusters 3000, plateau-frac 0.3, nodecap 100000
(defaults), `--rounds 1000000`, 4 threads. Rounds are 0-based; t = engine clock (s).

| step | stage, run folder (W `runs/`) | input .npy sha256 | seed | budget `--seconds` | new best: round, t | output TXT sha256 | output NPY sha256 | delivery commit (D), path |
|---|---|---|---|---|---|---|---|---|
| 8,698 -> 8,721 | F, `2026-10-19-0037-f-a25-6-11` (job J2, launched 00:44:32Z; stopped by the watcher at 00:48:25Z, J2 rc 15) | c42b36b1... (seed) | 102 | 1500 (175 rounds logged) | 171, t 228 s (227.656) | f886a562fd50bf07ae63ced0d9de60f22825b45fc638b15c55463eb4e95af526 | 9f5c52794af3d4d9992fa1f4ff403c9c0f89d2161b441c095d5a1a8c6c90be90 | 1efa284, `cwc-f-2026-10-19-0037/run/attempts/pilot/output/CANDIDATE_M8721.*` |
| 8,721 -> 8,728 | G, `2026-10-19-0223-g-a25-6-11-cont` (02:24:35Z-02:49:40Z) | 9f5c5279... | 103 | 1500 (1,160 rounds, last t 1501 s) | 1131, t 1466 s (1465.914) | 070d562c0c4665f04e10d9e181b922de081f4617812eadc88902bc90f2626cd6 | 086efc30919ba7a28bc3e465aa8f94cfd11a006884a8ec83df8c609e702e0d87 | eff2ba1, `cwc-g-2026-10-19-0223/run/attempts/cont/output/CANDIDATE_M8728.*` |
| 8,728 -> 8,732 | H, `2026-10-19-0307-h-a25-6-11-last` (03:08:13Z-03:48:19Z) | 086efc30... | 104 | 2400 (1,933 rounds, last t 2401 s) | 1443, t 1800 s (1800.001) | e66b06b68ab8a06a40f1cea36254008d781f047a69597464abc0aad04b150f26 | 0f9c84b89764187cd6780bf7fe234b8de08d7f48e5156d157ca2b3145b2c4868 | 3c77e02, `cwc-h-2026-10-19-0307/run/attempts/walk/output/CANDIDATE_M8732.*` |
| 8,732 -> 8,733 | K run R1, `2026-10-19-0955-k-a25-6-11-seeds` (09:54:08Z-10:04:14Z; frozen 09:57:22Z) | 0f9c84b8... | 201 | 600 (504 rounds, last t 601 s) | 159, t 192 s (192.068) | c8f381a3104918b937425f827d96c4be28f5997b28db0e262c820ed617541535 | 7973941673273ca373a15500570070de717106ffbf6e07d594b2481cd00f8381 | 942aad5, `cwc-k-2026-10-19-0953/attempts/seeds/output/s201/CANDIDATE_M8733.*` |
| 8,733 -> 8,734 | same run (frozen 10:03:39Z) | (same run) | 201 | 600 | 477, t 568 s (568.368) | **f9f280613ee2a5c500220a9f022d35d83264a14f96d940c9a517a15cebdf6fde** | **d9a093d62fb0e314c85584b0f4e98afe7e4e9ad7460615cc88ec4bb27897db96** | 942aad5, `cwc-k-2026-10-19-0953/attempts/seeds/output/s201/CANDIDATE_M8734.*` |

Checks: every step's input hash equals the previous output NPY (re-hashed now: `input_8721.npy`, `input_8728.npy`,
`input_8732.npy` of G, H, K); the committed bytes in D (`git show COMMIT:RELATIVE_PATH | sha256sum`) equal the TXT hashes
above for all five outputs and the 8,734 NPY. Sources: engine logs `F: attempts/pilot/output/J2_walk_s102.log`,
`G: attempts/cont/output/G_walk_s103.log`, `H: attempts/walk/output/H_walk_s104.log`,
`K: attempts/seeds/output/s201/K_s201.log`; `*_best.json` (round, t); `CANDIDATE_M*_freeze.json`; stage REPORTs.
The 8,734: 8,577 words from the 8,732 (0.982), 8,324 from the seed (0.9531) (`K_s201_summary.json`). Validity at
the freeze: cwcheck_int rc 0 (pairs 38,137,011, min distance 6, below-d 0), cwcheck_set rc 0 (t 9, collisions 0);
post-check 10:04:14Z both_valid true; owner recheck 10:45:27Z valid by both (`owner_recheck/recheck.log`).
Seed-105 control (not in the chain): five runs from the 8,732 (Stage I runs 1-3, K R0, L control) all gave 8,733 at
round 11 with TXT 4f972f16... / NPY e45842ba... (determinism over 12 rounds on this machine only).

## 4. Declared gaps (kept)
- F: the freeze-time checkers, the specialist re-run and the owner re-run ran outside the supervisor's Job Object
  (the watcher was a plain background process) (`runs/2026-10-19-0037-f-.../REPORT.md` section 9 item 8).
- G and H: the snapshot checkers ran CONCURRENTLY with the running engine (wrapper j5, no pause), sequentially with
  each other (H `REPORT.md` section 8 item 4 and section 11; same wrapper in G). G's panel checks ran outside the
  supervisor tree without CPU receipts (G `REPORT.md` addendum 03:08Z; H `BRIEF.md`).
- K: the supervisor queue had NO effective barrier conditioning R1-R5 on R0's result; the condition was met in fact
  (R0 rc 0, M 8,733, both checkers, before R1 started 09:54:08Z) but not guaranteed by design (declared 10:10Z;
  `runs/2026-10-19-0955-k-.../REPORT_K.md` "Status and deviations").
- K: the engine interpreter's package versions were not captured at run time (section 1b).
- K: the owner recheck's interpreter and command lines were not saved (only `recheck.log`).
- No full rebuild of the chain has been executed; the time-budgeted runs are not replayed. Status of the 8,734:
  candidate lower bound, live comparison PENDING, not a record.
