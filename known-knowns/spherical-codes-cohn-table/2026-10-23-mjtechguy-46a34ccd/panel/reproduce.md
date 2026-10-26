context: fresh headless grok CLI session (grok -p) started in a copy of claim/ only, given the reproduce instruction

Definition, quoted from CRITERION.md:

"Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization' (improving an entry the table itself flags as unconverged is partial win p2, never a claim), AND the row is not superseded by a newer arXiv result for the same (d, N) (search arXiv for 'spherical code' / 'Tammes' and N), AND the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 the claim belongs to the bank target kissing-number-low-dim and is not counted here). Uploading to /upload-code is an external submission and is never done without explicit permission from the human; the claim is for the verified code."

CLAIM.md asserts d=25, N=650, object codes/650.txt, c* = 0.24253540410617579968405548728311276930607147141846 after unit normalization in mpmath at 50 digits, table cosine 0.242872702057, and difference 0.00033729795082420031594451271688723069392852858154. No upload was performed.

Independent checker, written from that definition before reading check_one.py or REPRODUCE.md. Every coordinate in codes/650.txt was parsed as an exact integer over 10^27 and checked against Decimal. All 650*649/2 = 210925 unordered pairs were compared by the exact positive-cosine test D1^2 * Na * Nb versus D2^2 * Ni * Nj. The winning pair was then normalized and dotted in mpmath 1.3.0 at 50 decimal digits (plain sum and fsum/fdot), and the same cosine was recomputed from the integers at 120 decimal places.

Object. codes/650.txt has sha256 46a34ccdab0275a1796b02defb0f5f2ddf28601d56e6d565d4366578b9adfc97, matching CLAIM.md and object_sha256.txt. It contains 650 lines, each with 25 scientific-notation coordinates, and all 16250 mantissas have 21 digits, so every coordinate is given to at least 20 digits. No zero vector. Raw Euclidean norms are not exactly 1 (about 1.00000000000000011377 and 1.00000000000000015538 on the maximizing pair), so the normalization step changes the value.

Exhaustive maximum. There is one maximizing pair, file lines 624 and 634 (0-based indices 623 and 633). Its exact cosine begins

0.242535404106175799684055487283112769306071471418461193626415268072571790623455343589022560567945540119564261771678215535

Rounded to 50 decimal places, and also the string returned by mpmath 1.3.0 at dps=50, this is

0.24253540410617579968405548728311276930607147141846

which is the value in CLAIM.md and expected_c.txt. The next digit of the exact expansion is 1, so that 50-digit string is the correctly rounded value. The same 50-digit string was produced by both the running sum and by fsum/fdot. A second full scan, the float64 Gram matrix of all 210925 pairs, selected this same unordered pair. The runner-up is lines 7 and 324, cosine

0.24253540375381564985327378361419681603985895585264405...

Exact gap 0.00000000035236014983078170... = 3.523601498307817e-10, which is greater than 1e-10, so the maximizer is unique by a margin far above mpmath-50 rounding.

Table comparison. The 12-decimal table value is the exact decimal 0.242872702057. Decimal subtraction gives

0.242872702057 - 0.24253540410617579968405548728311276930607147141846 = 0.00033729795082420031594451271688723069392852858154

exactly the claimed difference. That difference is greater than 1e-10. Using the unrounded cosine, the gap to the table is 0.00033729795082420031594451271688723069392852858153880..., still greater than 1e-10, and the cosine is strictly smaller than the table value. Direction is minimal cosine.

Live table. Two reads, both HTTP 200.

- https://spherical-codes.org/ at Fri, 23 Oct 2026 13:39:11 GMT, sha256 fbf0205438e42592554a58159f84b3959fa51812d94dc048a214c8136db2f97a
- https://spherical-codes.org/plain at Fri, 23 Oct 2026 13:39:12 GMT, sha256 e849b8b9ad506b8cba0e0a1355bb7012d4753a49bf95e55a3d7912d1da1da671
- https://spherical-codes.org/ at Fri, 23 Oct 2026 13:45:10 GMT, sha256 4b257dd7b982ddc7242036d4627fa57dec981dc44097ad4a6161036de2a732dd
- https://spherical-codes.org/plain at Fri, 23 Oct 2026 13:45:11 GMT, sha256 d06d94a311ac722efd622484bbeed7f535ac380ea68ea4c913d9358fba022856

