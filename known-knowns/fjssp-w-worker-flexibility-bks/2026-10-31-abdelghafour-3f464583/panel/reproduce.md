# REPRODUCE skeptic verdict: p2-all95 (FJSSP-W, 95 schedules)

context: subagent (Claude Code Agent tool, fresh context)

## Definition used (quoted from claim/CLAIM.md)
"an assignment of each operation to an eligible (machine, worker) pair with start times such that an independent checker
written from the repository's instance format confirms job precedence, machine and worker no-overlap and the pair-specific
durations, and computes a makespan strictly below that instance's UB"
Schedule format (CLAIM.md): "{"ops": [[job, op, machine, worker, start], ...]}, all 1-based; op is the position inside its job".

## Method
1. Wrote my own checker BEFORE opening claim/fjsspw_check.py. It parses each .fjs as one integer token stream
   (header `jobs machines workers`; per job n_ops; per op n_machines; per machine `m n_workers (w d)*`), asserts the whole
   file is consumed exactly, ids in range, no conflicting duplicate pairs. Per schedule it asserts: only key "ops";
   every row is 5 ints; each (job,op) exists and appears exactly once; all ops present; start >= 0; (machine,worker)
   eligible, duration = that pair's duration; start(op k+1) >= end(op k); no overlap on any machine or any worker
   (sorted intervals, next start >= previous end); makespan = max end. It then compares with the CLAIM.md table row,
   claim/name_map.csv row, and round(UB) from claim/best_known.csv, requiring makespan == claimed and makespan <= round(UB)-1.
2. Mutation sanity test of my checker on Behnke1: moving a start earlier, dropping an op, and an ineligible worker were all rejected.
3. Ran it on ALL 95 schedules (not a sample), twice; outputs byte-identical (deterministic).
4. Then ran the author's claim/fjsspw_check.py on all 95 and diffed makespans against mine.
5. `shasum -a 256 -c claim/SHA256SUMS`; compared the file list against the SHA256SUMS list; checked every instance name is a `source` in claim/data.csv.

## Results (real outputs)
- My checker: `claim rows 95 instances 95 schedules 95 names match True` ... `PASS 95/95`; run 2 identical (`deterministic`).
- Author checker: `author non-valid: 0  valid: 95`; diff of makespans vs mine: `author == mine on all 95`.
- SHA256SUMS: `sha OK: 196 notOK: 0`; files on disk vs listed: 0 differences.
- best_known.csv sha256 74f982d5fdbdd7ebf6b889b0a57106474f9dd677a3813cf5762fc54afdfe30cf, data.csv sha256
  93debe7be69d1e6c700ca3f6c14aacd5bfa69a11648daa7c64e8034679c1d67f; both match CLAIM.md.
- All 95 instance names appear as `source` in data.csv; every name_map.csv row equals the CLAIM.md table row.
- Margin round(UB) - makespan: min 1, max 171. All 95 are <= round(UB) - 1.
- Not checked: live re-fetch of best_known.csv (the brief scopes me to the claim/ folder). The saved copy's hash matches CLAIM.md.
- Note: the shared scratchpad was overwritten by another process during my first pass, so I re-ran everything from scratch in a
  private subdirectory. All numbers here come from that clean re-run. This was an environment issue, not a problem with the claim.

