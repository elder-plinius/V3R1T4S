# PREREG — lychrel-new-base-proof (Mechanical Template-Closure Proof in New Bases b = 50, 98, 146)

Frozen: 2026-10-19T05:45:00Z

## Frozen Acceptance Rule
A Lychrel template family $(T_1(m), T_2(m), T_3(m), T_4(m))$ and start integer $n = T_1(1)$ (plus pre-template seed $n_{\text{seed}}$) in base $b$ are accepted as a confirmed solution if and only if:
1. The exact same symbolic and concrete verifier first reproduces David Seal's 1996 Period-4 baseline in Base 26 (`1N5ELA6C P^m P6E7 0^m 0D59ME5N`).
2. The base $b$ satisfies $b \notin \{2^k, 11, 17, 20, 26\}$ and is not listed as proven on `https://en.wikipedia.org/wiki/Lychrel_number` (`data/Lychrel_number.html`) at verification time.
3. Symbolic run-length block-by-block carry computation (`symbolic_rle_rev_add`) proves $F_b(T_1(m)) = T_2(m)$, $F_b(T_2(m)) = T_3(m)$, $F_b(T_3(m)) = T_4(m)$, and $F_b(T_4(m)) = T_1(m+1)$ for **all** integers $m \ge 1$, with every parameter-dependent block emitting a constant digit run and a constant outgoing carry $c_{\text{out}} = c_{\text{in}} \in \{0, 1\}$.
4. Symbolic mirrored-block comparison (`check_symbolic_non_palindromicity`) proves that no $T_i(m)$ ($i \in \{1, 2, 3, 4\}, m \ge 1$) is a base-$b$ palindrome.
5. Brute-force reverse-and-add verification holds for all $1 \le m \le 500$ ($\ge \max(\text{threshold}, 200) = 200$), and the orbit of $n = T_1(1)$ in primary base $b = 50$ is simulated for $100,000$ steps (`t = 0 .. 100,000`) with every iterate matched to $T_1(m)..T_4(m)$ via a compiled regular expression (`re.Pattern.fullmatch`).
6. Rostand S. Kuitché's 2023 preprint (`data/rs_2659802.pdf`) is obtained and mechanically audited across bases $3 \le b \le 10$ (`claim/kuitche_2023_audit.json`), subsuming partial win `p2`.

null_test: not needed because the claim is an explicit mathematical proof reduced to a finite mechanical symbolic carry-transducer check and regex-verified 100,000-step orbit simulation; in addition, 400 seeded random 82-digit base-50 starting numbers and two structural perturbation controls are verified in `author_checker_lychrel_check.py`.

ratchet_budget: n/a (deterministic symbolic template-closure proof)
