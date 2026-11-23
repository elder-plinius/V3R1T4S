# Mahler's problem: a Littlewood polynomial of degree 32 with larger Mahler measure than the table

## What

The ±1-coefficient polynomials in object/d32.txt, object/d36.txt and object/d40.txt (degrees 32, 36, 40; each irreducible and not skew-symmetric) have Arb-certified Mahler measures 5.53769342918880813876…, 5.86686085131976269717… and 6.15435589127620035909…, whose certified lower bounds exceed the maximum listed for that degree in LargeSkewSymmLittlewood.txt (database commit 7e3798516710370a758e16eb5de6bccbee98bb6a, identical to the live repository on 2026-11-21) by 8.16e-2, 4.35e-2 and 7.10e-4 respectively (each > 1e-9), and no other file of that database lists a value at those degrees that is as large; comparison with newer literature was not checked.

This package claims one cell, degree 32: the Littlewood polynomial in `object/littlewood_d32.txt` (coefficients of x^0, x^1, ..., x^32; `+` = +1, `-` = -1) has Mahler measure **M(f) = [5.53769342918880813876303151919 +/- 4.92e-30]**, certified by Arb root isolation. That beats the largest value listed for degree 32 in LargeSkewSymmLittlewood.txt, **5.456083591785**, by 8.161e-02. The polynomial is not skew-symmetric.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Python 3 standard library only, under 30 s. The check is rigorous: exact-integer Graeffe root squaring gives a certified lower bound on M(f) without root finding, and the decision is an exact integer comparison against the table value + 1e-9. Expected last line: `PASS`.

## Compared to

- Mahler-Measure-Database, LargeSkewSymmLittlewood.txt (https://github.com/mossinghoff/Mahler-Measure-Database, commit 7e3798516710370a758e16eb5de6bccbee98bb6a, 2026-07-18; sha256 38d92d006622b8c8aec8261a7b369ff96b419c547825ad6f9e65670a4742b5c0): the maximum listed for degree 32 is 5.456083591785. Re-cloned 2026-11-21 at 18:46Z and 19:28Z, unchanged.
- LargeLittlewood.txt (all Littlewood polynomials) stops at degree 30, so the skew-symmetric maximum is the best published value at degree 32.
- See `the-record-we-beat/record.md`.

## Not claimed

- Not claimed to be the maximum over all Littlewood polynomials of degree 32: the search is heuristic, not exhaustive.
- Normalized value M(f)/sqrt(d+1) = 0.963989, below the Barker-13 record 0.98636 (criterion (ii) not claimed).

## Credits

- Contributor: @adamtpayne-cmd (search, certification and write-up by an AI agent, Claude, run by the contributor).
- Michael J. Mossinghoff, Mahler-Measure-Database (LargeLittlewood.txt, LargeSkewSymmLittlewood.txt) and "Mahler's problem and Turyn polynomials", arXiv:2405.08281.
- Peter Borwein and Michael J. Mossinghoff, "Barker sequences and flat polynomials", 2008; Peter Borwein, Computational Excursions in Analysis and Number Theory (Problem P10), 2002.
- FLINT/Arb (python-flint) and mpmath, used for certification.
