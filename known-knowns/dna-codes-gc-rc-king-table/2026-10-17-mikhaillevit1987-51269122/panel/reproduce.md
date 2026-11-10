# Skeptic: REPRODUCE

context: subagent (Claude Code Agent tool, general-purpose, fresh context)

Scope: only `skeptic_reproduce/claim/` was read. No network was used.

## Definition checked (quoted from claim/CLAIM.md)

> checked to satisfy: length n, alphabet ACGT, GC count = floor(n/2), pairwise Hamming >= d, Hamming(x, rc(y)) >= d for all x,y including x=y, distinct

> reverse complement: reverse the word and swap A<->T, C<->G

Here n = 20, d = 15, floor(n/2) = 10. The claimed value is size 16 > 15 (table entry for (20,15)).

## Independent checker

Path: `skeptic_reproduce/my_check.py`. I wrote it before opening `claim/checker/check_dna.py`. It uses only the Python standard library.
It hard-codes n=20 and d=15 from the claim instead of reading them from the object. It checks every one of the 120 unordered pairs and all
256 ordered (x, rc(y)) pairs, including the 16 self-pairs. It also checks the sha256 of the file and that the declared n/d/size fields match.

Command (from `skeptic_reproduce/`): `python -I my_check.py claim/object/code_20_15_16.json`

Output (`skeptic_reproduce/my_check_run1.txt`). Run 2 (`my_check_run2.txt`) is byte-identical:

```
sha256 e3a3a885c67a9a34329ed2247d32dfe004b64645b8d2bd97ef528009a77e2de7
size 16
lengths [20]
alphabet_ACGT True
gc_counts [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
distinct True
pairs 120 min_pairwise 15
rc_pairs_checked 256 min_rc_all 15
min_self_rc 16 min_rc_cross 15
declared n,d,size 20 15 16
size_gt_table_15 True
VALID True
```

Summary: size 16. All 16 words are distinct, have length 20, use only ACGT and have GC = 10. Minimum pairwise distance is 15.
Minimum RC distance over all x,y is 15 (min self-RC 16, min cross-RC 15). The sha256 matches the value in CLAIM.md
(`e3a3a885c67a9a34329ed2247d32dfe004b64645b8d2bd97ef528009a77e2de7`).

## Author's commands (claim/REPRODUCE.md), each run twice

From `skeptic_reproduce/claim/`: `python -I checker/check_dna.py --self-test` (exit 0, both runs):

```
positive: {'valid': True, 'n': 2, 'd': 2, 'w': 1, 'size': 2}
negative rejected: RC self-pair reverse-complement distance
negative rejected: duplicate duplicate codeword
negative rejected: pair distance pairwise distance
negative rejected: GC weight GC weight
CHECKER SELF-TEST: PASS
```

`python -I checker/check_dna.py object/code_20_15_16.json` (exit 0, both runs):

```
{"valid": true, "n": 20, "d": 15, "w": 10, "size": 16}
```

This matches the expected last line in REPRODUCE.md exactly. Run 1 and run 2 gave byte-identical output for both commands
(`skeptic_reproduce/author_*_run{1,2}.txt`).

## Comparison / mismatches

- My checker and the author's agree: the code is valid and has size 16. I found no mismatch.
- The author's checker implements the definition correctly. Its rc uses translate ACGT->TGCA plus reverse. Its RC loop covers all ordered pairs including x=y. Its pairwise loop covers all unordered pairs. It checks distinctness, length, alphabet and GC = n//2.
- Minor robustness note, not a mismatch: the author's checker validates with `assert`, so under `python -O` it would print valid without checking anything. The documented commands do not use `-O`.
- Minor note: the author's checker takes n and d from the object file rather than from the claim. Here they match (20, 15). My checker fixed n and d independently.
- I did not verify (outside the REPRODUCE scope, and no network): that the live King table entry for (20,15) is 15 with no '.' or ':' marker, and novelty against post-2010 literature. The comparison "16 > 15" rests on `claim/table_record/` only, and that record itself says to re-fetch.
- This is a finite-object check, not an exhaustive search. Every pair was checked, not a sample.

Verdict for REPRODUCE: the object's validity and its size 16 are confirmed independently and deterministically.

pass: true
