# A204371(37) = 4403 (Rule 110, cyclic width 37) — bank target eca-rule30-rule110-cyclic-max-period

> Main success criterion only (exact A204371(37) from an exhaustive search by two independent implementations). Partial wins p1 (A334497(25..36)) and p2 (A204371(31..36)) are not claimed.

## What
An exhaustive search over all 2^37 cyclic configurations of elementary cellular automaton Rule 110, carried out by two independent implementations that agree (how-we-built-it/impl1/maxcycle.c marks every rotation orbit and converts an orbit return into a state period; how-we-built-it/impl2/maxcycle.c walks every state with a 3-colour scheme and no rotation folding), both reporting in how-we-built-it/results/ that the longest eventual period is 4403 with witness 0x1c7dbbb23e, so A204371(37)=4403; a direct iteration of that witness under the Wolfram rule-number convention (cell 0 = LSB, idx=(L<<2)|(C<<1)|R) returns to itself at step 4403 and at none of the proper divisors 1, 7, 17, 37, 119, 259 or 629; both implementations' shipped self-test log reproduces A334497(1..24) and A204371(1..30) exactly (120 OK lines, no BUG or MISMATCH) and both report A334497(25..30) as 588425, 312156, 240300, 249165, 1466066 and 374265; the live OEIS entry and b-file for A204371, fetched 2026-11-19T01:39:52Z, still end at n=36 with a(36)=1584, so the term was not listed at this check; and this maximum equals the single-cell floor A180001(37)=4403.

A note on impl1's rotation offset: impl1 converts an orbit return into a state period with the formula k*n/gcd(r,n), which can overcount the period of a state fixed by a non-trivial rotation (at Rule 110, n = 26, it first gave 702 and direct iteration corrected it to 351, see how-we-built-it/selftest/err_r110_n26_i1.txt). At the prime width 37 only the all-0 and all-1 states are fixed by a non-trivial rotation, so the n = 37 result is unaffected.

In plain words: object/a204371_37.txt records n=37, rule=110, max_period=4403 and witness=0x1c7dbbb23e. Two independent C programs searched all 2^37 cyclic states of Rule 110 (one by rotation-orbit marking, one by a 3-colour walk with no rotation folding) and both reported that same maximum and the same witness. A standard-library checker re-iterates the witness under the Wolfram rule-number convention (cell 0 = LSB; idx=(L<<2)|(C<<1)|R with L=i-1 and R=i+1 cyclic) and confirms that it returns to itself at step 4403 and at no proper divisor of 4403. The claimed maximum equals the eventual period of a single live cell, A180001(37)=4403; the exhaustive search is what shows that nothing longer exists. The witness itself lies on that single-cell cycle (it is the state first entered after a transient of 192 steps from a single live cell at position 0).

## Status note (added 2026-11-19, after maintainer review of PR #1173)
This run issued status CONFIRMED_SOLUTION (panel/gate.md). how-we-built-it/PREREG.md is left as frozen. The last sentence of its line 19 ("This packaging run writes PROMISING and does not stamp CONFIRMED_*") described the single-context packaging step, which was written before any review panel existed, and was not followed for the final status: after packaging, three skeptics in fresh contexts (panel/reproduce.md, panel/novelty.md, panel/criterion.md) each ended pass: true, the parent gate copied the criterion panelist's confirmed_scope exactly, and kit/check_run.py printed CHECK_RUN: PASS, which are the conditions the first sentence of PREREG.md line 19 sets for CONFIRMED_SOLUTION. The gate was therefore written as CONFIRMED_SOLUTION rather than PROMISING.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh, sha256sum and python3 3.8+, no other packages).
Expected last line: `PASS`. A fraction of a second on a laptop. verify-it-yourself/check_period.py is a standard-library checker written from the bank definition: it re-iterates the packaged witness under Rule 110 at width 37 and requires period exactly 4403, with no shorter period among the divisors of 4403. It does not go online and it does not re-run the exhaustive search. Re-fetch the OEIS entry and b-file yourself (URLs below) to see whether the term has been added since the snapshot in the-record-we-beat/RECORD.md. RUN_IT_YOURSELF.md also says how to rebuild and re-run the two search programs.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| OEIS A204371 b-file | A204371(37) | absent (file ends at n=36, a(36)=1584) | https://oeis.org/A204371/b204371.txt | 2026-11-19T01:26:03Z |
| OEIS A204371 entry | A204371(37) | absent (DATA ends at 1584; no a(37)) | https://oeis.org/A204371 | 2026-11-19T01:26:18Z |

The last published term is a(36)=1584. The bank also notes the floor A204371(37) >= A180001(37)=4403; the claimed value meets that floor with equality. Details and page sha256s: the-record-we-beat/RECORD.md.

## Not claimed
- Partial win p1 (an exhaustive recomputation of A334497(25..36)) or p2 (an exhaustive recomputation of A204371(31..36)). Both programs did report A334497(25..30), as the main criterion requires, and a held-out rerun at Rule 110 width 31 agreed with the listed term 2759, but those are supporting checks, not separate claims.
- That A204371(37) is still unpublished after 2026-11-19T01:26:18Z (the last live read of the entry).
- Any value of A334497(37) (Rule 30 at the same width). This package contains no result for that search.
- That 4403 is larger than the single-cell period. It is equal to it. The new work is the exhaustive census showing that no start has a longer eventual period.
- Any edit or upload to OEIS.

## Credits
- The On-Line Encyclopedia of Integer Sequences, A204371 (Ben Branman, Jan 14 2012; a(19)-a(36) from Lars Blomberg, Dec 24 2015): https://oeis.org/A204371
- OEIS A180001 (eventual period of a single live cell under Rule 110), which is the floor for this term: https://oeis.org/A180001
- OEIS A334497 (Rule 30, used for the required small-n reproduction and the A334497(25..30) report): https://oeis.org/A334497
- Stephen Wolfram, "Random sequence generation by cellular automata" (1986), whose sampled cycle lengths for larger widths are lower bounds, not exhaustive terms.
- Gage, Laub and McGarry (2005), Table 2, the source OEIS used for later A334497 terms: https://homes.luddy.indiana.edu/dgerman/2005midwestNKSconference/dgelbm.pdf
- Bradley Klee, Jinyuan Wang, Pontus von Brömssen and Paolo Xausa, for earlier A334497 ranges named in the bank target.
- Eric Weisstein, Rule 110: https://mathworld.wolfram.com/Rule110.html
- Contributor: whosedreams (V3R1T4S kit).
