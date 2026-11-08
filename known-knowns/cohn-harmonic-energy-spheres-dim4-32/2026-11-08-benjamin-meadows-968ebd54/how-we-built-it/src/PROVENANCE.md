# Provenance: harmonic energy (N, n) = (64, 20)

The configuration was produced by an unattended search lane (a series of AI coding sessions in a sandbox). The lane's working directory was `/work` inside the sandbox; paths below are relative to it unless marked as lane-root paths. The lane's logs use UTC; file times below are -0700.

## Object match

The claimed object `claim/object/64-20.txt` has the same coordinates as the lane file `work/cells/64-20.txt` (maximum absolute coordinate difference 0.0, measured). The header energy strings differ after about 30 digits, so the byte hashes differ: lane file sha256 starts `4ac9e1dd363b40a2`, object sha256 starts `968ebd541209b17f`. The first lane file with this configuration is `work/run4/w9/64-20.npz` (2026-11-06 10:02, energy 6.685463681357, sorted pairwise inner products equal to 2e-16, measured). `work/best/64-20.npz` is a later copy. The older files `run2/w1/64-20.npz` and `run3/w2/64-20.npz` hold a different configuration at the table energy 6.7232495038.

## 1. Producing scripts and starting point

`liftseed.py` (worker w9, lane session 002) is the producing script. For a target (N, n) it does three things:

- It starts from the best saved lane configuration for (64, 20). That file held energy 6.72324950, equal to the table (`run4/w9/liftseed.log:262`).
- It builds seeds by lifting the best saved (N, n-1) configuration into one more coordinate with Gaussian noise 0.05, 0.15 and 0.35 (`liftseed.py:92-97`). It also projects the best (N, n+1) configuration down along its weakest principal axes (`liftseed.py:98-106`). It relaxes each seed with `opt.minimize_energy` (L-BFGS-B, p = n - 2 = 18).
- With the remaining time it basin-hops: it kicks all points of the current best by Gaussian noise of 0.05 or 0.15, renormalises, and relaxes (`liftseed.py:115-123`).

For 64-20 the log shows two improvements (`run4/w9/liftseed.log:263-264`):

1. `lift0.05`: the lifted (64, 19) seed relaxed to 6.69931841, already below the table value 6.7232495038.
2. `hop`: one basin hop from that configuration reached 6.68546368, the final value.

The lift source was the best saved (64, 19) file, `work/run2/w0/64-19.npz` (mtime 07:33, energy 9.6249972657, measured). It was the only saved 64-19 file before this run, and `cfg()` prefers a saved lane file over the posted configuration (`liftseed.py:33-56`). That file is the lane's own improvement over the posted 64-19 (table 9.6271369221). `worker3.py` (column n = 19, session 001) produced it with basin hop 12, move type 2: remove the 1 to 4 highest-energy-contribution points, relax, and reinsert the same number at deep holes (`worker3.py:147-156`, `run2/w0/col19.log:21-22`). The row 64-19 is on the lane's already-published list, so the lane never claimed it.

Answer to the method question: basin hopping produced the final step. It started from a dimension lift of the lane's own improved (64, 19) configuration, which itself came from a basin hop on the posted (64, 19). There was no point deletion from a neighbouring N and no addition.

Same basin as the posted (64, 20) configuration: not measured in this provenance pass. NOTES.md:120-121 states that the lane's improved cells are "ENTIRELY different structures from posted".

`harvest.py` wrote the cell (mpmath renormalisation, header energy at 45 digits, `harvest.py:79-81`). The last rewrite of `cells/64-20.txt` (13:12) was `cd /work && python3 harvest.py /work/cells /work/best` (transcript, session 004).

Script versions: `liftseed.py` (mtime 08:09, sha256 starts `e57a08fe1063`), `worker3.py` (mtime 07:01) and `opt.py` (mtime 06:45) predate both runs. They are unchanged in all snapshots.

## 2. Command lines

From the lane's session transcript store (session 002), verbatim tail of the tool call:

```
mkdir -p run4/w9 && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nohup setsid python3 -u liftseed.py run4/w9 18 555 $(cat run4/lift2.txt) > run4/w9.out 2>&1 &
```

The arguments are an 18 s budget per row and rng seed 555. The row list `run4/lift2.txt` holds every non-universal, unpublished row with 13 <= n <= 27 and 45 <= N <= 64; 64-20 is word 130.

The lift source came from this run (transcript, session 001; worker w0 ran column 17, then column 19):

```
OMP_NUM_THREADS=1 python3 -u worker3.py 19 44 64 run2/w0 25 5 1 0
```

Both scripts use wall-clock budgets and one shared rng stream across rows, so an exact rerun can follow a different sequence.

## 3. Log lines showing the hit

`work/run4/w9/liftseed.log:262-265`, copied in `hit.log` with the lift-source lines `run2/w0/col19.log:21-22,46`.

## 4. What the lane tried that failed

For this cell:

- `run2/w1/col20.log:21,45` (session 001, `worker3.py` column n = 20): no improvement. There is no 65-20 configuration, so no del-1 step ran at N = 64; augmentation from 63-20 and 25 s of basin hops left the energy at the table value.
- `run3/w2/col20.log:1-2` (session 001, `worker4.py` second pass): no improvement.
- After the win, session 004 tried an SDP relaxation on 64-20. It found the relaxation far too loose, with seeds landing 0.13 to 35 above (NOTES.md:175-178).

For the family and the method, from `work/NOTES.md`:

- Basin hopping alone from a posted configuration found nothing (on 56-10, NOTES.md:32).
- The lift and projection seeds found the session-002 wins; three of the five were n = 20 rows (NOTES.md:61-70).
- Re-running the lift sweep with a fresh rng gave 0 gains (NOTES.md:153-154, session 003, liftseed2.py).

## Files copied

| file | role |
|---|---|
| `liftseed.py` | producing script (lift/project seeds + basin hops) |
| `worker3.py` | produced the (64, 19) lift source (column sweep, hop move 2) |
| `opt.py` | energy, gradient, L-BFGS relax, mpmath energy |
| `harvest.py` | writes the cell file from the best saved npz |
| `hit.log` | log excerpts with source file and line numbers |

Not copied: `configs/E.npy.npz` (the parsed 2021 data set), the lane-root `inputs/cohn_harmonic.tsv` and `inputs/already_published.txt`, `run4/lift2.txt`, and the npz files.

## Path, username and email scan of the copied files

No usernames and no email addresses. Absolute sandbox paths:

- `liftseed.py:11`: `/work/configs/E.npy.npz`
- `liftseed.py:14`: `/inputs/cohn_harmonic.tsv`
- `liftseed.py:21`: `/inputs/already_published.txt`
- `liftseed.py:37`: glob `/work/run*/**/`
- `worker3.py:16`: `/work/configs/E.npy.npz`
- `worker3.py:64`: glob `/work/run*/**/`
- `harvest.py:9`: `/inputs/cohn_harmonic.tsv`
- `harvest.py:32`: `/inputs/already_published.txt`
- `harvest.py:33-34`: defaults `/work/cells` and `/work/best`
- `harvest.py:38`: glob `/work/run*/w*/*.npz`

The copied code was not edited.
