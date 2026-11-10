# Errata lint and check_run errata mode

A data-integrity erratum (a table value or file that its own source data does not support) is filed lean. It is
**not** a record claim and does **not** go through the three-skeptic panel or the `CONFIRMED_*` gate. The lint blocks
disallowed paths, jargon, and leaks before the push.

## One command

```sh
python3 kit/errata_lint.py <package-dir>                  # one package folder
python3 kit/errata_lint.py <tree>                         # a tree holding known-knowns/<family>/<id>/
python3 kit/errata_lint.py --repo <clone> --git upstream/main   # what this branch adds vs its base (BASE...HEAD)
python3 kit/errata_lint.py --repo <clone> --git A..B      # an explicit range
```

Optional: `--workdir <WORKDIR>` loads extra blocked names from `<WORKDIR>/private/never_publish.txt` when that file
exists. Otherwise (or in addition) `kit/private/blocked_names.txt` in the clone, if present, is gitignored and local.

The last line is `ERRATA_LINT: PASS (...)` or `ERRATA_LINT: FAIL (<n> problems in <m> files)`, with one
`FAIL: <file>: <reason>` line per problem above it. Exit status 0 (pass), 1 (fail), 2 (usage or git error).

In `--git` mode every package the range touches is linted **in full at the head commit** (so a one-file fix commit
cannot slip past an old leak), and any changed path outside `known-knowns/<family>/<id>/` fails: an erratum PR
changes nothing else (`kit/SUBMIT.md` section 3.4). More than one package in one change set fails too. A package
whose `panel/gate.md` says `status: CONFIRMED_*` and whose title is not an erratum is a record package. The lint
prints `SKIP` for it and leaves it to `check_run.py --package`.

## What is allowed

The allowlist is the config block at the top of `kit/errata_lint.py`. It holds what the lean errata PRs actually
ship and what `kit/SUBMIT.md` section 1 names:

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

## What is blocked

| class | rule |
|---|---|
| path components | `panel*`, `PENDING*`, `PLACEMENT*`, `gate.md`, `CHECK_RUN_OUTPUT*`, `OPEN-FACTS*`, `_archive`, `.DS_Store` (case-insensitive glob on each component) |
| jargon | case-sensitive whole-word patterns in `JARGON` inside `kit/errata_lint.py` (every text file, including code) |
| local names | whole words or phrases from `private/never_publish.txt` (with `--workdir`) and/or `kit/private/blocked_names.txt` |
| internal references | `panel*/`, `PENDING.md`, `PLACEMENT.md`, `gate.md` mentioned in kept file text |
| copied upstream data | data file over 64 kB outside `fixtures/`; 50+ coordinate-style rows (≥ half the lines) outside `fixtures/`; HTML pages |
| size | file over 1 MB; package over 50 MB; binary content |
| leaks | `check_run.py` path, token, key, and email patterns |
| checksums | stale or missing `SHA256SUMS` entries |

### Jargon patterns (built-in)

Ordinary prose ("a promising lead", "pending review", "confirmed by the maintainer", "THRESHOLD", "panel data",
"the record held for ten years") must not trip these rules:

- `Panel status` / `panel status`
- `CONFIRMED`, `CONFIRMED_PARTIAL`, `CONFIRMED_SOLUTION`, except when directly negated (`not`, `no`, `never`,
  `nor`, `without` up to two words before it, on the same line)
- `PROMISING`, `NEED-HUMAN`, `PENDING`, `ERRATUM-READY`, `HOLD`
- `expected FAIL` / `Expected FAIL`
- `pass: true` / `pass: false` on their own line; `verdict: PASS|FAIL|TIE|NEED-HUMAN` at line start
- `injection_suspected`

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

Pass `--errata` explicitly. README titles, PR body text and contributor wording do not select errata mode.

In errata mode the record panel, gate, `confirmed_scope`, `INDEX.csv`, `the-record-we-beat/` and
corrupted-object checks are skipped (errata are not panel-gated). It runs:

1. `kit/errata_lint.py` on the package (every problem becomes a FAIL);
2. the lean body: `README.md` has a `Claim`, a `One-command repro` (or `Repro` / `Check it yourself`), a
   `Not claimed` (or `NOT_CLAIMED.md`) and a `Confidence` heading or bold table row;
3. `SHA256SUMS` and `verify-it-yourself/run_checks.sh` are present;
4. `SOURCES.csv` or `the-record-we-beat/` carries source URLs, sha256 and dates;
5. `HOW_WE_FOUND_IT.md`, if present, is marked "contributor text, unverified" (a WARN if it says only "contributor text");
6. the usual `check_run.py` leak scan (tokens, paths, emails, never-publish list, workspace path, placeholders);
7. unless `--no-exec`, `run_checks.sh` from a clean copy: last line `PASS` is ok, `REPLACED UPSTREAM` is a WARN
   (a dated observation: the original files are no longer served), anything else is a FAIL.

It prints `CHECK_RUN: PASS` or `CHECK_RUN: FAIL (<n> problems)` like every other mode, with no "expected FAIL". Don't
paste check_run output into an upstream PR. Upstream comments only answer the maintainer.

## Tests

```sh
python3 kit/tests/test_errata_lint.py    # lint, git mode, the hook, check_run errata mode
python3 kit/tests/test_check_run.py      # record mode, unchanged
```
