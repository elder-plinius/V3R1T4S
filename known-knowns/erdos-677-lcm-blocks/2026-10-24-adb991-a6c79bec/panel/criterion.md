# Panel: criterion skeptic, erdos-677-lcm-blocks (claim/)

context: subagent (fresh context, Claude Code Agent tool)

**What I read.** Only claim/ (CLAIM.md, REPRODUCE.md, object/, checker/, source/). Every sha256 listed in claim/CLAIM.md matches its file. My scratch scripts and logs are in panel_work/criterion/ in the run folder.

**Web.** Two search-engine queries. One fetch of the Erdős Problems forum thread for #677 failed with a DNS error and was not retried.

**Verdict.** The claim meets the first enumerated partial win literally, and it meets pre-registered judge item 3. As far as I can check it is correct, reproducible and independently corroborated. It is a modest result, in the regime where the problem is structurally easy.

## 1. Is the stated range a genuine range of (n, k), uncapped in m?

**Semantics.** checker/spec_677.lean is verbatim from source/fc_Erdos677.lean and source/fc_GCDMonoid_Finset.lean.
- m, n and k range over ℕ. So n = 0 and m = n + k (adjacent blocks) are both instances, and k > 0 means k ≥ 1.
- On ℕ, `Finset.Ioc n (n+k)` is {n+1, …, n+k}, whose elements are all ≥ 1, and `Finset.lcm id` is the ordinary lcm. So `lcmInterval n k` = lcm(n+1, …, n+k).
- The statement only quantifies over m ≥ n + k, so n always starts the lower block. The range condition n ≤ 5871·k therefore constrains only the lower block.

**Coverage**, checked against object/PROOF.md and object/range_nCk.py:
- **k = 1:** Step 0, since m+1 > n+1.
- **n = 0:** included; the program allows N = k (lo ≥ k).
- **m = n + k:** included; hi = min(m, 5872·k) allows N = m.
- **m ≥ 2010760:** excluded for every k ≥ 2 by Step S2.
- **m ≤ 2010759:** every prime-free block (m, m+k] with k ≥ 2 is visited. This means every m in [a, b−3] for consecutive primes a < b with a ≤ 2010760. Blocks with m < 2 contain the prime 2.
- **k ≥ 148:** covered by proof alone. The largest prime gap below 2010881 is 148 (from 2010733 to 2010881), so no prime-free block of length 148 or more has m ≤ 2010759. Step S2 handles every larger m.

**Assessment.** Nothing is quietly excluded. The range is an infinite cone, not a box, so it says nothing about, for example, k = 3 with n > 17613. That is a limitation, not a stretch: the partial win asks for "a stated range of (n, k)", and this range is stated exactly.

## 2. Are the candidate m's provably complete?

I checked each step of object/PROOF.md.

- **S0 is correct.**
  - If p^e divides b, and b divides lcm(A), then p^e divides some a ≤ N.
  - Elements of B exceed N, so none of them is a prime power, and in particular none is prime.
  - A prime P > k divides an element of (N−k, N] exactly when N mod P < k. The case N < P cannot occur, because N ≥ k.
- **S1 is correct.**
  - v_p(D(X)) = Σ_e (c_e − 1)^+, where c_e is ⌊k/p^e⌋ or ⌈k/p^e⌉. This gives k!/lcm(1..k) ≤ D(X) ≤ (k−1)!.
  - Because m ≥ n, the ratio (m+i)/(n+i) is non-increasing in i. This gives (E1): k(m+k)^k ≤ lcm(1..k)·N^k.
  - Rosser–Schoenfeld 1962 then gives c_k < e^{1.03883} = 2.8259088 < 2.8260.
- **S2 is correct.**
  - N ≤ 5872·k gives m + k < 16594.3·k.
  - Schoenfeld 1976 gives a prime p in (m, m(1 + 1/16597)), and p must exceed m + k.
  - So k < m/16597 < m/16593.3 < k, a contradiction for every m ≥ 2010760.
