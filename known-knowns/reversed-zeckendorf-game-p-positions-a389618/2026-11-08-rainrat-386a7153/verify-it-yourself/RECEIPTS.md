# Verification Receipts

## Command
```sh
/usr/bin/time -v sh verify-it-yourself/run_checks.sh
```

## Exact Output and Timing (`NUMERICAL`)
```text
Verified 249 contiguous rows (n=2..250): V(250)=21890964, E(250)=209975689, W(250)=1
Verified literal BFS on n=2..35, all 128 Table A1 rows (n=2..129), Theorem 1.1, and 4 negative controls (including frontier n=130).
Extension n=130..250: 30 P-positions (A389618), 91 N-positions (A389619).
Verified byte-identical match against fresh recomputation by both independent C++ solvers (universal_delta_solver and colex_rank_solver) across n=2..250.
PASS
	Command being timed: "sh verify-it-yourself/run_checks.sh"
	User time (seconds): 386.17
	System time (seconds): 4.93
	Percent of CPU this job got: 1022%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:38.23
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 121968
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 247587
	Voluntary context switches: 1186
	Involuntary context switches: 25569
	Swaps: 0
	File system inputs: 0
	File system outputs: 504
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```
