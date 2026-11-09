# Criterion skeptic: anomaly-free-atlas-qmax (charter quarry 5), run 2026-11-03-0919

Scope of reading: claim/ only (CLAIM.md, REPRODUCE.md, status.md, object/, source/, checker/). Working files are in
panel_work/criterion/ (compiled copies of the claim's sources and small-Q outputs only; no heavy runs).

## The criterion, clause by clause

Criterion (verbatim, CLAIM.md): "extend the exact census of anomaly-free U(1) charge assignments of the Standard Model
fermions (with and without three right-handed neutrinos) with integer charges bounded by `Q_max`, beyond the largest
`Q_max` tabulated by Allanach, Davighi and Melville; new exact counts, with the full solution list as the certificate."
The charter lists no partial wins, so only the full criterion can pass.

### 1. Same census, same counting convention as ADM?

- ACCs. checker/checklist.c checks all six ACCs in the all-left-handed basis. I compared them with ADM eqs. 2.1-2.6
  (source/atlas/arXiv-1812.04602v5.txt, lines 232-267). ADM write u, d, e, nu right-handed, so their signs differ. As
  CLAIM.md notes, flipping the sign of a whole species is a bijection that keeps |F|, the gcd, per-species
  permutations and the overall sign. The quadratic is the same. I re-derived the linear species-sum reduction by hand
  (s_d = -2s_Q - s_u, s_L = -3s_Q, s_e = 2s_Q - s_u, s_nu = 4s_Q + s_u), which the listers and both counters use. It
  is correct. The SM case sets nu = 0, as ADM do (their line 271).
- Equivalence. ADM quotient by per-species family permutations (S3 per species, their sec. 2 item 3), by rational
  rescaling including the sign (item 2, and the gcd removal plus the F_Q1 <= 0 choice in sec. 4.1), and they include
  the all-zero row ("Each row contains the all-zero charge solution", captions of Tables 2 and 3 and of erratum
  Table 1). The claim's convention, 1 + primitive nonzero solutions modulo per-species permutations and overall sign,
  is that convention. One wrinkle: ADM's text says the gcd test uses primes "less than Qmax". Read literally, that
  would keep 2x and 3x copies at Q_max = 2, 3, 5, 7. The published numbers are pure gcd-1 at those prime Q_max
  (e.g. SM Q_max = 2: 22, not the 29 that keeping multiples would give). So the tables, not the loose sentence, fix
  the convention, and the claim matches the tables.
- Null models (my rerun). I ran source/count.c for Q_max = 1..10, SM and SMnuR, and evaluated it with
  source/conventions.py. Only `prim_incl0` reproduces the published values. `prim_excl0` (zero not counted) is off by
  1 everywhere, `all_incl0` (no gcd quotient) is off at every Q_max >= 2, and `nosign` is about 2x. So the published
  data pick out the convention without ambiguity.
- Reproduction of published values (my rerun). source/mitm.c gives exactly the 20 "Solutions" values of v5 Tables 2
  and 3 for Q_max = 1..10, SM and SMnuR. source/csenum2.c and source/acclist.c both stream a SMnuR Q_max = 10 list
  that checker/checklist.c accepts with 21546919 = 21546920 - 1 lines. I did not re-check the "Symmetry" column
  myself; source/atlas/table_comparison.txt records it as matching.
- Verdict on clause 1: the convention matches the publication.

### 2. "beyond the largest Q_max tabulated by ADM"

ADM v5 Tables 2 and 3 go to Q_max = 10 for both contents. The erratum's Table 1 adds nothing beyond 10: it repeats
SMnuR 7..10. The paper itself says "for Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR" (v5 text, line 784). The
arXiv record (status.md; the abs page sha256 matches the copy in source/atlas/) shows v1..v5 only. Rows SMnuR 20 and
SM 36, 37, 38 are beyond 10. Met.

### 3. "with and without three right-handed neutrinos"

The claim has rows for both contents: SMnuR at Q_max = 20, and SM at Q_max = 36, 37, 38. The rows do not continue on
from the published range within this claim. Rows 11..19 and 11..35 are said to be confirmed elsewhere, which I may not
read. That is not needed, though. Canonical form and the gcd do not depend on Q_max, so the Q_max = 20 (or 38) list
filtered to max|F| <= q is the list at every q below it. The new rows therefore contain the lower rows, not the
reverse. Met, and not subsumed by the earlier rows.

### 4. "new exact counts, with the full solution list as the certificate"

- The lists are not stored. Each one is a deterministic byte stream from source/csenum2.c (SMnuR) or
  source/acclist.c (SM), pinned by the sha256 of the uncompressed stream (object/counts.txt, which matches
  object/receipts/*.sha256). The same piped bytes (tee) went through checker/checklist.c, which reported count - 1
  valid lines and PASS for all four rows (receipts).
- Is "regenerated plus hashed" a fair reading of "the full solution list as the certificate"? I accept it, with the
  wording made explicit. A list of 6.47e9 lines cannot practically be stored. More importantly, checking it does not
  require trusting the lister: the lister only acts as a decompressor. Every emitted line is checked independently
  (all six ACCs, the bound, nonzero, canonical form, gcd 1, strictly increasing order, hence no duplicates), and the
  hash pins the exact bytes. What a list cannot show by itself is completeness, which no finite list can self-certify.
  The claim covers completeness by agreement with source/mitm.c. That code uses a different algorithm (a different
  meet-in-the-middle split, (Q,L,nu)|(u,d,e), plus Moebius over the gcd and Burnside over the sign), and its receipt
  gives the identical count for all four rows. The pass ranges in the SMnuR 20 enumeration log are contiguous
  (0..1680), and the 80 per-pass line counts sum to 6465226974 = count - 1.
- Spot check (my rerun): `acclist 20 0` reproduces the REPRODUCE.md sha256 f8e2ce35... and passes the checker with
  1071440 lines, which is mitm's 1071441 - 1.
- I did not regenerate the four claimed rows. That is the reproduction skeptic's job, given the CPU and memory limits
  here. My pass is a criterion judgement on the evidence as recorded.

### 5. Overstatements and gaps (none decisive)

- "certified by a complete canonical solution list": the list certifies soundness and a lower bound. Completeness
  rests on agreement with an independent counter. For SMnuR 20, SM 37 and SM 38 that is a single counter (mitm.c),
  written in the same workspace.
- object/counts.txt credits SM 36 with "count.c:32457211(run 2026-11-02-0920)", but no receipt for it is in claim/.
- The status.md fetch at 2026-11-03T09:19:21Z has no line in source/atlas/fetch_log.txt, which records only
  2026-10-28. The two abs-page files are byte-identical, so nothing changes.
- "family-dependent" in the claim sentence is ADM's naming. The counts also include family-universal assignments
  (e.g. 6Y). This is harmless in ADM's convention, but I leave the word out of the scope.
- Novelty is judged literally against ADM, as the criterion says. I did not survey other literature (reading was
  restricted to claim/).
- CLAIM.md's own status line ("unpanelled") is out of date now that this panel is running. It does not affect
  correctness.

## Verdict

The rows meet the full criterion, read literally:
- the census and convention are ADM's, fixed by all published values and separated from the alternative
  conventions;
- every row is beyond Q_max = 10;
- both contents are present;
- the counts are exact, with two independent algorithms agreeing;
- each row has a complete canonical list, pinned by hash and checked line by line.

The certificate is a regenerable stream, not a stored file, and the scope below says so. The rows are new relative to
ADM and contain the workspace's earlier rows rather than being contained by them, so the win is genuine and not
subsumed.

confirmed_scope: In the Allanach-Davighi-Melville convention (1 + primitive nonzero integer solutions of the six ACCs with |F| <= Q_max, modulo per-species family permutations and overall sign; reproduces all their published Q_max <= 10 solution counts), the number of inequivalent anomaly-free U(1) charge assignments is 6465226975 for the Standard Model plus three right-handed neutrinos at Q_max = 20 and 32457211, 37347334 and 42898799 for the Standard Model fermions alone at Q_max = 36, 37 and 38, each certified by a code-regenerated (not stored) canonical list of count - 1 lines identified by the sha256 in object/counts.txt, validated line by line by checker/checklist.c and matched in count by the independent counter source/mitm.c.
context: subagent (fresh context, Claude Code Agent tool)
pass: true
