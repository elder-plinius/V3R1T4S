# Provenance: Grassmannian packing (m, n, N) = (11, 1, 62)

The configuration was produced by an unattended search lane (a series of AI coding sessions in a sandbox). The lane's working directory was `/work` inside the sandbox; paths below are relative to it unless marked as lane-root paths.

## Object match

The claimed object `claim/object/11-1-62.txt` has the same coordinates as the lane file `work/cells/11-1-62.txt` (maximum absolute coordinate difference 0.0, measured). The headers differ, so the byte hashes differ: lane file sha256 starts `fd33107b7cc0b03a`, object sha256 starts `c9da55b9f9cfe7a4`. The cell equals the saved result `work/results/11-1-62.pol.npy` up to re-orthonormalisation (projector difference 2.8e-16, measured). Minimum squared chordal distance: 0.889170554550 for the result, cell and object (measured).

## 1. Producing scripts and starting point

- `refix5.py` is the producing script. It loads a seed with `polsweep3.load_seed` (`polsweep3.py:5-29`) and runs one wide-tolerance sequential-LP polish, `lptrac.lp_trace(tol=5e-4, max_iter=40, r0=1e-3, method='highs-ipm', gapor_stop=8e-5, noacc_stop=18, max_r=0.05)` (`refix5.py:17-20`). It saves the result when it beats the seed (`refix5.py:29-30`).
- For (11, 1, 62), `load_seed` had one candidate: Sloane's file `work/grass/txts/grassc.11.1.62.txt` (sha256 starts `c4e91bfe7e2b0bf9`), downloaded from `https://neilsloane.com/grass/` in lane session 001 (NOTES.md:8). The lane's copy of the record archive (`work/packing-records/grassmannian/`) has no `11-1-62` file.
- Seed minimum distance: 0.8891150779699. The table value is 0.8891152435, credit "Henry Cohn, 2026". The seed sits 1.66e-7 below the table: the lane calls this a "weak seed".
- The polish ran 40 LP iterations with 25 accepted steps and reached 0.8891705545505, gain +5.53e-5 (`logs/q11w.log:54`).
- `harvest2.py` wrote the cell through `mkcell.write_cell` (mpmath re-orthonormalisation). The cell header `# packing 11-1-62 d=...` is the format of `harvest2.py:75`. The exact harvest invocation was not looked up.

Starting point: the posted Sloane configuration for (11, 1, 62). The result is a local LP polish of it, not a different construction. There was no basin hopping, deletion, addition or random start.

Same basin as a posted configuration:

- Sloane's posted (11, 1, 62) configuration: yes. In the seed's own coordinate frame (no realignment), each of the 62 result lines is nearest to the seed line with the same index. The per-line squared chordal displacement from seed to result is at most 4.5e-4, median 1.6e-4 (measured on the lane's seed file and saved result).
- Cohn's 2026 record configuration, the current table entry: unknown. That configuration was never in the lane, so no comparison was made. NOTES.md:326-327 states the lane's hypothesis that weak seeds win only when the record "was derived from" the same old configuration. The lane did not test that hypothesis for this row.

Script versions: `lptrac.py` was edited after this run (work copy mtime 2026-11-06 16:08 -0700, sha256 starts `b729bd5e5ac4`). The copy here is the version in the snapshots `best-work-010` (02:33) and `best-work-011` (04:12), which bracket the run at 03:21 (sha256 starts `22e918a0a163`). All other copied files have the same hash in those snapshots and in the work directory, with mtimes before the run.

## 2. Command lines

Launch, from the lane's session transcript store (session 011):

```
nohup ./run11w.sh q11_weak.txt w > /dev/null 2>&1 &
```

Queue row `q11_weak.txt:54` is `11 1 62 120`. Through `run11w.sh:3` that row runs:

```
timeout 180 python3 refix5.py 11 1 62 120 >> logs/q11w.log 2>&1
```

## 3. Log lines showing the hit

`work/logs/q11w.log:54`, `work/logs/q11w.prog:54` and `work/results/11-1-62.pol.json`, copied in `hit.log`.

## 4. What the lane tried that failed

For this cell: no earlier attempt is recorded. The row was queued in `q8_n1.txt`, `q8n1_w2.txt` and `cohn_n1.txt`, but no result line for it exists in any log. The saved result json holds only the session 011 run.

For the family and the method, from `work/NOTES.md`:

- Basin hopping and polish-hopping on posted [9]/[31] configurations found only worse optima (NOTES.md:50, 72).
- Sessions 002 to 008 called n = 1 rows "a dead lane" (NOTES.md:60). Session 009 traced this to a too-narrow LP tolerance (2e-5 or less) and reopened the n = 1 rows with tol = 5e-4 (NOTES.md:252-255).
- Session 010 called weak seeds unreachable. Session 011 corrected this when 11-1-62/63/64 won (NOTES.md:325-327).
- Polishing a different, weaker seed on rows where the record seed was rigid gave 0 of 9+ (NOTES.md:331).

## Files copied

| file | role |
|---|---|
| `refix5.py` | producing script (seed load + wide-tolerance LP polish) |
| `run11w.sh` | queue driver |
| `lptrac.py` | `lp_trace`, the sequential-LP polish (version at run time) |
| `polsweep3.py` | `load_seed` |
| `packlib.py` | Sloane file parser, QR re-orthonormalisation, table reader |
| `worker.py` | `mind`, `overlap_mat`, `orth_frames` |
| `opt.py` | imported by `worker.py` |
| `harvest2.py` | writes the cell file from the saved result |
| `mkcell.py` | mpmath re-orthonormalisation and cell writer |
| `hit.log` | log excerpts with source file and line numbers |

## Path, username and email scan of the copied files

No usernames and no email addresses. Absolute sandbox paths: `packlib.py:70` and `mkcell.py:89` open `/inputs/grassmannian_2026-11-04.tsv`. Relative data paths that the code expects: `grass/txts/`, `packing-records/grassmannian/`, `results/`, `cells/`. The copied code was not edited.
