# Status page check (the panel's single fetch of the status page was refused with HTTP 403)

The honest single fetch (curl, User-Agent naming V3R1T4S) was refused with HTTP 403 and was not retried. At the operator's instruction, both pages were then read in the operator's own logged-in Chrome browser on 2026-11-19 at about 12:00Z (the pages loaded normally, with no challenge page; no cookies, user agents or proxies were altered). The operator chose this machine read over a manual look, and it is disclosed here so the maintainer can judge it. What the automated read showed:

- https://www.erdosproblems.com/7: the problem is listed as open ($25 prize), with the BBMST and Hough-Nielsen results in the text; the page states no numeric lower bound on the lcm L. It shows 23 comments and 0 proof claims.
- https://www.erdosproblems.com/forum/thread/7: the newest post is dated 15 Sep 2026. The largest bound on L stated anywhere in the thread is 11,486,475 (Egeozturk). The numbers 9,704,539,845, 1,527,701,174 and 168,131,152,814,625 do not appear on the page.

Other bounds the novelty reviewers found off the status page (all below the claimed 168,131,152,814,625): Mian-Siddique (arXiv:2607.25628) L > 10,000; a Lean proof posted on GitHub on 2 Nov 2026, L > 1,527,701,174; Schroeder (Zenodo, Sep 2026, unrefereed) L >= 9,704,539,845. Dai, Li, Li and Yi (arXiv:2611.15110) prove that 45 divides L and that the least modulus is at most 9, which is not a lower bound on L.
