# Independent CRITERION review — frozen M8734
context: fresh delegated subagent, given frozen object and pinned bank definition; no author checker or other reviewer verdicts read
reviewed_utc: 2026-10-19T11:24:00.137229+00:00
mathematical_validity: PASS
bank_literal_success: PENDING CURRENT COMPARISONS
novelty: PENDING STATUS CHECK
packaging: NOT REVIEWED; no package/gate PASS claimed
confirmed_scope: The file CANDIDATE_M8734.txt (SHA256 f9f280613ee2a5c500220a9f022d35d83264a14f96d940c9a517a15cebdf6fde) contains 8734 distinct binary words of length25 and weight11 with every pair at Hamming distance at least6, proving A(25,6,11)>=8734.

PROVED-HERE: every supplied row has length25, alphabet{0,1}, weight11; row count and distinct count are8734; SHA256 matches the frozen digest. The independent checker enumerated every one of480370 9-subsets across all8734 words. All480370 are unique. This is a full certificate, not a pair sample.

Proof: identify a word with its support S. For |S|=|T|=11, Hamming distance is |S symmetric_difference T|=22-2|S intersection T|. Thus distance>=6 iff intersection<=8. Intersection>=9 iff there exists a 9-subset present in both words. The checker assigns each sorted 9-subset (a1,...,a9), zero-based coordinates, the exact colex rank sum(C(aj,j),j=1..9). This is an injective enumeration into C(25,9)=2042975 slots. Each slot records its owning row and a second owner is rejected. Therefore every pair satisfies the required distance.

The control suite passed all9 cases: valid distance6 pair and singleton accepted; distance4 valid-weight pair, duplicate, incorrect weight, incorrect length, changed file versus pinned hash, incorrect count, invalid alphabet rejected for their intended reasons. No null experiment is required: this checks an explicit object deterministically and makes no search or statistical significance claim.

Literal bank success criterion:
> Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell of https://aeb.win.tue.nl/codes/Andw.html (also checking the mirror cell A(n,d,n-w)), and also strictly greater than any value for that cell in arXiv:2608.13906 (Echols, 124 improved cells), arXiv:2607.19550 (Lysenstoen) or any newer arXiv paper. M must not exceed the tabulated upper bound; exceeding it means a bug.

Concrete unresolved conditions: live lower bounds for A(25,6,11) and A(25,6,14); live upper bound for both equivalent cells; maximum value for this cell in arXiv:2608.13906, arXiv:2607.19550 and newer arXiv papers; repo trophy/open contributions and equivalent or larger submissions. This review has performed no network request and has received no source receipts. These conditions are not implied by validity. A tie is not a full win. The object is not a rational dual upper certificate (p2). A p1 certificate claim would additionally require evidence that no explicit code already exists; nothing here establishes that.

The equivalent complement code has weight14, the same8734 rows and unchanged pair distances; this does not remove the requirement to compare the mirror cell.

Evidence files: checker.py, checker.stdout.json, checker.stderr.txt, guard.py, guard_receipt.json, host_memory_before.txt, host_memory_after.txt, instruction_hashes.json. No other reviewer's code or verdict was used.

Resources: numerical child ran one interpreter thread, exit0, elapsed 0.2121678750263527s, max RSS 32391168 bytes, below268435456-byte/900-second caps. Guard violation:null. Own lock was removed on completion. Host memory snapshots exist before/after; no global memory-floor PASS is claimed.

Decision: local object valid; genuine non-subsumed bank win remains unconfirmed pending source receipts. Default false until the literal criterion can be evaluated completely.
pass: false
