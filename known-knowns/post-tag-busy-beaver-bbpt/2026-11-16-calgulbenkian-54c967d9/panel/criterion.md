context: Claude Code subagent, fresh context [Sonnet 5.5]

Criterion skeptic report, target post-tag-busy-beaver-bbpt (claim: exact BB_PT(8) = 19).

What I checked
- Conventions: size = |A| + sum|w_a|, start tape 00, delete 2 and append, stop when fewer than 2 symbols remain, steps counted without an extra halting step. This matches the wiki page I re-fetched (oldid=8554, last edited 16 Sep 2026; table still reads "8 >= 19, 111_20_, 7 holdouts"). So clause (b)'s precondition "page still lists with >=" holds. Fetch recorded in a working copy (not shipped).
- Clause used: criterion (b), which also covers partial win p1. The claim says "full criterion (b)", and (b) for S=8 is the same content as p1, so it is the full criterion, not a downgrade.
- Ran verify-it-yourself/verify_bbpt8.py on object/bbpt8_certificates.json with python -I: calibration (0111_1=10, 111_20_=19, 11_021_2=49, 112_1_002=779, 120221_0_2=196841) OK, PASS.
- Wrote my own independent enumerator (compositions of word lengths, no canonicalisation): 19,693 raw size-8 systems (matches the formula sum C(7,n-1) n^(8-n)); 17,374 halt within 1000 steps, max 19, reached only by 111_20_ variants. The 2,319 non-halting raw systems equal the package's 1,404 cycle + 915 DFA-invariant. So coverage of every size-8 system and the halting count agree with the package.
- Read the DFA-invariant check logic. It is sound: the automaton must accept the entry tape, reject the empty word and all one-symbol words (so no accepted tape can be a halting tape), and for every accepted word a b u the successor u w_a is accepted, checked by product-BFS over all (a,b) with p1 from the state after "ab", p2 from the start state reading u, then w_a. That is a genuine inductive invariant, a checkable non-halting certificate in the criterion's "another proof re-checked by an independent decider" sense (the checker is a separate small program from the synthesizer, though from the same package; I re-ran it, and I did not write a second DFA checker).
- All 7 wiki holdouts (01010_1, 01111_0, 11011_0, 11110_0, 010_2_0, 010_21_, 0120__0) appear as DFA_INVARIANT classes (16, 10, 10, 10, 14, 29, 62 states).
- Hidden quantifiers: none found. "Every size-S system" is covered via raw enumeration; unreachable symbols are dropped by canonicalisation, which is harmless because behaviour from 00 depends only on reachable rules, and the pitfall about renaming duplicates is addressed (1,728 classes, raw multiplicities verified).

What I could not settle
- Whether sligocki/etc or AzertyWasTaken or any merged package already has exact BB_PT(8)=19 (the repository rule says an equal or better upstream value counts against the claim, and a result implied by a merged package is not new). The README says sligocki HEAD still has 4 holdouts at size 8 and the wiki still lists >=19; novelty search belongs to the NOVELTY skeptic.
- I did not independently verify the minimality of each DFA or the 1,728-class partition beyond my raw count; neither affects soundness of the value.

Weakness note: the certificate verifier and the package were produced by the same author; my independent check covers enumeration and the halting side only.

confirmed_scope: Under the wiki convention (size |A|+sum|w_a|, start 00, halt below 2 symbols), all 19,693 size-8 2-tag systems either halt (maximum 19 steps, only 111_20_) or have a checkable cycle or DFA-invariant non-halting certificate (including all 7 wiki holdouts), meeting criterion (b)/p1 for S=8 only, subject to the novelty skeptic finding no prior or merged equal result.
pass: true
