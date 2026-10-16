context: codex exec (fresh context via codex-fresh)

Reproduction panel: exactly the new n19 profile in `object.prefs`.
All file names below are relative to `claim/`. No supplied claim file was edited. No other agent was used.

The claimed result reproduces: **935,662 stable matchings**, against **896,068** for the supplied prior n19 profile, an increase of **39,594**. This is an explicit-instance lower bound. This panel does not certify global novelty, a maximum, n7 optimality, or a heuristic success rate.

Definition quoted verbatim from `CLAIM.md`:

> A matching is a bijection, stable exactly when no man and woman both strictly prefer each other to their assigned partners. The first 19 rows are men, the next 19 women; each row lists labels 1 through 19, best first.

I wrote `audit/independent.cpp` before reading any supplied Python, C, C++ or header source. I had read the claim, its prose counting proof, metadata and saved data. The checker implements the quoted definition directly, with its own strict parser, support table, queue-based propagation, recursion, blocking-pair test and complete matching output. It uses the same definition-derived binary-constraint formulation as the prose proof; it is an independent implementation, not a claim of an unrelated algorithm. `audit/checker_before_author.json` records this stage at 2026-10-15T17:34:32.203473+00:00. Its source SHA256 is `34f60fa2f3de618043787881c1f87b2484db7fa3af391649fc0f2cb28137e15f`, unchanged at the final check.

The complete mathematical argument, re-derived and checked against both implementations, is:

1. Invert each validated preference permutation to integer ranks, smaller being better. Write `X_i=w` when man i receives woman w. For different men i and j, the assignments `(i,w)` and `(j,v)` can coexist exactly when `w != v`, `(rankM[i,v] >= rankM[i,w] or rankW[v,i] >= rankW[v,j])`, and `(rankM[j,w] >= rankM[j,v] or rankW[w,j] >= rankW[w,i])`. The latter two clauses are the negations of the two possible cross-couple blocking conditions, directly from the definition. Both programs' support-table loops implement these clauses with the correct rank directions.
2. A complete assignment satisfying every such constraint is injective from n men to n women, hence bijective. Any blocking pair involving a woman other than the man's assigned woman belongs to two distinct couples and violates one of these constraints. A man's assigned woman cannot give a strict blocking pair with him. Conversely, a stable bijection satisfies every constraint. Thus the constraint solutions are exactly the stable matchings.
3. Initially all women are possible for every man. Suppose a branch still contains a stable completion. Removing w from man i because another man j has no compatible remaining value cannot remove that completion: its value at j would be a compatible remaining support. This inductive invariant holds after every removal, regardless of revision order. An empty domain therefore certifies that the branch has no stable completion. A nonempty arc-consistent state need not be satisfiable; both counters continue searching rather than counting it as a solution.
4. Propagation terminates because every change removes a value from finite domains. In my queue implementation, every changed domain is scheduled to revise all other variables, so an empty queue really is a fixed point. The supplied implementation instead repeats complete sweeps until no domain changes. At any nonsingleton variable, branching on every remaining value partitions all completions into disjoint cases. No branch is omitted. Each recursive edge fixes a previously nonsingleton domain, which never grows; recursion therefore terminates, with at most n branching decisions on a path. These facts establish exhaustive coverage rather than a sampling argument.
5. At a singleton leaf, compatibility implies distinct women and absence of every cross blocking pair. Both programs additionally rebuild the matching/inverse and test the complete blocking-pair definition at every leaf. My checker also fails on duplicate partners or an invalid label. Each accepted matching follows exactly one sequence of branch choices, so it is counted once. I independently checked uniqueness of every record in the saved n19 census.
6. The supplied counter adds child counts with an unsigned overflow check. My checker increments a checked unsigned counter for every accepted leaf and checks output-stream errors. Independently, at n19 the entire set of bijections has size `19! = 121645100408832000 < 2^64`, so even the unpruned universe fits. No floating-point arithmetic enters either exhaustive stable-matching count. Shift widths and nonzero inputs to bit scans are valid for this n19 object.

