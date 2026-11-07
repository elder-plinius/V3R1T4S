# PREREG — run 2026-11-07-1158, target wieferich-other-bases-fischer-table

frozen_utc: 2026-11-07T12:03:29Z (date -u read immediately before writing this file). No attack output exists yet.
The only results so far come from below-limit and below-1e12 self-tests: code/checker_output.txt,
attempts/frontier-archivist/code/selftest_output.txt, attempts/object-as-data/code/p1_known_positives_output.txt.

## Criterion and partial win judged (verbatim in target.md)
- Full win: new pair (b, p), 1053 <= b <= 10125 here, b not a perfect power, p proven prime, pow(b, p-1, p^2) == 1,
  p > 4.8E+12 (the live FermQ_Sorg.txt limit), p absent from row b of both Fischer files and from OEIS.
- Partial win p1: "New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12,
  b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS."

## What will judge a result (fixed now)
- Checker: code/wieferich_check.py (selftest PASS, code/checker_output.txt). A pair passes only if b is in range
  (full win: 3..10125; p1: run as `wieferich_check.py b p 10126 65536`), b is not a perfect power, p is a proven
  prime (deterministic Miller-Rabin, 12 bases, valid below 3.18e23; BPSW second opinion), p does not divide b, and
  pow(b, p-1, p*p) == 1 in exact integers.
- Table rule, checked right before any claim with one fresh honest request each:
  - Full win: p > 4.8E+12 and p absent from row b in FermQ_Sorg.txt and FermQ_Sort.txt.
  - p1: p > 1e12, b has no row in either file, and p appears nowhere in either file.
  - Both: OEIS search for p (one request, oeis.org/search?q=<p>&fmt=data) returns no sequence listing p as a
    Wieferich prime for base b.
- Thresholds: exact equality only. The float64 screen inside the sweep is a filter with a proven no-false-negative
  margin (2^-40 tolerance vs 2^-47 worst-case error at p < 2^43), and every flag is re-checked exactly.

## Attack plan (frozen before it runs)
- Lens frontier-archivist (attempts/frontier-archivist): wieferich_sweep.py sweep from 4814700000000 (run 1's
  frontier), blocks of 2e7, 15 workers at IDLE priority, B = 70, bases 1053..10125 (2360), MAX_HI 6e12.
- Lens object-as-data (attempts/object-as-data): wieferich_sweep.py sweep from 1000000000000 (p > 1e12 strictly;
  1e12 is even), blocks of 2e7, 15 workers at IDLE priority, B = 70, bases 10126..65536 (6852), MAX_HI 1.5e12.
- Both: no new block after 2026-11-07T12:38:00Z (epoch 1794055080); outer cap `timeout 2700`.
- Any exact hit → steps 5-7 (own break attempt, three fresh-context skeptics, gate) for that pair as its own claim.
  One pair per claim.
- Coverage statements allowed afterwards: only the maximal contiguous run of completed blocks of each lens, stated
  exactly, for that lens's base set only, labelled NUMERICAL.

## Null design
null_test: not needed because every claim is an explicit object (b, p) judged by a deterministic exact checker (one modular exponentiation plus a primality proof) against the live tables and OEIS; no score, statistic or "beats chance" inference is involved.

## Baseline (RUN.md step 3c)
Not an empirical benchmark: no published baseline to reproduce.
