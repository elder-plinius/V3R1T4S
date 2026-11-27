# Proof: gamma_2 >= m/K from an adaptive-strip certificate

Notation. A = a_1 a_2 ..., B = b_1 b_2 ... are independent uniform binary sequences. L(x,y) is the length
of a longest common subsequence of A_x = a_1..a_x and B_y = b_1..b_y. gamma_2 = lim E L(n,n)/n = sup_n E L(n,n)/n
(Fekete: E L(m+n,m+n) >= E L(m,m) + E L(n,n)). N >= 1 is the window size. The main certificate has N = 17,
K = 2^24, m = 13332272 (object/), giving gamma_2 >= 13332272/2^24 = 833267/1048576 = 0.794665336609...

## 1. The process

A full state is (h, b) with h, b in {0,1}^N (positions p = 0..N-1). The process also carries, for the proof only,
counters x (characters of A read), y (characters of B read), l = y - N, and integers F_0..F_N with
F_{p+1} - F_p = h_p. Column of position p is l+p+1, b_p = b_{l+p+1} and F_p belongs to column l+p.

Start: x = 0, y = N, l = 0, F all 0, so h = 0, and b = (b_1..b_N). Each step is one of two actions, chosen by a fixed
policy pi as a function of the state only:

ROW: read a = a_{x+1}. Put F'_0 = F_0 and, for p = 0..N-1,
    F'_{p+1} = max(F_{p+1}, F'_p, F_p + m_p), where m_p = 1 if b_p = a, else 0.
Then x increases by 1. Reward 0. b unchanged.

SHIFT: read c = b_{y+1}. New frontier (F_1, ..., F_N, F_N), new window (b_1..b_{N-1}, c) in positions 0..N-1. y and l
increase by 1. Reward r = h_0 = F_1 - F_0.

So the sum of rewards up to time t is F_0(t) - F_0(0) = F_0(t).

## 2. The update stays in increment form

Claim: in ROW, with v_p = F'_p - F_p, always v_p and h_p are in {0,1}, and with x_p = h_p | v_p | m_p:
F'_{p+1} = F_p + x_p, h'_p = x_p - v_p, v_{p+1} = x_p - h_p, all in {0,1}.
Proof: v_0 = 0. Given v_p, h_p in {0,1}: the three terms of the max equal F_p + h_p, F_p + v_p, F_p + m_p, so the max
is F_p + x_p. x_p >= v_p and x_p <= 1 give h'_p in {0,1}; x_p >= h_p gives v_{p+1} in {0,1}. So the next state is a
function of (h, b, a) only. SHIFT trivially keeps it (new last increment 0).

## 3. Every frontier value is the length of a real common subsequence

Invariant: at every time, for each p = 0..N, F_p <= L(x, l+p) (indeed some common subsequence of A_x and B_{l+p} has
length F_p).
Start: F = 0. ROW: F'_0 = F_0 <= L(x,l) <= L(x+1,l). Inductively for p: F_{p+1} <= L(x,l+p+1) <= L(x+1,l+p+1);
F'_p <= L(x+1,l+p) <= L(x+1,l+p+1); and F_p + m_p <= L(x+1,l+p+1), because if m_p = 1 then a common subsequence of
A_x, B_{l+p} extends by the pair (a_{x+1}, b_{l+p+1}), which are equal. SHIFT: the new index l' = l+1; for new position
p < N the value is the old F_{p+1} <= L(x, l+p+1) = L(x, l'+p); for p = N the value is old F_N <= L(x, l+N) <= L(x, l'+N).
Hence the total reward R_t = F_0(t) <= L(x_t, l_t) <= L(x_t, y_t), for every outcome.

## 4. The reduced state and the Markov property

