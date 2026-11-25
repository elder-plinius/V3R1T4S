# Claim (single context, not yet panelled)

target: prime-ktuple-skewes-numbers-next
status_source: https://oeis.org/A210439
cell: the (p, p+6) Skewes number (sexy primes)

**One sentence.** For the prime pair pattern (p, p+6) (p and p+6 both prime, not necessarily consecutive primes), with
pi_6(x) = #{prime q <= x : q+6 prime}, C = 4*C_2 = 2.6406472633874782957... and Li_2(x) = int_2^x dt/(log t)^2, the first
prime p with pi_6(p) > C*Li_2(p) is **p = 349018493647** (p+6 = 349018493653): pi_6(p) = 1416008996 while
C*Li_2(p) = 1416008995.5208362663590 (+/- 1e-14), and pi_6(q) <= C*Li_2(q) holds at every one of the 1416008995 earlier
pair starts q. Label: PROVED-HERE (computer-assisted exhaustive enumeration with two separately written sieves and
interval arithmetic; not peer reviewed).

## Success criterion (verbatim from bank/targets.json)
Success means a prime p and a pattern P such that (1) p starts an instance of P; (2) an exhaustive enumeration of all instances of P up to p (code and counts given) shows pi_P(q) <= C_P Li_P(q) at every instance q < p and pi_P(p) > C_P Li_P(p), with Li_P evaluated by rigorous quadrature (mpmath or Arb) and C_P computed to at least 15 digits; and (3) the value fills a cell absent on the day of claiming: A210439(10), A332493(9), or the (p, p+6) Skewes number, re-checked on OEIS (A210439, A332493) and on Wikipedia/OEIS for the sexy case. The skeptic recounts the instances with an independent sieve: all of them for the sexy case. For 9- and 10-tuplets the recount is cross-checked against Luhn's smallest k-tuplet database where it reaches (9-tuplets to 10^18, 10-tuplets to 10^20), plus random-window recounts beyond it. The skeptic also re-evaluates the comparison near p. A full win for A332493(9) also requires the first crossings of all four 9-tuplet types.

## Definitions and conventions used
- Pattern: Toth (arXiv:1910.02636, Definition 2) and Wikipedia "Skewes's number" section on prime k-tuples: pairs
  (p, p+6) of primes, consecutiveness NOT required (OEIS A023201 / A080841 sense, not A031924).
- Hardy-Littlewood constant: C = 2*C_2*prod_{p | 6, p > 2} (p-1)/(p-2) = 4*C_2, C_2 = 0.66016181584686957392781211001455577843262336029 (+/- 6e-48),
  certified in code/constant.py; equals OEIS A005597 (data/oeis.org_A005597.html).
- Li_2 from 2: Li_2(x) = [li(t) - t/log t] from 2 to x, evaluated in Arb (python-flint, 200 bits) and independently in mpmath (50 digits).
- Counting is inclusive (q <= p), the OEIS A210439 convention ("pi_n(p) > C_n*Li_n(p)"). Calibration: the same code
  with inclusive counting returns the published twin (1369391, Wolf 2011) and cousin (5206837, Toth 2019) Skewes
  numbers; exclusive counting (q < p) would give 1369427 and 5206963, which are not the published values. For
  transparency: under exclusive counting the sexy-pair first violation would be 349018493981 (outputs/exact_block27737_conventions.txt).

## Evidence (all in this folder)
- result/skewes.json: the value, counts, margins. result/block_counts_0_to_27737.txt: pair counts of all 27738 blocks of
  length 12582912 from n = 0 through the crossing block (identical in sieve A and sieve B).
- outputs/: captured outputs of every step (see REPRODUCE.md).
- Power-of-ten counts from both sieves: pi_6(1e8)=879908, (1e9)=6849047, (1e10)=54818296, (1e11)=448725003,
  (1e12)=3741217498; the last two equal OEIS A080841(11), A080841(12) (Jason Earls et al.; counts by upper member q+6 < 10^n,
  identical here).
- data/: status pages as fetched 2026-11-25T00:47:59Z-00:54:02Z (OEIS A210439, Wikipedia Skewes's number, OEIS A005597, OEIS A080841).

## Status check (scout, 2026-11-25T00:47:59Z, HTTP 200)
- OEIS A210439: terms a(2..9), no sexy-prime entry (A210439 is over minimal n-tuplets; the twin pair gives a(2)).
- Wikipedia "Skewes's number" (last edited 28 October 2026): "The Skewes number (if it exists) for sexy primes (p, p+6) is still unknown."
- GitHub search of elder-plinius/V3R1T4S pull requests (Skewes, sexy, Hardy-Littlewood, tuplets, target id): 0 results.
- Web search for the number 349018493647: no mathematical hit.

## Not claimed
- Nothing about consecutive sexy primes (A031924), about later sign changes, or about A210439(10) / A332493(9).
- Not peer reviewed; not panelled (single-context). The panel decides.

## Credits
Laszlo Toth (definition, arXiv:1910.02636), Marek Wolf (twin Skewes number 1369391), Hugo Pfoertner, Norman Luhn and
Karl Desfontaines (k-tuplet Skewes computations, OEIS A210439), Jason Earls and OEIS contributors (A080841 counts),
Hardy and Littlewood (1923 conjecture), the Arb/FLINT and mpmath authors.
