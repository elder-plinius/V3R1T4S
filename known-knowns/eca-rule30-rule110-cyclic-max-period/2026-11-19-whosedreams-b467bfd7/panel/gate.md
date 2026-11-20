# Honesty gate: packaging run 2026-11-19-eca37-pack, eca-rule30-rule110-cyclic-max-period, A204371(37)=4403, main success criterion

context: written 2026-11-19T01:57:04Z (date -u) by the parent, after reading panel/reproduce.md, panel/novelty.md and
panel/criterion.md in full. Each panel file was written on 2026-11-18 (evening, America/New_York) in its own fresh
subagent context. No vote was changed, re-run or written here.

## Panel files
- reproduce.md: pass: true. Own Rule 110 iterator: witness 0x1c7dbbb23e has first return 4403, none at proper divisors
  1, 7, 17, 37, 119, 259, 629. Own exhaustive census (no symmetry folding) matches live A204371(1..22) and A334497 at
  Rule 30 n=1..20. Source audit of both impls passed (Wolfram bit order, eventual image, rotation conversion, no reflection).
  Rebuilt impls matched the census at every tested width and both returned held-out A204371(32)=2368. 2^37 census not repeated.
- novelty.md: pass: true. Live OEIS 2026-11-18 20:39:25-20:39:26 ET: A204371 entry and b-file end at n=36 (a(36)=1584);
  no pending draft; history shows no a(37). No upstream V3R1T4S claim; no published exhaustive width-37 Rule 110 value.
  Framed honestly: 4403 equals the A180001(37) floor; the new content is the exhaustive upper bound.
- criterion.md: pass: true. Full main criterion met, not a partial win. TARGET_CRITERION.md verbatim; selftest 120 OK lines;
  A334497(25..30) match live terms; independent OEIS refetch 2026-11-19T01:39:52Z shows no a(37).

## Downgrade check (kit/RUN.md step 7)
- Hedging panelist: no; all three pass outright.
- Reproduction mismatch: none.
- Value not already listed: yes, A204371 has no n=37 term at three independent live fetches (20:26, 20:39, 20:39 ET), all under 6 hours old at this gate.
- Stretched criterion or hidden quantifier: no. Equality with the single-cell floor is allowed by the bank text and disclosed.
- Scope wider than reproduced: no. The 2^37 census ran on the user's PC and was not repeated on the box (16 GiB bitset vs 15 GiB here);
  the panel accepted the witness iteration, held-out reruns (n=31, n=32) and source audit as the kit requires. Disclosed in README.md.
- Several results bundled: no; A334497(37), p1 and p2 are not claimed.
- Plan frozen after the search: yes, disclosed in how-we-built-it/PREREG.md.
Result: no downgrade.

status: CONFIRMED_SOLUTION
confirmed_scope: An exhaustive search over all 2^37 cyclic configurations of elementary cellular automaton Rule 110, carried out by two independent implementations that agree (how-we-built-it/impl1/maxcycle.c marks every rotation orbit and converts an orbit return into a state period; how-we-built-it/impl2/maxcycle.c walks every state with a 3-colour scheme and no rotation folding), both reporting in how-we-built-it/results/ that the longest eventual period is 4403 with witness 0x1c7dbbb23e, so A204371(37)=4403; a direct iteration of that witness under the Wolfram rule-number convention (cell 0 = LSB, idx=(L<<2)|(C<<1)|R) returns to itself at step 4403 and at none of the proper divisors 1, 7, 17, 37, 119, 259 or 629; both implementations' shipped self-test log reproduces A334497(1..24) and A204371(1..30) exactly (120 OK lines, no BUG or MISMATCH) and both report A334497(25..30) as 588425, 312156, 240300, 249165, 1466066 and 374265; the live OEIS entry and b-file for A204371, fetched 2026-11-19T01:39:52Z, still end at n=36 with a(36)=1584, so the term was not listed at this check; and this maximum equals the single-cell floor A180001(37)=4403.
