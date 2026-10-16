# REPRODUCE skeptic verdict
context: subagent (Claude Code Agent tool, fresh context, model opus)

Scope: I used only claim/ and a working folder mywork/ next to it. I wrote my own checker before opening inputs/author_labs_energy.py.

## Definition quoted (claim/CLAIM.md, bank statement)
"For a +-1 sequence s of length L, the aperiodic autocorrelations are C_k = sum_i s_i s_{i+k}, the energy is
E = sum_{k=1}^{L-1} C_k^2, and the merit factor is F = L^2/(2E)."

## My checkers (written before I read the author's code)
- mywork/energy.py: reads the file as raw bytes, rejects any symbol other than '+'/'-', and maps + -> +1 and - -> -1.
  For each k it computes C_k = sum_{i=0}^{L-1-k} s_i s_{i+k} with an explicit double loop in Python integers, then
  E = sum C_k^2. It reports the exact fraction for F and a skew-symmetry flag.
- mywork/energy_alt.py: a second, separate method. It gets every C_k from one big-integer polynomial product
  (offset encoding a_i = s_i + 1, with the offset terms removed afterwards). It reports E and max|C_k|.
- mywork/pdftext.swift (macOS PDFKit) extracts the text of PDF pages 11-12. mywork/render.swift renders page 12
  to PNG so I could check the rows by eye.
- mywork/decode2.py splits the Table 3 hex into blocks. It decodes each block with the paper's rule (hex digit -> 4 bits,
  drop leading zero padding, 1 -> +1, 0 -> -1), then matches each block to a table row by its decoded length L and
  compares F = L^2/(2E), rounded to 4 decimals, with the printed "Our F".

## Commands and real outputs
Object (claim/sequence_L463.txt, sha256 24118ce24643733bfb3ba0b75f5a267cb278aced3992063690d06594fc914707, which matches CLAIM.md):
```
$ python3 -I energy.py ../claim/sequence_L463.txt
bytes 464 lines 1 trailing newline True
L=463 E=14047 F=7.630419 F_exact=214369/28094
plus 245 minus 218
skew True
$ python3 -I energy_alt.py ../claim/sequence_L463.txt mywork/table3_L463_pm.txt
../claim/sequence_L463.txt L=463 E=14047 maxabsC=23
table3_L463_pm.txt L=463 E=14439 maxabsC=23
```
- Alphabet: only '+' and '-' (anything else would have been rejected), plus one trailing newline. Length is 463.
- Determinism: I ran energy.py three times. The output hash was the same each time (b66152e4928485e19cffb89809b285c16b0644c3).

