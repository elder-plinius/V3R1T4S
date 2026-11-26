Saved by the main session from the subagent's returned text (CRITERION skeptic, Agent tool, fresh context, model opus; returned about 07:22Z 2026-10-18). The text below is verbatim.

# CRITERION skeptic: condorcet-domains, eleven rows (n = 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25)

context: subagent (Agent tool, fresh context, model opus; saw only a copy of claim/)

**What I read.** CLAIM.md, PREREG.md, REPRODUCE.md, SHA256SUMS_object.txt, tools/mcheck.c and tools/mdom.c. From status/: records_table4.tsv, human_status_check.md, scout_record.md, and the saved v1 text arxiv_html_2601.07336.extracted.txt (Section 2 definitions, Section 3 definition of f(n), Sections 5 and 6, Table 1 and Table 4). I made no web request.

**What I ran.** I wrote my own programs for this panel. They are kept in the panel's work folder, outside claim/, and they do not use tools/ except where named.
- **tri3.py and even3.py.** Brute force over profiles on 3 and 4 alternatives.
- **lcheck.c, a list checker.** For each line it checks the exact format, that the line is a permutation of 1..n, and that lines strictly increase in numeric-lexicographic order (so all lines are distinct). For each of the C(n,3) triples it collects the (alternative, position) pairs that occur and tests that some never condition holds. As an option it also tests that every order obeys a given assignment.
- **dpc.c, an exact count of |D(A)|.** It is a forward subset DP that builds each order from the top down. This method differs from the memoised DFS in tools/mdom.c.
- **Small scripts** for the restriction relations, the one-deletion maxima, published product bounds and the Table 4 ratio columns.
- **The claim's enumerator.** I built tools/mdom.c, regenerated the canonical streams of D(A) for n = 23, 24 and 25, hashed each stream with sha256sum, and piped it through lcheck.

**Results (all eleven rows).**

| n | object checked | lines = distinct orders | malformed / non-increasing | triples with no never condition | orders violating nN_assignment.txt | my DP \|D(A)\| | Table 4 | margin |
|---|---|---|---|---|---|---|---|---|
| 14 | list | 27040 | 0 / 0 | 0 of 364 | 0 | 27040 | 27026 | +14 |
| 15 | list | 60956 | 0 / 0 | 0 of 455 | 0 | 60956 | 59430 | +1526 |
| 16 | list | 135072 | 0 / 0 | 0 of 560 | 0 | 135072 | 131536 | +3536 |
| 17 | list | 300388 | 0 / 0 | 0 of 680 | 0 | 300388 | 292015 | +8373 |
| 18 | list | 675512 | 0 / 0 | 0 of 816 | 0 | 675512 | 649079 | +26433 |
| 19 | list | 1497276 | 0 / 0 | 0 of 969 | 0 | 1497276 | 1432836 | +64440 |
| 20 | list (parts aa, ab joined) | 3336208 | 0 / 0 | 0 of 1140 | 0 | 3336208 | 3155366 | +180842 |
| 22 | list (parts aa..af joined) | 16571072 | 0 / 0 | 0 of 1540 | 0 | 16571072 | 15037178 | +1533894 |
| 23 | stream of D(A) | 36894088 | 0 / 0 | 0 of 1771 | 0 | 36894088 | 33162136 | +3731952 |
| 24 | stream of D(A) | 81912986 | 0 / 0 | 0 of 2024 | 0 | 81912986 | 73279872 | +8633114 |
| 25 | stream of D(A) | 178950728 | 0 / 0 | 0 of 2300 | 0 | 178950728 | 160316046 | +18634682 |

- **Stream hashes.** For n = 23, 24 and 25, the sha256 of the mdom enum stream equals the CLAIM.md value: 7a5a7d8ca65a2668c6f8c4bba680f6275019f94d5189a0728febeecd3da633ff, 54baf18b85aecce8a420ce8c1b7350f86b3bf27590741ba9b23193ca0e4a0605 and 2ac0df90378e94892f7af7dc8df27581428be20fb21e90edfc751fee5246bd38.
- **Lists equal D(A).** For type L, every listed order obeys its assignment, the lines are distinct, and the line count equals my DP |D(A)|. So each list is exactly D(A) of its own assignment.
- **Assignments.** All eleven files have exactly C(n,3) lines, with each triple once. Only 1N1, 1N3, 2N1, 2N3, 3N1 and 3N3 occur: 12619 lines in total, so the domains are peak-pit.

## 1. Every clause of the criterion, row by row

