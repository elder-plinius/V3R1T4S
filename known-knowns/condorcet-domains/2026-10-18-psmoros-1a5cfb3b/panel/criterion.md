Saved by the main session from the subagent's returned text (CRITERION skeptic, Agent tool, fresh context, model opus; returned about 03:54Z 2026-10-18). The skeptic's preface to the main session is omitted and answered in panel/gate.md; the panel text below, after its "---" separator, is verbatim.

# Panel: CRITERION skeptic, run folder 2026-10-18-0238

context: subagent (Claude Code Agent tool, fresh context, model opus)

Read: claim/CLAIM.md, claim/PREREG.md, claim/REPRODUCE.md, all five files in claim/status/, and claim/object/. I did not use claim/tools/. All checks below come from my own programs, written fresh for this panel (C and Python, standard library only). No web requests were made.

## Criterion (verbatim)

"For some n >= 9, an explicit set of linear orders on n alternatives on which majority rule is transitive for every profile (every triple satisfies a never-condition), strictly larger than the best published Condorcet domain for that n."

This quarry has no enumerated partial wins, so only the full criterion is judged.

## Literal reading, clause by clause

**"For some n >= 9".** This is existential: one n is enough. The claim uses n = 21. 21 >= 9, and PREREG rule 1 (9 <= n <= 22) holds.

**"an explicit set of linear orders on n alternatives".**
- The object is the byte stream you get by concatenating object/n21_orders.txt.xz.part_aa, part_ab and part_ac in that order and xz-decompressing it.
- Is a compressed, split file "explicit"? I read yes:
  - The split is a plain concatenation, pinned by the sha256 of the joined file.
  - xz is a generic lossless container.
  - The decompressed text writes out every order, one per line.
  - No domain-specific program and no implicit description (such as a never-condition set) is needed to obtain the list.
- object/n21_assignment.txt is an implicit description. CLAIM.md declares it a by-product, not the object, and I did not count it as the object.
- My own hashes match CLAIM.md: the three parts, the joined file (1a5cfb3b...b75d), the decompressed text (0cb0dd88...8e27) and the assignment (aefb526e...2f5d).
- My strict parser requires exactly 21 tokens per line, each an integer 1..21 occurring once, single spaces, no leading zeros and a final newline. It found 7467760 lines and 0 malformed, so every line is a linear order on {1..21}.
- Distinctness was proved two ways:
  - the lines are strictly increasing in lexicographic order;
  - a sort of packed 105-bit keys gives 7467760 distinct keys and 0 duplicates.

**"on which majority rule is transitive for every profile (every triple satisfies a never-condition)".**
- Hidden quantifier: "every profile". The paper's definition (Section 2, quoted in CLAIM.md) speaks only of profiles "with an odd number of agents". The criterion's parenthetical makes Sen's triple condition the test.
- Read with even profiles and ties included (the weak majority relation), the clause would fail for nearly every domain, including Fishburn's and every published record. My n = 3 enumeration shows this: 33 of the 48 never-condition sets on 3 alternatives have an even profile (2 to 8 voters) whose weak majority relation is intransitive. So the clause can only carry its standard odd-profile meaning, which is what the parenthetical says.
- On 3 alternatives the two readings agree exactly. For all 63 nonempty sets of orders, "satisfies a never condition" matched "every odd profile with 1, 3, 5 or 7 voters is transitive": 63 agree, 0 disagree.
- Why the triple check is enough on 21 alternatives:
  - With an odd number of voters, the majority relation is a tournament.
  - A tournament is transitive if and only if it has no cyclic triple.
  - The majority relation on a triple depends only on the domain's restriction to that triple.
  - So checking all C(21,3) = 1330 triples is sufficient.
- As a by-product, the strict majority relation stayed transitive for every even profile up to 8 voters on every never-condition set: 0 failures.
- Object result:
  - 1330 triples, 0 violations, no impossible (cyclic) patterns.
  - Every triple restriction has exactly 4 orders, so the domain is copious.
  - Exactly one never condition holds per triple, all of peak-pit type: 1N1 161, 1N3 359, 2N1 311, 2N3 92, 3N1 188, 3N3 219.

**"strictly larger than the best published Condorcet domain for that n".**
- "That n" is 21; values for other n do not count.
- What the record is:
  - status/records_table4.tsv and Table 4 of arXiv:2601.07336v1 give n = 21 as "≥ 6674931", marked ks.
  - Section 8: "the entries marked with subscript ks are obtained by applying the construction of [16] to the domains found for smaller n" ([16] is Karpov and Slinko).
  - Section 6: the direct inductive search stopped at n = 20: "The same approach would likely improve the bounds for larger n as well, but we stopped at n = 20".
  - Abstract: the ks construction gives "the currently largest known domains for 21 ≤ n ≤ 25".
