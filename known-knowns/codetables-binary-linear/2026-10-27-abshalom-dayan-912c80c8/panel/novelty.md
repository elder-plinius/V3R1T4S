# Novelty skeptic: [29,19,8] over GF(9) vs codetables.de (q,n,k) = (9,29,19)

**Bottom line: novel as far as I could check.** The live codetables.de cell reads lower bound 7, upper bound 9. A
[29,19,8] code beats 7 by +1 (strictly, not a tie) and stays within the upper bound 9. I found nothing that already gives
d >= 8 at (29,19): not the table's neighbouring cells under the standard rules, not this repo's TROPHY_CASE.md or
known-knowns folder, not its pull requests, and not the literature I could reach. Scope: this is a novelty verdict only.
It assumes the claimed distance d = 8 is correct, which is for the other skeptics to check (I ran none of the claim's
checkers). Three web sources could not be read (listed below).

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Fetch record (one plain GET, no retries)

| item | value |
|---|---|
| URL | https://codetables.de/BKLC/BKLC.php?q=9&n=29&k=19 |
| client | curl, User-Agent "V3R1T4S-research-agent (honest single fetch)" |
| fetched (UTC) | 2026-10-27T02:00:51Z (fetched/bklc_q9_n29_k19.time; server Date header: Tue, 27 Oct 2026 02:00:51 GMT) |
| HTTP status | 200, 3136 bytes (fetched/bklc_q9_n29_k19.result, headers in fetched/bklc_q9_n29_k19.headers) |
| sha256 | fe750485b053225286430c77f5fa80a4686c4ea13208407331b2a126f5f63cf3 (fetched/bklc_q9_n29_k19.sha256) |
| same as claim copy? | yes: byte-identical to claim/table/bklc_q9_n29_k19.html (`cmp` reported no difference, same sha256) |
| bounds, verbatim | `<H3>Bounds on linear codes [29,19] over GF(9)</H3><TABLE><TR><TD>lower bound:</TD><TD>7</TD></TR><TR><TD>upper bound:</TD><TD>9</TD></TR></TABLE>` |
| construction listed | [37,28,7] subcode of a punctured Reed-Solomon code over GF(81) (Xing-Ling), shortened to [29,20,7], subcode [29,19,7]; "last modified: 2001-12-17"; Ub(29,19) = 9 via Ub(21,11) = 9 (construction B), Brouwer's table as of 2007-02-13 |

Range page, one GET: https://codetables.de/BKLC/Tables.php?q=9&n0=28&n1=36&k0=1&k1=36, fetched 2026-10-27T02:01:00Z,
HTTP 200, 39292 bytes, sha256 5a413ef3c4e0b0049207c144c0dd01cfac053bfba30bfe8f76456e0229fc75fa
(fetched/range_q9_n28-36.*). It shows the (29,19) cell as `7-9`, the same as the cell page.

## Does the table itself already imply d >= 8 at (29,19)? No

I parsed all 288 cells of the range page (scripts/implied.py). From any [N,K,D] with K >= 19, shortening K-19 times
and puncturing (N-K)-10 times gives a [29,19,D-(N-K-10)] code. Taking a subcode, or adding a zero column from n = 28,
covers the remaining standard rules. The best value any cell implies at (29,19) is **7**: 21 cells reach 7 and none
reaches 8.

| cell | table | what it gives at (29,19) |
|---|---|---|
| (30,20) | 7-9 | shorten: [29,19,7] |
| (30,19) | 8-10 | puncture: [29,19,7] |
| (29,20) | 7-9 | subcode: [29,19,7] |
| (28,19) | 7-9 | zero column: [29,19,7] |
| (28,18) | 8-9 | no standard rule raises k (lengthening is not a table rule) |
| (31,21), (32,22), ..., (36,26) | 7-9 each | shorten: 7 |
| (31,20), (32,21), ..., (36,25) | 8-10 each | shorten, then puncture once: 7 |
| (31,19), (32,20), ..., (36,24) | 9-11 each | shorten, then puncture twice: 7 |

A [30,20,8], [30,19,9], [29,20,8] or [28,19,8] code would each imply the claim. The table lists none of them.

## Repo (github.com/elder-plinius/V3R1T4S), GitHub API, one GET per query, all HTTP 200, 2026-10-27T02:02:02Z to 02:03:47Z

- **TROPHY_CASE.md** (blob 571f2411..., 31235 bytes): it has no codetables, GF(9) or linear-code row. The families
  it lists are degree-diameter graphs, matrix multiplication, VNN-COMP, constant-weight codes and others. Nothing at
  (29,19).
