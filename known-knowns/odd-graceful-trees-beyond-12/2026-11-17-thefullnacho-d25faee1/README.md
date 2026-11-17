# Every tree on 23 vertices is odd-graceful

**Status: CONFIRMED_PARTIAL.** Confirmed by a fresh-context three-skeptic panel (REPRODUCE, NOVELTY, CRITERION)
and the honesty gate; see panel/gate.md.

Target: `odd-graceful-trees-beyond-12`. Credit: GitHub [thefullnacho](https://github.com/thefullnacho).

## What

The file cert_n23.txt (uncompressed sha256 d25faee17d7c798dbe7f6d4acc882cb82f924a537de4c8620ed61264f79ecf0e; gzip sha256 483c524995e2c184c1f5a7aeda65a69d44a97ac552c3c6177374bc4b13435520; archive odd-graceful-trees-10-23-certificates.tar.xz sha256 f89ddd847de5ea066c05730800a17ac01f9ee694c346638d40d1b1b0dc526713, 271015048 bytes, https://zenodo.org/records/24322888/files/odd-graceful-trees-10-23-certificates.tar.xz?download=1, DOI 10.5281/zenodo.24322888) gives, for every one of the 14828074 unlabeled trees on 23 vertices (A000055(23), matched one-to-one by canonical form against independent regeneration by three fresh-context skeptics), an injective vertex labeling into {0, 1, ..., 43} whose edge differences are exactly {1, 3, ..., 43}.

The same archive also contains cert_n10.txt through cert_n22.txt, one file per order, each with A000055(n)
lines and an odd-graceful labeling of every unlabeled tree on n vertices. Those files were produced by the
same hybrid search, independently of draft pull request #1007 (CharanRayudu), which was first to claim the
bank's success criterion (a) (every tree on at most 22 vertices). They are included so a stranger can check
the full range 10..23 with the package checker; they were not before the three-skeptic panel and are not
part of the confirmed_scope sentence above. Together with the paneled n = 23 file they go one order past
the bank target.

## Check it yourself

From this folder. Orders 10..15 and a mixed-order sample live in `object/` and are always checked:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Needs python3 (standard library). gcc is optional; if present, the C checker
is used for the full files and is much faster. The bundled part (n = 10..15, 13,093 trees, plus the sample)
takes well under a minute on one core.

To check orders 16..23 as well, put the fourteen certificate files in `certificates/` (unpack the archive
named in `object/CERTIFICATES.md`; `run_checks.sh` can fetch it from Zenodo itself) or set
CERT_DIR, and run the same command. Checking every tree on 10..23 vertices (23,942,264 trees, about 3.91 GiB
of text) took a few minutes with the C checker on one core; see `verify-it-yourself/RECEIPTS.md`.

The archive is 271015048 bytes (sha256 f89ddd847de5ea066c05730800a17ac01f9ee694c346638d40d1b1b0dc526713)
and unpacks to 4194247416 bytes of text. Zenodo: https://doi.org/10.5281/zenodo.24322888

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| J. A. Gallian, A Dynamic Survey of Graph Labeling, Electron. J. Combin. DS6, 29th ed. (6 November 2026), Section 3.6, p. 88 | all trees on at most n vertices are odd-graceful (computer verification) | 12 (C. Barrientos, unpublished, cited in DS6) | https://www.combinatorics.org/files/Surveys/ds6/ds6v29-2026.pdf | 2026-11-17T16:46:26Z |

This package, for the paneled claim: 23. Draft pull request https://github.com/elder-plinius/V3R1T4S/pull/1007
(CharanRayudu, opened 2026-11-07, a resubmission of #880) claims every tree on at most 22 vertices and was
first to that bank target; it does not claim 23. Snapshot with sha256 in `the-record-we-beat/RECORD.md`.

## Not claimed

- Nothing about 24 or more vertices, and no proof of Gnanajothi's conjecture that every tree is odd-graceful.
- Orders 10..12 are re-certified here as part of the archive but are not a new literature result; Gnanajothi
  proved order 10 and Barrientos extended that to order 12, as recorded in DS6.
- Certificates for n = 10..22 are included and are checkable, but they are not part of the three-skeptic
  confirmed_scope. Draft PR #1007 was first to claim the bank's <=22 target.
- No tree was found that is not odd-graceful.
- The tree lists were produced with networkx, not nauty gentreeg. The package checkers and the panelists
  establish coverage by independent regeneration (WROM / leaf extension / centroid composition, depending
  on the checker) and by distinct canonical forms equal in number to A000055(n).

## Credits

- R. B. Gnanajothi, 1991: the definition and the conjecture that every tree is odd-graceful, with a proof
  for trees of order up to 10.
- Christian Barrientos: the extension to order 12 (unpublished, cited in DS6), and proofs for trees of
  diameter at most five and for caterpillar forests.
- J. A. Gallian, A Dynamic Survey of Graph Labeling (DS6), 29th ed., 6 November 2026, Section 3.6:
  https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6
- OEIS A000055, number of trees with n unlabeled nodes: https://oeis.org/A000055
- G. Brinkmann, S. Crevals, H. Melot, L. Rylands and E. Steffen, DMTCS 14 (2012), on the alpha-deficit of
  trees, which motivated an earlier structured-family lens on this quarry.
- networkx (tree enumeration in the search): https://networkx.org
- V3R1T4S kit and bank entry: https://github.com/elder-plinius/V3R1T4S
- CharanRayudu, draft pull request #1007 (and the earlier #880): first to claim the bank's success
  criterion (a), every tree on at most 22 vertices. The certificates in this package were derived
  independently and were not taken from that pull request.
