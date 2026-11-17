# How we found it (contributor text, unverified)

**Brief.** Charter quarry 11 takes Justin Sun Prize catalog problems; JSP-000550 is Erdős Problem 677: must
M(m, k) = lcm(m+1, …, m+k) differ from M(n, k) whenever m ≥ n + k? Earlier runs of this workspace built and panelled
the method (Lemma A, a complete small-X search, a margin proved in exact rational intervals and a continued-fraction
enumeration to q ≤ 10^495) and confirmed it for k ≤ 25 and 26 ≤ k ≤ 28 (separate packages). A cost forecast on
2026-11-07 said k = 29 (114817 ratios, five times k = 28) would fit a standard run if the exact margin checker were
split by ratio like the enumeration. Run 2026-11-09-0917 pre-registered the claim "for k = 29, every n ≤ 10^494 and
every m ≥ n + k, M(m,k) ≠ M(n,k)" (`how-we-built-it/PREREG.md`).

**What worked.** Two lenses ran.
- *extender-r3* ran the enumeration (deep_rig.py, unchanged) on 4 shards: 0 product solutions, 3288852 window
  candidates, the shards' ratio counts adding up to 114817.
- *rigor* reran the small-X search (complete, k = 29 line cand = 0), audited the ratio set (114817, 0 missing),
  proved the margin in interval arithmetic on the whole list, and in exact rational intervals on 4 shards through a
  new wrapper, `object/shard_margin.py`, which only restricts the ratio list (tested on k = 5..12 against the
  unsharded program; `object/out/wrap_test/`). 0 failures and 0 undecided everywhere.
- The claim's `object/PROOF.md` writes out the Step 4 reduction, which earlier claims left in code comments, and the
  claim carries the patch note of the enumeration's float pre-filter; both had been noted as gaps by an earlier panel.

**What failed.** The forecast: the enumeration took 1.5 h on 4 cores instead of 0.9 h (the per-ratio cost grows with
k), so the run went past its usual 3 h. The panel could not fit the same night. k = 30 and 31 need about 5 and 9 hours
on 4 cores before a panel (cost table of run 2026-11-10-0917).

**Panel.** Run 2026-11-10-0917 panelled the claim with three fresh-context skeptics who read only the claim folder.
REPRODUCE reran every step in full (the enumeration and the exact margin on 4 shards each, about 3950 and 2600 s per
shard on that night's machine), with every output identical to the saved one apart from times, and checked the method
with its own code: Lemma A on 3139 equal-lcm pairs, its own ratio set, its own small-X search, an exact-integer
enumerator agreeing with the program on 363 ratio checks (63 at the full q ≤ 10^495) and an independent margin
expansion on 3039 ratios. CRITERION checked the statement's quantifiers, the seam at X = 10^6 and the odd-k mapping,
and re-derived the Step 4 algebra. NOVELTY found the best posted computation (m + k ≤ 10^8) reaches "every m" only to
n ≈ 4.2·10^7. The gate (`panel/gate.md`) wrote CONFIRMED_PARTIAL with CRITERION's scope sentence.
