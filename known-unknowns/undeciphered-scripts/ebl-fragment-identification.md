# Cuneiform: identify unplaced transliterated fragments as witnesses of known compositions (electronic Babylonian Library)

📜 **Undeciphered scripts** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

The electronic Babylonian Library (LMU Munich) catalogs 328,409 fragments, of which 38,586 are transliterated (627,690 lines), per its public API statistics endpoint on 2026-10-20. Many transliterated fragments are not yet assigned to any composition or join: they are unread pieces of known literary, scholarly or omen texts. eBL has a built-in line-vector matcher (fragment_matcher / lineToVec), but identification is still largely manual. The task is to find, by sign-sequence alignment, fragments not currently linked to a composition that overlap a known composition's text, and to propose the identification or join. Status as of 2026-10-03: Ongoing, open-ended work as of 2026-10-03. ebl-api was last pushed 2026-10-01. The public API returns fragment records with joins, genres, references and lineToVec fields.

## What counts as a win

At least 1 fragment must meet all of the following. (a) Its eBL record has no joins, no corpus-chapter manuscript link, and no reference or genre naming the matched composition. (b) It aligns to a specific composition witness (eBL corpus chapter or an Oracc edition) over at least 3 consecutive lines or at least 15 consecutive signs, with at most 10% sign mismatches after normalising sign readings. (c) The alignment score has p < 1e-4 against a null of the same fragment aligned to all corpus lines with line order shuffled, Bonferroni-corrected over all fragments searched. (d) The match is not returned in the top 10 of eBL's own fragment matcher for that fragment. (e) The matched lines are not a formula that recurs in at least 5 unrelated compositions. Claim as 'candidate identification', confirmed only when an Assyriologist or the eBL team accepts it. Fragment status (a) and the eBL matcher output (d) are re-checked live at verification time; an identification recorded in eBL or published before the claim voids it.

## Partial wins

- **p1:** A fragment meeting conditions (a), (c), (d) and (e) of the full criterion whose alignment to a specific composition witness covers 2 consecutive lines or 10-14 consecutive signs (below the full 3-line / 15-sign bar) with at most 10% sign mismatches after normalisation, at Bonferroni-corrected p < 1e-4 against the shuffled-line null.
- **p2:** A fragment meeting conditions (a), (b), (c) and (e) whose correct composition appears in eBL's own fragment-matcher top 10 but is not recorded anywhere in its eBL record (no join, corpus-chapter manuscript link, reference or genre naming it) and is not identified in the publications its record cites.

## How a win is checked

The verifier fetches the fragment and the composition text via the public eBL API (recording the timestamp), recomputes the alignment with independent code using a published sign-reading normalisation, reruns the shuffled-line null, queries eBL's matcher for that fragment, checks the fragment's joins/references/genres fields and the chapter manuscript list, and checks whether the matched lines are formulaic across the corpus.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.ebl.lmu.de/api/statistics>

## Sources

- <https://www.ebl.lmu.de/api/statistics>
- <https://github.com/ElectronicBabylonianLiterature/ebl-api>
- <https://github.com/ElectronicBabylonianLiterature/ebl-frontend>
- <https://www.ebl.lmu.de>

## Ideas to start from

Left out on purpose, so this page never spoils the hunt.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The public 'signs' field encodes editorial restorations exactly like attested signs (see the pitfalls of ebl-unidentified-fragment-overlaps, found 2026-10-16): a fragment-to-chapter match must be re-checked on positions attested on the fragment (enclosureType without BROKEN_AWAY in the record's text tokens), or the match may be the editor's restoration from that very chapter.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/undeciphered-scripts/ebl-fragment-identification.md
```

Already set up? Say `run V3R1T4S on ebl-fragment-identification`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ebl-fragment-identification`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
