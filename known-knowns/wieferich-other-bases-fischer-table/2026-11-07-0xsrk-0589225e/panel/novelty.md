role: NOVELTY
context: hermes delegation (delegate_task subagent, fresh context, saw only claim/)

# Novelty: Wieferich pair (17766, 1016845912283), target wieferich-other-bases-fischer-table, partial win p1

novelty: NEW PAIR, not a tie and not a trivial variant of anything published. The pair (b, p) = (17766, 1016845912283), with 17766 = 2·3^3·7·47 not a perfect power, is absent from every source checked. Re-fetched once each with the honest User-Agent, no block met: FermQ_Sorg.txt http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt at 2026-11-07T18:34:23Z, HTTP 200, sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4; FermQ_Sort.txt http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt at 2026-11-07T18:34:23Z, HTTP 200, sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b; ErstBasen.txt http://www.fermatquotient.com/FermatQuotienten/ErstBasen.txt at 2026-11-07T18:34:24Z, HTTP 200, sha256 e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820; ErstPBasen.txt http://www.fermatquotient.com/FermatQuotienten/ErstPBasen.txt at 2026-11-07T18:34:24Z, HTTP 200, sha256 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 (all four byte-identical to the scout's copies in claim/inputs); OEIS search https://oeis.org/search?q=1016845912283&fmt=data at 2026-11-07T18:34:24Z, HTTP 200, sha256 3b751a6a9b1dd9316a8d9ae5d191fd88933026cf83d6a6de250a3645e61563e5, which answers "Sorry, but the terms do not match anything in the table." Primary table value for the cell: none. Base 17766 has no row (FermQ_Sorg.txt tabulates bases 2..10125, searched to 4.8E+12; FermQ_Sort.txt tabulates 2..1052 and 65537). The decimal string of p occurs in none of the four files, nor in Fischer's six other Fermat-quotient files, and 17766 occurs only inside longer numbers. No trivial edit or propagation rule reaches the pair from published work. Every such rule (powers, products and quotients through the additive Fermat quotient, negation or inversion mod p^2, restriction of a list) needs a published pair with the same p, and an exhaustive test of all bases 2..65537 finds 17766 alone for this p. The pair is neither a mod p^3 pair nor a double pair. The only published pairs in the cell (in Fischer's extreme-first-bases files) have perfect-power bases and other primes. In the repository, TROPHY_CASE.md, known-knowns/ (30 folders, none for this target), the target's known-unknowns page, bank/targets.json, 200 pull requests (#785 to #998, state=all), the issue/PR search and the releases (none) contain neither number. The two earlier claims of this target, #973 (24766, 1000747824697) and #983 (28910, 1011548897263), are different pairs: different primes, no Wieferich relation either way, and p lies outside both of their published sieve blocks. Web searches of the last 24 months of literature and code found neither number. Caveats: OEIS search does not index b-files, and GitHub's search index can lag. Verdict: the pair is strictly new in its cell, so it passes.

Scratch directory: work-novelty holds every fetched page, the analysis scripts and their outputs (out_*.txt).
Inputs read: claim/claim.md, claim/object/pair.json, claim/status_sources.md, claim/REPRODUCE.md, claim/verify.py
and the copies in claim/inputs/. Nothing else on the machine was read. The only look outside claim/ and
work-novelty was one directory listing of the run folder (names only), and no skill or memory was loaded.

## 1. Status sources, re-fetched once each (honest User-Agent, no retries, no block met)

User-Agent on every request: `V3R1T4S-agent/1.0 (open-research notebook; one honest request)`. Each URL was fetched
with one `curl -sS -L -A "$UA" -D hdr_FILE -o FILE -w 'http_code=%{http_code} num_redirects=%{num_redirects} ...' URL`,
after `date -u`, followed by `sha256sum FILE`. Output (work-novelty/fetch_log.txt):