- **"For some n >= 9".** Every row's n is in 14..25, so every row has n >= 9. The quantifier is existential, so one valid row meets the criterion. Each row is its own n, with its own bar.

- **"An explicit set of linear orders on n alternatives".**
  - Type L rows: every line is a permutation of exactly the symbols 1..n, in the stated format, and the lines are distinct. Each list is a literal finite set of linear orders on n alternatives.
  - Type A rows: see ruling 2.

- **"Majority rule is transitive for every profile (every triple satisfies a never-condition)".** I read this in the paper's sense: for every profile with an odd number of agents, whose preferences all lie in D (Section 2 of arXiv:2601.07336v1). The never-condition test is the right test, both necessary and sufficient:
  - **3 alternatives, exhaustive.** I took all 63 nonempty subsets of the 6 orders and tried every odd profile of at most 9 voters (multisets). "Some never condition holds" agrees with "the majority relation is transitive for every such profile" on 63 of 63 subsets.
    - There are 48 Condorcet domains, and the largest has size 4. That equals Table 4's n = 3 entry.
    - The 15 non-domains are exactly the subsets that contain one of the two cyclic triples, such as {123, 231, 312}. Three voters suffice to make a cycle.
  - **4 alternatives, sampled.** On 1500 random subsets (3 to 7 orders, odd profiles of at most 5 voters), the all-triples test agreed with brute force on 1500 of 1500.
  - **Why it extends to any n.**
    - With an odd number of voters with linear orders, the majority relation is a tournament.
    - A tournament is transitive if and only if it has no 3-cycle.
    - A 3-cycle on {a,b,c} depends only on the profile's restriction to {a,b,c}.
    - So D is a Condorcet domain if and only if each triple restriction is one, which holds if and only if each triple satisfies a never condition.
  - **Hidden quantifier: even profiles.** If "every profile" also took in even profiles, and ties counted as indifference, the weak majority relation is intransitive for some even profile on 33 of the 48 three-alternative Condorcet domains. Example: one voter each with 213 and 321. Only 15 domains of at most 2 orders escape. The strict majority relation stays transitive on all 48 (profiles of up to 8 voters).
    - So the literal weak, all-parity reading would exclude every domain of interest, including every published record that sets the bar.
    - The criterion's own parenthetical fixes the field's odd-profile meaning. Under that meaning, and also under a "strict majority, any profile" reading, the never-condition test is correct.
  - **The rows.** All eleven rows have 0 triples without a never condition.
    - Type L: checked directly on the lists.
    - Type A: by construction, every element of D(A) obeys A's condition on each triple. I also confirmed this on the full streamed enumerations.

- **"Strictly larger than the best published Condorcet domain for that n".** Comparing against the Table 4 "≥" entries is right.
  - **What the "≥" means.** The "≥" belongs to f(n), the unknown maximum (Section 3: f(n) = max size of a Condorcet domain on n alternatives). Each entry is the size of the largest domain the paper exhibits for that n:
    - n <= 20: Table 1, "Largest CDs found via the inductive search". These are sizes of found maximal (full) domains.
    - n = 21..25: the stated sizes of the domains the paper obtains with the construction of [16] (marked "ks").
  - **So the bar is that number.** "Best published Condorcet domain for that n" has exactly that size, and size > entry is the right test.
  - **Table 4's n is the number of alternatives.**
    - f(n) is defined "on a set of n alternatives", and X = [n].
    - The n = 3 entry 4 is the exhaustive maximum on 3 alternatives.
    - The Fishburn column (100, 222, 488 at n = 7, 8, 9) equals my DP count of Fishburn's alternating scheme on 7, 8 and 9 alternatives.
    - The n = 8 entry 224 is the known maximum on 8 alternatives.
  - **The bars match the paper's own ratio columns.** For n = 14..20 and 22..25, the bar values reproduce the printed x_n/x_{n-1} and sqrt(x_n/x_{n-2}) columns to the printed 3 decimals. Example: n = 14 gives 2.2185 and 2.2127, printed 2.218 and 2.212.
    - One slip in the paper: the n = 21 sqrt entry, 2.221, does not fit 6674931 (it gives 2.158). The n = 22 and n = 23 ratio columns do fit 6674931. n = 21 is not in this folder.
  - **No published construction raises a bar.** I applied Fishburn's f(a+b-1) >= f(a)f(b) and the paper's e(a+b) >= 2e(a)e(b) to the Table 4 values. They give at most 24364, 54052, 118860, 263072, 584030, 1298158, 2865672, 13535040, 30470400, 67244640 and 149183520 for the claimed n. All are below Table 4.
  - **Strict margins.** Every row exceeds its bar strictly; none is a tie.
  - **Not my remit.** Whether anything newer has been published is for the NOVELTY skeptic. Here the record is the saved v1 copy plus the human's hand check in status/.

