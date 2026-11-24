# CRITERION skeptic: A334497(37) = 49276415 (Rule 30, cyclic width 37), target eca-rule30-rule110-cyclic-max-period

context: subagent (started as a fresh executor subagent; judged only from files, the bank entry, the frozen plan, the raw send-back and my own checks; I did not write the package or any other panel file)
role: CRITERION
date: 2026-11-23 (ET)
tier: full solution (main success criterion); no partial win claimed or needed

## Provenance of criterion and plan
- how-we-built-it/TARGET_CRITERION.md contains the bank `success_criterion` of eca-rule30-rule110-cyclic-max-period verbatim (string-containment check against bank/targets.json at repo commit 5db3547; the packager's repo copy is byte-identical to the main kit's bank/targets.json at 5db3547).
- how-we-built-it/PREREG.md sha256 1d5713b309f383177e195f3b751ade50a26d9d4de38c572a94eeb75e0bbdbf14, identical to the frozen plan and its recorded sha256. Frozen 2026-11-22T16:51:29Z (file mtime agrees); the PC run started 2026-11-22T18:06:21Z (logs/run.log line 1). Plan precedes run.
- Programs: impl1/maxcycle.c sha256 9e244067..., impl2/maxcycle.c sha256 bf2321ce..., equal to the PREREG-fixed hashes and to the send-back's kit_sha256.txt.
- Send-back: raw archive sha256 e5a8004c... matches the brief. Package results/, selftest/, heldout/ are byte-identical to the unpacked send-back; logs/run.log differs only in three lines where a home-directory path was replaced by `~` (path scrubbing, no data change). all_results.txt identical.

## Success criterion, clause by clause
1. "exact value of A334497(37) ... from an exhaustive search over all 2^n states, or over all rotation orbits with the rotation factor accounted for": MET. I read both programs. impl2 loops s0 over all 2^37 states with a 2-bit white/grey/black colour array (results/err_impl2.txt: colour=34359738368 B = 2^37 * 2 bits), measures the grey segment on closing a cycle; no folding. impl1 loops over all states, marks whole rotation orbits, and converts f^k(s)=rot_r(s) to k*n/gcd(r,n) (bitset 17179869184 B = 2^37 bits). Rotation factor accounted for; the known overcount for rotation-symmetric states cannot touch n=37 (prime width: only all-0/all-1 are rotation-fixed, all-1 -> all-0 -> all-0 under Rule 30), and impl1's final witness re-iteration showed no adjustment (results/err_impl1.txt has no "adjusting" line). No reflection reduction (pitfall respected).
2. "run by two independent implementations that agree": MET. results/compare.txt: AGREE max_period=49276415; both name witness 0x7fbfe703e. Independence is algorithmic (orbit-marking vs 3-colour walk; same author and same textbook step function), which is what the criterion and PREREG specify.
3. "Both must reproduce A334497(1..24) and A204371(1..30) exactly": MET. logs/run.log selftest: 108 OK lines (2 x (24+30)), "SELFTEST: PASS", zero BUG/MISMATCH lines. Reference b-files used (sha 7339a6ff..., 9237e577...) equal my live fetches of the OEIS b-files today.
4. "both must report their values for A334497(25..30)": MET. Both report 588425, 312156, 240300, 249165, 1466066, 374265, all REPORT_MATCHES_LISTED. No difference from listed terms, so p1's correction rule is not triggered.
5. "A value below a listed term means a bug": no value below any listed term anywhere (selftest, n=25..30, held-out n=31).
6. "A witness state on the maximal cycle must be given ... confirm the cycle length by direct iteration": MET. object/a334497_37.txt gives witness 0x7fbfe703e. My own C iterator (written from the definition, no shared code) gives first return to the witness at exactly step 49276415, which also rules out every proper divisor. The shipped checker logs (results/check_period_impl1/2.txt) agree: no return at 185, 1331795, 9855283 (P/q for primes q = 266359, 37, 5; I confirmed 266359 is prime), return at 49276415.
7. "Bit order must follow the Wolfram rule-number convention, which the small-n reproduction checks": MET. Code uses cell 0 = LSB, idx=(L<<2)|(C<<1)|R, L=i-1, R=i+1 cyclic. My own independent census for n=1..20 reproduces the live OEIS terms of both A334497 and A204371 with that convention.
8. "The term must not already be in the live OEIS entry at claim time": MET as of my own fetch 2026-11-23T23:52:58Z (18:52:58 ET): b334497.txt HTTP 200, ends at n=36, a(36)=2237472 (sha256 7339a6ff...); search JSON id:A334497 HTTP 200, revision 40, data ends ...2237472, the string 49276415 does not appear. Must be re-fetched again before any submission (PREREG check 6).

