# Criterion skeptic

Full criterion clause "new exact term of A002851 at the first order beyond the live b-file" plus two-method agreement plus reproduction of published terms via inverse Euler.

## Clause 1: first order beyond the live b-file
data/b002851.txt (HTTP 200, fetched 2026-11-19T01:52:53Z) ends `20 8832736318937756165`. Index n is vertices/2, so n=21 is 42 vertices, the first order past the file. Odd vertex counts give 0 and are not indexed. Claimed value C(42)=264592224929900091377. I could not re-fetch the live file (no contact allowed), so "live" rests on the saved fetch record. Finding: met, conditional on that record.

## Clause 2: two independent methods agree exactly
- Method A (methodA/engine.py): Cheng-Xu histogram recurrence, exact Python big integers, memoised over histogram states.
- Method D (methodD/D.py, Dsym.py): closed power-sum/configuration-model formula for fixed points and 2-cycles, plus a residual-degree DP or symmetric count-vector DP for long cycles. D.py imports nothing from A (only stdlib), and Dsym imports only D.
- Shared: only the Burnside decomposition, the definition of F(lambda), the weights 1/z_lambda, and the standard internal-edge polynomial P_a (the same mathematical object in both). The recurrences and code differ. This is independent at the code and algorithm level, though not at the level of the underlying theory (same Burnside/orbit-edge model). A shared misreading of that model would be common-mode, but it is tested by the reproduction in clause 3.
- Per type agreement: 53174 of 53174 cycle types of N=42 give identical F_D (mod 2^521-1) and F_A.
- Modular gap: F(lambda) is at most F(1^42), the labeled cubic count, which has 72 digits, far below 2^521-1 (157 digits). So each residue is the exact value and modular arithmetic is not a gap. The argument is valid because a fixed graph is a labeled graph.
- Total agreement: the C port of A (mod p and CRT) and the exact Python A both give U(42)=264928974203634896907, equal to the D sum.

Commands run:
```
$ python3 -I s.py <claim>     (sums py42.csv F_A/z; compares to D lanes per type)
53174 53174 0 264928974203634896907      # types_A types_D per-type-mismatch U_A
$ cut -d';' -f4 results/D_N42_lane*.txt | sort | uniq -c
  53174 ok
$ spot type (6,6,4,4,4,3,3,3,3,3,3): F_Dsym = 2250892833300 ; F_A = 2250892833300
```
Finding: met. Caveat: the Python A column in the lane files was copied from py42.csv, but I recomputed the comparison from both files and from independent spot calls.

## Clause 3: same code reproduces published terms and A005638 via inverse Euler
My own script (python3 -I, own inverse Euler written from the log-derivative identity) used Dbfile_lane0/1 (D's U(N), even N=2..40) and U(42), against data/b002851.txt (n=1..20) and data/b_A005638.txt (n=0..20):
```
[2, 4, ..., 40]
terms 21 21 bad 0 C42 264592224929900091377 True
```
All 20 connected terms and all 20 A005638 terms match exactly, and the inverse Euler transform of D's U gives the claimed C(42). Note: data/b_A005638.txt is labelled "synthesized from sequence entry", not a true OEIS b-file, but it covers n<=20 and the match is exact. U(N) for N=2..40 comes from the same D code (bfileD.py), but the saved lane files are outputs I did not regenerate; I verified them against the published data. Finding: met.

## Null models
Not applicable: exact integers verified deterministically; I agree. The residual risks are a common-mode error in the shared Burnside model (excluded by exact reproduction of 40 published terms) and the unverified liveness of the b-file.

confirmed_scope: A002851(21)=264592224929900091377 (connected cubic graphs on 42 vertices, one order beyond a saved b-file ending at n=20) is obtained by two separately coded Burnside-type methods that agree on all 53174 cycle types and on U(42)=264928974203634896907, with the method-D code reproducing A002851(1..20) and A005638(1..20) exactly through the inverse Euler transform.
context: subagent (fresh, sonnet)
pass: true
