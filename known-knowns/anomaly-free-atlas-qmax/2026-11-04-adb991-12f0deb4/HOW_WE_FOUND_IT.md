# How we found it (contributor text, unverified)

**Brief.** Earlier runs of this workspace pinned the atlas convention and confirmed the census up to SMnuR Q_max 19
and SM Q_max 35 (four earlier submissions). Run 2026-11-02-0920 listed and checked SM 36..38, but its SMnuR 20 list
was killed by the session's memory cgroup (about 7.4 GB) in pass 28 of 40, so it made no claim. Run 2026-11-03-0919
pre-registered the four rows as one claim (`how-we-built-it/PREREG.md`): for every row and within that run, the full
list streamed through the C checker with PASS and "valid solutions" = count - 1, its sha256 recorded, and agreement
with `mitm.c`; all four rows or no claim. The three-skeptic panel did not fit in that run's budget, so the claim was
labelled single-context and unpanelled, and the next run's first job was its panel.

**What worked.**
- *extender-lists* (2026-11-03): `csenum2 20 1 80 3` (80 memory passes instead of 40; 7112 s on 3 threads, peak
  resident memory 4.66 GB, logged every 30 s with a stop line at 6.0 GB) and `acclist Q 0` for SM 36..38 (540, 660,
  843 s), each streamed through `sha256sum` and `checklist` with `set -o pipefail`: all PASS, line counts = count - 1,
  SM hashes equal to the 2026-11-02 record.
- *counters*: `mitm.c` gave all four counts (and the certified regression rows SMnuR 12, SM 20).
- *memory-plan*: per-pass bucket memory is about 17 bytes per line at capacity; the heaviest pass at 80 passes held
  208M lines (4.35 GB bucket) against 383M at 40 passes (6.53 GB).

**What failed.** `count.c` was run beside the lister as an optional third code and was itself killed by the memory
limit at SM q = 37 and 38 (about 10 GB): it was not sized first, and it could have taken the lister down instead.
The SMnuR 20 attempt at 40 passes (2026-11-02) failed the same way.

**Panel** (2026-11-04, three fresh subagent contexts, each given only the claim folder). REPRODUCE wrote its own
streaming checker and two counters from the definition before reading any code, regenerated all four lists in full
(SMnuR 20 in 7053 s) with matching hashes, validated every line with its own (stricter) checker, and its
meet-in-the-middle counter gave all four counts and all 40 published values; a nesting check (count(Q) - count(Q-1) =
lines touching the bound) held. NOVELTY fetched the arXiv record and the Zenodo release (last version 1.1.0, files up
to Q_max 10), ran 16 arXiv searches over 24 months, Zenodo and GitHub code searches, and searched the commit messages
and file trees of all 908 V3R1T4S pull-request heads: no census past Q_max 10. CRITERION checked the convention
against the paper's values and the alternatives and accepted code-regenerated lists pinned by sha256 as the
certificate. The gate wrote CONFIRMED_SOLUTION on 2026-11-04 (`panel/gate.md`).
