# The record this claim is measured against

This cell has no published leaderboard. Two things stand in for one: the bank's own `status_source`, and the only
public in-cell value, which is another contributor's draft pull request in this same repository - and which
cleared this cell before us.

## 1. The bank's status source

- URL: https://export.arxiv.org/api/query?search_query=abs:%22sperm%20whale%22&sortBy=submittedDate&sortOrder=descending&max_results=25
- Fetched: 2026-11-19T09:37:53Z
- HTTP status: 200
- Bytes: 40,549
- sha256 of the response: 1d1a18b7520dbb62d3416d2e8a45e0c0d01378ed080bc6d5929f0fc849c4e94f
- Selected headers: `content-type: application/atom+xml; charset=UTF-8`
- What was extracted: the entries newer than the bank's own 2026-11-13 check are 2606.16084v5, 2609.16612v3 and
  2610.33974v2 (all 2026-11-17, Sinha and Chavan) and 2610.29101v1. None reports a value on this cell; they use
  other corpora and other tokens, and none addresses the binary same-or-switch task at all. So the target was open
  on the literature side at the time of this run.

The page itself is not copied into this package. The NOVELTY panellist's own fetches are saved under the run's
`attempts/turn-taking/panel_work/novelty/`, not here.

## 2. The public in-cell value: V3R1T4S draft PR #1175

Found by this run's NOVELTY panellist at 2026-11-19T10:16:39Z.

| quantity | PR #1175 | this claim |
|---|---|---|
| model, pooled bits per position | 0.780268 | **0.763112** |
| reference, pooled bits per position | 0.850317 | 0.850317 |
| gain | 0.070050 | **0.087206** |
| scored positions | 3,418 | 3,418 |
| created | 2026-11-19T09:59:53Z | not filed when this package was built |

- **#1175 is the first public clearance of partial win p4.** This claim is a record improvement of 0.017156 bits
  on it, not first evidence, and any listing should say so. Maintainers can credit this cell only once.
- The timing is on the record because it is close: #1175 was created **4 minutes 42 seconds** after this run's
  pre-registration freeze at 2026-11-19T09:55:11Z, and the run's novelty check at packaging time is what found
  it. This claim does not derive from it. The model, its features and the freeze all predate its creation, and
  nothing in this package was changed after it was read, other than the disclosures that name it.
- Both sides use the same reference to six decimals (0.850317), which is a useful independent check that the
  bank's p4 comparator is unambiguous - unlike the bank's R1 for the full criterion, where the same run found
  three defensible readings. That difference is reported as a bank defect, separately from this claim.
- #1175 also discloses a switch-pattern-style limitation. Our own switch-pattern-only diagnostic gains 0.059453,
  which is **below** #1175's 0.070050, so neither result reduces to the switch pattern alone.

## 3. TROPHY_CASE.md

No entry covers this cell, so this claim is not a duplicate of an already-listed result. Checked against the
repository at commit 5d2d31e76fe1f4d7eb4b75c7646d06425c10640c.

## A refusal worth recording

api.github.com answered HTTP 403 (rate limit) at 2026-11-19T09:38:39Z during this run and was not retried, per
the operator's standing no-retry rule. The draft pull request above was therefore read through a different route
by the NOVELTY panellist, after that refusal.
