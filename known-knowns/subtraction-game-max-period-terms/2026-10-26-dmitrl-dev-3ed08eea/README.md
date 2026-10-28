# A389690(23) = 3570: the longest Sprague-Grundy period of a subtraction game with largest move 23

## What

Under the OEIS A389690 definition (S ranging over all 2^22 subsets of {1, ..., 23} that contain 23; period = minimal eventual period of the Sprague-Grundy sequence, i.e. the first repeat of the length-23 window counted once 23 values exist), the maximum period at n = 23 is 3570, attained by exactly one set, S = {2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23}, as shown by the claimant's two independently written exhaustive searches (A in C, B in Rust, both rerun by the CRITERION skeptic) and by that skeptic's own third search, all three agreeing on the maximum and on the full 673-period histogram over 4194304 sets, with that set's period recomputed as 3570 by the entry's own Python function (https://oeis.org/A389690/a389690_2.txt) and by a direct tail-periodicity check, and with no a(23) in the OEIS entry, its b-file or any of its 36 history revisions as fetched 2026-10-26T07:39:16Z to 07:40:19Z.

The object is object/A389690_23.txt (sha256 3ed08eead6e5ea1301ec09aaa499b0baeac472b4c423dcf0f56ea398ef220ee4): the value, the maximising set and the full histogram of periods
over all 4194304 sets.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. A few minutes on a laptop with 4 processes, Python 3 standard library only (an exhaustive pass
over all 2^22 sets). `python3 verify-it-yourself/check_term.py object/A389690_23.txt --quick` checks the object and the
maximising set in under a second. Details: RUN_IT_YOURSELF.md; real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| what | value | source | fetched (UTC) |
|---|---|---|---|
| OEIS A389690 | n = 1..22 listed (a(22) = 4464); no a(23) in the entry, b-file or history | https://oeis.org/A389690 | 2026-10-26T09:59:52Z |
| this object | **A389690(23) = 3570**, unique maximiser {2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23} | object/A389690_23.txt | - |

Snapshot with hashes: the-record-we-beat/RECORD.md.

## Not claimed

- Nothing about later terms. The same programs gave A389690(24) = 3680 and A389690(25) = 4104; those were not reviewed by a
  panel and are not part of this package.
- Nothing about A389689. For that sequence the 1997 dissertation of A. Flammenkamp (Bielefeld; record list of all move sets
  with max L < 30, printed pp. 40-41) already gives the maxima for n = 24 and n = 26..30. It is cited here because readers of
  this family will want it; it contains no table of Sprague-Grundy period maxima (panel/novelty.md).
- No claim about literature we could not read: J. Bueltermann's 1993 Diplomarbeit "Periodenlaengen in Nim-Spielen"
  (Bielefeld) is not online, and Althoefer-Bueltermann (TCS 148, 1995) was read by abstract only.
- The two programs share an author: they are independent implementations (different code, language, data layout and cycle
  detection), not independent authors. Each panel skeptic wrote and ran its own exhaustive search as well.

## Credits

- Rui Yao, OEIS A389690 and A389689 (October 2025), with the Python programs a389690_2.txt and a389689_1.txt.
- Achim Flammenkamp, Lange Perioden in Subtraktions-Spielen, dissertation, Universitaet Bielefeld 1997
  (https://wwwhomes.uni-bielefeld.de/~achim/diss.ps.gz).
- Ingo Althoefer and Joerg Bueltermann, Superlinear period lengths in some subtraction games, Theoretical Computer
  Science 148 (1995).
- r-nikhil, the V3R1T4S bank proposal for this target (PR #699).
- AI-assisted search and checks for DmitrL-dev; three-skeptic panel in fresh sub-agent contexts.
