# REPRODUCE — exact constant-weight-code object

context: subagent fresh independent Mac reproduction context; own checker derived from the mathematical definition before running it; no Windows checker code or Windows checker result used as reproduction evidence

Formalized UTC: 2026-10-19T11:52:10.378671+00:00. This panel records the already completed run; no mathematical rerun was performed to write this file.

## Claim and criterion reproduced

Claim: The exact object in `../run/CANDIDATE_M8734.txt` contains 8734 distinct binary words of length 25, each of Hamming weight exactly 11, and every pair of distinct words has Hamming distance at least 6. Consequently, this explicit object proves A(25,6,11) >= 8734.

Definition: A(n,d,w) is the maximum cardinality of a set of binary words of length n and weight w whose pairwise Hamming distances are at least d. The reproduced criterion is the explicit-object validity component: exactly M distinct binary n-tuples, weight w, all unordered pair distances >= d, with (n,d,w,M) = (25,6,11,8734).

This panel passes scoped mathematical reproduction only. It does not establish strict improvement over current tables or literature. Novelty, the global honesty gate, package checks and publication are outside this panel's scope; no conclusion from another reviewer is adopted here.

## Independent method and observed result

The original, unmodified independent program is `checker.py`. It uses only the Python standard library. It decodes the text as ASCII, requires exactly 8734 rows, requires each row to contain exactly 25 binary characters, checks each integer's bit_count() equals 11, and requires 8734 distinct integers. Text coordinate i is represented as integer bit i.

For every index pair 0 <= i < j < 8734, it calculates `(words[i] ^ words[j]).bit_count()`. XOR identifies exactly the differing coordinates, so this is the Hamming distance. Each unordered pair is visited once. The expected pair count is 8734*8733/2 = 38137011; the observed checked count is 38137011. The run returned exit code 0 and pass = true. Minimum observed distance: 6.

Full observed distance histogram:

| Distance | Unordered pairs |
|---|---:|
| 6 | 657169 |
| 8 | 2652252 |
| 10 | 7965356 |
| 12 | 11975256 |
| 14 | 9533429 |
| 16 | 4330519 |
| 18 | 919672 |
| 20 | 100335 |
| 22 | 3023 |

The histogram totals 38137011 pairs. Cardinality counts explicit distinct codewords, not symmetry orbits.

Seven calibration cases passed before the candidate check: a hand-constructed positive code {111000,000111} with n=6, w=3 and distance 6; a duplicate-word corruption; an invalid-weight corruption; an invalid-width corruption; a distance-2 corruption preserving weight 11 and uniqueness; an incorrect expected count; and an incorrect expected SHA256. Corruptions were applied to separate copies. The positive returned 0; each deliberately invalid case returned 1 with its expected rejection reason.

The NPY companion `../run/CANDIDATE_M8734.npy` was read independently with standard-library parsing of its NPY 1.0 header and little-endian int64 payload. Its shape is (8734,). Every integer equals the corresponding text word under text-coordinate-i = bit-i convention. Both source hashes matched before/after the completed reproduction.

## Identity and execution evidence

- TXT SHA256: `f9f280613ee2a5c500220a9f022d35d83264a14f96d940c9a517a15cebdf6fde`.
- NPY SHA256: `d9a093d62fb0e314c85584b0f4e98afe7e4e9ad7460615cc88ec4bb27897db96`.
- Original independent checker SHA256: `5769d0fef1e24b0b085fafcca88788d1abc790071b8a1a7414575055ce9f4e9d`.
- Candidate-check start UTC: 2026-10-19T11:22:22.207714+00:00.
- Candidate-check end UTC: 2026-10-19T11:22:25.581421+00:00.
- Candidate-check wall time: 3.373711500 seconds.
- Peak RSS observed by getrusage on Darwin: 23314432 bytes.
- One main Python compute thread; no numerical library or worker threads.

This was a new Manager verification, not reactivation of an older Mac techlead run. The proportional budget was one compute thread, numerical RSS <=256 MiB and wall time <=15 minutes; the historical 12 GiB reservation was not accredited. Memory enforcement was sampled/self-checked rather than an instantaneous OS RSS ceiling. The completed run stayed within the budget. Physical-memory and pressure observations were recorded before and after the run.

The local audit trail remains separate from this public panel. This panel contains relative artifact references only. The manifest accompanying this panel records its generation UTC and hashes without altering the original checker, object or reproduction report.

pass: true
