# REPRODUCE skeptic verdict — labs-merit-factor-records, L = 464

context: subagent (Claude Code Agent tool, fresh context, model opus)

Scope: only the claim package (claim/). My own checker was written and run before opening claim/inputs/author_labs_energy.py; the author's REPRODUCE.md steps were run last.

## Definition used (quoted from claim/CLAIM.md)
> "For a +-1 sequence s of length L, the aperiodic autocorrelations are C_k = sum_i s_i s_{i+k}, the energy is E = sum_{k=1}^{L-1} C_k^2, and the merit factor is F = L^2/(2E)."

My checker uses exact Python ints, with two separate implementations: (a) a direct double loop over k and i; (b) the full integer self-convolution of s with reversed s, reading C_k at offset L-1+k. Sanity check: Barker-5 `+++-+` gives E = 2 (correct) in both.

## Object: claim/sequence_L464.txt
- 465 bytes = 464 symbols + one trailing newline, one line. sha256 01c27fe0d4e2dd0c7a54205ad3741858339b745c7041dcf74119092fa5e63f2c (matches CLAIM.md).
- Alphabet {'+','-'} only.
- Output: `L=464 E=14396 E_alt=14396 F=7.477633`

## Baselines decoded independently from the PDFs (pypdf text extraction only)
Decoding rule taken from each paper's text: each hex digit -> 4 bits, drop leading zero padding down to length L, 1 -> +1, 0 -> -1. Each row's hex is split over two text lines and the two parts were joined. My decoder checks that the dropped padding bits really are all zero.
```
2607.09688 T3 L=461 hexdigits=116 prevF=7.6435 ourF=7.8282 decodedLen=461 E=13574 E_alt=13574 F=7.828238 F4=7.8282
2607.09688 T3 L=463 hexdigits=116 prevF=7.3885 ourF=7.4233 decodedLen=463 E=14439 E_alt=14439 F=7.423263 F4=7.4233
2607.09688 T3 L=464 hexdigits=116 prevF=7.2617 ourF=7.4569 decodedLen=464 E=14436 E_alt=14436 F=7.456913 F4=7.4569
2409.07222 T2 L=464 hexdigits=116 prevF=7.1347 ourF=7.2617 decodedLen=464 E=14824 E_alt=14824 F=7.261738 F4=7.2617
```
- The energies I computed reproduce the printed merit factors to 4 decimals. For L = 464 the printed F fixes E uniquely: 107648/14435 = 7.4574 and 107648/14437 = 7.4564, so only E = 14436 rounds to 7.4569. Likewise only E = 14824 rounds to 7.2617. This confirms that the PDF extraction and the decoding are correct.
- The L = 464 row appears only once in the Table 3 text of 2607.09688v1. Its "Previous F" of 7.2617 equals the "Our work" value for L = 464 in Table 2 of 2409.07222 (E = 14824).
- The status-source abstract page (claim/inputs/arxiv_2607.09688_abs.html) lists only [v1], "Submitted on 17 Jun 2026". Input sha256 values match TABLE_RECORD.md (PDF 53941410…, ref [42] PDF 7f29f9fa…, abs c14c75ea…).

## Construction statement
```
len 464 alphabet ['+', '-']
construction '--'+T3_L461+'+' equal: True
E(s)= 14396 14396
E(s[1:]) (claimed L=463 E=14047): 463 14047
s==T3_L464? False  s==ref42_L464? False
s in symmetry class of T3_L464: False
E < 14436: True  E<14824: True
```
The object equals "--" + (Table 3 L = 461 record) + "+" exactly. Dropping its first symbol gives an L = 463 sequence with E = 14047, as stated. The object is not the published L = 464 sequence and is not one of its 8 trivial symmetry images (reversal, negation, alternate negation).

## Author's steps (REPRODUCE.md), run last
```
$ python3 inputs/author_labs_energy.py "$(head -1 sequence_L464.txt)"   (run twice)
L=464 E=14396 F=7.477633 skew_symmetric=False
L=464 E=14396 F=7.477633 skew_symmetric=False
author checker on my decoded T3 L=464:   L=464 E=14436 F=7.456913 skew_symmetric=False
author checker on my decoded ref42 L=464: L=464 E=14824 F=7.261738 skew_symmetric=False
author checker on my decoded T3 L=461:   L=461 E=13574 F=7.828238 skew_symmetric=True
```
All claimed numbers match mine: object E = 14396, Table 3 E = 14436, ref [42] E = 14824, and 14396 < 14436 < 14824. Repeated runs gave identical output (deterministic). The author's checker is a plain O(L^2) exact-integer implementation of the same definition, and I found no discrepancy.

## Mismatches
None.

## Limits of this check
I verified only what is reproducible from the saved files. The bank criterion also requires the minimum over arXiv:2504.00987, the Boskovic et al. repository and any newer arXiv result. Those sources are not in the claim package; for them I rely on TABLE_RECORD.md's account (2504.00987 goes up to 120; the repository covers L <= 449 skew tables and the Knauer table; no newer table was found). I did not re-fetch them. Within the package, the claimed value and the strict integer improvement over every L = 464 entry present are confirmed.

pass: true
