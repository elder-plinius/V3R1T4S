context: subagent (fresh fork_turns none)
identity: REPRODUCE skeptic, agent reproduce_fresh

Verdict: PASS for the explicit lower-bound witness A(27,6,10) >= 13026.

I first read step 6 of `../upstream/repo/kit/RUN.md` and `../upstream/repo/AGENTS.md`, then only the claim, target definition and witness. I did not read other reviews. This report's file references and commands are relative to `claim/`.

Definition quoted from `CLAIM.md`: “A(n,d,w) is the maximum cardinality of a set of distinct binary vectors of length n, each of weight w, with all pairwise Hamming distances at least d.”

I wrote `../reviews/reproduce_fresh/check_witness.py` directly from that definition, froze it at 2026-10-14T02:48:48.188266+00:00 (SHA-256 `5cc3f6c4f42ef5581bfe81641cdaa048f2c87c008482975d597d3c578efe9045`), and launched its exhaustive run before reading author code. Author code was inspected only after the checker was written and timestamped; the independent process completed without changes. `../reviews/reproduce_fresh/checker_freeze.json` records that sequence. The checker uses Python integer XOR and bit count for each unordered pair, independent of the author's shared-eight-subset method.

Commands to repeat from `claim/` (Python 3, standard library):

```sh
python3 ../reviews/reproduce_fresh/check_witness.py A27_6_10_13026.txt > ../reviews/reproduce_fresh/independent_check.log 2>&1
python3 -B ../reviews/reproduce_fresh/reproduce.py ../evidence/verify_and_rebuild_A_27_6_10.py A27_6_10_13026.txt > ../reviews/reproduce_fresh/reproduction.log 2>&1
```

The positive control consists of `111000` and `000111`, with weight 3 and distance 6. Negative controls separately test distance 2, duplicate words, incorrect weight, incorrect length, nonbinary characters and incorrect cardinality; all six are rejected. Both positive and negative controls use the same checker as the witness.

The executed independent log establishes 13,026 distinct binary vectors, each of length 27 and weight 10. Exactly 84,831,825 unordered pairs were checked; minimum distance is 6. No sampling or probabilistic argument is used. The pair histogram is:

| Distance | Pairs |
| --- | ---: |
| 6 | 956,670 |
| 8 | 4,965,051 |
| 10 | 15,539,547 |
| 12 | 26,352,091 |
| 14 | 23,355,752 |
| 16 | 11,017,900 |
| 18 | 2,454,798 |
| 20 | 190,016 |

The saved witness has 364,728 bytes and SHA-256 `9e824e9f8a92e74226231152fc8e8a972be5ba79549e2a10e512fe63a3934f49`. The exhaustive check took 12.912600 seconds as measured in the log. Since an explicit set satisfies all defining constraints, its cardinality proves the stated lower bound directly, without any assumptions about the search or algebraic construction.

After inspecting the author's reconstruction for safe local execution, I rebuilt the code twice and ran its verifier both times. `../reviews/reproduce_fresh/reproduction.log` records exact byte equality to `A27_6_10_13026.txt` in each run (not merely set equality or matching hashes). Both runs reconstruct the same 13,026 words and 364,728 bytes with the witness hash above. No nondeterminism or mismatch was observed.

The author's subset verifier is mathematically valid here: weight-10 words have distance 20 minus twice their intersection size, so distance below 6 is equivalent to sharing at least eight coordinates; repeated eight-subsets therefore detect exactly those violations. The independent pairwise computation does not depend on this argument. The construction's group-theoretic narrative is unnecessary to the explicit-witness lower bound and is not certified here.

Confirmed scope: The saved witness is an explicit binary constant-weight code of length 27, weight 10, cardinality 13026 and minimum Hamming distance 6, proving A(27,6,10) >= 13026.

No verdict is given on auxiliary upper bounds, uniqueness or optimality of constructions, table comparisons, record novelty, or satisfaction of the target's broader strict-improvement criterion.

Evidence files: `../reviews/reproduce_fresh/check_witness.py`, `../reviews/reproduce_fresh/checker_freeze.json`, `../reviews/reproduce_fresh/independent_check.log`, `../reviews/reproduce_fresh/reproduce.py`, and `../reviews/reproduce_fresh/reproduction.log`.

pass: true
