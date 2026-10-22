# Novelty report: scu-739 (Packomania spheres in a cube, N = 739)

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

role: novelty (skeptic 1 of 3). Read: the claim statement, INDEX.csv and the record files. I did not read or run the author's verifier scripts or receipts. This report does not judge validity of the packing or the criterion wording.

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
- N=739: 0.058531064606; N=740 and N=741: both 0.058627036756 (largest rows at any N' >= 739); N=742: 0.058625297431.
- Claimed r* = 0.0586275441666459796 (INDEX value 0.0586275441666459796140567).
- Margin over the row for N=739: 9.648e-5. Margin over the propagated bar (rows 740/741, 0.058627036756): 0.058627544167 - 0.058627036756 = 5.074e-7, about 5e4 times the table resolution and 5e4 times the criterion's 1e-11 margin.

## Which bar applies (open question 1)
The live row for N=739 equals the row for N=733 to within 1e-12 and is below the rows for 740 and 741: it is a stale row. Deleting spheres from the posted 741 packing (credited in the History to Vidit Patankar, 17-Oct-2026) gives r(739) at least 0.058627036756 by propagation. The claim exceeds that by 5.07e-7, so it does not follow from the table by deletion alone; the extra gain comes from re-jamming. My answer: the bar is 0.058627036756, the claim strictly beats it, and it is not removed by the PR 350 propagation rule.

## Moki and Julio bundle (open question 3)
Faithful: the package folder's copy of the manifest rows (the-record-we-beat/mj_rows_extract.csv) matches the real manifest file of Zenodo v2.7 (sha256 b7a042ef..., zero row differences over 455 scu rows). Manifest scu N=739: 0.0586073866757681; maximum at any N' >= 739 in the manifest: 0.0586073866757681 (N=739 itself, since larger N have smaller values). All are below the claim (by 2.0e-5 at N=739). unresolved: contents of the queued 4666-candidate Packomania bundle; nothing visible suggests it is higher.

## Non-isometry against the derived packing (open question 2)
The object is the posted 741 packing with two spheres removed and relaxed. It strictly beats the radius of that packing by 5.07e-7, so it is not a copy of it. Wording of the isometry clause is left to the criterion skeptic.

## Table in motion (open question 4)
The radius table and the scu page are byte-identical to the triage fetch (same sha256). The 17-Oct History names 740-742 and 745-747 (Patankar) but not 739. The row may be raised later; no prior art visible.

## Exact decimals (open question 5)
Not a novelty question; margin 5e-7 is far above 20-decimal rounding.

## Literature, other sources
arXiv query 4 returned one unrelated paper. unresolved: the Lai, Hao, Xiao and Glover (2022) candidate set mentioned in the History; not searched (arXiv query budget was used); the live table has already absorbed it according to the History.
- Pending queue: the page (dated 17-Oct-2026) lists no scu entry. The category-unspecified 26-Sep-2026 Moki and Julio bundle of 4666 candidates is still listed. The Zenodo v2.7 release of Moki and Julio (27-Sep-2026) is the visible counterpart; its manifest has 455 scu rows and is lower than the claim at every N' >= N (below).
- History of updates (the scu page, last entry 17-Oct-2026): the 17-Oct entry credits Vidit Patankar with rows including 734-737 and 740-742, and announces a reorganization of the table. N=739 is not named in any 2026 entry; the radius table file was last modified 18-Oct-2026 08:54 GMT per PR 377, and its sha256 is the same as the package folder's copy and the triage fetch of 2026-10-19T04:31:56Z, so the table did not move between triage and now.
- Open and closed PRs: no PR in the saved list names scu N=739 (the scu PRs are N=385, 472 and neighbours, 619, 631, 793, 806, 812, 881-886, 1596; none near 739). Closed PRs 108-120 are the contributor's own bulk-closed filings for other N (the contributor's review ruling R1) and not relevant to this N. Merged scu known-knowns: two folders by another contributor (16-Oct-2026), not this N.
- The trophy-case file: no Packomania or sphere-in-cube entry for this N.

## Verdict
The claimed radius strictly exceeds the live row for N=739 (9.6e-5), the propagated bar (5.1e-7), the Moki and Julio v2.7 manifest (2.0e-5), and every PR and trophy entry I could find. Caveats: unreadable 4666-candidate bundle, table under revision.

novelty: NEW against all readable sources

pass: true
