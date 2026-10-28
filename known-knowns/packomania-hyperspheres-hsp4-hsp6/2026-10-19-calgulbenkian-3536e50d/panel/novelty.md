# Novelty report: hsp4-170 (Packomania equal balls in the unit 4-ball, N = 170)

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

role: novelty (skeptic 1 of 3). Read: the claim statement, INDEX.csv and the record files. I did not read or run the author's verifier scripts or receipts.

## Sources fetched (one plain GET each, honest client; the log is not shipped in this package; all fetched 2026-10-19, UTC times as listed)
| Source | URL | UTC | HTTP | sha256 |
|---|---|---|---|---|
| Packomania pending requests | https://packomania.com/pending-requests.html | 05:37:25 | 200 | 92ce2e3dd9802a85edda90ace95a1e7d81dac08297c3903bba46289cdb2a14ae |
| Packomania hsp4 radius.txt | https://packomania.com/hsp4/txt/radius.txt | 05:37:26 | 200 | f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f |
| Packomania hsp5 radius.txt | https://packomania.com/hsp5/txt/radius.txt | 05:37:27 | 200 | 2c87be8ca80d6c74044e2cb4c56acd8d0b735fb70faedc96fd54a1db1be18cf8 |
| Packomania hsp4.html | https://packomania.com/hsp4/hsp4.html | 05:37:27 | 200 | 1c3a30644ba8ff73955547ff94e769a1983c146f4d2b14989eab3e0060a3feb3 |
| Packomania hsp5.html | https://packomania.com/hsp5/hsp5.html | 05:37:28 | 200 | 2134e001531c02218920197518ded80babc08fdbd6caf8e9fbb85129893de7f4 |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 05:37:22 | 200 | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 |
| known-knowns listing | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns | 05:37:22 | 200 | 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011 |
| known-knowns hsp folder | .../contents/known-knowns/packomania-hyperspheres-hsp4-hsp6 | 05:38:50 | 200 | 129aa0cf10c6aad0df9bb54da21fb0f607ebb7ffdeebcc675385698a1a591144 |
| Zenodo Moki and Julio, latest version (record 22986800, v2.7, published 2026-09-27); the first request to record 22981305 versions/latest answered 301 and was followed once | https://zenodo.org/api/records/22986800 | 05:37:46 | 200 | 62935b6b5f6f418f78bf09d4573d046ce405c98c23fddd5efcda6f23afcf0f66 |
| Same record, the zip file (581877889 bytes; md5 matches Zenodo's 24462e98...); I read MANIFEST.csv inside it (sha256 b7a042ef6a29ce8b219660691212111262e4091c14b941721dd1d3f491eec568, identical to the package folder's snapshot copy; the 220 hsp4 rows in the-record-we-beat/mj_rows_extract.csv match it with zero differences). The zip itself was deleted after extraction; its sha256 was f2dc44bd0b2800fae918268fb97eeb21560aa889d6369a4e4877444339da3da7 | https://zenodo.org/api/records/22986800/files/Hashirama1337s/moki-julio-circle-packing-v2.7.zip/content | 05:38:21 to 05:48:07 | 200 | see left |
| Cohn spherical-codes table | https://spherical-codes.org/plain | 05:42:49 | 200 | b99df04be3cbcc783533027be54eb903ca462c00591caaccfaa0a0bdb8a3e577 |
| arXiv API, query 4 (packing, hyperball, records) | export.arxiv.org api query | 05:37:40 | 200 | 28cbee8a48f5e0378069c57ad29eba28f481bbe8bb0a4f50d4f8791c43030462 |

Pull requests: I used a saved list of every V3R1T4S pull request (title and body; 473 entries, highest number 481; fetched 2026-10-19T04:30:31Z; sha256 0a1d00562d9b2af7d165703ebb9732af8e1bc3328848eba98c8cc3096dd5bb14) instead of the api.github.com pulls pages. I read every title and the bodies of PRs 350, 372, 377, 390 and searched all titles and bodies for the target N values. The PR 350 maintainer ruling (a value that follows from table or merged values by a standard propagation rule is not a separate record) is taken as given to me; the saved body of PR 350 itself is an unrelated constant-weight-code claim, so I could not read the ruling text.

