# Independent Mac Manager reproduction

Mathematical validity: **PASS**. Label: PROVED-HERE.

Exact object: 8734 distinct binary words of length 25, weight 11.
All 38,137,011 unordered pairs were checked by XOR + bit_count.
Minimum distance: 6. Histogram: {'6': 657169, '8': 2652252, '10': 7965356, '12': 11975256, '14': 9533429, '16': 4330519, '18': 919672, '20': 100335, '22': 3023}.
Thus this explicit object proves A(25,6,11) >= 8734, independently of novelty.
TXT SHA256: `f9f280613ee2a5c500220a9f022d35d83264a14f96d940c9a517a15cebdf6fde`. NPY SHA256: `d9a093d62fb0e314c85584b0f4e98afe7e4e9ad7460615cc88ec4bb27897db96`.
The NPY is elementwise equal under text-coordinate-i = bit-i convention.

Started UTC: 2026-10-19T11:22:21.745550+00:00; ended UTC: 2026-10-19T11:22:25.607113+00:00.
Candidate checker wall: 3.373711 seconds.
Candidate peak RSS from getrusage on Darwin (bytes): 23314432.
One Python main thread, standard library only; no numerical libraries or workers.
RSS is additionally polled at 50ms intervals and self-checked every 200 outer rows;
this is sampled enforcement, not an OS-enforced instantaneous RSS ceiling.
Hard CPU limit: 880 seconds; own-PID watchdog: 900 seconds.
No resource-limit termination occurred. No other process was signalled.
Physical-memory and pressure command output before/after is retained in separate files.

Calibration: 7 cases passed: hand-constructed positive, duplicate,
wrong weight, wrong width, weight-preserving distance-2 corruption, wrong count,
and wrong expected hash. Each corruption is a separate copy; originals stayed read-only.
Expected rejection return codes are 1; positive and candidate return codes are 0.

This is a new Manager verification. It does not reactivate the old Mac techlead.
The old 12 GiB reservation was not accredited; the proportional budget is one compute
thread, <=256 MiB numerical RSS, <=15 minutes. No research/search was performed.
Novelty was not assessed; global CONFIRMED status was not assigned; no package gate
or publication was performed. A mathematical PASS does not replace those gates.
The root workspace report/log are untouched because this is not a new research run.

Definition and method are in checker.py. PREREG.json freezes the criterion/budget.
commands.json records exact commands, UTC and exit codes; stdout/stderr and resource
receipts are preserved. Reproduce with the candidate command in commands.json.

Physical memory observations (whole system):

- before: vm_stat free 2691661824 bytes (2.506805 GiB); speculative 64716800 bytes; pressure level 1; memory_pressure free report 48%.
- after: vm_stat free 3667509248 bytes (3.415634 GiB); speculative 66617344 bytes; pressure level 1; memory_pressure free report 49%.

These are whole-system observations, not memory reserved by this verifier. The two free-memory metrics have different definitions.

Evidence audit: PASS. Controller exit code observed: 0. Own lock released; recorded source and program hashes match.
