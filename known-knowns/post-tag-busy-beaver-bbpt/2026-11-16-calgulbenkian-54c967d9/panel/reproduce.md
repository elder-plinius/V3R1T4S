context: Claude Code subagent, fresh context [Sonnet 5.5]

# REPRODUCE report: BB_PT(8) = 19

## Definition checked against (quoted from the target's success criterion)
"A 2-tag system has an alphabet {0, 1, ...} and one production word w_a per symbol: while the tape has at least 2 symbols, read the first symbol a, delete the first 2 symbols and append w_a. Size is |A| + sum of |w_a|. BB_PT(S) is the most steps any size-S 2-tag system takes before halting when started on 00." Verification method: "stop when fewer than two symbols remain, counting steps" (no extra halting step counted).

## My checker (written before reading the author's code)
Own script (not shipped: has the output). It does this:
1. Enumerates every raw system with alphabet {0..n-1}, n=1..8, word lengths summing to 8-n, each letter any symbol. Expected count by hand: 1+448+5103+8960+4375+756+49+1 = 19,693. My enumerator produced 19,693 distinct systems. This matches the claim.
2. Simulates each from tape 00 with a 3000-step cap. Halting means fewer than 2 symbols; steps counted per production applied.
3. Reduction to classes (my own, independent): keep only symbols reachable by appearance from symbol 0 (the run from 00 can only ever contain such symbols, so dropping the other words leaves the trajectory identical), then rename by first appearance (a bijection fixing 0, which maps trajectories to trajectories, so halting and step count are preserved). I got 1,728 classes, the same set as the package's.
4. Non-halting classes: for CYCLE, I rebuilt the tape at entry_step and at entry_step+period myself and compared them exactly. For DFA_INVARIANT, my own code checks: (a) no accepted string of length 0 or 1; (b) the tape reached after entry_step steps is accepted (tape recomputed by me); (c) closure: for every first two symbols a,b, explore the product of (state after reading a b then r) and (state after r) over all r, and require that whenever the first is accepting, the DFA reading w_a after r accepts. This shows the accepted set is closed under one step and never contains a halting tape, so the run never halts.
5. Each raw system's class is looked up in the package's certificate file, and I compared the multiplicity, the halting step count and the certificate status.

## Exact output of my checker
```
raw systems enumerated: 19693 distinct: 19693
max halting steps (cap 3000): 19; raw systems attaining: ['222__10', '111_20_']
raw halters: 17374 (by class) ; nonhalters within cap: 2319
my canonical classes: 1728 cert classes: 1728
classes: {'DFA_INVARIANT': 368, 'HALT': 1012, 'CYCLE': 348} raw: {'DFA_INVARIANT': 915, 'HALT': 17374, 'CYCLE': 1404}
mismatches: 0
VERDICT OK
010_2_0 DFA_INVARIANT 14
01010_1 DFA_INVARIANT 16
010_21_ DFA_INVARIANT 29
0120__0 DFA_INVARIANT 62
```
- Halters: 17,374 raw systems, max 19 steps, reached by exactly two raw systems (222__10 and 111_20_), both in the one canonical class 111_20_.
- Every one of the 2,319 raw non-halters (348 cycle classes + 368 DFA classes) has a certificate that my own code verified. No class lacks both a halt and a verified certificate. All 1,012 halting classes' step counts match the package. All raw multiplicities match.
- Sanity test of my DFA checker: 278 of 322 random single-transition perturbations of real certificates were rejected (the rest plausibly change only unreachable transitions), so the checker is not vacuous.
- The 7 wiki holdouts are among the DFA classes; I spot-printed four of them (state counts 14, 16, 29, 62), all verified. All DFA classes passed, not a sample.
- Nothing needed a long run: the whole check takes seconds, far under the limits.

## Cross-check (run only after my verdict)
Ran verify-it-yourself/run_checks.sh: printed the calibration OK line, 1728 classes, HALT 17374 / CYCLE 1404 / DFA_INVARIANT 915 raw, "BB_PT(8) = 19 CERTIFIED EXACT.", PASS. Consistent with mine.

## Limits
My check covers the claim as stated (the exact value 19 under the wiki convention, with the stated reductions). I did not re-fetch the wiki table; whether an upstream value now ties or beats 19 is for other panelists. The certificates are a rule-by-rule soundness check, not a formal proof assistant check.

pass: true
