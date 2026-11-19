# Criterion review

context: subagent

Claim: A204371(37)=4403, under the main success criterion of bank target eca-rule30-rule110-cyclic-max-period. Partial wins p1 and p2 are not claimed. Each clause of the bank success criterion is checked below against the package, the bank text, and checks run in this review. File names are relative to the claim package.

## Bank text and write-up

how-we-built-it/TARGET_CRITERION.md copies the bank success_criterion paragraph, the p1 statement, the p2 statement, and the status_source URL verbatim. README.md claims only A204371(37), states that p1, p2 and any value of A334497(37) are not claimed, and states that 4403 equals the single-cell floor A180001(37) rather than exceeding it. That language does not overclaim.

## Exhaustive search over all 2^37 states, or all rotation orbits with the rotation factor accounted for

how-we-built-it/impl1/maxcycle.c walks every start in 0 .. 2^n-1, marks each rotation orbit once (reflection is not used), and when a walk closes on a rotate of a state already on the path, converts the orbit return f^k(s)=rot_r(s) into a state period by k*n/gcd(r,n), then checks the recorded witness by direct iteration. how-we-built-it/impl2/maxcycle.c is a 3-colour (white/grey/black) walk of the functional graph with no rotation folding: every state is visited, and a hit on a grey state gives the period as the stack distance. Both match the bank's allowed methods, and both, on inspection, would be exhaustive if run to completion. The n=37 census itself is represented by the shipped result files in how-we-built-it/results/; it was not re-executed in this review (impl1 needs a 16 GiB bitset and impl2 a 32 GiB colour array). The bank verification method asks for witness iteration, a held-out-width rerun, and inspection of the exhaustive code, not a second full 2^37 run. Those are all present: the witness is checked below; both programs were re-run at Rule 110, n=31 in how-we-built-it/heldout/ and both reported max_period=2759, the listed A204371(31), whose period was re-confirmed here by direct iteration of witness 0x3f647ff8 (return at 2759, not at 1, 31 or 89). That held-out value is not the single-cell floor (A180001(31)=7). Under the kit rules, the shipped n=37 result files plus inspectable exhaustive source, agreeing independent implementations, a passing self-test record, and a held-out rerun of the same source are adequate evidence that the term comes from an exhaustive search.

## Two independent implementations that agree

The two programs share a Wolfram neighbourhood step (cell 0 = LSB; idx=(L<<2)|(C<<1)|R) and output format, but they compute periods by different algorithms: orbit marking with a rotation-offset formula versus a 3-colour walk with no folding. That is independent enough for this criterion. The shared step is the bank's required bit-order convention, and a shared bug there would have broken the small-n reproductions. They can disagree before correction: at Rule 110, n=26, impl1's formula first produced 702 and the program's own direct-iteration check adjusted it to 351 (how-we-built-it/selftest/err_r110_n26_i1.txt), while impl2 reported 351 directly; the self-test log records both as 351, matching the listed term. For n=37 both result files, and both witness files, report max_period=4403 and witness=0x1c7dbbb23e:

- how-we-built-it/results/result_impl1.txt: rule=110 n=37 max_period=4403 witness=0x1c7dbbb23e time_sec=1699.3565 impl=1
- how-we-built-it/results/result_impl2.txt: rule=110 n=37 max_period=4403 witness=0x1c7dbbb23e time_sec=11946.5399 impl=2

object/a204371_37.txt records the same n, rule, period and witness (sha256 b467bfd76e68bdac2f2738c7436a1455c8a6379b9b336a5cb75032320a0b412d, matching INDEX.csv and verify-it-yourself/OBJECT_SHA256).

The same sources, compiled and re-run in this review at Rule 110 widths 12, 18, 20 and 22 and Rule 30 widths 12, 18 and 20, agreed with each other and with the live listed terms in each case.

## Both reproduce A334497(1..24) and A204371(1..30) exactly; both report A334497(25..30)

