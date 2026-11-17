# The record we beat: Erdős Problem 677 = Justin Sun Prize JSP-000550, k = 29

The status sources record the problem as open, with no verified range of (n, k). Previously known coverage for
k = 29, as found by the NOVELTY skeptic of this claim (`panel/novelty.md`, 2026-11-10):

| coverage | source |
|---|---|
| no solution with m + k ≤ 10^8, for every 3 ≤ k ≤ 100 (largest posted finite verification for this k) | laaielichter/erdos-677 on GitHub (2026-10-27) |
| every k, n ≤ 369k (n ≤ 10701 at k = 29), conditional on an assumed prime-interval hypothesis | HuanHuanHuanFFF/lean-math-lab |
| smaller searches (N = 40000 for k ≤ 24; n, m ≤ 2·10^5 for k ≤ 12; ...) | a trureturing pull request, Kuberwastaken/c5-k4, others (`panel/novelty.md`) |
| n ≤ 5871·k for every k, any m (n ≤ 170259 at k = 29; the contributor's own earlier package, not independent prior art) | package 2026-10-24-adb991-a6c79bec |

By Lemma A (`object/PROOF.md`, consequence (b): m + k ≤ (n + k)·R(29)^{1/29}, with R(29)^{1/29} ≈ 2.377), the
m + k ≤ 10^8 search implies "any m" only for n up to about 4.2·10^7 (`panel/novelty.md`). This package covers k = 29
for every n ≤ 10^494 and every m ≥ n + k.

## Status sources (fetched once each by the NOVELTY skeptic, User-Agent "V3R1T4S-research-bot")

| source | url | fetched (UTC) | HTTP | sha256 of the saved bytes | reads |
|---|---|---|---|---|---|
| prize catalog (status source) | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md | 2026-11-10T09:20:41Z | 200 | 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834 | JSP-000550: Current status Open, Lean proof No |
| problem page | https://www.erdosproblems.com/677 | 2026-11-10T09:20:41Z | 200 | bcafdf8fd4deee80f97ec3cf82d6c70d8a768c64d0bf062c7426882f53990e4c | open; "last edited 30 September 2025"; Proof claims (0) |
| forum thread | https://www.erdosproblems.com/forum/thread/677 | 2026-11-10T09:20:42Z | 200 | 4ba1f110375f8c29700dade626280c065f0149b60e33aa0a563084a2c750a512 | 8 comments (31 Mar to 2 Apr 2026), none on equal-k ranges |

The contributor's scouts also fetched the problem page on 2026-11-09T09:18:58Z (sha256 df78bb5f…) and
2026-11-10T09:19:01Z (sha256 ba6e9957…), and the catalog on both days (byte-identical, sha256 78ecc0e2…). The pages
are not copied into this package. No HTTP response headers were saved.