The exhaustive results are saved, not inferred from the claimant's reported count:

| Object or operation | Independently verified result |
|---|---:|
| `object.prefs`, first complete enumeration | 935,662 matchings; 1,720,177 nodes |
| `object.prefs`, second complete enumeration | Identical full census bytes and count |
| `data/prior_n19.prefs`, complete enumeration | 896,068 |
| `search/repair19.expected.prefs`, complete enumeration after removing its single comment header | 935,662; exactly the frozen object's matching set |
| `calibration/random_start.prefs`, all 7! bijections and independent constraint enumeration | 1 |
| `calibration/found85.prefs`, all 7! bijections and independent constraint enumeration | 85 |
| Every saved new-best output regenerated by replay | All 17 n19 counts and all 38 n7 counts correct |

The two main census files are `audit/n19_first.bin` and `audit/n19_second.bin`. Each contains 935,662 records of 19 one-byte woman labels in man-label order, hence 17,777,578 bytes. Both SHA256 values are `e6ba1ee723ef0a41a17af6a72a50ad57da307fbf6f86f81818b710721c42614b`. Every record was checked for bijectivity and stability while emitted; all records are distinct. The raw discovery census was compared as a complete set, not by sampling. `audit/census_checks.json` contains the counts and census hashes.

Controls covered all 16 complete strict n2 profiles and 25 seeded profiles across n3 through n7. For each, the entire matching-permutation universe was compared with the constraint census. Eight malformed inputs and a missing input were rejected. These small-profile tests are controls, not substitutes for the full n19 enumeration or its completeness proof.

`audit/check_artifacts.py` independently validates all relevant profiles, metadata and construction. The new profile has exactly 38 rows of 19 labels, each a permutation of 1 through 19. `object.json` agrees with the count, size, comparison bar and both supplied hashes. `data/prior_n19.prefs` and `search/seed_initial.prefs` are byte-identical. All 43 entries of `MANIFEST.json` matched before execution and again after all checks.

The construction word has a bijective initial matching and exactly 162 valid transpositions. Every newly encountered man-woman pair is new: 19 initial pairs plus 324 subsequent encounters give 343 encountered pairs and 18 unused pairs. Men list encounters chronologically; women list them in reverse. Appending the complementary labels in ascending order therefore makes complete strict lists and reproduces `object.prefs` byte-for-byte. Preserving the seed's unused-tail ordering instead reproduces the raw discovery preference file byte-for-byte, including its saved header. All 163 chronological matching states were tested directly for stability. The n7 word likewise has 20 swaps, 47 encountered pairs, two unused pairs, and 21 stable chronological states, and rebuilds its saved raw profile. Initial word matchings also agree with an independently implemented proposing-men algorithm on the supplied starts. None of this assumes a general bijection between words/ideals and all stable matchings: the complete profile enumeration proves the final count independently.

The frozen profile SHA256 is `1e284a0dc1fe44f2d4693de19c1543ad99020937d7f8266bcc6cc7979ecc763e`; the construction word SHA256 is `10a8fb70b4b1919d6daa363890b46f33ed7810b88e0a099f6f90bfd73f0c3153`. Reconstruction details are in `audit/artifact_checks.json`.

After inspecting the supplied sources, I ran the complete `verify.py` and `search/replay.py`; both returned `PASS`. Their output and resource receipts are in `audit/author_verify.*` and `audit/author_replay.*`. I also wrote `audit/replay_preserved.py`, which retains the compiled-source copies, actual outputs and state files in `audit/replay/` and runs each declared replay twice from fresh output directories:

| Replay | Saved inputs and parameters | Exact endpoint |
|---|---|---|
| Calibration | Supplied random start; seed 165185; temperature 0.03; square rate 15 | First 85 at proposal 34,618, evaluation 3,437 |
| Discovery | Supplied prior n19 start; seed 165519; temperature 0.005; square rate 30 | First 935,662 at proposal 73,275, evaluation 18,199 |