## 2. Ruling on explicitness of the type-A rows (n = 23, 24, 25)

**Ruling: yes.** D(A_n), given by the full assignment object/nN_assignment.txt (one never condition on each of the C(n,3) triples) together with the exact count of D(A_n) and a deterministic canonical enumerator whose stream hash is pinned, is an explicit set of linear orders. Reasons:
- **(a) It is definite.** A fixes D(A) uniquely. Whether a given order belongs takes C(n,3) direct checks. Nothing rests on an existence argument, a random construction or a bound.
- **(b) It is constructive and reproducible.** A supplied deterministic program lists every element in canonical numeric-lexicographic order.
  - I regenerated all three streams (about 2.5 to 12 GB of text, minutes each). Their sha256 values equal the pinned ones.
  - Each stream is strictly increasing, so it has no duplicates. It has 0 malformed lines and 0 violations under my own checker.
  - So the full list is materialised on demand and pinned bit for bit.
- **(c) Its size is exact, not estimated.** My independent forward subset DP gives 36894088, 81912986 and 178950728. These equal mdom's memoised count and the streamed line counts.
- **(d) It is the field's standard representation.** The record paper itself names a domain by its never conditions (N_[n] and D(N_[n]), "full Condorcet domain"). Its own n = 21..25 bars are not printed as lists either. Demanding a printed list would hold these rows to a stricter standard than the bar they are compared against.
- **(e) The criterion frames the property this way.** Its own parenthetical states the property in never-condition terms.
- **(f) A literal list cannot be packaged.** It is impossible within the package limits, and the charter foresaw this form.

**Limit of this ruling.** It covers a full assignment with an exactly computed |D(A)| and a pinned canonical stream. It would not cover an assignment whose size was only estimated or bounded, or a subset of D(A) described only implicitly.

## 3. Ruling on non-subsumption, and PREREG rule 3

**The relations hold as stated.** I checked them at both levels:
- Assignment level: the row-14 assignment is exactly the row-15 assignment with alternative 12 deleted and relabelled. Likewise row 15 is row 16 without 7, row 18 is row 19 without 11, and row 19 is row 20 without 5.
- List level: projecting the row-15 list onto [15]\{12} gives exactly the row-14 list (27040 distinct orders), and likewise for the other three pairs.

