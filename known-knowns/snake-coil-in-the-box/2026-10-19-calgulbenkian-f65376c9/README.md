# [claim] snake-coil-in-the-box: Q12 symmetric coil of length 1454 beats the live 1434 (partial win p1)

## What

A coil of length 1454 in Q12, valid and induced, whose first half of transitions equals its second half (the minortriad page's own symmetry test), which strictly exceeds the live minortriad symmetric-coil value 1434 for Q12; it is a partial win p1 only and is not claimed to exceed any ordinary coil or snake record.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: a few seconds.
- **Expected last line**: `ALL CHECKS PASS`. The script first verifies the object file against `SHA256SUMS`, then runs the checker, then a negative control that must be rejected.

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| minortriad.com snake table | Q12 symmetric coil | 1434 | https://www.minortriad.com/snake/ | 2026-10-19T04:32:30Z (HTTP 200); again 05:26:55Z and 08:25:29Z |
| Math-AI-Caltech Snake-in-the-Box README and record_symmetric_coils.csv | Q12 symmetric coil | none listed (symmetric coils only for Q10: 370 and Q11: 734) | https://raw.githubusercontent.com/Math-AI-Caltech/Snake-in-the-Box/main/README.md | 2026-10-19T04:43:29Z (HTTP 200); csv 05:34:07Z |
| arXiv:2607.15270 v3 | Q12 symmetric coil | none (symmetric coils only for n = 10, 11) | https://arxiv.org/abs/2607.15270 | 2026-10-19T05:32:40Z (HTTP 200) |

The table value used in `INDEX.csv` is 1434, from the first fetch (2026-10-19T04:32:30Z). Snapshot metadata with HTTP status and page checksum: `the-record-we-beat/README.md`; a later re-check of the pages used for the credits: `the-record-we-beat/SOURCE_RECHECK.md`. The panel's novelty report is `panel/novelty.md`.

## Not claimed

- This is the enumerated partial win p1 only: a symmetric coil whose first half of transitions equals its second half, under the minortriad page's own symmetry test. It exceeds the live symmetric-coil value (1434) but is not claimed to exceed any ordinary coil or snake record (the ordinary coil record for this dimension is larger).
- Symmetric here means the page's test and nothing else; no claim is made under any other definition of a symmetric coil.
- No published symmetric coil of this dimension longer than the page value was found in the sources read (the minortriad table, the Caltech README and csv files, arXiv:2607.15270 v3, EinsteinArena, Wikipedia). The minortriad table is updated from personal emails, so a longer value could exist before it is posted. Google Scholar and private communication were not searched.
- The panel's three skeptics are Claude Code subagents of one model family; the object's builder (Gemini, Argon) is a different family. The skeptics were given only the claim folder. This is not peer review.
- The panel checked the object file as shipped (sha256 f65376c952a341360326ffffc366447cce2b4ee96be4e6335d62fa0ceadf9cb2).

Gate notes, as written by the gate (`panel/gate.md`), in plain words:

- Object: object/best_sym12_Q12_1454.txt, sha256 f65376c952a341360326ffffc366447cce2b4ee96be4e6335d62fa0ceadf9cb2.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.

## Credits

- **William Echols** (written 'W. Echols' in the change log): the page's change log of 29 August 2026 credits him with the symmetric coils of length 1434 (Q12) and 2830 (Q13); the table value this claim exceeds.
- The **minortriad.com snake table** (https://www.minortriad.com/snake/): the live table compared against and the definition of its symmetric-coil test, quoted in `the-record-we-beat/`. The fetched page names contributors of individual records in its change log and reference list but names no maintainer, so none is named here.
- **Paul Orland, Lucas Fagan, Michele Tarquini, Davide Passaro, Maksymilian Manko, Elli Heyes, Angus Gruen, Giorgi Butbaia, Justin Tan and Sergei Gukov**, *New Snake-in-the-Box Records via Snakepit Surgery and Learned Construction*, arXiv:2607.15270 (2026; earlier versions were titled *A Census of New Snake-in-the-Box Records*), https://arxiv.org/abs/2607.15270, and their dataset repository Math-AI-Caltech/Snake-in-the-Box, https://github.com/Math-AI-Caltech/Snake-in-the-Box: the published record tables and record files compared against (author list and title as given in the repository README's citation block).
- **EinsteinArena** (https://einsteinarena.com/): its 13-dimensional snake problem page, compared against for Q13 snakes.
- The search code and pre-registration: the contributor's AI search agent (Gemini, Argon), under the contributor credit `calgulbenkian`. The checker in `verify-it-yourself/` was written by the orchestrator's triage agent from the definitions.
