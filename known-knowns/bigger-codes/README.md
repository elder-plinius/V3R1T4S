# Binary constant-weight codes: 30 explicit codes and 5 Delsarte LP certificates

A(n, d, w) is the largest size of a binary code of length n, constant weight w and minimum Hamming distance d. The
table of record is A. E. Brouwer's *Bounds for binary constant weight codes* (https://aeb.win.tue.nl/codes/Andw.html),
which lists a lower bound (an explicit code) and an upper bound for each cell and asks for "corrections and updates"
by email.

**Claim (exact scope), as of 2026-10-10.** The 30 files in `codes/` are valid binary constant-weight codes (distinct
words, weight exactly w, pairwise distance ≥ d) whose sizes **strictly exceed the lower bound printed in Brouwer's
table** in the version `Last-Modified: Sat, 10 Oct 2026 11:57:45 GMT`, fetched 2026-10-10T19:23:48Z with one plain
curl GET (sha256 of the page `0f1b51bf71c0ca91aef82eef740cb0dd9f6be6c4014983213d0eefe0eb631cee`, 127,021 bytes;
`the-record-we-beat/*2026-10-10T19-23-48Z*`), and none reaches the printed or Johnson upper bound of its cell. An earlier
snapshot of the version of 4 Oct 2026 (`the-record-we-beat/*2026-10-08T23-29-37Z*`) is kept for the record.

Table cells move fast: two of our earlier candidate cells were overtaken by another contributor before this release
and are not included. Two of the cells below also moved without overtaking us: A(33,8,8) is now 1 806 [Ol] (Antoine Olivier, email 2026-10-10;
ours 1 809, margin +3, was +9) and A(34,8,8) is now 1 960 [YZW] (Yang et al., now in the table; ours 1 965, +5). The 5 files in `certificates/` are exact rational Delsarte
linear-programming dual certificates proving upper bounds in five cells for which that table version prints only the
Johnson bound. Everything else (kissing-number corollaries, an A(32,8,8) code of size 1676 that only ties a published
value) is **not** claimed.

