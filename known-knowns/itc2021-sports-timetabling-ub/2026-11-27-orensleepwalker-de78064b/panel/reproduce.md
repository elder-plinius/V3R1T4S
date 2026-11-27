# Reproduce verdict
context: fresh subagent started for this claim only

Claim: lower bounds on the penalty of every feasible ITC2021 timetable: Early 14 >= 4, Early 9 >= 40, Middle 6 >= 60, Middle 9 >= 20, Late 9 >= 20.
Inputs read: claim/ (REPRODUCE.md, CLAIM.md, rows.csv, target.md, data/), then (after task 1) claim/object/, claim/code/, and attempts/certificates/code/certify_lbs.py. Rule source: the official ITC2021 problem description PDF (robinxval.ugent.be/ITC2021/images/OrganizationITC2021_V7.pdf, saved in panel/work-reproduce/dl/spec.pdf). `sha256sum -c SHA256SUMS` inside claim/: 42/42 OK, before and after my work. Nothing was written inside claim/. All my work is in panel/work-reproduce/ (own/ = my code and logs, ev/ = copies of the evidence, dl/ = downloads).

## Rule facts used (from the PDF)
- Compact 2RR, n even, 2(n-1) slots; each team plays exactly one game per slot; each pair meets once at each venue, so each team has exactly n-1 home games. Middle 6 is phased (each half is a 1RR, venues reversed between halves); the other four are not.
- Break at slot s > 0: same venue in s-1 and s. BR1 (per team) and BR2 (sum over teams) count breaks in the listed slots; penalty = weight x excess over intp. In all five instances BR2 is SOFT, covers all teams and all slots, intp = n-2, weight 10.
- CA1 penalty = weight x (count - max)+; FA2 penalty per pair = weight x (largest |home-count difference| - intp)+.

## Task 1: my own derivations (before reading object/ and code/)
Structural facts I used, each valid for every feasible timetable: (a) n/2 home teams in every slot; (b) n-1 home games per team; (c) two teams with identical home/away patterns never meet, so at most one team has the HAHA... pattern and at most one the AHAH... pattern, hence at most two break-free teams; (d) in every slot s>0, #home-home breaks = #away-away breaks (from (a) at s-1 and s), so every slot has an even number of breaks and the season total is even; (e) a balanced pattern (n-1 home of 2(n-1)) with exactly one break has it at an even slot index (odd index makes both alternating segments odd with the same majority venue: n home games, not n-1); (f) per-team venue facts from HARD rules: CA1, BR1, CA3 over all opponents (no HHH/AAA), venue forced by a HARD GA1 with one meeting, one slot and min >= 1.

