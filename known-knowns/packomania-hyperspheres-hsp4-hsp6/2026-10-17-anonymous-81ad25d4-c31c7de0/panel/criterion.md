context: fresh criterion subagent; research input restricted to claim/, this skeptic's own work, and the specifically supplied fresh primary raw responses with provenance; no parent attempts, other panel verdicts, archived rejected claims, or author checker code were read

target: packomania-hyperspheres-hsp4-hsp6

verdict: The single-cell construction meets the literal numerical, non-isometry, update-history and category-queue conditions against fresh primary responses and exceeds the supplied stronger prior, with the unresolved bundle caveat expressly required by the criterion.

NUMERICAL: I wrote `../panel/criterion-work/check_criterion.py` independently from the definition in `target.json`; `../panel/criterion-work/results.json` records its successful run at 2026-10-16T00:01:56.478728+00:00. It uses mpmath 1.4.1 with `mp.dps=50`, converts the original decimal coordinate strings directly, and applies no feasibility tolerance. Analytic positive and negative fixtures pass. All supplied checksums and the source-record/member checksums match. Run it from `claim/` with `python -X utf8 ../panel/criterion-work/check_criterion.py`.

NUMERICAL: There are exactly 119 distinct finite centers with four coordinates each. I checked all 7,021 pairs and all 119 wall constraints for each supplied object. The binding formula is `min(min_pair_distance/2, 1-max_center_norm)` in the origin-centered unit ball, so neither a header radius nor an optimizer objective is the score.

| Quantity | Independently computed value |
|---|---|
| Candidate feasible radius | 0.23606892889364886505664445893098935298010907228947 |
| Candidate half minimum pair distance | 0.23606892889364886505664445893098935298010907228947 |
| Candidate wall radius | 0.23606892889364893030105085677053991319349300944365 |
| Freshly verified Packomania N=119 row | 0.236068068183 |
| Gain over that exact decimal row | 0.00000086071064886505664445893098935298010907228946657795 |
| Posted configuration's feasible radius | 0.236068068182399835049801073000699386917878694583 |
| Posted parser/table absolute discrepancy | 0.00000000000060016495019892699930061308212130541699568986579886 |
| Supplied Moki & Julio object's feasible radius | 0.23606869597929028946544883264916203897792471496589 |
| Gain over the recomputed Moki & Julio object | 0.00000023291435857559119562628182731400218435732357172252 |
| Maximum sorted pair-distance difference from posted | 0.0096922017941812197496703550877266046816487656763648 |
| Maximum sorted pair-distance difference from Moki & Julio | 0.0083742046094268184659422488718013344963344420534179 |

NUMERICAL: The table gain exceeds the binding `1e-10` threshold; the smaller `1e-11` mentioned elsewhere in the target's pitfalls was not substituted for it. The posted parser reproduces the table within the required `1e-11`. The sorted multiset test exceeds `1e-8` at 7,015 positions against the posted object, including a maximum at sorted position 5,461, so the stated non-isometry condition is met. These are full finite checks, not samples.

PROVED-HERE: As an additional rounding safeguard, exact rational arithmetic directly on the coordinate strings verifies the feasible decimal radius 0.23606892889364886505, equal to 4721378577872977301/20000000000000000000, against every squared pair-distance and squared wall inequality. The longer radius above is the specified mpmath evaluation, not an assertion that its rounded display is an exact feasible rational radius.

KNOWN from fresh primary responses: The [radius source](https://packomania.com/hsp4/txt/radius.txt), [history source](https://packomania.com/hsp4/hsp4.html), and [pending source](https://packomania.com/pending-requests.html) were fetched with an honest V3R1T4S-named client and HTTP 200 at 2026-10-16T00:01:01.524918+00:00, 2026-10-16T00:01:02.420277+00:00, and 2026-10-16T00:01:03.511751+00:00 respectively. I independently hashed and parsed these specifically supplied source-only responses at 2026-10-16T00:05:41.978768+00:00 with `../panel/criterion-work/check_live_sources.py`; the raw bytes and request provenance are preserved under `../panel/criterion-work/live-source/`, and `../panel/criterion-work/live-results.json` records the checks. Each response is byte-identical to its corresponding claim snapshot. The radius source still lists N=119 at 0.236068068183. The history contains only 04-Jul-2025, 05-Jul-2025 and 06-Jul-2025 entries, with none later than the scout baseline 06-Jul-2025 supplied in `CLAIM.md`. The HTTP Last-Modified date is not an update-history entry. The pending source contains 20 submission rows and no HSP4 category row at all, so no explicit HSP4 range excludes N=119 at this verification time.

KNOWN from the supplied prior-art data: The [Moki & Julio manifest](https://raw.githubusercontent.com/Hashirama1337s/moki-julio-circle-packing/main/MANIFEST.csv) and [certificate archive](https://raw.githubusercontent.com/Hashirama1337s/moki-julio-circle-packing/main/certificates/hsp4.zip), represented by `moki-manifest.csv` and the hash-checked `prior-moki-119.txt` ZIP member, establish a stronger prior than Packomania. I did not accept the target background statement that no competing group had touched these tables. The candidate exceeds the prior certificate's recomputed feasible radius, not merely its rounded header. It also exceeds every one of the 166 supplied HSP4 manifest radii with N at least 119 and every larger-N row of the supplied Packomania table, so the simple deletion-of-extra-balls implication does not subsume this claim within those supplied data. This does not replace the NOVELTY skeptic's independent literature and current-source search.

CRITERION INTERPRETATION: This is the full success criterion for one listed cell, HSP4 N=119. It is not partial win p1, p2, or p3: there is no author-row claim, extension row, or all-listed-N audit. Nothing establishes optimality, completeness of a search, a new contact-graph class, or any other table cell. The unit-ball container, full four-dimensional coordinates, strict improvement direction and minimum gain, explicit non-isometry threshold, update-history condition, category queue condition, and absence of submission are separate requirements.

NULL DESIGN: The deterministic-object exemption in kit/RUN.md applies: the claim is one explicit object checked against finite distance and containment inequalities and a table value. It makes no statistical significance, solver superiority, chance-beating, exhaustive-search, or optimality claim. The fact that an optimizer found it does not turn this bounded object verification into a statistical claim requiring 400 controls. I do not attest to preregistration timing from the claim-only inputs.

QUEUE CAVEAT: The 26-Sep-2026 Moki & Julio `*many*` 4666-candidate bundle remains category-unspecified and unresolved. The criterion expressly requires this caveat instead of treating that bundle as a known HSP4 range. Beating the supplied public same-cell certificate does not identify everything in the queued bundle. N=119 must be checked again against the live HSP4 table once that bundle disappears. No email or other submission was made by this skeptic.

LIVE REQUIREMENT: The fresh primary responses resolve the stale-snapshot concern for this review. The literal table, history and category-queue clauses have been independently checked against those responses; the broader current-literature novelty search remains the separate NOVELTY role, and this file does not adopt another reviewer's reasoning or award a final gate status.

confirmed_scope: For HSP4 N=119, candidate.txt has mpmath-50 feasible radius 0.23606892889364886505664445893098935298010907228947, exceeding the freshly verified Packomania row and supplied Moki & Julio certificate with the specified non-isometry, history and category-queue conditions satisfied; the category-unspecified 26-Sep-2026 Moki & Julio 4666-candidate bundle remains unresolved, and N=119 must be re-checked against the live table when that bundle disappears.

pass: true
