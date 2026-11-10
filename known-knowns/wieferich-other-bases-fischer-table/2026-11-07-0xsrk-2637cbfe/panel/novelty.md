role: NOVELTY
context: claude code headless session (claude -p --safe-mode in a copy of claim/ outside the workspace; fresh context, saw only claim/)

# Novelty check: Wieferich pair (b, p) = (5481, 4848813530161), claimed as a full win of wieferich-other-bases-fischer-table

Object (claim/object/pair.json): `{"target_id": "wieferich-other-bases-fischer-table", "win": "full", "b": 5481, "p": 4848813530161}`

Every number, hash, time and status below was copied from a command output saved in work/. Paths in sha256sum
output are shortened to work/fetched/. The repository's GitHub owner is written as "(repository owner)".

## 1. Fetch records (one request per URL, User-Agent `V3R1T4S-agent/1.0 (open-research notebook; one honest request)`, no retries)

UTC time is from `date -u`, run just before the request(s) on that line. Where one timestamp covers several requests
in a row, the line says so. The HTTP status is curl's `%{http_code}`.

| # | URL | UTC (date -u) | HTTP | sha256 of saved file |
|---|---|---|---|---|
| 1 | http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt (status source) | 2026-11-07T22:45:05Z | 200 | 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 |
| 2 | http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt | 2026-11-07T22:45:14Z | 200 | bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b |
| 3 | https://oeis.org/search?q=4848813530161&fmt=data | 2026-11-07T22:45:19Z | 200 | d52d33b8cb6d89250b19f7d363c587eae781d3fa058663670a2716af0ebd6be8 |
| 4 | https://oeis.org/search?q=Wieferich+5481&fmt=data | 2026-11-07T22:45:30Z | 200 | 9aa70d40152947a43a5d9497db1dc25032b0cc99c5cad01c882e36dd1857dbdf |
| 5 | https://oeis.org/search?q=751787&fmt=data (the known base-5481 prime; any base-5481 Wieferich sequence would contain it) | 2026-11-07T22:45:35Z | 200 | 08e126fbcd778f0fa91b693861e3683ded878713e96246281dfc8281c986b3ea |
| 6 | https://raw.githubusercontent.com/(repository owner)/V3R1T4S/HEAD/TROPHY_CASE.md | 2026-11-07T22:45:43Z | 200 | 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 |
| 7 | https://api.github.com/repos/(repository owner)/V3R1T4S/git/trees/HEAD?recursive=1 | 2026-11-07T22:45:48Z | 200 | 93b7eef8c4a599e1c8925507d9f8ad7dbb3e982741af87c745c69000d6d73625 |
| 8 | https://api.github.com/repos/(repository owner)/V3R1T4S/releases?per_page=100 | 2026-11-07T22:47:11Z | 200 | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 |
| 9 | http://www.fermatquotient.com/ (Fischer's index) | 2026-11-07T22:47:50Z | 200 | 42508627832b9d654ea777db3c10126d558bf7bf13c21c07c5b74452b8e84fd1 |
| 10 | http://www.fermatquotient.com/FermatQuotienten/News.txt (timestamp covers 10 and 11) | 2026-11-07T22:48:14Z | 200 | 1970fbe5188e93b0fa0381beac91b0654b18c9491043bbdb42e256bc7f6080e7 |
| 11 | http://www.fermatquotient.com/FermatQuotienten/FermatQ3.txt | 2026-11-07T22:48:14Z | 200 | 022855e8d16257ca4931bd9f7f9133012f17bbf1bc528f9a6cd12995b02a0a41 |
| 12 | releases API of two third-party Wieferich-search GitHub repositories (one GPU search to 1e14 over 27 bases, updated 2026-06-14; one updated 2026-06-08) (timestamp covers both) | 2026-11-07T22:49:21Z | 200, 200 | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 (both) |
| 13 | https://raw.githubusercontent.com/(repository owner)/V3R1T4S/HEAD/known-unknowns/number-hunts/wieferich-other-bases-fischer-table.md | 2026-11-07T22:49:35Z | 200 | 8395b2fe8a39df3816c850ea9279ab8931e3e3655b4b7ad69c7e437b8f520d52 |
| 14 | http://www.fermatquotient.com/FermatQuotienten/ErstBasen.txt (timestamp covers 14 to 16) | 2026-11-07T22:49:49Z | 200 | e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 |
| 15 | http://www.fermatquotient.com/FermatQuotienten/ErstPBasen.txt | 2026-11-07T22:49:49Z | 200 | 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 |
| 16 | http://www.fermatquotient.com/FermatQuotienten/SwitchFermQ.txt | 2026-11-07T22:49:49Z | 200 | 8190a7ca0bf2a31d9b03b77e97e5d09f45abc8b7df6f4321d706732b329f3faa |