Both plain bodies contain the line 25,650,0.242872702057 and no minimal polynomial on that line. Both HTML rows for the cell are

<tr> ... <td>25</td> ... <a href="/data/25/650">650</a> ... <td>0.242872702057</td> <td>Azmi C. &Ouml;zgen, 2026.</td> ... </tr>

That row contains no '&ast;' and does not contain the text "needs more optimization". The same cosine, star flag 0, and needs-more-optimization flag 0 are what table_rows.tsv records for N=650. The whole-page hashes differ between the two reads because another cell changed: plain line 20,646 moved from 0.296471328838 to 0.295495996341. CLAIM.md's index_sha256 8d1a74f0e86a6dddb07cc6824adfd182131f9afb7aef7edded8ba979699753a3 and plain_sha256 e4a938fbe884a5f1955b36a2fb8d3ca05430fcfcb1cbf1c683f698322f787b9b, dated Fri, 23 Oct 2026 13:25:02 GMT and 13:25:03 GMT, match neither body above. The (25, 650) cosine, the missing star, and the missing optimization flag were stable across both reads and match the claim. The verdict uses those cell values, not the unstable full-page hashes.

arXiv, read-only, no blocked response and no retry. API feed times are the <updated> stamps.

- https://export.arxiv.org/api/query?search_query=all:%22spherical+code%22+AND+all:650&start=0&max_results=30 at 2026-10-23T13:41:54Z, totalResults 0
- https://export.arxiv.org/api/query?search_query=all:Tammes+AND+all:650&start=0&max_results=20 at 2026-10-23T13:42:13Z, totalResults 0
- https://export.arxiv.org/api/query?search_query=all:%22spherical+codes%22+AND+all:650&start=0&max_results=20 at 2026-10-23T13:42:13Z, totalResults 0
- https://export.arxiv.org/api/query?search_query=all:spherical+AND+all:code+AND+all:650&start=0&max_results=15 at 2026-10-23T13:45:09Z, totalResults 1: arXiv:2102.00775v3, "Spiral structures in gravito-turbulent gaseous disks", updated 2021-03-30T07:45:31Z, journal reference A&A 650, A49 (2021). The 650 is a journal volume, not a 650-point code in dimension 25.
- Control https://export.arxiv.org/api/query?search_query=all:Tammes&start=0&max_results=1 at 2026-10-23T13:45:09Z returned totalResults 474, so the empty searches are real empty feeds.

No arXiv result found that supersedes (25, 650).

Exclusions. Kissing-number gate: 9 <= 25 <= 23 is false, so the configuration is not moved to kissing-number-low-dim, even though c* <= 0.5. Partial p1 is dimension 3 only. Partial p2 needs the row text "needs more optimization", which this row does not have. Partial p3 is an algebraic match at 1e-12; the gap here is about 3.372979508242003e-4, a strict numerical improvement.

Author proof, re-derived after the independent value was already in hand. check_one.py sums coordinates in Decimal at the default precision 28. That sum is 33.18447246934687818545449886 and equals expected_sum.txt. The exact sum at precision 80 is 33.184472469346878185454498863, which quantizes to the same 26-decimal value. Their exhaustive loop normalizes in Decimal at precision 50. Re-doing that arithmetic on the winning pair produces 0.24253540410617579968405548728311276930607147141845, which is 1e-50 below expected_c.txt and inside their 1e-48 agreement test. Running check_one.py reproduced its own full search: it printed c*=0.24253540410617579968405548728311276930607147141845, delta=0.00033729795082420031594451271688723069392852858155, the precision-28 coordinate sum, needs_more_optimization=0, star=0, and PASS. The claimed c* is the mpmath-50 value, which matches this independent mpmath run; the Decimal-50 result is one unit low in the last place and is not the number CLAIM.md states.

posted/650.txt is a different 650-by-25 file, sha256 3bf5dd68ae7a0b723494149896947cd340f3540b83e280ad1e837cc556042635, matching STATUS.md. Its shortest token has 13 digit characters. Its float64 maximum inner product is 0.2428727020567017. The printed table cosine sits above that float by 2.983e-13, which is not an improvement of 1e-10. The claim under test is codes/650.txt.

Every success condition in the definition holds for codes/650.txt against the live (25, 650) cell observed at the times above.

pass: true
