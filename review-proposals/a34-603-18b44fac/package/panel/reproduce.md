# Independent REPRODUCE report

context: fresh invocation, canonical agent identifier `/root/reproduce`, `fork_turns=none`.

Reviewer: an independently invoked AI agent sharing the filesystem with the parent. This is neither a human review nor an external review, and shared filesystem access does not provide physical isolation. I did not inspect other reports, parent reasoning, staging archives, or author checker code. My task context contained the parent's role assignment and paths only. No author checker was read at any point.

Transcript reference: the invocation identifier is `/root/reproduce`. No independently accessible transcript URI or transcript export was provided. The tool-call output chunk identifiers for the initial permitted-source reading, independent checker creation, execution, and provenance collection were respectively `2e08b9`/`2397e9`, `1952bf`, `16c67d`, and the tool result accompanying `provenance.json`. These are internal execution references, not public transcript URLs. Code and raw execution results are preserved alongside this report.

## Definition and scope

The claim definition is quoted verbatim from `claim/claim.md`:

> 603 distinct binary vectors of length 34, constant Hamming weight 7 and minimum pairwise Hamming distance at least 8.

I independently wrote `check.py` directly from this definition before reading any author code. It counts differing coordinates directly for every pair, and separately enumerates support four-subsets. It also checks the supplied baseline and every field of the proposed delta. This is exhaustive certificate verification; it is not an exhaustive search for an optimum or a reproduction of the author's search trajectory, neither of which was claimed in the permitted materials.

The bank success criterion in `claim.md` additionally requires superiority to current tables, the complement mirror cell, the named papers, and newer papers, with consistency with the tabulated upper bound. As explicitly assigned by `claim/REPRODUCE.md`, current literature/status checks belong to NOVELTY. I make no finding about novelty, priority, or full bank success. The final verdict below is exclusively the REPRODUCE certificate/reconstruction verdict.

## Observations

The certificate inputs are `claim/A34_8_7_602.txt`, `claim/A34_8_7_603.txt`, and `claim/seed_to_result_delta.json`. The permitted contextual inputs were `claim/claim.md`, `claim/status_source.md`, `claim/REPRODUCE.md`, and the role instruction `reviewer_protocols/REPRODUCE.md`. The original handoff called its certificate directory `claim_only/`; the extraction-ready review archive calls it `claim/`.

| Check | Baseline | Candidate |
|---|---:|---:|
| Distinct words | 602 | 603 |
| Length of every word | 34 | 34 |
| Weight of every word | 7 | 7 |
| Exhaustively checked unordered pairs | 180,901 | 181,503 |
| Minimum distance | 8 | 8 |
| Pairs at distance 8 | 32,414 | 32,695 |
| Pairs at distance 10 | 44,914 | 44,893 |
| Pairs at distance 12 | 75,763 | 76,073 |
| Pairs at distance 14 | 27,810 | 27,842 |
| Four-subsets checked, including unused | 46,376 | 46,376 |
| Four-subsets used once | 21,070 | 21,105 |
| Four-subsets unused | 25,306 | 25,271 |
| Four-subsets used more than once | 0 | 0 |

The raw candidate SHA-256 is `18b44fac5d5ff1d4895fd9de1240669eb71543b3e15599f7f864e090aa1491ad`; the raw baseline SHA-256 is `1a1d0958047e78b8d29752ccb0210518b170663b6862f84d57669c7b0c02d81e`. Both match the claim and delta. Files use the claimed binary format and equal the sorted LF-terminated serialization. The candidate's first and second lines witness distance exactly 8; the baseline's first and third lines do likewise (one-based indexing).

The delta removes exactly 38 distinct baseline words and adds exactly 39 distinct words absent from the baseline, leaving 564 unchanged. Its removal/addition sets exactly equal the actual set differences. Applying the delta yields exactly the candidate set; sorting and appending LF gives the exact original candidate bytes and SHA-256. Net gain is exactly one. Delta source/target labels and hashes were also checked.

Both codebooks' complements were constructed and checked directly: all vectors have weight 27, retain distinctness by the bijectivity of bitwise complementation, and all pair distances have identical histograms. This proves a corresponding size-603 certificate for A(34,8,27), without claiming any current status-table result.

## Proof reconstruction

For binary words with supports S and T, Hamming distance is the size of their symmetric difference. Since both supports have size 7, d(S,T) = |S| + |T| - 2|S intersect T| = 14 - 2|S intersect T|. Hence distance at least 8 is equivalent to intersection size at most 3. Two supports share a four-subset exactly when their intersection has size at least 4. Therefore the independent exhaustive four-subset check is equivalent to the distance constraint. There are C(34,4) = 46,376 four-subsets; each word contributes C(7,4) = 35 incidences, giving 603 times 35 = 21,105 candidate incidences. Every incidence belongs to a different four-subset.

Direct pair enumeration independently establishes the same property without invoking that equivalence. There are 603 times 602 divided by 2 = 181,503 candidate unordered pairs. The checker visits each once using indices i < j and counts all 34 unequal-coordinate indicators. The smallest observed count is eight. Together with 603 distinct words of weight seven and length 34, this establishes A(34,8,7) >= 603 by definition. Complementation changes each weight to 34 - 7 = 27 and leaves equality/inequality at each coordinate unchanged, proving the mirror certificate.

No separate analytic proof or exhaustive-search transcript was supplied in the allowed materials; no claim of an optimal value or deterministic search reproduction is made here.

## Reproduction evidence

Independent source: `validation/reproduce/check.py`. Original source is preserved as `validation/reproduce/check.original.py`. Original raw outputs: `validation/reproduce/run1.json` and `validation/reproduce/run2.json`. Original environment/version and output/code hashes: `validation/reproduce/provenance.json`. The portable rerun output is `validation/reproduce/run_portable.json`; revision provenance is `validation/reproduce/provenance_portable.json`.

Portable commands, run from the extracted review archive root:

```sh
python validation/reproduce/check.py claim > validation/reproduce/run_portable.json
cmp validation/reproduce/run1.json validation/reproduce/run_portable.json
```

The original two executions used the same checker mathematics and the original handoff input directory. For this packaging revision I reran the portable checker against the same original handoff inputs with these relative commands, both of which exited successfully:

```sh
python validation/reproduce/check.py extracted/A34_603_Reviewer_Handoff/claim_only > validation/reproduce/run_portable.json
cmp validation/reproduce/run1.json validation/reproduce/run_portable.json
```

Two independent executions produced byte-identical raw result files. No mismatch, missing certificate object, or nondeterminism was observed. This demonstrates deterministic behavior for these runs, not a general theorem about arbitrary future runtime environments.

Verdict: PASS for exhaustive mathematical certificate verification and exact baseline-plus-delta reconstruction. Current-status novelty and full bank acceptance remain outside this role and are not established by this report.

Packaging revision: the same reviewer changed input-path selection to a required command-line directory argument, replaced host filesystem references with relative archive references, and reran the checker. Mathematical logic and verdict were unchanged; the portable run is byte-identical to the original output. No other reviewer material was read. Original logs/provenance were retained. Canonical agent identifier `/root/reproduce` is an invocation identifier, not a filesystem path.

Signed off: `/root/reproduce`, independent AI invocation, 2026-10-14; packaging revision in the same invocation.

pass: true
