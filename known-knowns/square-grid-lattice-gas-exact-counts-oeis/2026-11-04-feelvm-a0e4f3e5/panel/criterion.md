# CRITERION skeptic — verdict on the A054759 a(15) p1 partial win

context: subagent (repair round 1, criterion lane)

REPAIR-LANE NOTE: this file REPLACES the first criterion lane's verdict, which is preserved
verbatim at claim/criterion.v1.md (pass: false). That lane verified every arithmetic clause and
found exactly one failing clause — the literal growth-tolerance check — and left open the
inheritance question posed in claim/REPAIR.md (does p1 inherit the growth-constant clause, or only
the two-run and reproduction rules?). This repair lane resolves that question from the bank's own
words and re-verifies everything independently. My verification script is
panel/criterion_repair_check.py (stdlib-only, my own code; the CRT is written from scratch with
extended Euclid and pairwise congruence combining — it does NOT reuse claim/crt_check.py). Run as:
`<python3>` -I `criterion_repair_check.py`
— 50/50 checks PASS (two earlier FAIL lines in my first run were my own check tolerances, fixed
and documented below). I also re-fetched the live b-file myself (see Clause 1).

## 0. The inheritance question — my reading (decided from the bank's own words)

READING CHOSEN: B. Partial win p1 inherits exactly the two-run rule (full criterion clause 2,
"computed by two independent runs that agree exactly (different primes/CRT moduli sets AND a
different decomposition ... or one exact big-integer run)") and the reproduction rule (clause 3,
"with the same code reproducing every published term for n <= N-1 exactly"), plus the object that
p1 itself restates ("the next unknown term(s)"). Clause 4 (growth constant, 1e-3 tolerance) is NOT
inherited by p1's text.

Reasoning, from the text quoted verbatim in claim/CLAIM.md:

1. The full success criterion is ONE sentence scoped to three named sequences (A028420, A006506,
   A063443). p1 is a separate sentence naming two DIFFERENT sequences (A054759, A027683) and
   supplying its own object spec — "The next unknown term(s) of ..." — which restates clause 1 in
   p1's own words rather than inheriting it. The bank's drafting pattern is therefore: p1
   re-specifies its object and borrows only the rules it names.
2. What p1 borrows is an explicit two-item enumeration: "same two-run and reproduction rules".
   "Two-run" and "reproduction" are the operative words lifted from clauses 2 and 3 of the full
   criterion. Clause 4's operative words ("consistent with the known growth constant", "within
   1e-3") appear NOWHERE in p1. Had the bank meant the whole criterion it would have said "same
   rules" or "same success criterion"; naming two of the four clauses is a selection, and
   expressio unius applies: the enumeration of the two rules implies the others are not imported.
3. "is a partial only" confirms p1 is a deliberately defined, lesser win — not the full criterion
   with a relaxed object. Under reading A (clause 4 inherited), p1 would be unwinnable by
   construction: the 1e-3 tolerance is unattainable at the sequence's live frontier N = 15 for ANY
   correct value (the PUBLISHED a(14) violates it by 5.50e-3, more than the claimed value's
   4.79e-3; n^2*d(n) ~= 1.08 across all published terms puts first attainability around N >= 33).
   A bank-defined partial win that no correct computation could ever satisfy would be a dead
   letter; reading B gives every word of p1 work to do and imports nothing unsatisfiable.
4. Is reading B a "stretched criterion"? No — it is the NARROWER, literal reading. The stretch
   would be reading A's import of a clause the text does not name, or any loosening of what p1
   DOES name. Nothing is loosened: the two named rules below are applied at full strength
   (including the AND of different-prime-sets AND different encoding, and wide CRT margins).
5. The growth question is not dodged — I verified it anyway (Clause 4 below) and the package
   discloses it honestly (growth.json's caveat). The pending bank-amendment proposal (finite-size
   model check for small-N partials) is out of scope: I judge the bank text AS IT IS.

## 1. Clause 1 (object): a(15) is the next unknown term, N = one more than the live frontier

