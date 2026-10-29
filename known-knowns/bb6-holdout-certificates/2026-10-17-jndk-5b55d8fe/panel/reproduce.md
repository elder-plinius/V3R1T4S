# REPRODUCE skeptic verdict: 1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB, seven macro rules (p1)

context: subagent (fresh context, Claude Code Agent tool)

Inputs read: claim/CLAIM.md, claim/result/rules.json (sha256 7510c768...fdc24), claim/REPRODUCE.md. I did not open
claim/code/* until my own checker (work/mycheck.py) and my own simulator and replay (work/mysim.c) had run.
I ran everything on the remote compute server. Scripts and raw outputs are in work/ next to this file.

## Definition used (quoted)

Machine semantics (bbchallenge), as quoted in REPRODUCE.md: "start state A on an all-0 tape. `---` is undefined;
reading it halts. One step is one defined transition." The transition string has one 6-character group per state
A..F, two 3-character entries per group (read 0, read 1), each `<write><L|R><next state>`. For this machine:
A0=1RB A1=1LC B0=1LC B1=0RD C0=0LE C1=1LA D0=0RF D1=1RA E0=1LA E1=0LA F0=--- F1=0RB.

Rule notation, from rules.json: "A is a state marker immediately before the scanned cell, x is any single bit, powers
have nonnegative integer exponents, all omitted left/right context is arbitrary and untouched. Step counts count
defined transitions." From REPRODUCE.md: "input and output windows have equal length, with left edges aligned;
cells outside the window are arbitrary and must be untouched". What I checked for each rule: start in state A on
the input window. After exactly `steps` defined transitions the machine is in state A, the head is on the output's
marked cell, and the window equals the output. No undefined transition is read along the way. The head never
leaves the window, at every intermediate time and at the end. Leaving the window is the condition that makes the
outside cells irrelevant.

## 1. My own symbolic checker (work/mycheck.py, written before reading claim/code)

Method:
- Linear rules (even, odd, Eodd, Dstep; domain k>=1): I set k=j+1 with j a symbolic nonnegative integer. The
  symbolic 1-run becomes a block (11)^(j) plus concrete cells. I simulate on an edge-notation tape.
- Blocks are crossed only by context-carrying shift lemmas. A rightward lemma takes c.w, edge e in c, to w.c, edge
  e+|w|; a leftward lemma takes w.c to c.w. Each lemma is checked by concrete simulation of one copy, and every read
  must stay inside c.w. It is then extended to all n>=0 copies by induction on n. One other rewrite is used: the tape
  identity (1^2)^n 1 = 1 (1^2)^n.
- Success requires the configuration to equal the stated output as a run-length word with polynomially equal run
  lengths, with the same head cell and state A, and the step count to equal the stated count as a polynomial in j.
  Any read outside the window or any undefined transition is a failure.
- Quadratic rules (even_drain, Ddrain1, Ddrain3; domain k>=0): k=0 is checked by concrete simulation. The step
  k -> k+1 is a symbolic composition: the current tape must equal L ++ In_R(p) ++ R as run-length words with symbolic
  k. It is then replaced by L ++ Out_R(p) ++ R. The sub-rule parameter must lie in its domain for every k>=0. The IH
  may only be used at parameter k. At the end the tape must equal Out(k+1), and the step sum must equal steps(k+1).
  I re-derived the chains independently. They are the ones stated in rules.json: even(k+1) in left context 0^k,
  then IH with right context 111; Dstep(2k+1) or Dstep(2k+2), then IH with left context 1 and right context 111.
- Concrete cross-check: k = domain_min..30, x in {0,1}, 3 random exteriors of 40 cells per side. Exactly `steps`
  transitions, head inside the window at every step, exterior unchanged.

Output (work/mycheck.out):
```
RULE even: PROVED  [(0, (0,), 12*j + 9), (1, (0,), 12*j + 9)]
RULE odd: PROVED  [(0, (0,), 12*j + 17), (1, (0,), 12*j + 17)]
RULE Eodd: PROVED  [(0, (0,), 24*j + 31), (1, (0,), 24*j + 31)]
RULE Dstep: PROVED  [(0, (0,), 12*j + 25), (1, (0,), 12*j + 25)]
RULE even_drain: PROVED  ok
RULE Ddrain1: PROVED  ok
RULE Ddrain3: PROVED  ok
lemmas used: [('L', 'A', '<', 0, '', '11', 2), ('L', 'A', '<', 1, '1', '11', 2), ('R', 'C', '<', 2, '011', '11', 10), ('R', 'D', '>', 1, '01', '11', 10)]
ALL SEVEN PROVED: True
```
At k=j+1 the stated counts are 12k-3=12j+9, 12k+5=12j+17, 24k+7=24j+31 and 12k+13=12j+25, so all four agree. My
lemmas are phase-shifted versions of the author's: right shift 10 steps per copy of 11, left shift 2 steps per copy.

My checker rejected all 28 of its mutation controls (`all controls rejected: True`):
- steps+1 and steps-1 for each of the seven rules;
- a flipped output bit for each of the seven rules;
- head moved (even, Dstep, Ddrain1);
- domain widened to k>=0 (even, Dstep);
- 1^(3k) changed to 1^(3k+1) in even_drain;
- odd's input changed from x00 to x01.

Before I added the block-rotation identity, my first versions failed on `even` and `Eodd` ("no shift lemma at block,
state E"). That was a gap in my tool, not in the rule: a concrete trace at k=3 showed that state E erases the last 1
of the run. After the fix, every rule was proved.

## 2. My own naive simulator and replay (work/mysim.c, written before reading claim/code)

BB(5) champion validation:
```
HALT after 47176869 defined transitions, reading undefined E0; tape ones=4097
```
That is 47,176,869 defined transitions, then a halt on reading E0, which is step 47,176,870 counting the halting step.
The tape holds 4097 ones because the halting write is not executed.

The replay schedules every occurrence of every rule's input pattern with state A and the marked cell at the head,
at each t <= 1e8 of the blank-tape run. The parameter comes from the maximal 1-run, terminated by 0, and the whole
generated input window is compared with the tape. Each check is made at t+steps: state A, head cell, and the full
window. A max-heap on window left ends and a min-heap on window right ends confirm that the head stays inside every
pending window at every step. Output (work/mysim.out), mutation 0:
```
even       scheduled=8316353 passed=8316353 failed=0 zero_step=0 max_k=1855
odd        scheduled=15319 passed=15319 failed=0 zero_step=0 max_k=1855
Eodd       scheduled=22 passed=22 failed=0 zero_step=0 max_k=1845
even_drain scheduled=3531 passed=3531 failed=0 zero_step=102 max_k=647
Dstep      scheduled=15319 passed=15319 failed=0 zero_step=0 max_k=1855
Ddrain1    scheduled=7684 passed=7684 failed=0 zero_step=35 max_k=928
Ddrain3    scheduled=7707 passed=7707 failed=0 zero_step=37 max_k=814
TOTAL scheduled=8365935 passed=8365935 failures=0 (zero-step 174; nonzero-step 8365761) window_violations=0
last resolved at t=103007095, simulated to t=103007095, max duration=10346272, max pending=1858, head range [-3598,133]
```
Controls: every step count +1 gives `passed=0 failures=8365935`, and the last output bit flipped gives
`passed=0 failures=8365935`.

The total of 8,365,935 and the last resolution at t=103,007,095 match the claim exactly. The per-rule counts match
the author's table (below). The total includes 174 zero-step applications (k=0 of the three drain rules, where the
input equals the output). These are counted as trivial passes, as in the author's "trivial0" column. This is not a
mismatch, but the claim's headline figure includes them.

## 3. Author's code and REPRODUCE.md steps (read and run after steps 1 and 2)

I ran `bash code/remote_checks.sh` from a fresh copy of claim/ with sympy 1.14.0, then `python3 code/notes_check.py
data`. Results (work/author_checks.out, work/author_checks2.out):
- Parser test: `parser test pass: True`. Exponents and step counts using j are rejected.
- Proofs: `RESULT even/odd/Eodd/Dstep: PROVED K=1` and `RESULT even_drain/Ddrain1/Ddrain3: PROVED (induction)`.
  The embedded rules.json sha256 equals that of result/rules.json. The proof log shows the shift lemmas described in
  rules.json, and the induction step sums equal steps(k+1) (6k^2+15k+9, 12k^2+37k+25, 12k^2+49k+37).
- Controls: all 12 (C1 to C12) REJECTED, `all controls rejected: True`.
- Brute force: k up to 12, random exteriors. `all real pass: True` and `all mutants caught: True`.
- Replay: BB(5) gives `halted=1 defined_transitions=47176869 ... halting_state=E read=0`. Then
  `TOTAL scheduled=8365935 passed=8365935 failures=0`. Controls 1 and 2 each give `passed=0 failures=8365935`. The
  per-rule table is identical to mine, including the max_k values and the trivial0 counts 102/35/37.
- Notes check: hits=0 on holdouts_lists.html, bb6_page.html and sheet_gid806905077.csv. Exactly one SELF hit each on
  sheet_gid1330361301.csv (line 789), sheet_4319.csv (line 3567) and BB6_holdouts_663.txt (line 523). Sheet row
  `['...', '', 'Quadratic Mess', '', '', '']` gives `notes_empty: True`. There are two distance-2 relatives (lines 2
  and 633). The sha256 of BB6_holdouts_663.txt is cfb2540f...4ee9, as claimed. The sheet classifies the machine as
  "Quadratic Mess", a category label, not an accelerated rule set.

I reviewed the author's code. The symbolic engine (prove.py) uses shift lemmas checked on one copy and extended by
induction. The peel and regroup steps are tape identities. The induction checker requires sub-rule domains to hold
for all k>=0 and allows the IH only at k. The replay detects window escape via sentinel counters at L-1 and R+1,
which is sound because the head moves by exactly one cell per step. I found no unsound step, and nothing in it
contradicts my independent results.

## Mismatches

None. Every number I computed independently matches the claim: seven rules proved for all parameters, 8,365,935
replayed applications with 0 failures, last resolved at t=103,007,095, and the BB(5) validation. Notes:
(a) 174 of the 8,365,935 applications are zero-step (k=0 drain) identities.
(b) This verdict covers only the mathematical and replay content of p1. The live-status conditions (that the newest
holdout file at verification time still lists the machine, and the community-channel checks) are outside the
REPRODUCE lens and were not checked here. The Discord checks are human reports.

pass: true
