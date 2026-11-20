# The record this claim is measured against

This cell has no published leaderboard and, unusually, **no prior public claim either** - the one contributor who
computed a number on it withheld it. Both the bank's status source and that withheld figure are recorded here.

## 1. The bank's status source

- URL: https://export.arxiv.org/api/query?search_query=abs:%22sperm%20whale%22&sortBy=submittedDate&sortOrder=descending&max_results=25
- Fetched: 2026-11-19T09:37:53Z
- HTTP status: 200
- Bytes: 40,549
- sha256 of the response: 1d1a18b7520dbb62d3416d2e8a45e0c0d01378ed080bc6d5929f0fc849c4e94f
- Selected headers: `content-type: application/atom+xml; charset=UTF-8`
- What was extracted: the entries newer than the bank's own 2026-11-13 check are 2606.16084v5, 2609.16612v3 and
  2610.33974v2 (all 2026-11-17, Sinha and Chavan) and 2610.29101v1. None reports a value on this cell. The Sinha
  and Chavan line of work is on other corpora with other tokenisations and, on its own reported numbers, does not
  clear this benchmark. So the target was open on the literature side at the time of this run.

The page itself is not copied into this package. The NOVELTY panellist's own fetches are saved under the run's
`attempts/dominica/panel_work/novelty/`, not here.

## 2. The withheld in-cell figure: V3R1T4S draft PR #1159

Found by this run's NOVELTY panellist at 2026-11-19T10:16:39Z.

| quantity | PR #1159 | this claim |
|---|---|---|
| Dominica gain over the smoothed bigram | 0.097416 | **0.128423** |
| claimed as p3? | **no, withheld** | yes |
| stated reason | its own within-stream payload-shuffle control | - |

- That PR is the first public clearance of this target's **full criterion** and, through its companion #1175, of
  **p4**. On **p3** it makes no claim, so there is no prior public claim on this cell to improve on. Our figure is
  nonetheless higher than theirs, on the same file.
- Their reason for withholding is the most useful thing in the record, and it is the reason design N6 exists. See
  `how-we-built-it/composition-null/README.md`, which also explains why the obvious form of that control is
  invalid as a null and why, on our numbers, their figure may have been withheld unnecessarily. We have not seen
  their code and make no claim about their work.
- They also report the Dominica extension being added after their first results were seen. Ours was a
  pre-registered lens of the run, frozen at 2026-11-19T09:55:11Z with the other three, which is a difference in
  provenance rather than in quality and is stated here so a reader can weigh it.

## 3. TROPHY_CASE.md

No entry covers this cell, so this claim is not a duplicate of an already-listed result. Checked against the
repository at commit 5d2d31e76fe1f4d7eb4b75c7646d06425c10640c.

## A refusal worth recording

api.github.com answered HTTP 403 (rate limit) at 2026-11-19T09:38:39Z during this run and was not retried, per
the operator's standing no-retry rule. The draft pull request above was therefore read through a different route
by the NOVELTY panellist, after that refusal. Two secondary sources were never read at all: an OpenReview PDF and
a phys.org page, both HTTP 403, neither retried.
