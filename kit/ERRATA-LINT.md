# Errata lint and check_run errata mode

A data-integrity erratum (a table value or file that its own source data does not support) is filed lean. It is
**not** a record claim and does **not** go through the three-skeptic panel or the `CONFIRMED_*` gate. Every first
push of an errata PR so far still leaked internal scaffolding: `panel/PENDING.md` (#311), `panel/`,
`panel-evidence/` and `panel-scripts/` plus a gate file saying "PROMISING" (#312), `PLACEMENT.md` (#333), copied
table data (#206/#207), and "Panel status" text (#240). The lint blocks those mechanically, before the push.

## One command

```sh
python3 kit/errata_lint.py <package-dir>                  # one package folder
python3 kit/errata_lint.py <tree>                         # a tree holding known-knowns/<family>/<id>/
python3 kit/errata_lint.py --repo <clone> --git upstream/main   # what this branch adds vs its base (BASE...HEAD)
python3 kit/errata_lint.py --repo <clone> --git A..B      # an explicit range
```

The last line is `ERRATA_LINT: PASS (...)` or `ERRATA_LINT: FAIL (<n> problems in <m> files)`, with one
`FAIL: <file>: <reason>` line per problem above it. Exit status 0 (pass), 1 (fail), 2 (usage or git error).

In `--git` mode every package the range touches is linted **in full at the head commit** (so a one-file fix commit
cannot slip past an old leak), and any changed path outside `known-knowns/<family>/<id>/` fails: an erratum PR
changes nothing else (`kit/SUBMIT.md` section 3.4). More than one package in one change set fails too. A package
whose `panel/gate.md` says `status: CONFIRMED_*` and whose title is not an erratum is a record package. The lint
prints `SKIP` for it and leaves it to `check_run.py --package`.

## What is allowed

The allowlist is the config block at the top of `kit/errata_lint.py`. It holds what the lean errata PRs actually
ship (#311 and #333; the maintainer called #311's shape "exactly what we asked for") and what `kit/SUBMIT.md`
section 1 names:

| where | allowed |
|---|---|
| package root | `README.md`, `PR_BODY.md`, `SOURCES.csv`, `NOT_CLAIMED.md`, `SHA256SUMS`, `RUN_IT_YOURSELF.md`, `HOW_WE_FOUND_IT.md`, `INDEX.csv` |
| `verify-it-yourself/` | the one-command repro: `run_checks.sh`, the repro script, `CLAIM.json`, `RECEIPTS.md` (`.py .sh .md .txt .csv .tsv .json`) |
| `how-we-built-it/` | the code that found it, its dated output, `PREREG.md` (same extensions) |
| `object/` | the erratum cells or file lists we derived (`.csv .tsv .json .txt .md`) |
| `the-record-we-beat/` | snapshot: URL, fetch time, HTTP status, sha256 only (`.md .txt .csv .json`) |
| `fixtures/` (also `verify-it-yourself/fixtures/`, `how-we-built-it/fixtures/`) | minimal fixtures, at most 256 kB each |

Anything else fails with `not on the errata allowlist`. To allow a new kind of file, change the config block in a
reviewed commit; never edit around the lint.

## What is blocked, and why

| class | rule | example reason line |
|---|---|---|
| internal files | any path component matching `panel*`, `PENDING*`, `PLACEMENT*`, `gate.md`, `CHECK_RUN_OUTPUT*`, `OPEN-FACTS*`, `_archive`, `.DS_Store` (case-insensitive) | `panel/novelty.md: blocked: internal panel folder/file ...` |
| internal jargon | case-sensitive, whole words, in every text file (code too): see the list below | `README.md: internal jargon 'Panel status' text ('Panel status', line 12)` |
| references to internal files | `panel*/`, `PENDING.md`, `PLACEMENT.md`, `gate.md` mentioned in a kept file (a dangling pointer after a slim) | `README.md: references internal file 'panel/' (line 14)` |
| copied upstream data | any data file (`.txt .csv .tsv .json .dat .xyz`) over 64 kB outside `fixtures/`; 50 or more whitespace-separated number rows (`x y z`, `i x y z`, `N r`) making up at least half of a file outside `fixtures/`; any HTML page (`<!doctype html`, `<html>`, `<body>`) | `how-we-built-it/ssp1055.txt: 120 coordinate-style number rows (copied upstream data?) ...` |
| size | any file over 1 MB, package over 50 MB (`kit/SUBMIT.md` section 1); binary files | `larger than 1 MB` |
| leaks | the `check_run.py` patterns: home and `/tmp` paths, tokens, keys, email addresses (except no-reply/example) | `temporary-folder path (line 1)` |
| stale checksums | `SHA256SUMS` lists a file that is not there, misses a file, or has a wrong hash | `SHA256SUMS: lists panel/novelty.md, which is not in the package` |

### The jargon list

Matched case-sensitively as whole words, so ordinary prose ("a promising lead", "pending review", "confirmed by the
maintainer", "THRESHOLD", "Moe's table", "panel data", "the record held for ten years") does not trip it:

- `Panel status` / `panel status`
- `CONFIRMED`, `CONFIRMED_PARTIAL`, `CONFIRMED_SOLUTION`, except when directly negated (`not`, `no`, `never`,
  `nor`, `without` up to two words before it, on the same line). "Not a CONFIRMED_PARTIAL p3 win" is the
  maintainer's own requested wording (#206, #311) and passes.
- `PROMISING`, `NEED-HUMAN`, `PENDING` (also `PENDING STATUS CHECK` / `PENDING TABLE CHECK`), `ERRATUM-READY`, `HOLD`
- `expected FAIL` / `Expected FAIL`
- `moe` (lower case only; covers "held ... for moe")
- panel seat lines: `pass: true` / `pass: false` on their own line, `verdict: PASS|FAIL|TIE|NEED-HUMAN` at a line start
- `injection_suspected`
- fleet seat names: RªⁿÞ¡, RanPi, botmin, Botministrator, Bot-Admin, SuperProtoBot, SPB, el-Gringo, TiHQ,
  Hephaestus, Prototyper, Errand Boy, Ops Desk, BotOps

The public credit name (`MrxMoex@Grok_Fleet`, `...-grok-fleet-...` folder names) is not jargon. The words
"skeptic" and "seat" are not blocked; reword them by hand if they read as internal process.

## The pre-push gate

`kit/hooks/pre-push` runs the lint on every ref you push that touches a `known-knowns/` package, and blocks the
push on FAIL. Other pushes pass through (`ERRATA_LINT: SKIP`). For a new remote branch the base is the merge base
with `$ERRATA_LINT_BASE`, `upstream/main`, `origin/main` or `main` (the first that exists).

Install it only in the clone you file errata from (never globally, never through `core.hooksPath`):

```sh
ln -sf <kit-checkout>/kit/hooks/pre-push <filing-clone>/.git/hooks/pre-push
```

To uninstall: `rm <filing-clone>/.git/hooks/pre-push`. The hook finds `errata_lint.py` next to its own real path
(set `ERRATA_LINT=<path>` to override). If it can't find the lint, it blocks the push. `git push --no-verify` skips
it, so never use that on an errata push.

## check_run errata mode

```sh
python3 kit/check_run.py --package <dir> --errata [--workdir <WORKDIR>] [--no-exec]
```

`--package` switches to errata mode on its own when the package's `README.md` / `PR_BODY.md` title (or the
`verify-it-yourself/CLAIM.json` label) says erratum/errata and no `panel/gate.md` says `CONFIRMED_*`. `--record`
forces record mode. Record mode is unchanged.

In errata mode the record panel, gate, `confirmed_scope`, `INDEX.csv`, `the-record-we-beat/` and
corrupted-object checks are skipped (errata are not panel-gated). It runs:

1. `kit/errata_lint.py` on the package (every problem becomes a FAIL);
2. the lean body: `README.md` has a `Claim`, a `One-command repro` (or `Repro` / `Check it yourself`), a
   `Not claimed` (or `NOT_CLAIMED.md`) and a `Confidence` heading or bold table row;
3. `SHA256SUMS` and `verify-it-yourself/run_checks.sh` are present;
4. `SOURCES.csv` or `the-record-we-beat/` carries source URLs, sha256 and dates;
5. `HOW_WE_FOUND_IT.md`, if present, is marked "contributor text, unverified" (a WARN if it says only "contributor text");
6. the never-publish list, the workspace path, placeholders and your login name (the usual leak scan);
7. unless `--no-exec`, `run_checks.sh` from a clean copy: last line `PASS` is ok, `REPLACED UPSTREAM` is a WARN
   (a dated observation: the original files are no longer served), anything else is a FAIL.

It prints `CHECK_RUN: PASS` or `CHECK_RUN: FAIL (<n> problems)` like every other mode, with no "expected FAIL". Don't
paste check_run output into an upstream PR. Upstream comments only answer the maintainer.

## Tests

```sh
python3 kit/tests/test_errata_lint.py    # lint, git mode, the hook, check_run errata mode
python3 kit/tests/test_check_run.py      # record mode, unchanged
```
