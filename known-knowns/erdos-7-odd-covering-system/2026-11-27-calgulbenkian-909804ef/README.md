# Lower bound L >= 6,557,114,959,770,375 for coverings with distinct odd moduli

## What

A written proof (`object/PROOF.md`), unrefereed and not checked by any proof assistant, together with exact rational recomputation of its finite part (738 scalar certificates, 37 anchored certificates with 29,485 inequalities, and the domination of 6,782 exponent vectors) by two separately written checkers that both pass, shows that every finite covering of Z by residue classes with pairwise distinct odd moduli greater than 1 has L >= 6,557,114,959,770,375, strictly above 11,486,475.

In numbers: L >= 6,557,114,959,770,375 = 3^5 * 5^3 * 7^2 * 11^2 * 13^2 * 17 * 19 * 23 * 29 (partial win p2 of the target).

The proof is `object/PROOF.md` (Theorem 1). It is a written proof plus three finite computations in exact rational arithmetic, listed in its Section 9.4: 738 scalar certificates, 37 anchored certificates with 29,485 inequalities, and an enumeration of 6,782 exponent vectors. The certificate files are `object/certs/` (nine plain TSV files, indexed with byte sizes and SHA-256 digests in `object/MANIFEST.json`, format in `verify-it-yourself/FORMAT.md`). The proof is complete only together with a successful run of a checker on these files (PROOF.md Section 0).

## Check it yourself

From this package folder (needs `python3` 3.9 or later with its standard library, and a C++17 compiler `c++`):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. The script runs the first checker (`verify-it-yourself/check.py`, Python standard library only, no floating point, up to 4 processes) and then builds and runs the second, independently written checker (`verify-it-yourself/alternate/`, Python standard library plus a small C++17 integer kernel). It prints `PASS` only if both pass, and `FAIL` otherwise.

Time (NUMERICAL, measured, see `verify-it-yourself/RECEIPTS.md`): 197 s for the whole script on a 28-core desktop (Apple M3 Ultra) under heavy load from other jobs (first checker 182 s with 4 processes, second checker 14 s including its build); the first checker alone with one process took 424 s. Not measured on a laptop.

## Compared to

Target `erdos-7-odd-covering-system`, partial win p2. Status source: https://www.erdosproblems.com/7, read 2026-11-27T01:16:39Z in a browser (the site refuses automated requests; see `STATUS_CHECK_RECORD.md` and `the-record-we-beat/README.md`): problem listed as open, no numeric lower bound on L stated.

| bound on L | source | relation to this package |
|---|---|---|
| L >= 11,486,475 | Egeozturk, Erdős Problems forum thread 7, August 2026, https://www.erdosproblems.com/forum/thread/7 (the bank's p2 bar; thread read 2026-11-27T01:16:39Z, still the largest bound stated there) | this bound is 570,855,285 times larger |
| L > 1,527,701,174 | Lean 4 proof, https://github.com/rw762-sketch/Open-Math-problem (last checked 2026-11-19, to be re-fetched by the novelty reviewer) | this bound is about 4.29 million times larger |
| L >= 9,704,539,845 | M. Schroeder, Zenodo, https://doi.org/10.5281/zenodo.22759614, Corollary 1.3, unrefereed (last checked 2026-11-18, to be re-fetched by the novelty reviewer) | this bound is 675,675 = 3^3 * 5^2 * 7 * 11 * 13 times larger |
| L >= 168,131,152,814,625 | an earlier package by the same contributor on this target in this repository, an open, unmerged pull request when this package was written | this bound is exactly 39 = 3 * 13 times larger |

