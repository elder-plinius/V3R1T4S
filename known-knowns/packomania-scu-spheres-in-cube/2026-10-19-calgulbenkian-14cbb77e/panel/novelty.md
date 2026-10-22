# Novelty report: scu-733 (Packomania spheres in a cube, N = 733)

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

role: novelty (skeptic 1 of 3). Read: the claim statement, INDEX.csv and the record files. I did not read or run the author's verifier scripts or receipts. This report does not judge whether the packing is valid (reproduce does that) or whether the wording of the criterion is met (criterion does that).

## Sources fetched (one plain GET each, honest client; the log is not shipped in this package; all fetched 2026-10-19, UTC times as listed)
| Source | URL | UTC | HTTP | sha256 |
|---|---|---|---|---|
| Packomania scu radius.txt | https://packomania.com/scu/txt/radius.txt | 05:37:23 | 200 | 2e2af491aa08d8eba54a88cdbb6b3b007dacac59f4f12d60d00a3687d8b01791 |
| Packomania scu.html | https://packomania.com/scu/scu.html | 05:37:24 | 200 | 7b77906badc3ee9ed081ee8dd6033b4897531b3a932e6fd03fe828963eb8c1de |
| Packomania pending requests | https://packomania.com/pending-requests.html | 05:37:25 | 200 | 92ce2e3dd9802a85edda90ace95a1e7d81dac08297c3903bba46289cdb2a14ae |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 05:37:22 | 200 | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 |
| known-knowns listing | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns | 05:37:22 | 200 | 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011 |
| known-knowns scu folder | .../contents/known-knowns/packomania-scu-spheres-in-cube | 05:38:51 | 200 | c812a1132623d5d083cc982e44551b3db93005c10b12404434cac40d00ab87e7 |
| Zenodo Moki and Julio, latest version (record 22986800, v2.7, published 2026-09-27); the first request to record 22981305 versions/latest answered 301 and was followed once | https://zenodo.org/api/records/22986800 | 05:37:46 | 200 | 62935b6b5f6f418f78bf09d4573d046ce405c98c23fddd5efcda6f23afcf0f66 |
| Same record, the zip file (581877889 bytes; md5 matches Zenodo's 24462e98...); I read MANIFEST.csv inside it (sha256 b7a042ef6a29ce8b219660691212111262e4091c14b941721dd1d3f491eec568, identical to the package folder's snapshot copy; the 455 scu rows in the-record-we-beat/mj_rows_extract.csv match it with zero differences). The zip itself was deleted after extraction; its sha256 was f2dc44bd0b2800fae918268fb97eeb21560aa889d6369a4e4877444339da3da7 | https://zenodo.org/api/records/22986800/files/Hashirama1337s/moki-julio-circle-packing-v2.7.zip/content | 05:38:21 to 05:48:07 | 200 | see left |
| Cohn spherical-codes table | https://spherical-codes.org/plain | 05:42:49 | 200 | b99df04be3cbcc783533027be54eb903ca462c00591caaccfaa0a0bdb8a3e577 |
| arXiv API, query 4 (packing, hyperball, records) | export.arxiv.org api query | 05:37:40 | 200 | 28cbee8a48f5e0378069c57ad29eba28f481bbe8bb0a4f50d4f8791c43030462 |

Pull requests: I used a saved list of every V3R1T4S pull request (title and body; 473 entries, highest number 481; fetched 2026-10-19T04:30:31Z; sha256 0a1d00562d9b2af7d165703ebb9732af8e1bc3328848eba98c8cc3096dd5bb14) instead of the api.github.com pulls pages. I read every title and the bodies of PRs 350, 372, 377, 390 and searched all titles and bodies for the target N values. The PR 350 maintainer ruling (a value that follows from table or merged values by a standard propagation rule is not a separate record) is taken as given to me; the saved body of PR 350 itself is an unrelated constant-weight-code claim, so I could not read the ruling text.

