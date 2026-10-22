# Attempt records

A run that ends without a solution still learned something: which lenses were tried, how far they got, how close the
closest miss was. Today that stays in `<WORKDIR>/runs/` on the machine that ran it, so the next run on the same target can
repeat the same dead end, and the repository shows its wins without the attempts behind them. An attempt record is a short,
checkable summary of such a run, published at `attempts/<target-id>/<attempt-id>.md`.

An attempt record is not a claim: it needs no panel, is never listed in `TROPHY_CASE.md`, and its text is contributor text,
unverified. Only its format is checked. Say what the budget was, so a reader can tell "nothing in one hour" from "nothing in a
month".

## Format

A title line, a block of `key: value` lines, then the sections.

```
# Attempt <date>-<credit>-<first 8 hex of prereg_sha256>

target: <bank target id>
date: <UTC date of the run, YYYY-MM-DD>
credit: <credit name, lowercase letters, digits and hyphens, as in submission ids>
run_status: NOTHING | PROMISING | REFUTED | CONFIRMED_PARTIAL | CONFIRMED_SOLUTION
prereg_sha256: <sha256 of the run's PREREG.md>
prereg_url: <where that PREREG.md is public> (optional)
budget: <what was spent: time, machine, processes>
compared_with: <table or source, URL, UTC fetch time>
closest: <closest value reached and its cell, or none>
lenses: <lens folder>=<claim level>, ...   (claim levels of kit/RUN.md: nothing, negative, progress, partial_win_claim, solution_claim)
claims: none | #<pull request>, ...        (claims that came out of the same run)

## What was tried

## Why it fell short

## Reproduce (optional)
```

`run_status` is the run's final status from `kit/RUN.md`. A run that confirmed a partial win but found nothing for the main
target (for example an audit plus a failed search) has `run_status: CONFIRMED_PARTIAL` and lists its search lenses as
`negative`.

**Commit-only targets** (`disclosure: commit-only` in `bank/targets.json`; see `DONT_SPOIL_THE_HUNT.md`): the record is the
title and the header only, with `target`, `date`, `credit`, `run_status` and `commitment: <sha256 of a private salt and your
private notes>` in place of `prereg_sha256`; no method text, no closest miss, no sections. The checker refuses anything else.

## Check and publish

```sh
python3 <WORKDIR>/repo/kit/check_attempt.py attempts/<target-id>/<attempt-id>.md
```

The last line must be `CHECK_ATTEMPT: PASS`. It checks the fields, the target id against `bank/targets.json`, that the id,
title, file name and folder agree, the run status and claim levels, the commit-only rule, the size (at most 32 KB) and leaks
(absolute paths, e-mail addresses, token-like strings). Then publish as in `kit/SUBMIT.md` section 6.
