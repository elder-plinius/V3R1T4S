# CRITERION skeptic verdict — labs-merit-factor-records, L = 463
context: subagent (Claude Code Agent tool, fresh context, model opus)

Scope of inspection: claim/ only (CLAIM.md, REPRODUCE.md, TABLE_RECORD.md, sequence_L463.txt, inputs/). Scratch in
mywork/ (python3 stdlib; PDF text extracted with macOS PDFKit via a 10-line swift script, since no poppler is installed).
No network access was used.

## 1. Explicit +-1 sequence — MET
Own checker (mywork/energy.py, written before reading inputs/author_labs_energy.py), two independent routes (direct C_k
loop, and full convolution of coefficient products):
```
bytes 464 sha256(file) 24118ce24643733bfb3ba0b75f5a267cb278aced3992063690d06594fc914707
lines 1
charset ['+', '-']
L 463 E 14047 E2 14047
```
File hash matches the sha256 stated in CLAIM.md (hash is of the file including the trailing newline).

## 2. 67 <= L <= 600 — MET
L = 463 (counted from the file, not taken from the claim).

## 3. Exactly computed integer energy — MET
E = sum_{k=1}^{462} C_k^2 = 14047 by both routes, Python integers only. The claimant's checker, run afterwards, agrees:
```
L=463 E=14047 F=7.630419 skew_symmetric=True
```

## 4. Baseline: independent decode of Table 3, L = 463 (inputs/arxiv_2607.09688v1.pdf, p. 12) — CONFIRMED E = 14439
Decoding rule as printed in the paper (p. 9): "each hexadecimal digit is mapped to a 4-bit binary representation ...
leading zero-padding ... must be removed ... converting every 0 -> -1". I decoded every row of p. 12 (wrapped hex lines
re-joined) and checked bit length and the printed "Our F" to 4 decimals (mywork/dec.py):
```
461 116 hexdigits bitsL= 461 E= 13574 F=7.8282 printedF= 7.8282 OK
462 116 hexdigits bitsL= 462 E= 13811 F=7.7273 printedF= 7.7273 OK
463 116 hexdigits bitsL= 463 E= 14439 F=7.4233 printedF= 7.4233 OK
464 116 hexdigits bitsL= 464 E= 14436 F=7.4569 printedF= 7.4569 OK
...
```
(22 of 24 other rows also match; the 484 row prints the same hex as 483 in the extracted text and the 573 row is a
3-line wrap my parser mis-joined; neither affects L = 463.) The 463 row decodes to exactly 463 bits, is skew-symmetric,
and its F matches the print, so row/L alignment is confirmed. Table 3's "Previous F [42, 19]" for 463 is 7.3885, i.e.
E ~ 463^2/(2*7.3885) = 14506.9, worse than 14439. So the minimum for L = 463 attested in this PDF is 14439.

## 5. Strict integer comparison — MET for the verified baseline
14047 < 14439 (integers; margin 392). Not a tie. Merit factors (7.6304 vs 7.4233) were not used for the decision.

## 6. Coverage of "minimum over the tables in arXiv:2607.09688, arXiv:2504.00987, the Boskovic et al. repository, and any newer arXiv result"
- arXiv:2607.09688: VERIFIED by me from the supplied PDF (hash 53941410...b35b31 matches TABLE_RECORD.md). The abs page in
  inputs/ shows only [v1], submitted 17 Jun 2026. Also covers its own quoted prior literature [42] (Psenicnik, Mlinaric,
  Brest, Boskovic 2025) and [19] (Dimitrov, arXiv:2206.12070) at F 7.3885 for L = 463.
- arXiv:2504.00987: rests ONLY on the claimant's record ("problem sizes up to 120", so no L = 463 entry). Not supplied,
  not verified by me.
- Boskovic et al. repository: rests ONLY on the claimant's record (borkob/git_labs, last push 2020, skew tables L <= 449 +
  Knauer 2004 table). I also cannot confirm this is the repository "cited there" (2607.09688 contains no github URL; the
  citing document would be 2504.00987, not supplied). Indirect support: the 2025 paper [42] by the same group is the
  "previous best" that Table 3 beats, so any repo value would be expected to be no better than 7.3885.
- Newer arXiv results: UNVERIFIED at verification time. The claimant's 2026-10-16 API search returned HTTP 429 and was
  not retried; the only negative search is the claimant's own from 2026-10-15. This is the main residual risk.

## 7. Subsumption / derivation from published objects
Hunting for derivation (mywork/sub.py, mywork/ext.py), the object is exactly the published Table 3 L = 461 record with
one symbol prepended and one appended:
```
len461 461 E461 13574
obj[1:462]==Table3 L=461 sequence: True ; prepended -1 appended 1
all 4 two-end extensions of the L=461 record, energies: [14047, 14499, 14499, 14943]
```
So the "new" sequence is the best of the four trivial end-extensions of a published record (the paper itself describes
such append/remove "sequence operators"). Under the literal criterion this does not matter: the criterion compares
against the best PUBLISHED ENERGY FOR THAT L, and no published L = 463 value <= 14047 is attested in the evidence. It is
not subsumed in the sense of being equal-or-worse than a published L = 463 object (a symmetry image of a published
sequence would have equal energy, which is a tie; this object is not one: Hamming distance >= 179 to all 8 symmetry
images of the published 463 sequence). It is, however, a derivative, low-effort record, and its trivial derivability
raises the prior that someone else may already have published it (sharpening the risk in item 6, newer arXiv).

## 8. Null test
Not needed for the criterion: the claim is an explicit object checked by deterministic exact integer arithmetic against
a table value; there is no statistical inference to null-test. The relevant "null model" here is the trivial-operator
baseline (extend published neighbours), and the object IS that baseline; this informs significance, not criterion
satisfaction. L = 463 > 66, so the proven-optimum bug check does not apply.

## Literal reading
Every deterministic element of the criterion (explicit +-1, 67 <= 463 <= 600, exact integer E = 14047, strict integer
inequality vs the decoded published value 14439) is confirmed independently. The "minimum over all named sources" is
confirmed only for arXiv:2607.09688 (and the prior literature it quotes); the other three sources rest on the
claimant's dated record, with the newer-arXiv check not completed on verification day.

confirmed_scope: The 463-symbol +-1 sequence in sequence_L463.txt (the Table 3 L = 461 record of arXiv:2607.09688v1 with -1 prepended and +1 appended) has exact energy E = 14047, strictly below E = 14439 of the L = 463 sequence in Table 3 of arXiv:2607.09688v1 and below the previous best it quotes (F = 7.3885); absence of a lower L = 463 value in arXiv:2504.00987, the Boskovic et al. repository and newer arXiv work rests on the claimant's record, not on this check.
pass: true