## Primary table value (verbatim from my fetch of the scu radius table, 2026-10-19T05:37:23Z, HTTP 200)
- N=733: 0.058531064607
- N=734: 0.058943675866 (largest row at any N' >= 733 in the file; file has 1134 rows, N=1..1024192)
- N=739: 0.058531064606, N=741: 0.058627036756
- Claimed r* = 0.0589437529548279448 (from the claim sentence; INDEX.csv value 0.0589437529548279448024778).
- Margin over the row for N=733: 0.058943752955 - 0.058531064607 = 4.1269e-4. Margin over the propagated bar (row 734): 0.058943752955 - 0.058943675866 = 7.709e-8, which is 7.7e4 times the table's 12-decimal resolution and 7.7e3 times the criterion's 1e-11 margin.

## Which bar applies (open question 1)
The live row for N=733 sits below its neighbour N=734, so it is a stale row; a 733-sphere packing of radius at least r(734) follows by deleting one sphere from the posted 734 packing. That propagation is the PR 350 type of rule, and it gives exactly 0.058943675866, not more. The claim exceeds that propagated bar by 7.7e-8, so it is not a value that follows from the table by deletion. It comes from re-jamming after deletion, a local optimization that produces a new radius. My answer: the bar is 0.058943675866 (max over N' >= 733), and the claim strictly beats it. It is not removed by the PR 350 rule, because the rule covers values that follow by propagation, and this one does not (it is larger than the propagated value by far more than rounding). Whether the panel wants a different reading of "the live value for that N" is for the criterion role; on either reading the claim beats the bar.

## Moki and Julio bundle (open question 3)
The snapshot copy in the package folder is faithful: I read the real manifest file from the Zenodo v2.7 zip and every scu row in the package folder's copy (the-record-we-beat/mj_rows_extract.csv) matches it exactly. Manifest scu N=733: 0.0588218693814829; manifest maximum at any N' >= 733: 0.0588218693814829 (N=733 itself); N=734: 0.0586830674. All are below the claim (by 1.2e-4 at N=733). The Packomania bundle of 4666 candidates cannot be inspected (it is a private queue item); the Zenodo release holds 6071 rows over all shelves, so the two are not necessarily the same set. unresolved: whether the queued 4666-candidate bundle contains an scu N=733 value above 0.0589437. Nothing visible suggests it does.

## Non-isometry against the derived packing (open question 2)
Novelty point only: the contributor's triage record says the object is the posted 734 packing with one sphere removed and relaxed. The claim still strictly beats the radius of the packing it was derived from (7.7e-8), so it is not a copy. I leave the wording of the isometry clause to the criterion skeptic.

## Table in motion (open question 4)
The table was rewritten on 04, 05, 06, 08 and 17 Oct 2026. My fetch is 5 hours after triage and byte-identical in the radius table and the scu page. N=733 is not named in any update. The row could still be raised when the maintainer processes queued bundles; this is a risk to the claim's lifetime, not evidence of prior art. A neighbour already received the same kind of update on 17-Oct (734-737), so a competing 733 value by the same contributor is plausible but not visible.

## Exact decimals (open question 5)
Not a novelty question; the margin 7.7e-8 is far above any rounding of the 20-decimal coordinates (about 1e-20).

## Literature, other sources
- Listed in my fetches above: Packomania, Zenodo, V3R1T4S PRs and known-knowns, the trophy-case file. arXiv query 4 (packing, hyperball, records, 25 results max) returned one unrelated paper (hyperball coverings, 2021).
- unresolved: the 2022 Lai, Hao, Xiao and Glover candidates that the History says were posted on 04-Oct-2026 for about 60 values of N; I could not tell from the page whether N=733 is among them, but the row for 733 is still credited to the old reference and equals 0.058531064607 (as above), so no such value is in the live table. I did not search for that paper (the four arXiv queries were used). It could plausibly hold a larger-N value that propagates to 733, but the History says the table already incorporates it, and the table's maximum at N' >= 733 is the 734 row used above.
- Pending queue: the page (dated 17-Oct-2026) lists no scu entry. The category-unspecified 26-Sep-2026 Moki and Julio bundle of 4666 candidates is still listed. The Zenodo v2.7 release of Moki and Julio (27-Sep-2026) is the visible counterpart; its manifest has 455 scu rows and is lower than the claim at every N' >= N (below).
- History of updates (the scu page, last entry 17-Oct-2026): the 17-Oct entry credits Vidit Patankar with rows including 734-737 and 740-742, and announces a reorganization of the table. N=733 is not named in any 2026 entry; the radius table file was last modified 18-Oct-2026 08:54 GMT per PR 377, and its sha256 is the same as the package folder's copy and the triage fetch of 2026-10-19T04:31:56Z, so the table did not move between triage and now.
- Open and closed PRs: no PR in the saved list names scu N=733 (the scu PRs are N=385, 472 and neighbours, 619, 631, 793, 806, 812, 881-886, 1596; none near 733). Closed PRs 108-120 are the contributor's own bulk-closed filings for other N (the contributor's review ruling R1) and not relevant to this N. Merged scu known-knowns: two folders by another contributor (16-Oct-2026), not this N.
- The trophy-case file: no Packomania or sphere-in-cube entry for this N.

## Verdict
The claimed radius strictly exceeds the live row for N=733 (by 4.1e-4), the propagated bar (row 734, by 7.7e-8), the Moki and Julio v2.7 manifest (by 1.2e-4), and every PR and trophy entry I could find. No pending-queue entry names scu. Caveats: the 4666-candidate bundle is unreadable, and the table is being revised. Nothing known ties or beats the claim.

novelty: NEW against all readable sources

pass: true
