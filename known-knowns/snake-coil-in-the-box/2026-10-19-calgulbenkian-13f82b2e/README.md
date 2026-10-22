# snake-coil-in-the-box: Q11 snake of length 750, equal to the record, new class (partial win p3)

## What

A valid induced snake of length 750 in Q11, equal to the live record length 750 for this dimension and type and inequivalent (canonical relabelled transition sequence, with reversal) to every same-length record sequence in the Caltech files and the minortriad page that I read; this is an enumerated partial win p3 only, not a strict record.

The object is `object/p3_sn11_drifted_r0_Q11_750.txt` (sha256 13f82b2e8ef05882c7d78fe1511df710fa3754f9debec76c2ac83aa3ecd60c54). The sentence above is quoted word for word from `panel/gate.md`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 2 seconds (measured on the packager's laptop).
- **Expected last line**: `ALL CHECKS PASS`

The script first checks every file in `object/` against `SHA256SUMS`, then runs the standalone checker and a negative control.

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| minortriad snake table | Q11 snake | 750 | **750** (equal) | https://www.minortriad.com/snake/ | 2026-10-19T05:26:55Z |
| Math-AI-Caltech Snake-in-the-Box README | Q11 snake | snake bound by others: 750 | **750** (equal) | https://github.com/Math-AI-Caltech/Snake-in-the-Box | 2026-10-19T05:26:56Z |
| Math-AI-Caltech Snake-in-the-Box record files (record_coils.csv, record_snakes.csv.zip), same dimension and type | Q11 snake | no Caltech snake file of length 750 (its longest Q11 snake is 746) | **750**, in a class not among them | https://github.com/Math-AI-Caltech/Snake-in-the-Box | 2026-10-19T05:34:08Z |
| arXiv:2607.15270 v3 (snake-in-the-box literature; no value beyond the table for this cell) | Q11 snake | none | **750** | https://arxiv.org/html/2607.15270v3 | 2026-10-19T05:35:53Z |
| Contributor's own closed pull request 87 (same cell and length), closed unmerged 2026-10-14 | Q11 snake | n/a (own earlier filing) | **750** | https://github.com/elder-plinius/V3R1T4S/pull/87 | 2026-10-19T04:30:31Z |
| V3R1T4S known-knowns listing (no snake-coil-in-the-box directory, no merged package) | Q11 snake | none | **750** | https://github.com/elder-plinius/V3R1T4S | 2026-10-19T05:27:03Z |

The panel's novelty skeptic fetched every source itself (its report is `panel/novelty.md`); the triage fetch and its page sha256 values are in `the-record-we-beat/`.

## Not claimed

- This is an enumerated partial win p3 only: a valid induced path (snake) of length 750 in Q11 that EQUALS the live record length for this dimension and type and lies in a different equivalence class from the published record sequences the panel could read. It is not a strict record; no longer snake is claimed.
- Inequivalence is stated only against what the panel read: the Math-AI-Caltech record files of this dimension and type and the sample sequence on the minortriad page. The Caltech Snakepits folder, EinsteinArena and Zenodo were not read. Equivalence is canonical relabelling of the transition sequence, with reversal.
- The minortriad table is updated from personal emails, so a longer value could exist before it is posted. Google Scholar and private communication were not searched.
- The object is a 'drifted' copy of an earlier witness (a neutral random walk from it). The panel judged that p3 defines inequivalence by the canonical comparison, which the object passes; whether a neutral-walk neighbour is interesting is not part of that text.
- Not peer reviewed. It was checked by a three-skeptic panel (panel/) and by the standalone checker shipped here, which tests the induced property by two independent methods.

## Filing history

This is a refile of the contributor's pull request 87 (same cell and length; the object here is a different canonical class from the one filed then), closed unmerged on 2026-10-14 in the bulk close of about thirty early PRs during a handoff, not for a defect.

## Credits

- **The minortriad snake table** (https://www.minortriad.com/snake/): the live record lengths and the sample sequences. The claim folder does not name the page's maintainer or sample contributors, so no person is credited here.
- **Math-AI-Caltech/Snake-in-the-Box** (https://github.com/Math-AI-Caltech/Snake-in-the-Box): the record files and README the comparison uses.
- **arXiv:2607.15270** (https://arxiv.org/abs/2607.15270): the snake-in-the-box paper the bank entry names.
- The Caltech README attributes the equal bound 750 in Q11 to **Echols**; this package only equals that length.
- Contributor credit: `calgulbenkian`. The search was run by Gemini (Argon) for the contributor.