```text
URL: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt
UTC: 2026-11-07T18:34:23Z
http_code=200 num_redirects=0 url_effective=http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt size_download=288459
curl_exit=0
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 *FermQ_Sorg.txt

URL: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt
UTC: 2026-11-07T18:34:23Z
http_code=200 num_redirects=0 url_effective=http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt size_download=33141
curl_exit=0
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b *FermQ_Sort.txt

URL: http://www.fermatquotient.com/FermatQuotienten/ErstBasen.txt
UTC: 2026-11-07T18:34:24Z
http_code=200 num_redirects=0 url_effective=http://www.fermatquotient.com/FermatQuotienten/ErstBasen.txt size_download=115771
curl_exit=0
e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 *ErstBasen.txt

URL: http://www.fermatquotient.com/FermatQuotienten/ErstPBasen.txt
UTC: 2026-11-07T18:34:24Z
http_code=200 num_redirects=0 url_effective=http://www.fermatquotient.com/FermatQuotienten/ErstPBasen.txt size_download=81696
curl_exit=0
3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 *ErstPBasen.txt

URL: https://oeis.org/search?q=1016845912283&fmt=data
UTC: 2026-11-07T18:34:24Z
http_code=200 num_redirects=0 url_effective=https://oeis.org/search?q=1016845912283&fmt=data size_download=6737
curl_exit=0
3b751a6a9b1dd9316a8d9ae5d191fd88933026cf83d6a6de250a3645e61563e5 *oeis_search_p.txt
```

Selected response headers (work-novelty/hdr_*.txt):

```text
hdr_FermQ_Sorg.txt: HTTP/1.1 200 OK|Date: Sat, 07 Nov 2026 18:34:22 GMT|Last-Modified: Wed, 21 Oct 2026 05:59:16 GMT|Content-Length: 288459|Content-Type: text/plain|
hdr_FermQ_Sort.txt: HTTP/1.1 200 OK|Date: Sat, 07 Nov 2026 18:34:23 GMT|Last-Modified: Wed, 21 Oct 2026 05:59:05 GMT|Content-Length: 33141|Content-Type: text/plain|
hdr_ErstBasen.txt: HTTP/1.1 200 OK|Date: Sat, 07 Nov 2026 18:34:23 GMT|Last-Modified: Sat, 27 Sep 2025 12:51:33 GMT|Content-Length: 115771|Content-Type: text/plain|
hdr_ErstPBasen.txt: HTTP/1.1 200 OK|Date: Sat, 07 Nov 2026 18:34:24 GMT|Last-Modified: Sat, 27 Sep 2025 12:51:39 GMT|Content-Length: 81696|Content-Type: text/plain|
hdr_oeis_search_p.txt: HTTP/1.1 200 OK|Date: Sat, 07 Nov 2026 18:34:24 GMT|Content-Type: text/html; charset=utf-8|
```

The four Fischer files are byte-identical to the scout's copies (`cd claim && sha256sum inputs/*.txt`, to compare
with the hashes above and in claim/status_sources.md):

```text
e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 *inputs/ErstBasen.txt
3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 *inputs/ErstPBasen.txt
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 *inputs/FermQ_Sorg.txt
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b *inputs/FermQ_Sort.txt
```

The OEIS reply is an ordinary result page, not a challenge page. Its visible text, and the only occurrence of the
word "challenge" (the Cloudflare script path that is embedded in normal pages), from `python3 oeis_text.py`:

```text
1016845912283 - OEIS login The OEIS is supported by the many generous donors to the OEIS Foundation . Winners in the A400K Celebration Hints (Greetings from The On-Line Encyclopedia of Integer Sequences !) Search: 1016845912283 Sorry, but the terms do not match anything in the table. Search completed in 0.000 seconds Lookup Welcome Wiki Register Music Plot 2 Demos Index WebCam Contribute Format Style Sheet Transforms Superseeker Recents The OEIS Community Maintained by The OEIS Foundation Inc. Last modified November 7 13:12 EST 2026. Contains 401120 sequences. License Agreements, Terms of Use, Privacy Policy
raw-HTML occurrence of "challenge": "e){o=''}}var u='/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray=a56e6e"
```

## 2. Primary table value for the cell

FermQ_Sorg.txt (the bank's status source) and FermQ_Sort.txt were both fetched at 2026-11-07T18:34:23Z (records
above). Output of `python3 table_cell.py`:

```text
FermQ_Sorg.txt: limit lines ['Die Basen sind gegenwaertig durchsucht bis 4.8E+12']
   base rows: 10000, smallest 2, largest below 65537: 10125, row for 65537: 'none'
   rows with 10125 < base < 65537: []; row for 17766: 'none'
   signature line: '21.10.2026  Richard Fischer'
FermQ_Sort.txt: limit lines ['Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14', 'Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13']
   base rows: 982, smallest 2, largest below 65537: 1052, row for 65537: '65537  P: 2^16, 3, 131, 151, 163 (>1.2E+14)'
   rows with 10125 < base < 65537: []; row for 17766: 'none'
   signature line: '21.10.2026  Richard Fischer'
```