- **S3 is correct.** Each filter (a)–(f) is a necessary condition, and object/range_nCk.py implements each one soundly:
  - the block enumeration is complete;
  - P1 and P2 are the two largest distinct primes dividing elements of B, and each is used only if it exceeds k;
  - the N-windows list every N with N mod P1 < k;
  - floating point only loosens the filters (c_k·(1+1e-9), truncation minus 1, and 2.8260 > 2.82591);
  - (E1) and the final lcm equality are tested in exact integers.

**The cited results.** To my knowledge both are stated correctly: RS62 Theorem 12 (ψ(x) < 1.03883x for x > 0) and Sch76 Theorem 12 (a prime in (x, x(1 + 1/16597)) for x > 2010759.9). I could not read the papers here, but three numerical checks are consistent with them:
- the supremum of ψ(x)/x over prime powers x ≤ 10^6 is 1.0388206, reached at x = 113, which is below 1.03883;
- the gap of 148 after 2010733 breaks the 1/16597 property exactly for x < 2010759.848, which matches Schoenfeld's threshold of 2010759.9;
- the property has no violation for x in (2010759.9, 2.99·10^6).

**Are cited theorems acceptable for "provably complete"?** Yes. The pre-registration's own example, a Størmer/Lehmer argument, also rests on classical theorems. But the result is conditional on these two papers:
- Sch76 is essential for every m ≥ 2010760, and therefore for all k ≥ 148.
- RS62 is used only for the uniform bound c_k < 2.826 at large k. For k ≤ 3000 I computed c_k ≤ 2.7437 directly.

## 3. Is the certificate checkable and saved?

**Saved.** The certificate is object/range_nCk.py, its output object/out/range_nCk_C5871.txt, and object/PROOF.md.

**Reproduced.** I ran claim/REPRODUCE.md (python3 -I, nice 15, one core). The output was byte-identical (sha256 84b1d82f…). It took 134 s and about 107 MB of resident memory.

**Independent check** (panel_work/criterion/indep_check.py, my own code, using a different method):
- For every 2 ≤ k ≤ 147 it bounds m only by (E1), using the exact lcm(1..k). That allows m up to 2,187,014, which is beyond 2,010,759. So for these k it uses neither RS62 nor Sch76.
- It tests every maximal prime power q > k of lcm(B) (N mod q < k), not just two primes.
- Result: 880,576 feasible prime-free (m, k) pairs and 17,484,366 windowed candidates. None has lcm(B) dividing lcm(A), and there are no counterexamples. It ran in 35 s.
- Its divisibility test agrees with direct lcm computation on 3000 random triples. Its window logic and its smallest-N logic for (E1) agree with brute force.

**Filter-free brute force** (panel_work/criterion/brute_small_k.py):
- It computes the exact lcm values for 1 ≤ k ≤ 12 and every m up to the (E1) bound.
- It finds no disjoint coincidence with n ≤ 5871·k, and 98 overlapping ones.

**Weaknesses (not disqualifying).**
- No per-case witnesses are saved, so checking the certificate means re-running it.
- The two "validation" lines in the saved output each count 0 triples, so they are not a positive control.
- The program's docstring cites "NOTES.md, Theorem S", which is not in the package, and its step labels differ from object/PROOF.md.

## 4. Is this a genuine, non-subsumed win?

**How far classical or simple arguments reach in n/k.** I quote the cited prime-gap constants from memory.
- **The size bound (E1) alone** gives no uniform bound. It excludes k = 2 entirely (c_2 = 1), and otherwise only small n for small k.
- **Sylvester–Schur** says a prime > k divides ∏B when m ≥ k. With its strengthenings this gives only N > k (or about 2k), so n/k = O(1).
- **Grimm-type results** give no direct bound on n/k.
- **Explicit Bertrand-type bounds** say a prime lies in (x, x(1 + ε)]. Combined with (E1) they give n/k ≳ (1/ε)/2.83 − 1:
  - Bertrand: nothing.
  - Nagura (ε = 1/5, x ≥ 25): about 1.
  - Dusart 1998 (ε = 1/(2 ln² x), x ≥ 3275): about 45, plus a tiny check for m < 3275.
  - Schoenfeld 1976: 5871, but only for m ≥ 2010760.

