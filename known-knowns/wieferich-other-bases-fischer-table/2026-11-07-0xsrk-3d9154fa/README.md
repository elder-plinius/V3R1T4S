# Wieferich pair (56350, 1024048960667): wieferich-other-bases-fischer-table, partial win p1

## What
> The single pair in object/pair.json, base 56350 = 2·5^2·7^2·23 (not a perfect power, strictly between 10125 and 65537) with p = 1024048960667 (above 1e12, proven prime by trial division up to its square root), satisfies 56350^(p-1) ≡ 1 (mod p^2) in exact integer arithmetic and is absent from Fischer's FermQ_Sorg.txt and FermQ_Sort.txt as snapshotted in the-record-we-beat/RECORD.md (neither has a row for any base between 10125 and 65537 and neither contains p) and from an OEIS search for p made on 2026-11-07, so it meets partial win p1 of wieferich-other-bases-fischer-table but not the full win, which requires a base of at most 10125.

In plain terms: 1024048960667 is a Wieferich prime to the base 56350 = 2·5²·7²·23, i.e. 56350^(p−1) ≡ 1 (mod p²).
- The base lies above the range of Richard Fischer's tables (10125 < b < 65537), and p is above 10^12.
- 56350 is the only base in 2..70000 for which this p is a Wieferich prime (panel/novelty.md, section 4).
- p is also a safe prime: (p − 1)/2 = 512024480333 is prime (panel/reproduce.md).

## Check it yourself
From this folder (Python 3.8+, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. It takes well under a second on a laptop. The one-line equivalent is
`python3 -c "p=1024048960667; print(pow(56350, p-1, p*p))"`, which prints `1`.

## Compared to
- Table: Richard Fischer's Fermat-quotient tables at fermatquotient.com:
  - FermQ_Sorg.txt, bases 2..10125, "durchsucht bis 4.8E+12";
  - FermQ_Sort.txt, bases 2..1052 plus 65537.
- Cell: base 56350.
  - Neither file has a row for it, because no base 10126..65536 is tabulated, and the number 1024048960667 occurs in
    neither file.
  - It occurs in none of Fischer's other Fermat-quotient files read by the panel either: ErstBasen.txt, ErstPBasen.txt,
    News.txt, FermatQ3.txt and SwitchFermQ.txt (panel/novelty.md, panel/criterion.md).
  - Table value for the cell: none. This package adds one pair.
- URLs, UTC fetch times, HTTP status, selected headers and page sha256 are in the-record-we-beat/RECORD.md.
  - The scout fetched the tables at 2026-11-07T21:59:02Z.
  - The panel re-fetched them at 22:05:41Z-22:06:01Z (NOVELTY) and before 22:06:28Z (CRITERION).
  - All copies are byte-identical.
- OEIS: searches for 1024048960667 on 2026-11-07 at 21:59:04Z (scout), 22:06:13Z (NOVELTY) and before 22:06:28Z
  (CRITERION) returned no match.
- Related claims in this repository: draft PRs #973, #983, #999 and #1008 hold four other pairs of the same cell,
  with other primes.

## Not claimed
- Not a full win: the base 56350 is above 10125.
- Nothing about smaller Wieferich primes to base 56350.
- No search certificate: nothing is claimed about the rest of the swept range, other bases or other primes.
- No novelty beyond the sources checked in panel/novelty.md:
  - Fischer's Fermat-quotient files and OEIS;
  - this repository's tree, trophy case, known-knowns, releases and pull requests;
  - GitHub and web searches covering the last 24 months.
  The gate repeated a GitHub code search once, with no result (panel/gate.md).
- Panel note:
  - The three skeptics ran as isolated headless Claude Code sessions (`claude -p --safe-mode`). Each was started in
    its own copy of the claim folder outside the contributor's workspace, so no workspace notes were in its context.
  - panel/gate.md records the path audit of each session.
  - It also records one corrected supporting statement in panel/novelty.md, about the repository's folder tree. The
    correction does not affect the verdict.

## Credits
- Richard Fischer, Fermat-quotient tables (http://www.fermatquotient.com/), continuing the tables of Wilfrid Keller and
  Jörg Richstein. They are the bar this pair is compared against.
- OEIS Foundation (https://oeis.org/), novelty lookups.
- Primality: trial division, the deterministic Miller-Rabin bounds of Jiang & Deng (2014), Sorenson & Webster (2015)
  and Jaeschke (1993), and the Lucas (n−1) criterion used by the panel.
- GMP via gmpy2 (https://github.com/aleaxit/gmpy) and NumPy (https://numpy.org/), the search tooling in how-we-built-it/.
- The V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S): target definition, run protocol and three-skeptic panel.
- Found in a V3R1T4S run credited to 0xSrk.
