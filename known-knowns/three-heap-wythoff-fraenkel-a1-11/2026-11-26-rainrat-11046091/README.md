# Fraenkel's 3-Heap Wythoff Conjectures for Smallest Heap `A_1 = 12` (`three-heap-wythoff-fraenkel-a1-11`)

## What

Both of Fraenkel's three-heap Wythoff conjectures are proved and independently verified from the game rules for smallest heap A_1 = 12 (together with the full prerequisite inductive chain m = 0..11, including Sun and Zeilberger's Table 1 for m = 0..10 and N_3^i, B_{N_3^i}^i for all 0 <= i <= 11), with explicit thresholds (n_2, n_1) = (601, 1762) and derived constants satisfying Claims 3.3, 3.4, and 3.5 (under the intended midpoint alpha' = floor((max + min)/2)) as well as a self-contained Lemma 2.6 direct induction proof.

Summary of `m = 12` constants (Sun & Zeilberger `[m, A, B]` coordinates, `>=` threshold indexing):
- `T^{12} = {0, 8, 9, 18, 22, 24}`, `|S^{12}| = 43` (`max(S^{12}) = 105`)
- `alpha^{12} = -67`, `N_1^{12} = 64` (`B_j^{12} = j + 42` for `j >= 64`), `N_2^{12} = 352`, `N_3^{12} = 988` (`B_{N_3^{12}}^{12} = 1030`)
- `N = 600`, `n_2 = 601`, `n_1 = 1762`, `A_{n_1}^{12} = 2839`, `B_{n_1}^{12} = 1804`

## Check it yourself

From this package folder in a fresh shell (requires only Python 3.8+ standard library; ~31 s, ~27 MB RAM):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS`.

## Compared to

- **Status source**: Richard J. Nowakowski, *Unsolved Problems in Combinatorial Games*, *Games of No Chance 6* (MSRI Publ. 71, 2025), Problem `A4(53)`, pp. 61–62 — <https://library.slmath.org/books/Book71/files/GONC6-04.pdf> (fetched `2026-11-25T07:12:29Z`, `HTTP 200`, SHA-256 `cc1b985ef7fa16d79877677a49b59eb65924a6d082341ae53348544c22cde1f1`).
- **Companion table & paper**: Xinyu Sun & Doron Zeilberger, *On Fraenkel's N-Heap Wythoff's Conjectures*, *Ann. Comb.* 8 (2004), 225–238 — <https://sites.math.rutgers.edu/~zeilberg/mamarim/mamarimhtml/wythoff.html> (`2026-11-25T07:12:30Z`, `HTTP 200`) and <https://sites.math.rutgers.edu/~zeilberg/mamarimY/Zeilberger_y2004_p225.pdf> (`2026-11-25T07:12:30Z`, `HTTP 200`).
- **Prior published baseline**: Proved for `N = 3`, `0 <= A_1 <= 10` (with `N_3^i` and `B_{N_3^i}^i` omitted from Table 1). Open V3R1T4S PR `#1117` (<https://github.com/elder-plinius/V3R1T4S/pull/1117>, open/unmerged) claims `A_1 = 11` only.
- **This claim**: `A_1 = 12` proved and verified alongside the full prerequisite chain `0 <= m <= 11` (`N_3^i` and `B_{N_3^i}^i` recomputed for all `0 <= i <= 11`).

## Not claimed

- Fraenkel's three-heap Wythoff conjectures for general `A_1 >= 13` or `N >= 4` heaps remain open.
- No Lean 4, Coq/Rocq, or Isabelle formalization is claimed; the infinite continuation is proved mathematically in `how-we-built-it/PROOF.md` and checked finitely by `verify-it-yourself/verify_wythoff.py`.
- As documented in `how-we-built-it/PROOF.md`, Sun & Zeilberger (2004) p. 235 prints `alpha' = floor((max - min)/2)` with a typographical minus sign for `floor((max + min)/2)`; this claim documents that typo honestly, verifies Claim 3.5 under the intended half-sum matching Table 1, and proves the continuation directly via Lemma 2.6 without relying on the misprinted formula.
- Resubmission of draft PR #1245 per `kit/SUBMIT.md` section 3 item 4: clarifies Sun & Zeilberger Lemma 2.6's two-term exclusion in `how-we-built-it/PROOF.md` and adds Xinyu Sun (2005) to `## Credits`; the certificate `object/wythoff_a1_12_certificate.json`, verifier, receipts, and panel files are unchanged.

## Credits

- **Aviezri S. Fraenkel** (conjectures on $N$-heap Wythoff games) and **Aviezri S. Fraenkel & Dalia Krieger** (*J. Integer Seq.* 7, 2004).
- **Xinyu Sun & Doron Zeilberger** (*Ann. Comb.* 8 (2004), 225–238, <https://sites.math.rutgers.edu/~zeilberg/mamarim/mamarimhtml/wythoff.html>): Claims 3.1–3.5, Lemma 2.6, and Table 1 (`0 <= m <= 10`); and **Xinyu Sun** (*Discrete Math.* 300 (2005), 180–195).
- **Richard J. Nowakowski** (*Games of No Chance 6*, MSRI Publ. 71, 2025, <https://library.slmath.org/books/Book71/files/GONC6-04.pdf>).
- **calgulbenkian / V3R1T4S PR #1117** (<https://github.com/elder-plinius/V3R1T4S/pull/1117>): earlier open PR claiming `A_1 = 11` (independently re-verified here for `0 <= m <= 11`).
