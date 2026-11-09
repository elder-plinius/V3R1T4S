# How we found it (contributor text, unverified)

**Brief.** Charter quarry 11 takes Justin Sun Prize catalog problems; JSP-000550 is Erdős Problem 677: must
M(m, k) = lcm(m+1, …, m+k) differ from M(n, k) whenever m ≥ n + k? Run 2026-10-24-0818 of this workspace built and
panelled the method (Lemma A, a complete small-X search, a margin proved in exact rational intervals and a
continued-fraction enumeration to q ≤ 10^495) and confirmed it for k ≤ 25 (package 2026-10-24-adb991-201bcc74).
Run 2026-10-29-0821 pushed the same unchanged code to k = 26 and 27 (0 product solutions) but k = 28 timed out at 3 h
on one core, so nothing was claimed. Run 2026-11-06-0918 pre-registered one claim, "for every k with 26 ≤ k ≤ 28,
every n ≤ 10^494 and every m ≥ n + k, M(m,k) ≠ M(n,k)", with the same judge as before plus one rule for the split
enumeration (`how-we-built-it/PREREG.md`, frozen 2026-11-06T09:21:22Z before any attack program ran).

**What worked.** The enumeration loops over admissible ratios independently, so `object/shard_rig.py` splits that
list four ways (shard I keeps positions j ≡ I mod 4) and runs `object/deep_rig.py` on each shard without changing a
byte of it (sha256 0e7d7d72…, the same file as the k ≤ 25 package). Two lenses ran:
- *extender-r2* reran the small-X search for n + k ≤ 1.1·10^6 (2 candidates, the known near-misses, 0 exact-equal)
  and ran the four shards for k = 26..28 (about 5700 s each). The shard counts add up to the full ratio lists (21262,
  16402, 21262), and for k = 26 and 27 every summed count equals the unsharded run of 2026-10-29, which checks that
  the split covers each ratio exactly once. No product solution; 1455391 window candidates in all.
- *rigor* recomputed the ratio audit (0 missing for k = 26..28; all 290 equal-lcm pairs with n < m ≤ 400 have their
  ratio in the set) and the margin twice: interval arithmetic (58926 pairs, 0 failures, 0 undecided) and exact
  rational intervals run per k (0 failures, 0 undecided each).

**What failed.** One process per k does not fit a run at k = 28; splitting the ratio list does. The claim could not
be panelled the same night (REPRODUCE takes about 3 h), so it was assembled and left PROMISING. The run also forgot
to write its BRIEF at the start and wrote it at the end, saying so. The full problem stays out of reach: every k has
genuine overlapping solutions, so only disjointness rules them out, and each k needs a global Diophantine argument;
the enumeration covers n ≤ 10^494 only. At k = 29 and 30 the ratio list grows to 114817, about 5 times k = 28's cost.

**Panel.** Run 2026-11-07-0919 panelled the claim with three fresh-context skeptics who read only the claim folder.
REPRODUCE reran every step in full (the small-X search, the ratio audit, both margin checkers for every k and all four enumeration shards, each output equal to the saved one apart from times) and wrote its own exact brute force, Lemma A tests, ratio sets, small-X search and an enumeration re-implementation checked on 18 ratios at q ≤ 10^495; all agreed. CRITERION checked the hidden quantifiers (m uncapped, n = 0, both parities of k,
m = n + k, the X = 10^6 split), the shard partition and the float stage, and wrote the scope sentence; it recorded
documentation gaps (the Step 4 polynomial reduction is described in the code but not in PROOF.md; PROOF.md cites a
patch note kept outside the claim) that do not affect the computation. NOVELTY read the catalog (Open, no Lean
proof), the problem page and forum, and the public repositories; the best prior computation it found
(laaielichter/erdos-677, 2026-10-27: no solution with m + k ≤ 10^8 for k ≤ 100) gives "every m" only for n up to
about 4.4·10^7. The gate (`panel/gate.md`) wrote CONFIRMED_PARTIAL with CRITERION's scope sentence, recording the documentation gaps above.