- So the n = 21 record is a construction value, not a search value, and it is soft. Its x21/x20 ratio of 2.115 is the lowest in Table 4 for n >= 9.
- It is still the best published value: the paper says so, and it is the value the frozen PREREG names.
- The "≥" sign is Table 4's uniform notation for lower bounds on f(n). It is also used on searched entries such as ≥ 492. It does not mean a larger n = 21 domain was published.
- Unpublished restrictions of the published n = 22 domain are not "published values". The authors had their n = 22 domain and still list 6674931 for n = 21.
- Null baselines from published general constructions applied to Table 4 inputs (output below):
  - Proposition 1, 2 f(a) f(21-a): at most 6310732.
  - Fishburn replacement, f(a) f(22-a): at most 6310732.
  - Fishburn's own n = 21 domain: 4443896.
  - All are below 6674931 and below the object.
- Comparison: 7467760 > 6674931, a difference of 792829 (+11.8777 %). It is not a tie.
- Version status: the saved abstract page shows only [v1] (Mon, 12 Jan 2026). The human's hand check (status/human_status_check.md, 2026-10-18T00:58Z) also says v1 only.
- Gap: PREREG rule 2 also requires a literature re-check right before the claim (journals, the authors' pages and repositories, open and closed V3R1T4S pull requests). claim/ records only the arXiv hand check. I did not search. "Best published" is therefore confirmed relative to Table 4 of arXiv:2601.07336v1 only, and confirmed_scope says exactly that. If the main session has no rule-2 re-check on record, that is a process gap for it and the novelty lens, not a defect in the object.

**Subsumption (PREREG rule 3).**
- The stated method is the paper's Section 5.1 inductive extension step (a published search method, not one of rule 3's listed constructions), run past n = 20, followed by local search and restriction from higher n.
- Even if it counted as "a published construction on published inputs", rule 3 lets it count, because Table 4 lists less than 7467760 at n = 21.
- No published n = 21 domain can equal the object, since every published one has at most 6674931 orders.
- Structural check: all 21 restrictions of the object to 20 alternatives have between 3162160 and 3311844 orders. Every one is above, so not equal to, the published n = 20 maximum of 3155366.
  - Hence the object is not S1 or S2 (published n = 20 domain, one alternative). Such a product restricts to its 20-alternative factor.
  - For the same reason it is not Fishburn's replacement with the published n = 20 domain as the large factor.
  - I did not test splits into smaller blocks or the Karpov–Slinko construction structurally.

**Bundling (PREREG rule 4).**
- The claim sentence asserts one n and one object. Every factual part of it was reproduced, except "best published" beyond the named source (see the gap above).
- The by-product assignment, though not claimed, also checks out:
  - the list obeys it on all 1330 triples;
  - the list is exactly the full set of orders obeying it. An independent insertion-DFS count gives 7467760.
- Side finding: every restriction of the object to 20 alternatives beats the n = 20 record of 3155366. The largest is 3311844, a gain of +4.96 %.
  - So n = 20 also qualifies through the same object.
  - It is not claimed here, and rule 4 picks the larger relative gain. Since 11.88 % > 4.96 %, the choice of n = 21 as carrier agrees with rule 4 for these restrictions.
  - I did not compute restrictions to 19 or fewer alternatives.
  - I cannot see the run's other objects (for example n = 22), which are outside claim/.

## My checks and their real output

The checker is my own C program. It does strict parsing, distinctness both by lexicographic increase and by sorting packed keys, a 6-pattern mask for every one of the C(n,3) triples, evaluation of all nine iNj forms, an optional comparison with the assignment, and the sizes of all restrictions to n-1 alternatives.

I validated it on test files generated by my own Python code (Fishburn alternating scheme):

```
fishburn 9: 488  fishburn 8: 222
f9 (n=9):  ... distinct 488 duplicates 0 ... triples 84 violations 0 ... size 488 PASS
f8 (n=8):  ... distinct 222 ... triples 56 violations 0 ... size 222 PASS
f8_plus_one (order 1 2 3 4 5 6 8 7 added): ... triples 56 violations 6 ... size 223 FAIL
all3 (all 6 orders, n=3): triples 1 violations 1 ... size 6 FAIL
f9_dup: ... distinct 488 duplicates 1 not_strictly_lex_increasing 1 ... FAIL
f9_malformed: ... malformed 1 ... FAIL
```

