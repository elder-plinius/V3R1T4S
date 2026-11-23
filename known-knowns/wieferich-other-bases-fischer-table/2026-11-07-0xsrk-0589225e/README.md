# Wieferich pair (17766, 1016845912283): wieferich-other-bases-fischer-table, partial win p1

## What
> The pair in object/pair.json, base b = 17766 (2 × 3^3 × 7 × 47, not a perfect power, strictly between 10125 and 65537) and p = 1016845912283 (proven prime by trial division up to its square root and by a Lucas certificate, above 1e12), satisfies b^(p-1) == 1 (mod p^2) in exact integer arithmetic and is absent from both Fischer tables, FermQ_Sorg.txt and FermQ_Sort.txt, in the 2026-11-07 snapshots identified in the-record-we-beat/RECORD.md (sha256 beginning 35273a26 and bda97784 respectively), and from OEIS (no match for p on 2026-11-07), so it meets partial win p1 of wieferich-other-bases-fischer-table and not the full win, whose base range ends at 10125.

In plain terms: 1016845912283 is a Wieferich prime to the base 17766 = 2·3³·7·47, i.e. 17766^(p−1) ≡ 1 (mod p²). The
base lies above the range of Richard Fischer's tables (10125 < b < 65537), and p is above 10^12. 17766 is the only base
in 2..65537 for which this p is a Wieferich prime (panel/novelty.md, section 4).

## Check it yourself
From this folder (Python 3.8+, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. It takes well under a second on a laptop. The one-line equivalent is
`python3 -c "p=1016845912283; print(pow(17766, p-1, p*p))"`, which prints `1`.

## Compared to
- Table: Richard Fischer's Fermat-quotient tables at fermatquotient.com:
  - FermQ_Sorg.txt, bases 2..10125, "durchsucht bis 4.8E+12";
  - FermQ_Sort.txt, bases 2..1052 plus 65537.
- Cell: base 17766. Neither file has a row for it (no base 10126..65536 is tabulated), and the number 1016845912283
  occurs in neither file. It also occurs in none of Fischer's other files that list pairs, including the "extreme
  first bases" files ErstBasen.txt and ErstPBasen.txt, which list some pairs above 10^12. Table value for the cell:
  none. This package adds one pair.
- URLs, UTC fetch times, HTTP status, selected headers and page sha256 are in the-record-we-beat/RECORD.md. The scout
  fetched the tables at 2026-11-07T17:53:48Z, and the panel re-fetched them at 2026-11-07T18:34:23Z and 18:40:34Z; all copies
  are byte-identical.
- OEIS: four searches for 1016845912283 on 2026-11-07 (18:30:31Z, 18:34:24Z, 18:38:45Z, 18:40:34Z) returned no match.
- Related claims in this repository, different objects in the same cell: draft PR #973, the pair
  (24766, 1000747824697), and draft PR #983, the pair (28910, 1011548897263).

## Not claimed
- Not a full win: the base 17766 is above 10125.
- No search certificate: nothing is claimed about the rest of the swept range, other bases or other primes.
- No novelty beyond the sources checked in panel/novelty.md:
  - Fischer's files and OEIS;
  - web and GitHub repository searches of the last 24 months;
  - this repository's tree, trophy case, known-knowns, releases and pull requests.

## Credits
- Richard Fischer, Fermat-quotient tables (http://www.fermatquotient.com/), continuing the tables of Wilfrid Keller and
  Jörg Richstein. They are the bar this pair is compared against.
- OEIS Foundation (https://oeis.org/), novelty lookups.
- Primality: the deterministic Miller-Rabin bounds of Jiang & Deng (2014), Sorenson & Webster (2015) and Jaeschke (1993),
  and the Lucas (n−1) criterion used by the panel.
- GMP via gmpy2 (https://github.com/aleaxit/gmpy) and NumPy (https://numpy.org/), the search tooling in how-we-built-it/.
- The V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S): target definition, run protocol and three-skeptic panel.
- Found in a V3R1T4S run credited to 0xSrk.
