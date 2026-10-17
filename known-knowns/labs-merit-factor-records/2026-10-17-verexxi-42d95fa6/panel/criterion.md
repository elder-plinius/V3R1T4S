# Criterion skeptic verdict, claim L = 252

context: subagent (same VM)

confirmed_scope: The explicit +-1 sequence of length 252 in sequence.txt has exactly recomputed integer energy E = 3534 (F = 8.98), strictly below the baseline 3738 (the minimum over the rows for L = 252 in arXiv:2206.12070 [3738, also recomputed from its printed hex sequence] and the Knauer 2004 table as stored in the Boskovic git_labs repository [4386]), after reading ten sources (1406.5301, 1512.02475, 2011.00068, 2106.03377, 2206.12070, 2210.15962, 2409.07222, 2504.00987, 2607.09688, Knauer 2004), none of which has a lower value for L = 252; it is NOT established against the unread current Boskovic records pages or any arXiv result newer than the sources read, and it is a one-end trim of a published L = 253 record sequence.

## Element-by-element check
- Explicit +-1 sequence: sequence.txt is 252 characters over {0,1}, one line, mapped 0 -> +1, 1 -> -1. Pass.
- 67 <= L <= 600: L = 252. Pass.
- Exact integer energy: I recomputed E with the supplied checker and with a separate plain double loop in Python integers: both give 3534. Parent (L = 253, from 2011.00068) recomputes to 3670; the parent is exactly skew-symmetric; removing either end gives 3534 (symmetry), and sequence.txt equals the parent with its last element removed. Pass.
- Baseline: baseline.tsv rows are 4386 (Knauer, printed and recomputed), 3738 (2206.12070, hex decoded and recomputed by me: 3738; the printed MF 8.49438... equals 252^2/(2*3738)), and the old merit factor 7.2394 (= 4386). Minimum 3738. 3534 < 3738 as integers, and 3534 < 4386. Pass against the baseline as read.
- One table cell: one length, one energy, one comparison. Pass.

## Hidden quantifiers / stretched definitions
- The criterion says "minimum over the tables in 2607.09688, 2504.00987, the Boskovic et al. repository, and any newer arXiv result". 2607.09688 tabulates 450..573 and 2504.00987 tabulates 92..120, so neither has a row for 252; the real comparison sources for 252 are 2206.12070 and the repository. The baseline uses sources beyond the two named arXiv ids, which only makes it tighter (more sources checked), not looser. No quantifier is stretched in the claimed direction.
- Hole in the baseline: the repository was read only through one raw page (Knauer 2004 copy); the git_labs tree listing and the 2013 even/odd records pages were not readable, and no search for newer arXiv results could be run (listing endpoint 429). "At verification time" and "any newer arXiv result" are therefore not exhausted. The claim must be worded as "against the sources read", which the claim text does.
- Mitigations from the evidence: (a) 2206.12070 prints an old-record column for L = 252 equal to 7.2394, the Knauer value, so as of 2022 the best earlier known value (which would include the Boskovic records and 1406.5301) was Knauer's 4386; the 2022 value 3738 is the trim of its own best L = 253 sequence (3574), which I verified decodes to 3738 after removing one end. (b) 2607.09688 (June 2026) still cites only [boskovic17, dimitrov22] as the source of F > 8 for 172 <= L <= 268, which suggests no newer record covering this range was known to its authors. (c) 2210.15962 only covers odd lengths up to 247 and 2011.00068/1406.5301 have no 252 row.
- Parity / structure: L = 252 is even, so no skew-symmetric search applies directly; even-length records come from operators on odd skew-symmetric records or from plain search, and are less contested. F = 8.98 is above the best published odd neighbour (L = 253, F 8.95 in 2206.12070), which is surprising for an even length and is a flag, but it is explained by the structure: trimming one end of an exactly skew-symmetric odd sequence has expected energy change about +L, and here it is -136 (roughly a 3 sigma lucky event from a single parent); the same operator on 2206.12070's better parent gives only 3738. So the better value arises from picking a different parent, which the 2022 authors evidently did not try (or did not keep). That makes an unread better value possible (the same observation could be made by anyone, including in a post-2022 paper) but not likely on the evidence read.

## Is an end-operator result from another length's record genuine and non-subsumed?
- The criterion as written has no method or novelty clause: it asks only for an explicit sequence with exact energy strictly smaller than the best published energy for that L. A trim of a published L = 253 sequence qualifies literally; the published energy for 252 (3738) is not implied by the parent's printed data, and the 252 value 3534 appears in no source read.
- It is not subsumed by any read source: the only published 252 values are 4386 and 3738, and the 2206.12070 operator result is derived from a different parent. It is subsumed only if an unread source holds a 252 value <= 3534, which I cannot rule out.
- Weakness: it is a one-element edit, the derivation uses the same published operator family as the baseline, and the margin is not independent search work. This limits its significance but not its validity under the stated criterion.

## Decision
The full criterion is met literally relative to the sources read (energy recomputed, strict integer inequality, in range). The residual risk is the unread repository pages and unsearched newer arXiv results; the evidence (old-record column, 2026 literature statement, parity) makes a lower published 252 value unlikely. I pass, with the scope limited to the sources actually read as stated above.

pass: true