## Primary table value (my fetch of the hsp4 radius table, 2026-10-19T05:37:26Z, HTTP 200)
- N=170: 0.215589695168 (the file ends at N=300; the table is monotone near N=170; the maximum over all N' >= 170 is the N=170 row itself).
- Claimed r* = 0.2156450594683900081 (INDEX value 0.2156450594683900081281903). Margin over the live row: 5.5364e-5, above the criterion's 1e-10 by a factor of 5e5.

## Other known values
- Moki and Julio v2.7 manifest (read from the real manifest file inside the Zenodo zip; the package folder's copy matches exactly): hsp4 N=170 0.2155917530134953; maximum over N' >= 170 is that row. The claim exceeds it by 5.33e-5.
- Cohn's spherical-code table (my fetch, 4D rows): I converted every row N' >= 170 two ways, as a shell packing r = s/(2+s) with s = sqrt(2-2c), and as the N'-1 code plus a central ball (min of that r and 1/3). The best propagated value over N' >= 170 is 0.20897 (centre plus the 169-point code), far below the claim.
- Pull requests: none for N=170 other than the contributor's closed PR 106, which has the identical r* 0.2156450594683900081281903. Per ruling R1 this is a REFILE of an early filing closed unmerged in the 2026-10-14 bulk close, not a competing value. Reported, not counted against the claim.
- Pending queue (page dated 17-Oct-2026): categories named are csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv, cci, ssp. No hsp4, hsp5 or hsp6 entry. The category-unspecified Moki and Julio bundle (4666 candidates, 26-Sep-2026) is still listed.
- History of updates: the hsp4 page last update 06-Jul-2025 (Extension to N=300); the hsp5 page last update 01-Aug-2025 (first presentation N=2-300). No 2026 entry on either page. the radius table for each has 299 rows, N=2..300.
- Both Packomania histories say that for N=24-53 and 55 a ball packing is built from the spherical code on N-1 points plus one central ball; that is the same propagation I applied to Cohn's table below.
- V3R1T4S: PR 372 (open) reports that the hsp5 and hsp6 per-N files carry 4 coordinates and that the tables are contested (PR 286 is referred to but is not in the saved list). Known-knowns for this target hold 12 hsp4 folders, all by another contributor, none for the N value of this cell. Open and merged PRs on hsp4 are for N between 30 and 119 (e.g. 131-141, 242-251, 309-310, 361), none for N=170 or N>=300. Closed PR 106 (hsp4 N=170) is the contributor's own bulk-closed filing (the contributor's review ruling R1): reported, not competing. The trophy-case file has no hsp entry.

## Open questions answered
- Manifest copy faithful? Yes (verified against the real file). Does the bundle hold a value at or above the claim? The Zenodo release does not (max 0.21559). unresolved: the queued 4666-candidate bundle itself; no hsp entry is named in the queue.
- Same-day re-fetch the bar? I re-fetched; the table has not changed since July 2025 (the hsp4 page last update 06-Jul-2025).
- Header radius vs coordinate radius: not a novelty matter; the comparison here is against the table value, 5.5e-5 below the claim, so a 17th-digit mismatch does not change the verdict.

## Verdict
The claim strictly beats the live row (5.5e-5), the Moki and Julio v2.7 manifest (5.3e-5), the propagated Cohn bar (about 6.7e-3) and every PR. The only matching item is the contributor's own earlier closed filing (PR 106, the contributor's review ruling R1). The posted N=170 file is a real 4D file (4 coordinates), so non-isometry can be tested directly (criterion role).

novelty: NEW against all readable sources (refile of closed PR 106, ruling R1)

pass: true
