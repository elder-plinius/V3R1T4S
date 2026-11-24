# A334497(37) = 49276415 (Rule 30, cyclic width 37) — bank target eca-rule30-rule110-cyclic-max-period

> Main success criterion only (exact A334497(37) from an exhaustive search by two independent implementations). Partial wins p1 (A334497(25..36)) and p2 (A204371(31..36)) are not claimed.

## What
An exhaustive search over all 2^37 cyclic configurations of elementary cellular automaton Rule 30, run on the contributor's PC by two independent implementations that agree (how-we-built-it/impl1/maxcycle.c marks every rotation orbit and converts an orbit return into a state period; how-we-built-it/impl2/maxcycle.c walks every state with a 3-colour scheme and no rotation folding), with both shipped result files in how-we-built-it/results/ reporting that the longest eventual period is 49276415 with witness 0x7fbfe703e, gives A334497(37)=49276415; a direct iteration of that witness under the Wolfram rule-number convention (cell 0 = LSB, idx=(L<<2)|(C<<1)|R) returns to itself first at step 49276415, so at none of its proper divisors; both implementations' shipped self-test log reproduces A334497(1..24) and A204371(1..30) exactly (108 OK lines, no BUG or MISMATCH) and both report A334497(25..30) as 588425, 312156, 240300, 249165, 1466066 and 374265, equal to the listed terms; both programs also reproduce the held-out terms A204371(31)=2759 and A334497(31)=2841150; the live OEIS entry and b-file for A334497, fetched 2026-11-23T23:39:09Z and again 2026-11-23T23:52:58Z, end at n=36 with a(36)=2237472, so the term was not listed at those checks; and this maximum equals the single-cell floor A334496(37)=49276415 and the sampled maximum cycle length Wolfram (1986, Table 9.2) reported for N=37, so the census shows that value is exact; no result is claimed for A334497(32..36), A334497(38) or beyond, A204371 beyond the self-test and held-out values, or partial wins p1 and p2.

A note on impl1's rotation offset: impl1 converts an orbit return into a state period with the formula k*n/gcd(r,n), which can overcount the period of a state fixed by a non-trivial rotation (at Rule 110, n = 26, it first gave 702 and direct iteration corrected it to 351, see how-we-built-it/selftest/r110_n26/err_impl1.txt). At the prime width 37 only the all-0 and all-1 states are fixed by a non-trivial rotation (under Rule 30 all-1 maps to all-0, a fixed point), so the n = 37 result is unaffected; impl1's n = 37 log (how-we-built-it/results/err_impl1.txt) shows no adjustment, and impl2 does not use the formula.

In plain words: object/a334497_37.txt records n=37, rule=30, max_period=49276415 and witness=0x7fbfe703e. Two independent C programs searched all 2^37 cyclic states of Rule 30 (one by rotation-orbit marking, one by a 3-colour walk with no rotation folding) and both reported that same maximum and the same witness. A standard-library checker re-iterates the witness under the Wolfram rule-number convention (cell 0 = LSB; idx=(L<<2)|(C<<1)|R with L=i-1 and R=i+1 cyclic) and confirms that it returns to itself at step 49276415 and at no proper divisor of 49276415. The claimed maximum equals the eventual period of a single live cell, A334496(37)=49276415, and the number Wolfram (1986) listed for N=37 in Table 9.2 of "Random sequence generation by cellular automata", which came from a selection of seeds (including single nonzero sites) and so was only a lower bound; the exhaustive search is what shows that nothing longer exists. The witness itself lies on that single-cell cycle (it is the state first entered after a transient of 260564 steps from a single live cell at position 0).

