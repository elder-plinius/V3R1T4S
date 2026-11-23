# Wieferich pair (5481, 4848813530161): wieferich-other-bases-fischer-table, full win

## What
> The pair in object/pair.json (b = 5481 = 3^3·7·29, not a perfect power; p = 4848813530161, proven prime by trial division to its square root and by a Pocklington certificate) satisfies 5481^(p−1) ≡ 1 (mod p^2) in exact arithmetic, p is strictly greater than the 4.8E+12 searched limit stated in FermQ_Sorg.txt and is absent from base 5481's row there, from FermQ_Sort.txt (which has no 5481 row) and from OEIS as recorded in the-record-we-beat/RECORD.md (the three Fischer tables re-fetched byte-identical at 2026-11-07T22:46:58Z–22:47:13Z), so it counts as one new pair under the full success criterion of wieferich-other-bases-fischer-table, with neither headline flag (not a Mirimanoff prime, not a double Wieferich pair).

In plain terms: 4848813530161 is a Wieferich prime to the base 5481 = 3³·7·29, i.e. 5481^(p−1) ≡ 1 (mod p²).
- Base 5481 lies inside Richard Fischer's main table (bases 2..10125). Its row lists only 2 and 751787 up to the
  table's stated search limit of 4.8·10^12.
- This p is 1.0% above that limit, and it is a new entry for the row.
- 5481 is the only base in 2..10125 for which this p is a Wieferich prime (panel/novelty.md, section 6;
  panel/criterion.md, section 2).

## Check it yourself
From this folder (Python 3.8+, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. It takes well under a second on a laptop. The one-line equivalent is
`python3 -c "p=4848813530161; print(pow(5481, p-1, p*p))"`, which prints `1`.

## Compared to
- Table: Richard Fischer's Fermat-quotient table FermQ_Sorg.txt at fermatquotient.com: bases 2..10125, "Die Basen sind
  gegenwaertig durchsucht bis 4.8E+12". FermQ_Sort.txt covers bases 2..1052 plus 65537, so it has no row for 5481.
- Cell: base 5481. Its row reads `5481,  2^3, 751787`, so the table value for the cell is the primes 2 (to the third
  power) and 751787, searched to 4.8E+12.
  - This package adds 4848813530161 to that row.
  - The table lists no entry above 4.8E+12 for any base from 1053 to 10125; its largest is 4795482544417, for base
    1999 (panel/criterion.md).
- The number 4848813530161 occurs in none of Fischer's files read by the panel. Those are FermQ_Sorg.txt,
  FermQ_Sort.txt, ErstBasen.txt, ErstPBasen.txt, SwitchFermQ.txt, News.txt and FermatQ3.txt.
- URLs, UTC fetch times, HTTP status, selected headers and page sha256 are in the-record-we-beat/RECORD.md.
  - The scout fetched the tables at 2026-11-07T22:40:10Z, immediately before the claim.
  - The panel re-fetched them at 22:45:05Z-22:45:14Z (NOVELTY) and 22:46:58Z-22:47:13Z (CRITERION).
  - All copies are byte-identical.
- OEIS:
  - searches for 4848813530161 on 2026-11-07 (scout, NOVELTY, CRITERION) returned no match;
  - no OEIS sequence of base-5481 Wieferich primes exists. A search for the row's prime 751787 finds four
    sequences, none of them a Wieferich sequence.
- Related claims in this repository: draft PRs #973, #983, #999 and #1008 hold partial-win p1 pairs, with bases above
  10125 and other primes.

## Not claimed
- No headline flag: b is not 3 (no Mirimanoff prime), and p^(b−1) mod b² = 25942981, so this is not a double
  Wieferich pair.
- Nothing about computations Fischer has not published. The table's stated limit has two significant figures, and p
  is only 1.0% above it. The claim rests on the stated limit and the published row, as the criterion is written
  (panel/criterion.md, section 4).
- No search certificate: nothing is claimed about the rest of the swept range, other bases or other primes.
- No novelty beyond the sources checked in panel/novelty.md:
  - Fischer's files and OEIS;
  - this repository's tree, trophy case, known-knowns, releases and pull requests;
  - GitHub and web searches covering the last 24 months.
- Panel note: the three skeptics ran as isolated headless Claude Code sessions (`claude -p --safe-mode`). Each was
  started in its own copy of the claim folder outside the contributor's workspace, so no workspace notes were in its
  context. panel/gate.md records the path audit of each session.

## Credits
- Richard Fischer, Fermat-quotient tables (http://www.fermatquotient.com/), continuing the tables of Wilfrid Keller and
  Jörg Richstein. They are the record this pair extends.
- OEIS Foundation (https://oeis.org/), novelty lookups.
- Primality: trial division, the Lucas and Pocklington (n−1) criteria used by the panel, and the deterministic
  Miller-Rabin bounds of Jiang & Deng (2014) and Sorenson & Webster (2015) used by verify.py.
- GMP via gmpy2 (https://github.com/aleaxit/gmpy) and NumPy (https://numpy.org/), the search tooling in how-we-built-it/.
- The V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S): target definition, run protocol and three-skeptic panel.
- Found in a V3R1T4S run credited to 0xSrk.