Complement: let c(h,b) = (h, not b), and canon(h,b) = (h,b) if b_{N-1} = 0, else c(h,b). Row(h, not b, not a) = Row(h,b,a), since m_p
depends only on (b_p = a); Shift((h, not b), not c) = c(Shift((h,b),c)), with the same reward. The policy pi and the
potential V are defined on canonical states and extended by pi(c s) = pi(s), V(c s) = V(s).

At each time the next character read (a_{x+1} or b_{y+1}) has an index that is a function of the characters already read, and it has
not been read; so conditionally on the past it is uniform. With the state process s_t: for action ROW s_{t+1} = (Row(s_t, a), b), a
uniform; for action SHIFT, likewise with c uniform.

## 5. The certificate

Integers K > 0, m, a finite set S of canonical states, pi: S -> {ROW, SHIFT}, V: S -> Z, such that:
(C1) (h = 0, b) is in S for every canonical b. (Start, in canonical form.)
(C2) S is closed: for s in S, canon of both successors under pi(s) are in S.
(C3) for s in S with pi(s) = ROW: V(next_0) + V(next_1) - 2 V(s) >= m;
     for s in S with pi(s) = SHIFT, with r = h_0: 2 K r + V(next_0) + V(next_1) - 2 V(s) >= m.
By the symmetry of step 4 the same statements hold for complemented states with the two successors exchanged, so the inequality holds at
every state of the process. checkers/check_a17.c, checkers/check_d.c and checkers/check_e.c test C1, C2, C3 in full, exactly, in integers, each on all states (64-bit sums of values below 2^31 and 2K).

## 6. Telescoping

By C3, E[K r_{t+1} + V(s_{t+1}) | past] - V(s_t) >= m/2 for each t. Summing t = 0..T-1 and taking expectation:
K E[R_T] + E V(s_T) - E V(s_0) >= T m/2. S is finite, so |V| <= V_max, and E[R_T] >= T m/(2K) - 2 V_max/K.

## 7. From reward per character to gamma_2

x_T + y_T = N + T =: n (each step reads one character; y_0 = N). The policy may read different numbers of each string,
so a conversion is required.
Lemma 1. For fixed x + y = n, E L(x,y) <= n gamma_2 / 2. Proof: let A', B' be independent copies. Concatenation gives
L(A_x A'_y, B_y B'_x) >= L(A_x,B_y) + L(A'_y,B'_x), so E L(n,n) >= E L(x,y) + E L(y,x) = 2 E L(x,y), since the strings are
exchangeable, and E L(n,n) <= n gamma_2 (the sup).
Lemma 2. E max_{x+y=n} L(x,y) <= n gamma_2/2 + sqrt(n ln n) + 2. Proof: L(x,y) is a function of n independent characters
changing by at most 1 when one changes; McDiarmid: P(L(x,y) >= E L(x,y) + t) <= exp(-2 t^2 / n). With t = sqrt(n ln n) and a union
bound over n+1 pairs the probability is <= (n+1)/n^2; on that event the max is <= n. Total extra <= t + (n+1)/n <= t + 2.
By step 3, R_T <= max_{x+y=n} L(x,y) for every outcome (x_T, y_T are random, but this bound is uniform). So
T m/(2K) - 2 V_max/K <= E R_T <= (N+T) gamma_2/2 + sqrt((N+T) ln(N+T)) + 2. Divide by T, let T -> infinity:
m/(2K) <= gamma_2/2, that is

    gamma_2 >= m/K.

## 8. Tests of the steps

- tests/exact_small.py: exact gain by Fractions, compared with m/K, and exhaustive check of F_p <= L for all reveal sequences (step 3). Runs on object/small_old/.
- tests/sim_check.py: step 3 on long random strings, with a plain DP.
- tests/sim_rate17.c: long simulation against m/K (NUMERICAL).
- checkers/check_a17.c, checkers/check_d.c, checkers/check_e.c: C1 to C3; negative controls in REPRODUCE.md.
- tests/lemma1_small.py: exact enumeration of Lemma 1 for x + y <= 7.
