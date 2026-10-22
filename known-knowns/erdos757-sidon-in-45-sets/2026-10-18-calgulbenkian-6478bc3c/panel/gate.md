# Honesty gate (erdos757-sidon-in-45-sets)

status: CONFIRMED_PARTIAL
confirmed_scope: The set A in object/witness_n21_s12.json (21 distinct integers, 21 not a multiple of 14) is a (4,5)-set whose exact maximum Sidon subset has size 12 (agreed by two independent exact methods run here), giving s/|A| = 4/7, exactly equal to, not below, the 4/7 shown at erdosproblems.com/757 and on the EinsteinArena leaderboard on 2026-10-18; this meets only the p1 partial win, not the full criterion, and says nothing about the lemma in arXiv:2602.23282.

## Gate notes
- Object: object/witness_n21_s12.json, sha256 6478bc3cabcce580910f07fd9e3fee3a15d5b398ba12c9f9f557cfa7af7f2539.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Partial win p1 only: |A| = 21 is not a multiple of 14 and s/|A| = 4/7 equals the live best (erdosproblems.com/757 and the EinsteinArena leaderboard, fetched 2026-10-18). The full criterion is NOT met: item (3) needs a strictly smaller ratio.
- s(A) = 12 by two independent exact methods as the criterion names them: a bitmask branch-and-bound and an ILP (pulp 3.3.1 with CBC, status Optimal), plus an exhaustive enumeration of all 2^21 subsets; the Ma-Tang 14-set calibration gives s = 8 by every method.
- Refile of the author's pull request #29, closed unmerged on 2026-10-14 in the bulk close of about thirty early pull requests during a handoff between sessions, not for a defect. The ILP was added to the package on 2026-10-18 before this panel ran.
- The criterion skeptic notes that A contains an exact dilated copy of the Ma-Tang 14-set plus 7 further points; |A| is still not a multiple of 14, which is what p1 asks.
- No downgrade triggers found.