VERDICT: PASS. I re-fetched https://oeis.org/A054759/b054759.txt myself (WebFetch, 2026-11-04):
exactly 14 lines, largest index 14, a(14) = 15844635835975276495290739119895808472, and the
claimed 43-digit value appears nowhere in the file. So N = 14 + 1 = 15 and the claim is exactly
the next unknown term. This upgrades v1's "recorded assertion" caveat to an independent live check;
novelty.md additionally verified the entry page and full revision history end at a(14).

## 2. Two-run rule (p1's named clause 2) — VERDICT: PASS

All from my own script (own CRT, own primality by trial division):

- Prime sets: run1 {31231..32611}, run2 {30091..31081}, 14 primes each; all prime, distinct within
  each set, all = 1 (mod 15); sets DISJOINT. residues_run2.json's note documents that the one
  originally overlapping prime (32611) was replaced by fresh 30091 — good hygiene.
- Residues: all 28 recorded residues equal value.txt mod their prime individually.
- CRT (my own implementation, from scratch): run1 and run2 each reconstruct EXACTLY
  4310182149988584261406143524214457416387448 = value.txt; recorded "modulus" fields equal the
  products of their primes: 2^209.5248 (run1), 2^208.6084 (run2).
- Rigorous bound: 2^15 * 1220^15 = 646915258962549275091904510950375424000000000000000 =
  2^168.789981 — equals the recorded "bound" field exactly, and is < 2^168.8 as REPRODUCE.md
  states (v1 and my first run had this check worded too strictly; 168.79 < 168.8 is correct).
- Margins: modulus/bound = 1.83e12 (~2^40.7) for run1 and 9.69e11 (~2^39.8) for run2 — each run's
  modulus ALONE exceeds the bound (and the value) by far more than the stated 1e6 margin, so each
  residue set alone pins the integer; the agreement is a genuine two-run exact agreement.
- Different decomposition/state encoding: I read both programs. iso_row.py: 2^15 states, wrap edge
  integrated into the transfer element, flip-set enumeration of alternating cyclic flips.
  iso_ht.py: 2^16 states (s, c) with the wrap-edge direction carried explicitly, transfer element
  built by an independent per-row walk-DFS, orbit-pair (O, c) isotypic structure. Different state
  spaces AND different transfer-element constructions: satisfies the parenthetical on both
  branches.
- Execution authenticity cross-check: the reproduce lane ran BOTH programs at fresh prime 29881
  (prime, = 1 mod 15, in neither set — I re-verified all three properties) and both printed
  10495 = value.txt mod 29881 (I recomputed the residue).

## 3. Reproduction rule (p1's named clause 3) — VERDICT: PASS

- ladder_run1.json and ladder_run2.json: for every n = 1..14, isotypic_mod == bfile mod prime
  (28/28 congruences verified from the recorded integers); every recorded zeta satisfies
  zeta^n = 1 (mod p); every validation prime is prime with n | p-1 (an order-n root exists); all
  matches flags true.
- The bfile fields in BOTH ladders equal, term by term, MY OWN live b-file fetch above — the
  ladder is checked against the real published values, and a(14) matches CLAIM.md's status fact.
- run1's "ref" fields: exact published integers for n <= 7 (equal to my fetched b-file values);
  direct_mod refs for n = 8..14 equal bfile mod p for p = 17, 19, 31, 23, 37, 53, 29 (all prime).
- Validation primes {101, 103, 109, 113, 131, 199} and direct_mod primes {17, 19, 23, 29, 31, 37,
  53} are disjoint from both claim prime sets — the ladder checks are not rigged by the claim's
  own moduli.
- The reproduce lane re-ran both ladder modes fresh and got field-by-field identical JSONs (28/28
  OK lines), which I treat as corroboration; my own verification above stands on the recorded
  integers alone.

## 4. Growth-constant clause (full-criterion clause 4; NOT inherited by p1 — checked anyway)