None of these requests was blocked or met a challenge page. The checks ended at `date -u` = 2026-11-07T22:50:12Z.
My copies of Fischer's five files have the same sha256 as the claim's copies in claim/inputs/ and the hashes listed in
claim/status_sources.md. I computed the claim copies' hashes myself too (work/sha256.txt):

```
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 *claim/inputs/FermQ_Sorg.txt
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b *claim/inputs/FermQ_Sort.txt
```

## 2. The cell: base 5481's row and the stated limit (my fetch #1, FermQ_Sorg.txt)

Header lines 10 and 11, verbatim:

```
Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125
Die Basen sind gegenwaertig durchsucht bis 4.8E+12
```

The row for base 5481 and its neighbours (line numbers from the search):

```
5400: 5480,  3^3, 1051, 91577, 222499, 34020095891
5401: 5481,  2^3, 751787
5402: 5482,  3^3, 5, 47^3, 173
```

So the published pairs for base 5481 are p = 2 (5481 ≡ 1 mod 8, written 2^3) and p = 751787, and the stated searched limit
is 4.8E+12. Fischer's index (fetch #9) gives the date of this table: "Tabelle bis Basis 10125 / List from base 2 until 10125 /
Update 21.10.2026". I searched every fetched Fischer file (FermQ_Sorg, FermQ_Sort, News, FermatQ3, ErstBasen, ErstPBasen,
SwitchFermQ) for `4848813530161|48488135|\b5481\b`. The only match was the row above. 4848813530161 appears in none of
the files. The only near-hit was an unrelated number, `25481980477  25326143`, in FermatQ3.txt.

