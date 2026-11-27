# Reproduce verdict
context: fresh subagent started for this claim only

Claim: six ITC2021 timetables (claim/object/) are valid compact double round robins with 0 hard violations and a penalty strictly below the board's Best UB. Reviewer: REPRODUCE skeptic. I read only claim/ (plus the RobinX source and Boost headers I was allowed to use, the local git clone of RobinX, and public ITC2021 pages). I did not read claim/code/verify.py or claim/rows.csv until my own results were final (step 6). All my work is in panel/work-reproduce/. `sha256sum -c claim/SHA256SUMS` passed before and after my work. No __pycache__ appeared in claim/.

## Method
1. Rules: I fetched the official problem description once (https://robinxval.ugent.be/ITC2021/images/OrganizationITC2021_V7.pdf; www.sportscheduling.ugent.be/ITC2021/ redirects to robinxval.ugent.be/ITC2021/). Copy in panel/work-reproduce/web/.
2. My own checker: panel/work-reproduce/mycheck.py, standard library only, written from the PDF before I read verify.py.
   - Structure: n even, S = 2(n-1) slots; exactly n(n-1) games; ids in range, no self-games; every team exactly once in every slot; every ordered pair exactly once; gameMode P: every unordered pair meets exactly once in slots 0..n-2 and once in slots n-1..2n-3. Strict parsing: one `<Games>` element, only `ScheduledMatch` children, each with exactly the attributes home/away/slot. The checker stops if it finds an unknown constraint tag, a non-empty teamGroups or slotGroups attribute, or a mode the ITC rules do not allow.
   - Constraints, deviations (penalty = sum over soft constraints of weight x deviation; hard deviations reported separately): CA1 per team, number of H or A games in slots above max. CA2 per team in teams1, games of mode H/A/HA against teams2 in slots above max. CA3 per team in teams1 and per window of intp consecutive slots, games against teams2 above max (summed over windows). CA4 teams1 as one entity, games (i,j) with i in teams1 and j in teams2 (H; (j,i) for A, both for HA) above max, over all slots (GLOBAL) or per slot (EVERY). GA1 count of listed meetings in slots below min plus above max. BR1 per team, breaks of mode2 type at slots in slots above intp. BR2 total breaks of the teams over slots above intp. FA2 per pair, max over slots of the cumulative home-game difference minus intp (if positive). SE1 per pair, max(0, min - (s2 - s1 - 1)).
3. Validated on the six posted record timetables (claim/data/records/) against the Best UB I parsed myself from claim/data/board.html (panel/work-reproduce/board.py).
4. Ran it on the six claimed timetables with claim/data/inst/<instance>.xml.
5. RobinX: I confirmed the RobinX source. In the local clone scans/2026-11-24-itc2021-pilot/vendor/RobinX (origin github.com/Robin-X/RobinX, shallow, HEAD = 878bf2db7b25b43cc3022bc08c00be938b997b6a) I ran `git archive 878bf2db`. `diff -r` of its source/ against scans/2026-11-26-robinx-build/src/source shows them identical. The Makefile differs from the commit's Makefile only by the added `-I.../dl/boost_1_86_0`. boost/version.hpp says BOOST_VERSION 108600. I copied source/ and the Makefile into panel/work-reproduce/robinx/ and ran `make` (exit 0). My binary's sha256 is a143c8b8...; the provided src/RobinX is 080fcf6b.... I ran my binary and src/RobinX on all 12 files.
6. Live re-check (one request each, User-Agent "V3R1T4S-reproduce-skeptic", 2026-11-27T14:53:17Z): the board instances.php, the six instance XMLs and the six Best UB solution files linked on the board.
7. Negative and differential tests: panel/work-reproduce/negtest.py, output in negtest_out.tsv, files in neg/.

## Rule readings that are ambiguous, and how I read them
- CA3 windows: only full windows of intp consecutive slots inside the season (start slots 0..S-intp), with no wrap-around. Deviations are summed over windows.
- Break at slot s means the team has the same home/away status at s-1 and s. It counts toward a constraint if s is in slots. Slot 0 never has a break. A home break means both games are at home.
- FA2: home games counted cumulatively up to and including each slot in slots. The deviation per pair is the largest excess, not the sum over slots.
- SE1: max(0, min - (s2 - s1 - 1)), as the PDF's boxed correction states (not the RobinX-paper form).
- The PDF mentions only "more than max" for CA1/CA2/CA3/CA4/BR1. I also add "below min". It has no effect here, because min=0 in every CA and BR constraint of these instances.
- Infeasibility: I report the sum of hard deviations. RobinX's first Objective number equals it on every test.
- CA4 with HA and overlapping team sets would be ambiguous, but every CA4 here is mode1=H.
None of these readings changes any record or claim value: all records reproduce exactly. 180 random mutants also agree exactly with RobinX, and they exercise every constraint type, hard and soft (BR1, BR2, CA1, CA2, CA3, CA4 hard, FA2 soft, GA1, SE1 soft).

## Results per instance
Best UB parsed from claim/data/board.html. The live board fetched today is byte-identical (sha256 e008069e...). The six live instance files and the six live record files are byte-identical to claim/data/inst and claim/data/records.

| instance | gameMode | Best UB | record: mine / RobinX (mine) / RobinX (src) | claim: structure, hard, penalty (mine) | claim: RobinX (mine) / RobinX (src) | below by |
|---|---|---:|---|---|---|---:|
| Early 9 | NULL | 56 | 56 / 0 56 / 0 56 | valid, 0, 51 | 0 51 / 0 51 | 5 |
| Early 12 | P | 315 | 315 / 0 315 / 0 315 | valid, 0, 300 | 0 300 / 0 300 | 15 |
| Middle 5 | P | 279 | 279 / 0 279 / 0 279 | valid, 0, 278 | 0 278 / 0 278 | 1 |
| Middle 12 | P | 358 | 358 / 0 358 / 0 358 | valid, 0, 338 | 0 338 / 0 338 | 20 |
| Middle 15 | NULL | 462 | 462 / 0 462 / 0 462 | valid, 0, 459 | 0 459 / 0 459 | 3 |
| Late 11 | P | 196 | 196 / 0 196 / 0 196 | valid, 0, 191 | 0 191 / 0 191 | 5 |

My breakdowns of the claimed penalties by constraint type:
- Early 9: BR2 40, CA3 10, GA1 1.
- Early 12: BR2 280, CA3 20.
- Middle 5: BR2 220, CA1 13, GA1 45.
- Middle 12: BR2 220, CA1 18, CA2 100.
- Middle 15: BR2 440, GA1 19.
- Late 11: CA2 150, CA3 40, GA1 1.

The six claimed XML files contain only the XML declaration, MetaData/InstanceName and one Games element with n(n-1) ScheduledMatch lines (306 or 380). No history page in claim/data/hist lists a solution at or below the claimed value. The only smaller values there are linked Bounds files.

## Negative tests
For each instance I built up to 10 corrupted copies of the claimed timetable (58 in all):
- S1: one game's venue flipped.
- S2: one game deleted.
- S3: one game moved to another slot.
- S4: one game duplicated.
- S5: a slot out of range.
- S6: slot 0 swapped with the last slot (breaks the phase on Early 12, Middle 5 and Late 11).
- R1: the venues of one pair mirrored, so a hard CA1 max=0 is broken.
- R2: two slots swapped within a half.
- R3: the first half reversed.
- R4: a hard-forbidden GA1 meeting moved into its forbidden slot.

Middle 12 has no R1 or R4, because the generator found no usable hard CA1 max=0 or GA1 max=0 constraint there, so it has 8 copies; every other instance has 10.

- My checker rejected every structural corruption (S1-S5 everywhere; S6 on the three phased instances whose phase it breaks). It reported hard violations > 0 on every R mutant. On Middle 15 (NULL), S6 is still a valid timetable: hard 0, penalty 585 from me, RobinX and verify.py alike. On Middle 12 the slot-0/slot-37 swap keeps the phase (the two slots hold mirrored games); it is rejected through 2 hard violations.
- RobinX reported infeasibility > 0 for every S1, S2, S3, S6-phase-break and R mutant. Its (infeasibility, objective) equals my (hard, penalty) on every structurally valid mutant. S5 crashes it ("Slot N does not exist: map::at", no Objective line, exit code 0).
- **RobinX gap (does not affect the claim): RobinX accepts a duplicated ScheduledMatch (S4) with `Objective: 0 <same penalty>` on all six instances.** RobinX alone therefore does not certify the round-robin structure. For these claims the structure is certified by my checker and by verify.py: both find each claimed file a valid compact double round robin, with phase on the P instances.
- Differential test: 30 structurally valid random mutants per instance (180 in all), made by mirroring pair venues and swapping slots within halves. My (hard, penalty) equals RobinX's (infeasibility, objective) on 180/180.
- RobinX's per-line penalty column is cumulative within a constraint. For example, Early 12 team 15 shows 5 and then 10, and the line totals 305 against Objective 300. Only the Objective line is used.

## Comparison with the claim's code and rows (read after my results were final)
- claim/code/verify.py uses the same readings as mine for every rule: CA3 full windows only, break definition, cumulative FA2 max-excess, SE1 with s2-s1-1, CA4 GLOBAL/EVERY.
- Its structure check is the same in substance. It checks per team per slot, per ordered pair, and the first-half phase (with ordered pairs exactly once, that implies the second half too). It parses ids leniently with a regex where mine is strict. It ignores ScheduledMatch elements outside ./Games, which matters only for malformed files and not for these.
- Running it: PASS on all six claims, with the same penalties and the same per-rule splits as mine. FAIL on every corrupted copy except Middle 15 S6, which is a genuinely valid timetable. Its (hard, penalty) equals mine on all 180 random mutants.
- claim/rows.csv: best_ub, ours, saving, venue/opponent split (CA1, BR1, BR2 and FA2 counted as venue), robinx "0 <penalty">, and the object and instance sha256s all agree with my results and with the files.
- CLAIM.md's table agrees with them too.

## Not checked / limits
- Upstream identity of commit 878bf2db: the local clone is shallow (one commit). I did not contact GitHub. Identity rests on the commit hash in the local clone; the source tree matches it byte for byte.
- Boost: not checked against the official tarball's sha256 (not fetched); only version.hpp (1.86.0) was looked at. The headers do not affect the evaluation logic.
- The claimed files lack the SolutionName, Contributor and ObjectiveValue metadata that posted solutions carry. This is cosmetic: RobinX evaluates them without it.
- Novelty of the method, and whether the claimed timetables are minor edits of the records, are left to the other skeptics. The criterion only needs a strictly lower validated penalty.
- I re-fetched the board, but not the history pages.

pass: true