Code: own/floor.py (per-team exact minimum breaks f_t from the team's own hard venue rules via a one-team CP-SAT, then total >= sum max(1,f_t) minus the break-free teams allowed by (c), rounded up to even), own/hap.py (joint home/away-pattern relaxation over all teams: (a), (b), break indicators, pair condition "each pair has a slot with i home/j away and a slot with i away/j home" (phased: one in each half, opposite venues), all hard venue rules of (f) plus CA4 EVERY with teams2 = all teams; minimise total breaks), own/e14pat.py (Early 14 case split), own/e9team2.py (Early 9 team-2 enumeration).

| instance | per-team floors (own/floor.log) | elementary total breaks | joint HAP relaxation (own/breaks.log, 4 workers, 240 s) | my penalty bound | claimed |
|---|---|---:|---|---:|---:|
| Early 14 | teams 9,10: 1, rest 0 | 18 | OPTIMAL 18 | 4 (case split below) | 4 |
| Early 9 | team 2: 3; teams 4,6,10,14: 1; rest 0 | 18 | bound 19 -> even 20 | 40 | 40 |
| Middle 6 | 0:2, 1:1, 3:3, 4:3, 5:2, 17:1, rest 0 | 22 | bound 33 (incumbent 40, not closed) | 60 (elementary) | 60 |
| Middle 9 | 1,9,10,15: 1; 16: 2; rest 0 | 17 -> even 18 | OPTIMAL 18 | 20 | 20 |
| Late 9 | 1,4: 2; 6,9,12,16: 1; rest 0 | 18 | OPTIMAL 18 | 20 | 20 |

- Middle 6, Middle 9, Late 9: penalty >= 10 x (total breaks - 16) = 60 / 20 / 20 from the elementary floor alone. Reproduced.
- Early 9: the elementary floor gives only 18 breaks (penalty 0). The extra step: total = 18 forces exactly two break-free teams, team 2 at exactly 3 breaks and 15 teams at exactly 1 break (each at an even slot by (e)). My enumeration of team 2's 3-break patterns under its hard rules (CA1 slots 7, {14,15,16}, 17, {20,8,17,23}, {20,8,3,30}, {18,23,5}; away at slot 13 from GA1 "5,2" slot 13) finds 16 break sets, every one with a break at an odd slot (own/e9team2.log). That odd slot would hold exactly one break, contradicting (d). So total >= 19, even -> 20, penalty >= 40. My joint relaxation independently reached bound 19 (-> 20 by parity). Reproduced.
- Early 14: the objective is venue-only (soft CA1 w1, soft BR1 w5, BR2 w10 intp 18, FA2 w10). A direct relaxation (own/e14obj.log, own/e14tight.log) did not close (bound 0 in 500-600 s). Case split (own/e14pat.py): a timetable with BR2, a soft BR1 or FA2 violated costs >= 5. Otherwise total breaks <= 18 and, by (c), exactly two teams are break-free and 18 teams have exactly one break; enumerating the 38 balanced patterns with <= 1 break, filtering each team's hard CA1/BR1/forced-GA1 rules and soft BR1 rules, requiring distinct patterns, 10 home teams per slot and FA2 spread <= 2 at every slot, the minimum soft-CA1 penalty is OPTIMAL 4 (0.1 s). Bound = min(5, 4) = 4. Reproduced.
- Side observation, not part of the verdict: my phased HAP relaxation for Middle 6 proved >= 33 breaks (-> 34 -> penalty >= 180) within 240 s; this is stronger than the claim and was not reviewed by anyone.

## Task 2: evidence checks
Scripts run with python3 -I from copies in ev/:
- object/ITC2021_Early_14/certificate.py: prints team 0 minimum 3, team 15 minimum 1, "Lower bound on Early 14: 4"; its CSV output is identical to patterns.csv.
- object/ITC2021_Early_9/certificate.py: 16 three-repeat sequences, 0 with fewer, 0 with all-even repeats, "Lower bound on Early 9: 40"; output identical to patterns.csv; the 16 break sets equal my own enumeration.
- code/break_floor_stdlib.py (identical to the three object/ copies): Middle 6 floors [2,1,0,3,3,2,0,...,1], zero-break allowed 10/9, total 22 -> penalty 60; Middle 9 total 17 -> 18 -> 20; Late 9 total 18 -> 20. Floors and zero-break counts equal mine exactly.

PROOF.md Early 14, step by step: penalty <= 3 excludes a 19th break (cost 10) - true; at most two break-free teams (identical patterns never meet) - true; hence every team has <= 1 break - true; 19 home games - true; GA1 "9,0" slot 7 and "10,15" slot 4 (HARD, min=max=1) force teams 0 and 15 away there - true (checked in the XML); 19 patterns each, CA1 minima 3 and 1 over disjoint rule rows - true (re-run); contradiction with <= 3 - valid. The bound 4 equals the posted Team Gionar score, so the argument also closes the instance.

PROOF.md Early 9, step by step: at least 16 teams repeat - true; team 2 away at slot 13 and 17 home games - true; no team-2 pattern with < 3 repeats, 16 with 3, each with an odd index - true (reproduced by my own code); total >= 3 + 15 = 18 - true (team 2 is not break-free, at most 2 of the other 17 are); equality forces the stated configuration - true; one-repeat balanced patterns repeat at even indices - true (my fact (e)); per-slot HH = AA forbids a lone repeat - true; so >= 19, even -> >= 20, penalty >= 40 - valid.

break_floor_stdlib.py argument (docstring steps 1-4): all four steps hold for every feasible timetable; the code's DFS checks hard CA1 (min and max), BR1 (asserts mode HA), forced GA1 venues, and caps home and away games at n-1; floors are minima over exact break counts; zero-break teams chosen one per starting venue and distinct; parity rounding; BR2 applied only when it covers all teams and slots 1..R-1. It ignores CA3/CA2/CA4 (weaker but valid).

## Task 3: replay and model validity
Fresh CpModel, proto.parse_text_format, num_workers 1, random_seed from rows.csv, linearization_level 2, OR-Tools 9.15.6755 (ev/myreplay.py -> ev/replay.out; claim's code/replay.py copy gave the same):

| model | seed | status | objective = bound | vars / constraints | wall |
|---|---|---|---:|---|---:|
| Early 14 | 20261124 | OPTIMAL | 4 | 160 / 164 | 0.0 s |
| Early 9 | 20261125 | OPTIMAL | 40 | 4 / 5 | 0.0 s |
| Middle 6 | 20261126 | OPTIMAL | 60 | 3091 / 5123 | 17 s |
| Middle 9 | 20261126 | OPTIMAL | 20 | 3100 / 5115 | 17 s |
| Late 9 | 20261126 | OPTIMAL | 20 | 3097 / 5123 | 26 s |

Provenance: I regenerated each model from its generator and compared protos as text: Early 14 (cp_bound.build), Early 9 (cp_bound.build) and the three venue relaxations (build_venue_relax_model copied from certify_lbs.py, with a regex id parser standing in for the unavailable `base.parse_ids`) are all byte-identical to the bound.pbtxt files. So judging the generator code judges the files.

Admissibility: I downloaded the five posted best timetables (dl/sols/, treated as data), checked each is a complete 2RR (phased for Middle 6) with no hard venue-rule violation, computed their venue penalties with my own code, fixed their patterns in each bound.pbtxt and solved (own/admiss.log). Every model stays feasible with objective equal to the timetable's own corresponding penalty: Early 14 4 = 4 (CA1 of teams 0, 15); Early 9 40 = 40 (20 breaks, team 2 has 3 breaks incl. an odd one); Middle 6 590 = 590 (74 breaks, BR1 soft 10); Middle 9 60 = 60 (22 breaks); Late 9 100 = 100 (26 breaks).

Validity per model:
- Middle 6, Middle 9, Late 9 (venue relaxation): variables H[s,t]; n/2 home per slot; n-1 home per team; break linearisation; >= n-2 teams with a break and at most one break-free team per starting venue; HH = AA per slot; per-team floors from the team's hard CA1 (min/max), BR1 and GA1 rules requiring all listed meetings in one slot; hard CA1/BR1 as constraints; hard GA1 with min > 0 as "sum over meetings and slots of [i home and j away] >= min"; objective = soft CA1 (none in these three) + soft BR1 (weight 5) + BR2 (10 x (2 x pairs - 16)+). No soft rule in these three has min > 0, so the code's undershoot terms never fire. Every constraint holds for every feasible timetable and every objective term is at most the official penalty of the same rule. VALID.
- Early 9 (4 variables): under the projection team2 = min(team 2 breaks, 4), odd = [team 2 has exactly 3 breaks] (all 3-break patterns have an odd break), total = season breaks, every constraint holds for every feasible timetable: table {(3,1),(4,0)} (team 2 has >= 3 breaks); total >= 15 + team2; odd -> total >= 19 (PROOF step); total even; cost = 10 x (total - 16)+ is exactly the BR2 penalty. VALID (the model is an arithmetic shadow of PROOF.md; its force comes from the proof and certificate.py, both checked).
- Early 14 (two teams): home sum 19, forced away slot, soft CA1 of teams 0 and 15 - valid for every feasible timetable; but `sum(breaks) <= 1` per team is NOT valid for every feasible timetable. It holds only for timetables with at most 18 breaks, which includes every timetable with penalty < 10. The bound needs the outside case step "else penalty >= 10" (PROOF.md, first paragraph); with it the bound is min(10, 4) = 4, correct and independently reproduced by my own case-split model. So it is CONDITIONALLY VALID: the bound is right, but the .pbtxt on its own is not an unconditional relaxation. The claim text should say so (e.g. "model of the case with at most 18 breaks; the other case costs >= 10").

## Task 4: sanity against known timetables
Board (claim/data/board.html) Best UB / Best LB: Early 14 4 / 1; Early 9 56 / 0; Middle 6 1090 / 24; Middle 9 415 / 0; Late 9 498 / 3. Every claimed bound is <= Best UB (Early 14 equal) and strictly above the posted LB and the largest bound on each history page (1, 0, 24, 0, 3). The posted timetables' break counts (18, 20, 74, 22, 26) agree with the break bounds (18, 20, 22, 18, 18).

## Not checked
- I did not run the RobinX C++ validator; the posted timetables were checked only for 2RR structure and venue rules (CA1/BR1/BR2/FA2 penalties, hard CA1/BR1), not for CA2-CA4/GA1/SE1 hard rules or their full scores.
- `base.parse_ids` and the scout modules imported by certify_lbs.py were not read; the identical regeneration with a plain integer parser makes this immaterial for the three exported models.
- My Middle 6 >= 33 breaks side result was not reviewed.

## Findings
All five bounds are valid and reproduced, by my own code before I read the evidence and by the claim's scripts and replays. One disclosure: Early 14's bound.pbtxt holds only in the case of at most 18 breaks (constraint `sum(breaks) <= 1` per team), so the model certifies 4 only together with PROOF.md's "otherwise penalty >= 10" step. The bound itself is correct and is reproduced by my own case-split model.

pass: true