## Bank pitfalls
- Sampling is only a lower bound: this is exhaustive, not sampled. OK.
- Wolfram (1986) sampled value must be a floor: Table 9.2, CA30, N=37 = 49276415. The result EQUALS it; equality satisfies "at least as large". The bank's own statement says those 1986 values are lower bounds and were exceeded at other widths, so the exact value at N=37 was not established before this census. The exact value is the new content; README says so plainly ("Not claimed: That the number 49276415 is new"). Not subsumed.
- Rotation-orbit conversion: handled (clause 1). Reflection: not used. Max eventual period, not transient: impl2 measures cycle length only; the witness is itself periodic (first return verified).
- Mismatch at 25..36 not evidence of a bug: no mismatch occurred.

## PREREG checks 1-6
1. Self-test: PASS (clause 3-4).
2. Main run: impl1 then impl2 sequentially (impl1 18:24:13Z-19:26:39Z, impl2 19:26:39Z-06:51:05Z), same max_period and same witness. PASS.
3. Independent checker on both witnesses: PASS (logged, and reproduced by my own iterator).
4. Floor >= A334496(37) = 49276415: equal; allowed and disclosed (compare.txt FLOOR_OK; README). PASS.
5. Held-out width 31: both give A204371(31)=2759 (witness 0x3f647ff8, checker PASS) and A334497(31)=2841150 = listed. PASS.
6. Live table: absent at packager fetch 2026-11-23T23:39:09Z and at my fetch 23:52:58Z. PASS (re-fetch still required before submit).

## Scope wording and README
- Main criterion only; p1 and p2 explicitly not claimed; no result for A334497(32..36) (n=31 only as the held-out report), none for n>=38, none for A204371 beyond self-test/held-out. Matches the PREREG's fixed scope wording.
- Equality with the single-cell floor and with Wolfram's 1986 value is disclosed in ## What, ## Compared to and ## Not claimed. impl1 rotation-overcount note present. No personal paths, usernames or host names found in the package (grep). No overclaim found.
- One narrowing relative to the current README ## What: the 2^37 census is evidenced by the shipped PC logs (not re-run on the packaging machine, whose memory is too small), and I add my later live-fetch time. Everything else in the proposed paragraph I checked and accept.

## Caveats (do not block)
- The census itself could not be independently re-executed here; acceptance rests on two agreeing programs whose code I read, their shipped logs, and the independently verified witness, which is exactly what the criterion requires.
- Novelty of an exact confirmation of a 1986 sampled value is the NOVELTY skeptic's call; under the bank criterion (term absent from live OEIS, exact value from exhaustive search) it qualifies.

verdict: meets the full main success criterion (tier: solution)
confirmed_scope: An exhaustive search over all 2^37 cyclic configurations of elementary cellular automaton Rule 30, run on the contributor's PC by two independent implementations that agree (how-we-built-it/impl1/maxcycle.c marks every rotation orbit and converts an orbit return into a state period; how-we-built-it/impl2/maxcycle.c walks every state with a 3-colour scheme and no rotation folding), with both shipped result files in how-we-built-it/results/ reporting that the longest eventual period is 49276415 with witness 0x7fbfe703e, gives A334497(37)=49276415; a direct iteration of that witness under the Wolfram rule-number convention (cell 0 = LSB, idx=(L<<2)|(C<<1)|R) returns to itself first at step 49276415, so at none of its proper divisors; both implementations' shipped self-test log reproduces A334497(1..24) and A204371(1..30) exactly (108 OK lines, no BUG or MISMATCH) and both report A334497(25..30) as 588425, 312156, 240300, 249165, 1466066 and 374265, equal to the listed terms; both programs also reproduce the held-out terms A204371(31)=2759 and A334497(31)=2841150; the live OEIS entry and b-file for A334497, fetched 2026-11-23T23:39:09Z and again 2026-11-23T23:52:58Z, end at n=36 with a(36)=2237472, so the term was not listed at those checks; and this maximum equals the single-cell floor A334496(37)=49276415 and the sampled maximum cycle length Wolfram (1986, Table 9.2) reported for N=37, so the census shows that value is exact; no result is claimed for A334497(32..36), A334497(38) or beyond, A204371 beyond the self-test and held-out values, or partial wins p1 and p2.
pass: true
