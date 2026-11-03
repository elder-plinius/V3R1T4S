context: subagent (reproduce)

# REPRODUCE skeptic — claim: (9,3,4)_4 edit-metric DNA code with GC + reverse-complement constraints, k = 1042

Started fresh with only a scratch copy of `claim/`; worked only from that copy. Did not read other panel files, dossiers or reports.
Box load during the work: load average ~66-70 on 8 cores, MemAvailable ~6.9 GB. Every job ran at `nice -n 19`. The regen used about 40 MB RSS (well under rule 10).
Times are EST, 2026-11-03.

## Definition used (quoted)
From `sources/sun_thesis_tables_webfetch_1938Z.txt` (Sun 2010, Sec 1.5 as transcribed):
> "Constraint set (Sec 1.5): d_edit(x,y) >= d for x != y; d_edit(x^RC, y) >= d for all x,y in C including x = y; GC weight w = floor(n/2) (=4 for n=9)."
> "Edit distance = Levenshtein (substitution, insertion, deletion)."

From that definition, required here: every word has length 9 over {A,C,G,T}; the words are distinct; each word has exactly 4 C/G; Levenshtein(x,y) >= 3 for distinct x,y; Levenshtein(x, rc(y)) >= 3 for all x,y including x = y. Here rc means reverse, then complement A<->T, C<->G. The claimed size is 1042.

## 1. Own checkers, written BEFORE reading any author code
Two separate methods:

(a) `mycheck.c`: full Levenshtein DP on all 542,361 unordered distinct pairs, plus all 1042×1042 (x, rc(y)) pairs including x = y. It also checks length, alphabet and GC count.
```c
static int lev(const char*a,int n,const char*b,int m){int D[64][64];
 for(int i=0;i<=n;i++)D[i][0]=i; for(int j=0;j<=m;j++)D[0][j]=j;
 for(int i=1;i<=n;i++)for(int j=1;j<=m;j++){int c=D[i-1][j-1]+(a[i-1]!=b[j-1]);
  if(D[i-1][j]+1<c)c=D[i-1][j]+1; if(D[i][j-1]+1<c)c=D[i][j-1]+1; D[i][j]=c;} return D[n][m];}
/* rc: R[k][i]=comp(w[n-1-i]); loops: i<j lev(W[i],W[j]) ; all i,j lev(W[i],R[j]) ; gc==n/2 ; len==n ; alphabet ACGT */
```
(b) `ballcheck.py`: a second method that uses no DP. For each codeword it lists the whole edit ball of radius d-1 = 2: every string reachable with at most 2 unit insertions, deletions or substitutions. It then checks that this ball contains no other codeword and no reverse complement of any codeword, its own included. It also checks distinctness, length, alphabet, GC = 4, a trailing newline and the absence of CR characters.

Commands, run from a copy of claim/ (my tools in a sibling scratch dir):
```
sha256sum object/code_n9_d3_k1042.txt
wc -l object/code_n9_d3_k1042.txt ; sort object/code_n9_d3_k1042.txt | uniq -d | wc -l
nice -n 19 ./mycheck 9 3 object/code_n9_d3_k1042.txt
nice -n 19 python3 ballcheck.py 9 3 object/code_n9_d3_k1042.txt
```
Results:
- sha256 = b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a: **matches the claim**.
- 1042 lines, 0 duplicates, 1042 distinct words.
- mycheck: `lines=1042 words=1042 n=9 d=3 w=4 pairs=542361 min_d=3 min_d_rc_all=3 min_d_rc_self=3 bad=0 -> VALID` (**PASS**)
- ballcheck: `words 1042 distinct 1042 props_ok True bad 0 VALID` (**PASS**)
- The claimed minima are tight: min d(x,y) = 3, min d(x,rc(y)) = 3, and min d(x,rc(x)) = 3.

Negative controls: both of my checkers must reject each of these, and both did (all **INVALID**):
- neg1: a duplicate word (min_d=0).
- neg2: a word plus its own rc (min_d_rc=0).
- neg3: two GC-4 words 2 substitutions apart (min_d=2).
- neg4: words with GC weight 4 broken (AAAAACCCC, GGGGGAAAA).
- neg5: the single word ACGTACGTA, whose d(x,rc(x)) = 2. This shows the x = y reverse-complement case is enforced.

## 2. Author checkers (run only after step 1)
```
gcc -O2 -o check2 checkers/check2.c && ./check2 9 3 object/code_n9_d3_k1042.txt   -> VALID 1042 words n=9 d=3 gc=4 min=3
python3 checkers/check_dna.py 9 3 object/code_n9_d3_k1042.txt                    -> VALID 1042 n=9 d=3 w=4 min_cross_distance=3 (exit 0)
python3 checkers/check3.py 9 3 object/code_n9_d3_k1042.txt                       -> VALID 1042 n=9 d=3 w=4 min=3 (exit 0)
python3 checkers/check4.py 9 3 object/code_n9_d3_k1042.txt                       -> VALID 1042 n=9 d=3 w=4 min=3 (exit 0)
```
All 4 **PASS**, and they agree with my checkers.

## 3. Full same-seed regeneration (deterministic): PASS
`search/dnae.c` sha256 b4a39bfb177aa436f575f73c0ddf3393f77ae56b483721fe543dbdc613a21a81 matches the claim.
I read the code after steps 1–2. It uses a seeded xorshift PRNG. Wall-clock time only decides when the run stops; it never affects which move is chosen. So the iteration path for a fixed seed and restart length is deterministic.
```
gcc -O2 -o dnae search/dnae.c -lm
nice -n 19 timeout 1260 ./dnae 9 3 2 103 1200 out/p 20000 1042      # started 15:26:24 EST, finished 15:42:55 EST, exit 0
cmp out/p_n9_d3_G2_k1042.txt object/code_n9_d3_k1042.txt
```
Results:
- Header lines are identical to `search/orig_log_n9_d3_G2_s103.txt`: `n=9 d=3 w=4 valid=63224 ...` and `G=2 Korbits=15806 admissible=15084`.
- With the t= wall-time fields removed, all 521 FOUND lines are identical to the original log, ending with `FOUND k=1042 it=8159505 restarts=404`. My run printed `BEST 1042 its=8159505 restarts=404 t=379.7`.
- `cmp` shows the regenerated `p_n9_d3_G2_k1042.txt` is **byte-identical** to `object/code_n9_d3_k1042.txt` (same sha256 b51b30e3...a93a). My checker also passes on the regenerated file.
- There was no non-determinism.

## 4. Scope notes (not part of REPRODUCE)
I did not re-fetch the bar value (Sun 2010 Table 7.1 (9,3) = 939g) or check novelty or literature. Those belong to the NOVELTY and CRITERION panelists.
Arithmetic only: if the claim's quoted 939 is right, 1042 > 939 by 103. The claim's sources also say the cell is not marked exact. I did not verify that against the live source.
I did not regenerate the pre-existing 1011 object (G=0 seed 7). It is not claimed.

## Verdict
Every property and the claimed value of 1042 check out against the saved object, using two independent checkers of my own (validated by negative controls) and all four author checkers. A full same-seed regen reproduced the object byte for byte, and its log matched the original iteration for iteration. No mismatch, no missing object, no non-determinism.

pass: true
