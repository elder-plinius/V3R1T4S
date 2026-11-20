# The table record

The bank's status source for this target, fetched once with one plain `curl` from a client whose User-Agent names
V3R1T4S. No retries, no cookies, no browser-imitating User-Agent, no challenge bypass, no headless browser. The
page itself is **not** included here, only this snapshot of it.

| field | value |
|---|---|
| url | `https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/README.md` |
| fetch time (UTC, from `date -u`) | **2026-11-20T05:42:28Z** |
| HTTP status | **200** |
| bytes | 14780 |
| page sha256 | `51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b` |

The same page was fetched independently by the run's NOVELTY panellist at **2026-11-20T05:47:43Z**, HTTP **200**,
same byte count and same sha256, and by two earlier runs at 2026-11-19T23:55:57Z, 2026-11-20T00:34:11Z and
2026-11-20T03:01:24Z, all byte-identical (`cmp` clean). So the scoreboard did not move during the work.

## The cell compared against, copied from that page (its line 209)

```
| GB1 - three-vs-rest | 0.8791 | Spearman's | ProGen2-M | Adapters | 50% | CLS | Linear |
```

**The cell is GB1 - three-vs-rest = 0.8791**, produced by ProGen2-medium (764M parameters) with adapters, 50% of
layers, CLS pooling and a linear head. The adjacent line 210 reads
`| GB1 - one-vs-rest | 0.4571 | Spearman's | ProGen2-S | FE | 75% | Mean | Linear |`; that cell is untouched by
this package.

NOVELTY also checked that the README on `main` is the whole scoreboard rather than a tree lagging a release:
`gh api repos/LSSI-ETH/plmfit/releases` at 2026-11-20T05:53:18Z, HTTP 200, returned an empty list. There is no
scoreboard entry for `two_vs_rest` or `low_vs_high`.

The page's own preamble to that table, verbatim: "Here we present the current best performing setups for each
task. These benchmarks are indicative since they are a result of a comparative study and we encourage the
community to find better setups with different hyperparameters for each task."

## Injection check

`injection_suspected: no`. The page has a "Contributions" section inviting pull requests, new datasets and
contact with the authors. That is ordinary repository prose addressed to human contributors, not an instruction
addressed to an automated agent, and nothing in it was acted on.