Hashes, from my own shasum run:

```
joined parts: 1a5cfb3b80fe8600bee47668e068a0fcf8923f87f895da9e23a1efe07f02b75d
decompressed: 0cb0dd880cc7a0ad640634f505b7520bd2a5c0bb95fd7a2ce4d56fbeb8578e27 (403259040 bytes)
```

Object (n = 21), verbatim:

```
n 21 lines 7467760 malformed 0 kept 7467760 distinct 7467760 duplicates 0 not_strictly_lex_increasing 0
triples 1330 violations 0 impossible_codes 0
restriction-size histogram over triples (size:count): 4:1330
triples on which iNj holds (i=1..3 smallest, j=1 top,2 mid,3 bottom): 1N1:161 1N2:0 1N3:359 2N1:311 2N2:0 2N3:92 3N1:188 3N2:0 3N3:219
assignment lines 1330 unparsable 0 triples_missing 0 triples_repeated 0 triples_where_list_breaks_it 0
size 7467760 PASS
exit 0
```

Restrictions to 20 alternatives, from the same program's earlier run (identical PASS lines; its assignment parse had a format bug that I fixed for the rerun above):

```
restriction deleting 1: 3285824    deleting 2: 3281488    deleting 3: 3260524
deleting 4: 3294632    deleting 5: 3244604    deleting 6: 3311844    deleting 7: 3243664
deleting 8: 3277068    deleting 9: 3269052    deleting 10: 3162160   deleting 11: 3162160
deleting 12: 3243664   deleting 13: 3277068   deleting 14: 3269052   deleting 15: 3311844
deleting 16: 3260952   deleting 17: 3294632   deleting 18: 3260952   deleting 19: 3281488
deleting 20: 3238780   deleting 21: 3254700
largest restriction to 20 alternatives: 3311844
```

Full-domain count of the by-product assignment, from my own insertion DFS (validated on the Fishburn n = 8 and n = 9 assignments: 222 and 488):

```
assignment lines 1330; orders obeying it on [k] for k=1..21: 1 2 4 9 18 43 86 180 377 781 1904 4521 10615 24207 56908 124607 284430 650732 1481440 3254700 7467760
full domain size 7467760
```

Definition check on n = 3 (Python):

```
nonempty sets of orders on 3 alternatives: 63
satisfy a never condition: 48  all odd profiles (1..7 voters) transitive: 48
never condition <=> odd-profile transitivity: agree 63 disagree 0
never-condition sets with an even profile (2..8) whose STRICT majority relation is intransitive: 0
never-condition sets with an even profile (2..8) whose WEAK majority relation is intransitive: 33
```

Null baselines from Table 4 values (Python):

```
Table 4 n=21 (ks): 6674931
Prop. 1 best 2 f(a) f(21-a): (6310732, 20, 1)
Fishburn replacement best f(a) f(22-a): (6310732, 20, 2)
claimed size 7467760; gain over Table 4: 0.118777
Table 4 n=21 / n=20 ratio: 2.1154  n=22 / n=21: 2.2528
claimed / Table 4 n=20: 2.3667
```

The object's own ratio to its largest 20-restriction is 7467760 / 3311844 = 2.255. That is in line with Table 4's ratios of about 2.20 to 2.25, so nothing suggests a counting artefact.

## Judgement

Read literally, the full criterion is met:
- n = 21 >= 9;
- an explicit list of 7467760 distinct linear orders on 21 alternatives;
- every triple satisfies a never condition, which gives transitive majority for every odd profile (the definition's sense);
- strictly larger than 6674931, the best published n = 21 value in the named status source.

Rule 3 is satisfied, and the claim is not subsumed by any published domain. Nothing extra is bundled into the claim. The one open item is procedural, not about the object: claim/ has no record of the rule-2 literature re-check outside arXiv. The scope below is limited to the named status source.

confirmed_scope: The three files object/n21_orders.txt.xz.part_aa, part_ab and part_ac, joined in that order and xz-decompressed (sha256 0cb0dd880cc7a0ad640634f505b7520bd2a5c0bb95fd7a2ce4d56fbeb8578e27), list 7467760 distinct linear orders on the alternatives 1..21 whose restriction to each of the 1330 triples satisfies a never condition, so they form a Condorcet domain on 21 alternatives (in the odd-profile sense of arXiv:2601.07336v1, Section 2) strictly larger than 6674931, the n = 21 entry of Table 4 of arXiv:2601.07336v1, the only version of that paper at the human's hand check of 2026-10-18T00:58Z.

pass: true