This package reaches its bound by a different method from the earlier package (the anchored method of Schroeder's preprint, written out with exponent caps, together with a scalar bound for ten to thirteen primes). It does not rely on the earlier package and stands on its own.

## Not claimed

Taken from Section 10 of `object/PROOF.md`:

- The existence of an odd covering remains open. This is a lower bound on L for a hypothetical odd covering, not an answer to the question of Erdős and Selfridge.
- At least ten distinct prime factors of L (omega(L) >= 10, partial win p1) is **not** proved. The proof shows omega(L) >= 9 (Theorem A, due to Schroeder) and nothing more about the number of primes. The vector (5, 3, 2, 2, 2, 1, 1, 1, 1), whose product is the bound itself, is dominated by none of the nine-prime certificates, and no claim is made about it.
- No structural statement about which primes or prime powers divide L is claimed; only the inequality.
- The bound is not claimed to be the limit of the method.
- The lemma chain is **not** formalised in a proof assistant. Sections 1 to 8 of PROOF.md are a written proof; the finite computations are verified by recomputation with two independent programs, not by a formally verified program.
- Nothing is claimed about the other results of Schroeder's preprint.
- PROOF.md itself makes no claim of priority or novelty; the comparison above is the contributor's.

## Credits

- **M. Schroeder**, *Nine prime divisors in odd distinct covering systems*, author preprint, version 1.0.1, Zenodo, 13 September 2026, revised 15 September 2026, https://doi.org/10.5281/zenodo.22759614 (unrefereed). The method of PROOF.md Sections 3 and 5 to 8 is his; his Theorem 1.1 (omega(L) >= 9) is Theorem A of PROOF.md, and PROOF.md Section 11 gives a lemma-by-lemma correspondence. The certificate for Theorem A in this package was computed independently of the certificate published with his preprint. His earlier preprints on seven and eight prime divisors (https://doi.org/10.5281/zenodo.22739035, https://doi.org/10.5281/zenodo.22747841) are named in his reference list as using a scalar comparison; they were not consulted.
- **R. J. Simpson and D. Zeilberger**, *Necessary conditions for distinct covering systems with square-free moduli*, Acta Arithmetica 59 (1991), 59-70, https://doi.org/10.4064/aa-59-1-59-70: cited in Schroeder's preprint as the source of the prime replacement principle (not consulted; PROOF.md Lemma 2.1 is self-contained).
- **P. Erdős**, *On integers of the form 2^k + p and some related problems*, Summa Brasiliensis Mathematicae 2 (1950), 113-123, and **J. L. Selfridge**: the problem. Problem page maintained by **T. F. Bloom**: https://www.erdosproblems.com/7.
- **R. D. Hough and P. P. Nielsen**, *Covering systems with restricted divisibility*, Duke Mathematical Journal 168 (2019), 3261-3295, https://doi.org/10.1215/00127094-2019-0058 (context; not used in the proof).
- **P. Balister, B. Bollobás, R. Morris, J. Sahasrabudhe and M. Tiba**, *The Erdős-Selfridge problem with square-free moduli*, Algebra and Number Theory 15 (2021), 609-626, https://doi.org/10.2140/ant.2021.15.609, and *On the Erdős covering problem: the density of the uncovered set*, Inventiones Mathematicae 228 (2022), 377-414, https://arxiv.org/abs/1811.03547: the distortion method behind the kernels of PROOF.md Lemma 3.2 (context; not used in the proof).
- **I. Mian and S. Siddique**, *Kernel-checked exclusions for the Erdős-Selfridge odd covering problem: any odd covering of Z has lcm exceeding 10000*, https://arxiv.org/abs/2607.25628 (July 2026), and **X. Dai, H. Li, J. Li and S. Yi**, *On the moduli of distinct covering systems*, https://arxiv.org/abs/2611.15110 (November 2026): other statements about L named in PROOF.md Section 11.
- **Egeozturk**, Erdős Problems forum, thread 7 (https://www.erdosproblems.com/forum/thread/7), August 2026: the bound L >= 11,486,475 that the bank's p2 bar names.
- The authors of https://github.com/rw762-sketch/Open-Math-problem: the Lean 4 bound L > 1,527,701,174 compared against above.
