# hadamard-maxdet-records: order 81 frozen Gram target (partial win p2), above Orrick

## What

This is an enumerated partial win p2 only: a frozen Gram target for order 81 (symmetric positive-definite integer G with diagonal 81, odd off-diagonals obeying the triple congruence, sqrt(det G)/2^80 = 138538465099776000000000000000000000000000000000000000 above the Orrick record 196 * 20^39 = 107752139522048000000000000000000000000000000000000000, an exact rational Q with Q Q^T = G, and 80 realised +-1 rows matching the leading block), not a +-1 matrix of order 81 and not a determinant record.

The object is `object/G81_p2.json` (sha256 03b380a2074785deac39cb19b68c0853cd52ea469f7b848600cc756df42c8992). The sentence above is quoted word for word from `panel/gate.md`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 2 seconds (measured on the packager's laptop).
- **Expected last line**: `ALL CHECKS PASS`

The script first checks every file in `object/` against `SHA256SUMS`, then runs the standalone checker and a negative control.

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Orrick MaxDet archive, page 3 (Wayback copy of 2019-03-15) | order 81 | 196 * 20^39 = 107752139522048000000000000000000000000000000000000000 | **252*20^39** (Gram target, sqrt(det G) / 2^80) | https://web.archive.org/web/20190315055615/http://www.indiana.edu/~maxdet/page3.shtml | 2026-10-19T05:27:20Z |
| Rokicki newrec page (Wayback copy of 2021-01-26) | order 81 | no entry (N = 80) | **252*20^39** | https://web.archive.org/web/20210126204345/https://tomas.rokicki.com/newrec.html | 2026-10-19T05:27:21Z |
| Math-AI-Caltech hadamard-maxdet README and records CSV (orders 51 and 3 mod 4 only) | order 81 | no row (orders 3 mod 4 only) | **252*20^39** | https://github.com/Math-AI-Caltech/hadamard-maxdet | 2026-10-19T05:26:58Z |
| arXiv:2608.22518 v3, New Records for the Hadamard Maximal Determinant Problem | order 81 | not mentioned | **252*20^39** | https://arxiv.org/html/2608.22518 | 2026-10-19T05:32:55Z |
| EinsteinArena home page (only order 51 listed) | order 81 | none | **252*20^39** | https://einsteinarena.com/ | 2026-10-19T05:40:57Z |
| Contributor's own closed pull request 69 (same target, same value), closed unmerged 2026-10-14 | order 81 | n/a (own earlier filing) | **252*20^39** | https://github.com/elder-plinius/V3R1T4S/pull/69 | 2026-10-19T04:30:31Z |

The panel's novelty skeptic fetched every source itself (its report is `panel/novelty.md`); the triage fetch and its page sha256 values are in `the-record-we-beat/`.

## Not claimed

- This is an enumerated partial win p2 only. It is not a +-1 matrix of order 81 and not a determinant record. No +-1 matrix of order 81 with this determinant is claimed, and none is known to exist.
- Only 80 of the 81 rows are realised as +-1 rows (they match the leading block of G). The panel noted that G sits at a ratio of about 0.9930 to the Barba bound, far above the .77 of the archived record and above anything known for a +-1 matrix, which is a reason to expect that no completion exists. p2 as written does not require one.
- The rational equivalence of G to the identity (times n) is shown by an explicit exact rational matrix Q with Q Q^T = G, which the panel accepted in place of a Hasse-Minkowski computation; it is a certificate, not a search over +-1 matrices.
- No Gram-type value for this order is published anywhere the panel could read, so under p2 the live record is the plain determinant record. The Orrick copy used is dated March 2019 (web.archive.org captures; the archive-it addresses did not serve). Google Scholar was not searched.
- Not peer reviewed. It was checked by a three-skeptic panel (panel/) and by the standalone checker shipped here.

## Filing history

This is a refile of the contributor's pull request 69, closed unmerged on 2026-10-14 in the bulk close of about thirty early PRs during a handoff, not for a defect. The object here is the contributor's file from the 2026-10-18/19 snapshot and the panel re-checked it.

## Credits

- **Orrick's MaxDet archive** (http://www.indiana.edu/~maxdet, Wayback copies above): the record value this target is compared against.
- **Rokicki's newrec page** (https://tomas.rokicki.com/newrec.html): checked; it has no entry for this order.
- **Math-AI-Caltech/hadamard-maxdet** (https://github.com/Math-AI-Caltech/hadamard-maxdet) and **arXiv:2608.22518 v3**, *New Records for the Hadamard Maximal Determinant Problem* (https://arxiv.org/html/2608.22518): checked; neither covers this order.
- **Barba** (the bound the bank entry names) and the **Paley** Hadamard construction used for the realised rows.
- Contributor credit: `calgulbenkian`. The search was run by Gemini (Argon) for the contributor.