Baseline: Table 3, row L = 463. The PDF text and the rendered image of page 12 agree. The hex is printed over two lines:
```
7ffffff0007fd80787e13f04f0dc393c8e58276cb978e466c3ce727932731a7
26cb4e646da1bce27586dcb1b48d2c52b16a5a558aa5552aaaaaa
```
decode2.py output (all 35 Table 3 rows on pp. 11-12):
```
table rows 35 hex blocks 35
block00 hexdigits=113 pad=2 L=450 E=13009 F=7.783073 printedOurF=7.7831 match=True
block01 hexdigits=113 pad=1 L=451 E=12625 F=8.055485 printedOurF=8.0555 match=True
block02 hexdigits=113 pad=0 L=452 E=13074 F=7.813370 printedOurF=7.8134 match=True
block03 hexdigits=114 pad=1 L=455 E=13043 F=7.936249 printedOurF=7.9362 match=True
block04 hexdigits=114 pad=0 L=456 E=13288 F=7.824202 printedOurF=7.8242 match=True
block05 hexdigits=115 pad=3 L=457 E=13532 F=7.716856 printedOurF=7.7169 match=True
block06 hexdigits=115 pad=2 L=458 E=13837 F=7.579822 printedOurF=7.5798 match=True
block07 hexdigits=115 pad=1 L=459 E=14101 F=7.470428 printedOurF=7.4704 match=True
block08 hexdigits=115 pad=0 L=460 E=13870 F=7.627974 printedOurF=7.6280 match=True
block09 hexdigits=116 pad=3 L=461 E=13574 F=7.828238 printedOurF=7.8282 match=True
block10 hexdigits=116 pad=2 L=462 E=13811 F=7.727319 printedOurF=7.7273 match=True
block11 hexdigits=116 pad=1 L=463 E=14439 F=7.423263 printedOurF=7.4233 match=True
block12 hexdigits=116 pad=0 L=464 E=14436 F=7.456913 printedOurF=7.4569 match=True
block13 hexdigits=117 pad=3 L=465 E=14336 F=7.541330 printedOurF=7.5413 match=True
block14 hexdigits=119 pad=1 L=475 E=15197 F=7.423340 printedOurF=7.4233 match=True
block15 hexdigits=119 pad=0 L=476 E=15110 F=7.497551 printedOurF=7.4976 match=True
block16 hexdigits=120 pad=3 L=477 E=15022 F=7.573193 printedOurF=7.5732 match=True
block17 hexdigits=120 pad=2 L=478 E=15115 F=7.558187 printedOurF=7.5582 match=True
block18 hexdigits=120 pad=1 L=479 E=15007 F=7.644466 printedOurF=7.6445 match=True
block19 hexdigits=120 pad=0 L=480 E=15160 F=7.598945 printedOurF=7.5989 match=True
block20 hexdigits=121 pad=3 L=481 E=15016 F=7.703816 printedOurF=7.7038 match=True
block21 hexdigits=121 pad=2 L=482 E=15169 F=7.657855 printedOurF=7.6579 match=True
block22 hexdigits=121 pad=1 L=483 E=15321 F=7.613374 printedOurF=7.6134 match=True
block23 hexdigits=121 pad=1 L=483 E=15321 F=7.613374 printedOurF=7.6134 match=True
block24 hexdigits=123 pad=2 L=490 E=16005 F=7.500781 printedOurF=7.5008 match=True
block25 hexdigits=123 pad=1 L=491 E=15957 F=7.554083 printedOurF=7.5541 match=True
block26 hexdigits=124 pad=2 L=494 E=15955 F=7.647634 printedOurF=7.6476 match=True
block27 hexdigits=124 pad=1 L=495 E=16155 F=7.583565 printedOurF=7.5836 match=True
block28 hexdigits=124 pad=0 L=496 E=16308 F=7.542801 printedOurF=7.5428 match=True
block29 hexdigits=125 pad=3 L=497 E=16568 F=7.454400 printedOurF=7.4544 match=True
block30 hexdigits=125 pad=2 L=498 E=16825 F=7.370104 printedOurF=7.3701 match=True
block31 hexdigits=129 pad=0 L=516 E=18278 F=7.283510 printedOurF=7.2835 match=True
block32 hexdigits=130 pad=3 L=517 E=18150 F=7.363333 printedOurF=7.3633 match=True
block33 hexdigits=130 pad=2 L=518 E=18463 F=7.266533 printedOurF=7.2665 match=True
block34 hexdigits=146 pad=3 L=581 E=26622 F=6.339888 printedOurF=- match=False
rows without a decoded block: [484, 573]
duplicate decoded lengths: {483: 2} identical: {483: True}
L463 last-463-bits == stripped: True
```
- The decoding rule checks out: 33 rows decode to exactly their printed L and match the printed "Our F" to 4 decimals.
  These include the neighbours 461 (E=13574), 462 (E=13811), 464 (E=14436) and 465 (E=14336).
- For L = 463, stripping the leading padding gives the same bits as taking the last 463 bits (the REPRODUCE.md rule).
- The only integer energy that rounds to the printed 7.4233 is 14439:
```
E range consistent with Our F 7.4233 (rounding interval): 14438.83152485064 14439.026033071767
E from printed prev F 7.3885 (approx): 14506.936455302159
14047 < 14439: True diff 392
```
- The object is not the Table 3 sequence (`cmp`: differ at char 1).

Author's checker (read and run only after my own was done). It gives the same results:
```
$ python3 -I inputs/author_labs_energy.py "$(head -1 sequence_L463.txt)"
L=463 E=14047 F=7.630419 skew_symmetric=True
$ python3 -I inputs/author_labs_energy.py "$(head -1 ../mywork/table3_L463_pm.txt)"
L=463 E=14439 F=7.423263 skew_symmetric=True
```
Input hashes match TABLE_RECORD.md: the PDF is 53941410...bb35b31 and the abs HTML is c14c75ea...4420c. The abs page shows only [v1], "Submitted on 17 Jun 2026".

## Mismatches and observations
- None of these affect the claim. Every number for the object and for the L = 463 baseline matches the claim:
  E = 14047 and E_baseline = 14439, with 14047 < 14439.
- Two defects in the paper, both outside L = 463, confirmed on the rendered page 12:
  - Rows 483 and 484 print the same hex. It decodes to L = 483 (E = 15321), so row 484 has no valid sequence.
  - Row 573 decodes to 581 bits, not 573.
  Neither changes the L = 463 row, which I checked by eye and through its decoded length and printed F.
- Limit of my check: I reproduced the claim as stated, i.e. the object against Table 3 of arXiv:2607.09688v1. I could not
  check from the saved files that no other published L = 463 value is below 14047 (arXiv:2504.00987, the
  git_labs repository, any newer arXiv paper). That rests on the claimant's TABLE_RECORD.md, which records an
  HTTP 429 on the arXiv search. This is not a reproduction mismatch, but it is still open for the record question.

pass: true
