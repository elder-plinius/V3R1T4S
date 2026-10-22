# Reproduction of all 12 entries of He's Table 2 for the cubic-lattice dimer constant (partial win p1; reproduction only)

## What

The folder reproduces all 12 entries of He's Table 2, (2,2) to (6,3) at p = 4 and (5,5) at p = 2, rounded up to six decimals by exact integer arithmetic (seven confirmed by my own exact-integer recomputation, the rest by the folder's records), and it is a reproduction only, not a new bound.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: python3 3.8 or later, standard library only for the 11 Python entries; a C compiler (cc, libc and pthreads only) for the (5,5) entry at p = 2. Without a C compiler only the 11 Python entries are checked and the script says so. CW_QUICK=1 skips the slowest entry, (5,4).
- **Time**: about 14 minutes (13 min 36 s measured by the contributor on a loaded 28-core Mac; the Python entries alone took about 8 minutes when the machine was unloaded, (5,4) being about 7.5 minutes of that; the C check of the (5,5) entry takes about 75 seconds).
- **Expected last line**: `ALL CHECKS PASS`.

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Qidong He, arXiv 2607.28810 v2, Table 2 | (2,2) | 0.486478 (p = 4) | https://arxiv.org/abs/2607.28810 | 2026-10-19T05:25:59Z |
| same | (3,2), (3,3), (4,2), (4,3), (4,4) | 0.471408, 0.458558, 0.465970, 0.457380, 0.454673 (p = 4) | same | same |
| same | (5,2), (5,3), (5,4), (6,2), (6,3) | 0.463401, 0.454663, 0.453365, 0.462010, 0.454618 (p = 4) | same | same |
| same | (5,5) | 0.452130 (p = 2, as He's Section 4 states) | same | same |
| arXiv export API searches for a newer or citing bound (three queries) | newest items | none newer than He on l3, h3 or l4 | https://export.arxiv.org/api/query | 2026-10-19T06:36:39Z to 06:36:49Z (HTTP 200); the novelty skeptic repeated the search about 07:12 to 07:28Z |

This package compares equal to the table, entry by entry, rounded up to six decimals; it does not beat it. Snapshot metadata with HTTP status and page sha256: the-record-we-beat/README.md. The panel's novelty report is panel/novelty.md.

## Not claimed

- This is a reproduction only. It is not a new bound: every one of the 12 values equals He's published value, so nothing here improves on the table.
- Seven of the twelve entries were confirmed by the criterion skeptic's own exact-integer recomputation. The other five rest on the folder's own records (the shipped checker and its recorded output), which the skeptic looked at but did not recompute.
- The author's RESULTS.md (object/RESULTS.md) has two wrong ten-digit figures, for (5,4) and (6,3). The six-decimal values are unaffected. RESULTS.md also lists results beyond the gated claim (other win paths and a (6,4) entry that He did not compute); those are not part of this claim, and the l3 certificate and the monomer-dimer and four-dimensional results are separate packages.
- The cross-family reviewer (a model of a different family) saw the written derivations only, not the certificates. The three panel skeptics and the object's builder (Gemini, Argon) are different model families, but none of this is peer review.
- The (5,5) entry is He's bound at p = 2; nothing in this package says anything about deeper iterates at (5,5).

## Credits

- **Qidong He**, arXiv 2607.28810 (v1 30 Jul 2026, v2 11 Aug 2026), https://arxiv.org/abs/2607.28810: Table 2 and Corollary 3.4, the method and the values reproduced here.
- **Csikvari**, as cited by He (abstract: "an inequality of Csikvari (2017)"): the inequality behind the diagonal-layer bound. We did not read Csikvari's paper itself.
- The contributor's team (credit name calgulbenkian; the search code was produced by the model Gemini, Argon) for the independent reimplementation and checker.
- Contributor credit: `calgulbenkian`.
