# CRITERION skeptic verdict — N=3949 claim

Fresh-context review. Read only the claim/ package. Ran my own computations; did not look at
attempts/, dossiers, or logs.

## (a) 50-digit r* vs table value — VERIFIED (PASS)

I ran the package's claim/checker.py verbatim at low priority (nice -n 19; exit 0, ~4.6 min):
```
N=3949  r*=0.014967835309584944999961031442
table=0.014965462848801963299805173335
margin r*-r_table = 2.372e-06  (need >= 1e-11 to beat)
```
Independently, I wrote my own loader + feasible-radius implementation (double precision,
own code, panel/mycheck.py): r* = 0.014967835309584898, margin = 2.372461e-06 >= 1e-11,
same order as claimed. Arithmetic check on the CLAIM's quoted values:
0.0149678353095850 − 0.014965462848801963307763269064 = 2.37246078e-06, ≥ 1e-11.
Selftest analog: the same code on posted_cci3949.txt reproduces the table value to
1.162e-16 (double-precision floor), so my code is not manufacturing the margin.
The checker's table lookup reads ../data/radius.txt; I grepped it: the N=3949 row is
byte-identical to radius_3949.txt. Caveat noted, not a failure: the package renders r*
to only 16 significant digits despite the "50 digits" language; with the margin 2.37e-06
standing ~5 orders of magnitude above the 1e-11 threshold, rounding cannot flip the
verdict, and I executed the actual 50-digit computation rather than trusting the print.

## (b) Not isometric to posted cci3949.txt — VERIFIED (PASS)

My own double-precision sorted-distance-multiset comparison on all 7,795,326 pairs of each
file: 7,795,316 pairs differ by > 1e-9, max abs difference 5.056241e-03. Multisets differ,
so the configurations are definitively not isometric. Both files contain exactly 3949
lines with 1-based index columns; max |c| in the candidate is 0.98503 < 1 (container
constraint satisfied; the binding term is min-pair/2 ≈ r*). (Criterion's definition is
literally "sorted distance multisets differ"; no geometric-transform search is needed,
and difference of multisets is conclusive.)

## (c) History-of-updates — SATISFIED on the record

Per table-record.txt (the only evidence in my scope; the NOVELTY skeptic does the live
re-fetch): cci.html's newest line is 11-Oct-2026 (Zii Fave N=15 proofs); nothing touches
N=3949. I did not independently fetch cci.html. Literally read, the criterion only
requires that N not appear in a history line newer than the scout's fetch; on the record,
it does not.

## (d) Queue rule — SATISFIED on the record, WITH the criterion's own caveat

Per table-record.txt, pending-requests.html at 2026-10-20T09:52:24Z lists cci candidates
only in range 652–3943 (Vidit Patankar, 15-Oct-2026); 3949 > 3943, so N=3949 lies inside
no listed cci range. I did not independently fetch the pending page. On the caveat: the
26-Sep-2026 Moki & Julio "*many*" 4666-candidate bundle is category-unspecified. Does it
widen or void the scope? Literally neither: it does not widen (3949 remains outside every
LISTED cci range, and the rule applies to listed ranges), and it does not void — the
verbatim criterion itself anticipates exactly this case and prescribes the outcome:
"the verdict must state this caveat and the N must be re-checked against the live table
once that bundle disappears from the pending list." So the queue-rule element is met
subject to that stated caveat and the obligated future re-check; full unconditional
finality is not yet claimable.

## (e) Full criterion vs enumerated partial wins — FULL CRITERION MET

The verbatim bank success criterion is a single criterion over "one N listed in
radius.txt" — N=3949 is listed. Its four operative conditions (a)–(d) are all satisfied
(with (d) carrying the caveat prescribed by the criterion itself), so this is the FULL
success criterion, not merely a partial win. The bank's p2 label ("improvement for a gap
value N > 2600 with a lattice-like seed by Specht"; author.txt confirms Eckard Specht)
describes the class of this N; the "e.g. N=4495, 5000" examples are literally
non-exhaustive ("e.g." = for example). p1 ("second optimum, not a record") does not apply
— this is a record improvement. The win is non-subsumed: it strictly beats the live posted
value, is not isometric to the posted seed (verified above), and is not in any listed
queue range; the only unresolvable subsumption risk is the Moki & Julio bundle, which is
exactly the stated caveat.

## (f) Null models — AGREE with PREREG, literally

A null test guards against a statistic arising by chance under a sampling process. Here
the statistic is a deterministic function of an explicit submitted object, computed at
50 digits; there is no random draw whose fluke could produce a 2.37e-06 margin. The real
epistemic risks are checker bugs and criterion misapplication, which are addressed by the
checker's selftest (positive reproduction of the cci100 table value, negative collapse
under perturbation), my independent recomputation, and literal reading of the criterion —
none of which is a null test. Skipping null_test is correct as stated.

## (g) Hidden quantifiers / stretched definitions — none found

- "Improvement" is exactly r* − r_table ≥ 1e-11 at 50 digits: verified arithmetically and
  computationally. No tolerance, no smoothing, no epsilon-gaming.
- "The" table value is fixed by the criterion as the 30-decimal radius "re-fetched live
  immediately before claiming": table-record.txt documents the fetch at 2026-10-20T08:59:32Z
  and re-verification at 2026-10-20T09:52:24Z with the value unchanged (0.014965462848801963307763269064);
  no stale snapshot is smuggled in. Live re-fetch itself is the NOVELTY skeptic's lane.
- "STRICTLY GREATER ... by at least 1e-11": the margin 2.37e-06 clears it with 5 orders of
  headroom; "strictly" is satisfied in the strong sense.
- The isometry test is pinned by the criterion's own parenthetical ("sorted distance
  multisets differ") — I applied that literal test, which is conclusive in the
  difference direction observed.
- No quantifier stretch on the queue rule either: "inside any range listed for this
  category" was applied to listed cci ranges only, not to the unresolvable
  category-unspecified bundle, which the criterion handles separately and explicitly.

confirmed_scope: Candidate_n3949.txt's 50-digit feasible radius exceeds the record-quoted live Packomania value for N=3949 by 2.372e-06 and its sorted pairwise-distance multiset differs from the posted seed's, with N=3949 outside the record-quoted queued cci ranges and absent from record-quoted history updates — but the Moki & Julio "*many*" category-unspecified pending bundle leaves the queue rule unresolved until the bundle disappears and the criterion's required re-check happens.
context: subagent
pass: true
