# Provenance: Grassmannian packing (m, n, N) = (11, 4, 66)

The configuration was produced by an unattended search lane (a series of AI coding sessions in a sandbox). The lane's working directory was `/work` inside the sandbox; paths below are relative to it unless marked as lane-root paths.

## Object match

The claimed object `claim/object/11-4-66.txt` has the same coordinates as the lane file `work/cells/11-4-66.txt` (maximum absolute coordinate difference 0.0, measured). The headers differ, so the byte hashes differ: lane file sha256 starts `8956255dc04b2ecc`, object sha256 starts `18ce522b9988706b`. The cell equals the saved result `work/results/11-4-66.pol.npy` up to re-orthonormalisation (projector difference 5.6e-16, measured). Minimum squared chordal distance: 2.577769552477 for the result, cell and object (measured).

## 1. Producing scripts and starting point

- `refix6.py` is the producing script. It is `refix5.py` with `max_iter=60` and the early exit `dstop=n - tv - 1e-8` (`refix6.py:17-21`). It loads the seed with `polsweep3.load_seed` (`polsweep3.py:5-29`) and runs `lptrac.lp_trace(tol=5e-4, r0=1e-3, method='highs-ipm', gapor_stop=8e-5, noacc_stop=18, max_r=0.05, dstop=...)`. The early exit stops after the first accepted step that clears the table by 1e-8 (`lptrac.py:68-69`).
- For (11, 4, 66), `load_seed` had one candidate: Sloane's file `work/grass/txts/grassc.11.4.66.txt` (sha256 starts `010d75a544a5657a`). The lane's copy of the record archive has files for 11-4-65 and 11-4-70 but none for 11-4-66.
- Seed minimum distance: 2.5777278197507. The table value is 2.5777278197, credit [31]. The seed equals the table value to all 10 listed digits, so the seed is the configuration behind the posted table entry.
- The polish ran 3 LP iterations with 1 accepted step, which triggered the early exit at 2.5777695524773, gain +4.17e-5 (`logs/q14_3.log:37`).
- `harvest14.py` wrote the cell through `mkcell.write_cell`. The cell header `# packing 11-4-66 q14` is the tag at `harvest14.py:54`.

Starting point: the posted configuration (Sloane's file, credit [31], attaining the table value). The result is a re-polish of the posted configuration in the same basin, not a different construction. There was no basin hopping, deletion, addition or random start.

Same basin as the posted configuration: yes. In the seed's own coordinate frame (no realignment), each of the 66 result subspaces is nearest to the seed subspace with the same index. The per-subspace squared chordal displacement from seed to result is at most 8.2e-7, median 5.2e-7 (measured on the lane's seed file and saved result), after a single accepted LP step.

Script versions: `lptrac.py` was edited after this run (work copy mtime 2026-11-06 16:08 -0700). The copy here is the version in the snapshots `best-work-013` (07:47) and `best-work-014` (09:35), which bracket the run at 08:50 (sha256 starts `0afa7755f7d7`). `refix6.py` (mtime 06:35) and the other copied files have the same hash in those snapshots and in the work directory.

## 2. Command lines

Launch, from the lane's session transcript store (session 014), verbatim prefix:

```
cd /work && chmod +x run14.sh && for w in 0 1 2 3; do nohup ./run14.sh q14_w$w.txt $w > /dev/null 2>&1 & done
```

Queue row `q14_w3.txt:37` is `11 4 66 320`. Through `run14.sh:3` that row runs:

```
timeout 410 python3 refix6.py 11 4 66 320 >> logs/q14_3.log 2>&1
```

## 3. Log lines showing the hit

`work/logs/q14_3.log:37`, `work/logs/q14_3.prog:37` and `work/results/11-4-66.pol.json`, copied in `hit.log`.

## 4. What the lane tried that failed

For this cell:

- `work/logs/q7s2.log:16` (lane session 007): the narrow-tolerance polish screen returned stage `fixpt`, gain 1e-10, no improvement. `polsweep4.py` is the only script that emits `fixpt` (`polsweep4.py:45`), run by `runsweep4.sh`. That script was not copied, because it did not produce the result.
- The row was queued in more than ten earlier queue files across sessions 005 to 013. Only the session 007 and session 014 runs left progress lines.

For the family and the method, from `work/NOTES.md`:

- Basin hopping and polish-hopping on posted [9]/[31] configurations found only worse optima (NOTES.md:50, 72).
- Session 006 found 0 of about 44 [24]-credit probes improving in families including (11,4), all LP fixpoints under the narrow tolerance (NOTES.md:152).
- Session 009 found that tolerances of 2e-5 or less hid real slack (NOTES.md:252-255).
- Session 015 found the (11,4) tail N = 72 to 82 rigid at 0 of 11 (NOTES.md:447).

## Files copied

| file | role |
|---|---|
| `refix6.py` | producing script (seed load + wide-tolerance LP polish with early exit) |
| `run14.sh` | queue driver |
| `lptrac.py` | `lp_trace` with `dstop` (version at run time) |
| `polsweep3.py` | `load_seed` |
| `packlib.py` | Sloane file parser, QR re-orthonormalisation, table reader |
| `worker.py` | `mind`, `overlap_mat`, `orth_frames` |
| `opt.py` | imported by `worker.py` |
| `harvest14.py` | writes the cell file from the saved result |
| `mkcell.py` | mpmath re-orthonormalisation and cell writer |
| `hit.log` | log excerpts with source file and line numbers |

## Path, username and email scan of the copied files

No usernames and no email addresses. Absolute sandbox paths: `packlib.py:70` and `mkcell.py:89` open `/inputs/grassmannian_2026-11-04.tsv`. Relative data paths that the code expects: `grass/txts/`, `packing-records/grassmannian/`, `results/`, `cells/`. The copied code was not edited.
