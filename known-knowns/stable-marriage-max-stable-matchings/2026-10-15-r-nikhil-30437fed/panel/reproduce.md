context: codex exec (fresh context via codex-fresh)

The single claimed complete strict n=13 profile in `object.prefs` has exactly **9,836 stable matchings**, exceeding the independently recounted `data/prior_n13.prefs` value **9,796 by 40**. The fixed-profile mathematical claim and its stated deterministic reproduction pass. This is an explicit-instance lower bound, not a maximum or a certification of current global novelty.

The definition quoted from `CLAIM.md` is:

> A matching is a bijection. It is stable exactly when no man and woman both strictly prefer each other to their assigned partners. The first13 rows are men, the next13 women; every row orders labels1 through13, best first.

All filenames below are relative to `claim/`. No supplied file was modified. No additional agent or network request was used.

I wrote `audit/independent.cpp` and its streaming driver before opening any supplied implementation. The documents read beforehand were `CLAIM.md`, `COUNTING_PROOF.md`, `REPRODUCE.md`, the explicit preferences and word, metadata, and manifest. The checker uses fixed-order prefix enumeration, independently of the author's arc-consistency implementation. Its frozen SHA256 is `71501696e7b17b19d2421bfa0231949d7812d79b4f1bd46ae7d07014ecdd2abc`; `audit/checker_start.json` records this at 2026-10-15T17:51:29.099898+00:00. This is a local audit receipt, not an externally authenticated timestamp. A compile-time name collision was corrected before reading author code; the checker then remained unchanged.

The independent counter's proof follows directly from the definition:

1. At depth k, precisely the first k men have assigned, distinct women. The next man branches over every unused woman, so every bijection has exactly one possible root-to-leaf path.
2. Suppose the new couple is (k,w) and an earlier couple is (i,v). Reject the extension precisely if i prefers w to v and w prefers i to k, or if k prefers v to w and v prefers k to i. Either condition is an actual blocking pair whose two partners are already fixed. No later assignment can repair it. Therefore rejection cannot remove a stable completion.
3. Every prefix of every stable matching survives, so every stable matching reaches a leaf. At each leaf a separately written check constructs the inverse bijection and tests all 13×13 man/woman pairs against the definition. Thus every emitted leaf is stable.
4. Depth increases to 13; every branch is finite; there is no time, node, sample, or count cutoff. Unique assignment paths rule out double counting. Integer counters explicitly fail on overflow.

`object.prefs` has exactly 26 rows, and each row is exactly a permutation of 1 through 13. Its SHA256 is `30437fed4d5de6bf272631b49ae7a94298a2fdefb65c3cd5529df582506c9c56`. The word SHA256 is `cc29b1303f99b3a31ee75daa9977930949ebb97bf6f88fbce258f6c9971fa340`. Both agree with `object.json`. All 45 entries of `MANIFEST.json` exist and match; no supplied file is omitted except the manifest itself. They were checked again after the work and remained unchanged (`audit/manifest_check.json`, `audit/final_checks.json`).

The complete independent search visited **157,751 prefix nodes**, rejected **479,187 extensions** containing blocking pairs, and accepted **9,836 leaves**. Depth counts are preserved in `audit/object_run1.json` and `audit/object_run2.json`. Both complete runs produced identical counts and the same matching-stream SHA256:

`4fc843af5e822e67945ffb9e85f77ead0f7491308593b1c283c1746668569732`

The stream consists of 13 one-based unsigned bytes per matching, men in label order, matchings in lexicographic order, with no separators: **127,868 bytes**. It was hashed and discarded incrementally; no matching collection was dumped to disk. Exhaustive pruning, not a sample of the 13! bijections, establishes the count.

The comparison and other supporting counts were also complete:

| Saved evidence | Exact result | Independent evidence |
|---|---:|---|
| `data/prior_n13.prefs` | 9,796 | `audit/prior.json`; matching digest `92d2035ee2e36d758c7a3f3f784f0d5bc888c377a865b698f287ad1a99d88f71` |
| `search/expected_raw.prefs` | 9,836 | `audit/raw.json`; identical stable-matching stream to the final object |
| n=13 ranking table in `data/instances.txt` | 7,123 | Ranks independently inverted into lists; `audit/published_7123.json` |
| `calibration/random_start.prefs` | 1 | All 5,040 permutations tested by a second, Python implementation |
| `calibration/found85.prefs` | 85 | All 5,040 permutations tested by that Python implementation |

