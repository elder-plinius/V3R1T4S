# Honesty gate: run 2026-10-24-0139, langton-ant-fT-minimal-seed (local target), full success criterion
gate written: 2026-10-24T02:09Z (date -u) by the run's orchestrating session, after reading all three panel files in full.
status: CONFIRMED_SOLUTION
confirmed_scope: For Langton's ant (white right, black left), ant fixed at the origin facing north with y downward, g(k) for k=0..11 is 9977, 310, 162, 126, 67, 62, 49, 45, 40, 24, 17, 0 with minimiser counts 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2 in that frame modulo never-read cells, the 13 seeds in data/minimisers.txt, assuming the blank period-104 highway from update 9977 repeats forever.
partial win: not applicable. The full success criterion of the local target is met (clauses i-iii plus unpublished and a fresh three-skeptic panel). The target is user-added (targets-local/, charter quarry 7), not a pinned-bank target.

## Panel record (plain)
Each reviewer was a fresh headless Grok Build CLI session (grok --prompt-file, no prior conversation), started in its own copy of claim/, run in parallel, 1500 s timeout, nice -n 19.
- CRITERION (criterion.md): pass. It read both checkers line by line and wrote its own independent simulator (indep.py). It re-simulated all 13 minimisers against the blank highway word for 400 turns and ran an independent exhaustive T=0 enumeration over all 104 phases (2 seeds, both 11 cells; none with 10 or fewer). It rebuilt fsearch and lcone for spot runs with blank and planted-positive controls, and checked the Dmin=159 / debris radius 48 argument and the c_back=18 argument. It wrote the confirmed_scope above. Caveats: highway persistence is assumed, not proved; spot reruns, not every worker log; it did not re-run the k=2 box brute.
- NOVELTY (novelty.md): pass. Searched OEIS (many subsequences, both onset conventions), arXiv, OpenAlex, GitHub, the Jillhewar PDF, the Ke repo tarball (prefixTimes min 310, no table), and informal sites. No published table and no smaller onset for any k. New find: a 2026-10-15 YouTube clip shows one black cell below the ant giving a road at step 310, a single example that matches g(1) with no minimality claim. Caveats: Zenodo HTML and Semantic Scholar were blocked (403/429).
- REPRODUCE (reproduce.md): pass. It wrote its own simulator and an independent exhaustive search (mysearch.c) before opening the claim code. k=1, 2, 3 match exactly (no onset below the table value, one minimiser each). It rebuilt and reran every REPRODUCE.md command for fsearch and lcone. Transcripts match line by line and the leaf counts equal the five-worker sums. Caveats: k>=4 minimality rests on the two claim checkers rerun, not on a third enumeration. It flagged the stale first lines of minimiser_compare.txt (a parse slip, explained in attempts/rerun-lcone/output/minimiser_compare.NOTE.md; the data match).
- File sha256 at gate time: criterion.md 8e525285..., novelty.md 4bb849fc..., reproduce.md 5327c647....

## Downgrade check (kit/RUN.md step 7)
- Hedging panelist: no. All three pass outright and state their caveats.
- Reproduction mismatch: none. The only flagged item is a stale comparison line in a helper file; the underlying transcripts match.
- Table value: no record table exists. The known single points (9977; an 11-cell time-0 seed; one-cell 310 as an example; Ke's 182 in a different setting) are consistent and disclosed. The Ke fetch is from 2026-10-24T01:39Z, under 1 h old.
- Stretched criterion or hidden quantifier: the fixed frame, "modulo never-read cells", the onset convention, and the blank-highway assumption are all named in the scope sentence. That matches the criterion's clause (iii).
- Capped search used as an exclusion: no. Both checkers are uncapped first-read searches; T is the onset bound being proved, not a search cap.
- Sample presented as complete: no.
- Several objects bundled: one table with its minimiser list, as the criterion asks.
Result: no downgrade. Final status CONFIRMED_SOLUTION for the local target, subject to CHECK_RUN: PASS.
