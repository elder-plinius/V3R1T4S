# Run It Yourself

## 1. Run the Standalone Zero-Dependency Referee Verifier

From a fresh shell inside this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Dependencies**: Python 3.8+ standard library only (`json`, `math`, `os`, `sys`).
- **Runtime**: ~35 seconds on one CPU core (~30 MB RAM).
- **Expected final line**: `PASS`.

## 2. What the Checker Verifies

1. Cross-checks literal 3D brute-force move search (`172` P-positions up to `p_3 <= 55`) against clean-room retrograde generation of `P^m` (`0 <= m <= 11`) purely from the normal-play 3-heap Wythoff rules.
2. Verifies every Claim 3.3 `p(m) + 1` XOR-periodicity window witness (`p(11) = 16`), the non-circular Claim 3.4 threshold `N = 15`, all eight conditions of Claim 3.5 on `(n_2, n_1) = (1216, 3249)` plus Lemma 2.4 chopping (`j_chop = 1990, m_1 = 1993`), and exactness/minimality of `(T^m, S^m, alpha^m, N_1^m, N_2^m, N_3^m, B^m_{N_3^m})` for `0 <= m <= 11`.
3. Confirms exact match with all 11 rows (`0 <= i <= 10`) of Sun & Zeilberger's Table 1 (`p1`).