Value: base 17766 has no row in either table. FermQ_Sorg.txt rows are the 10000 non-perfect-power bases 2..10125,
searched to 4.8E+12. FermQ_Sort.txt rows are 2..1052 plus 65537. So the table value for the cell is none.

## 3. Raw-text search for the base and for the decimal string of p

`python3 search_fischer.py` reads the four Fischer files and the OEIS page. It searches p as a plain substring,
with optional separators between digits, and as any number between 1.0168e12 and 1.0169e12. The six hits on the
OEIS page are the page echoing the query:

```text
FermQ_Sorg.txt: raw substring '1016845912283' x0; with-separators regex x0; token 17766 x0; substring '17766' x1; integer tokens in [1.0168e12,1.0169e12]: [1016812692871]; integer tokens > 1e12: 572
   context: '41293 |   233,  2^3, 3, 11, 157, 86735239 |   234,  19, 46441, 817766595407 |   235,  3, 31, 118022689 |   236,  29, 229 |   237,  2 |   '
FermQ_Sort.txt: raw substring '1016845912283' x0; with-separators regex x0; token 17766 x0; substring '17766' x1; integer tokens in [1.0168e12,1.0169e12]: []; integer tokens > 1e12: 158
   context: '293 |  233  P: 2^3, 3, 11, 157, 86735239 |  234  P: 19, 46441, 817766595407 |  235  P: 3, 31, 118022689 |  236  P: 29, 229 |  237  P: 2'
ErstBasen.txt: raw substring '1016845912283' x0; with-separators regex x0; token 17766 x0; substring '17766' x0; integer tokens in [1.0168e12,1.0169e12]: []; integer tokens > 1e12: 431
ErstPBasen.txt: raw substring '1016845912283' x0; with-separators regex x0; token 17766 x0; substring '17766' x1; integer tokens in [1.0168e12,1.0169e12]: []; integer tokens > 1e12: 188
   context: '674953831, 171031732897, 172994868509, |        174996058519, 177662317837, 217635533729) |  2  P: 1194789287  PB: 9161, 11935588'
oeis_search_p.txt: raw substring '1016845912283' x6; with-separators regex x6; token 17766 x0; substring '17766' x0; integer tokens in [1.0168e12,1.0169e12]: [1016845912283]; integer tokens > 1e12: 6
FermQ_Sorg.txt scientific 1.01..E12 mentions: []
FermQ_Sort.txt scientific 1.01..E12 mentions: []
ErstBasen.txt scientific 1.01..E12 mentions: []
ErstPBasen.txt scientific 1.01..E12 mentions: []
```

Fischer's site index and his six other Fermat-quotient files were each fetched once (work-novelty/fq_index_log.txt
and fq_extra_log.txt):

