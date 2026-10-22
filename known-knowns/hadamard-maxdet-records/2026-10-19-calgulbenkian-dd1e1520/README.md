# hadamard-maxdet-records: order 105 matrix, normalised det 277*26^51, above Orrick and Rokicki

## What

The object is a 105 x 105 matrix with all entries +1 or -1 whose exact |det| / 2^104 is 403757419044975201959422423846994970270257858463738130848861743562151165952, strictly above the Orrick archive value 3.847437473E74, the Rokicki page value, and the sources listed above (all that I could read), and below the Barba bound, for an order where the earlier record was far below the bound.

The object is `object/M105_403757419044975201959422423846994970270257858463738130848861743562151165952.txt` (sha256 dd1e1520b87d97fe404bf0857235652e04d819a08484c85fd3e024fb1346d28b). The sentence above is quoted word for word from `panel/gate.md`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 5 seconds (measured on the packager's laptop).
- **Expected last line**: `ALL CHECKS PASS`

The script first checks every file in `object/` against `SHA256SUMS`, then runs the standalone checker and a negative control.

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Orrick MaxDet archive, page 3 (Wayback copy of 2019-03-15) | order 105 | 3.847437473E74 | **277*26^51** | https://web.archive.org/web/20190315055615/http://www.indiana.edu/~maxdet/page3.shtml | 2026-10-19T05:27:20Z |
| Rokicki newrec page (Wayback copy of 2021-01-26) | order 105 | 3.84744e74 (N = 104) | **277*26^51** | https://web.archive.org/web/20210126204345/https://tomas.rokicki.com/newrec.html | 2026-10-19T05:27:21Z |
| Math-AI-Caltech hadamard-maxdet README and records CSV (orders 51 and 3 mod 4 only) | order 105 | no row (orders 3 mod 4 only) | **277*26^51** | https://github.com/Math-AI-Caltech/hadamard-maxdet | 2026-10-19T05:26:58Z |
| arXiv:2608.22518 v3, New Records for the Hadamard Maximal Determinant Problem | order 105 | not mentioned (orders 51 and 3 mod 4 only) | **277*26^51** | https://arxiv.org/html/2608.22518 | 2026-10-19T05:32:55Z |
| EinsteinArena home page (only order 51 listed) | order 105 | none | **277*26^51** | https://einsteinarena.com/ | 2026-10-19T05:40:57Z |
| Contributor's own closed pull request 66, closed unmerged 2026-10-14 (a smaller value, not a competing record) | order 105 | 276 * 26^51 | **277*26^51** | https://github.com/elder-plinius/V3R1T4S/pull/66 | 2026-10-19T04:30:31Z |
| V3R1T4S TROPHY_CASE.md (no maximal-determinant row) | order 105 | none | **277*26^51** | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-19T05:27:03Z |

The panel's novelty skeptic fetched every source itself (its report is `panel/novelty.md`); the triage fetch and its page sha256 values are in `the-record-we-beat/`.

## Not claimed

- This is one matrix and one order. It is not a proof of maximality: the Barba bound is not attained and the true maximum is unknown.
- The comparison holds for the sources listed above as the panel could read them. The Orrick archive no longer exists at its own address; the copy used is dated March 2019 (the archive-it addresses did not serve, so the panel used web.archive.org captures of the same pages). Values published after 2019 outside the Caltech repository, arXiv:2608.22518, EinsteinArena and this repository could not be seen, and Google Scholar was not searched.
- The Math-AI-Caltech repository and arXiv:2608.22518 cover orders 51 and orders 3 mod 4 only, so they have no value for order 105.
- Not peer reviewed. It was checked by a three-skeptic panel (panel/) and by the standalone checker shipped here, which computes the determinant three independent exact ways.
- The matrix is a Hadamard matrix of order 104 with one border row and column. The novelty skeptic flagged for a maintainer ruling whether bordering counts as propagation under the PR #350 rule (no table value for order 104 determines the border). We make no claim on that ruling; if bordering a Hadamard matrix counts as propagation, this package should be judged accordingly.
- The contributor's notes quote Cauchy-Schwarz ceilings for single-row bordering (278 for order 105) that do not match the panel's own evaluation of the formula (about 291.2 * 26^51). This does not affect the verified determinant.

## Filing history

The contributor's earlier pull request 66 for this order filed the smaller value 276 * 26^51. It was closed unmerged on 2026-10-14 in the bulk close of about thirty early PRs during a handoff, not for a defect. This package is a new, larger value, not a refile.

## Credits

- **Orrick's MaxDet archive** (http://www.indiana.edu/~maxdet, read through the Wayback copies listed above): the standing record values. The claim folder names the page by its curator's surname only; no first name or paper is credited here.
- **Rokicki's newrec page** (https://tomas.rokicki.com/newrec.html, Wayback copy above): an independent listing of the same record values.
- **Math-AI-Caltech/hadamard-maxdet** (https://github.com/Math-AI-Caltech/hadamard-maxdet): the repository of record values and checker for orders 3 mod 4.
- **arXiv:2608.22518 v3**, *New Records for the Hadamard Maximal Determinant Problem* (https://arxiv.org/html/2608.22518): the 2026 records that the bank entry names; author list on the arXiv page.
- **Barba** (the bound for n = 1 mod 4 that the bank entry names) and the **Paley** and **Williamson** Hadamard constructions used as starting points.
- The 3-normalized construction used in `tools/os_3norm_search.c` is cited by the contributor's notes as Orrick-Solomon, arXiv:math/0311292. That attribution is the contributor's and has not been checked by the panel.
- Contributor credit: `calgulbenkian`. The search was run by Gemini (Argon) for the contributor.
