# How we found it (contributor text, unverified)

**Brief.** This run (2026-10-18, the second of the day on this target) resumed a live lead. The run before it had
pinned the atlas convention by reproducing every published value and listed SM Q_max 11..20 and SMnuR Q_max 11, 12;
its counters had also counted SMnuR up to 18 and SM up to 31 without lists. What was missing past Q_max 12 was a way
to certify lists that are too large to store. The pre-registration (`how-we-built-it/PREREG.md`, frozen 08:18:58 UTC
before any attack output of this run) required, for every row: an explicit list, a checker PASS with "valid
solutions" equal to the list's line count, and an independent counter giving that count + 1.

**What worked.**
- *extender*: a streaming C checker (`verify-it-yourself/checklist.c`) with the rules of the Python checker; it
  agreed with the Python checker on all 29 lists of the previous run and on 7 targeted negatives, one per rule. With
  it, a list is generated, hashed and checked in one stream and never stored. SMnuR 13 from `acclist.c`: 180207251
  lines in 225 s, Python and C checker PASS. SM 21..31 from `acclist.c`: C checker PASS on every row (SM 31: 13425698
  valid lines in 304 s). SMnuR 14..16 from the second lister, streamed: PASS in 277, 529 and 1020 s.
- *construct-space*: a second lister written independently (`csenum.c`): a hash join per pair of free linear sums,
  canonicalised to max(F, -F), sorted in memory passes on the first canonical charge and merged, on two threads.
  Its output is byte-identical to `acclist.c` wherever both ran (SMnuR 10..13, SM 1..20) and it reached SMnuR 16 in
  577 s with bounded memory.
- *smuggler*: a third, independent exact counter (`rcount.c`, power sums per species, Burnside and Moebius) that
  reproduces every count, and a circle-method explanation of the growth: R(Q) ~ S J (Q + 1/2)^9 for SMnuR with
  S J = 707 +- 5, plus a period-3 correction (heuristic, not part of the claim).

**What failed.** `acclist.c` at SMnuR 14 would have needed half-tables of about 2 x 4.4 GB on a shared 15 GB
machine and was not run; storing lists past 13 (about 3.5 GB gzip each) did not fit the 8 GB of free disk, hence
streaming. In the second lister, holding every block's build table at once (about 1.5 GB at Q_max 13) and one global
in-memory sort were replaced by passes on the first charge. No short P-recursive relation (order <= 4) fits the
counts, and they are not a quasi-polynomial of small period.

**Panel.** REPRODUCE regenerated all 25 rows in full with its own counter and its own strict checker (hashes and
line counts equal to `object/counts.txt`) and CRITERION passed on 2026-10-18; NOVELTY could not read the table and
returned PENDING STATUS CHECK (`panel/novelty_round1_pending.md`), so the gate wrote PROMISING. On 2026-10-23 the
workspace owner supplied the paper (v5) and the erratum as PDFs; a fresh NOVELTY skeptic read them (largest published
Q_max is 10 for both contents) and passed, all 40 published numbers were matched by the counters, and the gate's
second round wrote CONFIRMED_SOLUTION (`panel/gate.md`).