Comments in ancillary preference files were removed into audit copies before feeding the strict independent parser; all preference entries were retained. The Python n=7 exhaustive streams agree with the C++ counter, including digests. The independent counter also accepted the one-couple and known two-matching controls, and rejected duplicate labels, missing rows, out-of-range labels, noninteger garbage, empty input, and ragged rows. Details are in `audit/structural_checks.json`.

I checked each step of `COUNTING_PROOF.md` against `arc_count.cpp`:

1. Write the integer preference ranks as r_m and r_w, with smaller ranks preferred. For two men i≠j assigned w and v, compatibility is exactly w≠v, not [r_i(v)<r_i(w) and r_v(i)<r_v(j)], and not [r_j(w)<r_j(v) and r_w(j)<r_w(i)]. These are exactly the support-mask conditions in the source. For a bijection, every potentially blocking unmatched pair lies between two couples, so pairwise compatibility is equivalent to stability.
2. Initially all women occur in every domain. If a value belonging to a stable completion were removed because another man's domain lacked a support, that completion's value at the other man would be a support still present by induction, a contradiction. Sequential domain updates and repetition preserve this invariant. An empty domain consequently proves the branch has no completion.
3. The consistency loop can only shrink finite domains. After its fixed point, branching fixes a nonsingleton domain to each of its remaining values. The branches are exhaustive and disjoint. Along a recursive edge the total domain size strictly decreases, establishing termination.
4. At a singleton leaf, compatibility forbids duplicate women and all blocking cross pairs. With n distinct assignments among n women, the assignment is a bijection. The implementation additionally checks the used-woman mask and all blocking pairs directly before returning one.
5. Internal sums check `UINT64_MAX - total < child_count` before addition. The n=13 bit shifts are within the stated limit of 31. Consequently the returned sum counts all stable leaves exactly once without silent overflow.

Running the unmodified `verify.py` returned `PASS`, with 18,006 recursion nodes, 9,836 stable leaves, complete=true, construction_rebuilds=true, and improvement=40 (`audit/author_verify.log`). Its claimed positive and malformed controls passed. The independent manifest check covers all supplied files in addition to the object hashes checked by that script. The mathematical certification here concerns the validated saved input, not a blanket guarantee about every possible malformed input to the author's utilities.

The construction was re-derived independently in `audit/structural_checks.py`. The initial tokens form a permutation. At each event, destinations are read from the pre-event assignment, and each listed man receives the next listed man's token. The 72 events are 71 swaps followed by the cycle [2,9,5] in the word's zero-based notation. Every new encounter is distinct; there are **158 distinct man/woman encounters**. Men list their encounters chronologically, women in reverse chronology, and untouched labels are appended in ascending order. This reproduces `object.prefs` byte for byte. Replacing ascending tails with the seed's tail ordering reproduces the raw saved preference rows. Removing the final event recovers the prior profile's rows. All 73 chronological assignments were checked to be stable in the final profile.

The final event is also an exposed three-person rotation, not merely a syntactic cycle. At the penultimate matching the next willing-partner holder map is 3→10→6→3 in one-based labels, and no other man has a next willing partner. The transfers are man 3: woman 6→2; man 10: woman 2→12; man 6: woman 12→6. Both endpoint matchings pass the full stability check (`audit/final_rotation.json`).

As a further complete fixed-object check, `audit/exhaustive_family.py` forms event precedence from each participating man's preceding event and enumerates **all 9,836 ideals**, visiting 304,044 recursion nodes. It applies each ideal and checks every resulting matching directly for stability. To verify injectivity, it decodes each matching back to its ideal: because each man's encounter history has no repeated woman, his partner identifies how many of his events occurred; these progress counts uniquely recover event membership. Every decoded ideal equals its source ideal. Thus these are 9,836 distinct stable matchings; the complete independent counter proves there are no others. No generalized cycle/rotation-poset theorem is assumed. The order-independent sum of per-matching SHA256 values modulo 2^256 agrees with the direct enumerator and is `221fca8cd4a503a118e1526a8acb40a094f37bebfdf1dcae551d8f364e246ae4` (`audit/fixed_word_ideals.json`).

