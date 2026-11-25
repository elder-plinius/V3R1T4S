# Sexy-prime (p, p+6) Skewes number: p = 349018493647

## What

Under inclusive counting (pi_6(x) = #{prime q <= x : q+6 prime}, non-consecutive pairs), C = 4*C2 and Li_2(x) = int_2^x dt/log^2 t, the first prime p with pi_6(p) > C*Li_2(p) is p = 349018493647 (pi_6(p) = 1416008996 vs C*Li_2(p) = 1416008995.5208...), conditional on the exhaustive pair counts below 349012230144 being independently reproduced.

Note: the sentence above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`). Its condition is
met: the REPRODUCE skeptic recounted every pair start below 349024813056 with its own sieve (total 1416032531; all 27738 block counts
equal `object/block_counts_0_to_27737.txt`) and proved the inequality at every earlier pair (`panel/reproduce.md`).

Convention: counting is inclusive (q <= p), the OEIS A210439 wording ("pi_n(p) > C_n*Li_n(p)"); the same code with inclusive counting
returns the published twin (1369391, Wolf 2011) and cousin (5206837, Toth 2019) Skewes numbers. Under exclusive counting (q < p) the
first violation would be **349018493981** instead (disclosed; that convention does not reproduce the published twin/cousin values).
Object: `object/sexy_skewes.json` (sha256 `a05bd7cfaf93b4f4dc53cc370a9157e1ffa55e80d843120bde972940c56357c5`).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only).
- **Rough laptop time:** about 20-30 seconds (`verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It proves p and p+6 prime, recounts blocks 0..7 (n < 100663296) and pi6(1e8), checks every field of the object and the table index, sieves p's whole block (count must match the table) and compares every pair up to p with
C*Li2 (45-digit decimal Li2 plus monotone enclosures). The full exhaustive recount below p's block (C, about 5-10 minutes on a laptop)
is step 2 of `RUN_IT_YOURSELF.md`.

## Compared to

| source | cell | listed value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A210439 (status source) | sexy pairs (p, p+6) | no entry (sequence covers minimal-span n-tuplets) | 349018493647 | https://oeis.org/A210439 | 2026-11-25T00:47:59Z (panel: 01:41:55Z) |
| Wikipedia, Skewes's number | (p, p+6) | "still unknown" | 349018493647 | https://en.wikipedia.org/wiki/Skewes%27s_number | 2026-11-25T00:47:59Z |

Details in `the-record-we-beat/README.md`.

## Not claimed

- Nothing about consecutive sexy primes (A031924), later sign changes, A210439(10) or A332493(9).
- OEIS A080841(12) (Earls; Chaffin) together with C*Li2(10^12) already implies that some crossing lies below 10^12; what is new here is
  its exact location (the first one).
- Not peer reviewed; the panel reports are in `panel/`.

## Credits

- **Laszlo Toth**, "On the asymptotic density of prime k-tuples and a conjecture of Hardy and Littlewood", CMST 25(3) (2019),
  https://arxiv.org/abs/1910.02636 (definition of k-tuple Skewes numbers).
- **Marek Wolf** (twin-prime Skewes number 1369391, 2011), **Hugo Pfoertner**, **Norman Luhn**, **Karl Desfontaines** (k-tuplet Skewes
  numbers, https://oeis.org/A210439).
- **Jason Earls**, **Benjamin Chaffin** and OEIS editors (sexy-pair counts, https://oeis.org/A080841); twin prime constant
  https://oeis.org/A005597.
- **G. H. Hardy and J. E. Littlewood** (1923 prime k-tuple conjecture); FLINT/Arb (https://flintlib.org) and mpmath (https://mpmath.org).
- Contributor credit: BlockSavvy, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
