# [claim] snake-coil-in-the-box: Q13 snake of length 2946 equals the live record, new equivalence class (partial win p3)

## What

A valid induced snake of length 2946 in Q13, equal to the live record length 2946 for this dimension and type and inequivalent (canonical relabelled transition sequence, with reversal) to every same-length record sequence in the Caltech files and the minortriad page that I read; this is an enumerated partial win p3 only, not a strict record.

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
| minortriad.com snake table | Q13 snake | 2946 (page change log entry of 11-oct-2026) | https://www.minortriad.com/snake/ | 2026-10-19T04:32:30Z (HTTP 200); again 05:26:55Z and 08:25:29Z |
| Math-AI-Caltech Snake-in-the-Box README | Q13 snake | its own record 2924; 'subsequent bounds by others' line gives 2934 for Q13 | https://raw.githubusercontent.com/Math-AI-Caltech/Snake-in-the-Box/main/README.md | 2026-10-19T04:43:29Z (HTTP 200); again 05:26:56Z and 08:25:30Z |
| Caltech data file record_snakes.csv.zip | Q13 snakes | longest 2924; no file at 2946 (compared by the novelty skeptic) | https://github.com/Math-AI-Caltech/Snake-in-the-Box | 2026-10-19T05:34:07Z (HTTP 200) |
| EinsteinArena 13D snake page | Q13 snake | baseline 2,934, a reported 2,938-edge snake (both below 2946) | https://einsteinarena.com/ | 2026-10-19T05:40:57Z (HTTP 200) |

The table value used in `INDEX.csv` is 2946, from the first fetch (2026-10-19T04:32:30Z). Snapshot metadata with HTTP status and page checksum: `the-record-we-beat/README.md`; a later re-check of the pages used for the credits: `the-record-we-beat/SOURCE_RECHECK.md`. The panel's novelty report is `panel/novelty.md`.

## Not claimed

- This is the enumerated partial win p3 only: an equal-record witness. The length equals the live table value (2946); it is not a strict record and no longer snake or coil is claimed.
- Inequivalence is established against what the panel could read: the one minortriad page sample of this dimension and type, and the Caltech record files (the Caltech snake and coil files hold shorter classes for this dimension, so there was no Caltech file at this exact length to compare with). The Caltech Snakepits folder, EinsteinArena and Zenodo were not read.
- The claim folder's saved canonical class hashes cover only the page sample and the author's own earlier closed-PR object; the Caltech files were compared by the novelty skeptic, not by the package's checker. The checker's inequivalence line therefore reproduces only against the saved list.
- The object is described by its author as a 'drifted' copy of an earlier witness (a neutral random walk from it). It counts as a new class only under the canonical comparison that p3 prescribes (coordinate relabelling by first appearance, translation, reversal); whether such a neighbour is mathematically interesting is not claimed.
- The minortriad table is updated from personal emails, so a longer value or another class could exist before it is posted. Google Scholar and private communication were not searched.
- The panel's three skeptics are Claude Code subagents of one model family; the object's builder (Gemini, Argon) is a different family. The skeptics were given only the claim folder. This is not peer review.
- The panel checked the object file as shipped (sha256 ad7e599b39b1cb71bd665cc2458ef169ae4da434fdd1e97cfe684053125cac21).

Gate notes, as written by the gate (`panel/gate.md`), in plain words:

- Object: object/p3_sn13_drifted_r0_Q13_2946.txt, sha256 ad7e599b39b1cb71bd665cc2458ef169ae4da434fdd1e97cfe684053125cac21.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Refile of the contributor's PR #89, closed unmerged on 2026-10-14 in the bulk close of about thirty early PRs during a handoff, not for a defect.
- Partial win p3: an equal-record witness inequivalent to the published records the panel could read (minortriad sample, Caltech record files); the Caltech Snakepits folder, EinsteinArena and Zenodo were not read.

## Filing history

The contributor filed the same cell and the same length earlier as V3R1T4S pull request #89. That pull request was closed unmerged on 2026-10-14 in the bulk close of about thirty early pull requests during a handoff between sessions, not for a defect. This package is a refile of the cell; its object is a different object (a different canonical class by the triage agent's hash) from the closed pull request's object.

## Credits

- **William Toner**: the minortriad page's change log of 11 October 2026 credits him with the Q13 snake of length 2946; the table value this claim ties.
- The **minortriad.com snake table** (https://www.minortriad.com/snake/): the live table compared against and the definition of its symmetric-coil test, quoted in `the-record-we-beat/`. The fetched page names contributors of individual records in its change log and reference list but names no maintainer, so none is named here.
- **Paul Orland, Lucas Fagan, Michele Tarquini, Davide Passaro, Maksymilian Manko, Elli Heyes, Angus Gruen, Giorgi Butbaia, Justin Tan and Sergei Gukov**, *New Snake-in-the-Box Records via Snakepit Surgery and Learned Construction*, arXiv:2607.15270 (2026; earlier versions were titled *A Census of New Snake-in-the-Box Records*), https://arxiv.org/abs/2607.15270, and their dataset repository Math-AI-Caltech/Snake-in-the-Box, https://github.com/Math-AI-Caltech/Snake-in-the-Box: the published record tables and record files compared against (author list and title as given in the repository README's citation block).
- **EinsteinArena** (https://einsteinarena.com/): its 13-dimensional snake problem page, compared against for Q13 snakes.
- The search code and pre-registration: the contributor's AI search agent (Gemini, Argon), under the contributor credit `calgulbenkian`. The checker in `verify-it-yourself/` was written by the orchestrator's triage agent from the definitions.