**Update 2026-10-17.** A. E. Brouwer now lists 27 of the 30 codes in his table, credited as
[Pl] (Andw.html, Last-Modified Sat, 17 Oct 2026 16:06:01 GMT). The other three were overtaken in his table first: A(34,8,7) by [Fr] (603, 14 Oct 2026) and A(29,6,10)
and A(29,6,11) by [Dz] (27183 and 42042, 15 Oct 2026). In this repository A(26,6,9) has since been improved to 5997 by a
contributor (pull request #352). The status paragraph below is kept as written at release.

**Status.** Found by agents (see `READ_BEFORE_CITING.md` at the repository root), verified only internally, and **not yet sent to
A. E. Brouwer** at the time of this release; until he lists them, the correct description is "exceeds the printed
lower bound in the 10 Oct 2026 version of the table". Every code is a *polish* of somebody else's code: the seed of
each cell is named below and in `INDEX.csv`, and in the table's own convention credit for a polished code goes with
the submission, so these are small steps on the work of Boisclair, Gangl, Gippini, Lysenstøen, Echols, Graham–Sloane
and the archive contributors, not discoveries. Ten of the 30 margins are +1 to +3 words and are likely to be erased
by the next table update.

## The 30 codes

Table values are from the 2026-10-10 fetch above (`the-record-we-beat/parsed_cells_2026-10-10T19-23-48Z.tsv`, parsed with
`the-record-we-beat/parse_brouwer_table.py`; "[Bo]" etc. are the table's own source labels). "Other published" lists the best value
we found outside the table (arXiv:2608.13906 Echols, arXiv:2609.35051 Yang et al., arXiv:2603.00174 Rosin,
Zenodo 23075336 Gippini). Full rows, including sha256 and the method, are in `INDEX.csv`.

| cell | ours | table lower bound | margin | table / other published upper bound | seed code (credit) |
|---|---|---|---|---|---|
| A(25,6,11) | 8718 | 8698 [Bo] | +20 | 24630 | Boisclair a25.6.11.8698H |
| A(25,6,12) | 9895 | 9880 | +15 | 30587 | archive a25.6.12.9880H (2010) |
| A(26,6,8) | 3603 | 3602 [E] | +1 | 7891 | Echols a26.6.8.3602H |
| A(26,6,9) | 5986 | 5761 [Bo] | +225 | 16122 | Boisclair a26.6.9.5761H |
| A(26,6,11) | 12222 | 12206 | +16 | 42017 [Mo] | archive a26.6.11.12206H |
| A(26,6,13) | 16225 | 16117 | +108 | 61174 | archive a26.6.13.16117H |
| A(27,6,9) | 8325 | 8324 [Ga] | +1 | 23673 | Gangl a27.6.9.8324H (email to Brouwer 2026-10-04) |
| A(27,8,10) | 1737 | 1728 [Bo] | +9 | 4986 (Echols 1727, Rosin 1704) | Boisclair a27.8.10.1728H |
| A(27,8,11) | 2421 | 2404 | +17 | 7754 [KT] | archive a27.8.11.2404H |
| A(28,8,9) | 1406 | 1376 [Bo] | +30 | 3855 (Echols 1375) | Boisclair a28.8.9.1376H |
| A(28,8,11) | 3785 | 3773 | +12 | 11896 [KT] | archive a28.8.11.3773H |
| A(28,8,12) | 4962 | 4927 | +35 | 17008 [KT] | archive a28.8.12.4927H |
| A(28,8,14) | 6359 | 6218 | +141 | 22710 [S] | archive a28.8.14.6218H |
| A(29,6,10) | 25974 | 25896 [Gi] | +78 | Johnson 90465 | Gippini a29.6.10.25896H (Zenodo 23075336, 2026-10-01) |
| A(29,6,11) | 41219 | 41216 [gs] | +3 | Johnson 167926 | Graham–Sloane class + 4 free words |
| A(29,6,12) | 61823 | 61820 [gs] | +3 | Johnson 242434 | Graham–Sloane class + 3 free words |
| A(30,8,8) | 1166 | 1163 [Bo] | +3 | Johnson 2313 (Echols 1162) | Boisclair a30.8.8.1163H |
| A(33,8,8) | 1809 | 1806 [Ol] | +3 (was +9 over 1800 [L] on 4 Oct) | Johnson 4092 | Lysenstøen a33.8.8.1800H |
| A(34,8,7) | 602 | 601 [Bo] | +1 | 1175 (Echols 600) | Boisclair a34.8.7.601H |
| A(34,8,8) | 1965 | 1960 [YZW] | +5 (was +16 over 1949 [L] on 4 Oct) | Johnson 4585 | Lysenstøen a34.8.8.1949H |
| A(35,6,6) | 2217 | 2209 [Bo] | +8 | 3249 (Echols 2204) | Boisclair a35.6.6.2209H |
| A(45,8,7) | 1907 | 1904 [Bo] | +3 | 4050 (Echols 1885) | Boisclair a45.8.7.1904H |
| A(51,6,5) | 1785 | 1783 [Bo] | +2 | 2040 | Boisclair a51.6.5.1783H |
| A(51,6,6) | 11184 | 11156 [Bo] | +28 | 16660 | Boisclair a51.6.6.11156H |
| A(52,8,7) | 3799 | 3797 [Bo] | +2 | 7577 (Echols 3796) | Boisclair a52.8.7.3797H |
| A(53,8,7) | 3987 | 3980 [Bo] | +7 | 8003 (Echols 3979) | Boisclair a53.8.7.3980H |
| A(54,8,7) | 4193 | 4173 [Bo] | +20 | 8447 (Echols 4172) | Boisclair a54.8.7.4173H |
| A(55,8,7) | 4426 | 4417 [Bo] | +9 | 9617 (Echols 4386) | Boisclair a55.8.7.4417H |
| A(56,8,7) | 4685 | 4674 [Bo] | +11 | 10264 | Boisclair a56.8.7.4674H |
| A(58,6,5) | 2684 | 2678 [Bo] | +6 | 2969 (Echols 2677) | Boisclair a58.6.5.2678H |

Largest gains: A(26,6,9) +225, A(28,8,14) +141, A(26,6,13) +108, A(29,6,10) +78, A(28,8,12) +35. For the two
A(n,8,8) cells: in the 10 Oct table A(34,8,8) carries Yang et al.'s 1960 ([YZW], arXiv:2609.35051) and A(33,8,8)
carries Antoine Olivier's 1806 ([Ol]); Yang et al. give 1803 for A(33,8,8). Our seeds for both cells are Christian
Lysenstøen's codes ([L] in the 4 Oct table).

**Not claimed:** A(32,8,8) ≥ 1676, which our agents also found, only ties the 1676 of Yang et al. §5.5 (now in the
table as 1676 [YZW]) and is not included. The kissing-number corollaries τ_33 ≥ 364 736 and τ_34 ≥ 384 836 that would follow from the A(33,8,8) and
A(34,8,8) codes via the Edel–Rains–Sloane formula have **not** been verified by an explicit Gram-matrix check and are
not claimed here.

### How the codes were found

Local search warm-started from the seed codes: an exact *large-neighbourhood search* that repeatedly removes a small
set R of codewords (|R| ≤ 12, chosen as words that jointly block many candidate words), enumerates every weight-w word
compatible with the remaining code (a candidate may be blocked by at most 4 removed words), solves the maximum
independent set on the conflict graph of the candidates exactly, and accepts the move if it does not shrink the code
(a plateau walk). Two cells (A(29,6,11) and A(29,6,12)) instead start from a Graham–Sloane code and add an
exact maximum independent set of the words that are free with respect to it; the table itself notes that
Graham–Sloane codes "are not always maximal", so these cells are the weakest novelty claims here.
On the nine cells where this was measured, the codes differ from their seeds in between 1 % (A(27,6,9), A(26,6,8))
and 17 % (A(26,6,9)) of the words. The search code, the exact command chain and random seeds of every code and
certificate, and the sha256 of each archive seed file are in [`how-we-built-it/`](how-we-built-it/README.md) (25 of
the 30 codes and all 5 certificates come from seeded, deterministic command chains; the five A(n,8,7) walks cannot be
replayed exactly, see there); the story is in [`HOW_WE_FOUND_IT.md`](HOW_WE_FOUND_IT.md). The claim still rests on
the files and the checkers only.

### Checking the codes

Each code is a text file, one word per line as a 0/1 string of length n (file name `A<n>_<d>_<w>_<M>.txt`).
`verify-it-yourself/cwcheck.py FILE n d w` (python3 + numpy) checks the format, the weights, distinctness, all M(M−1)/2 pairwise
Hamming distances (XOR + popcount, with the full distance histogram) and, by a second route, that no two words share
t = w − d/2 + 1 common ones (a collision there is exactly a pair at distance < d). Negative controls (a duplicated
word, a word at distance 2, a wrong-weight word, a short line, a wrong count) are all rejected. Internally, each
code had passed two to four other separately written checkers before this release. Results on the shipped files:
`verify-it-yourself/RECEIPTS.md`; `sh verify-it-yourself/run_checks.sh` reruns everything.

## The 5 Delsarte upper bounds

| cell | table lower bound | table upper bound (Johnson, unmarked) | Delsarte LP bound (exact value) |
|---|---|---|---|
| A(31,12,10) | 108 [E] | 229 | **197** (8091/41) |
| A(31,12,11) | 186 [s] | 415 | **380** (145638/383) |
| A(32,12,10) | 123 [Bo] | 300 | **245** (26784/109) |
| A(32,12,15) | 629 | 2641 | **2511** (1102464/439) |
| A(32,12,16) | 1144 | 2870 | **2652** (801009/302) |

These are the classical Delsarte linear-programming bounds for the Johnson scheme (Delsarte 1973), computed exactly
and shipped as rational dual certificates (`certificates/cert_A*.json`: multipliers y_k, a primal solution a_i, the
exact optimum). `verify-it-yourself/delsarte_check.py` re-derives the Eberlein eigenmatrices from the definition, checks P·Q = C(n,w)·I,
verifies dual feasibility, recomputes the bound and its floor, and (since a primal solution is included) certifies LP
optimality. **Their novelty is as table entries only**: the table legend marks Delsarte bounds with "L" and prints
Johnson bounds for n > 28 by default; B. Polak's semidefinite-programming work (arXiv:1703.05171 and his thesis)
covers n = 29..32 and treats Delsarte values as previously known, although these five values do not appear in print.
They are a footnote, offered to the table as "L" entries; nothing stronger than the pure Delsarte LP was used.

## Limitations

- Lower bounds (codes) and routine LP upper bounds; no optimality claims.
- All verification is internal; no outside expert has looked at the codes or certificates.
- Not yet submitted to the table maintainer; private submissions by others (Boisclair, Gangl and Gippini all submit
  by email) are invisible to us, and 10 of the 30 margins are ≤ 3 words.
- The codes are polishes of other people's codes (1 %–17 % of the words changed); cite the seed authors.

## Files

```
README.md, RUN_IT_YOURSELF.md, INDEX.csv (30 codes), INDEX_delsarte.csv (5 certificates)
codes/               A<n>_<d>_<w>_<M>.txt, 30 files
certificates/        cert_A31_12_10.json ... cert_A32_12_16.json
verify-it-yourself/  cwcheck.py, delsarte_check.py, run_checks.sh, RECEIPTS.md
the-record-we-beat/  HTTP headers and sha256 of Andw.html at both fetch times (2026-10-08, 2026-10-10), parsed values of our cells, claims.csv (the 35 current claims), the parser
how-we-built-it/     the generating code (local-search engines, Graham-Sloane rebuild, Delsarte certificate maker), commands, seeds, SMOKE.md
HOW_WE_FOUND_IT.md   how the agents got there, what failed, credits
```

## References

- A. E. Brouwer, *Bounds for binary constant weight codes*, https://aeb.win.tue.nl/codes/Andw.html (table and code archive); A. E. Brouwer, J. B. Shearer, N. J. A. Sloane, W. D. Smith, *A new table of constant weight codes*, IEEE Trans. Inform. Theory 36 (1990).
- W. Echols, arXiv:2608.13906 (2026). C. Lysenstøen, arXiv:2607.19550 (2026). Yang et al., arXiv:2609.35051 (2026). Rosin, arXiv:2603.00174 (2026). A. Gippini, Zenodo doi:10.5281/zenodo.23075336 (2026). J. Boisclair and D. Gangl, codes contributed to the table by email (2026), as labelled there.
- R. L. Graham, N. J. A. Sloane, *Lower bounds for constant weight codes*, IEEE Trans. Inform. Theory 26 (1980).
- P. Delsarte, *An algebraic approach to the association schemes of coding theory*, Philips Res. Rep. Suppl. 10 (1973). B. Polak, arXiv:1703.05171 (2017).
