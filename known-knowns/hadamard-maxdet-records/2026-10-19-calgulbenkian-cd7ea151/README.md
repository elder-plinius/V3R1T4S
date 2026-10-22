# hadamard-maxdet-records: order 49 frozen Gram target (partial win p2), above Orrick

## What

This is an enumerated partial win p2 only: a frozen Gram target for order 49 (symmetric positive-definite integer G with diagonal 49, odd off-diagonals obeying the triple congruence, sqrt(det G)/2^48 = 768469522966111493289934848 above the Orrick record 96 * 12^23 = 635974777627126753067532288, an exact rational Q with Q Q^T = G, and 48 realised +-1 rows matching the leading block), not a +-1 matrix of order 49 and not a determinant record.

The object is `object/G49_p2.json` (sha256 cd7ea151cb23cea573fc617f983c2ce21a340dda94ec30baf82c4180c170e347). The sentence above is quoted word for word from `panel/gate.md`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 1 seconds (measured on the packager's laptop).
- **Expected last line**: `ALL CHECKS PASS`

The script first checks every file in `object/` against `SHA256SUMS`, then runs the standalone checker and a negative control.

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Orrick MaxDet archive, page 2 (Wayback copy of 2019-03-16) | order 49 | 96 * 12^23 = 635974777627126753067532288 | **116*12^23** (Gram target, sqrt(det G) / 2^48) | https://web.archive.org/web/20190316151116/http://www.indiana.edu/~maxdet/page2.shtml | 2026-10-19T05:36:45Z |
| Rokicki newrec page (Wayback copy of 2021-01-26) | order 49 | no entry (N = 48) | **116*12^23** | https://web.archive.org/web/20210126204345/https://tomas.rokicki.com/newrec.html | 2026-10-19T05:27:21Z |
| Math-AI-Caltech hadamard-maxdet README and records CSV (orders 51 and 3 mod 4 only) | order 49 | no row (orders 3 mod 4 only) | **116*12^23** | https://github.com/Math-AI-Caltech/hadamard-maxdet | 2026-10-19T05:26:58Z |
| arXiv:2608.22518 v3, New Records for the Hadamard Maximal Determinant Problem | order 49 | not mentioned | **116*12^23** | https://arxiv.org/html/2608.22518 | 2026-10-19T05:32:55Z |
| EinsteinArena home page (only order 51 listed) | order 49 | none | **116*12^23** | https://einsteinarena.com/ | 2026-10-19T05:40:57Z |
| Contributor's own closed pull request 68 (same target, same value), closed unmerged 2026-10-14 | order 49 | n/a (own earlier filing) | **116*12^23** | https://github.com/elder-plinius/V3R1T4S/pull/68 | 2026-10-19T04:30:31Z |

The panel's novelty skeptic fetched every source itself (its report is `panel/novelty.md`); the triage fetch and its page sha256 values are in `the-record-we-beat/`.

## Not claimed

- This is an enumerated partial win p2 only. It is not a +-1 matrix of order 49 and not a determinant record. No +-1 matrix of order 49 with this determinant is claimed, and none is known to exist.
- Only 48 of the 49 rows are realised as +-1 rows (they match the leading block of G). The panel noted that G sits at a ratio of about 0.9815 to the Barba bound, far above the .81 of the archived record and above anything known for a +-1 matrix, which is a reason to expect that no completion exists. p2 as written does not require one.
- The rational equivalence of G to the identity (times n) is shown by an explicit exact rational matrix Q with Q Q^T = G, which the panel accepted in place of a Hasse-Minkowski computation; it is a certificate, not a search over +-1 matrices.
- No Gram-type value for this order is published anywhere the panel could read, so under p2 the live record is the plain determinant record. The Orrick copy used is dated March 2019 (web.archive.org captures; the archive-it addresses did not serve). Google Scholar was not searched.
- Not peer reviewed. It was checked by a three-skeptic panel (panel/) and by the standalone checker shipped here.

## Filing history

This is a refile of the contributor's pull request 68, closed unmerged on 2026-10-14 in the bulk close of about thirty early PRs during a handoff, not for a defect. The object here is the contributor's file from the 2026-10-18/19 snapshot and the panel re-checked it.

## Credits

- **Orrick's MaxDet archive** (http://www.indiana.edu/~maxdet, Wayback copies above): the record value this target is compared against.
- **Rokicki's newrec page** (https://tomas.rokicki.com/newrec.html): checked; it has no entry for this order.
- **Math-AI-Caltech/hadamard-maxdet** (https://github.com/Math-AI-Caltech/hadamard-maxdet) and **arXiv:2608.22518 v3**, *New Records for the Hadamard Maximal Determinant Problem* (https://arxiv.org/html/2608.22518): checked; neither covers this order.
- **Barba** (the bound the bank entry names) and the **Paley** Hadamard construction used for the realised rows.
- Contributor credit: `calgulbenkian`. The search was run by Gemini (Argon) for the contributor.
