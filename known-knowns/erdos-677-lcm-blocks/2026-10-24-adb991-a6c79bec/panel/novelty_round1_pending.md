# NOVELTY: Erdős 677 partial claim (no counterexample with n ≤ 5871·k)

context: subagent (fresh context, Claude Code Agent tool)

Claim under review (claim/CLAIM.md): for every k ≥ 1, every 0 ≤ n ≤ 5871·k and every m ≥ n + k,
lcm(m+1, …, m+k) ≠ lcm(n+1, …, n+k). This is a partial result on JSP-000550 (Erdős Problem 677), not a solution.
The claim is novel only if no known result already covers this range or a wider one. "Known" includes results that
are published, recorded on the problem's page or forum, posted as preprints, or kept in repositories.

## 1. Status source (one request, no retry)

- URL: https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md
- Fetched: 2026-10-15T09:45:23Z (UTC), plain curl, User-Agent `V3R1T4S-research-bot`
- HTTP status: 200
- sha256: 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834. This matches the scout's fetch in
  claim/source/fetch_log.txt and the blob on the prize repository's main branch (commit fd8fa66a, 2026-10-14).
- JSP-000550, "Must two disjoint equal-length intervals of consecutive integers have different least common
  multiples?":
  - `| Current status | Open |`
  - `| Lean proof | No |`
  - The other rows are `| Eligible to claim | No |` and an empty `| Publication details |  |`.
- The catalog does not give the Erdős number. The mapping JSP-000550 = Erdős 677 comes from claim/CLAIM.md, and the
  problem description matches Erdős 677.

## 2. The problem's own page (one request, no retry)

- URL: https://www.erdosproblems.com/677
- Attempted: 2026-10-15T09:45:37Z (UTC), plain curl, same User-Agent.
- Result: the site sent no response (status 000). curl exited with code 56, "CONNECT tunnel failed, response 403":
  this machine's egress proxy refused the connection. The scout got the same result at 07:25:00Z.
- I did not retry and did not try mirrors, caches or other fetchers. The page's forum thread is on the same host, so
  it was not requested and was not read.

## 3. What I searched and what I found

| source | how / when (UTC) | finding |
|---|---|---|
| formal-conjectures `ErdosProblems/677.lean` | raw.githubusercontent.com, 09:46:20Z, HTTP 200, sha256 cc682a41950449c693578cdfc83060505bcd482abc12ab33233eaea483681bd0 (byte-identical to claim/source/fc_Erdos677.lean); main = 79eac378 (2026-10-15T08:35:37Z), read with git | Contains only `erdos_677` (`research open`, `sorry`) and the test lemma `lcmInterval_eq_example1` (M(4,3)=M(13,2) and M(3,4)=M(19,2); the two blocks have different lengths, so these are not counterexamples), plus "TODO: Add the other statements from the reference." There are no variants or solved sub-cases. The neighbouring 678.lean marks `erdos_678` as solved, but that is a different statement (`lcmInterval m (k+1) < lcmInterval n k`). |
| teorth/erdosproblems `data/problems.yaml` | raw.githubusercontent.com, 10:15:58Z, HTTP 200, sha256 f19b2f712cc7a64ebdbdd01ec8e2af32dc5b7ab67bf02c30002af9bb8067b15c | Entry 677: status `open` (last_update 2025-08-31), formalized `yes` (2025-12-02). This database records status only, not partial results, so it cannot replace the problem page. |
| prize repo pull requests | `git ls-remote` 09:46:20Z: 4521 `refs/pull/*/head`. Shallow fetches of #3543, #4846 and main. Blobless shallow fetch of all 4521 heads. The JSP-000550 entry was compared in all 252 distinct versions of `problems/catalog-0501-0600.md`, and 13,401 text blobs were grepped for JSP-000550, Erdős 677 and lcm-of-interval wording. | #3543 sets "Lean proof: Yes" and links `submissions/JSP-000550/Erdos550.lean`. That file proves only `Nat.Prime 2`, …, `550 % 3 = 1` and cites erdosproblems.com/550; it says nothing about lcm. #4846 sets "Lean proof: Yes" and links qzxuwenlong/jsp-lean-solutions@c67915b1 `jsp550.lean` (fetched 09:47:53Z, HTTP 200, sha256 18568b8adec7486a77554af0bf53888a803224c9efe73a751e7d4bd6082ee99d). That file is one `decide` theorem checking two instances: lcm{1,2,3}=6 ≠ lcm{4,5,6}=60 and lcm{2..5}=60 ≠ lcm{6..9}=504. #4288 points to plby/lean-proofs `Erdos550.lean`, which is Erdős Problem 550, a different problem. #4460 is a Jacobsthal note added to the JSP-000550 row by mistake (its title says JSP-000559). #2412 and #3298 (JSP-000677, a different catalog entry) add filler `Erdos677.lean` files (`True := trivial`, facts about primes); they cite erdosproblems.com/677 but state nothing about lcm. In #1–#5 the catalog used an older numbering in which JSP-000550 was another problem. In every PR, the status of the lcm problem is Open. None records a partial result or solution. |
| plby/lean-proofs | git, blobless shallow fetch of main (8822f7dd) | No `Erdos677` file. The only path containing "677" is a data chunk of Erdős 1038. |
| jaredwilder/erdos-proved-lemmas | raw README on branch `main` gave 404 at 10:15:59Z (not retried); read instead with a shallow git fetch of `master` (728bf79f, 2026-09-17) | `erdos677-k2-lcm-slice.md`: "complete k=2 slice: M(n,2)=(n+1)(n+2) is strictly increasing". The file itself says "This result is only the exact k=2 base case. Historical novelty is not claimed." It covers k = 2 for all n. That neither contains the claimed range nor is contained in it. |
| V3R1T4S TROPHY_CASE.md | read in full | 53 rows; none concerns Erdős 677, JSP-000550 or lcm. |
| V3R1T4S pull requests | `git ls-remote` 09:46:21Z: 156 `refs/pull/*/head`. Shallow fetch (depth 1, blobs ≤ 1 MB) of all heads plus main at 10:13:21Z. Grep (`git cat-file --batch`) of all 2,753 fetched blobs for 677, lcm, JSP-000550 and lcmInterval. | Nothing mentions Erdős 677 or JSP-000550. The lcm hits are unrelated (covering systems, Erdős–Moser, denominators in matrix schemes). The 16 blobs skipped by the size limit are data files (codes, graph edge lists, schemes, Lehmer logs, a tensor). |
| literature, last 24 months | web search tool, 8 queries | Cambie, arXiv:2410.09138 (2024), "Resolution of an Erdős' problem on least common multiples", answers the related question of whether a shorter block can have a larger lcm (Erdős 678-type), not 677. Also found, none about 677's equality question: arXiv:2501.10333 (Erdős 692), arXiv:2607.10431, and T. Tao's blog post of 2026-03-31 on products of consecutive integers. No computational verification of 677, no bound excluding n ≤ c·k, and no solution turned up. Search snippets gave only the statement of 677, not the page's list of partial results. |
| arXiv listings | export.arxiv.org API query at 10:17:15Z; arxiv.org abstract search at 10:17:41Z | Both blocked by the proxy (status 000, curl exit 56, CONNECT 403). Not retried. arXiv was covered only through search-engine results. |
| [Er79], [Er79d], [ErGr80] | not available on this machine | Not read. The only content seen is the paraphrase in the formal-conjectures docstring ("Erdős expected very few solutions for M(n,k)=M(m,l) … The only solutions he knew were …"). |

