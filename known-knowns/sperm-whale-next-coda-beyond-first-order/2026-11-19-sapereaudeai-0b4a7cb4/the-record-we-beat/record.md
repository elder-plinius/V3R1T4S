# The record this claim is measured against

This target has no published leaderboard or table cell. Two things stand in for one, and both are recorded here:
the bank's own `status_source`, and the only public in-cell value, which is another contributor's draft pull
request in this same repository.

## 1. The bank's status source

- URL: https://export.arxiv.org/api/query?search_query=abs:%22sperm%20whale%22&sortBy=submittedDate&sortOrder=descending&max_results=25
- Fetched: 2026-11-19T09:37:53Z
- HTTP status: 200
- Bytes: 40,549
- sha256 of the response: 1d1a18b7520dbb62d3416d2e8a45e0c0d01378ed080bc6d5929f0fc849c4e94f
- Selected headers: `content-type: application/atom+xml; charset=UTF-8`
- What was extracted: the entries newer than the bank's own 2026-11-13 check are 2606.16084v5, 2609.16612v3 and
  2610.33974v2 (all 2026-11-17, Sinha and Chavan) and 2610.29101v1. None of them reports a value on this cell:
  they use other corpora (1,483 to 1,952 audio codas) and other tokens. So the target was open on the literature
  side at the time of this run.

The page itself is not copied into this package.

## 2. The only public in-cell value: V3R1T4S draft PR #1159

Found by this run's NOVELTY panellist at 2026-11-19T10:16:39Z (its own fetches are saved under the run's
`panel_work/novelty/`, not here).

| quantity | PR #1159 | this claim |
|---|---|---|
| pooled cross-entropy of the model | 2.564371 | **2.123847** |
| reference R1 | 2.794781 | 2.780154 |
| single-previous-coda twin | 2.850952 | 2.654909 |
| model family | order-3 n-gram with backoff | log-linear with stream-local and ordered features |
| filed | 2026-11-18 | not filed |

- **#1159 cleared this criterion publicly first**, one day before this run. This claim is a record improvement of
  0.4406 bits on it, not first evidence of the effect, and any listing should say so.
- The same contributor's draft PR #1175, created 2026-11-19T09:59:53Z, is the first public clearance of partial
  win p4 (0.780268 bits against the same 0.850317 reference). That is a different cell from this package's and is
  recorded here only so the sequence of events is on the record: #1175 was created 4 minutes 42 seconds after
  this run's pre-registration freeze at 2026-11-19T09:55:11Z.
- The R1 difference (2.780154 here, 2.794781 there) is a convention difference in a step the bank leaves open,
  not a disagreement about a measured quantity. This run's CRITERION panellist reproduced 2.794781 exactly by
  recutting the duration bin edges inside the inner cross-validation. See README.md, "Compared to".

## 3. TROPHY_CASE.md

No entry covers this cell, so this claim is not a duplicate of an already-listed result. Checked against the
repository at commit 5d2d31e76fe1f4d7eb4b75c7646d06425c10640c.

## A refusal worth recording

api.github.com answered HTTP 403 (rate limit) at 2026-11-19T09:38:39Z during this run and was not retried, per
the operator's standing no-retry rule. The two draft pull requests above were therefore read through a different
route by the NOVELTY panellist, after that refusal.