- Literal check: ln(a15)/225 = 0.43630912920511505 (bit-match to growth.json); minus
  lnW = 1.5 ln(4/3) = 0.4315231086776713 (exact) gives deviation 4.786021e-3 > 1e-3: the LITERAL
  clause FAILS for the claimed value at N = 15 — as it does for the PUBLISHED a(14) (5.496760e-3,
  fails harder) and every published n = 4..14 (n^2*d = 1.0919, 1.0841, 1.0809, 1.0793, 1.0786,
  1.0780, 1.0779, 1.0774, 1.0775, 1.0770, 1.0774 — all recomputed by me from my fetched b-file
  values). The claimed value continues the trend at n^2*d = 1.0769. So the literal clause is
  unsatisfiable at N = 15 for ANY correct value: a criterion-tolerance defect, not a value defect
  (same finding as v1 — v1 was right on this clause).
- Finite-size model (the caveat's handling): ln a(n) = W2 n^2 + A + B/n with W2 fixed at Lieb's
  constant. I refit independently: unweighted LS on window n = 8..14 reproduces growth.json's
  fitA = 1.0753117737759896 and fitB = 0.0251737322223888 to ~1e-11 (mine: 1.075311773775986,
  0.02517373222242), and predicted_a15 == exp(W2*225 + A + B/15) exactly (log diff 0.0);
  |ln(computed/predicted)| = 1.354039e-4 < 1e-3. So the claimed value IS consistent with the
  entropy constant under the model the published terms themselves follow.
- free_fit_c = 0.4315333419 reproduces on the same window (mine 0.43153334197); it is
  window-dependent (my windows 4..14 through 10..14 give c* within 4.5e-5 of Lieb, all well below
  the 1e-3 scale) — immaterial, as REPAIR.md anticipates. growth.json's predicted_a15_free sits
  4.819e-4 off the computed value in log (recorded datum; still < 1e-3, and supplementary — the
  load-bearing fixed-W2 check is the 1.354e-4 one).
- Bank's own skeptic-side growth operationalization ("check digit count against the
  entropy-constant growth estimate"): value.txt has 43 digits; floor(225*lnW/ln10) + 1 = 43. PASS.
  Also a15/a14 = 272027.85 vs finite-size model 272134.11 (-0.039%).
- Known recording nits (immaterial, verified): growth.json records the model log-ratio with the
  sign convention ln(predicted/computed) (magnitude exact); CLAIM.md quotes the entry's Lieb value
  "0.431523058..." vs exact 0.431523109 (5e-8, entry rounding); REPRODUCE.md's "both CRT moduli
  exceed 2^209" is 2^209.52 / 2^208.61 in fact — the load-bearing bound-vs-margin claim is exact.

## 5. Digit count — VERDICT: PASS (43 digits, see Clause 4).

## confirmed_scope

Confirmed, under reading B of the bank's partial win p1 (p1 inherits exactly the two-run rule and
the reproduction rule from the full criterion, and restates its own object; the growth-constant
clause is not part of p1 as written): a(15) = 4310182149988584261406143524214457416387448 is the
next unknown term of A054759 after the live frontier a(14) (b-file re-fetched live by me,
2026-11-04), produced by two independent runs with disjoint 14-prime CRT sets and different state
encodings (2^15 row-integrated vs 2^16 h-tracked) that agree exactly, each CRT modulus exceeding
the rigorous bound 2^168.79 (recorded bound field verified exact) with ~2^40 margin and each
reconstructing value.txt under my own from-scratch CRT, with both codes reproducing all published
a(1)..a(14) (28/28 congruences verified against my own live b-file fetch, validation primes
disjoint from the claim primes) and the 43-digit count matching the entropy estimate; documented
caveat outside p1's inherited clauses: the full criterion's literal 1e-3 growth clause fails at
N = 15 for any correct value (published a(14) deviates 5.50e-3, claimed value 4.79e-3, n^2*d ~=
1.08 throughout the published range), while the claimed value is consistent with Lieb's constant
under the published terms' own finite-size model (|log-ratio| 1.354e-4, model and constants
reproduced independently) — a criterion-tolerance defect already flagged by v1 and now subject of
a separate bank-amendment proposal.

pass: true
