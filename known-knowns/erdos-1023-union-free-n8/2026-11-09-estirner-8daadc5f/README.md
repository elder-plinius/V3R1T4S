# Erdős problem #1023 (OEIS A347025): a union-free family of 80 subsets of {1..8}, so a(8) >= 80

## What

object/union_free_n8_80.txt lists exactly 80 distinct nonempty subsets of {1..8} (2 of size 2, 15 of size 3, 63 of size 4) in which no member equals the union of any nonempty subcollection of the other members (the OEIS A347025 property, equivalently no member equals the union of all other members it contains), confirmed by the contributor's script and by an independent brute force, so its size exceeds by one the bar a(8) >= 79 (Jon E. Schoenfield, Apr 2022), the only n = 8 value in the live OEIS A347025 entry body and comments as fetched 2026-11-09T13:28:00Z.

Status (panel/gate.md): CONFIRMED_SOLUTION (three-skeptic panel, 3/3 pass). In plain words: a(n) is the largest
number of nonempty subsets of {1..n} such that no member is the union of other members. The best known value at
n = 8 was 79 (Schoenfield, 2022). The 80 sets in object/union_free_n8_80.txt (2 pairs, 15 triples and 63 four-element
sets) have the property, so a(8) >= 80. The upper bound from Loo's recursion with a(7) = 44 is 89.

## Check it yourself

    sh verify-it-yourself/run_checks.sh          # Python 3 standard library; a few seconds; last line: PASS

It checks the file's sha256, calibrates on a(1..4) by exhaustive search, rejects malformed lines, and tests the union
condition for every member by two methods. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| OEIS A347025, revision 111 (2026-09-27) | a(8), lower bound in the comments (Schoenfield, Apr 2022) | 79 | https://oeis.org/A347025 | 2026-11-09T13:04:56Z (sha256 71e3c73b...0121480); again 13:27:28Z (panel/novelty.md) |
| M. Živković, Linear Algebra Appl. 436 (2012) 845-849, as quoted in Math.SE answer 3241237 (P. Taylor, 2019) | a(8), from his lower-bound formula 2^(ceil(n/2)-3) - 2 + sum_{k=0}^{n-1} C(k, ceil(k/2)) | 78 | https://doi.org/10.1016/j.laa.2011.03.061, https://math.stackexchange.com/questions/3241237 | Math.SE answer 2026-11-10T14:21:24Z (Stack Exchange API); the paper's abstract (via zbMATH) 2026-11-10; full text not read (the publisher refused a scripted request) |

## Not claimed

- Not the exact value of a(8): only a(8) >= 80. No search here found 81.
- Not the asymptotics asked by Erdős problem #1023 (they follow from Kleitman's work on #447).
- Nothing at n = 9 or n = 10. Živković's 2012 formula, as quoted, already gives 150 and 276 there, above the
  values in the OEIS entry (144, 270); this family lifted by the standard step gives the same 150 and 276.
- Not peer reviewed; checked by a three-skeptic panel (panel/) and by the standalone checker shipped here. This is a
  certified computational result (an explicit family checked exhaustively), not a proof of anything else.

## Credits

- The sequence and its bounds: OEIS A347025 (https://oeis.org/A347025): Michael S. Branicky (terms and program), Jon E.
  Schoenfield (the constructions giving 79, 144, 270), Jinyuan Wang (a(6), a(7) <= 45), William Blair (a(7) = 44),
  Jakob Süskind (the lattice reformulation).
- Andy Loo, Union-Free Families of Subsets, arXiv:1511.00170 (2015), for the recursive bounds.
- Miodrag Živković, Extremal families containing no two sets and their union, Linear Algebra Appl. 436 (2012)
  845-849 (https://doi.org/10.1016/j.laa.2011.03.061), for the best published lower-bound formula for general n;
  Peter Taylor's Math.SE answer 3241237 for quoting it. Not cited by the OEIS entry; found in a prior-art recheck
  on 2026-11-10.
- Erdős problem #1023, https://www.erdosproblems.com/1023 (Thomas Bloom's database).
- The second search (code/scan_unionfree_probe.py) comes from the 2026-11-09 V3R1T4S bank scan's deep check.
