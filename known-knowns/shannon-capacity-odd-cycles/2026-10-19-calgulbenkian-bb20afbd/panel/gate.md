# Honesty gate (shannon-capacity-odd-cycles)

status: CONFIRMED_SOLUTION
confirmed_scope: Under ruling R9, the 3-branch S3b schedule with Tandon's 30-dimensional left gadget and terminal code K4a gives, via Tandon's Lemma 1, Theorem 1 and the BPZ combining rules (re-derived in writing and instance-tested here) and with every finite ingredient (G5, C1 to C4, codebook independence, condition 33, tables) verified computationally, an independent set of size M (288 digits) in C_7^{box 560}, so Theta(C_7) >= M^(1/560) = 3.25883477557614484751818055569792750605282670056114, strictly above the live record 3.25883262035326630912153905181047543760538759432195 as of 2026-10-20 04:46 UTC; the 560-dimensional set itself is not enumerated.

## Gate notes
- Objects: 6 files under object/ (sha256 of each in INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Lower bound Theta(C7) >= 3.258834775576... (d = 560), above Tandon (arXiv:2608.30273, d = 500, 3.2588326203...) by 2.155e-6: Tandon's gadget calculus with his 30-dimensional left gadget substituted into all three branches of the S3b top level (dimensions 40, 60, 40) instead of one. A decimal step on a famous constant; this cascade moves every few weeks.
- Judged under the contributor's review ruling R9: the composition rules rest on Tandon's Lemma 1, Theorem 1 and Proposition 1 (single-author v1 preprint, not formalised), re-derived in writing by the criterion skeptic and tested on explicit vertex sets by three agents; every finite ingredient is verified in the folder (base gadget G5 axioms, certificates C1-C4 re-derived without Tandon's script, codebook independence and condition (33) at dimension 30 by box structure). Two earlier criterion skeptics failed this cell under a stricter reading (machine-checked composition theorem required), before R9 and before the folder was extended.
- The novelty report predates the folder extension; the claimed object (schedule and integer M) is unchanged, and the live record was re-fetched by the third criterion skeptic at 2026-10-20T04:46Z (still Tandon's d = 500 value).