```text
URL: http://www.fermatquotient.com/
UTC: 2026-11-07T18:38:01Z
http_code=200 num_redirects=0 url_effective=http://www.fermatquotient.com/ size_download=16104
curl_exit=0
42508627832b9d654ea777db3c10126d558bf7bf13c21c07c5b74452b8e84fd1 *fermatquotient_index.html

URL: http://www.fermatquotient.com/FermatQuotienten/News.txt
UTC: 2026-11-07T18:38:19Z
http_code=200 num_redirects=0 size_download=8500
curl_exit=0
1970fbe5188e93b0fa0381beac91b0654b18c9491043bbdb42e256bc7f6080e7 *News.txt
Last-Modified: Mon, 01 Sep 2025 16:07:15 GMT

URL: http://www.fermatquotient.com/FermatQuotienten/FermatQ3.txt
UTC: 2026-11-07T18:38:19Z
http_code=200 num_redirects=0 size_download=11274
curl_exit=0
022855e8d16257ca4931bd9f7f9133012f17bbf1bc528f9a6cd12995b02a0a41 *FermatQ3.txt
Last-Modified: Sat, 14 Oct 2023 16:13:58 GMT

URL: http://www.fermatquotient.com/FermatQuotienten/SwitchFermQ.txt
UTC: 2026-11-07T18:38:19Z
http_code=200 num_redirects=0 size_download=10726
curl_exit=0
8190a7ca0bf2a31d9b03b77e97e5d09f45abc8b7df6f4321d706732b329f3faa *SwitchFermQ.txt
Last-Modified: Tue, 10 Jun 2025 21:06:21 GMT

URL: http://www.fermatquotient.com/FermatQuotienten/Statistik.txt
UTC: 2026-11-07T18:38:20Z
http_code=200 num_redirects=0 size_download=24222
curl_exit=0
dde1fa8d6c6105a74895dfb64646b7b74cb327a15aa7c49695f1c58ebabd2b2b *Statistik.txt
Last-Modified: Wed, 21 Oct 2026 05:59:22 GMT

URL: http://www.fermatquotient.com/FermatQuotienten/PQuotient_Sort.txt
UTC: 2026-11-07T18:38:20Z
http_code=200 num_redirects=0 size_download=28364
curl_exit=0
375de4557fcf0569bf80040532606e7e2c1f9e7f2101d9878bc947ce95dce864 *PQuotient_Sort.txt
Last-Modified: Fri, 07 Oct 2022 08:27:41 GMT

URL: http://www.fermatquotient.com/FermatQuotienten/Generelles.txt
UTC: 2026-11-07T18:38:20Z
http_code=200 num_redirects=0 size_download=8011
curl_exit=0
418d7557fa5bd72192af394901187e5f8d0b18826e1dd63b13988bb0cfae3e69 *Generelles.txt
Last-Modified: Sat, 04 Sep 2010 21:36:54 GMT
```

`python3 extra_files.py`:

```text
News.txt: p x0, p-with-separators x0, token 17766 x0, substring 17766 inside: []
FermatQ3.txt: p x0, p-with-separators x0, token 17766 x0, substring 17766 inside: []
SwitchFermQ.txt: p x0, p-with-separators x0, token 17766 x0, substring 17766 inside: []
Statistik.txt: p x0, p-with-separators x0, token 17766 x0, substring 17766 inside: ['4, 817766595407 (']
PQuotient_Sort.txt: p x0, p-with-separators x0, token 17766 x0, substring 17766 inside: []
Generelles.txt: p x0, p-with-separators x0, token 17766 x0, substring 17766 inside: []
fermatquotient_index.html: p x0, p-with-separators x0, token 17766 x0, substring 17766 inside: []
b^(p-1) == 1 mod p^3 (FermatQ3 condition): False
p^(b-1) == 1 mod b^2 (double pair, SwitchFermQ condition): False
```

## 4. Trivial edits and propagation rules (same-p analysis)

Every rule that turns published pairs into a new pair works within one prime p: b to b^k, products and quotients
through the additivity q_p(ab) = q_p(a) + q_p(b) mod p, b to p^2 - b or to the inverse of b mod p^2, and deletion or
restriction of a published list. So each needs a published pair with this same p. An exhaustive test of every
base 2..65537 for this p finds 17766 alone. That is consistent with p's absence from FermQ_Sorg.txt, which is
complete for bases 2..10125 up to 4.8E+12, a bound above p. `python3 bases_for_p.py`:

```text
bases a in [2, 65537] with a^(p-1) == 1 mod p^2: [17766] (0.3s)
17766 == 2*3**3*7*47: True
q_p(2) mod p = 445933708628
q_p(3) mod p = 15748556942
q_p(7) mod p = 449860086901
q_p(47) mod p = 73806445928
q_p(2)+3q_p(3)+q_p(7)+q_p(47) mod p = 0 ; q_p(17766) = 0
earlier pair (24766, 1000747824697): pow(b, p-1, p^2) == 1 -> True; same p as claim: False; does 17766 pass for p2: False; does 24766 pass for claim p: False
earlier pair (28910, 1011548897263): pow(b, p-1, p^2) == 1 -> True; same p as claim: False; does 17766 pass for p2: False; does 28910 pass for claim p: False
```

Negation and inversion mod p^2 send 17766 to bases far outside every table (`python3 symmetry.py`):

```text
p^2 = 1.0340e+24; p^2 - b = 1.0340e+24; b^-1 mod p^2 = 3.4495e+23
both Wieferich for p: True True | both above 65537: True
```

Fischer's two extreme-first-bases files list published pairs in this cell (bases 10126 to 65536, p above 1e12). All of
them have perfect-power bases, which the cell excludes, and none has this p (`python3 cell_pairs.py`):

