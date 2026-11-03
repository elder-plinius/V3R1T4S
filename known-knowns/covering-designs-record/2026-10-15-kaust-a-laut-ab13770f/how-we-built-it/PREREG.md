# PREREG: covering-designs-record, run 2026-10-15-2309

frozen: 2026-10-15T23:14:24Z (date -u), before any scored attack output in this run and before claim/ is built.

## Criterion (verbatim from repo/bank/targets.json)
Success means b blocks, each a k-subset of a v-set (no repeated points), covering every t-subset (checked exhaustively), where b is STRICTLY SMALLER (direction: min) than EVERY one of the following, each re-fetched at verification time: the live coveringrepository.com plain (v,k,t) value (m=t section, https://coveringrepository.com/), the live LJCR value (https://dmgordon.org/covering-designs/), and the dmgordo/LJCR GitHub/Zenodo value. It must also beat any value found by grepping GitHub/arXiv for that (v,k,t) over the last 6 months, including unverified hobbyist claims (e.g. thebrockchain/covering-designs: C(28,13,4) <= 53, C(32,13,4) <= 95). If a live table cannot be fetched, the claim is 'PENDING TABLE CHECK', not a record. Parameters must be within v <= 99, k <= 25, t <= 8, and b must be at least the Schonheim bound L(v,k,t); going below it means a bug. Same-day claim only if C(v,t) <= 5e9, so the exhaustive coverage check runs on a laptop; larger cases are logged as 'PENDING chunked exhaustive check' and claimed only after that full check completes.

## Statistic and checker
- The object: a block file, one block per line, k integers in 1..v.
- Checkers: runs/2026-10-15-1535/attempts/evaluator-first/code/cover_check.py (exact, exhaustive over all C(v,t)
  t-subsets) plus, at claim time, a second independently written check. Statistic: b = number of blocks, with
  distinct == b, uncovered == 0, every block k distinct points in 1..v.
- Comparison values, re-fetched when a candidate exists: (1) the live coveringrepository.com value from
  https://coveringrepository.com/download_archive_vkt.aspx (m = t row); (2) LJCR: Zenodo latest version
  coverdata.json "size" and GitHub dmgordo/LJCR coverdata.json "size" (dmgordon.org/covering-designs/ shows no
  per-cell numbers); (3) a GitHub/arXiv search for the same (v,k,t) over the last 6 months.

## Thresholds
- Win (full criterion): b < min(all comparison values), b >= Schonheim L(v,k,t), b >= LJCR low_bd, v <= 99, k <= 25,
  t <= 8, C(v,t) <= 5e9, checker PASS. A tie is not a win and is not claimed.
- The carried claim C(61,25,3) <= 27 (run 2026-10-15-1535) is judged by exactly this rule; its panel runs on a copy
  in claim/ with the table re-fetched in this run.
- A cell improved by anyone in the last 7 days is not a target (charter kill criterion 3).
- Partial wins p1 (lottery) and p2 (lower bound) are not pursued unless a lens says so in a new, timestamped
  PREREG.v2.md.
- Each further hit is a separate one-cell claim; a hit found after 80% of the budget is recorded as PROMISING
  (single-context, unpanelled) for the next run's panel.

## Null design
null_test: not needed because every claim is an explicit block set checked exhaustively by a deterministic checker
against a fetched table value; no statistical or search-chance statistic is scored.

## Lens kill rules (charter)
- evaluator-first: dead if the engine cannot reproduce a published entry exactly within an hour.
- oldest-entry: dead after three old cells in a row reproduce at the live value but not below it under a solid search.
- symmetric-constructor: dead when the best structured object for a cell sits more than 2% above the live value after
  the family is exhausted.
- solver: dead when calibrated scaling puts the target beyond a week of nights.
- any search: dead after two hours on a plateau above the record with no downward trend.
