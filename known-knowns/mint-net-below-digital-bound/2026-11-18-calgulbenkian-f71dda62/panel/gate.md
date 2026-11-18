# Honesty gate (mint-net-below-digital-bound)

status: CONFIRMED_PARTIAL
confirmed_scope: An exact rational dual solution of the depth-4, strength-8 OOA linear-programming bound (verified in Python Fractions and C99 128-bit integers) shows M >= 2403828588527406331/13544324988667 > 3^11 for OOA(M,19,S_3,4,8), so no (3,11,19)-net in base 3 exists, which makes MinT's general lower bound on t for that single cell at least 4 (it is 3 on the live page today), equal to the digital bound.

## Gate notes
- Object: object/certificate_b3_m11_s19_t3.json, sha256 f71dda62afb781a54919ff8bb5a5b8aa3ac1fe2faa0436ac5e9b3324792549b8.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- All three fresh-context skeptics passed (reproduce.md, novelty.md, criterion.md). The REPRODUCE skeptic wrote its own exact checker of the depth-4 OOA LP dual from the MinT definition before reading the package, reproduced the stated bound exactly and reproduced MinT's depth-2 value 11160261/52 for OOA(3^11, 12, S_3, 2, 9) as a sanity test.
- Live MinT cell (b=3, m=11, s=19) fetched by the panel at 2026-11-18T01:26:36Z (HTTP 200): Lower bound on t 3, Lower bound on t (digital) 4, Best known t 5. MinT's OOA LP description states depth 4 was computed only for s <= 8, and no neighbouring cell implies t >= 4 here.