```text
ErstBasen.txt pairs with base in 10126..65536 and p above 1e12: [(12100, 1219715607577, '110^2', True), (19321, 1822333408543, '139^2', True), (64000, 7036306088681, '40^3', True), (12100, 14438374183481, '110^2', True), (12167, 2549536629329, '23^3', True), (10648, 9809862296159, '22^3', True)]
   any with p == claim p: False ; any non-perfect-power base: []
ErstPBasen.txt pairs with base in 10126..65536 and p above 1e12: []
   any with p == claim p: False ; any non-perfect-power base: []
```

The pair is neither a mod p^3 pair (FermatQ3.txt) nor a double pair (SwitchFermQ.txt); see the last two lines of
the extra_files.py output in section 3. It is not seeded from a published object, because no published object
shares its p, so there is no seed to name.

## 5. The V3R1T4S repository (public data, plain unauthenticated GETs)

Requests (work-novelty/gh_fetch_log1.txt to gh_fetch_log5.txt):

```text
URL: https://api.github.com/repos/elder-plinius/V3R1T4S
UTC: 2026-11-07T18:36:01Z
http_code=200 num_redirects=0 size_download=5400
curl_exit=0
b0a749bd13179087835aabe982346e65f1ed0cca23af6cb1cc753ba1d3e6dcad *gh_repo.json
X-RateLimit-Remaining: 58

URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&sort=created&direction=desc&per_page=100&page=1
UTC: 2026-11-07T18:36:02Z
http_code=200 num_redirects=0 size_download=1917438
curl_exit=0
61d90228dd09f3efeca58c03e98679f848c8e10d3b0a326f073ad7a5f19c4f03 *gh_pulls_p1.json
X-RateLimit-Remaining: 57

URL: https://api.github.com/repos/elder-plinius/V3R1T4S/releases?per_page=100
UTC: 2026-11-07T18:36:04Z
http_code=200 num_redirects=0 size_download=2
curl_exit=0
4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 *gh_releases.json
X-RateLimit-Remaining: 56

URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&sort=created&direction=desc&per_page=100&page=2
UTC: 2026-11-07T18:36:32Z
http_code=200 num_redirects=0 size_download=1973431
curl_exit=0
9a50b336f7331618c7e461cab0e75d356beca71ea1b1826178b262b2bce9be0a *gh_pulls_p2.json
X-RateLimit-Remaining: 55

URL: https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns?ref=main
UTC: 2026-11-07T18:36:34Z
http_code=200 num_redirects=0 size_download=26227
curl_exit=0
305aaee9a1e826dd285d23e0852d1106eec5d8bd56ea17e94713939a94c6e528 *gh_known_knowns.json
X-RateLimit-Remaining: 54

URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
UTC: 2026-11-07T18:36:34Z
http_code=200 num_redirects=0 size_download=31306
curl_exit=0
83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 *TROPHY_CASE.md

URL: https://api.github.com/search/issues?q=wieferich%20repo:elder-plinius/V3R1T4S&per_page=100
UTC: 2026-11-07T18:36:57Z
http_code=200 num_redirects=0 size_download=12188
curl_exit=0
674b65dfcb45a81ea6f1480e0b1a56f42a65aaedefb8989d432f9bab16d84609 *gh_search_wieferich.json
X-RateLimit-Remaining: 9

URL: https://api.github.com/search/issues?q=17766%20repo:elder-plinius/V3R1T4S&per_page=100
UTC: 2026-11-07T18:36:57Z
http_code=200 num_redirects=0 size_download=79
curl_exit=0
c9938edecb99d754b2d039ac9eec320a94c769b6a6417921e2dcbef9e2fe01a0 *gh_search_17766.json
X-RateLimit-Remaining: 8

URL: https://api.github.com/search/issues?q=1016845912283%20repo:elder-plinius/V3R1T4S&per_page=100
UTC: 2026-11-07T18:36:58Z
http_code=200 num_redirects=0 size_download=79
curl_exit=0
c9938edecb99d754b2d039ac9eec320a94c769b6a6417921e2dcbef9e2fe01a0 *gh_search_p.json
X-RateLimit-Remaining: 7

URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/973/files?per_page=100
UTC: 2026-11-07T18:36:58Z
http_code=200 num_redirects=0 size_download=127263
curl_exit=0
dd0a8ac346174a51e019b1b7c018c08a0b205f8f077185628e16188f1c3d8dbb *gh_pr973_files.json
X-RateLimit-Remaining: 53

URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/983/files?per_page=100
UTC: 2026-11-07T18:36:59Z
http_code=200 num_redirects=0 size_download=155485
curl_exit=0
9ba6172b4153f6488202980f3eba1a2bf6fb39b8a070d02c64a7d67a97199fe4 *gh_pr983_files.json
X-RateLimit-Remaining: 52

URL: https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1
UTC: 2026-11-07T18:38:43Z
http_code=200 num_redirects=0 size_download=2167895
curl_exit=0
93b7eef8c4a599e1c8925507d9f8ad7dbb3e982741af87c745c69000d6d73625 *gh_tree_main.json
X-RateLimit-Remaining: 51

URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-unknowns/number-hunts/wieferich-other-bases-fischer-table.md
UTC: 2026-11-07T18:38:55Z
http_code=200 num_redirects=0 size_download=5492
curl_exit=0
8395b2fe8a39df3816c850ea9279ab8931e3e3655b4b7ad69c7e437b8f520d52 *ku_wieferich-other-bases-fischer-table.md

URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json
UTC: 2026-11-07T18:38:56Z
http_code=200 num_redirects=0 size_download=6189749
curl_exit=0
c2ee5ddad1634104acc41512e052dd4ab2c3af70d26cae8bc82f3af0bf6be65e *bank_targets.json
```

