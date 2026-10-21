# Independent mathematical reproduction

reviewer: Independent Codex REPRODUCE skeptic
context: fresh Codex subagent with no inherited conversation
scope: Mathematical validity of the frozen submitted object only.

## Definition and independence

The mathematical condition in `claim/target.json` is: "an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even)". The supplied claim instantiates this as M = 5997, n = 26, w = 9, d = 6.

Only `claim/CLAIM.json`, `claim/target.json`, and `claim/object/A26_6_9_5997.txt` were inspected as claim inputs. No author checker, author code, earlier review, memory, literature material, unrelated mission, or research search was used. The independent checker was written directly from this definition before any author tooling was read; no author tooling was read at any point.

## Exact method

`independent-reproduce/check_exact.py` uses only the Python standard library. It hashes the original bytes, decodes ASCII strictly, splits line boundaries without trimming word characters, requires exactly 5997 words, checks that each word consists solely of binary digits and has length 26 and weight 9, and checks distinctness using a set.

Each word is then converted to an integer. For every unordered pair i < j, the checker computes `(left ^ right).bit_count()`, the exact Hamming distance. It tracks the global minimum and any violation, and continues through every pair rather than stopping at a counterexample or sampling. A successful result also requires the checked pair count to equal M(M-1)/2 and the supplied SHA256 to match. The real object was checked once, as a finite job at nice level 10, using the workspace virtual-environment Python.

## Calibration performed before the object check

All seven handmade tests passed their expected outcomes. They are recorded with full inputs and outputs in `independent-reproduce/receipt.json`:

| Case | Handmade words | Expected and observed result |
| --- | --- | --- |
| Positive, n=6,w=2,d=4 | 110000; 001100; 000011 | Accepted; 3 pairs; minimum distance 4 |
| Duplicate | 110000; 110000 | Rejected for duplicate and distance; minimum 0 |
| Wrong weight | 111000 | Rejected for weight |
| Wrong length | 11000 | Rejected for length |
| Inadequate distance | 110000; 101000 | Rejected for distance; minimum 2 |
| Wrong count | 110000, with expected count 2 | Rejected for count |
| Nonbinary alphabet | 11000x | Rejected for alphabet |

The negative cases use n=6,w=2,d=4 and their actual listed count except the explicit wrong-count case.

## Actual evidence

- Started UTC: 2026-10-17T14:15:18.133087+00:00.
- Finished UTC: 2026-10-17T14:15:18.783251+00:00.
- Original object size: 161919 bytes.
- Object SHA256: `6be5a215f0b662497e21330c98db83b5128095af52e4a45a8484ba60ff524de8`; matches the supplied expected hash.
- Word count: 5997; distinct word count: 5997.
- Every word has binary alphabet, length 26, and Hamming weight 9.
- Exhaustive unordered pairs checked: 17979006 = 5997*5996/2.
- Observed exact minimum Hamming distance: 6.
- Distance violations: none; other validation errors: none.
- Checker process exit code: 0, independently observed in the process result and recorded in the JSON output.
- Full actual output: `independent-reproduce/receipt.json`.
- Checker SHA256: `7b8cd623f3bf705dd19bae8ac1dd03446649ddcb45fd63d364241a29fe0c90cd`.
- Receipt SHA256: `8eb51ae14b1c6be2c0cb3396147c0851960d792744f3d7e57080d0f8fc20785a`.

The command below reproduces the executed check from `independent-reproduce/`; choose a new output filename to preserve the original receipt:

```sh
nice -n 10 ../../../../.venv/bin/python check_exact.py ../claim/object/A26_6_9_5997.txt --n 26 --w 9 --d 6 --count 5997 --sha256 6be5a215f0b662497e21330c98db83b5128095af52e4a45a8484ba60ff524de8 > recheck.json
```

## Verdict and boundary

PASS for mathematical reproduction: the fixed bytes encode 5997 distinct binary length-26 words, each of weight 9, with all pairwise Hamming distances at least 6. This independently supplies a valid construction establishing A(26,6,9) >= 5997. This report makes no finding about novelty, optimality, priority, table improvement, publication eligibility, or external acceptance. It does not set the manager's honesty gate or replace other required reviewers.

pass: true
