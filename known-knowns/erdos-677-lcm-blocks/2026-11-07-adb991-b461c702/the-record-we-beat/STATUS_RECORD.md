# The record we beat: Erdős Problem 677 = Justin Sun Prize JSP-000550, k = 26..28

The status sources record the problem as open, with no verified range of (n, k). Previously known coverage for
k = 26..28, as found by the NOVELTY skeptic of this claim (`panel/novelty.md`, 2026-11-07):

| coverage | source |
|---|---|
| no solution with m + k ≤ 10^8, for every 3 ≤ k ≤ 100 (largest posted finite verification for these k) | laaielichter/erdos-677 on GitHub (2026-10-27) |
| n < m ≤ 1.5·10^5 for k ≤ 150 (second-hand: the paper itself could not be read) | Danesh–Bianchetti, IJMTT 72(9), 2026, as cited by MaxwellLaw/erdos-677-research |
| smaller searches (n, m ≤ 2·10^5 for k ≤ 12; N = 40000 for k ≤ 24; ...) | Kuberwastaken/c5-k4, a trureturing pull request, others (`panel/novelty.md`) |
| k ≤ 25 for every n ≤ 10^494, any m (the contributor's own earlier package, not independent prior art) | package 2026-10-24-adb991-201bcc74 |

By Lemma A (`object/PROOF.md`), the m + k ≤ 10^8 search implies "any m" only for n up to about 4.4·10^7
(`panel/novelty.md`). This package covers k = 26, 27, 28 for every n ≤ 10^494 and every m ≥ n + k.

## Status sources (fetched once each by the NOVELTY skeptic, User-Agent "V3R1T4S-research-bot")

| source | url | fetched (UTC) | HTTP | sha256 of the saved bytes | reads |
|---|---|---|---|---|---|
| prize catalog (status source) | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md | 2026-11-07T09:20:31Z | 200 | 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834 | JSP-000550 Current status Open, Lean proof No |
| problem page | https://www.erdosproblems.com/677 | 2026-11-07T09:20:32Z | 200 | 837f45777da64c53a1cd319f3df5173968d686c0e3c7ae8f310b5def282bc6de | open; "This page was last edited 30 September 2025"; Proof claims (0) |
| forum thread | https://www.erdosproblems.com/forum/thread/677 | 2026-11-07T09:20:32Z | 200 | 27734c68eb1109f9f73a2a5243889d7852d47b0cb804079bbd888ffc05a73c9c | 8 posts (31 Mar to 2 Apr 2026); no verification of the equal-length question for these k |

The contributor's own scouts also fetched the problem page on 2026-11-06T09:20:24Z (sha256 7ce2c96a…) and
2026-11-07T09:19:34Z (sha256 a8ff819a…): same statement and status. The pages are not copied into this package. No
HTTP response headers were saved.
