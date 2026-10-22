# hadamard-maxdet-records: order 117 matrix, normalised det 325*29^57, above Orrick and Rokicki

## What

The object is a 117 x 117 matrix with all entries +1 or -1 whose exact |det| / 2^116 is 73887205478246242985652874268409752933911041846892660492861670872395821475850942725425, strictly above the Orrick archive value 7.231499425E85, the Rokicki page value, and the sources listed above (all that I could read), and below the Barba bound, for an order where the earlier record was far below the bound.

The object is `object/M117_73887205478246242985652874268409752933911041846892660492861670872395821475850942725425.txt` (sha256 fb62d553933dd6bdc7f5539d03b59092c1e624f47a382e4363b30499eb051bf5). The sentence above is quoted word for word from `panel/gate.md`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 8 seconds (measured on the packager's laptop).
- **Expected last line**: `ALL CHECKS PASS`

The script first checks every file in `object/` against `SHA256SUMS`, then runs the standalone checker and a negative control.

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Orrick MaxDet archive, page 3 (Wayback copy of 2019-03-15) | order 117 | 7.231499425E85 | **325*29^57** | https://web.archive.org/web/20190315055615/http://www.indiana.edu/~maxdet/page3.shtml | 2026-10-19T05:27:20Z |
| Rokicki newrec page (Wayback copy of 2021-01-26) | order 117 | 7.2315e85 (N = 116) | **325*29^57** | https://web.archive.org/web/20210126204345/https://tomas.rokicki.com/newrec.html | 2026-10-19T05:27:21Z |
| Math-AI-Caltech hadamard-maxdet README and records CSV (orders 51 and 3 mod 4 only) | order 117 | no row (orders 3 mod 4 only) | **325*29^57** | https://github.com/Math-AI-Caltech/hadamard-maxdet | 2026-10-19T05:26:58Z |
| arXiv:2608.22518 v3, New Records for the Hadamard Maximal Determinant Problem | order 117 | not mentioned (orders 51 and 3 mod 4 only) | **325*29^57** | https://arxiv.org/html/2608.22518 | 2026-10-19T05:32:55Z |
| EinsteinArena home page (only order 51 listed) | order 117 | none | **325*29^57** | https://einsteinarena.com/ | 2026-10-19T05:40:57Z |
| Contributor's own closed pull request 67, closed unmerged 2026-10-14 (a smaller value, not a competing record) | order 117 | 324 * 29^57 | **325*29^57** | https://github.com/elder-plinius/V3R1T4S/pull/67 | 2026-10-19T04:30:31Z |
| V3R1T4S TROPHY_CASE.md (no maximal-determinant row) | order 117 | none | **325*29^57** | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-19T05:27:03Z |

The panel's novelty skeptic fetched every source itself (its report is `panel/novelty.md`); the triage fetch and its page sha256 values are in `the-record-we-beat/`.

## Not claimed

- This is one matrix and one order. It is not a proof of maximality: the Barba bound is not attained and the true maximum is unknown.
- The comparison holds for the sources listed above as the panel could read them. The Orrick archive no longer exists at its own address; the copy used is dated March 2019 (the archive-it addresses did not serve, so the panel used web.archive.org captures of the same pages). Values published after 2019 outside the Caltech repository, arXiv:2608.22518, EinsteinArena and this repository could not be seen, and Google Scholar was not searched.
- The Math-AI-Caltech repository and arXiv:2608.22518 cover orders 51 and orders 3 mod 4 only, so they have no value for order 117.
- Not peer reviewed. It was checked by a three-skeptic panel (panel/) and by the standalone checker shipped here, which computes the determinant three independent exact ways.
- The panel found that the object is not a single-row bordered Hadamard matrix.

## Filing history

The contributor's earlier pull request 67 for this order filed the smaller value 324 * 29^57. It was closed unmerged on 2026-10-14 in the bulk close of about thirty early PRs during a handoff, not for a defect. This package is a new, larger value, not a refile.

## Credits

- **Orrick's MaxDet archive** (http://www.indiana.edu/~maxdet, read through the Wayback copies listed above): the standing record values. The claim folder names the page by its curator's surname only; no first name or paper is credited here.
- **Rokicki's newrec page** (https://tomas.rokicki.com/newrec.html, Wayback copy above): an independent listing of the same record values.
- **Math-AI-Caltech/hadamard-maxdet** (https://github.com/Math-AI-Caltech/hadamard-maxdet): the repository of record values and checker for orders 3 mod 4.
- **arXiv:2608.22518 v3**, *New Records for the Hadamard Maximal Determinant Problem* (https://arxiv.org/html/2608.22518): the 2026 records that the bank entry names; author list on the arXiv page.
- **Barba** (the bound for n = 1 mod 4 that the bank entry names) and the **Paley** and **Williamson** Hadamard constructions used as starting points.
- The 3-normalized construction used in `tools/os_3norm_search.c` is cited by the contributor's notes as Orrick-Solomon, arXiv:math/0311292. That attribution is the contributor's and has not been checked by the panel.
- Contributor credit: `calgulbenkian`. The search was run by Gemini (Argon) for the contributor.
