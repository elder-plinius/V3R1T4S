# REPRODUCE: inherited n23 claim

context: codex exec (fresh context via codex-fresh)

The saved n23 claim reproduces. The explicit profile has exactly **19,305,568 stable matchings**, exceeding the independently counted saved predecessor's **19,290,640** by **14,928**. No unresolved mismatch, missing required object, or nondeterministic mathematical result was found.

I reviewed the inherited historical criterion literally. The criterion in `CLAIM.md` matches `search/PREREG.md` verbatim. Its eligible n ≥ 17 cell requires beating the saved A357271 composition bound; the saved n23 term is 15,481,956. The stronger local comparison was also checked. This is a reproduction verdict for that inherited claim, not a fresh global-novelty assessment or a maximum claim.

The definition in `CLAIM.md` is:

> A matching is a bijection. It is stable exactly when no man and woman both strictly prefer each other to their assigned partners. The first 23 rows are men, the next 23 women; every row orders labels 1 through 23, best first.

Before reading any supplied executable source, I wrote `review/independent.cpp` from this definition. It validates every preference row, builds binary compatibility constraints, exhaustively branches with sound domain pruning, and independently checks bijectivity and blocking pairs at every accepted leaf. It imports no author code. Its SHA-256 is `98cba53e37e0cf930d446e8933e0cc6e1bf8502112d78ed042b77124e95fe992`. The later `review/memo.cpp` adds exact residual-state memoization to these independently written constraints; `review/audit.py` independently checks receipts, construction, controls, and the complete suffix family.

| Saved object | n | Independently verified stable matchings |
|---|---:|---:|
| `object.prefs` | 23 | 19,305,568 |
| `data/prior_n23.prefs` | 23 | 19,290,640 |
| `search/repair23.expected.prefs` | 23 | 19,290,640 |
| `search/seed_initial.prefs` | 23 | 19,025,864 |
| `calibration/random_start.prefs` | 7 | 1 |
| `calibration/found85.prefs` | 7 | 85 |

The final profile's independent exhaustive run visited 35,526,695 search nodes. A separate repeat produced exactly the same count, node count, and matching checksum, `12698416009006274952`. Both saved predecessor forms independently produced the same count, node count, and checksum. Their unused preference tails have different orderings: the raw repair preserves seed ordering, while the comparison profile uses ascending labels. Both were reconstructed using their respective conventions. Evidence is in `review/counts.jsonl`, `review/repeated-counts.jsonl`, and `review/final-validation.json`.

I re-derived every step of `COUNTING_PROOF.md`; the detailed derivation is saved in `review/derivation.md`:

1. Write r_i(w) for man i's rank of w and s_w(i) for woman w's rank of i. Two assignments (i,w), (j,v), with i ≠ j, are compatible exactly when w ≠ v and neither `r_i(v) < r_i(w) && s_v(i) < s_v(j)` nor `r_j(w) < r_j(v) && s_w(j) < s_w(i)` holds. These are precisely injectivity and the two possible cross-couple blocking pairs.
2. Every stable matching satisfies those constraints. Conversely, a complete satisfying assignment is injective between equal finite sets, hence bijective. Any blocking pair would cross two distinct assigned couples and violate one of their constraints. Thus compatibility is sufficient as well as necessary.
3. Deleting a value without support in another variable cannot delete a stable completion: that completion's assignment to the other variable would supply a support. Induction preserves every stable completion after every deletion; an empty domain certifies no completion. Domains only shrink, so propagation terminates.
4. Branching on every remaining value of one nonsingleton domain partitions all completions into disjoint children. Each child strictly reduces domain cardinality, proving termination. Singleton leaves are checked directly against the definition. Therefore every stable matching is counted exactly once, without sampling. Unsigned count additions are checked for overflow.
5. The author's support construction, fixed-point pruning, branching, leaf checks, and overflow guard implement these steps. The independent implementation schedules changed domains instead of rescanning every pair. Its later memoization removes fixed variables only after their compatibility constraints have propagated. Identical residual domains then describe identical residual problems; caching their exact counts preserves every branch's multiplicity.

The construction also checks independently. `construction.word` consists of the 229 saved repair swaps followed by the zero-based suffix `[[0,17,21],[7,14,12],[20,21]]`. Every simultaneous token permutation is valid and every new encounter is nonrepeating. Chronological men's histories, reversed women's histories, and the specified unused tails reproduce `object.prefs` byte for byte. All 233 prefix matchings are stable under the final preferences. For each of the 232 cycles, every participating man's first lower-ranked woman who prefers him to her current partner is exactly the next token specified by the cycle, verifying that the cycle is an exposed rotation. No general word-to-poset theorem is needed for the independent stable-matching count.

The suffix check is exhaustive for the stated family. I regenerated every simple directed cycle in each unused-pair graph, canonically rooted at its least-labelled vertex, with minimum length three initially and two thereafter, and recursively visited every extension through depth four. The independent traversal matches **all 93 saved records**, including every count, and covers **40 distinct preference profiles**. The selected suffix is the first maximum in the specified traversal and has count 19,305,568. The author's scan also completed all 93 nodes without reaching its time/node guards (`cutoff: false`). No sample was accepted as evidence of this exhaustive result. Full independent records are in `review/suffix-independent.json`.

Both supplied entry points completed with `PASS`: `python3 verify.py` and `python3 search/replay.py`, run sequentially through `review/limited.py`. The verifier independently reported 19,305,568 stable leaves. Discovery reproduced the exact preference and word bytes at proposal 669,716, evaluation 161,410; calibration reproduced its exact bytes at proposal 34,618, evaluation 3,437. All **49** saved `NEWBEST` events matched, including counts, word lengths, evaluations, and proposals. The suffix replay reproduced the final JSON and preference bytes. Logs are `review/author-verify.log`, `review/author-replay.log`, and `review/replay-events.json`.

All **51** original manifest entries and all **five** HTTP-response receipts match their saved SHA-256 values, and the original files remain unchanged. The b-file agrees with the saved OEIS sequence. Both representations of each published ranking matrix agree; their independently enumerated counts are 81, 365, 1,690, 7,123, and 27,059 for n = 7, 9, 11, 13, and 15. The two independent counters also agree with direct permutation enumeration on 74 control profiles, covering 57,416 permutations, and reject five malformed inputs. These controls supplement the complete n23 enumeration and complete suffix audit.

The saved calibration start plus its 15-second run precedes the historical n19 start, which precedes the n23 start. As explicitly disclosed in the package, those are unauthenticated local timestamps, and the reused random starting profile's sampling RNG is not certified. The reproducible claim is the saved-start trajectory; no sampling-success rate or independently authenticated chronology is inferred. No blocked endpoint was retried, no web request or outward action was made, and no other session or prior run folder was consulted.

Counters and searches ran sequentially with one computation thread. The largest recorded child-process peak resident memory was 370,229,248 bytes, below 1.5 GB. The final independent audit, including the full suffix check and rotation checks, passed; see `review/audit-final.log`, `review/audit-results.json`, the resource receipts in `review/`, and `review/final-validation.json`.

pass: true