how-we-built-it/selftest/selftest.log has 120 OK lines and no BUG or MISMATCH lines. Parsed against the live b-files: both implementations match A334497(1..24) and A204371(1..30) in every cell (48+60 records), and both report A334497(25..30) as 588425, 312156, 240300, 249165, 1466066 and 374265 (12 records), which are exactly the live listed terms, so p1's correction rule is not invoked. Those reports are a required supporting check, not a p1 claim (p1 would also need n=31..36).

## Witness on the maximal cycle, verifiable, Wolfram bit order

A small independent iterator written from the bank definition (not the packaged checker), using cell 0 = LSB and idx=(L<<2)|(C<<1)|R with L=i-1 and R=i+1 cyclic, was run on witness 0x1c7dbbb23e at Rule 110, width 37. The state returns at step 4403 and at none of the proper divisors of 4403 (1, 7, 17, 37, 119, 259, 629). A full walk's first return is 4403. The same convention is the bit order in both C programs. Starting from a single live cell (state 1) enters a cycle of period 4403 after a transient of 192 steps, and the packaged witness is the first state of that cycle. So the witness lies on a cycle of length 4403, and that length equals the single-cell floor.

## Term not already in the live OEIS entry at claim time; value at least A180001(37)=4403

Fetched once, no retries, User-Agent naming V3R1T4S, at 2026-11-19T01:39:52Z (2026-11-18 8:39:52 PM ET, America/New_York, UTC-5), all HTTP 200:

- https://oeis.org/A204371/b204371.txt ends at n=36, a(36)=1584; index 37 is absent. sha256 9237e577a1b8e6c74b30a2c2ee7c95e67b20f061fc22e230230f59b12ce41091, identical to the packaging snapshot in the-record-we-beat/RECORD.md.
- https://oeis.org/A204371 DATA ends at 1584, "Table of n, a(n) for n=1..36.", no a(37) and no 4403 in the entry. last-modified remains Tue, 11 Nov 2025 02:50:40 GMT.
- https://oeis.org/A180001/b180001.txt has a(37)=4403.

The claimed value meets the bank floor with equality. Equality is allowed; a report of the floor without an exhaustive census would not be. The two inspected programs, their agreeing n=37 outputs, the self-test, and the held-out n=31 run (2759, not 7) are what show that no start has a longer eventual period.

## Other notes

how-we-built-it/PREREG.md was written after the n=37 runs and says so. That is a process defect in the packaging run, not a failure of the success criterion as applied to this object. No hidden quantifier or stretched definition was found: "exhaustive" is used for a full-state or full-orbit census, "eventual period" for the cycle length after the transient, and "independent implementations" for the two algorithms above.

The result meets the full success criterion, not only a partial win.

confirmed_scope: An exhaustive search over all 2^37 cyclic configurations of elementary cellular automaton Rule 110, carried out by two independent implementations that agree (how-we-built-it/impl1/maxcycle.c marks every rotation orbit and converts an orbit return into a state period; how-we-built-it/impl2/maxcycle.c walks every state with a 3-colour scheme and no rotation folding), both reporting in how-we-built-it/results/ that the longest eventual period is 4403 with witness 0x1c7dbbb23e, so A204371(37)=4403; a direct iteration of that witness under the Wolfram rule-number convention (cell 0 = LSB, idx=(L<<2)|(C<<1)|R) returns to itself at step 4403 and at none of the proper divisors 1, 7, 17, 37, 119, 259 or 629; both implementations' shipped self-test log reproduces A334497(1..24) and A204371(1..30) exactly (120 OK lines, no BUG or MISMATCH) and both report A334497(25..30) as 588425, 312156, 240300, 249165, 1466066 and 374265; the live OEIS entry and b-file for A204371, fetched 2026-11-19T01:39:52Z, still end at n=36 with a(36)=1584, so the term was not listed at this check; and this maximum equals the single-cell floor A180001(37)=4403.

pass: true
