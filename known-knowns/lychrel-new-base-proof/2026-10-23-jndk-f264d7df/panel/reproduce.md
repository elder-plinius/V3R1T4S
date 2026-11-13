# REPRODUCE skeptic verdict: lychrel-new-base-proof, base 13

context: subagent (Claude Code Agent tool, fresh context)

Scope: I read only the claim package copy (CLAIM.md, REPRODUCE.md, result/, status/, code/). I wrote my own checker
`mycheck/check.py` after reading CLAIM.md and result/ and before opening anything in code/. I ran every program on the
job queue (short queue).

## Definition implemented (quoted)

"reverse-and-add in base b: x + reverse of x's base-b digit string; a Lychrel number never reaches a palindrome."
So RA(x) = x + R(x), where R(x) is the integer whose base-13 digit string is x's digit string (no leading zeros)
reversed. The reversed string may begin with zeros. The orbit is x_0 = n, x_{t+1} = RA(x_t).
Template semantics (from result/lychrel_base13.json): "each template is a list of runs [digit, a, k]: digit repeated
a + k*m times, most significant run first; x_{entry_step + m*period + i} = T_i(m) for all m >= 0".

## What my checker establishes

Object consistency:
- The seed digits in result/lychrel_base13.json equal result/seed_base13.txt (134 digits).
- Their value equals result/seed_decimal.txt and the json `seed_decimal`.
- result/b13.tpl parses to the same base, period, entry step, seed and 10 templates as the json.
- Every run has digit in 0..12 and a, k >= 0. Every template's first run has a >= 1 and a nonzero digit.

(1) Orbit entry: entry_step = 0, and the seed digit string equals T_0(0) exactly.

(2) Closure for all m >= 0 (symbolic argument, written and justified independently):
Every template has exactly one growing run (k = 3 in all ten; checked). So T_i(m) = P d^n S, where P and S are fixed
strings (|P| = p, |S| = s) and n = a + 3m.
- Lemma A (column sums). Index columns j = 0 from the least significant end, and let L = p+n+s. Column j adds
  x_j + x_{L-1-j}.
  - For j < max(p,s): x_j is S's j-th digit from the right, or d if j >= s. x_{L-1-j} is P[j], or d if j >= p.
    Neither depends on n as long as n >= w := |p-s|.
  - For max(p,s) <= j < L - max(p,s): both digits lie in the d-run.
  - The column-sum sequence is symmetric in j.
  - So the column sums are exactly A . (2d)^(n-w) . reverse(A), with |A| = max(p,s) and A independent of n.
- Lemma B (carries). Carries are 0 or 1. Process A with carry-in 0. This gives fixed low digits and a carry c.
  - Inside the constant run, the carry map c -> floor((2d+c)/13) reaches a fixed point after a transient of t
    columns. The script computes t and checks the fixed point; here t <= 1.
  - From then on every column emits the same digit e = (2d+c*) mod 13 with the same carry c*.
  - reverse(A) is then processed with carry c*, which gives fixed high digits plus an optional final carry digit.
  - Result: RA(P d^n S) = Q e^(n-w-t) R, with Q, e, R, w, t independent of n. Valid whenever n >= w + t.
- Equality for all m. I put both sides into canonical form: (prefix, run digit, run-length offset, suffix), with
  copies of the run digit that sit next to the run absorbed into it. Equal canonical forms plus equal slopes (3 = 3)
  give identical strings for every m at which both formulas hold.
  - i < 9 targets T_{i+1}(m).
  - i = 9 targets T_0(m+1), where the run length is a_0 + 3 + 3m.
- Exact threshold: the smallest m >= 0 with a_i + 3m >= w_i + t_i. It is 0 for all ten templates: every a_i >= 27,
  and w_i + t_i <= 1. So the symbolic argument covers every m >= 0 and leaves no m to brute-force.
- Extra checks (cross-checks only, not part of the proof):
  - exact big-integer RA for m = 0..39 on each template;
  - the symbolic formula Q e^(n-w-t) R compared with exact RA at 12 values of n per template;
  - a direct orbit simulation of 3000 steps.

