status: CONFIRMED_PARTIAL
confirmed_scope: For k = 29, every 0 ≤ n ≤ 10^494 and every m ≥ n + 29 (m unbounded), lcm(m+1, …, m+29) ≠ lcm(n+1, …, n+29), established by a computer-assisted, not kernel-checked certificate (Lemma A, a complete small-X search for n + 29 ≤ 1.1·10^6, an exact-rational-interval margin for X ≥ 10^6, and a continued-fraction enumeration to q ≤ 10^495 whose window bounds and candidate generation use high-precision/float arithmetic with error bounds and brute-force validation rather than interval arithmetic) — a workspace partial win for `Erdos677.erdos_677`, not a prize solution.

Gate (RUN.md step 7), run 2026-11-10-0917, written 2026-11-10T11:11:43Z after reading all three panel files in full.

- panel/reproduce.md: pass: true. Every REPRODUCE.md step rerun in full on the whole ratio list: small-X search and
  exact verification, ratio audit (byte-identical), rig_margin.py on 114817 ratios, the exact margin on 4 shards
  (28705 + 3 × 28704 pairs, 0 failures, 0 undecided) and the enumeration on 4 shards, every output identical to the
  saved one apart from times (sums 114817 / 3332527 / 3288852, 0 product solutions). Own checks: Lemma A on 3139
  equal-lcm pairs (0 violations), its own ratio set equal to admissible_r(29), its own small-X search (0 candidates),
  an exact-integer enumerator agreeing with enum_pairs on 300 ratios at q <= 3000 and on 63 ratios at q <= 10^495
  (incl. the 10 with the largest partial quotients), and an independent margin expansion on 3039 ratios.
- panel/criterion.md: pass: true, partial win 1 (not the full criterion, not partial win 2). Statement, seam, upper
  end and odd-k mapping checked; the Step 4 algebra re-derived; confirmed_scope above is its sentence, copied exactly.
- panel/novelty.md: pass: true. Catalog JSP-000550 Open, Lean proof No (2026-11-10T09:20:41Z); best posted
  computation laaielichter/erdos-677 (m + k <= 10^8), giving "every m" only to n ≈ 4.2·10^7 at k = 29.

The main session's reading found nothing to downgrade. Recorded, not decisive:
- The enumeration's window bounds, s-interval generation and float pre-filter are not interval arithmetic (stated in
  the scope); both skeptics judged the error negligible against the measured slack.
- PROOF.md Step 5 item 4 says "an interval" where the admissible s can form two pieces; the code handles both.
- deep_rig.py's docstring says 1050 digits (the code uses 1090); the enumeration outputs do not print η or the digit
  count (CRITERION inferred η = 10^-3 from a 1/1000 shard).
- A stray __pycache__/deep_cf.cpython-313.pyc appeared in claim/object at 2026-11-10T09:20:33Z, during the panel; it
  is not part of the frozen claim, affects no output, and was removed after this gate.
