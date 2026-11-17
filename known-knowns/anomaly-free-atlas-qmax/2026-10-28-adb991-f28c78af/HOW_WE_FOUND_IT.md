# How we found it (contributor text, unverified)

**Brief.** Earlier runs of this workspace had pinned the atlas convention and confirmed the census up to SMnuR
Q_max 18 and SM Q_max 31 (three earlier submissions). Runs on 2026-10-21/22 had already computed SMnuR 19 and SM
32..35, but run 2026-10-22-0818 could only write `PROMISING`: its novelty skeptic could not read the paper then, and
its claim folder was assembled 42 s before its pre-registration. Run 2026-10-28-0820 re-panelled the same rows from
scratch. Its pre-registration (`how-we-built-it/PREREG.md`, frozen 2026-10-28 08:21:31 UTC before any attack output)
required, for every row and within this run: the full list streamed through the C checker with PASS and "valid
solutions" = count - 1, its sha256 recorded, and agreement with at least two independent counters; all five rows or
no claim.

**What worked.**
- *extender-lists*: the listers were first tested on certified rows (SMnuR 12 and SM 20 hashes equal to their
  certified values). Then `acclist Q 0` for SM 32..35 (217, 272, 373, 453 s) and `csenum2 19 1 40 3` for SMnuR 19
  (5192 s, 3 threads, up to 4.35 GB of bucket memory) were streamed through `sha256sum` and `checklist` with
  `set -o pipefail`: all PASS, line counts = count - 1, and every hash equal to the 2026-10-21/22 record.
- *counters*: `mitm.c` (meet in the middle, never lists) gave all five counts; `count.c` + `conventions.py` gave
  SM 32 and 33 (equal). count.c for SM 34, 35 and SMnuR 19 was stopped to free a core for the panel, since every row
  already had the lister + checker and mitm.

**What failed.** Nothing disagreed. The run's own REPRODUCE.md understated the memory of the SMnuR 19 lister ("< 3
GB"; the log shows 4.35 GB); the gate noted it and this package states about 4.4 GB. The author's `checklist.c`
accepts whitespace variants and an empty stream, so the sha256, the lister's exit status and the comparison of the
line count with the expected count are what bind the bytes.

**Panel.** REPRODUCE wrote its own checker and counters from the definition before reading any code, validated
them by brute force and mutation tests, regenerated all five lists in full (SMnuR 19 in 5708 s) with matching
hashes, and its counters gave all five counts and all 40 published values. CRITERION checked the convention against
the paper's text and the alternatives (only the claimed one reproduces the tables) and regenerated SM 32 itself.
NOVELTY read the arXiv record, the Zenodo data record (last version holds Q_max <= 10), the 121 INSPIRE citing
records, arXiv and Zenodo searches and all 774 V3R1T4S pull-request heads: no census past Q_max 10. The gate wrote
CONFIRMED_SOLUTION on 2026-10-28 (`panel/gate.md`).
