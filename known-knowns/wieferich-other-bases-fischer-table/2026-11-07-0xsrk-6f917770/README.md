# Wieferich pair (28860, 1017279755641): wieferich-other-bases-fischer-table, partial win p1

## What
> The single pair in object/pair.json, b = 28860 = 2^2*3*5*13*37 (not a perfect power, an integer from 10126 to 65536) with p = 1017279755641 (above 1e12, proven prime by exhaustive trial division up to isqrt(p)), satisfies b^(p-1) == 1 mod p^2 in exact integer arithmetic and is absent from both Fischer tables identified by URL and sha256 in the-record-we-beat/RECORD.md (neither FermQ_Sorg.txt nor FermQ_Sort.txt has a row for base 28860 or contains p) and from OEIS (a search for p on 2026-11-07 matched no sequence), so it is one new pair meeting partial win p1 of wieferich-other-bases-fischer-table, and not the full win, which requires b at most 10125.

In plain terms: 1017279755641 is a Wieferich prime to the base 28860 = 2²·3·5·13·37, i.e. 28860^(p−1) ≡ 1 (mod p²).
The base lies above the range of Richard Fischer's tables (10125 < b < 65537), and p is above 10^12. 28860 is the
only base in 2..65536 for which this p is a Wieferich prime (panel/novelty.md, section 3; panel/criterion.md, C9).

## Check it yourself
From this folder (Python 3.8+, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. It takes well under a second on a laptop. The one-line equivalent is
`python3 -c "p=1017279755641; print(pow(28860, p-1, p*p))"`, which prints `1`.

## Compared to
- Table: Richard Fischer's Fermat-quotient tables at fermatquotient.com:
  - FermQ_Sorg.txt, bases 2..10125, "durchsucht bis 4.8E+12";
  - FermQ_Sort.txt, bases 2..1052 plus 65537.
- Cell: base 28860. Neither file has a row for it, because no base 10126..65536 is tabulated, and the number
  1017279755641 occurs in neither file. It occurs in none of Fischer's ten Fermat-quotient files either, even with
  digit separators removed (panel/novelty.md, section 2). Table value for the cell: none. This package adds one pair.
- URLs, UTC fetch times, HTTP status, selected headers and page sha256 are in the-record-we-beat/RECORD.md.
  - The scout fetched the tables at 2026-11-07T20:11:24Z.
  - The panel re-fetched them at 21:08:48Z-21:08:54Z (NOVELTY) and 21:15:55Z-21:16:01Z (CRITERION).
  - All copies are byte-identical.
- OEIS: searches for 1017279755641 on 2026-11-07 at 20:11:27Z (scout), 21:10:36Z (NOVELTY) and 21:15:43Z
  (CRITERION) returned no match.
- Related claims in this repository: draft PRs #973, #983 and #999 hold three other pairs of the same cell, with
  other primes.
- History: the pair was first mentioned publicly in PR #999's panel/gate.md, by the same contributor, as explicitly
  unclaimed and awaiting its own panel. This package is that panel's result.

## Not claimed
- Not a full win: the base 28860 is above 10125.
- Not the smallest Wieferich prime to base 28860: 7, 17 and 1801 are smaller (panel/novelty.md, section 3).
- No search certificate: nothing is claimed about the rest of the swept range, other bases or other primes.
- No novelty beyond the sources checked in panel/novelty.md:
  - Fischer's ten Fermat-quotient files and OEIS;
  - this repository's tree, trophy case, known-knowns, sealed envelopes, releases and pull requests;
  - GitHub code, issue and repository searches, and web searches, covering the last 24 months.
- Panel note: the three skeptics ran as Claude Code subagents.
  - Their harness preloaded the workspace's hand-off notes, which summarise the find.
  - None of them opened a workspace file outside the claim folder and its own scratch folder. Each verdict rests on
    its own computations and fetches.
  - This is the run's second panel. The first judged a copy of the claim folder assembled 30 to 60 s before the
    run's preregistration was frozen, an order the kit's checker rejects. The claim folder was rebuilt byte for byte
    after the freeze and judged afresh (panel/gate.md).

## Credits
- Richard Fischer, Fermat-quotient tables (http://www.fermatquotient.com/), continuing the tables of Wilfrid Keller and
  Jörg Richstein. They are the bar this pair is compared against.
- OEIS Foundation (https://oeis.org/), novelty lookups.
- Primality: the deterministic Miller-Rabin bounds of Jiang & Deng (2014), Sorenson & Webster (2015) and Jaeschke (1993),
  and the Lucas (n−1) criterion used by the panel.
- GMP via gmpy2 (https://github.com/aleaxit/gmpy) and NumPy (https://numpy.org/), the search tooling in how-we-built-it/.
- The V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S): target definition, run protocol and three-skeptic panel.
- Found in a V3R1T4S run credited to 0xSrk.