## Per-instance table (my checker; ms = recomputed makespan)
| instance file | best_known row | ms | claimed | round(UB) | margin | status |
|---|---|---|---|---|---|---|
| Behnke1.fjs | behnkegeiger1 | 83 | 83 | 85 | 2 | OK |
| Behnke2.fjs | behnkegeiger2 | 85 | 85 | 86 | 1 | OK |
| Behnke4.fjs | behnkegeiger4 | 88 | 88 | 90 | 2 | OK |
| Behnke5.fjs | behnkegeiger5 | 84 | 84 | 85 | 1 | OK |
| BrandimarteMk4.fjs | brandimarte4 | 55 | 55 | 56 | 1 | OK |
| ChambersBarnes1.fjs | chambersbarnes1 | 863 | 863 | 880 | 17 | OK |
| ChambersBarnes10.fjs | chambersbarnes10 | 855 | 855 | 893 | 38 | OK |
| ChambersBarnes11.fjs | chambersbarnes11 | 846 | 846 | 871 | 25 | OK |
| ChambersBarnes12.fjs | chambersbarnes12 | 853 | 853 | 859 | 6 | OK |
| ChambersBarnes13.fjs | chambersbarnes13 | 864 | 864 | 890 | 26 | OK |
| ChambersBarnes14.fjs | chambersbarnes14 | 848 | 848 | 874 | 26 | OK |
| ChambersBarnes2.fjs | chambersbarnes2 | 852 | 852 | 860 | 8 | OK |
| ChambersBarnes3.fjs | chambersbarnes3 | 857 | 857 | 863 | 6 | OK |
| ChambersBarnes5.fjs | chambersbarnes5 | 789 | 789 | 805 | 16 | OK |
| ChambersBarnes6.fjs | chambersbarnes6 | 863 | 863 | 888 | 25 | OK |
| ChambersBarnes7.fjs | chambersbarnes7 | 840 | 840 | 846 | 6 | OK |
| ChambersBarnes8.fjs | chambersbarnes8 | 875 | 875 | 896 | 21 | OK |
| ChambersBarnes9.fjs | chambersbarnes9 | 860 | 860 | 892 | 32 | OK |
| Fattahi19.fjs | fattahi19 | 994 | 994 | 1024 | 30 | OK |
| Hurinkedata10.fjs | hurinkedata10 | 738 | 738 | 741 | 3 | OK |
| Hurinkedata11.fjs | hurinkedata11 | 813 | 813 | 817 | 4 | OK |
| Hurinkedata12.fjs | hurinkedata12 | 851 | 851 | 855 | 4 | OK |
| Hurinkedata17.fjs | hurinkedata17 | 1071 | 1071 | 1077 | 6 | OK |
| Hurinkedata2.fjs | hurinkedata2 | 812 | 812 | 825 | 13 | OK |
| Hurinkedata25.fjs | hurinkedata25 | 819 | 819 | 850 | 31 | OK |
| Hurinkedata26.fjs | hurinkedata26 | 937 | 937 | 942 | 5 | OK |
| Hurinkedata44.fjs | hurinkedata44 | 1086 | 1086 | 1117 | 31 | OK |
| Hurinkedata45.fjs | hurinkedata45 | 862 | 862 | 884 | 22 | OK |
| Hurinkedata49.fjs | hurinkedata49 | 5956 | 5956 | 6007 | 51 | OK |
| Hurinkedata50.fjs | hurinkedata50 | 6067 | 6067 | 6223 | 156 | OK |
| Hurinkedata51.fjs | hurinkedata51 | 6494 | 6494 | 6524 | 30 | OK |
| Hurinkedata57.fjs | hurinkedata57 | 916 | 916 | 924 | 8 | OK |
| Hurinkedata58.fjs | hurinkedata58 | 810 | 810 | 826 | 16 | OK |
| Hurinkedata59.fjs | hurinkedata59 | 889 | 889 | 910 | 21 | OK |
| Hurinkedata6.fjs | hurinkedata6 | 537 | 537 | 541 | 4 | OK |
| Hurinkedata60.fjs | hurinkedata60 | 917 | 917 | 948 | 31 | OK |
| Hurinkedata61.fjs | hurinkedata61 | 794 | 794 | 812 | 18 | OK |
| Hurinkedata62.fjs | hurinkedata62 | 897 | 897 | 916 | 19 | OK |
| Hurinkedata63.fjs | hurinkedata63 | 364 | 364 | 366 | 2 | OK |
| Hurinkedata64.fjs | hurinkedata64 | 825 | 825 | 832 | 7 | OK |
| Hurinkedata65.fjs | hurinkedata65 | 875 | 875 | 885 | 10 | OK |
| Hurinkedata66.fjs | hurinkedata66 | 864 | 864 | 893 | 29 | OK |
| Hurinkrdata2.fjs | hurinkrdata2 | 640 | 640 | 651 | 11 | OK |
| Hurinkrdata20.fjs | hurinkrdata20 | 592 | 592 | 593 | 1 | OK |
| Hurinkrdata21.fjs | hurinkrdata21 | 618 | 618 | 624 | 6 | OK |
| Hurinkrdata22.fjs | hurinkrdata22 | 649 | 649 | 663 | 14 | OK |
| Hurinkrdata23.fjs | hurinkrdata23 | 706 | 706 | 709 | 3 | OK |
| Hurinkrdata49.fjs | hurinkrdata49 | 4840 | 4840 | 4857 | 17 | OK |
| Hurinkrdata50.fjs | hurinkrdata50 | 5684 | 5684 | 5701 | 17 | OK |
| Hurinkrdata51.fjs | hurinkrdata51 | 5408 | 5408 | 5426 | 18 | OK |
| Hurinkrdata53.fjs | hurinkrdata53 | 5410 | 5410 | 5581 | 171 | OK |
| Hurinkrdata54.fjs | hurinkrdata54 | 5859 | 5859 | 5895 | 36 | OK |
| Hurinkrdata56.fjs | hurinkrdata56 | 5350 | 5350 | 5423 | 73 | OK |
| Hurinkrdata57.fjs | hurinkrdata57 | 704 | 704 | 722 | 18 | OK |
| Hurinkrdata59.fjs | hurinkrdata59 | 664 | 664 | 671 | 7 | OK |
| Hurinkrdata60.fjs | hurinkrdata60 | 692 | 692 | 702 | 10 | OK |
| Hurinkrdata62.fjs | hurinkrdata62 | 704 | 704 | 710 | 6 | OK |
| Hurinkrdata63.fjs | hurinkrdata63 | 281 | 281 | 289 | 8 | OK |
| Hurinkrdata64.fjs | hurinkrdata64 | 590 | 590 | 595 | 5 | OK |
| Hurinkrdata65.fjs | hurinkrdata65 | 657 | 657 | 660 | 3 | OK |
| Hurinkrdata66.fjs | hurinkrdata66 | 701 | 701 | 712 | 11 | OK |
| Hurinkrdata8.fjs | hurinkrdata8 | 438 | 438 | 444 | 6 | OK |
| Hurinksdata19.fjs | hurinksdata19 | 883 | 883 | 907 | 24 | OK |
| Hurinksdata2.fjs | hurinksdata2 | 870 | 870 | 894 | 24 | OK |
| Hurinksdata22.fjs | hurinksdata22 | 793 | 793 | 800 | 7 | OK |
| Hurinksdata23.fjs | hurinksdata23 | 842 | 842 | 847 | 5 | OK |
| Hurinksdata24.fjs | hurinksdata24 | 1000 | 1000 | 1031 | 31 | OK |
| Hurinksdata25.fjs | hurinksdata25 | 861 | 861 | 869 | 8 | OK |
| Hurinksdata27.fjs | hurinksdata27 | 904 | 904 | 924 | 20 | OK |
| Hurinksdata28.fjs | hurinksdata28 | 908 | 908 | 909 | 1 | OK |
| Hurinksdata44.fjs | hurinksdata44 | 1132 | 1132 | 1135 | 3 | OK |
| Hurinksdata45.fjs | hurinksdata45 | 874 | 874 | 886 | 12 | OK |
| Hurinksdata51.fjs | hurinksdata51 | 7043 | 7043 | 7141 | 98 | OK |
| Hurinksdata53.fjs | hurinksdata53 | 7337 | 7337 | 7376 | 39 | OK |
| Hurinksdata55.fjs | hurinksdata55 | 6174 | 6174 | 6244 | 70 | OK |
| Hurinksdata56.fjs | hurinksdata56 | 7895 | 7895 | 7916 | 21 | OK |
| Hurinksdata57.fjs | hurinksdata57 | 1000 | 1000 | 1033 | 33 | OK |
| Hurinksdata58.fjs | hurinksdata58 | 822 | 822 | 837 | 15 | OK |
| Hurinksdata59.fjs | hurinksdata59 | 954 | 954 | 976 | 22 | OK |
| Hurinksdata6.fjs | hurinksdata6 | 573 | 573 | 574 | 1 | OK |
| Hurinksdata60.fjs | hurinksdata60 | 935 | 935 | 960 | 25 | OK |
| Hurinksdata61.fjs | hurinksdata61 | 826 | 826 | 832 | 6 | OK |
| Hurinksdata62.fjs | hurinksdata62 | 939 | 939 | 951 | 12 | OK |
| Hurinksdata63.fjs | hurinksdata63 | 373 | 373 | 386 | 13 | OK |
| Hurinksdata64.fjs | hurinksdata64 | 842 | 842 | 855 | 13 | OK |
| Hurinksdata65.fjs | hurinksdata65 | 874 | 874 | 882 | 8 | OK |
| Hurinksdata66.fjs | hurinksdata66 | 874 | 874 | 877 | 3 | OK |
| Hurinkvdata4.fjs | hurinkvdata4 | 546 | 546 | 549 | 3 | OK |
| Hurinkvdata50.fjs | hurinkvdata50 | 5608 | 5608 | 5612 | 4 | OK |
| Hurinkvdata51.fjs | hurinkvdata51 | 5406 | 5406 | 5474 | 68 | OK |
| Hurinkvdata56.fjs | hurinkvdata56 | 4223 | 4223 | 4264 | 41 | OK |
| Hurinkvdata58.fjs | hurinkvdata58 | 560 | 560 | 565 | 5 | OK |
| Hurinkvdata6.fjs | hurinkvdata6 | 456 | 456 | 458 | 2 | OK |
| Hurinkvdata7.fjs | hurinkvdata7 | 480 | 480 | 486 | 6 | OK |
| Hurinkvdata8.fjs | hurinkvdata8 | 437 | 437 | 439 | 2 | OK |

## Verdict
95/95 schedules valid per my independent checker and the author's checker. Every makespan matches CLAIM.md exactly and is strictly below round(UB). Hashes match and runs are deterministic.

pass: true