`python3 scan_pulls2.py` covers two pages of pull requests (state=all, newest first, per_page=100), the issue/PR
search, the releases, known-knowns/, the main tree, TROPHY_CASE.md, the target's known-unknowns page,
bank/targets.json, and the files of PR 973 and PR 983:

```text
PRs listed: 200 | numbers 998 down to 785 | created 2026-10-27T01:17:17Z to 2026-11-07T18:24:27Z
  #983 [open] 2026-11-07T16:47:06Z: [claim] wieferich-other-bases-fischer-table: Wieferich pair (28910, 1011548897263), partial win p1
  #973 [open] 2026-11-07T13:02:22Z: [claim] wieferich-other-bases-fischer-table: Wieferich pair (24766, 1000747824697), partial win p1
  PR titles/bodies containing 17766: 0
  PR titles/bodies containing 1016845912283: 0
gh_search_wieferich.json: total_count=2 incomplete_results=False items=[983, 973]
gh_search_17766.json: total_count=0 incomplete_results=False items=[]
gh_search_p.json: total_count=0 incomplete_results=False items=[]
releases: []
known-knowns/ entries: 30 | any named wieferich*: []
main tree: 06b61ea410a5ee90f3c9377a01d468c7cf05c0bd truncated: False entries: 7190 | paths containing 'wieferich': ['known-unknowns/number-hunts/wieferich-base-2-beyond-2-64.md', 'known-unknowns/number-hunts/wieferich-other-bases-fischer-table.md']
TROPHY_CASE.md: '17766' x0, '1016845912283' x0, 'ieferich' x0
ku_wieferich-other-bases-fischer-table.md: '17766' x0, '1016845912283' x0, 'ieferich' x10
bank_targets.json: '17766' x0, '1016845912283' x0, 'ieferich' x26
gh_pr973_files.json: 23 files, any patch omitted: False; '1016845912283' x0; '17766' x2 (contexts: ['(17766, 141121),'])
gh_pr983_files.json: 23 files, any patch omitted: False; '1016845912283' x0; '17766' x2 (contexts: ['(17766, 141121),'])
```

The two earlier claims of this target, by the same contributor, are different pairs. Their primes differ, neither
base is Wieferich for the other prime (section 4), and the claimed p lies outside both published sieve blocks, so it
does not contradict their hit lists (`python3 pr_blocks.py`):

```text
PR 973: object {'target_id': 'wieferich-other-bases-fischer-table', 'partial_win': 'p1', 'b': 24766, 'p': 1000747824697}; block [1000740000000, 1000760000000) hits [[24766, 1000747824697]]; claimed p inside this block: False; same p: False; same base: False
PR 983: object {'target_id': 'wieferich-other-bases-fischer-table', 'partial_win': 'p1', 'b': 28910, 'p': 1011548897263}; block [1011540000000, 1011560000000) hits [[28910, 1011548897263]]; claimed p inside this block: False; same p: False; same base: False
```

