# Provenance: harmonic energy (N, n) = (61, 21)

The configuration was produced by an unattended search lane (a series of AI coding sessions in a sandbox). The lane's working directory was `/work` inside the sandbox; paths below are relative to it unless marked as lane-root paths. The lane's logs use UTC; file times below are -0700.

## Object match

The claimed object `claim/object/61-21.txt` has the same coordinates as the lane file `work/cells/61-21.txt` (maximum absolute coordinate difference 0.0, measured). The header energy strings differ after about 30 digits, so the byte hashes differ: lane file sha256 starts `6acee03d3cd767d8`, object sha256 starts `80cabc361c4f9c45`. These lane files hold the same configuration (energy 4.103948302434, sorted pairwise inner products equal to 3e-16, measured): `work/run2/w2/61-21.npz` (first, 2026-11-06 07:34), `work/run3/w3/61-21.npz` and `work/best/61-21.npz`.

## 1. Producing scripts and starting point

- `worker3.py` is the producing script, a column sweep for n = 21 run from N = 64 down to N = 44. For each N it runs these steps in order:
  1. del-1 of best[N+1] (`worker3.py:80-92`)
  2. augmentation of best[N-1] with one deep-hole point (`worker3.py:123-133`)
  3. basin hops until the 25 s budget is used (`worker3.py:134-174`)
- The hit came from the augmentation step, logged as `61-21 r0 aug` (`run2/w2/col21.log:22-23`). Of the two augmentation tries, the first relaxed to 4.1068451763 and the second to 4.1039483024, which is the final value (`run2/w2/col21.log:43`).
- best[60] at that moment was the posted 2021 data-set configuration for (60, 21). Its init energy 3.8972329293 (`run2/w2/col21.log:17`) equals the energy_2021 column of the lane-root `inputs/cohn_harmonic.tsv`. No lane file for 60-21 existed before this run.
- The deep-hole point (`worker3.py:37-43`) is the farthest candidate from the existing points among 300 random directions and the antipodes of the existing points.
- The relaxation is `opt.minimize_energy`: L-BFGS-B on row-normalised coordinates with p = n - 2 = 19, gtol 1e-10, ftol 1e-16 (`worker3.py:24-25`, `opt.py`).
- The del-1 step that runs first for N = 61 (deleting each point of best[62]) logged no improvement. No basin hop improved 61-21 after the augmentation.

Answer to the method question: point addition (augmentation) from the posted neighbour (60, 21). It is not basin hopping and not point deletion.

The lane's own summary disagrees. NOTES.md:43 says the four session-001 wins, 61-21 among them, were "All 4 found by del-1 enumeration chains". The log shows `aug`, not `del1`, for 61-21. Later, NOTES.md:186-187 reports that the weighted-augment continuation "reproduced our 61-21 improved basin exactly".

Same basin as the posted (61, 21) configuration: not measured in this provenance pass. NOTES.md:120-121 states that the lane's improved cells are "ENTIRELY different structures from posted" (Procrustes-aligned median point displacement about 0.9 to 1.0).

`harvest.py` wrote the cell (mpmath renormalisation, header energy at 45 digits, `harvest.py:79-81`). The last rewrite of `cells/61-21.txt` (13:12) was `cd /work && python3 harvest.py /work/cells /work/best` (transcript, session 004).

Script versions: `worker3.py` (mtime 07:01, sha256 starts `079cfb27f6af`) and `opt.py` (mtime 06:45) predate the run at 07:12 to 07:34. `harvest.py` (mtime 07:10) is unchanged in all snapshots.

## 2. Command lines

Launch, from the lane's session transcript store (session 001). Worker w2 ran column 23, then column 21:

```
bash -c for c in 23 21; do OMP_NUM_THREADS=1 python3 -u worker3.py $c 44 64 run2/w2 25 31 1 0; done
```

The run for this cell was therefore:

```
OMP_NUM_THREADS=1 python3 -u worker3.py 21 44 64 run2/w2 25 31 1 0
```

The arguments are n = 21, Nlo = 44, Nhi = 64, outdir, hop budget 25 s, rng seed 31, 1 round, del-2 off. The budgets are wall-clock times, so an exact rerun can follow a different sequence.

## 3. Log lines showing the hit

`work/run2/w2/col21.log:22-23` (hit) and `:43` (final), copied in `hit.log` with the init lines.

## 4. What the lane tried that failed

For this cell: the first attempt won. Later runs only reproduced or kept it: worker4.py `run3/w3/col21.log:5`, halo.py `run5/h2/halo.log:2`, and augcont (NOTES.md:186-187).

For the family and the method, from `work/NOTES.md`:

- Basin hopping alone on a posted configuration found nothing (on 56-10, NOTES.md:32).
- A second pass that diversified the (N+1) minima and then deleted one point gave no new gains on the n = 21 column, among others (NOTES.md:45-47).
- The del-2 experiment found no gains on 60-21 and 62-21 (NOTES.md:48-49).
- Session 002 found that teleport (delete one point and reinsert it at a deep hole) and multi-start random restarts return the same or the posted minima. It also lists dead mechanisms for n = 28 to 32 and for structured rows (NOTES.md:78-92).

## Files copied

| file | role |
|---|---|
| `worker3.py` | producing script (column sweep: del-1, augment, hops) |
| `opt.py` | energy, gradient, L-BFGS relax, mpmath energy |
| `harvest.py` | writes the cell file from the best saved npz |
| `hit.log` | log excerpts with source file and line numbers |

Not copied: `configs/E.npy.npz` (the parsed 2021 data set that `worker3.py:16` loads, built from data.txt).

## Path, username and email scan of the copied files

No usernames and no email addresses. Absolute sandbox paths:

- `worker3.py:16`: `/work/configs/E.npy.npz`
- `worker3.py:64`: glob `/work/run*/**/`
- `harvest.py:9`: `/inputs/cohn_harmonic.tsv`
- `harvest.py:32`: `/inputs/already_published.txt`
- `harvest.py:33-34`: defaults `/work/cells` and `/work/best`
- `harvest.py:38`: glob `/work/run*/w*/*.npz`

The copied code was not edited.
