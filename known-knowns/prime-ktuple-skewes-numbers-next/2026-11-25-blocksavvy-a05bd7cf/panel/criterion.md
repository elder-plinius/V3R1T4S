role: CRITERION
context: fresh subagent (knowledgeWork)
claim: sexy-prime Skewes number p = 349018493647
date_utc: Wed Nov 25 01:44:29 UTC 2026

## Criterion being judged (bank target prime-ktuple-skewes-numbers-next, full success criterion, not a partial win)
(1) p starts an instance of P; (2) exhaustive enumeration of all instances up to p (code and counts given) shows
pi_P(q) <= C_P Li_P(q) at every instance q < p and pi_P(p) > C_P Li_P(p), Li_P by rigorous quadrature, C_P to >= 15 digits;
(3) the value fills a cell absent on the day of claiming, here "the (p, p+6) Skewes number". Partial wins p1/p2 are not
claimed and not needed.

## Hidden quantifiers and definitions checked
- Counting convention. Toth (arXiv:1910.02636, fetched once 2026-11-25T01:42Z UTC, HTTP 200): Conjecture 1 says "less then n",
  but Definition 2 only says "pi_P(n) the counting function for P"; his twin-prime paragraph says "primes not exceeding n";
  his Algorithm 1 tests (i - C*Li(p_i)) at the i-th instance p_i, which is inclusive counting. OEIS A210439 (saved copy and the
  live text) says "the least prime ... at which for the first time pi_n(p) > C_n*Li_n(p)", and its example counts the twin
  crossing as "the 10744th pair (1369391, 1369393)", i.e. pi_2(1369391) = 10744 includes p. My own sieve plus mpmath (mycheck.py
  in the sandbox) reproduces 1369391 (Wolf; Toth) and 5206837 (Toth) only under inclusive counting; exclusive gives 1369427 and
  5206963, which match no published value. So inclusive is the operative published convention; "less than" in Conjecture 1 is
  an asymptotic statement where the convention does not matter. The claim states its convention and also discloses the
  exclusive value 349018493981, which I reproduced independently (mywin.py). Not a stretched definition.
- Consecutive vs non-consecutive: Toth's patterns (and the bank pitfall) do not require consecutiveness; the claim counts all
  (q, q+6) with both prime (A023201/A080841 sense) and explicitly disclaims A031924. My counts of blocks 0..7 (n < 100663296)
  match result/block_counts exactly, and its counts at 1e11, 1e12 equal OEIS A080841(11), A080841(12) (consecutive-only counts
  would be far smaller), so the code counts non-consecutive pairs.
- C_P: Toth's formula with k=1, w(3)=1 gives 2*C2*(3/2)/(3/4) = 4*C2. Claim C = 2.6406472633874782957...; mpmath 4*twinprime
  = 2.64064726338747829571124844005822311...; agrees to > 30 digits (>= 15 required).
- Li_P from 2: code uses [li(t) - t/log t] from 2 to x in Arb (200 bits); I checked mpmath.quad of int_2^x dt/log^2 t at p
  equals the closed form to 30 digits: C*Li2(p) = 1416008995.520836266359010..., pi_6(p) = 1416008996, margin -0.479.
- Every earlier pair (the "at every instance q < p" quantifier): coverage is complete with no gap: (a) n <= 100663296 exact
  Arb comparison at every pair (small2.py, undecided=0, min margin 5.25 at q=5); (b) blocks 8..27736 (starts >= 100663296,
  ends 349012230144) by a chord bound: L[] = Arb lower bounds of C*Li2 rounded down 2 ulps at block ends, Li2 is concave
  (second derivative -2/(t log^3 t) < 0), so the chord of lower bounds is below C*Li2 inside each block; sexyA records
  M = max over pairs of (rank - slope*(n-a)) and post.py requires L[b] - N_before - M > 0; reported min margin 143.296 (block
  27736), flagged only block 27737; float error in M is ~1e-6, irrelevant at that margin; (c) block 27737 up to p: exact Arb
  check of all 23595 pairs (verify_claim.py, I ran it: PASS), and my own independent numpy sieve + mpmath over the same window
  with the table prefix N0 = 1415985401 gives the same first violation, min margin before p 0.1758 (at 349018490077), 23594
  earlier pairs all satisfied. Equality pi = C*Li2 cannot occur at the margins involved (all decided intervals).
- Pattern instance: p = 349018493647 and p+6 = 349018493653 both prime (flint BPSW + sympy in verify_claim; my sieve agrees).
- Cell (3): re-checked once each, 2026-11-25T01:43Z UTC, honest UA, HTTP 200: Wikipedia "Skewes's number" (last edited
  28 October 2026) still says "The Skewes number (if it exists) for sexy primes (p, p+6) is still unknown."; OEIS search for
  349018493647: "No results."; A210439 has no sexy entry (it is over minimal-span n-tuplets). The cell is unfilled.
- Null model / subsumption: public A080841(12) together with C*Li2(1e12) already implies some crossing below 1e12 (deficit
  -97764 at 1e12), but not its location; the first crossing value is not published anywhere I checked, so the claim is not a
  trivial consequence of published data. It is a full win, not one subsumed by p1 or any published object (novelty in depth is
  the NOVELTY skeptic's job).

## Dependency / limits of this verdict
I did not rerun the full 3.5e11 recount (the REPRODUCE skeptic's mandate). The quantifier over blocks 8..27736 rests on the
author's two sieves (agreeing per block to 1e12 and with A080841) plus the chord-bound logic I audited; I verified block counts
0..7, the crossing window, the constant, the Li2 evaluation, the convention calibration and the cell status independently.
If REPRODUCE's independent recount disagrees with result/block_counts, this pass is void.

## Verdict
Literally meets the full success criterion (1)-(3) for the cell "the (p, p+6) Skewes number" under the published (inclusive,
Toth-algorithm / OEIS A210439 / Wolf-calibrated) convention, non-consecutive pairs, C = 4*C2, Li2 from 2. The exclusive
reading would give 349018493981 instead; the claim must keep that convention stated wherever the number is reported.

confirmed_scope: Under inclusive counting (pi_6(x) = #{prime q <= x : q+6 prime}, non-consecutive pairs), C = 4*C2 and Li_2(x) = int_2^x dt/log^2 t, the first prime p with pi_6(p) > C*Li_2(p) is p = 349018493647 (pi_6(p) = 1416008996 vs C*Li_2(p) = 1416008995.5208...), conditional on the exhaustive pair counts below 349012230144 being independently reproduced.
pass: true
