# Provenance: spherical code (d, N) = (29, 727)

The configuration was produced by an unattended search lane (a series of AI coding sessions in a sandbox). The lane's working directory was `/work` inside the sandbox; paths below are relative to it unless marked as lane-root paths.

## Object match

The claimed object `claim/object/29_727.txt` has the same 727 x 29 coordinates as the lane file `work/cells/29-727.txt` (maximum absolute coordinate difference 0.0, measured). The byte hashes differ because the posted object has a header line: lane file sha256 starts `61f8caf2e7c18236`, object sha256 starts `a796ba15c620c062`. The lane copy `work/tpM14_29-727.txt` has the same bytes as `work/cells/29-727.txt`. Max cosine of the lane file: 0.236502969457658 (`work/verify17.log:218`).

## 1. Producing scripts and starting point

The final configuration came from `chain3.py` in mode `add:cells/29-725.txt` (header at `work/bM14.log:84`). That mode calls `run_add` (`chain3.py:106-136`):

- it loads the donor, our own earlier cell for N = 725 (max cosine 0.236140651, `work/bM14.log:85`);
- it inserts k = 2 points; trial tr0 places each point with the hole search `sph._min_ip_to_core` (`chain3.py:118-123`, `sph.py`), not at random;
- it polishes all 727 points with `polish` (`chain3.py:92-103`): L-BFGS at beta = 1e3, 3e3, 1e4, 3e4, 1e5, 5e5, 2e6 (`slbfgs.lbfgs_b`), then 10 iterations of sequential LP (`slpf.slp_fast`, cap 700);
- trial tr0 reached 0.236502969458 against the target 0.240054045221 and wrote the cell (`work/bM14.log:86-87`, `chain3.py:130-133`).

The starting point is point addition to our own earlier file. It is not basin hopping, not point deletion and not a random start. The donor chain, each step by `chain3.py` point addition plus the same polish:

1. Posted table configuration for (29, 715), `work/data/29-715.txt`, fetched from `https://spherical-codes.org/data/29/715` by the lane's fetch scripts. Adding 5 points gave our cell 29-720 (`work/b29.log:1-7`).
2. Our cell 29-720 plus 5 points gave 29-725 at max cosine 0.236140651361 (`work/bLoop14.log:38-44`, run by `runloop14.sh`).
3. Our cell 29-725 plus 2 points gave 29-727 (`work/bM14.log:84-88`).

The donor file `work/cells/29-725.txt` was overwritten twice during and after this run (a weaker 0.239387 version, kept in the snapshot `best-work-017/cells/29-725.txt`, and a later restore). The 0.236140651 version is preserved as `work/tpQ14_29-725.txt` (sha256 starts `a5f48931ca6c3689`, max cosine 0.2361406513611278, measured), which is also the current `work/cells/29-725.txt`. The match to the donor that bM14 read rests on the logged max cosine (9 digits). The byte content at read time is not recorded.

Script versions: `chain3.py` (sha256 starts `e848ec39b945`, mtime 2026-11-05 03:55 -0700) predates the bM14 run (about 06:24 to 06:36 -0700) and equals the copy in the snapshot `best-work-013`. `sph.py`, `slbfgs.py` and `slpf.py` have mtimes on 2026-11-04 and the same hashes in `best-work-012` and `best-work-013`.

## 2. Command lines

From the lane's session transcript store (session 014, assistant tool call), verbatim:

```
cd /work && cat /proc/loadavg && export OMP_NUM_THREADS=1 && (TP=tpM14 python3 chain3.py qRetp.txt > bM14.log 2>&1 &) && echo launched
```

The queue row for 29-727 in `qRetp.txt` is not recorded: the file no longer exists, and the session overwrote it while bM14 was running. The logged header shows the mode field `add:cells/29-725.txt`. The trials and iters fields are not recorded. If they were absent, the defaults are trials = 4 and iters = 160 (`chain3.py:222-223`).

Donor steps:

- 29-725: `runloop14.sh` runs `TP=tpQ14 python3 chain3.py qCur14.txt >> bLoop14.log` (`runloop14.sh:14`). The queue builder `chainregen.py` that it calls was not copied, because it only selects rows.
- 29-720: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 TP=tp29 nohup python3 chain3.py wD29.txt > b29.log 2>&1 &` (transcript, session 013).

## 3. Log lines showing the hit

`work/bM14.log:84-88`, copied in `hit.log` with the donor-chain lines and the transcript excerpts.

## 4. What the lane tried that failed

For this cell:

- `work/b29.log:8-9`: chain3.py mode auto from our cell 29-724 (k = 3). The log ends after the donor line. The outcome is not recorded.
- Transcript, session 014 (row 6489 in `hit.log`): two-point greedy deletion from our cell 29-729 gave 0.24051379 against the table 0.240054045231, a failure.
- Transcript, session 014 (row 6492 in `hit.log`, run 2026-11-05T13:32Z): greedy deletion from our cell 29-728 (one point, 0.23727122) and from our cell 29-731 (four points, 0.23751781) both beat the table and each wrote `cells/29-727.txt`. These results are not failures; they were superseded. About four minutes later the bM14 addition result (0.23650297) overwrote them. The final file matches the bM14 value, not the deletion values.

For the family, from `work/NOTES.md` (all lane-written):

- Subtractive seeding (delete the worst k points of an N+k donor, then polish) lands at the donor level (NOTES.md:174).
- Basin hopping on tight posted codes does not move them (NOTES.md:176).
- Generic deletion or cover is dead on dense bad-edge graphs (NOTES.md:172).
- The working mechanism is adding points to the lane's own improved cells, then repolishing (NOTES.md:331-336).
- Sessions 014 to 016, which produced this cell, wrote no NOTES entries (NOTES.md:829).

## Files copied

| file | role |
|---|---|
| `chain3.py` | producing script (point addition + polish) |
| `sph.py` | hole search `_min_ip_to_core`, numba kernels |
| `slbfgs.py` | L-BFGS beta ramp |
| `slpf.py` | sequential-LP polish |
| `runloop14.sh` | driver of the run that produced the 29-725 donor |
| `hit.log` | log and transcript excerpts with source file and line numbers |

Not copied: `chainregen.py` (queue builder), the table snapshot `/inputs/plain_2026-11-04.txt` that `chain3.py:13` reads, `data/29-715.txt` and the donor cells.

## Path, username and email scan of the copied files

No usernames and no email addresses. Absolute sandbox paths:

- `chain3.py:8`, `slbfgs.py:4`, `slpf.py:4`: `sys.path.insert(0, '/work')`
- `chain3.py:13`: `/inputs/plain_2026-11-04.txt`
- `runloop14.sh:2`: `cd /work`
- `hit.log`: `/work/slpf.py` in copied warning lines and `cd /work` in copied commands

The copied code was not edited.