## Status note
The status of this claim is whatever panel/gate.md says. how-we-built-it/PREREG.md was frozen on 2026-11-22T16:51:29Z, before any Rule 30 width-37 computation, and is shipped unedited; its line 34 sets the conditions for CONFIRMED_SOLUTION (checks 1 to 6 pass, three fresh skeptics end pass: true, the gate copies confirmed_scope exactly, and kit/check_run.py prints CHECK_RUN: PASS). The width-37 census ran on the contributor's PC (AMD Ryzen 9 9900X, about 55 GiB visible to WSL2); it was not repeated on the packaging machine, which has far less memory than the 16 GiB and 32 GiB the two programs need.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh, sha256sum and python3 3.8+, no other packages).
Expected last line: `PASS`. About 30 to 60 seconds on a laptop (it iterates the witness 49276415 steps). verify-it-yourself/check_period.py is a standard-library checker written from the bank definition: it re-iterates the packaged witness under Rule 30 at width 37 and requires period exactly 49276415, with no shorter period among the divisors of 49276415. It does not go online and it does not re-run the exhaustive search. Re-fetch the OEIS entry and b-file yourself (URLs below) to see whether the term has been added since the snapshot in the-record-we-beat/RECORD.md. RUN_IT_YOURSELF.md also says how to rebuild and re-run the two search programs.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| OEIS A334497 b-file | A334497(37) | absent (file ends at n=36, a(36)=2237472) | https://oeis.org/A334497/b334497.txt | 2026-11-23T23:39:09Z |
| OEIS A334497 entry | A334497(37) | absent (DATA ends at 2237472; no a(37)) | https://oeis.org/A334497 | 2026-11-23T23:39:09Z |
| Wolfram (1986), Adv. Appl. Math. 7, Table 9.2, CA30 | N=37 | 49276415 (sampled seeds, a lower bound) | https://content.wolfram.com/sw-publications/2020/07/random-sequence-generation-cellular-automata.pdf | 2026-11-23T23:46:57Z |

The last published term is a(36)=2237472. The pre-registration notes the floor A334497(37) >= A334496(37)=49276415, and the bank notes that a new term must be at least Wolfram's 1986 sampled value for that width; the claimed value meets both with equality. Details and sha256s: the-record-we-beat/RECORD.md.

## Not claimed
- Partial win p1 (an exhaustive recomputation of A334497(25..36)) or p2 (an exhaustive recomputation of A204371(31..36)). Both programs did report A334497(25..30) and A334497(31), as the main criterion and the held-out check require, but those are supporting checks, not separate claims. This package contains no result for A334497(32..36).
- Any value of A334497(38) or beyond, or of A204371 beyond the self-test and held-out values. This package contains no result for those searches.
- That A334497(37) is still unpublished after 2026-11-23T23:39:09Z (the last live read of the entry).
- That the number 49276415 is new. It is the single-cell period A334496(37), and Wolfram (1986, Table 9.2) already reported it as the longest cycle found at N=37 from sampled seeds. The new work is the exhaustive census showing that no start has a longer eventual period, which makes it the exact value of A334497(37).
- Any edit or upload to OEIS.

## Credits
- The On-Line Encyclopedia of Integer Sequences, A334497 (Rule 30 maximum eventual period; a(1)-a(7) by Bradley Klee; later terms from the references in the entry): https://oeis.org/A334497
- OEIS A334496 (eventual period of a single cell under Rule 30), which is the floor for this term: https://oeis.org/A334496
- OEIS A204371 (Rule 110, used for the required small-n reproduction and the held-out check): https://oeis.org/A204371
- Stephen Wolfram, "Random sequence generation by cellular automata", Advances in Applied Mathematics 7 (1986) 123-169, Table 9.2, whose sampled cycle lengths for N=37..54 are lower bounds, not exhaustive terms; its N=37 entry, 49276415, is the value confirmed here. The table credits Holly Peck and Tsutomu Shimomura for its larger-N results. https://content.wolfram.com/sw-publications/2020/07/random-sequence-generation-cellular-automata.pdf
- Gage, Laub and McGarry (2005), "Cellular Automata: Is Rule 30 Random?", Table 2, the source OEIS used for later A334497 terms: https://homes.luddy.indiana.edu/dgerman/2005midwestNKSconference/dgelbm.pdf
- Bradley Klee, Jinyuan Wang, Pontus von Brömssen and Paolo Xausa, for earlier A334497 ranges named in the bank target.
- The two search programs are the ones reviewed with the Rule 110 width-37 claim A204371(37)=4403 (V3R1T4S PR #1173), byte-identical.
- Contributor: whosedreams (V3R1T4S kit).