FermQ_Sort.txt (fetch #2) gives the limits for the small bases that are the prime factors of 5481:

```
Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14
Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13
   3  P: 11, 1006003 (>1.2E+15)
```

## 3. OEIS

- #3 `q=4848813530161`: "Sorry, but the terms do not match anything in the table."
- #4 `q=Wieferich 5481`: "Sorry, but the terms do not match anything in the table."
- #5 `q=751787`: "Displaying 1-4 of 4 results found." The four are A042380, A181245, A181241 and A208267. Their names
  (work/oeis_751787_names.txt): "Numerators of continued fraction convergents to sqrt(717)", "T(n,k) = Number of n X k
  binary matrices with no 2 X 2 circuit having pattern 0101 in any orientation", "Number of nX6 binary matrices with no
  2X2 circuit ...", "Number of nX6 0..1 arrays with new values 0..1 introduced in row major order ...". None of them is a
  Wieferich sequence, so OEIS has no base-5481 Wieferich sequence, and p is not in OEIS.

## 4. The V3R1T4S repository (TROPHY_CASE.md, known-knowns/, pull requests, releases)

- TROPHY_CASE.md (#6): a search for `(?i)wieferich|5481|4848813530161|fermat ?quot|fischer` gives "No matches found".
- Tree (#7, work/tree_search.txt): `sha 06b61ea410a5ee90f3c9377a01d468c7cf05c0bd truncated False entries 7190`. The 30
  directories under known-knowns/ include no Wieferich or Fermat-quotient family. The only paths matching
  wieferich|fermat|fischer|5481 are 4 target files under known-unknowns/number-hunts/, including this target's own file.
- The target file (#13) lists no banked pairs. It confirms the same limit (FermQ_Sorg.txt "all searched to 4.8e12, and was
  updated 2026-10-21").
- Releases (#8): `releases 0`. The repository has no release assets that could be ahead of its tree.
- Pull requests. `gh pr list --state all --limit 500` returned `total PRs listed 500 min# 471 max# 1008`. Its Wieferich
  titles are the same 4 that `gh pr list --state all --search "wieferich OR 5481 OR 4848813530161 OR fermatquotient"`
  returns, and that search covers all PRs:
  ```
  1008 OPEN 2026-11-07T21:41:22Z [claim] wieferich-other-bases-fischer-table: Wieferich pair (28860, 1017279755641), partial win p1
  999 OPEN 2026-11-07T19:01:07Z [claim] wieferich-other-bases-fischer-table: Wieferich pair (17766, 1016845912283), partial win p1
  983 OPEN 2026-11-07T16:47:06Z [claim] wieferich-other-bases-fischer-table: Wieferich pair (28910, 1011548897263), partial win p1
  973 OPEN 2026-11-07T13:02:22Z [claim] wieferich-other-bases-fischer-table: Wieferich pair (24766, 1000747824697), partial win p1
  ```
  These are different bases (all above 10125) with different p. `gh search prs --repo ... "5481"` returned `[]`, and
  `gh search issues --repo ... "wieferich 5481" --include-prs` returned `[]`.

## 5. Literature and code from the last 24 months

- Web search for `"4848813530161"`: no page contains the number. The hits were unrelated hashes and IDs.
- Web search for "Wieferich primes base 5481": nothing specific to base 5481.
- Web search for 2025–2026 Wieferich searches in other bases: new per-base OEIS entries (for example A397320, base 40,
  June 2026) and theory papers (arXiv 2607.29329, arXiv 2609.13904). None concerns base 5481 or this p.
- `gh search code "4848813530161"`: `[]`. `gh search prs "4848813530161"`: `[]`. `gh search issues "4848813530161"`: `[]`.
  `gh search code "751787 wieferich"`: `[]`.
- `gh search repos wieferich` found the active Wieferich-search repositories. I code-searched the four relevant ones for
  "5481" and for "4848813530161": `[]` both times. The two most recent have no releases (#12, `0 []` each).

## 6. My own computation, and comparison with trivial edits of published objects

work/check_pair.py was written fresh and is standard library only. It proves p prime by full trial division up to
sqrt(p). Output (work/check_pair_out.txt):

```
b = 5481  p = 4848813530161
p prime by full trial division: True
p > 4.8e12 strictly: True
p divides b: False
b^(p-1) mod p^2 = 1
b perfect power: None
factorisation of b: [3, 3, 3, 7, 29]
  q_p(3) mod p = 1100775266518
  q_p(7) mod p = 3839059523915
  q_p(29) mod p = 2556241736853
sum of q_p over factors (with multiplicity) mod p = 0
bases 2..10125 with c^(p-1) == 1 mod p^2: [5481]
```

Double-pair flag (work/double_check.txt): `p^(b-1) mod b^2 = 25942981`. This is not a double Wieferich pair, so no headline
flag applies, which is consistent with SwitchFermQ.txt not containing p.

Trivial edits checked against the published objects for this cell and the neighbouring cells:
- Power or root relabelling: 5481 = 3^3·7·29 is not a perfect power, and 5481^2 > 10125, so no other base in range
  repeats this pair.
- Propagation by additivity of Fermat quotients, q_p(xy) = q_p(x) + q_p(y): q_p(3), q_p(7) and q_p(29) are all nonzero
  mod p. The pair is therefore not a product of published pairs for its factors. Bases 3, 7 and 29 are searched far past
  p (beyond 1.2E+15 for 3, and at least 7.4E+13 for the others in FermQ_Sort.txt), and p is not in their rows, which agrees
  with these values. The quotients cancel only in the combination 3·q_p(3) + q_p(7) + q_p(29), which is the new fact itself.
- Same p in neighbouring cells: 5481 is the only base in 2..10125 for which p is a Wieferich prime. So no other
  published or unpublished pair with this p exists in the range that could seed this one. The pair counts once.
- Symmetry (−b ≡ p² − b, b⁻¹ mod p²), deletion, restriction and numerical polish: these do not apply. The other bases
  they give lie outside 3..10125, and the object is an exact integer pair.
- Seeding: the object is not seeded from any published pair, because no published source contains p.

Strictly beats what is known: the published row for 5481 contains only 2 and 751787, with a stated limit of 4.8E+12.
4848813530161 is strictly above that limit and appears in none of the sources above. This is a new pair, not a tie.
Caveat: p is only about 1% above the searched limit, and Fischer's search is ongoing (last update 21.10.2026). The novelty
holds as of my fetch at 2026-11-07T22:45:05Z. I cannot rule out an unpublished find by Fischer.

novelty: As of my fetch of FermQ_Sorg.txt at 2026-11-07T22:45:05Z (HTTP 200, sha256 35273a26…45ff4, row `5481,  2^3, 751787`, limit 4.8E+12), the pair (5481, 4848813530161) is exact (5481^(p-1) mod p^2 = 1, with p proven prime) and above the stated limit, and it is absent from every Fischer file, OEIS, the V3R1T4S repository (trophy case, known-knowns, all PRs, releases) and recent literature and code; it is not obtainable by any trivial edit of a published pair, because p is a Wieferich prime to no other base in 2..10125, so it is a new pair.

pass: true
