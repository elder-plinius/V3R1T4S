# A(26,6,9) >= 5997: an explicit binary constant-weight code

## What

The frozen 5997-word object proves A(26,6,9) >= 5997, equivalently A(26,6,17) >= 5997, exceeding the 5986 lower bound in the 17 October 2026 Brouwer snapshot by 11 without exceeding its 16122 upper bound or being subsumed by the mandatory papers and examined newer sources and contributions.

PROVED-HERE: the object SHA256 is `6be5a215f0b662497e21330c98db83b5128095af52e4a45a8484ba60ff524de8`.
All 17,979,006 unordered pairs were checked exactly. The complement is the same finding, not a second result.

## Check it yourself

From this folder, with standard-library Python 3:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough laptop time: about 10 seconds. Actual origin output is in
`verify-it-yourself/RECEIPTS.md`. The final Mac package check also executes clean and corrupted copies.
For the independently authored checker and seven calibration cases, run with Python 3.10 or newer:

```sh
python3 independent-reproduce/check_exact.py object/A26_6_9_5997.txt --n 26 --w 9 --d 6 --count 5997 --sha256 6be5a215f0b662497e21330c98db83b5128095af52e4a45a8484ba60ff524de8
```

It emits JSON and exits zero on success; its complete mathematical receipt is included.

## Compared to

KNOWN: [A. E. Brouwer's table](https://aeb.win.tue.nl/codes/Andw.html), n=26, d=6, w=9,
read 2026-10-17T14:00:04Z, HTTP200: **5986 [Pl] to 16122**. Independent NOVELTY re-fetched the same page hash.
The table uses the representative weight; w=17 is equivalent by complement. The improvement is **+11 over 5986**,
not over the obsolete 5761 baseline. The existing [V3R1T4S catalogue](https://github.com/elder-plinius/V3R1T4S/tree/7dd4480512cc47fe0f897164844432a2738fe649/known-knowns/bigger-codes)
also lists 5986. Live receipts, selected-cell extraction and comparison scopes are in `the-record-we-beat/`.

The independent panel examined the two binding papers, newer relevant primary texts, upstream contributions,
and the concrete nearby published constructions. Official API responses covered all 309 records of the literal
query and a combined 378-record union after supplementary queries; metadata screening is not full-text reading
of all records. These queries are declared coverage, not a proof of absence of unpublished work.

## Not claimed

No optimality, new search algorithm, exhaustive search, first-ever/global priority, award, external acceptance,
or claim about another cell. This is a finite explicit lower-bound improvement at the recorded comparison snapshot.
No third-party paper, webpage or dataset is redistributed in this package. Prior provisional assessments remain
in the origin record; this package contains a new independent assessment, described in `VERSION.md`.

## Credits

- Contribution: **Jean Francois Gutierrez / DrZuzzjen**, [GitHub](https://github.com/DrZuzzjen).
- Jordan Boisclair: original 5761-word seed, identified as [Bo] in [Brouwer's archive](https://aeb.win.tue.nl/codes/cwc/d6/a26.6.9.5761H).
- A. E. Brouwer: table, archive and reference framework.
- [V3R1T4S and its contributors](https://github.com/elder-plinius/V3R1T4S): existing large-neighbourhood search engine
  and prior published 5986-word construction; the reused engine is unchanged and AGPL-3.0 licensed.
- Compared sources include [William Echols](https://arxiv.org/abs/2608.13906),
  [Christian Lysenstøen](https://arxiv.org/abs/2607.19550), [Christopher D. Rosin](https://arxiv.org/abs/2603.00174),
  [Yang and coauthors](https://arxiv.org/abs/2609.35051), and [Alfonso Gippini Requeijo](https://zenodo.org/records/23075336).
  Freelsgood's [A(27,6,10) contribution](https://github.com/elder-plinius/V3R1T4S/pull/28) was also compared.
  Further sources and exact review boundaries are recorded in the independent panel reports.