**The other rows are independent objects.** I recomputed the maximum |D(A')| over all one-alternative deletions of the next row's assignment:

| row | deleted from | best x | max \|D(A')\| | row size | row larger by |
|---|---|---|---|---|---|
| 16 | row 17 | 1 | 135032 | 135072 | 40 |
| 17 | row 18 | 4 | 298128 | 300388 | 2260 |
| 22 | row 23 | 5 | 16556290 | 16571072 | 14782 |
| 23 | row 24 | 7 | 36860224 | 36894088 | 33864 |
| 24 | row 25 | 18 | 81355460 | 81912986 | 557526 |

- These match CLAIM.md. A domain's restriction is a subset of D(A'), so these maxima also bound the restrictions of the domains themselves.
- **Row 20 and the n = 21 object.** CLAIM.md reports that the separately claimed n = 21 object restricts to at most 3311844, which is below 3336208. That object is not in my copy, so I take this from CLAIM.md.
- **Doubling and product bounds.** Doubling a domain by adding a new alternative at top or bottom gives f(n+1) >= 2f(n). That, and the product bounds applied to our own smaller rows, give at most 13654144, 33142144, 73788176 and 163825972 for n = 22, 23, 24 and 25. All are below the rows.
  - Doubling row 23 alone would already beat Table 4 at n = 24 (73788176 > 73279872), and doubling row 24 would beat it at n = 25. But rows 24 and 25 are far above these, so they are not subsumed by doubling.

**Ruling: a row that is a restriction of another unpublished row is still a genuine, non-subsumed win for its own n, judged against what is published.**
- The criterion is a per-n statement, and its bar is the published value for that n. f(14) >= 27040 (and likewise for 15, 18 and 19) is implied by nothing published.
- The object that implies it (row 15, 16, 19 or 20) is itself new, unpublished and part of this same folder. Each row stands on its own explicit, separately checked object, so it survives even if a neighbour were dropped.
- Restriction carries no guarantee of beating the n-1 record. That it does so here is an exact, checked fact.
- The paper itself lists derived values as separate per-n records: its ks rows are built from its own smaller-n domains.
- **What this does not allow.** The four restriction rows must not be presented as independent discoveries. The eleven rows come from seven independent objects (rows 16, 17, 20, 22, 23, 24 and 25). The scope sentences below say so.

**PREREG rule 3 holds for every row.**
- The paper's Section 5.1 method on its own inputs produced the Table 1 values (the paper reports its greedy shortcut reconstructs those records for 8 <= n <= 20). The Karpov-Slinko construction on its own inputs produced the Table 4 ks values. Every row is strictly above the listed value for its n.
- So no row is a published construction applied to published inputs whose value the paper lists, and the rule's fallback ("counts only if Table 4 does not already list that value or more") would pass anyway.
- Restriction is a trivial operation, but its inputs here (rows 15, 16, 19 and 20) are not published.

## 4. Hidden quantifiers and stretched definitions elsewhere

- **The n = 14 margin is 14 orders (+0.052 %).**
  - Both numbers are exact integers. 27040 is a count of distinct orders.
  - 27026 is the size of the paper's found domain, the same in Table 1 and Table 4 and consistent with the ratio columns.
  - The criterion asks only "strictly larger", with no minimum margin, so the row passes. It is the most fragile row if a larger n = 14 domain has been published since v1; that is the NOVELTY skeptic's remit.
  - The paper's Table 3 analysis of record-sized sub-domains suggests its own n = 15 domain gives no larger n = 14 restriction. It reports none above the record.
- **The sizes are exact counts of distinct orders.**
  - Type L: the lines strictly increase and the count equals my DP.
  - Type A: my DP equals mdom's count and the strictly increasing stream's line count.
  - No row's size is a bound, an estimate or a count with multiplicity.
- **Table 4's n is the number of alternatives.** Yes (see point 1).
- **The "⌈4/5^1.5 √5^n⌉" column.** The paper does not claim it as a bound. Every row lies below it anyway (for example 178950728 < 195312500 at n = 25), so there is no tension.
- **Like-for-like comparison.** Table 4's column is "f(n) & h(n)". The rows' assignments are peak-pit, so they also exceed the h(n) entries. The criterion needs only f(n).
- **CLAIM.md's wording.** Its one-sentence claim says "the best published value for that n". My scope sentences say "the n entry of Table 4 of arXiv:2601.07336v1", which is what the evidence here shows.

## 5. Null models

**I agree that no null test is needed.**
- The claim is an exact existence statement about finite explicit objects, checked by deterministic exact programs. No search statistic, sample or chance event enters it. How the objects were found does not matter to the claim.
- What matters instead is:
  - **Negative controls**, which exist:
    - tools/tests/all_orders_n3.txt and fishburn_8_plus_one.txt are rejected by the folder's checkers, and also by mine (1 and 6 bad triples).
    - On 3 alternatives the equivalence check is exhaustive.
  - **Trivial baselines**, none of which reaches any row: Fishburn domains, product and doubling constructions on published values, and doubling of our own smaller rows.

## Per-row verdicts

row n=14: PASS
row n=15: PASS
row n=16: PASS
row n=17: PASS
row n=18: PASS
row n=19: PASS
row n=20: PASS
row n=22: PASS
row n=23: PASS
row n=24: PASS
row n=25: PASS

scope n=14: The 27040 distinct linear orders on the alternatives 1..14 listed in object/n14_orders.txt.xz satisfy a never condition on every one of the 364 triples, so they form a Condorcet domain on 14 alternatives (majority relation transitive for every odd profile) of size 27040, strictly larger than the n = 14 entry 27026 of Table 4 of arXiv:2601.07336v1, and this domain is the restriction of the row-15 domain to the alternatives other than 12.
scope n=15: The 60956 distinct linear orders on the alternatives 1..15 listed in object/n15_orders.txt.xz satisfy a never condition on every one of the 455 triples, so they form a Condorcet domain on 15 alternatives (majority relation transitive for every odd profile) of size 60956, strictly larger than the n = 15 entry 59430 of Table 4 of arXiv:2601.07336v1, and this domain is the restriction of the row-16 domain to the alternatives other than 7.
scope n=16: The 135072 distinct linear orders on the alternatives 1..16 listed in object/n16_orders.txt.xz satisfy a never condition on every one of the 560 triples, so they form a Condorcet domain on 16 alternatives (majority relation transitive for every odd profile) of size 135072, strictly larger than the n = 16 entry 131536 of Table 4 of arXiv:2601.07336v1.
scope n=17: The 300388 distinct linear orders on the alternatives 1..17 listed in object/n17_orders.txt.xz satisfy a never condition on every one of the 680 triples, so they form a Condorcet domain on 17 alternatives (majority relation transitive for every odd profile) of size 300388, strictly larger than the n = 17 entry 292015 of Table 4 of arXiv:2601.07336v1.
scope n=18: The 675512 distinct linear orders on the alternatives 1..18 listed in object/n18_orders.txt.xz satisfy a never condition on every one of the 816 triples, so they form a Condorcet domain on 18 alternatives (majority relation transitive for every odd profile) of size 675512, strictly larger than the n = 18 entry 649079 of Table 4 of arXiv:2601.07336v1, and this domain is the restriction of the row-19 domain to the alternatives other than 11.
scope n=19: The 1497276 distinct linear orders on the alternatives 1..19 listed in object/n19_orders.txt.xz satisfy a never condition on every one of the 969 triples, so they form a Condorcet domain on 19 alternatives (majority relation transitive for every odd profile) of size 1497276, strictly larger than the n = 19 entry 1432836 of Table 4 of arXiv:2601.07336v1, and this domain is the restriction of the row-20 domain to the alternatives other than 5.
scope n=20: The 3336208 distinct linear orders on the alternatives 1..20 listed in object/n20_orders.txt.xz (parts part_aa and part_ab joined in name order) satisfy a never condition on every one of the 1140 triples, so they form a Condorcet domain on 20 alternatives (majority relation transitive for every odd profile) of size 3336208, strictly larger than the n = 20 entry 3155366 of Table 4 of arXiv:2601.07336v1.
scope n=22: The 16571072 distinct linear orders on the alternatives 1..22 listed in object/n22_orders.txt.xz (parts part_aa to part_af joined in name order) satisfy a never condition on every one of the 1540 triples, so they form a Condorcet domain on 22 alternatives (majority relation transitive for every odd profile) of size 16571072, strictly larger than the n = 22 entry 15037178 of Table 4 of arXiv:2601.07336v1.
scope n=23: The set D(A_23) of all linear orders on the alternatives 1..23 that obey every one of the 1771 never conditions in object/n23_assignment.txt has exactly 36894088 elements (canonical enumeration sha256 7a5a7d8ca65a2668c6f8c4bba680f6275019f94d5189a0728febeecd3da633ff) and is a Condorcet domain on 23 alternatives (majority relation transitive for every odd profile), strictly larger than the n = 23 entry 33162136 of Table 4 of arXiv:2601.07336v1.
scope n=24: The set D(A_24) of all linear orders on the alternatives 1..24 that obey every one of the 2024 never conditions in object/n24_assignment.txt has exactly 81912986 elements (canonical enumeration sha256 54baf18b85aecce8a420ce8c1b7350f86b3bf27590741ba9b23193ca0e4a0605) and is a Condorcet domain on 24 alternatives (majority relation transitive for every odd profile), strictly larger than the n = 24 entry 73279872 of Table 4 of arXiv:2601.07336v1.
scope n=25: The set D(A_25) of all linear orders on the alternatives 1..25 that obey every one of the 2300 never conditions in object/n25_assignment.txt has exactly 178950728 elements (canonical enumeration sha256 2ac0df90378e94892f7af7dc8df27581428be20fb21e90edfc751fee5246bd38) and is a Condorcet domain on 25 alternatives (majority relation transitive for every odd profile), strictly larger than the n = 25 entry 160316046 of Table 4 of arXiv:2601.07336v1.

**Not checked by me** (other skeptics' remit):
- Status freshness and the literature (NOVELTY).
- The xz-file hashes and the list-text sha256 values. My list = D(A) result does not depend on them.
- The n = 21 object, which is not in my copy.

confirmed_scope: For each n in {14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25}, this folder's row-n object (for n <= 22 the explicit list object/nN_orders.txt.xz, and for n = 23, 24, 25 the full domain D(A_n) of all linear orders on 1..n obeying object/nN_assignment.txt, of exactly counted size with a hash-pinned canonical enumeration) is a Condorcet domain on n alternatives of size 27040, 60956, 135072, 300388, 675512, 1497276, 3336208, 16571072, 36894088, 81912986 and 178950728 respectively, each strictly larger than the n entry of Table 4 of arXiv:2601.07336v1 (27026, 59430, 131536, 292015, 649079, 1432836, 3155366, 15037178, 33162136, 73279872 and 160316046), with the n = 14, 15, 18 and 19 domains being one-alternative restrictions of the n = 15, 16, 19 and 20 domains.
pass: true
