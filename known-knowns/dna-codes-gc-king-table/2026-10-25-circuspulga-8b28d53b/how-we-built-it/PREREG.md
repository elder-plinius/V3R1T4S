# PREREG — A_4^GC(19,14,9), re-done formalization run
frozen: 2026-10-25T10:17:04Z (start_utc.txt, from date -u; folder name from date -u +%Y-%m-%d-%H%M, UTC)
null_test: required
target: dna-codes-gc-king-table, cell n=19 d=14 w=9. Expected table value: 38 (unmarked). Expected object: 44 words, sha256 8b28d53b3639dc0cc9d1a1afd37dfca139f5c3852c66003db5ee118b476c1a1a.

## prior sight (disclosed)
This result was already seen before this PREREG. First in the exploratory sweep runs/2026-10-25-0955. That folder was named by hand and the name is misleading: the sweep started at 2026-10-25T08:51:32Z. It was seen again in runs/2026-10-25-0948 (PREREG 09:48:30Z), whose CRITERION skeptic failed.
runs/2026-10-25-1015 is an aborted attempt: its PREREG text was broken by shell quoting, and nothing was measured. This run is a clean re-formalization, not a blind search.

## bank criterion (verbatim, repo/known-unknowns/biology/dna-codes-gc-king-table.md line 11, repo commit 1ebdef41c30414cd2a036b00f5e81d0fc4c1dc25)
> A plain-text list of codewords for some (n,d) whose table entry on https://rambutan.umassmed.edu/king/dnacodes.html is NOT followed by '.' or ':' such that a checker confirms all words have length n over {A,C,G,T}, exactly the table's GC-content w (w = floor(n/2), confirm from King 2003), pairwise Hamming distance >= d, are distinct, and the count is strictly greater than the table entry re-fetched live immediately before claiming, AND strictly greater than any value for the same (n,d,w) found by a novelty search of post-2010 literature (e.g. Limbachiya-Gupta-Rao altruistic-algorithm papers, Montemanni-Smith, arXiv 1903.03535, 2108.02033).

## code (frozen sha256)
- attempts/regenerate/code/gf4slice.py d37c340ed102534ba3c3d68f04a5335539ba9a6baddc9945216bbe887fb7549c
- attempts/null-and-leak-auditor/code/nullsample.c 7c5e3d1aa8831e110084edc29626fc450db7950ee485db6acdfdfe563358b3ee
- checker/check_gc_code.py ba053c3e29af5b2b82815e15e9c6af9560cfc16d1a07d4beb029c00217f5bb70

## regeneration (deterministic)
command: python3 attempts/regenerate/code/gf4slice.py 19 1 3000 attempts/regenerate/A4GC_19_14_object.txt
seed: 1; restarts: 3000. If the sha256 differs from the expected value, that is reported.

## run-level criterion
The object's size must exceed the table value in data/dnacodes.html, fetched once in this run. The command `python3 checker/check_gc_code.py OBJECT 19 14 data/dnacodes.html` must print "VERDICT: VALID, beats_table=True", and `python3 checker/check_gc_code.py --selftest OBJECT 19 14` must print PASS.
The bank criterion's post-2010 literature clause is left to the NOVELTY skeptic. Until it is met, the run stays PROMISING at most.

## null
Pre-registered substitute: nullsample 19 14, seeds 1..400, STOP=20000000. It replaces nullgreedy, which does not fit in RAM at n=19.
Statistic: code size. The real object beats the null if real > max over the 400 controls.
