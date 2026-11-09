# PREREG v2 (written 2026-11-02T04:48:19Z per date -u; neither Program A nor Program B has produced A364417(20) yet - A is mid-sweep, B not started)

Everything in PREREG.md stays frozen except ONE change to Program B's arithmetic:
- Reason: memory. Program A's (20,37) sweep peaked at ~3.4 GB RSS with ~7 GB of the machine used by other processes;
  the 128-bit packed-slot build of Program B (benzB128) needs ~1.5x A's memory and would exceed half of the free memory
  (kit/RULES.md rule 10).
- Change: Program B = attempts/contrarian/code/benzB64.c, identical to benzB128.c except (a) counts are u64 with every
  addition overflow-checked (any overflow sets a flag, the run prints OVERFLOW and the result is void), and (b) hash load
  factor 0.9. This is still exact integer arithmetic whenever the run reports overflow 0; it replaces "exact 128-bit or
  multi-modulus arithmetic" in PREREG.md's Program B line. benzB64 reproduces A364416(3,6,9,12,14) and A364417(3,6,9,12,14)
  (smoke test before this file). The published-term reproductions already run with benzB128 stay valid for B's region,
  ordering and pruning code (the counting logic is the same source).
- Unchanged: Program A = benzZQ.c, its reproduction duty (all published A364416(3..20), A364417(3..19)), the claim rule
  (A == B exactly, both overflow-free, DATA re-fetched immediately before claiming still lacks the term), thresholds,
  null_test line.
