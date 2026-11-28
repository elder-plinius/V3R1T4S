# Wieferich pair (24766, 1000747824697): wieferich-other-bases-fischer-table, partial win p1

## What
> Against the p1 text as quoted in claim.md, the pair (b, p) = (24766, 1000747824697) has 10125 < b < 65537, b = 2*7*29*61 not a perfect power, p > 10^12 proven prime (full trial division and a Lucas certificate) and not dividing b, and 24766^(p-1) == 1 (mod p^2) by exact integer arithmetic, while neither claim/inputs copy of FermQ_Sorg.txt or FermQ_Sort.txt (hashes as recorded, not re-fetched) has a row for 24766 or contains p, and one OEIS search at 2026-11-07T12:24:27Z returned HTTP 200 with no match, so the object meets partial win p1 and not the full win (b > 10125); novelty against any other source, a live re-fetch of the tables and whether the quoted criterion matches the bank file are not established.

In plain terms: 1000747824697 is a Wieferich prime to the base 24766, i.e. 24766^(p−1) ≡ 1 (mod p²). The base lies above
the range of Richard Fischer's tables (10125 < b < 65537), and p is above 10^12. Two of the items the sentence leaves open
are covered in panel/novelty.md and panel/gate.md:
- the NOVELTY skeptic re-fetched both Fischer files live (2026-11-07T12:18:47Z, HTTP 200, byte-identical to the
  snapshots) and searched further sources;
- the gate compared the quoted p1 text with the bank file and found it verbatim.

## Check it yourself
From this folder (Python 3.8+, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. It takes well under a second on a laptop. The one-line equivalent is
`python3 -c "p=1000747824697; print(pow(24766, p-1, p*p))"`, which prints `1`.

## Compared to
- Table: Richard Fischer's Fermat-quotient tables at fermatquotient.com:
  - FermQ_Sorg.txt, bases 2..10125, "durchsucht bis 4.8E+12";
  - FermQ_Sort.txt, bases 2..1052 plus 65537.
- Cell: base 24766. Neither file has a row for it (no base 10126..65536 is tabulated), and the number 1000747824697 occurs
  in neither file. Table value for the cell: none. This package adds one pair.
- URLs, UTC fetch times, HTTP status and page sha256 are in the-record-we-beat/RECORD.md: scout fetch
  2026-11-07T11:58:09Z, panel re-fetch 2026-11-07T12:18:47Z.
- OEIS: three independent searches for 1000747824697 on 2026-11-07 returned no match.

## Not claimed
- Not a full win: the base 24766 is above 10125.
- Not the smallest Wieferich prime to base 24766: 777979 is smaller (panel/novelty.md).
- No search certificate: nothing is claimed about the rest of the swept range, other bases or other primes.
- No novelty beyond the sources checked in panel/novelty.md: Fischer's files, OEIS, arXiv, web and GitHub searches of the
  last 24 months, and this repository's trophy case, known-knowns and pull requests. GitHub code search (login
  required) was not run.

## Credits
- Richard Fischer, Fermat-quotient tables (http://www.fermatquotient.com/), continuing the tables of Wilfrid Keller and
  Jörg Richstein. They are the bar this pair is compared against.
- OEIS Foundation (https://oeis.org/), novelty lookups.
- Primality: the deterministic Miller-Rabin bounds of Jiang & Deng (2014), Sorenson & Webster (2015) and Jaeschke (1993),
  and the Lucas (n−1) criterion used by the panel.
- GMP via gmpy2 (https://github.com/aleaxit/gmpy) and NumPy (https://numpy.org/), the search tooling in how-we-built-it/.
- The V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S): target definition, run protocol and three-skeptic panel.
- Found in a V3R1T4S run credited to 0xSrk.