(3) No palindrome for any m: for each template I find a position j < min(p,s) where digit j from the most
significant end (P[j]) differs from digit j from the least significant end (S's j-th digit from the right). Both
digits are independent of m, so T_i(m) is not a palindrome for every m >= 0.

Induction: x_0 = T_0(0). If x_{10m+i} = T_i(m), closure gives x_{10m+i+1} = T_{i+1}(m) (or T_0(m+1) when i = 9).
So every iterate is some T_i(m), and none of them is a palindrome.

## Jobs and real output lines

Job 2345, `python3 mycheck/check.py . 3000` (my checker):
```
(1) orbit entry x_0 == T_0(0): True
(2) i=0 |P|=52 |S|=52 run d=4 n=30+3m w=0 transient=1 -> e=8, symbolic match=True, valid for m>=0
(2) i=1 |P|=53 |S|=53 run d=8 n=29+3m w=0 transient=0 -> e=4, symbolic match=True, valid for m>=0
(2) i=2 |P|=53 |S|=53 run d=4 n=29+3m w=0 transient=1 -> e=8, symbolic match=True, valid for m>=0
(2) i=3 |P|=54 |S|=54 run d=8 n=28+3m w=0 transient=0 -> e=4, symbolic match=True, valid for m>=0
(2) i=4 |P|=54 |S|=54 run d=4 n=28+3m w=0 transient=0 -> e=8, symbolic match=True, valid for m>=0
(2) i=5 |P|=54 |S|=54 run d=8 n=28+3m w=0 transient=1 -> e=4, symbolic match=True, valid for m>=0
(2) i=6 |P|=55 |S|=55 run d=4 n=27+3m w=0 transient=0 -> e=8, symbolic match=True, valid for m>=0
(2) i=7 |P|=51 |S|=52 run d=8 n=34+3m w=1 transient=0 -> e=4, symbolic match=True, valid for m>=0
(2) i=8 |P|=52 |S|=51 run d=4 n=34+3m w=1 transient=0 -> e=8, symbolic match=True, valid for m>=0
(2) i=9 |P|=52 |S|=52 run d=8 n=33+3m w=0 transient=0 -> e=4, symbolic match=True, valid for m>=0
   exact checks m=0..39: mismatches=0        (printed for each i)
(3) i=0 non-palindrome witness: position 0 from each end (10 vs 9)
(3) i=4 non-palindrome witness: position 1 from each end (11 vs 10)
(3) i=7 non-palindrome witness: position 2 from each end (12 vs 11)
    (every i has a witness)
orbit simulation steps=3000 mismatches=0 palindromes=0 final_len=1034
max threshold: 0
MYCHECK VERDICT: PASS
```
Job 2353 (the same command rerun) produced an identical log. The output is deterministic.

Author commands from REPRODUCE.md, run only after my verdict:
- Job 2350, `python3 code/prove_claim.py result/lychrel_base13.json`:
  `entry: OK at step 0` / `symbolic closure for m >= M0: OK M0 = 0` /
  `exact closure and non-palindromicity for 0 <= m <= 200 (+ special m []): OK` / `CLAIM CHECK: PASS`
- Job 2351, `gcc -O2 -o lo code/longorbit.c && ./lo result/b13.tpl 100000`:
  `RESULT base=13 steps=100000 final_len=30134 template_checks=100001 mismatches=0 palindromes=0`
  (gcc printed only unused-result warnings about fscanf.)

Comparison: the author's M0 = 0 matches my threshold of 0. The carry lemma in the code/rle_check.py docstring
("carries settle after one digit") is the same as my Lemma B. The author's 100000-step C simulation agrees with my
3000-step simulation and with the claimed growth: final length 30134 = 134 + 3*10000.

## Mismatches

None. The base, 13, is not a power of 2 and is not in {11, 17, 20, 26}. Novelty and Wikipedia status are outside
this skeptic's scope and are not assessed here.

pass: true
