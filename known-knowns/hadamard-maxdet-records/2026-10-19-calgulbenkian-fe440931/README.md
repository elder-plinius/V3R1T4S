# hadamard-maxdet-records: order 109 matrix, normalised det 297*27^53, above Orrick and Rokicki

## What

The object is a 109 x 109 matrix with all entries +1 or -1 whose exact |det| / 2^108 is 2162897555231082049798834993796033279114137960386362436200469570917630303164899, strictly above the Orrick archive value 1.877483842E78, the Rokicki page value, and the sources listed above (all that I could read), and below the Barba bound, for an order where the earlier record was far below the bound. It also exceeds the merged V3R1T4S value 291 * 27^53 for this order.

The object is `object/M109_2162897555231082049798834993796033279114137960386362436200469570917630303164899.txt` (sha256 fe44093142381fa403c5bc471d6639775c6a3d4f5150f3ee70519e646ed1425e). The sentence above is quoted word for word from `panel/gate.md`.

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
| Orrick MaxDet archive, page 3 (Wayback copy of 2019-03-15) | order 109 | 1.877483842E78 | **297*27^53** | https://web.archive.org/web/20190315055615/http://www.indiana.edu/~maxdet/page3.shtml | 2026-10-19T05:27:20Z |
| Rokicki newrec page (Wayback copy of 2021-01-26) | order 109 | 1.87748e78 (N = 108) | **297*27^53** | https://web.archive.org/web/20210126204345/https://tomas.rokicki.com/newrec.html | 2026-10-19T05:27:21Z |
| Math-AI-Caltech hadamard-maxdet README and records CSV (orders 51 and 3 mod 4 only) | order 109 | no row (orders 3 mod 4 only) | **297*27^53** | https://github.com/Math-AI-Caltech/hadamard-maxdet | 2026-10-19T05:26:58Z |
| arXiv:2608.22518 v3, New Records for the Hadamard Maximal Determinant Problem | order 109 | not mentioned (orders 51 and 3 mod 4 only) | **297*27^53** | https://arxiv.org/html/2608.22518 | 2026-10-19T05:32:55Z |
| EinsteinArena home page (only order 51 listed) | order 109 | none | **297*27^53** | https://einsteinarena.com/ | 2026-10-19T05:40:57Z |
| V3R1T4S merged pull request 155 (contributor's own, known-knowns 2026-10-15-anonymous-c6d1e0ab-0108345c), order 109 | order 109 | 2119202655125403624550373680790052808829003860176536932438843923020304438454497 (291 * 27^53) | **297*27^53** | https://github.com/elder-plinius/V3R1T4S/pull/155 | 2026-10-19T05:27:58Z |
| Contributor's own closed pull request 65 (order 109, same value as merged 155), closed unmerged 2026-10-14 | order 109 | 291 * 27^53 | **297*27^53** | https://github.com/elder-plinius/V3R1T4S/pull/65 | 2026-10-19T04:30:31Z |
| V3R1T4S TROPHY_CASE.md (no maximal-determinant row) | order 109 | none | **297*27^53** | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-19T05:27:03Z |

The panel's novelty skeptic fetched every source itself (its report is `panel/novelty.md`); the triage fetch and its page sha256 values are in `the-record-we-beat/`.

## Not claimed

- This is one matrix and one order. It is not a proof of maximality: the Barba bound is not attained and the true maximum is unknown.
- The standing record this package must beat is the V3R1T4S merged value 291 * 27^53 (pull request 155, the contributor's own). This object exceeds it by 6 * 27^53, a factor of about 1.0206. The merged package remains a valid result for its own value.
- The comparison holds for the sources listed above as the panel could read them. The Orrick archive no longer exists at its own address; the copy used is dated March 2019 (the archive-it addresses did not serve, so the panel used web.archive.org captures of the same pages). Values published after 2019 outside the Caltech repository, arXiv:2608.22518, EinsteinArena and this repository could not be seen, and Google Scholar was not searched.
- The Math-AI-Caltech repository and arXiv:2608.22518 cover orders 51 and orders 3 mod 4 only, so they have no value for order 109.
- Not peer reviewed. It was checked by a three-skeptic panel (panel/) and by the standalone checker shipped here, which computes the determinant three independent exact ways.
- The contributor's notes quote Cauchy-Schwarz ceilings for single-row bordering (294 for order 109) that do not match the panel's own evaluation of the formula (about 307.6 * 27^53). This does not affect the verified determinant. The panel found that the object is not a single-row bordered Hadamard matrix.

## Filing history

The contributor's earlier pull request 65 (order 109, 291 * 27^53) was closed unmerged on 2026-10-14 in the bulk close of about thirty early PRs during a handoff, not for a defect; the same value was later merged as pull request 155. This package is a new, larger value, not a refile.

## Credits

- **Orrick's MaxDet archive** (http://www.indiana.edu/~maxdet, read through the Wayback copies listed above): the standing record values. The claim folder names the page by its curator's surname only; no first name or paper is credited here.
- **Rokicki's newrec page** (https://tomas.rokicki.com/newrec.html, Wayback copy above): an independent listing of the same record values.
- **Math-AI-Caltech/hadamard-maxdet** (https://github.com/Math-AI-Caltech/hadamard-maxdet): the repository of record values and checker for orders 3 mod 4.
- **arXiv:2608.22518 v3**, *New Records for the Hadamard Maximal Determinant Problem* (https://arxiv.org/html/2608.22518): the 2026 records that the bank entry names; author list on the arXiv page.
- **Barba** (the bound for n = 1 mod 4 that the bank entry names) and the **Paley** and **Williamson** Hadamard constructions used as starting points.
- The 3-normalized construction used in `tools/os_3norm_search.c` is cited by the contributor's notes as Orrick-Solomon, arXiv:math/0311292. That attribution is the contributor's and has not been checked by the panel.
- Contributor credit: `calgulbenkian`. The search was run by Gemini (Argon) for the contributor.