The only mention of base 17766 in those PRs is the small pair (17766, 141121) in a pipeline self-test window. That
is another pair, with a different prime below 1e12, and it does not propagate to this one.

## 6. Literature and code, last 24 months (web search)

I ran nine web searches: the decimal string of p, the base with Wieferich or Fermat quotient, recent searches for
Wieferich primes to large bases, GitHub code, and arXiv 2025-2026. I also extracted four pages:
OrygnsCode/wieferich-base-search (a June 2026 GPU search over 27 bases, all at most 986, with no releases), arXiv
2609.13904 and 2607.29329 (generalized Wieferich primes, 2026), and arXiv 2506.17684 (Fermat-quotient statistics,
2025). They are saved as work-novelty/web_search_results.json and extract_1.md to extract_4.md.
`python3 web_summary.py`:

```text
web searches saved at (UTC): 2026-11-07T18:39:55Z
  '"1016845912283"': 10 results; mention 17766: 0; mention 1016845912283: 0; of those, also about Wieferich/Fermat: []
  '"17766" Wieferich': 10 results; mention 17766: 2; mention 1016845912283: 0; of those, also about Wieferich/Fermat: []
  '"17766" "1016845912283"': 10 results; mention 17766: 3; mention 1016845912283: 0; of those, also about Wieferich/Fermat: []
  'Wieferich prime "base 17766"': 10 results; mention 17766: 0; mention 1016845912283: 0; of those, also about Wieferich/Fermat: []
  '"fermat quotient" "17766"': 10 results; mention 17766: 1; mention 1016845912283: 0; of those, also about Wieferich/Fermat: [('Supercongruences involving Domb numbers and binary quadratic forms', 'https://ar5iv.labs.arxiv.org/html/2112.12732', 'rarily on Researchgate, Doi:10.13140/RG.2.2.12033.17766. htt')]
  'Wieferich primes bases above 10125 new pairs 2025 2026': 10 results; mention 17766: 0; mention 1016845912283: 0; of those, also about Wieferich/Fermat: []
  'Wieferich pairs bases 10126 65536 search p > 10^12': 10 results; mention 17766: 0; mention 1016845912283: 0; of those, also about Wieferich/Fermat: []
  'github wieferich base search fermat quotient sweep 2026': 10 results; mention 17766: 0; mention 1016845912283: 0; of those, also about Wieferich/Fermat: []
  'arXiv 2025 2026 computation Wieferich primes many bases table': 10 results; mention 17766: 0; mention 1016845912283: 0; of those, also about Wieferich/Fermat: []
extract_1.md: URL: https://github.com/OrygnsCode/wieferich-base-search | chars 10641 | 17766 x0 | 1016845912283 x0
extract_2.md: URL: https://arxiv.org/pdf/2609.13904 | chars 27057 | 17766 x0 | 1016845912283 x0
extract_3.md: URL: https://arxiv.org/html/2607.29329v1 | chars 40635 | 17766 x0 | 1016845912283 x0
extract_4.md: URL: https://arxiv.org/pdf/2506.17684v1 | chars 61811 | 17766 x0 | 1016845912283 x0
```

The results containing "17766" are unrelated: a court case number, other listings, and a DOI suffix in ar5iv
2112.12732. None mentions p.

## 7. Sanity check of the object (outside this role, recorded for completeness)

`cd claim && python3 -B verify.py object/pair.json`:

```text
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 17766, p = 1016845912283, Fermat quotient q_p(b) mod p = 0
PASS
verify exit=0
```

## Caveats

- OEIS's search indexes the sequences' data lines, not b-files. The web search found no base-17766 Wieferich
  sequence either.
- GitHub's issue/PR search index can lag. The PR list itself is live: at fetch time 18:36:02Z, the newest PR had been
  created at 2026-11-07T18:24:27Z. Sealed envelopes in the repository cannot be inspected, by design.
- Web search covers only what engines index, so it cannot prove that no private or unindexed list holds the pair.

## Verdict

The object is new and strictly beats what is known in its cell. The pair is absent from both Fischer tables,
Fischer's other files, OEIS, the repository (main tree, TROPHY_CASE.md, known-knowns/, PRs, releases), and the
literature and code found. It is not a tie, and no trivial edit or propagation rule produces it from anything
published.

pass: true