Discovery reproduction was checked at its actual stated scope. Three runs of `search/replay.py` printed `PASS`. They reproduced the supplied word and raw preference bytes. The graft trajectory reached its saved first improvement at proposal **2,673,573**, valid evaluation **30,008**, RNG state **2432212175335879719**. The calibration reproduced every saved NEWBEST line through its first 85 at proposal **34,618**, evaluation **3,437**, with seed 165185, temperature 0.03, and square rate 15. It reconstructed the saved calibration word and preferences exactly. The saved initial profile is reused and its original sampling RNG is not certified; this demonstrates one reproducible trajectory, not a success rate, fresh random sampling, or n=7 optimality.

The suffix-family enumeration was independently repeated in full, including every candidate and every allowed further extension through depth five. An edge a→b exists exactly when a has not encountered b's current token. Every allowed suffix event is a simple directed cycle of that graph. Requiring its least label first removes only cyclic duplicate representations; both orientations remain eligible. The first event requires arity at least three, later events at least two. Every resulting state is recursively explored. There were exactly **three evaluated extensions and 90 cycle-walk nodes**, with no cutoff; all three occurred at depth one and had no allowed continuation:

| Cycle, zero-based labels | Independently enumerated stable matchings |
|---|---:|
| [0,10,9,5] | 9,804 |
| [2,9,5] | 9,836 |
| [4,5,8,7] | 9,816 |

The candidate counts, profile digests and matching digests are in `audit/suffix_family.json`. This is completeness within the explicitly fixed seed and suffix family. The graft procedure is a heuristic trajectory; neither procedure is an exhaustive search of all n=13 profiles.

The three replay transcripts agree after removing clock-triggered checkpoint lines and normalizing only PID and elapsed-time fields. Their common normalized SHA256 is `56fbfbfe19edb5d2d09c0325711c0edbcfb4c3fd0e21571424816d73a891c653`. Saved NEWBEST sequences, final counters, output bytes and asserted RNG state agree. Elapsed times, process IDs and wall-clock checkpoint positions are telemetry, not deterministic mathematical outputs. The second replay's `/usr/bin/time -l` wrapper failed to query `kern.clockrate` after the replay printed PASS; the subsequent directly supervised replay returned zero and recorded resources successfully. This utility failure is recorded in `audit/final_checks.json` and does not conceal a failed claim check.

Recorded calibration start is 16:51:11.650683 UTC; the supplied log ends after 15 seconds. Pilot and suffix starts are 17:13:20.990090 and 17:15:51.849418 UTC on 2026-10-15. These local logs consistently place calibration before both discovery procedures. They do not authenticate historical wall time or prove an externally witnessed prospective registration.

Saved public responses were treated solely as untrusted evidence. The five hashes in `data/fetches.json` match their saved bodies; the recorded statuses are 200. The saved b-file states 6,720 at n=13, and the saved published ranking table independently counts to 7,123. Public shell/compiler instructions in `data/TROPHY_CASE.md`, MiniZinc-use directions in `data/instances.txt`, and scripts/navigation in `data/oeis.html` were ignored and flagged in `audit/saved_sources.json`. No third-party response was fetched during this audit, so there is no new fetch receipt requiring headers. The supplied receipts do not contain selected response headers. Historical weaker-bound mentions, unrelated sizes, literature pointers and unseen materials are not premises of the fixed-profile result; current literature priority remains outside this reproduction panel.

All workload processes were run sequentially with single-threaded counting/search code and numerical thread settings fixed to one. The resource-recorded full replay took 45.33 seconds and reported peak resident memory **61,521,920 bytes**, below 1 GB. Audit artifacts occupied approximately 113 KB at the final check, far below 500 MB; subsequent receipts and this panel remain negligible. The work completed within the 25-minute limit. Compact counts and digests were preserved under `audit/`; supplied claim files stayed unchanged. No required object, mathematical mismatch, incomplete enumeration, or nondeterministic result remains unresolved.

pass: true
