# Wieferich pair (36260, 1026120862861): wieferich-other-bases-fischer-table, partial win p1

## What
> The pair in object/pair.json (b = 36260, not a perfect power, strictly between 10125 and 65537; p = 1026120862861, proven prime and above 1e12) satisfies 36260^(p-1) == 1 mod p^2 in exact integer arithmetic, and neither p nor a row for base 36260 appears in the Fischer files or the OEIS search recorded in the-record-we-beat/RECORD.md, which meets partial win p1 only (not the full win, and not a beyond-searched-limit result, since those tables give no row or limit for base 36260).

In plain terms: 1026120862861 is a Wieferich prime to the base 36260 = 2²·5·7²·37, i.e. 36260^(p−1) ≡ 1 (mod p²).
- The base lies above the range of Richard Fischer's tables (10125 < b < 65537), and p is above 10^12.
- 36260 is the only base in 2..65536 for which this p is a Wieferich prime (panel/novelty.md, section 4). CRITERION
  extends the scan to 2..131072 (panel/criterion.md).

## Check it yourself
From this folder (Python 3.8+, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. It takes well under a second on a laptop. The one-line equivalent is
`python3 -c "p=1026120862861; print(pow(36260, p-1, p*p))"`, which prints `1`.

## Compared to
- Table: Richard Fischer's Fermat-quotient tables at fermatquotient.com:
  - FermQ_Sorg.txt, bases 2..10125, "durchsucht bis 4.8E+12";
  - FermQ_Sort.txt, bases 2..1052 plus 65537.
- Cell: base 36260.
  - Neither file has a row for it, because no base 10126..65536 is tabulated, and the number 1026120862861 occurs in
    neither file.
  - It occurs in none of Fischer's ten Fermat-quotient files, even with digit separators removed (panel/novelty.md,
    section 3).
  - Table value for the cell: none. This package adds one pair.
- URLs, UTC fetch times, HTTP status, selected headers and page sha256 are in the-record-we-beat/RECORD.md.
  - The scout fetched the tables at 2026-11-07T23:19:19Z.
  - The panel re-fetched them at 23:26:16Z-23:26:39Z (NOVELTY) and 23:29:42Z-23:29:44Z (CRITERION).
  - All copies are byte-identical.
- OEIS: searches for 1026120862861 on 2026-11-07 at 23:19:21Z (scout), 23:26:47Z (NOVELTY) and 23:29:46Z (CRITERION)
  returned no match.
- Related claims in this repository: draft PRs #973, #983, #999 and #1008 hold four other pairs of the same cell,
  with other primes. None of them mentions this pair (panel/novelty.md, section 5).

## Not claimed
- Not a full win: the base 36260 is above 10125.
- Not a result beyond a searched limit: Fischer's tables give no row or limit for base 36260 (panel/criterion.md).
- Not the smallest Wieferich prime to base 36260: 3, 11 and 491 are smaller (panel/criterion.md).
- No search certificate: nothing is claimed about the rest of the swept range, other bases or other primes.
- No novelty beyond the sources checked in panel/novelty.md:
  - Fischer's ten Fermat-quotient files and OEIS;
  - this repository's tree, trophy case, known-knowns, releases, pull requests (with the full patches of the four
    Wieferich ones) and issues;
  - GitHub code, issue and repository searches, and web searches, covering the last 24 months.
- Panel note: the three skeptics ran as isolated headless Claude Code sessions (`claude -p --safe-mode`). Each was
  started in its own copy of the claim folder outside the contributor's workspace, so no workspace notes were in its
  context. panel/gate.md records the path audit of each session.

## Credits
- Richard Fischer, Fermat-quotient tables (http://www.fermatquotient.com/), continuing the tables of Wilfrid Keller and
  Jörg Richstein. They are the bar this pair is compared against.
- OEIS Foundation (https://oeis.org/), novelty lookups.
- Primality: trial division, the Lucas (n−1) criterion used by the panel, and the deterministic Miller-Rabin bounds
  of Jiang & Deng (2014) and Sorenson & Webster (2015) used by verify.py.
- GMP via gmpy2 (https://github.com/aleaxit/gmpy) and NumPy (https://numpy.org/), the search tooling in how-we-built-it/.
- The V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S): target definition, run protocol and three-skeptic panel.
- Found in a V3R1T4S run credited to 0xSrk.