## 4. Call

Nothing I could read covers the claimed range:

- The status source says Open, so no full solution is recorded.
- formal-conjectures has no variant or solved sub-case.
- Every prize-repository PR that claims a "Lean proof" for JSP-000550 is either filler or checks two instances.
- The only partial result found, the k = 2 slice, is a different slice.
- The searches found no range verification and no theorem of the form n ≤ c·k.

Even so, I cannot confirm novelty. The problem's own page (erdosproblems.com/677) and its forum thread could not be
read; that is where partial results on this problem are recorded. arXiv listings could not be read directly either.
A remark such as "no counterexample with n ≤ C·k" for some C ≥ 5871, or for a wider region, would most likely be
recorded there, and it would defeat this claim. Such a remark cannot be ruled out in advance, because the method is a
natural one. The size bound of claim/object/PROOF.md (S1) gives m + k < 2.826·(C+1)·k. Any explicit
short-interval prime theorem then caps m for every fixed C; Dusart-type bounds can stand in for Schoenfeld's
1/16597. So "n ≤ C·k" reduces to a finite computation for any C, and a known result with a larger C is plausible.
Since I cannot show that the claim strictly beats everything known, and the default is to fail, I fail it.

novelty: PENDING STATUS CHECK

- Read: the status source (JSP-000550 Open, Lean proof No); formal-conjectures 677 at main; teorth/erdosproblems
  (677 open); all 4521 prize-repository PR heads; plby/lean-proofs; jaredwilder/erdos-proved-lemmas (k = 2 slice
  only); V3R1T4S TROPHY_CASE.md and all 156 V3R1T4S PR heads; 8 web searches.
- Not readable: erdosproblems.com/677 and its forum thread (proxy 403), the arXiv API and listing search (proxy 403),
  and the 1979–80 classical references.
- Human check by hand: read https://www.erdosproblems.com/677 and https://www.erdosproblems.com/forum/thread/677,
  and scan arXiv. The claim fails novelty if any recorded result already excludes counterexamples for every (n, k)
  with n ≤ 5871·k (or a superset of that range), or solves the problem. It passes only if it strictly extends
  everything recorded there.

pass: false
