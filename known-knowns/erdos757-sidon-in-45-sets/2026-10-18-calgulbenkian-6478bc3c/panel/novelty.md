# Novelty report: e757-n21

context: Claude Code subagent, fresh context

Claim (partial win p1): a (4,5)-set with 21 elements (not a multiple of 14), exact Sidon number 12, ratio 12/21 = 4/7, equal to the live best upper bound. This is a tie in the ratio by definition; the novelty question is whether a witness with |A| not a multiple of 14 at 4/7 is already known.

## Primary and named sources (each fetched once)
- https://www.erdosproblems.com/757, 2026-10-18T14:25:04Z, HTTP 200, sha256 0e2f7de764a9423eafe5210cf0d1e6ee8c91125d37f3c98bfdf3a9eb8ca785de. Quote: "Ma and Tang [MaTa26] have improved these bounds to 9/17 <= c <= 4/7." Page last edited 10 April 2026. Live best upper bound: 4/7.
- Forum thread https://www.erdosproblems.com/forum/thread/757, 14:25:05Z, HTTP 200, sha256 15efc704e89536fca85068c46dcea85c8ac03debfea015e281f155b626167f16. Seven comments (Jan to Feb 2026): the positivity assumption, the Gyarfas-Lehel bound, the Ma-Tang paper and the optimization-constants entry. No witness of any size is posted, so nobody posted a non-multiple-of-14 witness at 4/7.
- EinsteinArena https://einsteinarena.com/problems/sidon-45-set, 14:25:05Z, HTTP 200, sha256 8aa7ed037111d6a9eac59bc01f82cc9a382698fe45abbe26a0c822a17ba22044. Leaderboard: 1 Ma-Tang (previous SOTA) 0.571428571, 2 Hermes-Nous 0.588235294, 3 Wilhelmina 0.600000000, 4 GPT-Explorer 0.615384615. The one witness shown is the 14-element Ma-Tang set. Discussion threads concern extending the 14-set and a hypergraph reformulation for n = 9..18. No 21-element set and no other set at 4/7.
- arXiv 2602.23282, abstract page 14:25:06Z, HTTP 200, sha256 e28d7f4e587488ce7d6748db3448109e60937f944b7f6860c2df13472a705155; HTML (https://arxiv.org/html/2602.23282, v2 of 6 Mar 2026) 14:27:27Z, sha256 d1aace4ca6e952deda0f2dbad7336e7e539b74c2e83eaef5a1954c2c1bd6bc29. The paper proves "c* = lim f(n)/n = inf f(n)/n" (Theorem 1.5) and gets 4/7 from n = 14 only. Its only explicit witnesses are the 14-point set and an earlier 12-point example giving 7/12. No 21-element or other non-multiple-of-14 witness at 4/7 appears.
- arXiv query (Sidon AND Erdos AND (4,5)), 14:26:18Z, HTTP 200 (sent over https after an http 301), sha256 e8f7624ed4f1b78210a438a1cc690bd6b1c8fb8ecb8a39f13a5f19cdab4f878d: one hit, 2602.23282 itself. No newer arXiv work on (4,5)-sets found.

## Repository sources (fetched once)
- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, 2026-10-18T14:23:15Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1. It lists no entry for this target family (no Erdos 757 row).
- Pull requests, pages 1 to 5: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1 to 5, 2026-10-18T14:23:15Z to 14:23:21Z, HTTP 200 each; page sha256 values cca876cd..., 176c41b2..., 20ec05c4..., f5d26a78..., and page 5 is an empty list (2ba33ca0...). 392 pull requests read by title.
- known-knowns folder listing: https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns, 2026-10-18T14:23:22Z, HTTP 200, sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011. Twenty folders; none belongs to this target.

## Pull requests on this target
Pull request 29 (calgulbenkian, closed unmerged, 2026-10-14) is the author's own earlier filing of the same 21-element set; not a competing value. No other pull request is about Erdos 757.

## Verdict
No source I could fetch lists a (4,5)-set with |A| not a multiple of 14 at 4/7. The ratio 4/7 itself only ties the live best (the kit says a tie is not a record); I pass this only as the enumerated partial win p1, whose definition is a tie in ratio plus a new witness shape, and only for the sources above. A reader who holds that a tie can never pass should read this as pass: false.
unresolved: Ma and Tang's code repository and the optimization-constants page (teorth.github.io, constant 5b) were not fetched, and EinsteinArena submissions beyond the four leaderboard rows were not inspected; an unlisted 4/7 witness there is possible though not indicated.
novelty: no earlier non-multiple-of-14 witness at 4/7 found; the ratio 4/7 equals the live best (tie), counted only as partial win p1.

pass: true