- **known-knowns/codetables-binary-linear/**: four entries, read from their INDEX.csv files:
  - q=2 [173,17,72]
  - q=2 [175,25,61]
  - q=2 [213,26,77]
  - q=9 [31,18,10] (2026-10-24-abshalom-dayan-0dc7555b, pull request #644, merged)

  The [31,18,10]_9 code has k = 18, so shortening, puncturing and subcodes cannot reach k = 19. Its best derivative is
  [29,18,8], which says nothing at (29,19). It is a different code: C(D,17P) inside C(D,20P) with a [4,3] tail, not the
  claim's C(D,19P) inside C(D,21P) with a 2-column tail. The range page still shows (31,18) as 9-12, so the table has
  not absorbed it.
- **Pull requests**: I read the 100 most recent (state=all) and ran search queries for "codetables-binary-linear"
  (46 hits), "GF(9)" (21), "q=9" (10), "Hermitian" (20) and "29,19" (**0 hits**). None claims a [29,19,>=8]_9 code or
  any GF(9) code with k >= 19.
- **Qutrit EAQECC pull requests**: I read the bodies of #643, #645, #646, #651, #728, #721, #726, #710, #729 and #727.
  The classical GF(9) codes they name, with distances, are:
  - [28,11,15], [28,12,14], [28,14,12], [28,15,11], [28,13,13], [28,10,16], [28,6,20], [28,9,17] (length-28 Hermitian)
  - [27,15,11], [33,13,16], [33,14,15], [33,15,14], [33,9,20], [35,14,16], [37,15,17]
  - small tails [5,3,3] and [7,4,4]

  Every one has k <= 15, so none reaches k = 19 by the standard rules. The length-28 family [28,k,26-k] gives [28,19,7]
  at k = 19, a tie with the table. I did not open those pull requests' file lists. Their bodies quote no
  higher-dimension code with a distance.

## Literature and other databases

- **LinCodeEvolve, arXiv:2609.37056** (abstract fetched 2026-10-27T02:04:59Z, HTTP 200): binary codes only. Its seven
  codes are [172,21,66] through [200,21,77]. Nothing over GF(9).
- **Chen & Wu, arXiv:2401.06184** (Jan 2024, slightly older than 24 months): cyclic and negacyclic codes over F9 and
  other fields, "optimal or best known", so at most ties. I also checked that no constacyclic code of length 29 over
  GF(9) can have dimension 19 at all (scripts/constacyclic_dims.py: the cyclotomic coset sizes are 1, 14, 14 for every
  constant), so no cyclic, negacyclic or constacyclic [29,19]_9 code exists.
- **arXiv:2509.03337** "New Bounds for Linear Codes with Applications" (fetched, HTTP 200): it gives weight-restriction
  bounds and constructs no codes.
- **Web searches** (exact "[29,19,8]" with GF(9); new GF(9) codes improving codetables.de 2025-2026; Hermitian /
  Construction X over GF(9); quasi-twisted and quasi-cyclic codes over F9; arXiv F9 best-known 2026): no source gives a
  [29,19,>=8]_9 code. The only recent GF(9) record found is this repo's own [31,18,10] (pull request #644).
- **Older sources the table may have missed**:
  - Xing-Ling codes are the table's own construction for this cell.
  - Daskalov-Metodieva-Hristov (2004, 31 new GF(9) codes) and Daskalov-Kapralov (2001, quasi-cyclic codes of dimension
    7 and 8) work at low dimension.
  - Bierbrauer-Gulliver, "New linear codes over F9", Australasian Journal of Combinatorics 21 (2000): the page lists no
    parameters.
  - Couvreur's [91,18,53]_9 has a different length.
  - None gives (29,19).
- **Hermitian-curve reasoning (mine, not a source)**:
  - The curve y^3+y = x^4 over GF(9) has genus 3 and 28 rational places. Plain one-point codes give [27,19,>=6] (m = 21).
  - The 28-point version gives [28,19,>=7]. The 28-point [28,18,8] (m = 20) is not a subcode of the 28-point m = 21
    code, because the evaluation at the point at infinity is normalised differently. So the textbook Construction X
    with a [1,1,1] tail does not apply.
  - The curve has no degree-2 places over GF(9): N_2 = 81+1-6*9 = 28 = N_1. So Xing-Ling lengthening by degree-2
    places is unavailable.
  - Feng-Rao improved Hermitian codes for designed distance 8 still need 10 checks at length 27 (order-bound values
    1,2,2,3,4,3,4,6,6,7 for s = 0..12 in the semigroup <3,4>), giving [27,17,8], the same as the one-point code.
  - None of these routes gives [29,19,8].

## Could not read (no retries, no workaround)

- arXiv export API, two queries (2026-10-27T02:05:47Z): HTTP **429** and HTTP **503**. I stopped there. arXiv was
  covered only through web search and two abstract pages.
- MinT database (https://mint.sbg.ac.at/, 2026-10-27T02:04:59Z): connection failed (curl exit 7, HTTP code 000).
- Y. Edel's GF(9) code-matrix index (mathi.uni-heidelberg.de, 2026-10-27T02:04:24Z): TLS certificate name mismatch
  (curl exit 60, HTTP code 000). I did not bypass certificate checking.
- The Magma BKLC database (mirrored by codetables.de) is not openly queryable.
- injection_suspected: none seen in any fetched page.

## Verdict

The table reads lower bound 7 and upper bound 9. Claimed d = 8 > 7 (strict, not a tie) and 8 <= 9. Nothing found
reaches d >= 8 at (29,19). Novel at the time of the check, provided the claim's d = 8 holds.

pass: true