The computation over m ≤ 2010759 (where k ≤ 147) is what lifts the uniform bound from tens to 5871. So the range is neither trivial nor a direct corollary of classical results.

**Literature, as far as I could see.**
- The JSP catalog lists the problem as Open (source/jsp_entry_JSP-000550.txt), and formal-conjectures marks it research open.
- Search-engine snippets of the Erdős Problems page mention only two things: Thue–Siegel gives finitely many solutions for each fixed k (ineffective, so not subsuming), and some examples with different block lengths.
- I found no published or forum range verification. Caveat: I could not read that site's page or forum directly.

**Nothing is presented as more than it is.** claim/CLAIM.md says this is neither a full solution nor a prize solution, and the constant is honest. Schoenfeld's 16597 caps this method at C ≈ 5872, so 5871 is the natural endpoint of a classical method, not the product of a new idea.

## 5. Null model

**Overlapping coincidences are real.** lcm(3,4,5) = lcm(4,5,6) = 60, which is (n, m, k) = (2, 3, 3). There are 98 such coincidences for k ≤ 12 inside the cone, for example (1, 2, 4), (0, 1, 5), (4, 5, 5) and (9, 10, 5).

**Disjoint coincidences with different lengths occur at tiny sizes.** M(4,3) = M(13,2) = 210 and M(3,4) = M(19,2) = 420; I verified both.

**Disjoint coincidences with equal lengths are absent.** More strongly, inside the cone not even the one-sided relation "lcm(B) divides lcm(A)" ever holds:
- none among the 17.5M residue-filtered candidates for k ≤ 147;
- none in the wider cone n ≤ 20000·k for k ≤ 10.

**Why the cone is easy.** Steps S0–S2 use only the fact that lcm(B) divides lcm(A). Inside the cone they force B to be a short prime-free block in (N, 2.83N] with N ≤ 5872·k. That in turn forces k ≤ 147 and m ≤ 2010759. The residue conditions then eliminate every candidate before equality is even in question.

**Effect on the win.** So yes, the statement is "easy" in this range. The verification confirms what a null model predicts, and it says nothing about n/k > 5871. That is where long prime-free blocks inside (N, 2.83N] exist and where the real difficulty lies. This lowers the result's weight as evidence for the conjecture. It does not lower the literal partial win, which asks for an exhaustive, uncapped range verification, not a hard or surprising one.

## 6. Decision

The literal criterion is met:
- every (n, k) with k ≥ 1 and 0 ≤ n ≤ 5871·k is covered;
- there is no cap on m, and completeness of the m's is proved from cited explicit theorems;
- the certificate is saved and reproducible;
- the claim invokes the first enumerated partial win, not a stretched variant of it.

Pass, with the scope below.

confirmed_scope: Computer-assisted and relying on the cited explicit prime bounds of Rosser–Schoenfeld 1962 (ψ(x) < 1.03883·x for all x > 0) and Schoenfeld 1976 (a prime in (x, x(1 + 1/16597)) for every x > 2010759.9), object/PROOF.md together with the reproduced run of object/range_nCk.py 5871 shows that lcm(m+1, …, m+k) ≠ lcm(n+1, …, n+k) for every k ≥ 1, every n with 0 ≤ n ≤ 5871·k and every m ≥ n + k with no cap on m, i.e. every instance of Erdos677.erdos_677 with n ≤ 5871·k holds — an informal, not kernel-checked result that meets the first enumerated partial win and is not a solution of the problem.

pass: true
