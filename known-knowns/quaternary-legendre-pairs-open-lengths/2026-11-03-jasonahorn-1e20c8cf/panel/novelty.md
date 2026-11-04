context: subagent

# NOVELTY

Role: novelty skeptic. The object in claim/CLAIM.md is not a pair. It is an empty result: no quaternary Legendre pair of length 70 with both sequences constant on the orbits of either order-12 subgroup of (Z/70Z)* that does not contain -1, namely H1 = (1, 3, 9, 11, 13, 17, 27, 29, 33, 39, 47, 51) and H2 = (1, 9, 11, 23, 29, 37, 39, 43, 51, 53, 57, 67). A tie with a printed exhaustion of those two groups would fail. Lebedev's reversible queue and Kumar's Gaussian estimate are different objects.

## Status page, one GET, not retried

URL: https://arxiv.org/abs/2609.25573
Fetch time: 2026-11-03T07:50:04Z (header date: Tue, 03 Nov 2026 07:50:04 GMT)
HTTP status: 200
sha256 of the body: e8f65b7be0ac47c453feddab01a7875c01792a8d77681dd44bb89fa63d1764d2
Redirects: 0. No captcha, challenge, or access-denied page.

Quoted value, from the page itself: title "A Quaternary Legendre Pair of Length 64"; dateline "[Submitted on 22 Sep 2026 (v1), last revised 30 Oct 2026 (this version, v2)]"; author Harshit Verma; abstract "A quaternary Legendre pair of length ell is a pair of sequences over {±1, ±i} whose periodic autocorrelations sum to -2 at every nonzero shift. We give a quaternary Legendre pair of length 64. To the best of our knowledge, this is the first reported construction at this length."

That page does not mention length 70, does not give a pair of length 70, and does not name either subgroup. The live status value for the existence cell is a pair at 64, not a closure of 70. This claim does not compete with that pair.

injection_suspected: none on the status page. Footer links were not followed.

## What would already count as this result

A printed exhaustion of these two groups, or a short necessary condition that already empties them, is not new. A pair at 70 would overtake the claim, but none was found. An empty reversible queue is not this family: neither listed group contains -1 (69 mod 70), so the invariance is not reflection symmetry.

## Literature and code, last 24 months

arXiv HTML search for "quaternary Legendre", one GET, not the export API: https://arxiv.org/search/?query=quaternary+Legendre&searchtype=all&source=header
HTTP 200 at 2026-11-03T07:51:07Z. The page says "Showing 1-6 of 6 results". The six are 2609.25573 (Verma, length 64, announced September 2026), 2609.04589 (Lebedev, announced September 2026), 2408.16318 (revised 27 March 2025), 2408.08472 (revised 9 February 2025), 2212.10953 (2022), and 2105.13826 (a different quaternary-sequence paper, 2021). None of the six abstracts reports a pair at 70 or an exhaustion of these two groups. export.arxiv.org was not queried and was not retried.

Lebedev, https://arxiv.org/html/2609.04589v1, one GET, HTTP 200 at 2026-11-03T07:51:07Z, sha256 8a080247e6073c00033b35f97483ea3ce458adf9bcdc78c1ca16784bc6fcc8d0. Quoted: "In each case the object exhausted is the reversible factor-2 queue that the cost-ranked ladder constructed at that length, and in each case no pair was found." Length-70 row: queue ranks closed 170/170, exact hits examined 39,798, pairs found none. Quoted limit: "These results do not assert that no quaternary Legendre pair exists at 64, 70 or 76. They assert that a specific finite queue was searched exhaustively and yielded nothing." The HTML does not contain either group tuple, and the only multiplier remark is that the new witnesses at settled lengths have no simple multiplier explanation. That is not an exhaustion of H1 or H2.

Lebedev release, Zenodo record 21776795, one GET of the API, HTTP 200 at 2026-11-03T07:54:18Z. The description names two files and says the length-64, 70, and 76 exhaustions are reversible four-block queues, not nonexistence results. The release tarball (HTTP 200) contains certificates-length70.tar.gz. Its README says each certificate "shows that the reversible factor-2 queue recorded at its length was searched to exhaustion and yielded no pair. That is all it shows." The exact tuples "1, 3, 9, 11, 13, 17" and "1, 9, 11, 23, 29, 37", and the phrase "multiplier subgroup", are absent from the paper source, the README, and the length-70 certificate archive. "plant_orbit" files in that archive are a planted qualification of the reversible matcher, not these groups.

Kumar, https://raw.githubusercontent.com/vatskishan03/Hadamard/main/NOTES.md, one GET, HTTP 200 at 2026-11-03T07:51:07Z, sha256 371b9f8b529f0b17c62450482d47e53e4aca66b12db8d3e118932e8fd19c750c. Quoted open list: "Quaternary Legendre pairs (qLP; open lengths up to 100 after Lebedev and Verma 2026: 70, 76, 88, 92, 94 and 100)." The note says Lebedev exhausted the all-centres-at-0 family at 70, and that a mixed half-integer-centre Gray family is impossible at 70 because 71 is not a sum of two squares. That short obstruction is not these groups. The only multiplier remark at 70 is a Gaussian estimate, not an exhaustion: "At the open lengths every multiplier structure has a Gaussian estimate of 10^-2.2 or less: 70: 10^-4.4 (generated by 11)." The generator 11 has order 3, so that estimate is not H1 or H2. The companion script search/qlp_bin.py (HTTP 200, 2026-11-03T07:52:53Z) searches a different shape: binary A on H-orbits and reversible r, s on the orbits of the group generated by H and -1. It prints an estimate. It does not record an empty run of H1 or H2. search/sym_qlp.py stores only Verma's length-64 pair. search/NOTES.md (HTTP 200, same minute) discusses quaternary pairs as propus quadruples and does not exhaust these two groups. The Hadamard releases endpoint returned HTTP 200 and an empty list, so there is no release asset ahead of that tree.

Earlier papers in the window still list 70 as open and do not name these groups: Jedwab and Pender, arXiv:2408.08472v2, unresolved list includes 70; Kotsireas, Koutschan and Winterhof, arXiv:2408.16318, same open list. Web search for the two tuples together with "quaternary Legendre" and for an order-12 multiplier exhaustion at length 70 returned those papers, Lebedev, Verma, and unrelated multiplier searches (binary Legendre pairs of lengths 85 and 333). None prints this emptiness. Pender's April 2026 thesis is a construction paper, not this census.

## This repo

TROPHY_CASE.md: no match for quaternary or Legendre. known-knowns has no settled package for this target. The open problem statement in known-unknowns still lists 70 as open and names Lebedev's queues and Kumar's half-integer obstruction as the published negatives. GitHub issue search for this repository and "Legendre", HTTP 200 at 2026-11-03T07:52:05Z, total_count 2: pull 862 (least-qnr, open) and pull 148 (erdos-699, closed). Neither is a quaternary Legendre pair or this exhaustion.

GitHub code search for the Hadamard repository returned HTTP 401, "Requires authentication". Not retried. The public tree files above were read instead.

## Verdict

No accessible source prints an exhaustion of H1 or H2, and none prints a pair at length 70. Lebedev's empty reversible factor-2 queue (170/170, 39,798 hits) is a different family. Kumar's 10^-4.4 figure is an estimate for a binary-A search under the order-3 group generated by 11, not an exhaustion of these two groups. The half-integer-centre obstruction is a short condition on a different family. This empty multiplier family is not a tie with any of those, and it is not a trivial edit of a published pair. It does not settle length 70. Relative to everything found, the stated exhaustion is new.

pass: true
