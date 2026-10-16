# CRITERION skeptic verdict: labs-merit-factor-records, L = 464

context: subagent (Claude Code Agent tool, fresh context, model opus)

Inputs read: claim/CLAIM.md, claim/TABLE_RECORD.md, claim/REPRODUCE.md, claim/sequence_L464.txt,
claim/inputs/arxiv_2607.09688v1.pdf, claim/inputs/arxiv_2409.07222.pdf, claim/inputs/arxiv_2607.09688_abs.html,
and (only after my own checker had produced its result) claim/inputs/author_labs_energy.py. Nothing outside claim/ was read.

## Element-by-element check

1. **Explicit object.** PASS. claim/sequence_L464.txt is one line of 464 symbols plus a trailing newline (465 bytes);
   sha256 01c27fe0d4e2dd0c7a54205ad3741858339b745c7041dcf74119092fa5e63f2c, matching CLAIM.md.
2. **+-1 alphabet.** PASS. After stripping the single trailing newline, the only characters are '+' and '-'.
3. **Length 67 <= L <= 600.** PASS. L = 464. The L <= 66 proven-optimum clause does not apply.
4. **Exactly computed integer energy (my own checker).** PASS. I wrote my own checker from the bank definition
   (E = sum_{k=1}^{L-1} C_k^2, Python ints). I also ran a second, independent method that counts index-pair differences
   over the +1 and -1 position sets. Both give **E = 14396**. The claimant's checker, run afterwards, also gives
   E = 14396 (F = 7.477633). That merit factor is not used in the comparison.
5. **Baseline, arXiv:2607.09688v1 Table 3, L = 464.** I decoded Table 3 (pp. 11-12) myself with the paper's stated
   rule: hex digit -> 4 bits, drop the leading zero padding, keep the last L bits, 0 -> -1. The L = 464 row decodes
   to a 464-bit string with only zero padding removed, and its energy is **E = 14436**. That gives 464^2/(2*14436) = 7.4569,
   exactly the printed "Our F". As a control, 33 of the 35 Table 3 rows reproduce their printed F to 4 decimals. The
   two that do not are rows 484 and 573: under this text extraction, 484 decodes to only 483 bits and 573 to 581 bits.
   Neither affects L = 464.
6. **Other named sources.**
   - arXiv:2409.07222 (ref [42]) Table 2, L = 464: I decoded it myself and get **E = 14824**, which matches its printed 7.2617.
     The older value it cites, [7] at F = 7.1347, corresponds to E of about 15088, which is larger.
   - Table 3 of 2607.09688 gives the previous best from [42, 19] at L = 464 as F = 7.2617, i.e. E = 14824. So refs [42]
     and [19] give nothing below 14436.
   - arXiv:2504.00987 ("up to 120"), the Boskovic et al. repository (skew-symmetric, odd L <= 449, plus Knauer 2004) and
     the newer-arXiv search (newest relevant entry 2609.05771, no record table) are in the package **only** as the
     claimant's scout record in TABLE_RECORD.md. None of their contents are included. I could not check them
     independently inside this package. Nothing in the package contradicts them.
   - Minimum over the sources I could check: 14436.
7. **Strictly smaller, integer comparison.** PASS. 14396 < 14436, by 40 in integer energy. This is not a tie. The claimed
   sequence is not the published L = 464 row, its negation, or its reversal (all checked).
8. **One cell / bundling / subsumption.** The claim is exactly one cell, L = 464. Construction check: the file equals
   "--" + (Table 3 L = 461 record, 1 -> '+') + "+", and dropping its first symbol gives the claimant's separate L = 463
   sequence with E = 14047, which I computed. So this is a derivative of the same padding construction as the L = 463
   claim (#255). The criterion is per length, though, and the L = 463 claim says nothing about L = 464. L = 464 is
   therefore its own, non-subsumed cell. It must not be counted as extra evidence for L = 463 or any other length,
   or the other way round. The method is trivial (a published record padded with 3 symbols), but the criterion does
   not require a non-trivial method.
9. **Null model.** Not needed. The object is explicit and checked deterministically with exact integer arithmetic. No
   statistical claim is involved.
10. **Hidden quantifiers and stretched definitions.**
    - "at verification time" and "any newer arXiv result": these are open-ended. They are covered here only by the
      claimant's dated search (2026-10-16), which I cannot re-run within this package.
    - "best published value ... found by the claimant" (CLAIM.md): this is suitably hedged and not overstated.
    - Rounded merit factors were not used in the decision. The printed F values served only as decode controls.
    - Energy does not change under negation, so the sign convention does not matter.

## Decision
The object meets the full success criterion for the single cell L = 464 against every source whose content is in
the package. It is a genuine, strict, integer-energy improvement, and the per-length criterion does not let the
L = 463 claim subsume it. The only residual risk is the open-ended "any newer result" quantifier. That rests on the
claimant's dated scout, and other panel members should cover it.

confirmed_scope: The explicit +-1 sequence in claim/sequence_L464.txt (length 464) has exact aperiodic autocorrelation energy 14396, strictly below the L = 464 energies 14436 (arXiv:2607.09688v1 Table 3) and 14824 (arXiv:2409.07222 Table 2) that I decoded and recomputed, with the other named sources and any newer arXiv results covered only by the claimant's 2026-10-16 search record.

pass: true
