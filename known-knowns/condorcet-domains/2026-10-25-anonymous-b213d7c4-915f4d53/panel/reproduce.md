# REPRODUCE skeptic

context: fresh subagent

Scope: reproduction of the single frozen assignment in `claim/assignment.txt`.
Only claim-package research inputs were read. No attempts, research notes,
author reasoning outside the claim, or other panel reports were read. The
requested route was `gpt-6.1-sol` with `xhigh`; effective runtime settings are
not independently observable from this context. No network requests or
descendants were used. All computation was short foreground validation in the
default sandbox, with no background processes or elevated computation.

Definition used, quoted from the frozen criterion:

> The object is a never-condition assignment A: exactly one line 'a b c iNj' for each of the C(n,3) triples a < b < c of 1..n, meaning the i-th smallest of {a,b,c} is never in position j (1 = top, 3 = bottom) within the triple.

`panel/reproduce-work/independent.py` was written and successfully run before
`claim/verify_assignment.py` was opened. It uses only the Python standard
library and takes the assignment path through argv. It constructs orders from
bottom to top, memoizing the exact number of completions for each suffix set.
When the forbidden element of a triple is added, k partners already in the
suffix means its final position within the triple is 3-k, so it rejects exactly
when k = 3-j. Each order follows exactly one path, and the suffix set contains
all information needed for subsequent choices. Python integers are exact.
There is no sampling, cap on counted orders, probabilistic estimate, or search
space truncation.

Commands run from the run directory (both exited 0):

```text
python3 panel/reproduce-work/independent.py claim/assignment.txt
python3 claim/verify_assignment.py claim/assignment.txt 25 180870896
```

The independent implementation was also run once before the supplied verifier
was read; its second run reproduced every mathematical value and the SHA.
The saved outputs are `panel/reproduce-work/independent-output.txt`,
`panel/reproduce-work/independent-repeat-output.txt`, and
`panel/reproduce-work/supplied-output.txt`.

Actual independent output summary:

```text
SHA256 915f4d534bc6a8557649f3b02bf4ed21d8782ce01a450c2c39c53c25751d508b
parsed_triples 2300
Fishburn 9 488 states 125
Fishburn 20 2115186 states 6109
first9_DP 458 brute_all_9factorial 458 permutations 362880 states 92
full_exact_count 180870896 states 4598
PASS
```

The independent strict parser verifies all 2300 unique triples of 1..25, sorted
and within range, with i,j in 1..3 and no missing triple. All eleven deliberate
negative inputs were rejected: missing line, duplicate triple, extra line,
unsorted triple, zero label, out-of-range label, invalid i, invalid j, malformed
condition syntax, extra token, and blank line. The actual assignment passed.
Fishburn's alternating assignment (middle alternative forbidden top for even
middle label and bottom for odd) gave the requested n=9 and n=20 calibrations.
Every one of the 9! first-nine orders was evaluated directly against its 84
conditions, independently of the DP; precisely 458 passed, matching that
restriction's DP count. This restriction is a calibration and is not being
presented as the n=25 enumeration.

Afterward the supplied implementation was inspected and run. Its forward
prefix DP independently returned n=25, 2300 triples, exact_count=180870896,
reachable_prefix_sets=3792, the same assignment SHA256, and first9_dp=
first9_bruteforce=458, ending in PASS. Its calibration output reports
Fishburn9=488 and Fishburn20=2115186 with malformed negatives rejected.
The numbers of suffix and prefix states differ because the two algorithms
traverse opposite directions; they are not counts of the same partial objects.

PROVED-HERE (finite exact computation): the frozen assignment defines exactly
180870896 orders under the quoted never-position definition, and two separate
implementations agree. The assignment identity, completeness, calibrations,
exhaustive first-nine comparison, and a repeat of the independent full count
all pass. No nondeterminism or mismatch was observed.

Reproduction limits: this review does not establish current comparison-table
values, novelty, optimality, the historical source attribution for Sen's
theorem, or the full binding success criterion's external-source clauses.
Those belong to the other panel roles and coordinator. No native search count
or search artifact outside `claim/` was consulted; the supplied Python forward
DP and this independent suffix DP are the two reproduced exact counters.

pass: true
