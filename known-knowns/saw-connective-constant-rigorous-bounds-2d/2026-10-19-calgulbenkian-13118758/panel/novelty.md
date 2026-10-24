# Novelty report: saw-482-k34p (4.8^2 lattice, rigorous upper bound 169287/92732 = 1.825551050339)

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

Package verified from inside the package folder against the contributor's hash list: every line OK (0 non-OK). Every fetch was logged with UTC time, HTTP status and sha256 (all 200 on first attempt, honest client); the log is not shipped. I read the k = 32 novelty report (read-only) and re-ran the searches rather than relying on them.

## Baseline
- Jensen 2004 (cond-mat/0409381) Table 3, 4.8^2 upper bound 1.82926, credited to Alm / Parviainen (private communication). Alm, J. Phys. A 38 (2005), section 5.1.3, quoted in the-record-we-beat/LITERATURE_ADDENDUM.md: "The matrix G(19, 42), with dimension 125 094, gives the bound mu < 1.829 254". Best published bound is therefore 1.829254. I did not read Alm 2005 itself (paywalled); I rely on the addendum and the k = 32 report's confirmation.
- Claim 1.825551050339 is below 1.829254 by 3.703e-3 and below 1.82926 by 3.709e-3, far above the required 1e-6. It is also below the k = 32 value (1.826966832) in PR #534 by 1.416e-3.

## 1. Literature (arXiv API over https, 2026-10-19, four queries, sorted by date; the saved responses are not shipped)
- q1 "connective constant" AND (Archimedean OR octagon OR 4.8 OR truncated square): 1 hit, Jensen 2004 only.
- q2 self-avoiding AND (upper bound OR rigorous bound) AND connective constant: 8 hits, newest 2509.04568 (Sep 2025, restricted walks), 2508.01993 (He), 2211.16146 (Couronne), then 2018 and older. None gives a 4.8^2 bound.
- q3 self-avoiding AND (finite memory OR automaton OR transfer matrix) AND upper bound: 2 hits (Couronne, Jensen).
- q4 self-avoiding AND (trapped OR pocket OR finite component OR enclosed) AND (automaton OR upper bound): 0 hits.
- Nothing new since the k = 32 report; no arXiv item after 2025-09-04 on this topic. (Note: arXiv API has no entries dated after the existing ones; this is a search, not a proof of absence.)
- Full texts fetched and searched (saved copies not shipped): Couronne 2211.16146v2 (square lattice only), He 2508.01993v3 (lattices: square, triangular, hexagonal, and 3D cubic; no 4.8^2), 2509.04568v1 (square/triangular restricted walks). None states a 4.8^2 bound.
- Pruning prior art (credits only, not novelty of the bound):
  - Alm (as described in He's paper, Remark 2.5): Alm "noted without proof in [1, Remark 5] that, by discarding dead-end m-step SAWs and assuming no parity restriction on the lattice, his matrix G(m, n) ... will be positive for all sufficiently large n." So discarding dead-end walks is mentioned in Alm's original method, for primitivity, not as a bound-tightening device with a proof. This is the closest published relative of "finite-pocket" pruning.
  - Couronne 2211.16146 (Section 3): simplification of states with a "small loop": "As C and D ... are such that d_inf(C, D) <= 2, we should never go in the area enclosed by the loop delimited by C and D", so enclosed areas are excluded from the automaton. This is the same family of idea (a walk that enters an enclosed region is dropped from the state set), for the square lattice, by a different rule.
  - I found no published treatment of exactly "pruning a move when the new head, or the state's oldest vertex, cannot reach infinity avoiding the state's vertices" (a finite-pocket test) combined with a bridge-growth argument (Grimmett-Li Theorem 4.3). I cannot exclude it (Parviainen's thesis, Alm 2005 and the Laves/Archimedean chapters were not readable). Credits recommendation: cite Alm 2005 (method, dead-end remark), Couronne 2022 (enclosed-area exclusion and finite-memory loop states), He 2025 (open software), Ponitz-Tittmann 2000, Grimmett-Li (bridge theorem); present the pocket-pruning theorem as the builder's own adaptation, "as far as we found".

## 2. PRs
- Used a snapshot of all V3R1T4S pull requests (titles and bodies; 473 PRs, fetched 2026-10-19T04:30:31Z) in place of the pulls pages. Its highest number is #483, so it predates #534 (opened 2026-10-19T07:51Z); the k = 32 report's statement that #534 appears in it is wrong for this snapshot. Keyword scan of titles and bodies (self-avoiding, connective, saw-, 4.8, Archimedean, octagon, kagome, Alm): 7 hits, none on SAW or this target (cluster-energy, constant-weight code, percolation, packing and spherical-code PRs matching "4.8" or similar by accident).
- Read-only, once more for the later numbers: `gh pr list --repo elder-plinius/V3R1T4S --state all --search "4.8"` at 2026-10-19T15:52Z returned one PR: #534 (calgulbenkian, OPEN, opened 07:51:24Z), title still k = 32, 1.826966832, "below 1.829254". Extra read-only searches "connective constant" and "self-avoiding" returned the same single PR. So no other filing on this target; #534 is the author's own and is the claim's intended replacement, not a competing value.
- Closed calgulbenkian bulk-close PRs (#65-#120): none concerns this target.
- The repository trophy-case listing and the known-knowns listing (fetched earlier today, and the k = 32 report): no connective-constant entry, no SAW folder.

## 3. Propagation (PR #350 rule)
No table or merged or open value gives a 4.8^2 upper bound that implies 1.8255. Bounds for other lattices (square 2.662342, triangular, kagome, hexagonal) do not bound the 4.8^2 constant from above; the only monotone relation (subgraph inclusion) goes the wrong way, since every supergraph of 4.8^2 has a larger constant. The k = 34 value does not follow from the k = 30 or k = 32 values: the automaton is different (pocket-pruned, 16,873,086 states), it is the same family run deeper. Relation to #534: it is the same record slot; this value would replace the k = 32 (or k = 30) value in place, not stand as a second record.

## 4. Open questions concerning novelty, answered
- "Published baseline 1.82926 is quoted from Jensen 2004 Table 3 (best published is Alm's 1.829254); post-2025 literature was not searched again": confirmed. Baseline is 1.829254 (Alm 2005) rounded to 1.82926 in Jensen; the claim beats both by more than 3.7e-3. Post-2025 literature searched now (queries above, plus Couronne, He, and the Sep 2025 paper in full text): no 4.8^2 upper bound found. Residual: Google Scholar, MathSciNet, Alm 2005 full text and Parviainen's thesis not read.
- The other open questions in the claim record (not shipped) (pruning theorem, Bridge theorem application, pocket test, rounded certificate, symmetry windows) concern reproduce or criterion, not novelty. The one novelty aspect: the author's own value 1.825523 is not claimed, so nothing is there to compare.

unresolved: Alm 2005 full text and Parviainen's thesis not read; Google Scholar and MathSciNet not searchable. A non-arXiv better bound could plausibly exist but nothing in arXiv, He's paper, Couronne's paper or this repo points to one.

Verdict: strictly better than the best published 4.8^2 bound (1.829254 / 1.82926) by 3.7e-3 and than all later work found; not implied by any table or PR value; not a competing value to #534 (it supersedes it). Pruning-idea credit should go to Alm (dead-end remark) and Couronne (enclosed-area exclusion).

pass: true