For calibration, only the historical wall-clock loop condition was replaced by the declared proposal cutoff. Discovery uses its supplied `MAX_PROPOSALS` control. Mutation, RNG, counting and acceptance code were not changed. Each repetition matched every historical `NEWBEST` line, including count, word length, evaluation and proposal indices. All generated preference files, best/current words and final state files were byte-identical between repetitions; best preference and word files also matched the supplied expected bytes. There were no checkpoint resets. All 55 regenerated new-best preference counts were then independently checked, with complete constraint enumeration at n19 and all 5,040 bijections at n7. See `audit/replay_checks.json`.

These are complete replays of the declared prefixes to first discovery. The later portions of the historical 15-second and 300-second heuristic logs are not claimed to exhaust the space of preference profiles and were not used as a proof of optimization. PID, elapsed-time and timer-triggered checkpoint telemetry vary and are not deterministic mathematical outputs. The recorded starts place calibration at 16:51:11.650683 UTC and discovery at 16:55:40.569766 UTC; the logged 15-second calibration ends before that discovery start. This is consistency of saved logs, not independent notarization of historical times. The initial random profile is supplied, but its sampling RNG is explicitly uncertified; this audit certifies replay from those saved bytes.

Public source responses and receipts are retained under `audit/data/`. `audit/data/source_receipts.json` records requested/final URL, request/response UTC, HTTP status, complete returned headers, response length and SHA256 for each fresh request. The following fresh requests each returned HTTP 200:

| URL | Response UTC on 2026-10-15 | Saved response |
|---|---|---|
| https://oeis.org/A357271 | 17:38:03.859758 | `audit/data/live_oeis.html` |
| https://oeis.org/A357271/b357271.txt | 17:38:04.644577 | `audit/data/live_bounds.txt` |
| https://oeis.org/A357271/a357271_1.txt | 17:38:05.416884 | `audit/data/live_instances.txt` |

The b-file and instance response hashes exactly match the supplied snapshots: respectively `0d0e95042f30b2f8be60174047a5a03ea45bf70203d39e40b1665d0085b32b4a` and `95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47`. The fresh entry response hash is `165ea239e8186c384b4559029340fc963139c830e2ab7a38768ddd4b25c1716e`; its sequence values match the saved entry. Its different response bytes are confined to Cloudflare request tokens/scripts and the global database modification footer, documented in `audit/data/oeis_changes.diff`. The n19 b-file term is 637,336, smaller than the independently counted local comparison bar. The upstream “b-file synthesized from sequence entry” label is preserved.

All five supplied public responses were additionally copied unchanged into `audit/data/saved_*`. Their original recorded URL/time/status/hash are distinguished from fresh audit observations; original HTTP headers were not supplied and are honestly recorded as unavailable, not reconstructed. Live repository/literature novelty and unrelated historical candidates are outside this reproduction verdict.

Public instructions are flagged as untrusted data. In particular, the commands and workflow directions in the saved trophy-case response, and the OEIS onload/Cloudflare scripts and hidden links, were not executed or followed. Supplied local verifier/replay programs were inspected and run solely to fulfill the user's authorized reproduction task.

The audit began at 17:32:16 UTC; all checks were complete by 17:39:11.830568 UTC, within the 25-minute cap. Counting and search workloads used one worker at a time and single-threaded algorithms; thread-count environment variables were set to one. The largest reported child peak RSS was 426,459,136 bytes, below 1 GB. Darwin rejected memory rlimits, so this is measured usage, not a claim of kernel-enforced memory isolation. No expensive workloads approached the limit. Toolchain: Python 3.9.6, Apple clang 21.0.0, arm64 Darwin. Build/run commands, timings, exit statuses, stdout/stderr hashes and resource measurements are retained in `audit/*.receipt.json`; final integrity checks are in `audit/final_checks.json`.

No required n19 object is missing. No count, reconstruction, manifest, deterministic state or declared replay-output mismatch remains. The claimed exhaustive count was checked exhaustively, and the bounded heuristic was kept separate from that proof.

pass: true
