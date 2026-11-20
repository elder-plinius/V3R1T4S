# Proof of Both of Fraenkel's 3-Heap Wythoff Conjectures for `A_1 = 11` (`three-heap-wythoff-fraenkel-a1-11`)

## What

For N = 3 and smallest heap A1 = 11, under Sun and Zeilberger's convention, with n2 = 1216, n1 = 3249 and N3^i and B^i_{N3^i} recomputed for every i <= 10, the constants T^11, S^11, alpha = -61, N1 = N2 = 1214, N3 = 1381 and S1(3249) satisfy every hypothesis of their Claims 3.4 and 3.5, so both of Fraenkel's conjectures follow by their published Claim 3.5 and not by any independent formal proof; I reproduced this with separate code, and found no evidence it was already published.

## Check it yourself

From this package folder in a fresh shell (requires only Python 3.8+ standard library):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (runs in about 35 seconds on a single laptop core using ~30 MB RAM).

## Compared to

- **Status source**: https://library.slmath.org/books/Book71/files/GONC6-04.pdf (`Games of No Chance 6`, Problem `A4(53)`, pp. 61-62)
- **Companion table**: https://sites.math.rutgers.edu/~zeilberg/mamarim/mamarimhtml/wythoff.html (Xinyu Sun & Doron Zeilberger, *Ann. Comb.* 8 (2004), 225-238, Table 1)
- **Prior record**: Proved for `0 <= A_1 <= 10` (with `N_3^i` and `B^i_{N_3^i}` omitted from Table 1); `A_1 = 11` open
- **Fetched**: `2026-11-16T19:42:23Z` (`HTTP 200`, SHA-256 `cc1b985ef7fa16d79877677a49b59eb65924a6d082341ae53348544c22cde1f1`)

## Not claimed

- Fraenkel's 3-heap Wythoff conjectures for general `A_1 >= 12` (or `N >= 4` heaps) remain open.
- The finite inductive proof architecture (`Claims 3.3, 3.4, 3.5` and `Lemma 2.4`) is due to Xinyu Sun and Doron Zeilberger (2004).

## Credits

- **Aviezri S. Fraenkel** (conjectures on `N`-heap Wythoff games) and **Aviezri S. Fraenkel & Dalia Krieger** (*J. Integer Seq.* 7, 2004).
- **Xinyu Sun & Doron Zeilberger** (*Annals of Combinatorics* 8 (2004), 225-238, https://sites.math.rutgers.edu/~zeilberg/mamarim/mamarimhtml/wythoff.html): inductive `Claims 3.3-3.5` framework and `A_1 <= 10` Table 1.
- **Richard J. Nowakowski** (*Games of No Chance 6*, MSRI Publ. 71, 2025, https://library.slmath.org/books/Book71/files/GONC6-04.pdf).
